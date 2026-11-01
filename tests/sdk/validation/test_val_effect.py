# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_val_effect
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Effect of the blocks without a reference test set (VAL-EFF): motion
#    targets, superimposed motions, write / read round trips, work areas
#    and kinematic calculations.
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

"""Effect of the blocks without a reference test set (area VAL-EFF).

The reference test sets do not stop at "Done": they check that the command had its effect on
the RC - MoveLinearAbsolute / MoveAxesAbsolute end at the commanded target (ReadActualPosition),
WriteToolData / WriteFrameData / WriteLoadData are read back unchanged by the Read blocks. The
same is checked here for the other blocks:

* every motion block of the planner ends at the target the specification defines for it
  (absolute target, start + distance, reference position + offset, end point of a circle; the
  approach / depart / pick-and-place offsets only shape the path, the end is TargetPosition),
* MoveSuperImposed / MoveSuperImposedDynamic add their offset to an active motion,
* Write... -> Read... round trips of registers, analog / digital outputs and work areas,
* ActivateWorkArea is reported by MonitorWorkArea,
* the kinematic calculations are consistent: inverse(forward(J)) = J, forward kinematic of the
  actual joints = ReadActualPosition, a position converted to another frame and back is unchanged.

Only facts that hold for every RC are checked (no vendor kinematics): the simulated robot uses
an identity kinematics, the checks themselves do not rely on it.
"""

from __future__ import annotations

import copy
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import ProcessingMode, SequenceFlag
from tests.bilateral import distinct_values, leaves
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import enable, move_axes
from tests.sdk.test_methodology import CLASSES_ALL, _motion, outputs, robot, start
from tests.sdk.validation.test_val_motion import NAMES as MOTION_NAMES

MOVE_CYCLES = 100
CART = ("X", "Y", "Z", "Rx", "Ry", "Rz")
JOINT = ("J1", "J2", "J3", "J4", "J5", "J6")
START = [10.0, 20.0, 30.0, 0.0, 0.0, 0.0] + [0.0] * 6
_F110 = (
    "LIB-BUG F110: CheckParameterValid of WriteIntegers rejects every negative value (UDINT range check), "
    "Values is ARRAY OF INT"
)
_F150 = (
    "LIB-BUG F150: MoveSuperImposedDynamic resets Busy / Active with the falling edge of Enable but keeps "
    "Enabled TRUE and sends nothing: the superimposed function stays ACTIVE on the RC"
)


@contextmanager
def _robot(joints: list[float] | None = None) -> Iterator[tuple[SdkSimulator, RobotTaskHarness]]:
    """SDK + RobotTask + enabled robot standing at ``joints`` (default START)."""
    with robot(enable_robot=False) as (sim, h):
        sim.set_move_cycles(MOVE_CYCLES)
        enable(h, sim)
        sim.joints = list(START if joints is None else joints)
        h.run(2)
        yield sim, h


def _block(h: RobotTaskHarness, name: str, **par: Any) -> Any:
    """Block ``name`` (parallel, no sequence) with ParCmd values ``par`` (dotted paths allowed)."""
    fb = h.add(CLASSES_ALL[name]())
    if hasattr(fb, "ProcessingMode"):
        fb.ProcessingMode = ProcessingMode.PARALLEL
    if hasattr(fb, "SequenceFlag"):
        fb.SequenceFlag = SequenceFlag.NO_SEQUENCE
    for path, value in par.items():
        owner = fb.ParCmd
        *parents, last = path.split(".")
        for p in parents:
            owner = getattr(owner, p)
        setattr(owner, last, value)
    return fb


def _execute(h: RobotTaskHarness, fb: Any, cycles: int = 100) -> Any:
    fb.Execute = True
    h.run(cycles, until=lambda: bool(fb.Done or fb.Error))
    assert fb.Done and not fb.Error, outputs(fb)
    out = copy.deepcopy(fb.OutCmd)
    fb.Execute = False
    h.run(2)
    return out


