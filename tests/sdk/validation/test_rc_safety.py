# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_safety
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    BrakeTest, SafeReferencing, ReadSafeReferencePosition and the mode
#    change of a moving robot, run against the SDK simulator.
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

"""Safety related commands against the SDK simulator (robot controller behaviour).

The simulator answers BrakeTest and SafeReferencing at once and does not move the robot during a
safe referencing; the result values are set with ``set_response``. RC errors that the simulator
cannot produce by itself (optional parameter not supported, maximum distance exceeded, undefined
reference position) are stimulated with a forced command error.

* BrakeTest: all axes / single axis, failure and warning bits, not enabled, interrupted,
  aborting mode, sequence flags, parking sequences (move - brake test - move)
* SafeReferencing: default command, status values, forced RC errors, negative rates, aborting
  mode, GroupStop abort, interrupted, sequence flags
* ReadSafeReferencePosition: position and number of positions, undefined index
* auto external -> T1 external while a motion runs: the robot stops and does not resume by itself
* SDK gaps (strict xfail): bit order of the brake test result, external axes status, safe
  referencing status / motion / maximum distance, index check, motion in T1 external
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import AbortingMode, CmdType, OperationMode, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import cartesian, enable, execute, fb, move_axes, order, state, watch

ALL_AXES = 0x7E  # J1..J6 (bit 1..6)
INFO_INTERRUPT_ACTIVE = 0x6F01
INFO_NOT_ENABLED = 0x6F02
INFO_ABORT_BY_STOP = 0x6C05
INFO_ABORT_BY_MOTION = 0x6C06
ERR_DISABLED_BY_RC = 0x8C04
ERR_SECONDARY_NOT_ACTIVE = 0x8F16
ERR_MAX_DISTANCE = 0x8C67
ERR_SAFE_REF_FAILED = 0x8C68
ERR_OPTION_NOT_SUPPORTED = 0x8E31
ERR_REF_INDEX = 0x8D47

GAP_BIT_ORDER = "SDK-GAP: simulator reverses the bit order of the brake test result bytes"
GAP_SAFE_REF_MOTION = "SDK-GAP: simulator completes a safe referencing at once without moving the robot"


def _axes(flags: Any, bits: int, prefix: str = "AxisJ") -> None:
    for i in range(1, 7):
        setattr(flags, f"{prefix}{i}", bool(bits & (1 << i)))


def _bits(flags: Any, prefix: str = "AxisJ", n: int = 6) -> list[int]:
    return [i for i in range(1, n + 1) if getattr(flags, f"{prefix}{i}")]


def _brake_test(h: RobotTaskHarness, bits: int = ALL_AXES, **inputs: Any) -> Any:
    b = fb(h, "MC_BrakeTestFB", **inputs)
    _axes(b.ParCmd.RobotAxesActive, bits)
    return b


def _command(h: RobotTaskHarness, name: str, **inputs: Any) -> Any:
    return _brake_test(h, **inputs) if name == "MC_BrakeTestFB" else fb(h, name, **inputs)


def _mover(h: RobotTaskHarness, kind: str, target: float = 10.0, **inputs: Any) -> Any:
    """MoveLinear / MoveDirect (X = target) or MoveAxes (J1 = target); identity kinematics moves J1 in all cases."""
    if kind == "axes":
        return move_axes(h, target, **inputs)
    m = fb(h, "MC_MoveLinearAbsoluteFB" if kind == "linear" else "MC_MoveDirectAbsoluteFB", **inputs)
    cartesian(m, target, 0.0, 0.0)
    m.ParCmd.VelocityRate = 100.0
    m.ParCmd.AccelerationRate = 100.0
    m.ParCmd.DecelerationRate = -1.0
    m.ParCmd.JerkRate = -1.0
    return m


def _sequence(h: RobotTaskHarness, secondary: bool) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = (
        SequenceFlag.SECONDARY_SEQUENCE if secondary else SequenceFlag.PRIMARY_SEQUENCE
    )
    assert execute(h, seq).final["Done"]


def _set_mode(h: RobotTaskHarness, mode: OperationMode) -> None:
    om = fb(h, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    assert execute(h, om).final["Done"]
    h.run(3)


SAFETY_COMMANDS = pytest.mark.parametrize(
    "name", ["MC_BrakeTestFB", "MC_SafeReferencingFB"], ids=["brake_test", "safe_ref"]
)
MOVES = pytest.mark.parametrize("kind", ["linear", "direct", "axes"])


# ---------------------------------------------------------------- BrakeTest


def test_brake_test_all_axes(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """BrakeTest of all robot axes: Busy then Done, every axis reported as passed, no warning; the selection reaches the RC."""
    enable(robot)
    b = _brake_test(robot)
    s = execute(robot, b, reset=False)
    assert order(s, "Busy", "Done") and not s.final["Error"], s.flags
    assert _bits(b.OutCmd.RobotAxesStatus) == [1, 2, 3, 4, 5, 6]
    assert _bits(b.OutCmd.RobotAxesWarning) == []
    assert int(sdk.firmware_command(int(CmdType.BrakeTest))["RobotAxesActive"]) == ALL_AXES


@pytest.mark.parametrize("axis", [1, 2, 3, 4, 5, 6], ids=[f"j{i}" for i in range(1, 7)])
def test_brake_test_single_axis(robot: RobotTaskHarness, axis: int) -> None:
    """BrakeTest of one robot axis: Done, only this axis is reported as passed."""
    enable(robot)
    b = _brake_test(robot, 1 << axis)
    s = execute(robot, b, reset=False)
    assert s.final["Done"] and not s.final["Error"], s.final
    assert _bits(b.OutCmd.RobotAxesStatus) == [axis]


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: external axes status reports E1..E5 as tested although no external axis was selected",
)
def test_brake_test_external_axes_not_selected(robot: RobotTaskHarness) -> None:
    """BrakeTest without external axes: no external axis is reported as tested."""
    enable(robot)
    b = _brake_test(robot)
    assert execute(robot, b, reset=False).final["Done"]
    assert _bits(b.OutCmd.ExternalAxesStatus, "AxisE") == []


def test_brake_test_failure_and_warning_reported(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A failed brake on J2 and J5 (with warning) set by the RC: Done, J2 and J5 not passed and flagged in the warning output.

    The pattern is symmetric, so it is not affected by the bit-order gap of the simulator."""
    enable(robot)
    sdk.set_response(int(CmdType.BrakeTest), {"RobotAxesStatus": 0x5A, "RobotAxesWarning": 0x24})
    b = _brake_test(robot)
    assert execute(robot, b, reset=False).final["Done"]
    assert _bits(b.OutCmd.RobotAxesStatus) == [1, 3, 4, 6]
    assert _bits(b.OutCmd.RobotAxesWarning) == [2, 5]


