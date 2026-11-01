# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_dynamics_limits
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of the robot controller: default dynamics, reference
#    dynamics and software limits (write, read back, rejected values).
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

"""Validation tests of the robot controller: default dynamics, reference dynamics, software limits.

Covered commands: WriteRobotDefaultDynamics / ReadRobotDefaultDynamics (spec 6.2.14 / 6.2.15),
WriteRobotReferenceDynamics / ReadRobotReferenceDynamics (6.2.13 / 6.2.9), WriteRobotSWLimits /
ReadRobotSWLimits (6.2.16 / 6.2.10). Every test writes a known start state first (when it needs
one), then checks the reaction of the RC (flags, ErrorID) and the values the RC reports back.

The simulated RC of the SDK harness: rate ranges 1..100 %, reference ranges velocity 0..2000,
acceleration / deceleration 0..5000, jerk 0..50000; axes J1..J6 and E1 exist; software limits are
not checked during a motion and the motion time does not depend on the dynamics (MOVE_CYCLES).
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import CmdType, OperationMode, SequenceFlag
from srci.types import RobotLibraryErrorIdEnum as E
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    cartesian,
    enable,
    execute,
    fb,
    move_axes,
    order,
    state,
    watch,
)

RATES = ("VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate")
REFS = ("VelocityReference", "AccelerationReference", "DecelerationReference", "JerkReference")
JOINTS = tuple(f"J{i}" for i in range(1, 7))
EXTERNAL = tuple(f"E{i}" for i in range(1, 7))
# limits that contain the start position (all joints 0) of the simulated robot
LIMITS_A = (
    (-160.0, 160.0),
    (-80.0, 120.0),
    (-140.0, 90.0),
    (-120.0, 120.0),
    (-110.0, 110.0),
    (-100.0, 100.0),
)
LIMITS_B = ((-160.0, 160.0), (-80.0, 120.0), (-80.0, 90.0), (-120.0, 120.0), (-110.0, 110.0), (-100.0, 100.0))
LIMITS_C = ((-170.0, 170.0), (-90.0, 130.0), (-90.0, 90.0), (-130.0, 130.0), (-120.0, 120.0), (-110.0, 110.0))
LIMITS_D = ((-160.0, 160.0), (-80.0, 120.0), (-80.0, 80.0), (-120.0, 120.0), (-110.0, 110.0), (-100.0, 100.0))
BASE_RATES = (20.0, 30.0, 40.0, 50.0)
BASE_REFS = (900.0, 1900.0, 2100.0, 9000.0)
SIM_MIN_RATE = 1.0  # minimum rate of the simulated RC (rate 0 % = "use the internal minimum")


# ---------------------------------------------------------------- helpers


def _sent(sdk: SdkSimulator, cmd_type: int, since: int) -> int:
    """Commands of ``cmd_type`` the RC accepted since log entry ``since``."""
    return sum(
        1
        for log in sdk.logs[since:]
        if f"({int(cmd_type)}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _default_dynamics(h: RobotTaskHarness, rates: tuple[float, float, float, float]) -> Any:
    block = fb(h, "MC_WriteRobotDefaultDynamicsFB")
    for name, value in zip(RATES, rates, strict=True):
        setattr(block.ParCmd.DynamicValues, name, value)
    return block


def _reference_dynamics(h: RobotTaskHarness, refs: tuple[float, float, float, float]) -> Any:
    block = fb(h, "MC_WriteRobotReferenceDynamicsFB")
    for name, value in zip(REFS, refs, strict=True):
        setattr(block.ParCmd.DynamicValues, name, value)
    return block


def _set_limits(
    block: Any, joints: tuple[tuple[float, float], ...], external: tuple[tuple[float, float], ...] = ()
) -> None:
    values = block.ParCmd.LimitValues
    for axis, (low, high) in [*zip(JOINTS, joints, strict=False), *zip(EXTERNAL, external, strict=False)]:
        setattr(values, f"{axis}LowerLimit", low)
        setattr(values, f"{axis}UpperLimit", high)


def _sw_limits(
    h: RobotTaskHarness,
    joints: tuple[tuple[float, float], ...],
    external: tuple[tuple[float, float], ...] = (),
) -> Any:
    block = fb(h, "MC_WriteRobotSWLimitsFB")
    _set_limits(block, joints, external)
    return block


def _done(h: RobotTaskHarness, block: Any) -> Any:
    """Execute and require Done without error; returns the flags seen."""
    seen = execute(h, block, reset=False)
    assert seen.final["Done"] and not seen.final["Error"], (seen.flags, seen.final, hex(block.ErrorID))
    block.Execute = False
    h.run(2)
    return seen


def _read_rates(h: RobotTaskHarness) -> tuple[float, ...]:
    rd = fb(h, "MC_ReadRobotDefaultDynamicsFB")
    _ = execute(h, rd, reset=False)
    assert rd.Done and not rd.Error, state(rd)
    values = tuple(getattr(rd.OutCmd.DynamicValues, n) for n in RATES)
    rd.Execute = False
    h.run(2)
    return values


def _read_refs(h: RobotTaskHarness) -> tuple[float, ...]:
    rd = fb(h, "MC_ReadRobotReferenceDynamicsFB")
    _ = execute(h, rd, reset=False)
    assert rd.Done and not rd.Error, state(rd)
    values = tuple(getattr(rd.OutCmd.DynamicValues, n) for n in REFS)
    rd.Execute = False
    h.run(2)
    return values


def _flat(pairs: tuple[tuple[float, float], ...]) -> tuple[float, ...]:
    return tuple(v for pair in pairs for v in pair)


def _read_limits(h: RobotTaskHarness) -> tuple[float, ...]:
    """Lower, upper limit of J1..J6, E1..E6 (24 values)."""
    rd = fb(h, "MC_ReadRobotSWLimitsFB")
    _ = execute(h, rd, reset=False)
    assert rd.Done and not rd.Error, state(rd)
    values = rd.OutCmd.LimitValues
    out = tuple(
        v
        for a in JOINTS + EXTERNAL
        for v in (getattr(values, f"{a}LowerLimit"), getattr(values, f"{a}UpperLimit"))
    )
    rd.Execute = False
    h.run(2)
    return out


def _expect(written: tuple[float, ...], before: tuple[float, ...]) -> tuple[float, ...]:
    """Values after a write: a negative value keeps the value of the RC."""
    return tuple(b if w < 0 else w for w, b in zip(written, before, strict=True))


def _rejected(h: RobotTaskHarness, block: Any, error: int) -> Any:
    seen = execute(h, block, reset=False)
    assert seen.final["Error"] and not seen.final["Done"], (seen.flags, seen.final)
    assert block.ErrorID == error, (hex(block.ErrorID), hex(error))
    block.Execute = False
    h.run(2)
    return seen


def _linear(h: RobotTaskHarness, x: float) -> Any:
    """MoveLinearAbsolute to (x, 0, 0) with the default dynamics of the RC (all rates -1)."""
    mv = fb(h, "MC_MoveLinearAbsoluteFB")
    cartesian(mv, x, 0.0, 0.0)
    for name in RATES:
        setattr(mv.ParCmd, name, -1.0)
    return mv


def _set_operation_mode(h: RobotTaskHarness, sdk: SdkSimulator, mode: OperationMode) -> None:
    om = fb(h, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    _done(h, om)
    assert sdk.states.operation_mode == int(mode)


def _enter_secondary_sequence(h: RobotTaskHarness, sdk: SdkSimulator) -> Any:
    """Enable, interrupt a running primary motion, switch to the secondary sequence."""
    enable(h)
    sdk.set_move_cycles(200)
    primary = move_axes(h, 100.0)
    primary.Execute = True
    h.run(100, until=lambda: sdk.joints[0] > 5.0)
    _done(h, fb(h, "MC_GroupInterruptFB"))
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    _done(h, seq)
    assert h.ag.State.StatusRobotArm.SecondarySequenceActive
    return primary


def _valid_block(h: RobotTaskHarness, name: str) -> Any:
    """A block with valid parameters (the write blocks change one value of the start state)."""
    if name == "MC_WriteRobotDefaultDynamicsFB":
        return _default_dynamics(h, (10.0, -1.0, -1.0, -1.0))
    if name == "MC_WriteRobotReferenceDynamicsFB":
        return _reference_dynamics(h, (1500.0, -1.0, -1.0, -1.0))
    if name == "MC_WriteRobotSWLimitsFB":
        return _sw_limits(h, LIMITS_C)
    return fb(h, name)


ALL_BLOCKS = (
    "MC_WriteRobotDefaultDynamicsFB",
    "MC_ReadRobotDefaultDynamicsFB",
    "MC_WriteRobotReferenceDynamicsFB",
    "MC_ReadRobotReferenceDynamicsFB",
    "MC_WriteRobotSWLimitsFB",
    "MC_ReadRobotSWLimitsFB",
)


# ---------------------------------------------------------------- default dynamics


@pytest.mark.parametrize(
    "rates",
    [(100.0, 70.0, 80.0, 50.0), (10.0, 90.0, 10.0, 25.0)],
    ids=["high-rates", "low-velocity"],
)
def test_default_dynamics_written_and_read_back(robot: RobotTaskHarness, rates: tuple[float, ...]) -> None:
    """WriteRobotDefaultDynamics with all four rates ends with Done and the RC reports exactly these rates.

    Both the outputs of the write block and a following ReadRobotDefaultDynamics show the new values."""
    write = _default_dynamics(robot, rates)
    seen = execute(robot, write, reset=False)
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    out = write.OutCmd.DefaultDynamicValues
    assert tuple(getattr(out, n) for n in RATES) == pytest.approx(rates)
    write.Execute = False
    robot.run(2)
    assert _read_rates(robot) == pytest.approx(rates)


@pytest.mark.parametrize(
    "rates",
    [
        (-1.0, 100.0, -1.0, -1.0),
        (100.0, -100.0, -100.0, -100.0),
        (-1.0, -1.0, -1.0, 100.0),
        (-1.0, -1.0, 100.0, -1.0),
        (-1.0, 50.0, -1.0, -1.0),
    ],
    ids=["only-acceleration", "only-velocity", "only-jerk", "only-deceleration", "acceleration-50"],
)
def test_default_dynamics_negative_rate_keeps_the_value(
    robot: RobotTaskHarness, rates: tuple[float, ...]
) -> None:
    """A negative default rate leaves that rate of the RC unchanged, the other rates are written.

    Start state: rates 20/30/40/50 %. The write ends with Done; its outputs and the read back show
    the written rates and the start values for the negative ones."""
    _done(robot, _default_dynamics(robot, BASE_RATES))
    write = _default_dynamics(robot, rates)
    _ = execute(robot, write, reset=False)
    assert write.Done and not write.Error, state(write)
    expected = _expect(rates, BASE_RATES)
    out = write.OutCmd.DefaultDynamicValues
    assert tuple(getattr(out, n) for n in RATES) == pytest.approx(expected)
    write.Execute = False
    robot.run(2)
    assert _read_rates(robot) == pytest.approx(expected)


@pytest.mark.parametrize("value", [-1.0, -100.0], ids=["minus-1", "minus-100"])
def test_default_dynamics_without_any_rate_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, value: float
) -> None:
    """WriteRobotDefaultDynamics with all four rates negative (nothing to change) is rejected by the RC.

    Error with 16#8D07 (no value given), the rates of the RC stay unchanged."""
    _done(robot, _default_dynamics(robot, BASE_RATES))
    since = len(sdk.logs)
    _rejected(robot, _default_dynamics(robot, (value,) * 4), E.ERR_INVALID_PARAM_VALUE_ZERO)
    assert _sent(sdk, CmdType.WriteRobotDefaultDynamics, since) == 1
    assert _read_rates(robot) == pytest.approx(BASE_RATES)


