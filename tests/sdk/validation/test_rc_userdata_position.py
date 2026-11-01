# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_userdata_position
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests: ReadActualPosition and ReadActualPositionCyclic against the RC (SDK).
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

"""Validation tests: ReadActualPosition and ReadActualPositionCyclic against the RC (SDK).

Behaviour of the robot controller: returned positions, coordinate systems (requested, -1 =
currently used), robot state (enabled / disabled), sequences, processing modes with triggers and
the optional cyclic position data. The simulated robot has J1..J6 and E1 and an identity
kinematics (X..Rz = J1..J6).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import ProcessingMode, RobotLibraryInfoIdEnum, SequenceFlag
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import MOVE_CYCLES, cartesian, enable, execute, fb, move_axes, order, state

# position of the simulated robot used by most tests (J1..J6, E1..E6)
JOINTS = [300.0, 200.0, 100.0, 0.0, 0.0, 0.0] + [0.0] * 6


# ---------------------------------------------------------------- helpers


def _read(h: RobotTaskHarness, **inputs: Any) -> Any:
    """ReadActualPosition block; ``ToolNo`` / ``FrameNo`` / ``ListenerID`` go to ParCmd."""
    rp = fb(h, "MC_ReadActualPositionFB")
    for name, value in inputs.items():
        if name in ("ToolNo", "FrameNo", "ListenerID"):
            setattr(rp.ParCmd, name, value)
        else:
            setattr(rp, name, value)
    return rp


def _move_linear(h: RobotTaskHarness, x: float, tool: int = 0, frame: int = 0) -> Any:
    mv = fb(h, "MC_MoveLinearAbsoluteFB")
    cartesian(mv, x, 0.0, 0.0)
    mv.ParCmd.ToolNo, mv.ParCmd.FrameNo = tool, frame
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    return mv


def _wait_active(h: RobotTaskHarness, mv: Any) -> None:
    mv.Execute = True
    h.run(100, until=lambda: bool(mv.Active or mv.Error))
    assert mv.Active and not mv.Error, state(mv)


def _finish(h: RobotTaskHarness, mv: Any) -> None:
    h.run(10 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    mv.Execute = False
    h.run(2)


def _cart(pos: Any) -> tuple[float, ...]:
    return (pos.X, pos.Y, pos.Z, pos.Rx, pos.Ry, pos.Rz)


@contextmanager
def _configured(sdk: SdkSimulator, setup: Callable[[RobotTaskHarness], None]) -> Iterator[RobotTaskHarness]:
    """RobotTask initialized with a configuration changed by ``setup`` (before the start-up)."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        setup(h)
        h.run(200, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, (hex(h.rt.ErrorID), h.history[-3:])
        yield h


def _optional(*names: str) -> Callable[[RobotTaskHarness], None]:
    def setup(h: RobotTaskHarness) -> None:
        for name in names:
            setattr(h.cfg.Rob.OptionalCyclic, name, True)

    return setup


def _cyclic(h: RobotTaskHarness, **par: Any) -> Any:
    """ReadActualPositionCyclic enabled with ``par`` (ParCmd); waits for Enabled."""
    cy = fb(h, "MC_ReadActualPositionCyclicFB")
    for name, value in par.items():
        setattr(cy.ParCmd, name, value)
    cy.Enable = True
    h.run(30, until=lambda: bool(cy.Enabled or cy.Error))
    assert cy.Enabled and not cy.Error, state(cy)
    h.run(2)
    return cy


# ---------------------------------------------------------------- ReadActualPosition: values and state


@pytest.mark.parametrize("motion", ["linear", "axes"])
def test_read_after_motion_returns_target(robot: RobotTaskHarness, sdk: SdkSimulator, motion: str) -> None:
    """After a completed motion ReadActualPosition returns the target in joint and Cartesian values.

    Default inputs (parallel, no sequence, tool 0, frame 0); flags Busy before Done and Valid.
    """
    enable(robot)
    if motion == "linear":
        mv = _move_linear(robot, 150.0)
    else:
        mv = move_axes(robot, 20.0, 30.0, 40.0)
    assert execute(robot, mv).final["Done"]
    rp = _read(robot)
    seen = execute(robot, rp, reset=False)
    assert order(seen, "Busy", "Done") and rp.Valid and not rp.Error, seen.flags
    joints = rp.OutCmd.ActualJointPosition
    expected = (150.0, 0.0, 0.0) if motion == "linear" else (20.0, 30.0, 40.0)
    assert (joints.J1, joints.J2, joints.J3) == pytest.approx(expected)
    assert _cart(rp.OutCmd.ActualCartesianPosition)[:3] == pytest.approx(expected)  # identity kinematics
    assert (rp.OutCmd.ToolNoReturn, rp.OutCmd.FrameNoReturn) == (0, 0)


def test_read_parallel_while_robot_disabled(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A parallel ReadActualPosition is executed while the robot is not enabled: Done, Valid, position.

    Reading does not need power; the robot stands at a known joint position.
    """
    sdk.joints = JOINTS
    assert not robot.user_data.Enabled
    rp = _read(robot, ProcessingMode=ProcessingMode.PARALLEL, SequenceFlag=SequenceFlag.NO_SEQUENCE)
    seen = execute(robot, rp, reset=False)
    assert order(seen, "Busy", "Done") and rp.Valid and not rp.Error, seen.flags
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(300.0)
    assert _cart(rp.OutCmd.ActualCartesianPosition) == pytest.approx(tuple(JOINTS[:6]))


def test_read_in_primary_sequence_while_disabled_is_interrupted(robot: RobotTaskHarness) -> None:
    """A buffered ReadActualPosition in the primary sequence is interrupted while the robot is disabled.

    The sequence cannot run without power: CommandInterrupted with InfoID 16#6F02, no error, no Done.
    """
    rp = _read(robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    seen = execute(robot, rp, cycles=60, reset=False)
    robot.run(60, until=lambda: bool(rp.CommandInterrupted))
    assert rp.CommandInterrupted and not rp.Error and not rp.Done, state(rp)
    assert rp.InfoID == RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED
    assert seen.flags[0] == "Busy"


@pytest.mark.parametrize(
    ("mode", "flag"),
    [
        (ProcessingMode.PARALLEL, SequenceFlag.NO_SEQUENCE),
        (ProcessingMode.BUFFERED, SequenceFlag.PRIMARY_SEQUENCE),
    ],
    ids=["parallel-no-sequence", "buffered-primary"],
)
def test_read_with_sequence_settings(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: ProcessingMode, flag: SequenceFlag
) -> None:
    """ReadActualPosition with the valid ProcessingMode / SequenceFlag pairs ends with Done and Valid.

    Robot enabled and idle, primary sequence active; the secondary sequence stays inactive.
    """
    enable(robot)
    sdk.joints = JOINTS
    rp = _read(robot, ProcessingMode=mode, SequenceFlag=flag)
    seen = execute(robot, rp, reset=False)
    assert order(seen, "Busy", "Done") and rp.Valid and not rp.Error, seen.flags
    assert not robot.user_data.SecondarySequenceActive
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(300.0)


@pytest.mark.parametrize(
    ("tool", "frame"), [(0, 0), (1, 0), (0, 1), (4, 3)], ids=["default", "tool1", "frame1", "tool4-frame3"]
)
def test_read_returns_requested_coordinate_system(
    robot: RobotTaskHarness, sdk: SdkSimulator, tool: int, frame: int
) -> None:
    """ReadActualPosition reports the requested tool and frame numbers with the position.

    Done and Valid; ToolNoReturn / FrameNoReturn equal the requested numbers; joint position unchanged.
    """
    sdk.joints = JOINTS
    rp = _read(robot, ToolNo=tool, FrameNo=frame)
    seen = execute(robot, rp, reset=False)
    assert order(seen, "Busy", "Done") and rp.Valid, seen.flags
    assert (rp.OutCmd.ToolNoReturn, rp.OutCmd.FrameNoReturn) == (tool, frame)
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(300.0)


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated RC returns the flange position in the world frame for every "
    "ToolNo / FrameNo; tool and frame data are not applied to the returned Cartesian position "
    "(spec ReadActualPosition: position in the requested TCS / UCS).",
)
@pytest.mark.parametrize("target", ["tool", "frame"])
def test_read_position_is_transformed_into_tool_and_frame(
    robot: RobotTaskHarness, sdk: SdkSimulator, target: str
) -> None:
    """The Cartesian position is expressed in the requested tool / user frame.

    RC data (like a teach pendant): frame 1 shifted by X +100 / Y +50, tool 1 with Z +50, robot at
    X 300 Y 200 Z 100 without rotation. Expected: frame 1 gives X 200 / Y 150, tool 1 gives Z 150.
    """
    sdk.rc_change(sdk.RC_FRAME, 1, [100.0, 50.0, 0.0, 0.0, 0.0, 0.0])
    sdk.rc_change(sdk.RC_TOOL, 1, [0.0, 0.0, 50.0, 0.0, 0.0, 0.0])
    robot.run(50)
    sdk.joints = JOINTS
    rp = _read(robot, ToolNo=1 if target == "tool" else 0, FrameNo=1 if target == "frame" else 0)
    assert execute(robot, rp, reset=False).final["Done"]
    xyz = _cart(rp.OutCmd.ActualCartesianPosition)[:3]
    expected = (300.0, 200.0, 150.0) if target == "tool" else (200.0, 150.0, 100.0)
    assert xyz == pytest.approx(expected)


@pytest.mark.parametrize("kind", ["tool", "frame"])
def test_read_minus_one_returns_coordinate_system_of_running_motion(
    robot: RobotTaskHarness, sdk: SdkSimulator, kind: str
) -> None:
    """ToolNo / FrameNo -1 returns the tool / frame currently used by the RC (the running motion).

    Two MoveLinear one after another with tool (frame) 4 and then 3; a read during each motion
    reports 4 and then 3.
    """
    enable(robot)
    for number, x in ((4, 50.0), (3, 100.0)):
        mv = _move_linear(robot, x, **{kind: number})
        _wait_active(robot, mv)
        rp = _read(robot, **{"ToolNo" if kind == "tool" else "FrameNo": -1})
        seen = execute(robot, rp, reset=False)
        assert order(seen, "Busy", "Done") and rp.Valid, seen.flags
        got = rp.OutCmd.ToolNoReturn if kind == "tool" else rp.OutCmd.FrameNoReturn
        assert got == number
        _finish(robot, mv)


@pytest.mark.parametrize("kind", ["tool", "frame"])
def test_read_explicit_number_during_motion_with_other_number(
    robot: RobotTaskHarness, sdk: SdkSimulator, kind: str
) -> None:
    """An explicit ToolNo / FrameNo 4 is returned even while the motion uses number 6."""
    enable(robot)
    mv = _move_linear(robot, 60.0, **{kind: 6})
    _wait_active(robot, mv)
    rp = _read(robot, **{"ToolNo" if kind == "tool" else "FrameNo": 4})
    assert execute(robot, rp, reset=False).final["Done"]
    got = rp.OutCmd.ToolNoReturn if kind == "tool" else rp.OutCmd.FrameNoReturn
    assert got == 4
    _finish(robot, mv)


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK response of ReadActualPosition has 2 reserved bytes before the "
    "extended axes (not in the spec table), so the joint value of E1 arrives as Cartesian E2 "
    "(tests/sdk/test_payload_sdk.py KNOWN).",
)
def test_read_returns_external_axis(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """The external axis E1 is returned in the Cartesian and the joint position; missing axes are 0.0.

    Simulated robot with J1..J6 and E1 = -10.0 (E2..E6 do not exist).
    """
    sdk.joints = [*JOINTS[:6], -10.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    rp = _read(robot)
    assert execute(robot, rp, reset=False).final["Done"]
    cart, joint = rp.OutCmd.ActualCartesianPosition, rp.OutCmd.ActualJointPosition
    assert cart.E1 == pytest.approx(-10.0)
    assert joint.E1 == pytest.approx(-10.0)
    assert (cart.E2, cart.E3, cart.E4, cart.E5, cart.E6) == (0.0,) * 5
    assert (joint.E2, joint.E3, joint.E4, joint.E5, joint.E6) == (0.0,) * 5


def test_read_buffered_in_primary_while_secondary_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A read buffered into the primary sequence while the secondary one is active waits for it.

    SetSequence(secondary); ReadActualPosition (buffered, primary) stays buffered; SetSequence(primary)
    interrupts it (CommandInterrupted, InfoID <> 0); GroupContinue executes it: Done and Valid.
    """
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert robot.user_data.SecondarySequenceActive
    rp = _read(robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    rp.Execute = True
    robot.run(20)
    assert rp.Busy and rp.CommandBuffered and not rp.Done, state(rp)
    seq.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    robot.run(20, until=lambda: bool(rp.CommandInterrupted))
    assert not robot.user_data.SecondarySequenceActive
    assert rp.CommandInterrupted and rp.InfoID != 0 and not rp.Done, state(rp)
    cont = fb(robot, "MC_GroupContinueFB")
    execute(robot, cont, reset=False)
    robot.run(50, until=lambda: bool(rp.Done or rp.Error))
    assert rp.Done and rp.Valid and not rp.Error, state(rp)


def test_two_reads_in_the_same_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Two ReadActualPosition instances started in the same cycle both end with Done and Valid.

    Instance 2 requests frame 1 and gets frame 1; both return the same joint position.
    """
    sdk.joints = JOINTS
    a = _read(robot)
    b = _read(robot, FrameNo=1)
    a.Execute = b.Execute = True
    robot.run(50, until=lambda: bool((a.Done or a.Error) and (b.Done or b.Error)))
    assert a.Done and a.Valid and b.Done and b.Valid, (state(a), state(b))
    assert b.OutCmd.FrameNoReturn == 1
    assert a.OutCmd.ActualJointPosition.J1 == b.OutCmd.ActualJointPosition.J1 == pytest.approx(300.0)


# ---------------------------------------------------------------- ReadActualPosition: continuous / triggers


def _continuous(h: RobotTaskHarness, **inputs: Any) -> Any:
    rp = _read(h, ProcessingMode=ProcessingMode.CONTINUOUS, SequenceFlag=SequenceFlag.NO_SEQUENCE, **inputs)
    rp.Execute = True
    h.run(30, until=lambda: bool(rp.Valid or rp.Error))
    assert rp.Valid and rp.Busy and not rp.Done and not rp.Error, state(rp)
    return rp


def test_continuous_read_survives_disable(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A continuous read keeps running when the robot is disabled: Valid, Busy, no Done, no error."""
    en = enable(robot)
    rp = _continuous(robot)
    en.Enable = False
    robot.run(50, until=lambda: not robot.user_data.Enabled)
    assert not robot.user_data.Enabled
    sdk.joints = [12.0] + [0.0] * 11
    robot.run(10)
    assert rp.Valid and rp.Busy and not rp.Done and not rp.Error, state(rp)
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(12.0)


def test_continuous_read_new_rising_edge_keeps_running(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A second rising edge of Execute on a running continuous read does not end it: Busy and Valid stay.

    No Done and no error; the values are still updated afterwards.
    """
    rp = _continuous(robot)
    rp.Execute = False
    robot.run(2)
    rp.Execute = True
    robot.run(10)
    sdk.joints = [5.0] + [0.0] * 11
    robot.run(10)
    assert rp.Busy and rp.Valid and not rp.Done and not rp.Error, state(rp)
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(5.0)


def test_continuous_read_in_frame_follows_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A continuous read in frame 1 follows a running MoveDirect and keeps reporting frame 1."""
    enable(robot)
    rp = _continuous(robot, FrameNo=1)
    mv = fb(robot, "MC_MoveDirectAbsoluteFB")
    cartesian(mv, 80.0, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    mv.Execute = True
    values = set()
    for _ in range(3 * MOVE_CYCLES):
        robot.run(1)
        values.add(round(rp.OutCmd.ActualJointPosition.J1, 1))
        assert rp.Valid and rp.OutCmd.FrameNoReturn == 1, state(rp)
        if mv.Done:
            break
    assert mv.Done and len(values) > 5 and max(values) == pytest.approx(80.0)


def _trigger(h: RobotTaskHarness, emitter: int = 1) -> Any:
    tu = fb(h, "MC_SetTriggerUserFB")
    tu.ParCmd.EmitterID = emitter
    return tu


def test_trigger_once_reads_after_the_trigger(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """TRIGGER_ONCE with ListenerID 1 waits for the trigger, then reads once: Done, Valid, counter 1.

    While waiting: Busy, CommandBuffered, ParameterAccepted, InvocationCounter 0, no Done / Valid.
    """
    sdk.joints = JOINTS
    rp = _read(robot, ProcessingMode=ProcessingMode.TRIGGER_ONCE, ListenerID=1)
    rp.Execute = True
    robot.run(20)
    assert rp.Busy and rp.CommandBuffered and rp.ParameterAccepted, state(rp)
    assert not (rp.Done or rp.Valid) and rp.OutCmd.InvocationCounter == 0
    tu = _trigger(robot)
    tu.Execute = True
    robot.run(30, until=lambda: bool(rp.Done or rp.Error))
    assert rp.Done and rp.Valid and not rp.Busy and not rp.Error, state(rp)
    assert rp.OutCmd.InvocationCounter == 1
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(300.0)


def test_trigger_multiple_reads_at_each_trigger_and_is_deactivated(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """TRIGGER_MULTIPLE reads at every trigger (Valid, counter 1, 2; no Done) until DEACTIVATE ends it.

    DEACTIVATE is a new rising edge with ProcessingMode 9 on the same instance: Done, Busy FALSE.
    """
    rp = _read(robot, ProcessingMode=ProcessingMode.TRIGGER_MULTIPLE, ListenerID=1)
    rp.Execute = True
    robot.run(20)
    assert rp.Busy and rp.CommandBuffered and not rp.Valid, state(rp)
    tu = _trigger(robot)
    for count in (1, 2):
        tu.Execute = True

        def counted(c: int = count) -> bool:
            return bool(rp.OutCmd.InvocationCounter == c)

        robot.run(30, until=counted)
        assert rp.OutCmd.InvocationCounter == count and rp.Valid and rp.Busy and not rp.Done, state(rp)
        tu.Execute = False
        robot.run(2)
    rp.Execute = False
    robot.run(2)
    rp.ProcessingMode = ProcessingMode.DEACTIVATE
    rp.Execute = True
    robot.run(50, until=lambda: bool(rp.Done or rp.Error))
    assert rp.Done and not rp.Busy and not rp.Error, state(rp)


# ---------------------------------------------------------------- ReadActualPositionCyclic


@pytest.mark.parametrize(("tool", "frame"), [(0, 0), (1, 0), (0, 1)], ids=["default", "tool1", "frame1"])
def test_cyclic_cartesian_position(sdk: SdkSimulator, tool: int, frame: int) -> None:
    """Cyclic Cartesian position: Enabled, ReadingCartesianPosition, position and requested coordinate system.

    Telegram configured with the Cartesian position; CurrentCoordinateSystem is 0 / 0 (no motion yet).
    """
    with _configured(sdk, _optional("UseCartesianPosition")) as h:
        sdk.joints = JOINTS
        cy = _cyclic(h, ReadCartesianPosition=True, ToolNo=tool, FrameNo=frame)
        h.run(3)
        out = cy.OutCmd
        assert out.ReadingCartesianPosition and h.user_data.ReadingCartesianPosition
        assert _cart(out.CartesianPosition) == pytest.approx(tuple(JOINTS[:6]))
        assert (out.CoordinateSystem.ToolNo, out.CoordinateSystem.FrameNo) == (tool, frame)
        assert (out.CurrentCoordinateSystem.ToolNo, out.CurrentCoordinateSystem.FrameNo) == (0, 0)


@pytest.mark.parametrize("field", ["ToolNo", "FrameNo"])
def test_cyclic_coordinate_system_changed_online(sdk: SdkSimulator, field: str) -> None:
    """Changing ToolNo / FrameNo of an enabled cyclic read switches the coordinate system without restart.

    Enabled drops (Busy) while the change is applied and comes back with CoordinateSystem = 1.
    """
    with _configured(sdk, _optional("UseCartesianPosition")) as h:
        cy = _cyclic(h, ReadCartesianPosition=True)
        setattr(cy.ParCmd, field, 1)
        seen = []
        for _ in range(30):
            h.run(1)
            seen.append(bool(cy.Enabled))
            if seen[-1] and getattr(cy.OutCmd.CoordinateSystem, field) == 1:
                break
        assert False in seen and seen[-1], seen
        assert getattr(cy.OutCmd.CoordinateSystem, field) == 1 and not cy.Error


@pytest.mark.parametrize("field", ["ToolNo", "FrameNo"])
def test_cyclic_minus_one_without_motion_is_zero(sdk: SdkSimulator, field: str) -> None:
    """ToolNo / FrameNo -1 of the cyclic read after start-up (no motion yet) reports 0."""
    with _configured(sdk, _optional("UseCartesianPosition")) as h:
        cy = _cyclic(h, ReadCartesianPosition=True, **{field: -1})
        assert getattr(cy.OutCmd.CoordinateSystem, field) == 0
        assert getattr(cy.OutCmd.CurrentCoordinateSystem, field) == 0


@pytest.mark.parametrize("field", ["ToolNo", "FrameNo"])
@pytest.mark.parametrize("requested", [-1, 4], ids=["current", "fixed4"])
def test_cyclic_coordinate_systems_follow_motions(sdk: SdkSimulator, field: str, requested: int) -> None:
    """During two motions with tool (frame) 3 and then 5 the current coordinate system follows them.

    Requested -1: CoordinateSystem and CurrentCoordinateSystem show 3, then 5.
    Requested 4: CoordinateSystem stays 4, CurrentCoordinateSystem shows 3, then 5.
    """
    with _configured(sdk, _optional("UseCartesianPosition")) as h:
        cy = _cyclic(h, ReadCartesianPosition=True, **{field: requested})
        enable(h)
        kind = "tool" if field == "ToolNo" else "frame"
        for number, x in ((3, 40.0), (5, 80.0)):
            mv = _move_linear(h, x, **{kind: number})
            _wait_active(h, mv)
            h.run(3)
            assert cy.Enabled and not cy.Error, state(cy)
            assert getattr(cy.OutCmd.CurrentCoordinateSystem, field) == number
            assert getattr(cy.OutCmd.CoordinateSystem, field) == (number if requested == -1 else requested)
            _finish(h, mv)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F123: MC_ReadActualPositionCyclicFB copies only J1..J6 of the cyclic joint position "
    "(OnExecRun step 1), the first external axis E1 (part of 'Receive joint position', spec "
    "optional cyclic data) stays 0.0 although AxesGroup.CyclicOptional has it.",
)
def test_cyclic_joint_position(sdk: SdkSimulator) -> None:
    """Cyclic joint position: ReadingJointPosition, J1..J6 and E1 equal the robot position."""
    with _configured(sdk, _optional("UseJointPosition")) as h:
        sdk.joints = JOINTS[:6] + [-10.0] + [0.0] * 5
        cy = _cyclic(h, ReadJointPosition=True)
        h.run(3)
        joints = cy.OutCmd.JointPosition
        assert cy.OutCmd.ReadingJointPosition and h.user_data.ReadingJointPosition
        assert (joints.J1, joints.J2, joints.J3, joints.J4, joints.J5, joints.J6) == pytest.approx(
            tuple(JOINTS[:6])
        )
        assert h.ag.CyclicOptional.RobToPlc.JointPosition.E1 == pytest.approx(-10.0)
        assert joints.E1 == pytest.approx(-10.0)


@pytest.mark.parametrize("kind", ["cartesian", "joint"])
def test_cyclic_extended_axes_missing_axes_are_zero(sdk: SdkSimulator, kind: str) -> None:
    """Cyclic extended position (E2..E6): Reading flag set, the axes the robot does not have report 0.0.

    The values are also in the UserData (ReadingExt flag and extended position).
    """
    opt, par = (
        ("UseCartesianPositionExt", "ReadCartesianPositionExt")
        if kind == "cartesian"
        else (
            "UseJointPositionExt",
            "ReadJointPositionExt",
        )
    )
    with _configured(sdk, _optional(opt)) as h:
        sdk.joints = JOINTS[:6] + [-10.0] + [0.0] * 5
        cy = _cyclic(h, **{par: True})
        h.run(3)
        if kind == "cartesian":
            ext, reading, ud = (
                cy.OutCmd.CartesianPositionExt,
                cy.OutCmd.ReadingCartesianPositionExt,
                h.user_data.ReadingExtCartesianPosition,
            )
            ud_ext: Any = h.user_data.ExtCartesianPosition
        else:
            ext, reading, ud = (
                cy.OutCmd.JointPositionExt,
                cy.OutCmd.ReadingJointPositionExt,
                h.user_data.ReadingExtJointPosition,
            )
            ud_ext = h.user_data.ExtJointPosition
        assert reading and ud and not cy.Error, state(cy)
        assert (ext.E2, ext.E3, ext.E4, ext.E5, ext.E6) == (0.0,) * 5
        assert (ud_ext.E2, ud_ext.E6) == (0.0, 0.0)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F124: with Rob.OptionalCyclic.UseCartesianPosition and UseCartesianPositionExt both "
    "set, MC_RobotTaskFB.CheckParameterValid (MC_RobotTaskFB.py ~1113) clears UseCartesianPositionExt "
    "in its copy of ParCfg; the start-up then never completes (no CMDsEnabled, no error, no timeout).",
)
def test_cyclic_all_position_data(sdk: SdkSimulator) -> None:
    """All four cyclic position data activated: the RobotTask starts and every output follows the robot.

    Cartesian, extended Cartesian, joint and extended joint position; non-existing axes 0.0.
    """
    names = ("UseCartesianPosition", "UseCartesianPositionExt", "UseJointPosition", "UseJointPositionExt")
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        _optional(*names)(h)
        h.run(300, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, (hex(h.rt.ErrorID), h.history[-3:])
        sdk.joints = JOINTS
        cy = _cyclic(
            h,
            ReadCartesianPosition=True,
            ReadCartesianPositionExt=True,
            ReadJointPosition=True,
            ReadJointPositionExt=True,
        )
        out = cy.OutCmd
        assert out.ReadingCartesianPosition and out.ReadingCartesianPositionExt
        assert out.ReadingJointPosition and out.ReadingJointPositionExt
        assert _cart(out.CartesianPosition) == pytest.approx(tuple(JOINTS[:6]))


def test_cyclic_without_any_data(sdk: SdkSimulator) -> None:
    """Cyclic read enabled with no position data selected: Enabled, all Reading flags FALSE, values 0."""
    with _configured(sdk, _optional("UseCartesianPosition", "UseJointPosition")) as h:
        sdk.joints = JOINTS
        cy = _cyclic(h)
        out = cy.OutCmd
        assert not (out.ReadingCartesianPosition or out.ReadingCartesianPositionExt)
        assert not (out.ReadingJointPosition or out.ReadingJointPositionExt)
        assert _cart(out.CartesianPosition) == (0.0,) * 6 and out.JointPosition.J1 == 0.0


def test_cyclic_disabled_resets_outputs(sdk: SdkSimulator) -> None:
    """Disabling the cyclic read resets its outputs; the AxesGroup keeps receiving the cyclic position."""
    with _configured(sdk, _optional("UseCartesianPosition", "UseJointPosition")) as h:
        cy = _cyclic(h, ReadCartesianPosition=True, ReadJointPosition=True)
        cy.Enable = False
        h.run(5)
        assert not (cy.Enabled or cy.Busy or cy.Error), state(cy)
        assert not cy.OutCmd.ReadingCartesianPosition and cy.OutCmd.CartesianPosition.X == 0.0
        sdk.joints = [33.0] + [0.0] * 11
        h.run(3)
        assert h.ag.CyclicOptional.RobToPlc.CartesianPosition.X == pytest.approx(33.0)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F125: no warning when the cyclic read is disabled although the RC keeps sending the "
    "data; WARN_CYCLIC_DATA_DISABLED_STILL_ACTIVE (16#7303) exists in the enum but is never set "
    "(MC_ReadActualPositionCyclicFB, MC_RobotTaskFB).",
)
def test_cyclic_disabled_reports_data_still_sent(sdk: SdkSimulator) -> None:
    """Disabling the cyclic read reports warning 16#7303: the position data are still transmitted."""
    from srci.types import RobotLibraryWarningIdEnum as W

    with _configured(sdk, _optional("UseCartesianPosition")) as h:
        cy = _cyclic(h, ReadCartesianPosition=True)
        cy.Enable = False
        h.run(5)
        codes = {int(cy.WarningID), int(h.rt.WarningID)}
        codes |= {int(m.MessageCode) for m in h.ag.MessageLog.Messages}
        assert int(W.WARN_CYCLIC_DATA_DISABLED_STILL_ACTIVE) in codes


@pytest.mark.parametrize("kind", ["cartesian", "joint"])
def test_cyclic_data_in_user_data(sdk: SdkSimulator, kind: str) -> None:
    """The cyclic position is mirrored into the UserData (Reading flag, position) with its coordinate systems.

    Cartesian with tool 1: UserData CoordinateSystem tool 1, current tool 0. Joint: J1..J6.
    """
    opt = "UseCartesianPosition" if kind == "cartesian" else "UseJointPosition"
    with _configured(sdk, _optional(opt)) as h:
        sdk.joints = JOINTS
        if kind == "cartesian":
            _cyclic(h, ReadCartesianPosition=True, ToolNo=1)
            ud: Any = h.user_data.CartesianPosition
            assert h.user_data.ReadingCartesianPosition
            assert _cart(ud) == pytest.approx(tuple(JOINTS[:6]))
            # the coordinate systems of the cyclic data are kept in the AxesGroup (not in UserData)
            cyc = h.ag.CyclicOptional.RobToPlc.CartesianPosition
            assert (cyc.CoordinateSystem.ToolNo, cyc.CurrentCoordinateSystem.ToolNo) == (1, 0)
        else:
            _cyclic(h, ReadJointPosition=True)
            ud = h.user_data.JointPosition
            assert h.user_data.ReadingJointPosition
            assert (ud.J1, ud.J2, ud.J3) == pytest.approx(tuple(JOINTS[:3]))


@pytest.mark.parametrize(("tool", "frame"), [(0, 0), (1, 0), (0, 1)], ids=["default", "tool1", "frame1"])
def test_cyclic_and_acyclic_read_match(sdk: SdkSimulator, tool: int, frame: int) -> None:
    """ReadActualPositionCyclic and ReadActualPosition return the same position and coordinate system.

    Robot moved to a position first (MoveAxes), then both blocks read with the same tool / frame.
    """
    with _configured(sdk, _optional("UseCartesianPosition", "UseJointPosition")) as h:
        enable(h)
        assert execute(h, move_axes(h, 25.0, -15.0, 35.0)).final["Done"]
        cy = _cyclic(h, ReadCartesianPosition=True, ReadJointPosition=True, ToolNo=tool, FrameNo=frame)
        rp = _read(h, ToolNo=tool, FrameNo=frame)
        assert execute(h, rp, reset=False).final["Done"]
        out = rp.OutCmd
        assert _cart(cy.OutCmd.CartesianPosition) == pytest.approx(_cart(out.ActualCartesianPosition))
        assert cy.OutCmd.JointPosition.J2 == pytest.approx(out.ActualJointPosition.J2)
        assert (cy.OutCmd.CoordinateSystem.ToolNo, cy.OutCmd.CoordinateSystem.FrameNo) == (
            out.ToolNoReturn,
            out.FrameNoReturn,
        )
        cfg = cy.OutCmd.CartesianPosition.Config
        assert (cfg.Shoulder, cfg.Elbow, cfg.Wrist) == (
            out.ActualCartesianPosition.Config.Shoulder,
            out.ActualCartesianPosition.Config.Elbow,
            out.ActualCartesianPosition.Config.Wrist,
        )