@pytest.mark.xfail(strict=True, reason=GAP_BIT_ORDER)
def test_brake_test_failure_of_one_axis(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A failed brake on J2 only (with warning): J2 is reported as not passed and flagged in the warning output."""
    enable(robot)
    sdk.set_response(int(CmdType.BrakeTest), {"RobotAxesStatus": 0x7A, "RobotAxesWarning": 0x04})
    b = _brake_test(robot)
    assert execute(robot, b, reset=False).final["Done"]
    assert _bits(b.OutCmd.RobotAxesStatus) == [1, 3, 4, 5, 6]
    assert _bits(b.OutCmd.RobotAxesWarning) == [2]


@SAFETY_COMMANDS
def test_command_needs_enabled_robot(robot: RobotTaskHarness, name: str) -> None:
    """BrakeTest / SafeReferencing while the robot is not enabled: Busy, then CommandInterrupted with info 16#6F02."""
    b = _command(robot, name)
    b.Execute = True
    robot.run(100, until=lambda: bool(b.CommandInterrupted or b.Done or b.Error))
    assert b.CommandInterrupted and b.Busy and not b.Done and not b.Error, state(b)
    assert b.InfoID == INFO_NOT_ENABLED


@SAFETY_COMMANDS
def test_command_while_interrupted(robot: RobotTaskHarness, name: str) -> None:
    """BrakeTest / SafeReferencing after GroupInterrupt: CommandInterrupted with info 16#6F01, Done after GroupContinue."""
    enable(robot)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    b = _command(robot, name)
    b.Execute = True
    robot.run(50, until=lambda: bool(b.CommandInterrupted or b.Done or b.Error))
    assert b.CommandInterrupted and not b.Done, state(b)
    assert b.InfoID == INFO_INTERRUPT_ACTIVE
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    robot.run(50, until=lambda: bool(b.Done or b.Error))
    assert b.Done and not b.Error, state(b)


@SAFETY_COMMANDS
@MOVES
def test_aborting_mode_cancels_motion(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, kind: str
) -> None:
    """BrakeTest / SafeReferencing with AbortingMode ABORT during a motion: the motion ends with
    CommandAborted (16#6C06), the command with Done.
    """
    sdk.set_move_cycles(100)
    enable(robot)
    mv = _mover(robot, kind)
    mv.Execute = True
    robot.run(20)
    assert mv.Active, state(mv)
    b = _command(robot, name, AbortingMode=AbortingMode.ABORT)
    b.Execute = True
    w = watch(robot, [mv, b], 100, lambda: bool(b.Done or b.Error))
    assert order(w[0], "Active", "CommandAborted") and mv.InfoID == INFO_ABORT_BY_MOTION, w[0].flags
    assert order(w[1], "Busy", "CommandBuffered", "Done") and not b.Error, w[1].flags
    robot.run(5)
    assert sdk.joints[0] < 10.0 and sdk.states.ra_sequence_state == 91


@SAFETY_COMMANDS
def test_secondary_flag_rejected_in_primary_sequence(robot: RobotTaskHarness, name: str) -> None:
    """BrakeTest / SafeReferencing with the secondary sequence flag while the primary sequence is active: Error 16#8F16."""
    enable(robot)
    b = _command(robot, name, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    s = execute(robot, b)
    assert s.final["Error"] and s.final["ErrorID"] == ERR_SECONDARY_NOT_ACTIVE, s.final


@SAFETY_COMMANDS
def test_primary_command_waits_during_secondary_sequence(robot: RobotTaskHarness, name: str) -> None:
    """BrakeTest / SafeReferencing in the primary sequence while the secondary is active: buffered, done after
    switching back and GroupContinue.
    """
    enable(robot)
    _sequence(robot, True)
    b = _command(robot, name)
    b.Execute = True
    robot.run(20)
    assert b.Busy and b.CommandBuffered and not b.Done, state(b)
    _sequence(robot, False)
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    robot.run(50, until=lambda: bool(b.Done or b.Error))
    assert b.Done and not b.Error, state(b)


@SAFETY_COMMANDS
def test_secondary_command_in_secondary_sequence(robot: RobotTaskHarness, name: str) -> None:
    """BrakeTest / SafeReferencing with the secondary flag while the secondary sequence is active: Done."""
    enable(robot)
    _sequence(robot, True)
    s = execute(robot, _command(robot, name, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE))
    assert s.final["Done"] and not s.final["Error"], s.final


@pytest.mark.parametrize("failed", [False, True], ids=["brakes_ok", "brake_failed"])
@MOVES
def test_parking_sequence(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str, failed: bool) -> None:
    """Buffered motion to the test position, BrakeTest, motion to the parking position: all three end with
    Done, also after a failed brake.
    """
    enable(robot)
    if failed:
        sdk.set_response(int(CmdType.BrakeTest), {"RobotAxesStatus": 0x5A, "RobotAxesWarning": 0x24})
    m1 = _mover(robot, kind, 10.0)
    b = _brake_test(robot)
    m2 = _mover(robot, kind, 0.0)
    m1.Execute = True
    robot.run(2)
    b.Execute = True
    robot.run(2)
    m2.Execute = True
    w = watch(robot, [m1, b, m2], 500, lambda: bool(m2.Done or m2.Error))
    assert all(order(x, "Busy", "Done") for x in w), [x.flags for x in w]
    assert sdk.joints[0] == pytest.approx(0.0)
    assert _bits(b.OutCmd.RobotAxesStatus) == ([1, 3, 4, 6] if failed else [1, 2, 3, 4, 5, 6])


def test_parking_after_interrupted_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Motion - BrakeTest - parking motion with GroupInterrupt during the parking motion: interrupted, Done after GroupContinue."""
    sdk.set_move_cycles(100)
    enable(robot)
    m1 = _mover(robot, "linear", 10.0)
    b = _brake_test(robot)
    m2 = _mover(robot, "linear", 0.0)
    for x in (m1, b, m2):
        x.Execute = True
        robot.run(2)
    robot.run(300, until=lambda: bool(m2.Active))
    robot.run(20)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    robot.run(10, until=lambda: bool(m2.CommandInterrupted))
    assert m2.CommandInterrupted and m1.Done and b.Done, (state(m1), state(b), state(m2))
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    robot.run(300, until=lambda: bool(m2.Done or m2.Error))
    assert m2.Done and sdk.joints[0] == pytest.approx(0.0)


@pytest.mark.xfail(strict=True, reason="SDK-GAP: brake test is answered at once, Active is never visible")
def test_brake_test_active_while_running(robot: RobotTaskHarness) -> None:
    """A BrakeTest takes time on the robot: Busy, Active, then Done."""
    enable(robot)
    s = execute(robot, _brake_test(robot))
    assert order(s, "Busy", "Active", "Done"), s.flags


# ---------------------------------------------------------------- SafeReferencing


def test_safe_referencing_default_command(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SafeReferencing with default values: Busy then Done without error; the command reaches the RC."""
    enable(robot)
    s = execute(robot, fb(robot, "MC_SafeReferencingFB"), reset=False)
    assert order(s, "Busy", "Done") and not s.final["Error"], s.flags
    assert sdk.last_command(int(CmdType.SafeReferencing)) is not None


@pytest.mark.xfail(
    strict=True, reason="SDK-GAP: simulator reports status 1 (in progress) at Done instead of 2 (completed)"
)
def test_safe_referencing_status_completed(robot: RobotTaskHarness) -> None:
    """A finished SafeReferencing reports status 2 (completed)."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    assert execute(robot, s, reset=False).final["Done"]
    assert s.OutCmd.Status == 2


@pytest.mark.parametrize("status", [3, 4], ids=["additional_position", "user_input"])
def test_safe_referencing_status_passed_through(
    robot: RobotTaskHarness, sdk: SdkSimulator, status: int
) -> None:
    """The status reported by the RC (another reference position required / user input required) appears at the output."""
    enable(robot)
    sdk.set_response(int(CmdType.SafeReferencing), {"Status": status})
    s = fb(robot, "MC_SafeReferencingFB")
    assert execute(robot, s, reset=False).final["Done"]
    assert s.OutCmd.Status == status


@pytest.mark.xfail(strict=True, reason=GAP_SAFE_REF_MOTION)
def test_safe_referencing_moves_to_reference_position(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SafeReferencing moves the robot to the given joint position: Active while moving, Done at the position."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    s.ParCmd.JointPosition.J1 = 5.0
    seen = execute(robot, s, reset=False)
    assert order(seen, "Busy", "Active", "Done"), seen.flags
    assert sdk.joints[0] == pytest.approx(5.0)


@pytest.mark.xfail(strict=True, reason="SDK-GAP: simulator does not check MaximumDistance")
def test_safe_referencing_maximum_distance_exceeded(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A reference position farther away than MaximumDistance: Error 16#8C67, the robot does not move."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    s.ParCmd.JointPosition.J1 = 50.0
    s.ParCmd.MaximumDistance = 1.0
    seen = execute(robot, s)
    assert seen.final["ErrorID"] == ERR_MAX_DISTANCE, seen.final
    assert sdk.joints[0] == 0.0


@pytest.mark.parametrize(
    "code",
    [ERR_OPTION_NOT_SUPPORTED, ERR_MAX_DISTANCE, ERR_SAFE_REF_FAILED],
    ids=["option_not_supported", "max_distance", "referencing_failed"],
)
def test_safe_referencing_rc_error(robot: RobotTaskHarness, sdk: SdkSimulator, code: int) -> None:
    """An RC error (optional parameter not supported, distance exceeded, referencing failed): Busy then Error with the RC code, no Done.

    Stimulated by a forced command error."""
    enable(robot)
    sdk.set_command_error(int(CmdType.SafeReferencing), code)
    seen = execute(robot, fb(robot, "MC_SafeReferencingFB"))
    assert order(seen, "Busy", "Error") and seen.final["ErrorID"] == code and not seen.final["Done"], (
        seen.final
    )


@pytest.mark.parametrize(
    "rate",
    ["VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate"],
    ids=["velocity", "acceleration", "deceleration", "jerk"],
)
def test_safe_referencing_negative_rate_uses_default(robot: RobotTaskHarness, rate: str) -> None:
    """A negative dynamic rate selects the default of the RC: Done without error."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    setattr(s.ParCmd, rate, -1.0)
    seen = execute(robot, s)
    assert order(seen, "Busy", "Done") and not seen.final["Error"], seen.final


@pytest.mark.parametrize("tool", [0, 1], ids=["default_tool", "tool_1"])
def test_safe_referencing_tool_reaches_rc(robot: RobotTaskHarness, sdk: SdkSimulator, tool: int) -> None:
    """SafeReferencing with the default tool or tool 1: Done, the tool number reaches the RC."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    s.ParCmd.ToolNo = tool
    assert execute(robot, s).final["Done"]
    assert int(sdk.last_command(int(CmdType.SafeReferencing))["ToolNo"]) == tool


def test_safe_referencing_aborted_by_group_stop(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SafeReferencing buffered behind a motion, then GroupInterrupt and GroupStop: both end with CommandAborted (16#6C05)."""
    sdk.set_move_cycles(100)
    enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(10)
    s = fb(robot, "MC_SafeReferencingFB")
    s.Execute = True
    robot.run(5)
    assert s.CommandBuffered and not s.Done, state(s)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    gs = fb(robot, "MC_GroupStopFB")
    gs.Execute = True
    robot.run(50, until=lambda: bool(gs.Done or gs.Error))
    assert gs.Done, state(gs)
    assert s.CommandAborted and s.InfoID == INFO_ABORT_BY_STOP and not s.Done, state(s)
    assert mv.CommandAborted, state(mv)


# ---------------------------------------------------------------- ReadSafeReferencePosition


def test_read_reference_position(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReadSafeReferencePosition: Busy then Done; joint position and number of positions as reported by the RC."""
    sdk.set_response(int(CmdType.ReadSafeReferencePosition), {"NumberOfPositions": 3})
    sdk.joints = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] + [0.0] * 6
    r = fb(robot, "MC_ReadSafeReferencePositionFB")
    r.ParCmd.Index = 2
    seen = execute(robot, r, reset=False)
    assert order(seen, "Busy", "Done") and not seen.final["Error"], seen.flags
    assert r.OutCmd.NumberOfPositions == 3
    p = r.OutCmd.Position
    assert [p.J1, p.J2, p.J3, p.J4, p.J5, p.J6] == pytest.approx([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    assert int(sdk.last_command(int(CmdType.ReadSafeReferencePosition))["Index"]) == 2


def test_read_reference_position_undefined_index(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """No reference position defined for the index: Busy then Error with the RC code, no Done (stimulated by a forced error)."""
    sdk.set_command_error(int(CmdType.ReadSafeReferencePosition), ERR_REF_INDEX)
    r = fb(robot, "MC_ReadSafeReferencePositionFB")
    r.ParCmd.Index = 3
    seen = execute(robot, r)
    assert order(seen, "Busy", "Error") and seen.final["ErrorID"] == ERR_REF_INDEX, seen.final


@pytest.mark.xfail(
    strict=True, reason="SDK-GAP: simulator accepts any index, also one above the number of positions"
)
def test_read_reference_position_index_out_of_range(robot: RobotTaskHarness) -> None:
    """Index 255 (no such reference position): Error from the RC."""
    r = fb(robot, "MC_ReadSafeReferencePositionFB")
    r.ParCmd.Index = 255
    seen = execute(robot, r)
    assert seen.final["Error"] and seen.final["ErrorID"] == ERR_REF_INDEX, seen.final


# ---------------------------------------------------------------- mode change while moving


@MOVES
def test_auto_to_t1_stops_motion(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str) -> None:
    """Auto external to T1 external during a motion: the drives switch off, the robot stops, the motion is interrupted (16#6F02)
    and EnableRobot reports 16#8C04; after enabling again the motion does not resume by itself."""
    sdk.set_move_cycles(200)
    _set_mode(robot, OperationMode.AUTO_EXT)
    en = enable(robot)
    mv = _mover(robot, kind)
    mv.Execute = True
    robot.run(30)
    assert mv.Active, state(mv)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.T1_EXT
    assert execute(robot, om).final["Done"]
    robot.run(20)
    assert not sdk.enabled and en.Error and en.ErrorID == ERR_DISABLED_BY_RC, state(en)
    assert mv.CommandInterrupted and mv.InfoID == INFO_NOT_ENABLED and not mv.Done, state(mv)
    stop = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == stop < 10.0
    en.Enable = False
    robot.run(5)
    en.Enable = True
    robot.run(100, until=lambda: bool(en.Enabled or en.Error))
    assert en.Enabled, state(en)
    robot.run(50)
    assert sdk.joints[0] == stop and not mv.Done


@pytest.mark.xfail(
    strict=True, reason="SDK-GAP: motion in T1 external never starts (sequence stays 'interrupting')"
)
@MOVES
def test_t1_to_auto_stops_motion(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str) -> None:
    """T1 external to auto external during a motion with HoldToRun: the robot stops and the motion is interrupted."""
    sdk.set_move_cycles(200)
    _set_mode(robot, OperationMode.T1_EXT)
    en = enable(robot)
    en.ParCmd.HoldToRun = True
    mv = _mover(robot, kind)
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Active))
    robot.run(10)
    assert mv.Active and sdk.joints[0] > 0.0, state(mv)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.AUTO_EXT
    assert execute(robot, om).final["Done"]
    robot.run(20)
    assert mv.CommandInterrupted and not sdk.enabled, state(mv)