@pytest.mark.parametrize("untouched", [False, True], ids=["explicit-zero", "untouched-parcmd"])
def test_default_dynamics_zero_selects_the_minimum(robot: RobotTaskHarness, untouched: bool) -> None:
    """A default rate of 0 % selects the internal minimum of the RC (spec 6.2.14): Done, the RC reports its minimum.

    The untouched ParCmd of the block has all rates 0.0, so it behaves like an explicit 0 %."""
    _done(robot, _default_dynamics(robot, BASE_RATES))
    write = fb(robot, "MC_WriteRobotDefaultDynamicsFB") if untouched else _default_dynamics(robot, (0.0,) * 4)
    _done(robot, write)
    assert _read_rates(robot) == pytest.approx((SIM_MIN_RATE,) * 4)


def test_default_velocity_above_the_rc_range_rejected(robot: RobotTaskHarness) -> None:
    """A default velocity rate of 200 % (sent by the client) is rejected by an RC that allows at most 100 %.

    Error 16#8D38 (invalid VelocityRate); the rates of the RC stay unchanged. Other RCs may accept it."""
    _done(robot, _default_dynamics(robot, BASE_RATES))
    _rejected(robot, _default_dynamics(robot, (200.0, -1.0, -1.0, -1.0)), E.ERR_INVALID_PARAM_VELOCITY_MODE)
    assert _read_rates(robot) == pytest.approx(BASE_RATES)


