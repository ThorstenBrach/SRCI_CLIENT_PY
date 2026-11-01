# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_move_direct
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    MoveDirectAbsolute against the SDK: execution, buffering, sequences, parameters.
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

"""MoveDirectAbsolute against the SDK: execution, buffering, sequences, parameters.

Behaviour of the robot controller (SDK simulator) for MoveDirectAbsolute (spec 6.3.3.3): output flag
sequence, motion, Progress, AbortingMode (5.5.9.1), interrupt / continue / stop, disabling the robot,
primary and secondary sequence (6.3.3.2, 5.5.3.4), dynamics rates, MoveTime, ToolNo / FrameNo,
arm configuration, TurnMode and software limits.

The simulated robot uses an identity kinematics and a fixed move duration: tool, frame, arm
configuration and dynamics rates have no visible effect on the motion, so those tests check that the
values reach the RC (decoded telegram of the SDK) and that the command completes.
Blending is in ``test_rc_move_direct_blending``.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import (
    AbortingMode,
    ArmConfigElbow,
    ArmConfigShoulder,
    ArmConfigWrist,
    CmdType,
    RobotLibraryErrorIdEnum,
    RobotLibraryInfoIdEnum,
    SequenceFlag,
    TurnMode,
)
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    MOVE_CYCLES,
    cartesian,
    enable,
    execute,
    fb,
    finished,
    order,
    read_position,
    state,
    watch,
)

E = RobotLibraryErrorIdEnum
INFO = RobotLibraryInfoIdEnum
MOVE_DIRECT = int(CmdType.MoveDirectAbsolute)  # 2102


def _move(h: RobotTaskHarness, x: float, y: float = 0.0, z: float = 0.0, **inputs: Any) -> Any:
    """MoveDirectAbsolute to (x, y, z) with 100 % velocity / acceleration (deceleration / jerk:
    default); ``inputs`` are block inputs (AbortingMode, SequenceFlag)."""
    mv = fb(h, "MC_MoveDirectAbsoluteFB", **inputs)
    cartesian(mv, x, y, z)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = -1.0
    mv.ParCmd.JerkRate = -1.0
    return mv


def _telegram(sdk: SdkSimulator) -> dict[str, str]:
    """Fields of the last MoveDirectAbsolute telegram as the SDK decoded them."""
    received = sdk.last_command(MOVE_DIRECT)
    assert received is not None, "no MoveDirectAbsolute telegram received"
    return received


def _accepted(sdk: SdkSimulator, since: int) -> int:
    """MoveDirectAbsolute commands the SDK accepted since log entry ``since``."""
    return sum(
        1
        for log in sdk.logs[since:]
        if f"({MOVE_DIRECT}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    s = execute(h, seq)
    assert s.final["Done"] and not s.final["Error"], s.final


def _group(h: RobotTaskHarness, name: str) -> None:
    """Run a group command (GroupInterrupt / GroupContinue / GroupStop) until Done."""
    g = fb(h, name)
    s = execute(h, g)
    assert s.final["Done"] and not s.final["Error"], (name, s.final)


def _secondary_active(h: RobotTaskHarness) -> bool:
    return bool(h.ag.State.StatusRobotArm.SecondarySequenceActive)


# ---------------------------------------------------------------- execution


def test_valid_move_reaches_the_target(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A valid MoveDirectAbsolute shows Busy, CommandBuffered, Active, Done and the robot reaches the target.

    Progress rises to 100 % while the command is active; RemainingDistance is either not provided by
    the RC (-1) or falls to 0. Done stays TRUE as long as Execute is held and is reset with Execute.
    """
    enable(robot)
    mv = _move(robot, 120.0, 40.0, -30.0, Name="TestName")
    mv.Execute = True
    progress: list[float] = []
    remaining: list[float] = []

    def step() -> bool:
        if mv.Active:
            progress.append(mv.OutCmd.Progress)
            remaining.append(mv.OutCmd.RemainingDistance)
        return finished(mv)

    s = watch(robot, [mv], 3 * MOVE_CYCLES, step)[0]
    assert mv.Done and not mv.Error, state(mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[:3] == pytest.approx([120.0, 40.0, -30.0])
    assert progress == sorted(progress) and mv.OutCmd.Progress == pytest.approx(100.0), progress
    assert all(r == -1.0 for r in remaining) or remaining == sorted(remaining, reverse=True), remaining
    robot.run(10)
    assert mv.Done, "Done is held while Execute is TRUE"
    mv.Execute = False
    robot.run(1)
    assert not mv.Done and not mv.Busy, state(mv)


def test_flag_sequence_of_a_valid_move(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveDirectAbsolute with default parameters runs through Busy, CommandBuffered, Active, Done in this order."""
    enable(robot)
    mv = _move(robot, 80.0)
    s = execute(robot, mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert "Error" not in s.flags and "CommandAborted" not in s.flags, s.flags
    assert sdk.joints[0] == pytest.approx(80.0)


def test_empty_position_moves_to_the_origin(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveDirectAbsolute with an empty (all zero) position completes and the robot ends at the origin.

    The simulated robot has no collision model: the zero position is reachable. A real robot may
    instead stop with a warning (not reachable / limits).
    """
    enable(robot)
    execute(robot, _move(robot, 50.0, 50.0, 50.0))
    mv = fb(robot, "MC_MoveDirectAbsoluteFB")
    mv.ParCmd.VelocityRate = 10.0
    mv.ParCmd.AccelerationRate = 10.0
    s = execute(robot, mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[:6] == pytest.approx([0.0] * 6)


def test_robot_not_enabled_command_waits(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Without power the command is buffered by the RC but neither becomes Active nor moves the robot.

    The RC may additionally report CommandInterrupted (sequence state "interrupt active").
    """
    mv = _move(robot, 100.0)
    mv.Execute = True
    s = watch(robot, [mv], 4 * MOVE_CYCLES, lambda: bool(mv.Error or mv.Done))[0]
    assert order(s, "Busy", "CommandBuffered"), s.flags
    assert mv.Busy and not mv.Active and not mv.Done and not mv.Error, state(mv)
    assert sdk.joints[0] == 0.0


# ---------------------------------------------------------------- AbortingMode (5.5.9.1)


def test_aborting_command_cancels_active_and_buffered(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A command with AbortingMode ABORT aborts the active and the buffered command; a later buffered command runs.

    Four commands: the first is active, the second is buffered, the third aborts both, the fourth is
    buffered behind the third.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    moves = [_move(robot, 100.0 * (i + 1), float(i)) for i in range(4)]
    moves[2].AbortingMode = AbortingMode.ABORT
    moves[0].Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(moves[0].Active))
    assert moves[0].Active, state(moves[0])
    for mv in moves[1:]:
        mv.Execute = True
    seen = watch(robot, moves, 8 * MOVE_CYCLES, lambda: all(finished(m) for m in moves))
    assert order(seen[0], "Busy", "CommandBuffered", "Active", "CommandAborted"), seen[0].flags
    assert "CommandAborted" in seen[1].flags and "Active" not in seen[1].flags, seen[1].flags
    for s in seen[2:]:
        assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[:2] == pytest.approx([400.0, 3.0])


def test_every_command_aborting(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Three commands with AbortingMode ABORT: the first two end with CommandAborted, the last one with Done."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    moves = [_move(robot, 100.0 * (i + 1), float(i), AbortingMode=AbortingMode.ABORT) for i in range(3)]
    moves[0].Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(moves[0].Active))
    moves[1].Execute = moves[2].Execute = True
    seen = watch(robot, moves, 6 * MOVE_CYCLES, lambda: all(finished(m) for m in moves))
    assert order(seen[0], "Busy", "CommandBuffered", "Active", "CommandAborted"), seen[0].flags
    assert "CommandAborted" in seen[1].flags and "Done" not in seen[1].flags, seen[1].flags
    assert order(seen[2], "Busy", "CommandBuffered", "Active", "Done"), seen[2].flags
    assert sdk.joints[:2] == pytest.approx([300.0, 2.0])


# ---------------------------------------------------------------- interrupt / continue / stop / disable


def test_interrupt_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt stops the active MoveDirectAbsolute (CommandInterrupted), GroupContinue lets it finish at the target."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    mv = _move(robot, 300.0)
    mv.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(mv.Active))
    robot.run(10)
    _group(robot, "MC_GroupInterruptFB")
    stopped = sdk.joints[0]
    robot.run(20)
    assert mv.CommandInterrupted and not mv.Active and not mv.Done, state(mv)
    assert sdk.joints[0] == stopped and 0.0 < stopped < 300.0
    _group(robot, "MC_GroupContinueFB")
    s = watch(robot, [mv], 4 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert order(s, "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(300.0)


def test_new_command_while_interrupted_waits(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A MoveDirectAbsolute started while the group is interrupted is buffered and only runs after GroupContinue.

    The RC may report the new command as CommandInterrupted or as buffered; it must not move.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    first = _move(robot, 300.0)
    first.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(first.Active))
    robot.run(10)
    _group(robot, "MC_GroupInterruptFB")
    stopped = sdk.joints[0]
    second = _move(robot, 50.0, 20.0)
    second.Execute = True
    s = watch(robot, [second], MOVE_CYCLES, lambda: bool(second.Error))[0]
    assert order(s, "Busy", "CommandBuffered"), s.flags
    assert not second.Active and not second.Done and not second.Error, state(second)
    assert sdk.joints[0] == stopped
    _group(robot, "MC_GroupContinueFB")
    robot.run(8 * MOVE_CYCLES, until=lambda: finished(second))
    assert first.Done and second.Done, (state(first), state(second))
    assert sdk.joints[:2] == pytest.approx([50.0, 20.0])


def test_interrupt_then_stop_aborts(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop after GroupInterrupt ends the interrupted MoveDirectAbsolute with CommandAborted."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    mv = _move(robot, 300.0)
    mv.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(mv.Active))
    robot.run(10)
    _group(robot, "MC_GroupInterruptFB")
    stopped = sdk.joints[0]
    _group(robot, "MC_GroupStopFB")
    robot.run(10)
    assert mv.CommandAborted and not mv.Done and not mv.Busy, state(mv)
    assert sdk.joints[0] == stopped


def test_disable_during_motion_interrupts(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Switching the power off during the motion turns Active off and sets CommandInterrupted with the matching InfoID."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    en = enable(robot)
    mv = _move(robot, 300.0)
    mv.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(mv.Active))
    robot.run(10)
    en.Enable = False
    robot.run(MOVE_CYCLES, until=lambda: bool(mv.CommandInterrupted or mv.Error))
    assert mv.CommandInterrupted and not mv.Active and not mv.Done, state(mv)
    assert mv.InfoID == INFO.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, hex(mv.InfoID)
    stopped = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == stopped < 300.0


# ---------------------------------------------------------------- sequences (6.3.3.2, 5.5.3.4)


@pytest.mark.parametrize("flag", [None, SequenceFlag.PRIMARY_SEQUENCE], ids=["default", "explicit_primary"])
def test_primary_sequence_command(
    robot: RobotTaskHarness, sdk: SdkSimulator, flag: SequenceFlag | None
) -> None:
    """MoveDirectAbsolute with the default or the explicit primary SequenceFlag runs in the primary sequence."""
    enable(robot)
    mv = _move(robot, 60.0)
    if flag is not None:
        mv.SequenceFlag = flag
    assert mv.SequenceFlag == SequenceFlag.PRIMARY_SEQUENCE
    s = execute(robot, mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert not _secondary_active(robot)
    assert sdk.joints[0] == pytest.approx(60.0)


def test_primary_command_waits_while_secondary_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """While the secondary sequence is active a primary MoveDirectAbsolute is only buffered and does not move."""
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    mv = _move(robot, 100.0)
    mv.Execute = True
    s = watch(robot, [mv], 3 * MOVE_CYCLES, lambda: bool(mv.Error or mv.Done))[0]
    assert order(s, "Busy", "CommandBuffered"), s.flags
    assert not mv.Active and not mv.Done and not mv.Error, state(mv)
    assert _secondary_active(robot)
    assert sdk.joints[0] == 0.0


def test_secondary_command_runs_after_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After SetSequence(secondary) and GroupContinue a MoveDirectAbsolute with the secondary SequenceFlag finishes."""
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    assert _secondary_active(robot)
    mv = _move(robot, 100.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    mv.Execute = True
    robot.run(10)
    _group(robot, "MC_GroupContinueFB")
    s = watch(robot, [mv], 3 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert mv.Done and not mv.Error, state(mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(100.0)


def test_back_to_primary_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Two buffered primary commands are interrupted by SetSequence(secondary) and finish after SetSequence(primary) and GroupContinue."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    first, second = _move(robot, 300.0), _move(robot, 100.0, 50.0)
    first.Execute = second.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(first.Active))
    robot.run(10)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    robot.run(5)
    assert first.CommandInterrupted and not first.Active, state(first)
    _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    _group(robot, "MC_GroupContinueFB")
    seen = watch(robot, [first, second], 8 * MOVE_CYCLES, lambda: finished(first) and finished(second))
    assert first.Done and second.Done, (state(first), state(second))
    assert order(seen[1], "Busy", "CommandBuffered", "Active", "Done"), seen[1].flags
    assert not _secondary_active(robot)
    assert sdk.joints[:2] == pytest.approx([100.0, 50.0])


def test_secondary_commands_aborted_when_back_to_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Secondary commands not yet executed end with CommandAborted when the sequence returns to primary; the
    primary commands then finish.
    """
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    p1, p2 = _move(robot, 300.0), _move(robot, 100.0, 50.0)
    p1.Execute = p2.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(p1.Active))
    robot.run(10)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    s1 = _move(robot, 10.0, 10.0, 10.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    s2 = _move(robot, 20.0, 20.0, 20.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    s1.Execute = s2.Execute = True
    robot.run(20, until=lambda: bool(s1.CommandBuffered and s2.CommandBuffered))
    assert s1.CommandBuffered and s2.CommandBuffered, (state(s1), state(s2))
    _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    robot.run(5)
    for s in (s1, s2):
        assert s.CommandAborted and not s.Done and not s.Active, state(s)
    _group(robot, "MC_GroupContinueFB")
    robot.run(8 * MOVE_CYCLES, until=lambda: finished(p2))
    assert p1.Done and p2.Done, (state(p1), state(p2))
    assert sdk.joints[:3] == pytest.approx([100.0, 50.0, 0.0])


def test_secondary_flag_while_primary_active_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A secondary-sequence MoveDirectAbsolute while the primary sequence is active is rejected by the RC and the robot does not move."""
    enable(robot)
    mv = _move(robot, 100.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    s = execute(robot, mv)
    assert s.final["Error"] and s.final["ErrorID"] == E.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE, s.final
    assert "Active" not in s.flags and "Done" not in s.flags, s.flags
    assert sdk.joints[0] == 0.0


# ---------------------------------------------------------------- dynamics rates


RATES = ("VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate")


@pytest.mark.parametrize("rate", RATES)
@pytest.mark.parametrize(
    ("value", "encoded"),
    [(50.0, 5000), (0.0, 0), (100.0, 10000), (-25.0, 0xFFFF)],
    ids=["half", "minimal", "maximal", "negative_is_default"],
)
def test_dynamics_rate_reaches_the_rc(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, value: float, encoded: int
) -> None:
    """A dynamics rate in the valid range (or negative = default) is sent to the RC and the move completes.

    0 % means the minimal, 100 % the maximal reference dynamics, a negative rate the default dynamics
    (sent as 16#FFFF). The speed effect itself is checked in ``test_lower_velocity_rate_takes_longer``.
    """
    enable(robot)
    mv = _move(robot, 100.0)
    setattr(mv.ParCmd, rate, value)
    s = execute(robot, mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), (s.flags, s.final)
    assert int(_telegram(sdk)[rate]) == encoded
    assert sdk.joints[0] == pytest.approx(100.0)


def _duration(h: RobotTaskHarness, x: float, velocity: float) -> int:
    mv = _move(h, x)
    mv.ParCmd.VelocityRate = velocity
    mv.Execute = True
    s = watch(h, [mv], 20 * MOVE_CYCLES, lambda: bool(mv.Active))[0]
    s = watch(h, [mv], 20 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert mv.Done, state(mv)
    mv.Execute = False
    h.run(2)
    return s.cycles


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated robot moves every command in a fixed number of cycles, the "
    "VelocityRate does not change the move duration (spec 6.3.3.3, 5.5.7 robot dynamics)",
)
def test_lower_velocity_rate_takes_longer(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """The same distance takes longer with a VelocityRate of 5 % than with 95 %."""
    enable(robot)
    slow = _duration(robot, 200.0, 5.0)
    fast = _duration(robot, 0.0, 95.0)
    assert slow > fast, (slow, fast)


# ---------------------------------------------------------------- MoveTime


def _done_or_rejected(seen: Any, errors: tuple[int, ...]) -> bool:
    """The RC either executes the command (Done) or rejects it with one of ``errors`` (unsupported option)."""
    f = seen.final
    if f["Done"]:
        return order(seen, "Busy", "CommandBuffered", "Active", "Done")
    return bool(f["Error"] and f["ErrorID"] in errors and "Active" not in seen.flags)


@pytest.mark.parametrize("move_time", [100, 150, 200, 5], ids=["100ms", "150ms", "200ms", "5ms_long_segment"])
def test_move_time(robot: RobotTaskHarness, sdk: SdkSimulator, move_time: int) -> None:
    """A MoveTime is executed by the RC (Done at the target) or rejected as unsupported without motion.

    A very short time on a long segment may also be refused by an RC that supports MoveTime.
    """
    enable(robot)
    mv = _move(robot, 1200.0)
    mv.ParCmd.MoveTime = move_time
    s = execute(robot, mv)
    allowed: tuple[int, ...] = (E.ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED,)
    assert _done_or_rejected(s, allowed), (s.flags, s.final)
    expected = 1200.0 if s.final["Done"] else 0.0
    assert sdk.joints[0] == pytest.approx(expected)


def test_move_time_overrides_velocity(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Two commands with the same MoveTime but different VelocityRate take the same time, or both are rejected as unsupported."""
    enable(robot)
    results = []
    for x, velocity in ((200.0, 80.0), (400.0, 10.0)):
        mv = _move(robot, x)
        mv.ParCmd.MoveTime = 150
        mv.ParCmd.VelocityRate = velocity
        results.append(execute(robot, mv))
    allowed: tuple[int, ...] = (E.ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED,)
    assert all(_done_or_rejected(s, allowed) for s in results), [(s.flags, s.final) for s in results]
    if all(s.final["Done"] for s in results):
        assert abs(results[0].cycles - results[1].cycles) <= 2, [s.cycles for s in results]


# ---------------------------------------------------------------- ToolNo / FrameNo


@pytest.mark.parametrize(
    ("field", "number"),
    [("ToolNo", 0), ("ToolNo", 5), ("FrameNo", 0), ("FrameNo", 5)],
    ids=["default_tool", "tool_5", "default_frame", "frame_5"],
)
def test_tool_and_frame_number(robot: RobotTaskHarness, sdk: SdkSimulator, field: str, number: int) -> None:
    """MoveDirectAbsolute with the default or a defined tool / frame sends that number and completes at the target."""
    enable(robot)
    mv = _move(robot, 100.0, 20.0)
    setattr(mv.ParCmd, field, number)
    s = execute(robot, mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), (s.flags, s.final)
    assert int(_telegram(sdk)[field]) == number
    tool, frame = (number, 0) if field == "ToolNo" else (0, number)
    pos = read_position(robot, tool, frame)
    assert (pos.ToolNoReturn, pos.FrameNoReturn) == (tool, frame)
    assert (pos.ActualCartesianPosition.X, pos.ActualCartesianPosition.Y) == pytest.approx((100.0, 20.0))


# ---------------------------------------------------------------- arm configuration / ConfigMode

S, EL, W = ArmConfigShoulder, ArmConfigElbow, ArmConfigWrist
# (target config shoulder/elbow/wrist of the second move, ConfigMode shoulder/elbow/wrist)
CONFIG_CASES = [
    pytest.param((S.FRONT, EL.UP, W.NON_FLIP), (0, 0, 0), id="use_config_unchanged"),
    pytest.param((S.FRONT, EL.UP, W.FLIP), (0, 0, 0), id="use_config_wrist_changed"),
    pytest.param((S.FRONT, EL.UP, W.NON_FLIP), (1, 1, 1), id="keep_config_unchanged"),
    pytest.param((S.FRONT, EL.UP, W.FLIP), (1, 1, 1), id="keep_config_wrist_changed"),
    pytest.param((S.FRONT, EL.UP, W.NON_FLIP), (2, 2, 2), id="free_config_unchanged"),
    pytest.param((S.FRONT, EL.UP, W.FLIP), (2, 2, 2), id="free_config_wrist_changed"),
    pytest.param((S.BACK, EL.UP, W.FLIP), (1, 1, 0), id="only_wrist_from_position"),
    pytest.param((S.BACK, EL.DOWN, W.FLIP), (0, 1, 1), id="only_shoulder_from_position"),
    pytest.param((S.BACK, EL.DOWN, W.FLIP), (1, 0, 1), id="only_elbow_from_position"),
    pytest.param((S.FRONT, EL.DOWN, W.NON_FLIP), (0, 4, 0), id="elbow_forced_up"),
    pytest.param((S.FRONT, EL.UP, W.NON_FLIP), (0, 3, 0), id="elbow_forced_down"),
    pytest.param((S.BACK, EL.UP, W.NON_FLIP), (4, 0, 0), id="shoulder_forced_front"),
    pytest.param((S.FRONT, EL.UP, W.NON_FLIP), (3, 0, 0), id="shoulder_forced_back"),
    pytest.param((S.FRONT, EL.UP, W.FLIP), (0, 0, 4), id="wrist_forced_non_flip"),
    pytest.param((S.FRONT, EL.UP, W.NON_FLIP), (0, 0, 3), id="wrist_forced_flip"),
]


@pytest.mark.parametrize(("config", "mode"), CONFIG_CASES)
def test_arm_config_and_config_mode(
    robot: RobotTaskHarness, sdk: SdkSimulator, config: tuple[int, int, int], mode: tuple[int, int, int]
) -> None:
    """A second MoveDirectAbsolute with a given arm configuration and ConfigMode completes and both reach the RC.

    The first move uses the base configuration (front, up, non-flip); the second one sets the target
    configuration and the ConfigMode per joint (0 use position, 1 keep, 2 free, 3 / 4 force a value).
    The telegram packs ConfigMode as shoulder / elbow nibbles in byte 0 and wrist in byte 1.
    """
    enable(robot)
    first = _move(robot, 100.0)
    first.ParCmd.Position.Config.Shoulder, first.ParCmd.Position.Config.Elbow = S.FRONT, EL.UP
    first.ParCmd.Position.Config.Wrist = W.NON_FLIP
    assert execute(robot, first).final["Done"]
    second = _move(robot, 150.0, 30.0)
    second.ParCmd.Position.Config.Shoulder, second.ParCmd.Position.Config.Elbow = config[0], config[1]
    second.ParCmd.Position.Config.Wrist = config[2]
    second.ParCmd.ConfigMode.Shoulder, second.ParCmd.ConfigMode.Elbow = mode[0], mode[1]
    second.ParCmd.ConfigMode.Wrist = mode[2]
    s = execute(robot, second)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), (s.flags, s.final)
    t = _telegram(sdk)
    assert (int(t["ConfigMode[0]"]) & 0x0F, int(t["ConfigMode[0]"]) >> 4, int(t["ConfigMode[1]"])) == mode
    assert sdk.joints[:2] == pytest.approx([150.0, 30.0])


# ---------------------------------------------------------------- TurnMode


@pytest.mark.parametrize(
    ("mode", "turns"),
    [
        (TurnMode.FREE, (0, 1)),
        (TurnMode.FREE, (-1, -1)),
        (TurnMode.SAME, (0, 0)),
        (TurnMode.SAME, (-1, 0)),
        (TurnMode.USE_TURN_NUMBER, (0, 0)),
    ],
    ids=["free", "free_unusual_turns", "keep_turns", "keep_unusual_turns", "use_turns"],
)
def test_turn_mode(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: TurnMode, turns: tuple[int, int]
) -> None:
    """After a move with turn number 1 on J2, a second move with the given TurnMode / turn numbers completes
    and both values reach the RC.
    """
    enable(robot)
    first = _move(robot, 100.0)
    first.ParCmd.Position.TurnNumber.J2Turns = 1
    assert execute(robot, first).final["Done"]
    second = _move(robot, 150.0)
    second.ParCmd.TurnMode = mode
    second.ParCmd.Position.TurnNumber.J1Turns, second.ParCmd.Position.TurnNumber.J2Turns = turns
    s = execute(robot, second)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), (s.flags, s.final)
    t = _telegram(sdk)
    assert int(t["TurnMode"]) == int(mode)
    assert int(t["Position.TurnNumber[0]"]) != 0 or turns == (0, 0)
    assert sdk.joints[0] == pytest.approx(150.0)


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated robot has no turn ranges, every turn number is reachable; an "
    "unreachable turn number with TurnMode 'use turn number' cannot be stimulated (spec 6.3.3.3 TurnMode)",
)
def test_unreachable_turn_number_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """With TurnMode 'use turn number' a turn number the robot cannot reach ends with Error and no motion."""
    enable(robot)
    mv = _move(robot, 100.0)
    mv.ParCmd.TurnMode = TurnMode.USE_TURN_NUMBER
    mv.ParCmd.Position.TurnNumber.J1Turns = -7
    s = execute(robot, mv)
    assert s.final["Error"] and not s.final["Done"], (s.flags, s.final)
    assert sdk.joints[0] == 0.0


# ---------------------------------------------------------------- software limits


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated robot ignores the software limits (RC_SW_LIMITS of the harness are "
    "stored but not checked), the robot moves beyond them (spec 6.3.3.3, 5.5.x SW limits)",
)
def test_target_outside_software_limits(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A target outside the software limits is not reached: the robot stops at the limit with a warning or the command ends with Error."""
    sdk.rc_change(sdk.RC_SW_LIMITS, 0, [-50.0, 50.0] * 6)
    robot.run(10)
    enable(robot)
    mv = _move(robot, 200.0)
    s = execute(robot, mv)
    assert sdk.joints[0] <= 50.0 + 1e-6, sdk.joints[:3]
    assert s.final["Error"] or mv.WarningID != 0 or mv.InfoID == INFO.INFO_SW_LIMITS_REACHED, (
        s.flags,
        s.final,
    )


# ---------------------------------------------------------------- many short moves


def test_ten_short_moves_buffered(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Ten short MoveDirectAbsolute commands, each started when the previous one is buffered, run one after
    another and all end with Done.
    """
    enable(robot)
    since = len(sdk.logs)
    moves = [_move(robot, 20.0 * (i + 1)) for i in range(10)]
    moves[0].Execute = True
    active_order: list[int] = []
    for _ in range(30 * MOVE_CYCLES):
        robot.cycle()
        for i, mv in enumerate(moves):
            if mv.CommandBuffered and i + 1 < len(moves):
                moves[i + 1].Execute = True
            if mv.Active and i not in active_order:
                assert all(moves[j].Done for j in range(i)), [state(m) for m in moves[:i]]
                active_order.append(i)
            assert not mv.Error, state(mv)
        assert sum(bool(m.Active) for m in moves) <= 1
        if all(finished(m) for m in moves):
            break
    assert active_order == list(range(10)), active_order
    assert all(m.Done for m in moves), [state(m) for m in moves]
    assert _accepted(sdk, since) == 10
    assert sdk.joints[0] == pytest.approx(200.0)
