"""Core function blocks (transpiled from the PLC library) against the SRCI SDK.

Every test starts with an initialized RobotTask (``robot`` fixture); the function blocks are
called in every cycle before the RobotTask like in a PLC program (``RobotTaskHarness.add``).
The simulated robot of the SDK harness moves linearly within ``set_move_cycles`` cycles and
uses an identity kinematics (X..Rz = J1..J6).
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.iec.rt import copy_into
from srci.sim.sdk import SdkSimulator, sdk_transport
from srci.types import JogMode, ProcessingMode, RobotLibraryErrorIdEnum, SequenceFlag
from srci.types.iec import new_instance
from tests.robot_task_harness import SIZE, RobotTaskHarness

MOVE_CYCLES = 20


@pytest.fixture(autouse=True)
def sdk_parameters() -> Iterator[None]:
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@pytest.fixture
def robot(sdk: SdkSimulator) -> Iterator[RobotTaskHarness]:
    """Initialized RobotTask, commands enabled."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, h.history
        yield h


def fb(h: RobotTaskHarness, name: str, **inputs: Any) -> Any:
    """Creates the function block ``name`` (e.g. ``"MC_GroupResetFB"``) and adds it to the program."""
    return h.add(new_instance(name), **inputs)


def state(block: Any) -> dict[str, Any]:
    names = (
        "Busy",
        "Done",
        "CommandBuffered",
        "Enabled",
        "Valid",
        "Error",
        "ErrorID",
        "CommandAborted",
        "CommandInterrupted",
    )
    return {n: getattr(block, n) for n in names if hasattr(block, n)}


def execute(h: RobotTaskHarness, block: Any, cycles: int = 100, reset: bool = True) -> int:
    """Rising edge on ``Execute``, run until Done or Error; returns the cycles needed."""
    block.Execute = True
    n = h.run(cycles, until=lambda: bool(block.Done or block.Error))
    assert block.Done and not block.Error, (state(block), hex(block.ErrorID), h.history)
    if reset:
        block.Execute = False
        h.run(2)
    return n


def enable(h: RobotTaskHarness, sdk: SdkSimulator) -> Any:
    execute(h, fb(h, "MC_GroupResetFB"))
    en = fb(h, "MC_EnableRobotFB", Enable=True)
    h.run(100, until=lambda: bool(en.Enabled or en.Error))
    assert en.Enabled and not en.Error, state(en)
    assert sdk.enabled
    return en


def move_axes(h: RobotTaskHarness, j1: float, j2: float = 0.0, **inputs: Any) -> Any:
    mv = fb(h, "MC_MoveAxesAbsoluteFB", **inputs)
    mv.ParCmd.JointPosition.J1 = j1
    mv.ParCmd.JointPosition.J2 = j2
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = -1.0  # optional; the SDK only accepts "not set" (0x8E03)
    mv.ParCmd.JerkRate = -1.0
    return mv


# ---------------------------------------------------------------- general


def test_group_reset(robot: RobotTaskHarness) -> None:
    execute(robot, fb(robot, "MC_GroupResetFB"))