@pytest.mark.parametrize(
    ("first", "second"),
    [
        ((10.0, 90.0, 10.0, -1.0), (10.0, 90.0, 10.0, -1.0)),
        ((20.0, 30.0, 25.0, -1.0), (80.0, 60.0, 70.0, -1.0)),
    ],
    ids=["same-values", "different-values"],
)
def test_default_dynamics_written_twice(
    robot: RobotTaskHarness, first: tuple[float, ...], second: tuple[float, ...]
) -> None:
    """The same write block executed twice (Execute released while Busy) ends both times with Done; the second values win.

    Execute is reset as soon as Busy is seen; the command still completes and Done is shown."""
    write = _default_dynamics(robot, first)
    for rates in (first, second):
        for name, value in zip(RATES, rates, strict=True):
            setattr(write.ParCmd.DynamicValues, name, value)
        write.Execute = True
        robot.run(50, until=lambda: bool(write.Busy or write.Error))
        write.Execute = False
        seen = watch(robot, [write], 50, lambda: bool(write.Done or write.Error))[0]
        assert write.Done and not write.Error and write.ErrorID == 0, (seen.flags, state(write))
        out = write.OutCmd.DefaultDynamicValues
        assert tuple(getattr(out, n) for n in RATES[:3]) == pytest.approx(rates[:3])
        robot.run(2)
    assert _read_rates(robot)[:3] == pytest.approx(second[:3])