def _run(h: RobotTaskHarness, name: str, **par: Any) -> Any:
    """Execute ``name`` once; returns a copy of OutCmd."""
    return _execute(h, _block(h, name, **par))


def _values(position: Any, keys: tuple[str, ...]) -> list[float]:
    return [float(getattr(position, k)) for k in keys]


# ------------------------------------------------------------------ motion targets

# SearchHardStop ends at the hard stop, not at its target
TARGET_NAMES = [n for n in MOTION_NAMES if not n.startswith("MC_SearchHardStop")]


def _target(mv: Any, start_joints: list[float]) -> list[float]:
    """Expected J1..J6, E1 after the motion (identity of joint / Cartesian values not assumed for
    joint motions; the Cartesian targets are compared with the Cartesian position read back)."""
    p = mv.ParCmd
    name = type(mv).__name__
    if hasattr(p, "JointDistance"):
        return [a + b for a, b in zip(start_joints, _values(p.JointDistance, (*JOINT, "E1")), strict=True)]
    if hasattr(p, "JointPosition"):
        return _values(p.JointPosition, (*JOINT, "E1"))
    if hasattr(p, "ReferencePosition"):
        offset = [*_values(p.Offset, CART), 0.0]
        return [a + b for a, b in zip(_values(p.ReferencePosition, (*CART, "E1")), offset, strict=True)]
    if "Relative" in name:
        distance = p.Distance if hasattr(p, "Distance") else p.EndPoint
        return [a + b for a, b in zip(start_joints, _values(distance, (*CART, "E1")), strict=True)]
    for field in ("TargetPosition", "EndPoint", "Position"):
        if hasattr(p, field):
            return _values(getattr(p, field), (*CART, "E1"))
    raise AssertionError(f"no target of {name}")


# ReadActualPosition of the SDK returns the joint value of E1 in the wrong place (SDK-GAP, see
# test_rc_userdata_position.py::test_read_returns_external_axis): E1 is compared for Cartesian targets only
def _joint_keys(joint_motion: bool) -> tuple[str, ...]:
    return JOINT if joint_motion else (*CART, "E1")


