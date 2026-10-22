# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_sequences
#  Author:      Thorsten Brach
#  Date:        2026-10-22
#
#  Description:
#    Sequences, edges and the speed override against the SRCI SDK.
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Sequences, edges and the speed override against the SRCI SDK (SDK-SEQ).

* data command in the secondary sequence: rejected by the RC while the primary sequence is
  active, executed after SetSequence(SECONDARY)
* a second rising edge while the block is Busy sends no second command
* several commands started in the same PLC cycle all finish
* speed override 0 % holds a motion (the block stays Busy), raising it lets the motion finish;
  the override can be changed while a motion runs (parallel command)

For the override tests the simulated robot of the SDK harness scales the motion with the speed
override (``set_override_motion``; the SDK starts with 5 %, so the tests set 100 % first).
"""

from __future__ import annotations

from typing import Any

from srci_sdk_sim.sdk import SdkSimulator

from srci.types import ProcessingMode, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import MOVE_CYCLES, enable, execute, fb, move_axes, robot, sdk_parameters, state

__all__ = ["robot", "sdk_parameters"]  # fixtures

# RC error: command for the secondary sequence while the primary sequence is active
RC_SECONDARY_WHILE_PRIMARY = 0x8F16

MOVE_AXES_ABSOLUTE = 2101  # CmdType (SDK log)


def accepted(sdk: SdkSimulator, cmd_type: int, start_log: int) -> int:
    """Commands of ``cmd_type`` the SDK accepted since log entry ``start_log``."""
    return sum(
        1
        for log in sdk.logs[start_log:]
        if f"({cmd_type}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def tool_data(h: RobotTaskHarness, tool_no: int, x: float, **inputs: Any) -> Any:
    wr = fb(h, "MC_WriteToolDataFB", **inputs)
    wr.ParCmd.ToolNo = tool_no
    wr.ParCmd.ToolData.X = x
    wr.ParCmd.ToolData.LoadNo = 1
    return wr


def set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    execute(h, seq)


def scaled(h: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Motion scaled with the override, override 100 %, robot enabled."""
    sdk.set_override_motion(True)
    enable(h, sdk)
    execute(h, override(h, 100.0))


def override(h: RobotTaskHarness, value: float) -> Any:
    ov = fb(h, "MC_ChangeSpeedOverrideFB")
    ov.ParCmd.Override = value
    return ov


# ---------------------------------------------------------------- sequences


def test_secondary_data_command_while_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A data command for the secondary sequence while the primary one is active: the RC rejects
    it, the block reports the error of the RC."""
    enable(robot, sdk)
    wr = tool_data(
        robot, 3, 1.0, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE
    )
    wr.Execute = True
    robot.run(100, until=lambda: bool(wr.Done or wr.Error))
    assert wr.Error and wr.ErrorID == RC_SECONDARY_WHILE_PRIMARY, state(wr)


def test_secondary_data_command(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After SetSequence(SECONDARY) a buffered data command of the secondary sequence is executed;
    the value can be read back after the return to the primary sequence."""
    enable(robot, sdk)
    set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    wr = tool_data(
        robot, 3, 42.5, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE
    )
    execute(robot, wr)
    set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    rd = fb(robot, "MC_ReadToolDataFB")
    rd.ParCmd.ToolNo = 3
    execute(robot, rd, reset=False)
    assert rd.OutCmd.ToolData.X == 42.5