def test_default_dynamics_changed_while_motions_are_queued(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """WriteRobotDefaultDynamics runs in parallel to two buffered motions: it is Done while the first motion is still active.

    Both motions (default dynamics, all rates -1) reach their targets; the RC reports the new
    velocity rate. The slower second motion is not observable in the simulation (fixed motion time)."""
    enable(robot)
    _done(robot, _default_dynamics(robot, (100.0, -1.0, -1.0, -1.0)))
    first, second = _linear(robot, 80.0), _linear(robot, 160.0)
    first.Execute = second.Execute = True
    robot.run(50, until=lambda: bool(first.Active))
    assert first.Active and second.CommandBuffered, (state(first), state(second))
    write = _default_dynamics(robot, (10.0, -1.0, -1.0, -1.0))
    seen = execute(robot, write, reset=False)
    assert write.Done and not write.Error, seen.flags
    assert first.Active and not first.Done, state(first)
    robot.run(400, until=lambda: bool(second.Done or second.Error or first.Error))
    assert first.Done and second.Done, (state(first), state(second))
    assert sdk.joints[0] == pytest.approx(160.0)
    assert _read_rates(robot)[0] == pytest.approx(10.0)


def test_default_dynamics_changed_after_group_stop(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After a motion was aborted by GroupStop the default dynamics can be written and a new motion reaches its target.

    Steps: write velocity 10 %, start a motion, GroupStop (motion CommandAborted), write velocity
    100 %, start the motion again: Done at the target."""
    enable(robot)
    sdk.set_move_cycles(200)
    _done(robot, _default_dynamics(robot, (10.0, -1.0, -1.0, -1.0)))
    move = _linear(robot, 100.0)
    move.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 5.0)
    assert move.Active, state(move)
    stop = fb(robot, "MC_GroupStopFB")
    stop.Execute = True
    robot.run(200, until=lambda: bool(move.CommandAborted or move.Error))
    assert move.CommandAborted, state(move)
    robot.run(200, until=lambda: bool(stop.Done or stop.Error))
    assert stop.Done, state(stop)
    stop.Execute = False
    move.Execute = False
    robot.run(2)
    _done(robot, _default_dynamics(robot, (100.0, -1.0, -1.0, -1.0)))
    sdk.set_move_cycles(50)
    again = _linear(robot, 100.0)
    _done(robot, again)
    assert sdk.joints[0] == pytest.approx(100.0)
    assert _read_rates(robot)[0] == pytest.approx(100.0)


# ---------------------------------------------------------------- reference dynamics


@pytest.mark.parametrize(
    "refs",
    [(1500.0, 1300.0, 1700.0, 5000.0), (1200.0, 400.0, 500.0, 8000.0)],
    ids=["set-1", "set-2"],
)
def test_reference_dynamics_written_and_read_back(robot: RobotTaskHarness, refs: tuple[float, ...]) -> None:
    """WriteRobotReferenceDynamics with all four values ends with Done and the RC reports exactly these values.

    Both the outputs of the write block and a following ReadRobotReferenceDynamics show them."""
    write = _reference_dynamics(robot, refs)
    seen = execute(robot, write, reset=False)
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    out = write.OutCmd.ReferenceDynamicValues
    assert tuple(getattr(out, n) for n in REFS) == pytest.approx(refs)
    write.Execute = False
    robot.run(2)
    assert _read_refs(robot) == pytest.approx(refs)


@pytest.mark.parametrize(
    "refs",
    [(1500.0, -1.0, -1.0, -1.0), (1500.0, -100.0, -100.0, -100.0), (-1.0, -1.0, -1.0, 8000.0)],
    ids=["only-velocity", "only-velocity-minus-100", "only-jerk"],
)
def test_reference_dynamics_negative_value_keeps_the_value(
    robot: RobotTaskHarness, refs: tuple[float, ...]
) -> None:
    """A negative reference value leaves that value of the RC unchanged, the other values are written.

    Start state 900 / 1900 / 2100 / 9000; Done; outputs and read back show the merged values."""
    _done(robot, _reference_dynamics(robot, BASE_REFS))
    write = _reference_dynamics(robot, refs)
    _ = execute(robot, write, reset=False)
    assert write.Done and not write.Error, state(write)
    expected = _expect(refs, BASE_REFS)
    out = write.OutCmd.ReferenceDynamicValues
    assert tuple(getattr(out, n) for n in REFS) == pytest.approx(expected)
    write.Execute = False
    robot.run(2)
    assert _read_refs(robot) == pytest.approx(expected)


def test_reference_dynamics_without_any_value_rejected(robot: RobotTaskHarness) -> None:
    """WriteRobotReferenceDynamics with all four values negative (nothing to change) is rejected with 16#8D25.

    The reference dynamics of the RC stay unchanged."""
    _done(robot, _reference_dynamics(robot, BASE_REFS))
    _rejected(robot, _reference_dynamics(robot, (-1.0,) * 4), E.ERR_INVALID_PARAM_REF_DYNAMICS_LESS_THAN_ZERO)
    assert _read_refs(robot) == pytest.approx(BASE_REFS)


def test_reference_dynamics_zero_accepted(robot: RobotTaskHarness) -> None:
    """Reference values of 0 are inside the range of the simulated RC: Done, the RC reports 0 for all four values.

    Vendor specific: another RC may reject 0; this RC allows 0..max."""
    _done(robot, _reference_dynamics(robot, BASE_REFS))
    _done(robot, _reference_dynamics(robot, (0.0,) * 4))
    assert _read_refs(robot) == pytest.approx((0.0,) * 4)


@pytest.mark.parametrize(
    "refs",
    [
        (250000.0, 10000.0, 10000.0, -1.0),
        (600000.0, 600000.0, 600000.0, -1.0),
        (6000.0, 6000.0, 6000.0, 10000.0),
    ],
    ids=["velocity-250000", "all-600000", "all-6000"],
)
def test_reference_dynamics_above_the_rc_range_rejected(
    robot: RobotTaskHarness, refs: tuple[float, ...]
) -> None:
    """A reference velocity above the range of the RC (here 2000 mm/s) is rejected with 16#8D29.

    The reference dynamics of the RC stay unchanged."""
    _done(robot, _reference_dynamics(robot, BASE_REFS))
    _rejected(robot, _reference_dynamics(robot, refs), E.ERR_INVALID_PARAM_VELOCITY)
    assert _read_refs(robot) == pytest.approx(BASE_REFS)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F126: the ReferenceDynamics values default to 0.0; the parameter table of WriteRobotReferenceDynamics "
    "(spec 6.2.13) names '<0' as the default (= do not change), so an untouched block writes 0 to all four values",
)
def test_reference_dynamics_untouched_parcmd_changes_nothing(robot: RobotTaskHarness) -> None:
    """WriteRobotReferenceDynamics with an untouched ParCmd (spec default: negative = no change) is rejected with 16#8D25.

    The reference dynamics of the RC stay unchanged."""
    _done(robot, _reference_dynamics(robot, BASE_REFS))
    write = fb(robot, "MC_WriteRobotReferenceDynamicsFB")
    seen = execute(robot, write, reset=False)
    assert write.Error and write.ErrorID == E.ERR_INVALID_PARAM_REF_DYNAMICS_LESS_THAN_ZERO, (
        seen.flags,
        state(write),
    )
    write.Execute = False
    robot.run(2)
    assert _read_refs(robot) == pytest.approx(BASE_REFS)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ((10.0, 10.0, 10.0, 10.0), (10.0, 10.0, 10.0, 10.0), (10.0, 10.0, 10.0, 10.0)),
        ((1500.0, 10.0, 10.0, 10.0), (150.0, -1.0, 10.0, 10.0), (150.0, 10.0, 10.0, 10.0)),
    ],
    ids=["same-values", "different-values"],
)
def test_reference_dynamics_written_twice(
    robot: RobotTaskHarness, first: tuple[float, ...], second: tuple[float, ...], expected: tuple[float, ...]
) -> None:
    """The same write block executed twice ends both times with Done; the RC reports the result of the second write.

    A negative value in the second write keeps the value of the first write."""
    write = _reference_dynamics(robot, first)
    _done(robot, write)
    for name, value in zip(REFS, second, strict=True):
        setattr(write.ParCmd.DynamicValues, name, value)
    seen = _done(robot, write)
    assert order(seen, "Busy", "Done"), seen.flags
    assert _read_refs(robot) == pytest.approx(expected)


def test_reference_dynamics_changed_while_motions_are_queued(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """WriteRobotReferenceDynamics runs in parallel to two buffered motions: Done while the first motion is still active.

    Both motions reach their targets, the RC reports the new reference velocity. The effect on the
    speed of the second motion is not observable in the simulation (fixed motion time)."""
    enable(robot)
    first, second = _linear(robot, 80.0), _linear(robot, 160.0)
    first.Execute = second.Execute = True
    robot.run(50, until=lambda: bool(first.Active))
    assert first.Active and second.CommandBuffered, (state(first), state(second))
    write = _reference_dynamics(robot, (250.0, -1.0, -1.0, -1.0))
    _ = execute(robot, write, reset=False)
    assert write.Done and not write.Error, state(write)
    assert first.Active and not first.Done, state(first)
    robot.run(400, until=lambda: bool(second.Done or second.Error or first.Error))
    assert first.Done and second.Done, (state(first), state(second))
    assert sdk.joints[0] == pytest.approx(160.0)
    assert _read_refs(robot)[0] == pytest.approx(250.0)


# ---------------------------------------------------------------- software limits


@pytest.mark.parametrize("limits", [LIMITS_A, LIMITS_B], ids=["set-a", "set-b"])
@pytest.mark.parametrize("style", ["held", "pulse"])
def test_sw_limits_written_and_read_back(
    robot: RobotTaskHarness, limits: tuple[tuple[float, float], ...], style: str
) -> None:
    """WriteRobotSWLimits with limits for J1..J6 ends with Done and ReadRobotSWLimits reports exactly these limits.

    held: Execute stays TRUE, Done stays TRUE until Execute falls. pulse: Execute is reset while
    Busy, Done is shown for exactly one cycle. RestartRequested stays FALSE (the RC applies the
    limits at once); E1..E6 are reported as 0."""
    write = _sw_limits(robot, limits)
    write.Execute = True
    if style == "pulse":
        robot.run(50, until=lambda: bool(write.Busy))
        write.Execute = False
    done_cycles = 0
    for _ in range(60):
        robot.run(1)
        assert not write.Error, state(write)
        done_cycles += bool(write.Done)
    if style == "held":
        assert write.Done and done_cycles > 1, state(write)
        write.Execute = False
        robot.run(1)
        assert not write.Done
    else:
        assert done_cycles == 1
    assert not write.OutCmd.RestartRequested
    assert not robot.ag.State.StatusRobotArm.RestartRequested
    assert _read_limits(robot) == pytest.approx(_flat(limits) + (0.0,) * 12)


def test_sw_limits_written_twice_the_second_set_wins(robot: RobotTaskHarness) -> None:
    """The write block is executed with a first set of limits, changed while Busy and executed again: the second set is active.

    The first execution still completes with the values sampled at its rising edge."""
    write = _sw_limits(robot, LIMITS_C)
    write.Execute = True
    robot.run(50, until=lambda: bool(write.Busy))
    write.Execute = False
    _set_limits(write, LIMITS_D)
    robot.run(50, until=lambda: bool(write.Done or write.Error))
    assert write.Done, state(write)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_C))
    robot.run(2)
    _done(robot, write)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_D))


def test_sw_limits_with_negative_ranges(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Limits -10..-1 for J1..J6 are accepted when the robot stands inside them: Done, the RC reports -10 / -1.

    The robot is moved to -5 on every joint first; E1..E6 stay 0."""
    enable(robot)
    _done(robot, move_axes(robot, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0))
    _done(robot, _sw_limits(robot, ((-10.0, -1.0),) * 6))
    assert _read_limits(robot) == pytest.approx((-10.0, -1.0) * 6 + (0.0,) * 12)


@pytest.mark.parametrize("untouched", [False, True], ids=["explicit-zero", "untouched-parcmd"])
def test_sw_limits_all_zero_rejected(robot: RobotTaskHarness, untouched: bool) -> None:
    """WriteRobotSWLimits with all limits 0 is rejected with 16#8D15; the limits of the RC stay unchanged.

    The untouched ParCmd has all limits 0 as well."""
    _done(robot, _sw_limits(robot, LIMITS_C))
    write = (
        fb(robot, "MC_WriteRobotSWLimitsFB")
        if untouched
        else _sw_limits(robot, ((0.0, 0.0),) * 6, ((0.0, 0.0),) * 6)
    )
    _rejected(robot, write, E.ERR_INVALID_PARAM_SWLIMITS)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_C))


