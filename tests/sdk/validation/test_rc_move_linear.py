# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_move_linear
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    MoveLinearAbsolute against the SDK: execution, buffering, sequences, faults.
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

"""MoveLinearAbsolute against the SDK: execution, buffering, sequences, faults.

Behaviour of the robot controller (SDK simulator) for MoveLinearAbsolute (spec 6.3.2): output flag
sequence, motion, Progress / RemainingDistance, AbortingMode, interrupt / continue / stop, disabling
the robot, primary and secondary sequence and motion faults during the movement.
"""

from __future__ import annotations

import itertools
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import AbortingMode, RaSequenceState, RobotLibraryErrorIdEnum, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    MOVE_CYCLES,
    cartesian,
    enable,
    execute,
    fb,
    finished,
    order,
    state,
    watch,
)

MOVE_LINEAR = 2103  # command type MoveLinearAbsolute


def _move_linear(h: RobotTaskHarness, x: float, y: float = 0.0, z: float = 0.0, **inputs: Any) -> Any:
    """MoveLinearAbsolute to (x, y, z) with 100 % velocity / acceleration; ``inputs`` are block inputs
    (AbortingMode, SequenceFlag) or ParCmd fields."""
    mv = fb(h, "MC_MoveLinearAbsoluteFB")
    cartesian(mv, x, y, z)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    for name, value in inputs.items():
        setattr(mv if name in ("AbortingMode", "SequenceFlag") else mv.ParCmd, name, value)
    return mv


def _arm(h: RobotTaskHarness) -> Any:
    """Status of the robot arm (RobotData of the axes group)."""
    return h.ag.State.StatusRobotArm


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    seen = execute(h, seq)
    assert seen.final["Done"] and not seen.final["Error"], seen.final


def _group(h: RobotTaskHarness, name: str) -> None:
    """Execute a group command (GroupInterrupt / GroupContinue / GroupStop) and expect Done."""
    seen = execute(h, fb(h, name))
    assert seen.final["Done"] and not seen.final["Error"], (name, seen.final)


# ---------------------------------------------------------------- basic execution


def test_reaches_target_with_progress(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A valid MoveLinearAbsolute with Execute held runs Busy, CommandBuffered, Active, Done and reaches the target.

    Done stays TRUE while Execute is TRUE and is reset with the falling edge. Progress rises to
    100 %; RemainingDistance is either supported (>= 0) or reported as not available (-1)."""
    enable(robot)
    mv = _move_linear(robot, 100.0, 20.0, -10.0)
    mv.Execute = True
    progress: list[float] = []
    seen = watch(robot, [mv], 300, lambda: progress.append(mv.OutCmd.Progress) or finished(mv))[0]
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert not mv.Error and mv.ErrorID == 0
    assert sdk.joints[:3] == pytest.approx([100.0, 20.0, -10.0])
    assert all(0.0 <= p <= 100.0 for p in progress) and progress == sorted(progress)
    assert mv.OutCmd.Progress == pytest.approx(100.0)
    assert mv.OutCmd.RemainingDistance == -1.0 or mv.OutCmd.RemainingDistance >= 0.0
    robot.run(10)
    assert mv.Done, state(mv)
    mv.Execute = False
    robot.run(2)
    assert not mv.Done and not mv.Busy and not mv.CommandBuffered, state(mv)


def test_robot_not_enabled_no_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """With the robot not enabled a MoveLinearAbsolute is buffered but neither becomes active nor moves the robot.

    Whether CommandInterrupted must also be set in this situation is an open question; the
    simulator keeps the command only buffered."""
    assert not sdk.enabled
    mv = _move_linear(robot, 50.0)
    mv.Execute = True
    seen = watch(robot, [mv], 100, lambda: finished(mv))[0]
    assert order(seen, "Busy", "CommandBuffered"), seen.flags
    assert "Active" not in seen.flags and not finished(mv), state(mv)
    assert sdk.joints[0] == 0.0


# ---------------------------------------------------------------- new rising edge while busy


def test_second_edge_while_active_same_target(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A new rising edge on Execute while the motion is active does not start a second command; the first motion ends with Done."""
    enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Active))
    robot.run(5)
    mv.Execute = False
    robot.run(1)
    mv.Execute = True
    seen = watch(robot, [mv], 300, lambda: finished(mv))[0]
    assert mv.Done and not mv.Error, state(mv)
    assert "CommandAborted" not in seen.flags
    assert sdk.joints[0] == pytest.approx(100.0)
    assert sdk.last_command(MOVE_LINEAR)["ParSeq"] == "1"  # sent once, no update