@pytest.mark.parametrize("name", TARGET_NAMES)
def test_motion_ends_at_its_target(name: str) -> None:
    """After Done the robot stands at the target of the block (ReadActualPosition): absolute target,
    start + distance, reference position + offset or end point of the circle."""
    with _robot() as (_, h):
        start_position = _run(h, "MC_ReadActualPositionFB")
        joint_motion = hasattr(CLASSES_ALL[name]().ParCmd, "JointPosition") or name == "MC_MoveAxesRelativeFB"
        keys = _joint_keys(joint_motion)
        start_values = _values(
            start_position.ActualJointPosition if joint_motion else start_position.ActualCartesianPosition,
            keys,
        )
        mv = _motion(name, h)
        start(mv)
        h.run(6 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done and not mv.Error, outputs(mv)
        expected = _target(mv, [*start_values, 0.0][:7])[: len(keys)]
        end = _run(h, "MC_ReadActualPositionFB")
        actual = _values(end.ActualJointPosition if joint_motion else end.ActualCartesianPosition, keys)
        assert actual == pytest.approx(expected, abs=1e-3), (expected, actual)


# ------------------------------------------------------------------ superimposed motions


def _superimposed(h: RobotTaskHarness, name: str, **offset: float) -> Any:
    fb = h.add(CLASSES_ALL[name]())
    for key, value in offset.items():
        setattr(fb.ParCmd.Offset, key, value)
    fb.ParCmd.VelocityDiffRate = fb.ParCmd.AccelerationDiffRate = 100.0
    fb.ParCmd.DecelerationDiffRate = fb.ParCmd.JerkDiffRate = -1.0
    return fb


def _base_motion(h: RobotTaskHarness) -> Any:
    """MoveAxesAbsolute to J1 50, J2 20 that is Active."""
    mv = move_axes(h, 50.0, 20.0)
    mv.Execute = True
    h.run(100, until=lambda: bool(mv.Active or mv.Error))
    assert mv.Active, outputs(mv)
    return mv


def test_superimposed_offset_is_added_to_the_motion() -> None:
    """MoveSuperImposed during a motion: both Done, the robot ends at target + offset."""
    with _robot([0.0] * 12) as (_, h):
        mv = _base_motion(h)
        si = _superimposed(h, "MC_MoveSuperImposedFB", X=5.0, Y=-3.0)
        si.Execute = True
        h.run(8 * MOVE_CYCLES, until=lambda: bool((si.Done or si.Error) and (mv.Done or mv.Error)))
        assert si.Done and not si.Error, outputs(si)
        assert mv.Done and not mv.Error, outputs(mv)
        assert si.OutCmd.Progress == pytest.approx(100.0)
        position = _run(h, "MC_ReadActualPositionFB").ActualCartesianPosition
        assert (position.X, position.Y) == pytest.approx((55.0, 17.0))


def _offset_reached(h: RobotTaskHarness, fb: Any) -> None:
    h.run(4 * MOVE_CYCLES, until=lambda: bool(fb.OutCmd.OffsetReached or fb.Error))
    assert fb.OutCmd.OffsetReached and fb.Enabled and not fb.Error, outputs(fb)


def test_superimposed_dynamic_follows_the_offset() -> None:
    """MoveSuperImposedDynamic during a motion: Enabled, the robot ends at target + offset
    (OffsetReached); a changed offset moves the robot by the difference."""
    with _robot([0.0] * 12) as (_, h):
        mv = _base_motion(h)
        dyn = _superimposed(h, "MC_MoveSuperImposedDynamicFB", X=5.0)
        dyn.Enable = True
        h.run(8 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error or dyn.Error))
        assert mv.Done, outputs(mv)
        _offset_reached(h, dyn)
        assert _run(h, "MC_ReadActualPositionFB").ActualCartesianPosition.X == pytest.approx(55.0)
        dyn.ParCmd.Offset.X = 8.0
        h.run(5)
        _offset_reached(h, dyn)
        assert _run(h, "MC_ReadActualPositionFB").ActualCartesianPosition.X == pytest.approx(58.0)


@pytest.mark.xfail(strict=True, reason=_F150)
def test_superimposed_dynamic_disable() -> None:
    """Enable FALSE ends MoveSuperImposedDynamic: Enabled, Busy and Active FALSE without error."""
    with _robot([0.0] * 12) as (_, h):
        mv = _base_motion(h)
        dyn = _superimposed(h, "MC_MoveSuperImposedDynamicFB", X=5.0)
        dyn.Enable = True
        h.run(8 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error or dyn.Error))
        _offset_reached(h, dyn)
        dyn.Enable = False
        h.run(100, until=lambda: not (dyn.Enabled or dyn.Busy))
        assert not (dyn.Enabled or dyn.Busy or dyn.Active or dyn.Error), outputs(dyn)


# ------------------------------------------------------------------ write / read round trips