def test_sw_limits_for_missing_external_axes_rejected(robot: RobotTaskHarness) -> None:
    """Limits for external axes the robot does not have (E2..E6) are rejected with 16#8C29; the limits stay unchanged.

    J1..J6 valid, E1..E6 with limits +-100 .. +-150."""
    _done(robot, _sw_limits(robot, LIMITS_C))
    external = (
        (-100.0, 100.0),
        (-110.0, 110.0),
        (-120.0, 120.0),
        (-130.0, 130.0),
        (-140.0, 140.0),
        (-150.0, 150.0),
    )
    _rejected(robot, _sw_limits(robot, LIMITS_A, external), E.ERR_SOFTWARE_LIMITS_FOR_NON_EXISTING_AXIS)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_C))


def test_sw_limits_during_a_motion_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """WriteRobotSWLimits while a motion is active is rejected with 16#8C54; the motion continues to its target.

    Vendor specific: another RC may accept the limits (with or without RestartRequested)."""
    enable(robot)
    _done(robot, _sw_limits(robot, LIMITS_C))
    sdk.set_move_cycles(200)
    move = move_axes(robot, 100.0)
    move.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 5.0)
    assert move.Active, state(move)
    _rejected(robot, _sw_limits(robot, ((-110.0, 110.0),) * 6), E.ERR_SWLIMITS_NOT_ALLOWED_DURING_MOVE)
    robot.run(400, until=lambda: bool(move.Done or move.Error))
    assert move.Done and sdk.joints[0] == pytest.approx(100.0), state(move)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_C))


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK accepts software limits beyond the mechanical range of the axis (J1 -361..361, "
    "the simulated axes have +-360); spec 6.2.16 / error table expects 16#8D16 (invalid LimitValues)",
)
def test_sw_limits_beyond_the_mechanical_range_rejected(robot: RobotTaskHarness) -> None:
    """A J1 limit of -361..361 degree (beyond the +-360 degree of the axis) is rejected with 16#8D16; the limits stay unchanged."""
    _done(robot, _sw_limits(robot, LIMITS_C))
    _rejected(robot, _sw_limits(robot, ((-361.0, 361.0), *LIMITS_D[1:])), E.ERR_INVALID_PARAM_LIMITVALUES)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_C))


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK does not check the range of the external axis E1 (-655.36..655.36 accepted); "
    "spec 6.2.16 / error table expects 16#8D16 (invalid LimitValues)",
)
def test_sw_limits_external_axis_out_of_range_rejected(robot: RobotTaskHarness) -> None:
    """Limits -655.36..655.36 for the external axis E1 (outside its range) are rejected with 16#8D16."""
    _done(robot, _sw_limits(robot, LIMITS_C))
    _rejected(robot, _sw_limits(robot, LIMITS_D, ((-655.36, 655.36),)), E.ERR_INVALID_PARAM_LIMITVALUES)
    assert _read_limits(robot)[:12] == pytest.approx(_flat(LIMITS_C))