def test_primary_data_command(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A buffered data command of the primary sequence (not parallel) is executed."""
    enable(robot, sdk)
    wr = tool_data(
        robot, 4, 7.0, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE
    )
    execute(robot, wr)


def test_sequence_flag_invalid_for_parallel(robot: RobotTaskHarness) -> None:
    """A parallel command must not name a sequence (and a buffered one must name one): the block
    rejects the combination before sending."""
    for mode, flag in (
        (ProcessingMode.PARALLEL, SequenceFlag.PRIMARY_SEQUENCE),
        (ProcessingMode.BUFFERED, SequenceFlag.NO_SEQUENCE),
    ):
        wr = tool_data(robot, 3, 1.0, ProcessingMode=mode, SequenceFlag=flag, Execute=True)
        robot.run(10, until=lambda: bool(wr.Error))  # noqa: B023
        assert wr.Error and wr.ErrorID == 0x8625, (mode, flag, state(wr))


# ---------------------------------------------------------------- edges


def test_second_edge_while_busy(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A second rising edge on Execute while the motion runs: no second command, the block stays
    Busy and finishes the first motion."""
    sdk.set_move_cycles(100)
    enable(robot, sdk)
    start_log = len(sdk.logs)
    mv = move_axes(robot, 20.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 2.0)
    assert mv.Busy
    mv.Execute = False
    robot.run(2)
    mv.Execute = True
    robot.run(2)
    assert mv.Busy and not mv.Error, state(mv)
    robot.run(300, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert accepted(sdk, MOVE_AXES_ABSOLUTE, start_log) == 1
    robot.run(MOVE_CYCLES * 2)
    assert accepted(sdk, MOVE_AXES_ABSOLUTE, start_log) == 1


def test_several_commands_in_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Commands started in the same PLC cycle: all finish (they share the telegram)."""
    enable(robot, sdk)
    blocks = [
        fb(robot, "MC_ReadRobotDataFB"),
        fb(robot, "MC_ReadActualPositionFB"),
        override(robot, 80.0),
        tool_data(robot, 5, 3.0),
        move_axes(robot, 10.0),
    ]
    for block in blocks:
        block.Execute = True
    robot.run(200, until=lambda: all(b.Done or b.Error for b in blocks))
    assert all(b.Done and not b.Error for b in blocks), [state(b) for b in blocks]
    assert sdk.override == 80.0 and sdk.joints[0] == 10.0


def test_interrupt_and_override_in_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt and ChangeSpeedOverride in the same cycle while a motion runs; GroupContinue
    afterwards finishes the motion."""
    sdk.set_move_cycles(200)
    enable(robot, sdk)
    mv = move_axes(robot, 50.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 5.0)
    gi = fb(robot, "MC_GroupInterruptFB")
    ov = override(robot, 50.0)
    gi.Execute = ov.Execute = True
    robot.run(100, until=lambda: bool((gi.Done or gi.Error) and (ov.Done or ov.Error)))
    assert gi.Done and ov.Done, (state(gi), state(ov))
    held = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == held and mv.Busy
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(600, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert sdk.override == 50.0


# ---------------------------------------------------------------- override


def test_override_during_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ChangeSpeedOverride is a parallel command: accepted while a motion runs, the motion
    continues (regression of the HMI: the override was blocked by the running program)."""
    sdk.set_move_cycles(100)
    scaled(robot, sdk)
    mv = move_axes(robot, 40.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 4.0)
    for value in (30.0, 100.0):
        execute(robot, override(robot, value))
        assert sdk.override == value
        assert mv.Busy and not mv.Error, state(mv)
    robot.run(300, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == 40.0


def test_override_zero_holds_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Override 0 %: the motion stands still and the block stays Busy (no Done, no error, not
    aborted); 100 % lets it finish."""
    sdk.set_move_cycles(100)
    scaled(robot, sdk)
    mv = move_axes(robot, 40.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 4.0)
    execute(robot, override(robot, 0.0))
    held = sdk.joints[0]
    robot.run(200)
    assert sdk.joints[0] == held
    assert mv.Busy and not (mv.Done or mv.Error or mv.CommandAborted), state(mv)
    execute(robot, override(robot, 100.0))
    robot.run(300, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == 40.0


def test_override_half_speed(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Override 50 %: the same motion takes about twice as many cycles."""
    scaled(robot, sdk)
    full = execute(robot, move_axes(robot, 10.0))
    execute(robot, override(robot, 50.0))
    half = execute(robot, move_axes(robot, 0.0), cycles=200)
    assert half >= 2 * MOVE_CYCLES - 2 and half > full + MOVE_CYCLES // 2, (full, half)


def test_override_out_of_range(robot: RobotTaskHarness) -> None:
    """Override above 100 %: rejected (block or RC), the override stays unchanged."""
    ov = override(robot, 150.0)
    ov.Execute = True
    robot.run(100, until=lambda: bool(ov.Done or ov.Error))
    assert ov.Error and not ov.Done, state(ov)