ROUND_TRIPS = [
    pytest.param(
        "MC_WriteIntegersFB",
        {"Index": [1, 2, 3, 4, 5, 6, 7], "Values": [11, 22, 33, 44, 55, 66, 32767]},
        "MC_ReadIntegersFB",
        {"Index": [7, 6, 5, 4, 3, 2, 1]},
        [32767, 66, 55, 44, 33, 22, 11],
        id="integers",
    ),
    pytest.param(
        "MC_WriteIntegersFB",
        {"Index": [1, 2, 3, 4, 5, 6, 7], "Values": [-1, -22, 33, -32768, 55, 66, 77]},
        "MC_ReadIntegersFB",
        {"Index": [1, 2, 3, 4, 5, 6, 7]},
        [-1, -22, 33, -32768, 55, 66, 77],
        id="integers-negative",
        marks=pytest.mark.xfail(strict=True, reason=_F110),
    ),
    pytest.param(
        "MC_WriteRealsFB",
        {"Index": [1, 2, 3, 4, 5, 6, 7], "Values": [1.5, -2.5, 3.5, 4.5, 5.5, 6.5, -7.5]},
        "MC_ReadRealsFB",
        {"Index": [7, 6, 5, 4, 3, 2, 1]},
        [-7.5, 6.5, 5.5, 4.5, 3.5, -2.5, 1.5],
        id="reals",
    ),
    pytest.param(
        "MC_WriteAnalogOutputFB",
        {"Index": 3, "Value": 4.25},
        "MC_ReadAnalogOutputFB",
        {"Index": 3},
        4.25,
        id="analog-output",
    ),
    # the bit mask selects the bits written: byte 1 keeps its upper nibble, byte 2 gets bits 0..3
    pytest.param(
        "MC_WriteDigitalOutputsFB",
        {"Index": [1, 2, 0, 0, 0], "OutputBitmask": [0xFF, 0x0F, 0, 0, 0], "Values": [0xA5, 0xF3, 0, 0, 0]},
        "MC_ReadDigitalOutputsFB",
        {"Index": [1, 2, 0, 0, 0]},
        [0xA5, 0x03],
        id="digital-outputs",
    ),
]


@pytest.mark.parametrize(("write", "par", "read", "read_par", "expected"), ROUND_TRIPS)
def test_written_value_is_read_back(
    write: str, par: dict[str, Any], read: str, read_par: dict[str, Any], expected: Any
) -> None:
    """A value written by the Write block is returned by the Read block (other order of indices)."""
    with _robot() as (_, h):
        _run(h, write, **par)
        out = _run(h, read, **read_par)
        got = out.Value if hasattr(out, "Value") else list(out.Values)[: len(expected)]
        assert got == pytest.approx(expected)


def test_digital_output_bits_outside_the_mask_are_kept() -> None:
    """A second write with a bit mask changes only the masked bits of the output byte."""
    with _robot() as (_, h):
        _run(
            h,
            "MC_WriteDigitalOutputsFB",
            Index=[1, 0, 0, 0, 0],
            OutputBitmask=[0xFF, 0, 0, 0, 0],
            Values=[0xA5, 0, 0, 0, 0],
        )
        _run(
            h,
            "MC_WriteDigitalOutputsFB",
            Index=[1, 0, 0, 0, 0],
            OutputBitmask=[0x0F, 0, 0, 0, 0],
            Values=[0x00, 0, 0, 0, 0],
        )
        assert _run(h, "MC_ReadDigitalOutputsFB", Index=[1, 0, 0, 0, 0]).Values[0] == 0xA0


# ------------------------------------------------------------------ work areas

# not part of the telegram (ST-FIX F33): DefinitionMode is not transferred and cannot be read back
NOT_TRANSFERRED = {"DefinitionMode"}


@pytest.mark.parametrize("number", [1, 7])
def test_work_area_is_read_back(number: int) -> None:
    """WriteWorkArea -> ReadWorkArea: every transferred value of the work area is returned, with
    the requested work area number."""
    with _robot() as (_, h):
        write = _block(h, "MC_WriteWorkAreaFB")
        distinct_values(write.ParCmd)
        write.ParCmd.WorkAreaNo = number
        write.ParCmd.WorkAreaData.FrameNo = 2
        _execute(h, write)
        out = _run(h, "MC_ReadWorkAreaFB", WorkAreaNo=number)
        assert out.WorkAreaNoReturn == number
        written = {p: v for p, v, _, k in leaves(write.ParCmd.WorkAreaData) if str(k) not in NOT_TRANSFERRED}
        read = {p: v for p, v, _, k in leaves(out.WorkAreaData) if str(k) not in NOT_TRANSFERRED}
        assert read == pytest.approx(written)