def test_many_edges_while_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Fifty rising edges on Execute while the motion is active neither fill a buffer nor raise an error; the motion ends with Done."""
    sdk.set_move_cycles(8 * MOVE_CYCLES)
    enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Active))
    for _ in range(50):
        mv.Execute = False
        robot.run(1)
        mv.Execute = True
        robot.run(1)
        assert mv.Busy and not mv.Error, state(mv)
    robot.run(1000, until=lambda: finished(mv))
    assert mv.Done and not mv.Error, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)
    assert sdk.last_command(MOVE_LINEAR)["ParSeq"] == "1"  # sent once, no update


def test_second_edge_with_new_target_is_ignored(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A changed target together with a new rising edge while the motion is active is ignored; the robot ends at the first target."""
    enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Active))
    robot.run(5)
    mv.Execute = False
    mv.ParCmd.Position.Y = 40.0
    robot.run(1)
    mv.Execute = True
    robot.run(300, until=lambda: finished(mv))
    assert mv.Done and not mv.Error, state(mv)
    assert sdk.joints[:2] == pytest.approx([100.0, 0.0])


# ---------------------------------------------------------------- motion faults


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: a motion fault of the firmware (16#6C01 collision, 16#6C03 not reachable, 16#6C04 "
    "software limit) is only logged as an alarm; the SDK puts the active command back to BUFFERED, the "
    "block stays Busy without Error / CommandInterrupted (spec 6.3.2 outputs, 5.5.x error handling). "
    "Software limits, reachability and singularities are not simulated; the fault is injected.",
)
@pytest.mark.parametrize(
    "code", [0x6C04, 0x6C03, 0x6C01], ids=["software-limit", "not-reachable", "collision"]
)
def test_motion_fault_during_motion(robot: RobotTaskHarness, sdk: SdkSimulator, code: int) -> None:
    """A motion fault during the movement stops the robot before the target and ends the command with Error or CommandInterrupted."""
    enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 10.0)
    sdk.set_motion_error(code)
    seen = watch(robot, [mv], 100, lambda: bool(mv.Error or mv.CommandInterrupted))[0]
    assert sdk.joints[0] < 100.0
    assert "Active" in seen.flags
    assert mv.Error or mv.CommandInterrupted, state(mv)
    assert not mv.Done


# ---------------------------------------------------------------- AbortingMode


