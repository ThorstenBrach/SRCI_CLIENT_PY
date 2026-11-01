# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_move_axes
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of MoveAxesAbsolute: behaviour of the robot controller.
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

"""Validation tests of MoveAxesAbsolute: behaviour of the robot controller.

The tests run the client library against the SDK simulator (identity kinematics, every motion
takes ``MOVE_CYCLES`` cycles). They check what the RC does with a MoveAxesAbsolute command:
flag sequence, motion, progress, dynamics and blending parameters, aborting / buffering,
interrupt / continue / stop, sequences and limits.

Where the simulator cannot show the specified behaviour (no software limit check, no dynamics
model, optional parameters not supported) the test asserts the specification and is a strict
``xfail`` with the reason ``SDK-GAP``.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import AbortingMode, BlendingMode, RobotLibraryErrorIdEnum, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    MOVE_CYCLES,
    enable,
    execute,
    fb,
    finished,
    move_axes,
    order,
    state,
    watch,
)

MOVE_AXES_ABSOLUTE = 2101
E = RobotLibraryErrorIdEnum

_GAP_BLENDING = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK rejects the optional blending modes DEFINED_VELOCITY (2), CORNER_DISTANCE_2R (10) "
    "and CORNER_DISTANCE_1R (12) with 16#8E05 (optional parameter not supported); an RC that supports "
    "them executes the motion (spec 6.3.4.3 BlendingMode, 5.5.8 blending)",
)
_GAP_TIME = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK rejects every MoveTime > 0 with 16#8E06 (optional parameter Time not supported); "
    "spec 6.3.4.3: with Time > 0 the velocity is ignored and the motion takes the given time, an RC that "
    "cannot keep it answers with an error",
)
_GAP_DYNAMICS = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated motion always takes MOVE_CYCLES cycles, the dynamic rates have no effect "
    "on the duration (spec 5.5.7 robot dynamics: rates in % of the reference dynamics)",
)
_GAP_LIMITS = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulator does not check the target against the software limits of the robot "
    "(default -360..360 deg, also after rc_change RC_SW_LIMITS) and moves to every target (spec 6.3.4.3, "
    "5.5.7: the RC stops at the limit with an error / warning or rejects the target)",
)


# ------------------------------------------------------------------ local helpers


def _last(sdk: SdkSimulator) -> dict[str, str]:
    cmd = sdk.last_command(MOVE_AXES_ABSOLUTE)
    assert cmd is not None
    return cmd


def _first_cycles(h: RobotTaskHarness, blocks: list[Any], cycles: int, until: Any) -> list[dict[str, int]]:
    """Cycle of the first appearance of every flag of every block (bounded by ``cycles``)."""
    first: list[dict[str, int]] = [{} for _ in blocks]
    count = [0]

    def step() -> bool:
        count[0] += 1
        for i, b in enumerate(blocks):
            for f in (
                "Busy",
                "CommandBuffered",
                "Active",
                "Done",
                "Error",
                "CommandAborted",
                "CommandInterrupted",
            ):
                if getattr(b, f, False) and f not in first[i]:
                    first[i][f] = count[0]
        return bool(until())

    h.run(cycles, until=step)
    return first


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> dict[str, Any]:
    ss = fb(h, "MC_SetSequenceFB")
    ss.ParCmd.TargetSequence = target
    return execute(h, ss).final


def _secondary_active(h: RobotTaskHarness) -> bool:
    return bool(h.ag.State.StatusRobotArm.SecondarySequenceActive)


def _duration(h: RobotTaskHarness, sdk: SdkSimulator, target: float, **par: float) -> int:
    """Cycles from the rising edge of Execute to Done of a MoveAxesAbsolute with ``par``."""
    mv = move_axes(h, target)
    for k, v in par.items():
        setattr(mv.ParCmd, k, v)
    seen = execute(h, mv, cycles=20 * MOVE_CYCLES)
    assert seen.final["Done"], seen.final
    return seen.cycles


# ------------------------------------------------------------------ basic execution


def test_flag_sequence_progress_and_done_reset(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A valid MoveAxesAbsolute runs Busy, CommandBuffered, Active, Done, reports a rising Progress up to 100 % and Done falls with Execute.

    Progress is the share of the distance already travelled; it never exceeds 100 %.
    """
    enable(robot)
    mv = move_axes(robot, 30.0, -10.0)
    progress: list[float] = []
    mv.Execute = True

    def until() -> bool:
        progress.append(mv.OutCmd.Progress)
        return bool(finished(mv))

    seen = watch(robot, [mv], 4 * MOVE_CYCLES, until)[0]
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert not mv.Error and mv.ErrorID == 0
    assert sdk.joints[:2] == pytest.approx([30.0, -10.0])
    assert all(0.0 <= p <= 100.0 for p in progress)
    assert progress == sorted(progress) and progress[-1] == pytest.approx(100.0)
    assert any(0.0 < p < 100.0 for p in progress)
    mv.Execute = False
    robot.run(2)
    assert not mv.Done and not mv.Busy