def test_activated_work_area_is_monitored() -> None:
    """ActivateWorkArea TRUE / FALSE is reported by a running MonitorWorkArea (ActivationState 1 / 0)."""
    with _robot() as (_, h):
        monitor = _block(h, "MC_MonitorWorkAreaFB", WorkAreaNo=3)
        monitor.Enable = True
        h.run(30, until=lambda: bool(monitor.Valid or monitor.Error))
        assert monitor.Valid and monitor.OutCmd.ActivationState == 0, outputs(monitor)
        for activate, state in ((True, 1), (False, 0)):
            _run(h, "MC_ActivateWorkAreaFB", WorkAreaNo=3, ActivateArea=activate)

            def reported(s: int = state) -> bool:
                return bool(monitor.OutCmd.ActivationState == s)

            h.run(20, until=reported)
            assert monitor.OutCmd.ActivationState == state and not monitor.Error, outputs(monitor)


# ------------------------------------------------------------------ kinematic calculations

JOINTS = {"J1": 11.0, "J2": -22.0, "J3": 33.0, "J4": 4.0, "J5": 5.0, "J6": 6.0, "E1": 7.0}


def test_inverse_of_forward_kinematic_returns_the_joints() -> None:
    """CalculateInverseKinematic of the result of CalculateForwardKinematic returns the joint values."""
    with _robot() as (_, h):
        forward = _run(
            h, "MC_CalculateForwardKinematicFB", **{f"JointPosition.{k}": v for k, v in JOINTS.items()}
        )
        inverse = _block(h, "MC_CalculateInverseKinematicFB")
        inverse.ParCmd.CartesianPosition = copy.deepcopy(forward.CartesianPosition)
        joints = _execute(h, inverse).JointPosition
        assert _values(joints, tuple(JOINTS)) == pytest.approx(list(JOINTS.values()))


def test_forward_kinematic_of_the_actual_joints_is_the_actual_position() -> None:
    """CalculateForwardKinematic of the joints ReadActualPosition returns gives its Cartesian position."""
    # E1 0: the SDK returns the joint value of E1 in the wrong place (see _joint_keys)
    with _robot([*list(JOINTS.values())[:6], *[0.0] * 6]) as (_, h):
        actual = _run(h, "MC_ReadActualPositionFB")
        forward = _block(h, "MC_CalculateForwardKinematicFB")
        forward.ParCmd.JointPosition = copy.deepcopy(actual.ActualJointPosition)
        cartesian = _execute(h, forward).CartesianPosition
        assert _values(cartesian, (*CART, "E1")) == pytest.approx(
            _values(actual.ActualCartesianPosition, (*CART, "E1"))
        )


def test_position_converted_to_another_frame_and_back_is_unchanged() -> None:
    """CalculateCartesianPosition frame 1 -> frame 2 and back returns the position (frames written
    with WriteFrameData); the position in frame 2 differs from the one in frame 1."""
    with _robot() as (_, h):
        for number, (x, y, z) in ((1, (100.0, 50.0, 0.0)), (2, (-20.0, 10.0, 5.0))):
            _run(
                h,
                "MC_WriteFrameDataFB",
                FrameNo=number,
                **{"FrameData.X": x, "FrameData.Y": y, "FrameData.Z": z},
            )
        position = {"X": 1.0, "Y": 2.0, "Z": 3.0, "Rx": 0.0, "Ry": 0.0, "Rz": 0.0}
        par = {f"CartesianPosition.{k}": v for k, v in position.items()}
        there = _run(h, "MC_CalculateCartesianPositionFB", FrameNo=1, TargetFrameNo=2, **par)
        moved = _values(there.CartesianPositionReturn, CART)
        assert moved != pytest.approx(list(position.values()))
        back = _run(
            h,
            "MC_CalculateCartesianPositionFB",
            FrameNo=2,
            TargetFrameNo=1,
            **{f"CartesianPosition.{k}": v for k, v in zip(CART, moved, strict=True)},
        )
        assert _values(back.CartesianPositionReturn, CART) == pytest.approx(list(position.values()))