def test_enable_and_disable_robot(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    en = enable(robot, sdk)
    en.Enable = False
    robot.run(100, until=lambda: not en.Enabled and not en.Busy)
    assert not en.Enabled and not en.Error, state(en)
    assert not sdk.enabled


def test_enable_robot_fails(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    sdk.set_fail_enable(True)
    execute(robot, fb(robot, "MC_GroupResetFB"))
    en = fb(robot, "MC_EnableRobotFB", Enable=True)
    robot.run(200, until=lambda: bool(en.Enabled or en.Error))
    assert en.Error and not en.Enabled, state(en)
    # the SDK resets the RI state on the fatal error -> the RobotTask loses the initialization
    assert en.ErrorID == RobotLibraryErrorIdEnum.ERR_COMMANDS_NOT_ENABLED
    assert robot.rt.Error and robot.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0x80A2
    # ST-FIX F29: Initialized / CMDsEnabled are reset with the error
    assert not robot.rt.Initialized and not robot.ag.State.CMDsEnabled


def test_sequence_number_overflow(robot: RobotTaskHarness) -> None:
    """ST-FIX F56: 600 commands one after the other (more than 255 telegram sequences): every
    command gets its response. Before the fix the Seq number wrapped from 254 to 0 and the
    response of that sequence was ignored (the block hung)."""
    block = fb(robot, "MC_ReadRobotDataFB")
    for run in range(600):
        block.Execute = True
        robot.run(100, until=lambda: bool(block.Done or block.Error))
        assert block.Done and not block.Error, (run, state(block), hex(block.ErrorID))
        block.Execute = False
        robot.run(1)


def test_change_speed_override(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    ov = fb(robot, "MC_ChangeSpeedOverrideFB")
    ov.ParCmd.Override = 50.0
    execute(robot, ov)
    assert sdk.override == 50.0


def test_read_robot_data(robot: RobotTaskHarness) -> None:
    rd = fb(robot, "MC_ReadRobotDataFB")
    execute(robot, rd, reset=False)
    assert rd.OutCmd.RCManufacturer == "SRCI_PY SimRobot"
    assert rd.OutCmd.RCSupportedFunctions.MoveAxesAbsolute
    assert rd.OutCmd.AxisJointUsed.J1 and rd.OutCmd.AxisJointUsed.J6
    assert rd.OutCmd.InterpreterCycleTime == 10  # ST-FIX F30: UINT, the ST read a USINT (0)


def test_exchange_configuration(robot: RobotTaskHarness) -> None:
    ex = fb(robot, "MC_ExchangeConfigurationFB", Enable=True)
    copy_into(ex.ParCmd, robot.rt._exchangeConfiguration.ParCmd)  # the configuration of the RobotTask
    robot.run(100, until=lambda: bool(ex.OutCmd.HighestToolIndex or ex.Error))
    assert ex.Enabled and not ex.Error, state(ex)
    assert ex.OutCmd.HighestToolIndex == 19
    assert ex.OutCmd.HighestFrameIndex == 19 and ex.OutCmd.HighestLoadIndex == 19


def test_set_sequence(robot: RobotTaskHarness) -> None:
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    execute(robot, seq)
    seq.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
    execute(robot, seq)


def test_set_sequence_invalid_parameter(robot: RobotTaskHarness) -> None:
    seq = fb(robot, "MC_SetSequenceFB", Execute=True)
    robot.run(10, until=lambda: bool(seq.Error))
    assert seq.Error and seq.ErrorID == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD


def test_read_messages(robot: RobotTaskHarness) -> None:
    rm = fb(robot, "MC_ReadMessagesFB", Enable=True)
    robot.run(100, until=lambda: bool(rm.Valid or rm.Error))
    assert rm.Valid and not rm.Error, state(rm)


# ---------------------------------------------------------------- motion


def test_read_actual_position(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    sdk.joints = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] + [0.0] * 6
    rp = fb(robot, "MC_ReadActualPositionFB")
    execute(robot, rp, reset=False)
    pos = rp.OutCmd.ActualJointPosition
    assert (pos.J1, pos.J2, pos.J6) == (1.0, 2.0, 6.0)
    assert rp.OutCmd.ActualCartesianPosition.X == 1.0  # identity kinematics


def test_read_actual_position_valid(robot: RobotTaskHarness) -> None:
    rp = fb(robot, "MC_ReadActualPositionFB")
    execute(robot, rp, reset=False)
    assert rp.Valid


def test_move_axes_absolute(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    enable(robot, sdk)
    mv = move_axes(robot, 10.0, -20.0)
    n = execute(robot, mv)
    assert n >= MOVE_CYCLES
    assert sdk.joints[:3] == [10.0, -20.0, 0.0]


def test_move_axes_absolute_before_enable(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Without power the command stays buffered (sequence interrupted), GroupContinue starts it."""
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(50)
    assert mv.Busy and not mv.Done and not mv.Error, state(mv)
    assert sdk.joints[0] == 0.0
    enable(robot, sdk)
    robot.run(10)
    assert mv.Busy and sdk.joints[0] == 0.0
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(100, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == 10.0


def test_move_axes_absolute_deceleration_rate(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """The SDK rejects every DecelerationRate except "not set" (validateDynamicsParameters, 0x8E03)."""
    enable(robot, sdk)
    mv = move_axes(robot, 10.0)
    mv.ParCmd.DecelerationRate = 100.0
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Error and mv.ErrorID == 0x8E03, state(mv)


def test_buffered_moves(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    enable(robot, sdk)
    first = move_axes(robot, 10.0)
    second = move_axes(robot, 30.0, ProcessingMode=ProcessingMode.BUFFERED)
    first.Execute = second.Execute = True
    robot.run(3 * MOVE_CYCLES + 50, until=lambda: bool(second.Done or second.Error or first.Error))
    assert first.Done and second.Done, (state(first), state(second))
    assert sdk.joints[0] == 30.0


def test_move_direct_absolute(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    enable(robot, sdk)
    mv = fb(robot, "MC_MoveDirectAbsoluteFB")
    mv.ParCmd.Position.X, mv.ParCmd.Position.Y, mv.ParCmd.Position.Z = 5.0, 6.0, 7.0
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    execute(robot, mv)
    assert sdk.joints[:3] == [5.0, 6.0, 7.0]


def test_move_linear_absolute(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    enable(robot, sdk)
    mv = fb(robot, "MC_MoveLinearAbsoluteFB")
    mv.ParCmd.Position.X, mv.ParCmd.Position.Z = 50.0, -10.0
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    execute(robot, mv)
    assert sdk.joints[0] == 50.0 and sdk.joints[2] == -10.0


def test_group_interrupt_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    sdk.set_move_cycles(200)
    enable(robot, sdk)
    mv = move_axes(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 5.0)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    stopped = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == stopped and not mv.Done
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(400, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == 100.0


def test_group_stop(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    sdk.set_move_cycles(200)
    enable(robot, sdk)
    mv = move_axes(robot, 100.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 5.0)
    stop = fb(robot, "MC_GroupStopFB")
    execute(robot, stop, reset=False)
    robot.run(50, until=lambda: bool(mv.CommandAborted or mv.Error))
    assert mv.CommandAborted and not mv.Done, state(mv)
    assert sdk.joints[0] < 100.0


def jog(h: RobotTaskHarness, axis: str, cycles: int) -> Any:
    """Jogs ``axis`` (e.g. ``"Y_J2_Pos"``) in joint mode for ``cycles`` cycles (sim: 0.1 per cycle)."""
    j = fb(h, "MC_GroupJogFB", Enable=True)
    j.ParCmd.Mode = JogMode.JOG_AXES
    j.ParCmd.Override = 100
    h.run(50, until=lambda: bool(j.Enabled or j.Error))
    assert j.Enabled and not j.Error, state(j)
    setattr(j.ParCmd.Control, axis, True)
    h.run(cycles)
    assert j.OutCmd.MotionActive
    setattr(j.ParCmd.Control, axis, False)
    h.run(5)
    assert not j.OutCmd.MotionActive
    j.Enable = False
    h.run(50, until=lambda: not j.Enabled and not j.Busy)
    assert not j.Enabled and not j.Error, state(j)
    return j


def test_group_jog(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    enable(robot, sdk)
    jog(robot, "X_J1_Pos", 30)
    assert sdk.joints[0] == pytest.approx(3.0)


def test_interrupt_jog_return_to_primary_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    sdk.set_move_cycles(100)
    enable(robot, sdk)
    mv = move_axes(robot, 50.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 10.0)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    interrupted_at = list(sdk.joints)
    jog(robot, "Y_J2_Pos", 30)  # secondary sequence
    assert sdk.joints[1] == pytest.approx(3.0)
    rtp = fb(robot, "MC_ReturnToPrimaryFB", Enable=True)
    rtp.ParCmd.VelocityRate = rtp.ParCmd.AccelerationRate = 100.0
    rtp.ParCmd.DecelerationRate = rtp.ParCmd.JerkRate = -1.0
    robot.run(300, until=lambda: bool(rtp.Done or rtp.Error))
    assert rtp.Done and rtp.OutCmd.Progress == 100.0, state(rtp)
    assert sdk.joints == pytest.approx(interrupted_at)
    rtp.Enable = False
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(300, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert sdk.joints[:2] == [50.0, 0.0]


# ---------------------------------------------------------------- data


def test_write_and_read_tool_data(robot: RobotTaskHarness) -> None:
    wr = fb(robot, "MC_WriteToolDataFB")
    wr.ParCmd.ToolNo = 3
    wr.ParCmd.ToolData.X = 12.5
    wr.ParCmd.ToolData.Z = 100.0
    wr.ParCmd.ToolData.LoadNo = 1
    execute(robot, wr)
    rd = fb(robot, "MC_ReadToolDataFB")
    rd.ParCmd.ToolNo = 3
    execute(robot, rd, reset=False)
    assert rd.OutCmd.ToolNoReturn == 3
    assert rd.OutCmd.ToolData.X == 12.5 and rd.OutCmd.ToolData.Z == 100.0


def test_write_tool_data_invalid_load(robot: RobotTaskHarness) -> None:
    """ToolData.LoadNo 0 is rejected. Before ST-FIX F28 ToolNo was not sent at all (0x8D35)."""
    wr = fb(robot, "MC_WriteToolDataFB")
    wr.ParCmd.ToolNo = 3
    wr.Execute = True
    robot.run(100, until=lambda: bool(wr.Done or wr.Error))
    assert wr.Error and wr.ErrorID == 0x8D17  # invalid load number


def test_write_tool_0_is_rejected(robot: RobotTaskHarness) -> None:
    wr = fb(robot, "MC_WriteToolDataFB")
    wr.ParCmd.ToolNo = 0
    wr.Execute = True
    robot.run(100, until=lambda: bool(wr.Done or wr.Error))
    assert wr.Error


def test_write_and_read_frame_data(robot: RobotTaskHarness) -> None:
    wr = fb(robot, "MC_WriteFrameDataFB")
    wr.ParCmd.FrameNo = 5
    wr.ParCmd.FrameData.Y = -7.25
    execute(robot, wr)
    rd = fb(robot, "MC_ReadFrameDataFB")
    rd.ParCmd.FrameNo = 5
    execute(robot, rd, reset=False)
    assert rd.OutCmd.FrameNoReturn == 5 and rd.OutCmd.FrameData.Y == -7.25


def test_write_and_read_load_data(robot: RobotTaskHarness) -> None:
    wr = fb(robot, "MC_WriteLoadDataFB")
    wr.ParCmd.LoadNo = 2
    wr.ParCmd.LoadData.Mass = 4.5
    execute(robot, wr)
    rd = fb(robot, "MC_ReadLoadDataFB")
    rd.ParCmd.LoadNo = 2
    execute(robot, rd, reset=False)
    assert rd.OutCmd.LoadNoReturn == 2 and rd.OutCmd.LoadData.Mass == 4.5


def test_write_and_read_sw_limits(robot: RobotTaskHarness) -> None:
    rd = fb(robot, "MC_ReadRobotSWLimitsFB")
    execute(robot, rd)
    assert rd.OutCmd.LimitValues.J1UpperLimit == 360.0
    wr = fb(robot, "MC_WriteRobotSWLimitsFB")
    wr.ParCmd.LimitValues.J1LowerLimit = -170.0
    wr.ParCmd.LimitValues.J1UpperLimit = 170.0
    execute(robot, wr)
    execute(robot, rd, reset=False)
    assert rd.OutCmd.LimitValues.J1LowerLimit == -170.0 and rd.OutCmd.LimitValues.J1UpperLimit == 170.0


def test_write_and_read_default_dynamics(robot: RobotTaskHarness) -> None:
    rd = fb(robot, "MC_ReadRobotDefaultDynamicsFB")
    execute(robot, rd)
    wr = fb(robot, "MC_WriteRobotDefaultDynamicsFB")
    wr.ParCmd.DynamicValues = rd.OutCmd.DynamicValues
    wr.ParCmd.DynamicValues.VelocityRate = 42.0
    execute(robot, wr)
    execute(robot, rd, reset=False)
    assert rd.OutCmd.DynamicValues.VelocityRate == 42.0


def test_write_and_read_reference_dynamics(robot: RobotTaskHarness) -> None:
    rd = fb(robot, "MC_ReadRobotReferenceDynamicsFB")
    execute(robot, rd)
    wr = fb(robot, "MC_WriteRobotReferenceDynamicsFB")
    wr.ParCmd.DynamicValues = rd.OutCmd.DynamicValues
    execute(robot, wr)


# ---------------------------------------------------------------- cyclic position


def test_read_actual_position_cyclic_with_tool(sdk: SdkSimulator) -> None:
    """ST-FIX F59: the position is updated also when the motion uses another tool than the one of
    the requested coordinate system (the ST compared the *currently used* tool with the request)."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.cfg.Rob.OptionalCyclic.UseJointPosition = True
        h.cfg.Rob.OptionalCyclic.UseCartesianPosition = True
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        cyc = fb(h, "MC_ReadActualPositionCyclicFB", Enable=True)
        cyc.ParCmd.ReadJointPosition = cyc.ParCmd.ReadCartesianPosition = True
        h.run(20, until=lambda: bool(cyc.Enabled or cyc.Error))
        assert cyc.Enabled and not cyc.Error, state(cyc)
        enable(h, sdk)
        mv = move_axes(h, 10.0, 20.0)
        mv.ParCmd.ToolNo = 1
        execute(h, mv)
        h.run(3)
        assert (cyc.OutCmd.JointPosition.J1, cyc.OutCmd.JointPosition.J2) == (10.0, 20.0)
        assert cyc.OutCmd.CartesianPosition.X == 10.0  # identity kinematics, flange (tool 0)
        assert cyc.OutCmd.CoordinateSystem.ToolNo == 0  # requested
        assert cyc.OutCmd.CurrentCoordinateSystem.ToolNo == 1  # used by the motion