def test_aborting_command_discards_buffered(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Four commands, the third with AbortingMode ABORT: the active and the buffered command are aborted, the
    third and fourth end with Done.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    modes = [AbortingMode.BUFFER, AbortingMode.BUFFER, AbortingMode.ABORT, AbortingMode.BUFFER]
    moves = [_move_linear(robot, 10.0 * (i + 1), AbortingMode=m) for i, m in enumerate(modes)]
    moves[0].Execute = True
    robot.run(100, until=lambda: bool(moves[0].Active))
    for mv in moves[1:]:
        mv.Execute = True
    seen = watch(robot, moves, 1000, lambda: all(finished(m) for m in moves))
    assert order(seen[0], "Busy", "CommandBuffered", "Active", "CommandAborted"), seen[0].flags
    assert moves[1].CommandAborted and "Active" not in seen[1].flags, seen[1].flags
    for s in seen[2:]:
        assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(40.0)


def test_aborting_commands_in_a_row(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Three commands with AbortingMode ABORT started after the first one is active: the first two are
    aborted, the last one ends with Done.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    moves = [_move_linear(robot, 10.0 * (i + 1), AbortingMode=AbortingMode.ABORT) for i in range(3)]
    moves[0].Execute = True
    robot.run(100, until=lambda: bool(moves[0].Active))
    moves[1].Execute = True
    robot.run(100, until=lambda: bool(moves[1].Active))
    moves[2].Execute = True
    seen = watch(robot, moves, 1000, lambda: all(finished(m) for m in moves))
    assert moves[0].CommandAborted and moves[1].CommandAborted, [state(m) for m in moves]
    assert order(seen[2], "Busy", "CommandBuffered", "Active", "Done"), seen[2].flags
    assert sdk.joints[0] == pytest.approx(30.0)


# ---------------------------------------------------------------- interrupt / continue / stop / disable


def test_interrupt_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt during the motion resets Active and sets CommandInterrupted; after GroupContinue the
    motion ends with Done at the target.
    """
    enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 10.0)
    _group(robot, "MC_GroupInterruptFB")
    robot.run(5)
    assert mv.CommandInterrupted and not mv.Active and mv.Busy, state(mv)
    stopped = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == stopped < 100.0
    _group(robot, "MC_GroupContinueFB")
    robot.run(300, until=lambda: finished(mv))
    assert mv.Done and not mv.CommandInterrupted, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)


def test_interrupt_and_stop(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop after GroupInterrupt ends the interrupted motion with CommandAborted; the robot stays where it stopped."""
    enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    seen = watch(robot, [mv], 100, lambda: sdk.joints[0] > 10.0)[0]
    _group(robot, "MC_GroupInterruptFB")
    stop = fb(robot, "MC_GroupStopFB")
    assert execute(robot, stop, reset=False).final["Done"]
    robot.run(50, until=lambda: finished(mv))
    seen.record()
    assert order(seen, "Busy", "CommandBuffered", "Active", "CommandAborted"), seen.flags
    assert not mv.Done and sdk.joints[0] < 100.0


def test_disable_during_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Disabling the robot during the motion resets Active and sets CommandInterrupted; the command stays buffered."""
    en = enable(robot)
    mv = _move_linear(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 10.0)
    en.Enable = False
    seen = watch(robot, [mv], 100, lambda: not sdk.enabled and bool(mv.CommandInterrupted))[0]
    robot.run(10)
    assert order(seen, "Busy", "CommandBuffered", "Active", "CommandInterrupted"), seen.flags
    assert mv.CommandInterrupted and mv.CommandBuffered and not mv.Active and not finished(mv), state(mv)
    assert sdk.joints[0] < 100.0


def test_start_while_interrupted(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A MoveLinearAbsolute started while the robot is enabled and interrupted is buffered and does not move;
    after GroupContinue it ends with Done.

    Whether CommandInterrupted must also be set for the not yet started command is an open
    question; the SDK only reports it as buffered."""
    enable(robot)
    _group(robot, "MC_GroupInterruptFB")
    assert _arm(robot).RaSequenceState == RaSequenceState.INTERRUPTED
    mv = _move_linear(robot, 50.0)
    mv.Execute = True
    seen = watch(robot, [mv], 50, lambda: finished(mv))[0]
    assert order(seen, "Busy", "CommandBuffered"), seen.flags
    assert "Active" not in seen.flags and sdk.joints[0] == 0.0
    _group(robot, "MC_GroupContinueFB")
    robot.run(300, until=lambda: finished(mv))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(50.0)


# ---------------------------------------------------------------- sequences


def test_primary_sequence_flag(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """With SequenceFlag PRIMARY the command runs in the primary sequence to Done; the secondary sequence stays inactive."""
    enable(robot)
    mv = _move_linear(robot, 50.0, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert not _arm(robot).SecondarySequenceActive
    assert sdk.joints[0] == pytest.approx(50.0)


def test_primary_command_waits_while_secondary_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A primary command started while the secondary sequence is active is buffered without motion; after
    returning to the primary sequence and GroupContinue it ends with Done.
    """
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    assert _arm(robot).SecondarySequenceActive
    mv = _move_linear(robot, 100.0, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    mv.Execute = True
    seen = watch(robot, [mv], 60, lambda: finished(mv))[0]
    assert order(seen, "Busy", "CommandBuffered"), seen.flags
    assert "Active" not in seen.flags and sdk.joints[0] == 0.0
    _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    assert not _arm(robot).SecondarySequenceActive
    robot.run(20)
    assert not mv.Active and sdk.joints[0] == 0.0, state(mv)
    _group(robot, "MC_GroupContinueFB")
    robot.run(300, until=lambda: finished(mv))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)


def test_secondary_command_in_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After switching to the secondary sequence and GroupContinue a command with SequenceFlag SECONDARY runs to Done."""
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    _group(robot, "MC_GroupContinueFB")
    mv = _move_linear(robot, 100.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert _arm(robot).SecondarySequenceActive
    assert sdk.joints[0] == pytest.approx(100.0)


def _change_sequence_during_motion(h: RobotTaskHarness) -> tuple[Any, Any]:
    """Two primary commands, switch to the secondary sequence while the first one is active (the
    primary sequence is interrupted) and back to the primary sequence."""
    first = _move_linear(h, 50.0, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    second = _move_linear(h, 80.0, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    first.Execute = second.Execute = True
    h.run(100, until=lambda: bool(first.Active))
    _set_sequence(h, SequenceFlag.SECONDARY_SEQUENCE)
    assert _arm(h).RaSequenceState == RaSequenceState.INTERRUPTED
    assert first.CommandInterrupted, state(first)
    _set_sequence(h, SequenceFlag.PRIMARY_SEQUENCE)
    assert not _arm(h).SecondarySequenceActive
    return first, second


def test_change_sequence_during_motion_then_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Switching to the secondary sequence during a primary motion interrupts it; back in the primary sequence
    GroupContinue finishes both primary commands.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    first, second = _change_sequence_during_motion(robot)
    _group(robot, "MC_GroupContinueFB")
    seen = watch(robot, [first, second], 600, lambda: finished(first) and finished(second))
    assert first.Done and second.Done, (state(first), state(second))
    assert order(seen[1], "CommandBuffered", "Active", "Done"), seen[1].flags
    assert sdk.joints[0] == pytest.approx(80.0)
    assert not _arm(robot).SecondarySequenceActive


def test_secondary_commands_after_return_to_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Secondary commands started after the return to the primary sequence end with Error
    ERR_SECONDARY_SEQUENCE_NOT_ACTIVE; the primary commands finish after GroupContinue.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    first, second = _change_sequence_during_motion(robot)
    extra = [
        _move_linear(robot, 10.0 * i, 10.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE) for i in (1, 2)
    ]
    for mv in extra:
        mv.Execute = True
    seen = watch(robot, extra, 50, lambda: all(finished(m) for m in extra))
    for mv, s in zip(extra, seen, strict=True):
        assert mv.Error and mv.ErrorID == RobotLibraryErrorIdEnum.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE, state(mv)
        assert "Active" not in s.flags
    _group(robot, "MC_GroupContinueFB")
    robot.run(600, until=lambda: finished(first) and finished(second))
    assert first.Done and second.Done, (state(first), state(second))
    assert sdk.joints[:2] == pytest.approx([80.0, 0.0])


def test_secondary_flag_without_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A command with SequenceFlag SECONDARY while the primary sequence is active ends with Error
    ERR_SECONDARY_SEQUENCE_NOT_ACTIVE (16#8F16) without motion.
    """
    enable(robot)
    mv = _move_linear(robot, 100.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    seen = execute(robot, mv)
    assert order(seen, "Busy", "Error"), seen.flags
    assert seen.final["ErrorID"] == RobotLibraryErrorIdEnum.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE
    assert "Active" not in seen.flags and sdk.joints[0] == 0.0


# ---------------------------------------------------------------- many short commands


@pytest.mark.parametrize("blending", [False, True], ids=["exact-stop", "corner-distance"])
def test_ten_short_commands_buffered(robot: RobotTaskHarness, sdk: SdkSimulator, blending: bool) -> None:
    """Ten short MoveLinearAbsolute commands, each started when the previous one is buffered, all end with
    Done in order; each one gets Active only after its predecessor is Done.
    """
    from srci.types import BlendingMode

    sdk.set_move_cycles(10)
    enable(robot)
    extra: dict[str, Any] = (
        {"BlendingMode": BlendingMode.CORNER_DISTANCE, "BlendingParameter": [10.0, 0.0]} if blending else {}
    )
    moves = [_move_linear(robot, 20.0 * (i + 1), **extra) for i in range(10)]
    for i, mv in enumerate(moves):
        mv.Execute = True
        if i < len(moves) - 1:
            robot.run(50, until=lambda mv=mv: bool(mv.CommandBuffered or mv.Error))
    active_while_previous_busy = []

    def step() -> bool:
        for prev, nxt in itertools.pairwise(moves):
            if nxt.Active and not prev.Done:
                active_while_previous_busy.append(moves.index(nxt))
        return all(finished(m) for m in moves)

    robot.run(2000, until=step)
    assert all(m.Done and not m.Error for m in moves), [state(m) for m in moves]
    assert not active_while_previous_busy
    assert sdk.joints[0] == pytest.approx(200.0)