def test_sw_limits_applied_without_restart(robot: RobotTaskHarness) -> None:
    """An RC that applies new software limits at once reports RestartRequested FALSE and returns the new limits immediately.

    Steps: read the start limits, write new ones, check the RestartRequested output and status bit,
    read again. The variant with a required restart cannot be stimulated in the simulation."""
    before = _read_limits(robot)
    write = _sw_limits(robot, LIMITS_B)
    _ = execute(robot, write, reset=False)
    assert write.Done and not write.Error, state(write)
    assert not write.OutCmd.RestartRequested
    assert not robot.ag.State.StatusRobotArm.RestartRequested
    write.Execute = False
    robot.run(2)
    after = _read_limits(robot)
    assert after != before
    assert after[:12] == pytest.approx(_flat(LIMITS_B))


# ---------------------------------------------------------------- robot states


@pytest.mark.parametrize("name", ALL_BLOCKS)
def test_commands_with_the_robot_disabled(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """Reading and writing dynamics and software limits does not need an enabled robot: Done without error."""
    assert not sdk.enabled
    seen = _done(robot, _valid_block(robot, name))
    assert order(seen, "Busy", "Done"), seen.flags
    assert not sdk.enabled


@pytest.mark.parametrize("name", ALL_BLOCKS)
def test_commands_in_operation_mode_t1_external(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str
) -> None:
    """Reading and writing dynamics and software limits works in operation mode T1 external: Done without error."""
    _set_operation_mode(robot, sdk, OperationMode.T1_EXT)
    seen = _done(robot, _valid_block(robot, name))
    assert order(seen, "Busy", "Done"), seen.flags


@pytest.mark.parametrize("name", ALL_BLOCKS)
def test_commands_while_the_secondary_sequence_is_active(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str
) -> None:
    """Reading and writing dynamics and software limits works while the secondary sequence is active: Done without error.

    The primary motion stays interrupted."""
    primary = _enter_secondary_sequence(robot, sdk)
    seen = _done(robot, _valid_block(robot, name))
    assert order(seen, "Busy", "Done"), seen.flags
    assert robot.ag.State.StatusRobotArm.SecondarySequenceActive
    assert primary.CommandInterrupted, state(primary)