def test_linear_external_axis_moves_in_mm(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute moves the linear external axis E1 (unit mm) to its target and ends with Done."""
    enable(robot)
    assert robot.ag.State.RobotData.AxisExternalUsed.E1
    mv = move_axes(robot, 0.0)
    mv.ParCmd.JointPosition.E1 = 500.0
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert sdk.joints[6] == pytest.approx(500.0)


@pytest.mark.parametrize("j6", [370.0, -370.0], ids=["j6_plus_370", "j6_minus_370"])
def test_wrist_axis_beyond_one_turn(robot: RobotTaskHarness, sdk: SdkSimulator, j6: float) -> None:
    """A J6 target beyond one turn either runs to Done at exactly that angle or is rejected as not reachable without motion.

    Both reactions are allowed (robot specific): the RC moves the axis in the direction of the sign to
    the given angle, or it answers ERR_POSITION_NOT_REACHABLE before the motion starts.
    """
    enable(robot)
    mv = move_axes(robot, 0.0, j6=j6)
    seen = execute(robot, mv)
    if seen.final["Done"]:
        assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
        assert sdk.joints[5] == pytest.approx(j6)
    else:
        assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_POSITION_NOT_REACHABLE, seen.final
        assert "Active" not in seen.flags and sdk.joints[5] == 0.0


@pytest.mark.parametrize("tool_no", [0, 5], ids=["flange", "tool_5"])
def test_tool_number_is_used(robot: RobotTaskHarness, sdk: SdkSimulator, tool_no: int) -> None:
    """MoveAxesAbsolute with the flange or an available tool runs to Done and the RC receives that ToolNo."""
    enable(robot)
    mv = move_axes(robot, 15.0)
    mv.ParCmd.ToolNo = tool_no
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert _last(sdk)["ToolNo"] == str(tool_no)
    assert sdk.joints[0] == pytest.approx(15.0)


# ------------------------------------------------------------------ dynamics


@pytest.mark.parametrize(
    ("name", "value", "sent"),
    [
        ("VelocityRate", 50.0, 5000),
        ("VelocityRate", 100.0, 10000),
        ("VelocityRate", 0.0, 0),
        ("VelocityRate", -25.0, 0xFFFF),
        ("AccelerationRate", 50.0, 5000),
        ("AccelerationRate", 100.0, 10000),
        ("AccelerationRate", 0.0, 0),
        ("AccelerationRate", -25.0, 0xFFFF),
        ("DecelerationRate", 50.0, 5000),
        ("DecelerationRate", 100.0, 10000),
        ("DecelerationRate", 0.0, 0),
        ("DecelerationRate", -25.0, 0xFFFF),
        ("JerkRate", 50.0, 5000),
        ("JerkRate", 100.0, 10000),
        ("JerkRate", 0.0, 0),
        ("JerkRate", -25.0, 0xFFFF),
    ],
    ids=lambda v: str(v),
)
def test_dynamic_rate_in_range_is_executed(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, value: float, sent: int
) -> None:
    """A dynamic rate between 0 % and 100 % or a negative rate (default) is executed to Done and reaches the RC in 1/100 %.

    0 % means the internal minimal value, a negative rate the default dynamics (sent as 16#FFFF).
    """
    enable(robot)
    mv = move_axes(robot, 40.0)
    setattr(mv.ParCmd, name, value)
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert (
        not seen.final["Error"] and not seen.final["CommandAborted"] and not seen.final["CommandInterrupted"]
    )
    assert int(_last(sdk)[name]) == sent
    assert sdk.joints[0] == pytest.approx(40.0)


@pytest.mark.parametrize(
    "rates", [(40.32, 4032), (60.12, 6012), (27.27, 2727)], ids=["40_32", "60_12", "27_27"]
)
def test_fractional_velocity_rate(
    robot: RobotTaskHarness, sdk: SdkSimulator, rates: tuple[float, int]
) -> None:
    """A VelocityRate with two decimals is executed to Done without error and reaches the RC with full resolution."""
    enable(robot)
    mv = move_axes(robot, 25.0)
    mv.ParCmd.VelocityRate = rates[0]
    seen = execute(robot, mv)
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    assert int(_last(sdk)["VelocityRate"]) == rates[1]


@_GAP_DYNAMICS
@pytest.mark.parametrize("name", ["VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate"])
def test_lower_rate_takes_longer(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """The same motion with a rate of 5 % takes longer than with 95 %."""
    enable(robot)
    slow = _duration(robot, sdk, 100.0, **{name: 5.0})
    fast = _duration(robot, sdk, 0.0, **{name: 95.0})
    assert slow > fast


def test_swapped_acceleration_and_deceleration_take_the_same_time(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """A motion with acceleration 50 % / deceleration 100 % takes the same time as the way back with 100 % / 50 %."""
    enable(robot)
    there = _duration(robot, sdk, 300.0, AccelerationRate=50.0, DecelerationRate=100.0)
    back = _duration(robot, sdk, 0.0, AccelerationRate=100.0, DecelerationRate=50.0)
    assert there == back


@_GAP_TIME
def test_move_time_is_executed(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute with a reachable MoveTime runs to Done and the RC receives the time."""
    enable(robot)
    mv = move_axes(robot, 50.0)
    mv.ParCmd.MoveTime = 1500
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.final
    assert int(_last(sdk)["Time"]) == 1500


@_GAP_TIME
def test_move_time_overrides_velocity(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Two motions with the same MoveTime but VelocityRate 80 % and 10 % take the same time (the velocity is ignored)."""
    enable(robot)
    first = _duration(robot, sdk, 100.0, MoveTime=1500, VelocityRate=80.0)
    second = _duration(robot, sdk, 0.0, MoveTime=1500, VelocityRate=10.0)
    assert first == second


@_GAP_TIME
def test_move_time_too_short_for_the_distance(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A MoveTime far too short for a long distance ends with an error of the RC (dynamic limit, not reachable or invalid time).

    Robot specific: the RC rejects the command before the motion or stops it at the dynamic limit.
    """
    enable(robot)
    mv = move_axes(robot, 300.0)
    mv.ParCmd.MoveTime = 5
    seen = execute(robot, mv)
    assert seen.final["Error"], seen.final
    assert seen.final["ErrorID"] in (
        E.ERR_LIMIT_EXCEEDED_RETURN_POS,
        E.ERR_POSITION_NOT_REACHABLE,
        E.ERR_INVALID_PARAM_TIME,
    )
    assert sdk.joints[0] < 300.0


# ------------------------------------------------------------------ blending

_SINGLE_BLENDING = [
    (BlendingMode.EXACT_STOP, (20.0, 0.0)),
    (BlendingMode.EXACT_STOP, (0.0, 0.0)),
    pytest.param(BlendingMode.DEFINED_VELOCITY, (10.0, 0.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.DEFINED_VELOCITY, (20.0, 0.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.DEFINED_VELOCITY, (20.0, 30.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.DEFINED_VELOCITY, (100.0, 0.0), marks=_GAP_BLENDING),
    (BlendingMode.CORNER_DISTANCE, (10.0, 0.0)),
    (BlendingMode.CORNER_DISTANCE, (50.0, 0.0)),
    (BlendingMode.CORNER_DISTANCE, (0.0, 0.0)),
    (BlendingMode.CORNER_DISTANCE, (0.0, 50.0)),
    (BlendingMode.MAX_CORNER_DEVIATION, (10.0, 0.0)),
    (BlendingMode.MAX_CORNER_DEVIATION, (0.0, 0.0)),
    (BlendingMode.MAX_CORNER_DEVIATION, (30.0, 50.0)),
    (BlendingMode.MAX_CORNER_DEVIATION, (0.0, 50.0)),
    pytest.param(BlendingMode.CORNER_DISTANCE_2R, (10.0, 30.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.CORNER_DISTANCE_2R, (0.0, 0.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.CORNER_DISTANCE_2R, (50.0, 30.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.CORNER_DISTANCE_2R, (0.0, 30.0), marks=_GAP_BLENDING),
    (BlendingMode.RAMP_OVERLAP, (10.0, 30.0)),
    (BlendingMode.RAMP_OVERLAP, (0.0, 0.0)),
    (BlendingMode.RAMP_OVERLAP, (50.0, 30.0)),
    (BlendingMode.RAMP_OVERLAP, (0.0, 30.0)),
    pytest.param(BlendingMode.CORNER_DISTANCE_1R, (10.0, 0.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.CORNER_DISTANCE_1R, (0.0, 0.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.CORNER_DISTANCE_1R, (50.0, 30.0), marks=_GAP_BLENDING),
    pytest.param(BlendingMode.CORNER_DISTANCE_1R, (0.0, 30.0), marks=_GAP_BLENDING),
]


def _blend_id(v: Any) -> str:
    if isinstance(v, BlendingMode):
        return v.name.lower()
    return "par_" + "_".join(f"{x:g}" for x in v)


@pytest.mark.parametrize(("mode", "par"), _SINGLE_BLENDING, ids=_blend_id)
def test_single_blended_motion_stops_at_target(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: BlendingMode, par: tuple[float, float]
) -> None:
    """A single MoveAxesAbsolute with a blending mode and no following motion runs to Done and stops exactly at its target.

    Without a successor there is nothing to blend into; the RC receives mode and parameters unchanged.
    Execute is reset as soon as the command is buffered.
    """
    enable(robot)
    mv = move_axes(robot, 60.0)
    mv.ParCmd.BlendingMode = mode
    mv.ParCmd.BlendingParameter = list(par)
    mv.Execute = True
    robot.run(20, until=lambda: bool(mv.CommandBuffered or mv.Error))
    mv.Execute = False
    seen = watch(robot, [mv], 4 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert mv.Done and not mv.Error, (seen.flags, state(mv))
    assert sdk.joints[0] == pytest.approx(60.0)
    cmd = _last(sdk)
    assert int(cmd["BlendingMode"]) == int(mode)
    assert (float(cmd["BlendingParameter[0]"]), float(cmd["BlendingParameter[1]"])) == pytest.approx(par)


_TWO_BLENDING = [
    pytest.param(BlendingMode.DEFINED_VELOCITY, (20.0, 0.0), marks=_GAP_BLENDING),
    (BlendingMode.MAX_CORNER_DEVIATION, (20.0, 0.0)),
    (BlendingMode.CORNER_DISTANCE, (20.0, 0.0)),
    pytest.param(BlendingMode.CORNER_DISTANCE_2R, (20.0, 10.0), marks=_GAP_BLENDING),
    (BlendingMode.RAMP_OVERLAP, (20.0, 10.0)),
    pytest.param(BlendingMode.CORNER_DISTANCE_1R, (20.0, 10.0), marks=_GAP_BLENDING),
    (BlendingMode.CORNER_DISTANCE, (0.0, 0.0)),
]


@pytest.mark.parametrize(("mode", "par"), _TWO_BLENDING, ids=_blend_id)
def test_blended_motion_into_a_second_motion(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: BlendingMode, par: tuple[float, float]
) -> None:
    """Two buffered MoveAxesAbsolute, the first with a blending mode: both run to Done in order and the robot ends at the second target.

    The second command is buffered while the first is active and becomes Active not before the first one
    is Done. The geometric shape of the blending (path near the first target) is not simulated.
    """
    enable(robot)
    first = move_axes(robot, 40.0, 10.0)
    first.ParCmd.BlendingMode = mode
    first.ParCmd.BlendingParameter = list(par)
    second = move_axes(robot, 40.0, 50.0)
    first.Execute = True
    robot.run(20, until=lambda: bool(first.CommandBuffered or first.Error))
    second.Execute = True
    robot.run(20, until=lambda: bool(second.CommandBuffered or second.Error))
    first.Execute = second.Execute = False
    cycles = _first_cycles(
        robot, [first, second], 6 * MOVE_CYCLES, lambda: finished(second) or bool(first.Error)
    )
    assert "Done" in cycles[0] and "Error" not in cycles[0], (cycles, state(first))
    assert "Done" in cycles[1] and "Error" not in cycles[1], (cycles, state(second))
    assert cycles[1]["Active"] >= cycles[0]["Done"]
    assert sdk.joints[:2] == pytest.approx([40.0, 50.0])


def test_blended_motion_aborted_by_second_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A second MoveAxesAbsolute with AbortingMode ABORT started while a blended first motion is active aborts it and runs to Done."""
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    first = move_axes(robot, 80.0)
    first.ParCmd.BlendingMode = BlendingMode.CORNER_DISTANCE
    first.ParCmd.BlendingParameter = [20.0, 0.0]
    second = move_axes(robot, 10.0, 30.0, AbortingMode=AbortingMode.ABORT)
    first.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: bool(first.Active or first.Error))
    second.Execute = True
    s1, s2 = watch(robot, [first, second], 8 * MOVE_CYCLES, lambda: finished(second))
    assert order(s1, "Active", "CommandAborted") and not first.Done, (s1.flags, state(first))
    assert order(s2, "Busy", "CommandBuffered", "Active", "Done"), s2.flags
    assert sdk.joints[:2] == pytest.approx([10.0, 30.0])


@pytest.mark.parametrize(
    "blending", [None, (BlendingMode.CORNER_DISTANCE, (10.0, 0.0))], ids=["exact_stop", "corner_distance_10"]
)
def test_ten_short_motions_in_a_row(
    robot: RobotTaskHarness, sdk: SdkSimulator, blending: tuple[BlendingMode, tuple[float, float]] | None
) -> None:
    """Ten MoveAxesAbsolute of 2 deg each, each started when the previous one is buffered, all run to Done one after the other.

    Every command becomes Active only after the previous one is Done; the robot ends at the last target.
    """
    enable(robot)
    sdk.set_move_cycles(10)
    cmds = [move_axes(robot, 2.0 * (i + 1)) for i in range(10)]
    if blending is not None:
        for c in cmds:
            c.ParCmd.BlendingMode = blending[0]
            c.ParCmd.BlendingParameter = list(blending[1])
    first: list[dict[str, int]] = [{} for _ in cmds]
    count = [0]

    def step() -> bool:
        count[0] += 1
        for i, b in enumerate(cmds):
            for f in ("Busy", "CommandBuffered", "Active", "Done", "Error"):
                if getattr(b, f) and f not in first[i]:
                    first[i][f] = count[0]
        return finished(cmds[-1])

    for c in cmds:
        c.Execute = True
        robot.run(20, until=lambda: step() or bool(c.CommandBuffered or c.Error))  # noqa: B023
        c.Execute = False
    robot.run(20 * 10 + 50, until=step)
    for i, f in enumerate(first):
        assert "Error" not in f and "Done" in f, (i, f)
        assert f["Busy"] <= f["CommandBuffered"] <= f["Active"] <= f["Done"], (i, f)
        if i:
            assert f["Active"] >= first[i - 1]["Done"], (i, first[i - 1], f)
    assert sdk.joints[0] == pytest.approx(20.0)


# ------------------------------------------------------------------ aborting / buffering


def test_aborting_command_between_buffered_commands(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Of four commands (buffer, buffer, abort, buffer) started while the first is active, the first two are
    aborted and the last two run to Done.
    """
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    cmds = [move_axes(robot, 10.0 * (i + 1)) for i in range(4)]
    cmds[2].AbortingMode = AbortingMode.ABORT
    cmds[0].Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: bool(cmds[0].Active or cmds[0].Error))
    for c in cmds[1:]:
        c.Execute = True
    seen = watch(robot, cmds, 12 * MOVE_CYCLES, lambda: all(finished(c) for c in cmds))
    assert order(seen[0], "Busy", "CommandBuffered", "Active", "CommandAborted"), seen[0].flags
    assert order(seen[1], "Busy", "CommandAborted") and "Active" not in seen[1].flags, seen[1].flags
    for s in seen[2:]:
        assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert not any(c.Error for c in cmds)
    assert sdk.joints[0] == pytest.approx(40.0)


@pytest.mark.parametrize("first_active", [True, False], ids=["after_first_active", "same_cycle"])
def test_aborting_commands_last_one_wins(
    robot: RobotTaskHarness, sdk: SdkSimulator, first_active: bool
) -> None:
    """Of three MoveAxesAbsolute with AbortingMode ABORT the earlier ones end with CommandAborted and only the last one runs to Done.

    Started either while the first command is active or all in the same cycle.
    """
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    cmds = [move_axes(robot, 10.0 * (i + 1), AbortingMode=AbortingMode.ABORT) for i in range(3)]
    cmds[0].Execute = True
    if first_active:
        robot.run(4 * MOVE_CYCLES, until=lambda: bool(cmds[0].Active or cmds[0].Error))
    for c in cmds[1:]:
        c.Execute = True
    seen = watch(robot, cmds, 12 * MOVE_CYCLES, lambda: all(finished(c) for c in cmds))
    for s in seen[:2]:
        assert order(s, "Busy", "CommandAborted") and "Done" not in s.flags, s.flags
    assert order(seen[2], "Busy", "CommandBuffered", "Active", "Done"), seen[2].flags
    assert sdk.joints[0] == pytest.approx(30.0)


# ------------------------------------------------------------------ interrupt / continue / stop / power


def test_interrupt_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt during MoveAxesAbsolute resets Active, sets CommandInterrupted and freezes Progress; GroupContinue resumes to Done.

    After the continue Active is TRUE again, CommandInterrupted FALSE and Progress rises again.
    """
    enable(robot)
    sdk.set_move_cycles(4 * MOVE_CYCLES)
    mv = move_axes(robot, 100.0)
    mv.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: sdk.joints[0] > 20.0)
    assert mv.Active
    interrupt = execute(robot, fb(robot, "MC_GroupInterruptFB"))
    assert interrupt.final["Done"], interrupt.final
    robot.run(3)
    assert mv.CommandInterrupted and not mv.Active and mv.Busy, state(mv)
    held, pos = mv.OutCmd.Progress, sdk.joints[0]
    robot.run(20)
    assert mv.OutCmd.Progress == held and sdk.joints[0] == pos
    cont = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert cont.final["Done"], cont.final
    robot.run(10)
    assert mv.Active and not mv.CommandInterrupted, state(mv)
    assert mv.OutCmd.Progress > held
    robot.run(8 * MOVE_CYCLES, until=lambda: finished(mv))
    assert mv.Done and not mv.Error, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)


def test_stop_after_interrupt_aborts_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop after GroupInterrupt ends the interrupted MoveAxesAbsolute with CommandAborted; the robot
    stays where it was interrupted.
    """
    enable(robot)
    sdk.set_move_cycles(4 * MOVE_CYCLES)
    mv = move_axes(robot, 100.0)
    mv.Execute = True
    seen = watch(robot, [mv], 4 * MOVE_CYCLES, lambda: sdk.joints[0] > 20.0)[0]
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    pos = sdk.joints[0]
    stop = execute(robot, fb(robot, "MC_GroupStopFB"), reset=False)
    assert stop.final["Done"], stop.final
    seen2 = watch(robot, [mv], 50, lambda: finished(mv))[0]
    assert order(seen, "Busy", "CommandBuffered", "Active"), seen.flags
    assert "CommandAborted" in seen2.flags and not mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(pos)


def test_power_off_during_motion_interrupts(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Disabling the robot during MoveAxesAbsolute resets Active and sets CommandInterrupted; the command stays buffered (Busy)."""
    en = enable(robot)
    sdk.set_move_cycles(4 * MOVE_CYCLES)
    mv = move_axes(robot, 100.0)
    mv.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: sdk.joints[0] > 5.0)
    mv.Execute = False
    en.Enable = False
    seen = watch(robot, [mv], 50, lambda: bool(mv.CommandInterrupted))[0]
    assert mv.CommandInterrupted and not mv.Active and mv.Busy and mv.CommandBuffered, (seen.flags, state(mv))
    assert not mv.Done and not mv.Error
    pos = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == pos < 100.0


def test_start_without_power_waits_buffered(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute started while the robot is disabled is buffered (Busy, CommandBuffered) and the robot does not move.

    It does not become Active; once the robot is enabled and GroupContinue is given the motion runs to Done.
    """
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    seen = watch(robot, [mv], 50, lambda: False)[0]
    assert order(seen, "Busy", "CommandBuffered"), seen.flags
    assert "Active" not in seen.flags and "Error" not in seen.flags
    assert sdk.joints[0] == 0.0
    enable(robot)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(4 * MOVE_CYCLES, until=lambda: finished(mv))
    assert mv.Done and sdk.joints[0] == pytest.approx(10.0), state(mv)


def test_start_while_interrupted_waits_buffered(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute started while the enabled robot is interrupted is buffered and waits; after GroupContinue it runs to Done."""
    enable(robot)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    seen = watch(robot, [mv], 50, lambda: False)[0]
    assert order(seen, "Busy", "CommandBuffered") and "Active" not in seen.flags, seen.flags
    assert sdk.joints[0] == 0.0
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(4 * MOVE_CYCLES, until=lambda: finished(mv))
    assert mv.Done and sdk.joints[0] == pytest.approx(10.0), state(mv)


# ------------------------------------------------------------------ sequences


def test_default_sequence_flag_runs_in_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute with the default SequenceFlag runs in the primary sequence to Done; the secondary sequence stays inactive."""
    enable(robot)
    mv = move_axes(robot, 10.0)
    assert mv.SequenceFlag == SequenceFlag.PRIMARY_SEQUENCE
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert not _secondary_active(robot)


def test_secondary_flag_rejected_while_primary_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute with SequenceFlag SECONDARY while the primary sequence is active is rejected by the RC
    (secondary not active) without motion.
    """
    enable(robot)
    mv = move_axes(robot, 10.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    seen = execute(robot, mv)
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE, seen.final
    assert "Active" not in seen.flags and "Done" not in seen.flags
    assert sdk.joints[0] == 0.0 and not _secondary_active(robot)


def test_primary_command_waits_while_secondary_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After SetSequence(secondary) a primary MoveAxesAbsolute is buffered but not executed; the secondary sequence stays active."""
    enable(robot)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)["Done"]
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    seen = watch(robot, [mv], 2 * MOVE_CYCLES, lambda: False)[0]
    assert order(seen, "Busy", "CommandBuffered") and "Active" not in seen.flags, seen.flags
    assert sdk.joints[0] == 0.0
    assert _secondary_active(robot)


def test_secondary_command_runs_after_set_sequence_and_continue(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """After SetSequence(secondary) and GroupContinue a MoveAxesAbsolute with SequenceFlag SECONDARY runs to
    Done in the secondary sequence.
    """
    enable(robot)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)["Done"]
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    mv = move_axes(robot, 10.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    seen = execute(robot, mv, reset=False)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert sdk.joints[0] == pytest.approx(10.0)
    assert _secondary_active(robot)


def test_primary_motions_continue_after_sequence_round_trip(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """Two primary motions, SetSequence(secondary) while the first is active, then SetSequence(primary) and GroupContinue: both run to Done.

    The change to the secondary sequence interrupts the active motion; after the return the primary sequence
    is active again and both commands finish in order.
    """
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    a, b = move_axes(robot, 50.0), move_axes(robot, 80.0)
    a.Execute = b.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: bool(a.Active or a.Error))
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)["Done"]
    robot.run(5)
    assert a.CommandInterrupted and _secondary_active(robot), state(a)
    assert _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)["Done"]
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    watch(robot, [a, b], 8 * MOVE_CYCLES, lambda: finished(b))
    assert a.Done and b.Done and not (a.Error or b.Error), (state(a), state(b))
    assert sdk.joints[0] == pytest.approx(80.0)
    assert not _secondary_active(robot)


def test_secondary_commands_aborted_on_return_to_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Secondary commands still buffered when SetSequence(primary) is given end with CommandAborted; the primary ones stay buffered."""
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    a, b = move_axes(robot, 50.0), move_axes(robot, 80.0)
    a.Execute = b.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: bool(a.Active or a.Error))
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)["Done"]
    c, d = (move_axes(robot, v, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE) for v in (20.0, 30.0))
    c.Execute = d.Execute = True
    robot.run(20, until=lambda: bool(c.CommandBuffered and d.CommandBuffered))
    assert c.CommandBuffered and d.CommandBuffered and not (c.Active or d.Active)
    pos = sdk.joints[0]
    assert _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)["Done"]
    seen = watch(robot, [a, b, c, d], 2 * MOVE_CYCLES, lambda: False)
    for s in seen[2:]:
        assert "CommandAborted" in s.flags and "Active" not in s.flags, s.flags
    for blk in (a, b):
        assert blk.Busy and blk.CommandBuffered and not blk.Active and not blk.Done, state(blk)
    assert sdk.joints[0] == pytest.approx(pos)
    assert not _secondary_active(robot)


def test_aborting_primary_command_given_in_secondary_takes_over(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """An aborting primary MoveAxesAbsolute given while the secondary sequence is active aborts the
    interrupted one after the return to primary and runs to Done.
    """
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    a = move_axes(robot, 50.0)
    a.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: bool(a.Active or a.Error))
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)["Done"]
    robot.run(5)
    assert a.CommandInterrupted, state(a)
    b = move_axes(robot, 20.0, AbortingMode=AbortingMode.ABORT)
    b.Execute = True
    robot.run(10)
    assert b.CommandBuffered and not b.Active, state(b)
    assert _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)["Done"]
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    sa, sb = watch(robot, [a, b], 8 * MOVE_CYCLES, lambda: finished(b))
    assert "CommandAborted" in sa.flags and not a.Done, state(a)
    assert order(sb, "Active", "Done"), sb.flags
    assert sdk.joints[0] == pytest.approx(20.0)


# ------------------------------------------------------------------ limits


@_GAP_LIMITS
def test_target_outside_software_limits(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A target outside the software limits is not reached: the RC rejects it or stops at the limit with an error or a warning."""
    enable(robot)
    sdk.rc_change(sdk.RC_SW_LIMITS, 0, [-50.0, 50.0] * 7)
    robot.run(20)
    mv = move_axes(robot, 100.0)
    seen = execute(robot, mv)
    assert not seen.final["Done"], seen.final
    assert seen.final["Error"] or seen.final["CommandInterrupted"], seen.final
    assert sdk.joints[0] <= 50.0 + 1e-6


@_GAP_LIMITS
def test_target_beyond_axis_range(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A J1 target far beyond the axis range (1000 deg) is not reached: the RC rejects it or stops at the limit."""
    enable(robot)
    mv = move_axes(robot, 1000.0)
    seen = execute(robot, mv)
    assert not seen.final["Done"], seen.final
    assert seen.final["Error"] or seen.final["CommandInterrupted"], seen.final
    assert sdk.joints[0] <= 360.0 + 1e-6
