# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_userdata_position_userdata
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests: UserData of the RobotTask (configuration, info, state) against the RC (SDK).
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

"""Validation tests: UserData of the RobotTask (configuration, info, state) against the RC (SDK).

The UserData structure of the RobotTask mirrors the configuration sent to the RC
(ExchangeConfiguration, ReadMessages), the information of the RC (ReadRobotData) and the
state of the robot arm from the cyclic telegram. The telegram layout values (telegram numbers,
lengths of the cyclic and sequence areas) are taken from the AxesGroup and the RobotTask.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.iec.rt import copy_into
from srci.types import (
    AxisUnit,
    CmdType,
    ComDirection,
    JogMode,
    MessageLevel,
    OperationMode,
    RobotLibraryConstants,
    RobotLibraryErrorIdEnum,
    RobotLibraryInfoIdEnum,
    SequenceFlag,
    Severity,
)
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import MOVE_CYCLES, cartesian, enable, execute, fb, move_axes, order, state

# ---------------------------------------------------------------- helpers


@contextmanager
def _robot_with(
    sdk: SdkSimulator, setup: Callable[[RobotTaskHarness], None] | None = None, size: int = SIZE
) -> Iterator[RobotTaskHarness]:
    """RobotTask with a configuration changed by ``setup`` before the start-up (not yet initialized)."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, size, size), advance=clock.advance, size=size)
        if setup is not None:
            setup(h)
        yield h


def _start(h: RobotTaskHarness, cycles: int = 300) -> None:
    h.run(cycles, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))


def _started(h: RobotTaskHarness) -> None:
    _start(h)
    assert h.ag.State.CMDsEnabled and not h.rt.Error, (hex(h.rt.ErrorID), h.history[-3:])


def _move_linear(h: RobotTaskHarness, x: float, **par: Any) -> Any:
    mv = fb(h, "MC_MoveLinearAbsoluteFB")
    cartesian(mv, x, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    for name, value in par.items():
        setattr(mv.ParCmd, name, value)
    return mv


def _jog(h: RobotTaskHarness) -> Any:
    """GroupJog (axes, override 100 %) enabled; returns the block."""
    jog = fb(h, "MC_GroupJogFB", Enable=True)
    jog.ParCmd.Mode = JogMode.JOG_AXES
    jog.ParCmd.Override = 100
    h.run(50, until=lambda: bool(jog.Enabled or jog.Error))
    assert jog.Enabled and not jog.Error, state(jog)
    return jog


def _interrupt_running_motion(h: RobotTaskHarness) -> Any:
    """MoveAxes started and interrupted by GroupInterrupt; returns the motion block."""
    mv = move_axes(h, -30.0)
    mv.Execute = True
    h.run(100, until=lambda: bool(mv.Active))
    gi = fb(h, "MC_GroupInterruptFB")
    assert execute(h, gi, reset=False).final["Done"]
    h.run(2)
    assert mv.CommandInterrupted, state(mv)
    return mv


def _ud(h: RobotTaskHarness, *names: str) -> dict[str, Any]:
    return {n: getattr(h.user_data, n) for n in names}


# ---------------------------------------------------------------- telegram layout


@pytest.mark.parametrize(
    ("options", "number", "plc_cyclic", "rc_cyclic"),
    [
        ((), 0, 18, 10),
        (("UseCartesianPosition",), 2, 20, 50),
        (("UseJointPosition",), 4, 18, 40),
        # the extended position switches the base position on (InfoID 16#6002 / 16#6003, ST-FIX F137)
        (("UseCartesianPositionExt",), 514, 20, 70),
        (("UseJointPositionExt",), 1028, 18, 60),
        (("UseJointPosition", "UseJointPositionExt"), 1028, 18, 60),
    ],
    ids=["default", "cartesian", "joint", "cartesian-ext", "joint-ext", "joint-and-ext"],
)
def test_telegram_number_and_cyclic_lengths(
    sdk: SdkSimulator, options: tuple[str, ...], number: int, plc_cyclic: int, rc_cyclic: int
) -> None:
    """The optional cyclic position data set the telegram number RC->PLC and the cyclic lengths.

    The RC accepts the layout (start-up completes). Cyclic area PLC->RC: 18 bytes (+2 for the
    ToolNo / FrameNo of the Cartesian position); RC->PLC: 10 bytes plus 40 (Cartesian),
    30 (joint), 20 (each extended part). An extended part without its base position also activates
    the base position. The telegram number PLC->RC stays 0.
    """

    def setup(h: RobotTaskHarness) -> None:
        for name in options:
            setattr(h.cfg.Rob.OptionalCyclic, name, True)

    with _robot_with(sdk, setup) as h:
        _started(h)
        assert h.ag.Cyclic.PlcToRob.TelegramNumberRobToPlc == number
        assert h.ag.Cyclic.PlcToRob.TelegramNumberPlcToRob == 0
        assert h.rt.CalculateCyclicDataLength(h.ag, ComDirection.PLC_TO_ROB) == plc_cyclic
        assert h.rt.CalculateCyclicDataLength(h.ag, ComDirection.ROB_TO_PLC) == rc_cyclic


@pytest.mark.parametrize("two", [False, True], ids=["one-sequence", "two-sequences"])
@pytest.mark.parametrize(
    "direction", [ComDirection.PLC_TO_ROB, ComDirection.ROB_TO_PLC], ids=["plc-rc", "rc-plc"]
)
def test_sequence_areas(sdk: SdkSimulator, two: bool, direction: ComDirection) -> None:
    """The acyclic area (telegram size - cyclic data - 1 footer byte) belongs to one or two sequences.

    One sequence: sequence 1 gets the whole area, sequence 2 is 0. Two sequences: both > 0, the sum is
    the whole area; the telegram numbers of both directions are 256.
    """

    def setup(h: RobotTaskHarness) -> None:
        h.cfg.Com.TwoSequences = two
        h.cfg.Plc.OptionalCyclic.UseTwoSequences = two
        h.cfg.Rob.OptionalCyclic.UseTwoSequences = two

    with _robot_with(sdk, setup) as h:
        _started(h)
        area = SIZE - h.rt.CalculateCyclicDataLength(h.ag, direction) - 1
        first = h.rt.CalculateSequencePayloadMax(h.ag, direction, SequenceFlag.PRIMARY_SEQUENCE)
        second = h.rt.CalculateSequencePayloadMax(h.ag, direction, SequenceFlag.SECONDARY_SEQUENCE)
        assert h.user_data.ActivateTwoSequences == two
        if two:
            assert first > 0 and second > 0 and first + second == area
            assert h.ag.Cyclic.PlcToRob.TelegramNumberPlcToRob == 256
            assert h.ag.Cyclic.PlcToRob.TelegramNumberRobToPlc == 256
        else:
            assert (first, second) == (area, 0)
            assert h.ag.Cyclic.PlcToRob.TelegramNumberPlcToRob == 0


@pytest.mark.parametrize("size", [128, 256])
def test_telegram_size_follows_configuration(sdk: SdkSimulator, size: int) -> None:
    """The telegram lengths in the cyclic header equal the configured telegram size (both directions).

    A bigger telegram gives a bigger sequence area (128 vs. 256 bytes); the RC accepts both.
    """
    with _robot_with(sdk, size=size) as h:
        _started(h)
        assert h.ag.Cyclic.PlcToRob.TelegramLengthPlcToRob == size
        assert h.ag.Cyclic.PlcToRob.TelegramLengthRobToPlc == size
        area = h.rt.CalculateSequencePayloadMax(h.ag, ComDirection.PLC_TO_ROB, SequenceFlag.PRIMARY_SEQUENCE)
        assert area == size - 18 - 1


# ---------------------------------------------------------------- info


def test_plc_and_rc_info(sdk: SdkSimulator) -> None:
    """UserData shows the PLC information of the configuration, the library version and the RC information.

    PLC: manufacturer id, order id, serial number, firmware and interface version as configured;
    library version = the version constant (not 0.0.0). RC: the values of ReadRobotData (not empty).
    """

    def setup(h: RobotTaskHarness) -> None:
        p = h.cfg.Plc.Parameter
        p.ManufacturedID, p.OrderID, p.SerialNumber = 42, "ORDER-1", "SN-7"
        p.FirmwareVersion, p.InterfaceVersion = "V3.1", "IF-2"

    with _robot_with(sdk, setup) as h:
        _started(h)
        ud = h.user_data
        assert (ud.PLCManufacturedID, ud.PLCOrderID, ud.PLCSerialNumber) == (42, "ORDER-1", "SN-7")
        assert (ud.PLCFirmwareVersion, ud.PLCInterfaceVersion) == ("V3.1", "IF-2")
        lib = RobotLibraryConstants.PLCLibraryVersion
        version = (
            ud.PLCLibraryVersion.MajorVersion,
            ud.PLCLibraryVersion.MinorVersion,
            ud.PLCLibraryVersion.PatchVersion,
        )
        assert version == (lib.MajorVersion, lib.MinorVersion, lib.PatchVersion) and version != (0, 0, 0)
        rd = h.ag.State.RobotData
        for name in ("RCManufacturer", "RCOrderID", "RCSerialNumber", "RASerialNumber", "RCFirmwareVersion"):
            assert getattr(ud, name) == getattr(rd, name) != "", name
        assert ud.RCInterpreterVersion.MajorVersion > 0 or ud.RCInterpreterVersion.MinorVersion > 0


def test_axes_used_and_units(robot: RobotTaskHarness) -> None:
    """UserData reports the axes and units of the RC: J1..J6 used (degrees), E1 used (mm), E2..E6 unused.

    The values equal the ReadRobotData answer of the simulated robot (6 joints + 1 linear axis).
    """
    ud = robot.user_data
    joints = [getattr(ud.AxisJointUsed, f"J{i}") for i in range(1, 7)]
    external = [getattr(ud.AxisExternalUsed, f"E{i}") for i in range(1, 7)]
    assert joints == [True] * 6
    assert external == [True] + [False] * 5
    assert [getattr(ud.AxisJointUnit, f"J{i}") for i in range(1, 7)] == [AxisUnit.DEG] * 6
    assert ud.AxisExternalUnit.E1 == AxisUnit.MM
    assert ud.AxisJointUsed == robot.ag.State.RobotData.AxisJointUsed


# ---------------------------------------------------------------- configuration


@pytest.mark.parametrize(
    "level",
    [
        Severity.DEACTIVATE,
        Severity.DEBUG,
        Severity.INFO,
        Severity.WARNING,
        Severity.ERROR,
        pytest.param(
            Severity.FATAL_ERROR,
            marks=pytest.mark.xfail(
                strict=True,
                reason="SDK-GAP: the SDK rejects LogLevel 29 (FATAL_ERROR) in ExchangeConfiguration with "
                "16#8D18 although it is a defined severity (spec ExchangeConfiguration LogLevel, "
                "Severity 0/4/5/20/28/29).",
            ),
        ),
    ],
    ids=lambda s: s.name,
)
def test_server_log_level_is_transmitted(sdk: SdkSimulator, level: Severity) -> None:
    """Every defined LogLevel of the RC server log is sent with ExchangeConfiguration and accepted.

    The start-up completes; ExchangeConfiguration carries the level; UserData.LogLevel shows it.
    (Which messages the RC writes to its server log is not observable in the simulation.)
    """

    def setup(h: RobotTaskHarness) -> None:
        h.rt.LogLevel = level

    with _robot_with(sdk, setup) as h:
        _started(h)
        sent = sdk.last_command(int(CmdType.ExchangeConfiguration)) or {}
        assert sent.get("LogLevel") == str(int(level))
        assert h.user_data.LogLevel == level


@pytest.mark.parametrize("level", list(MessageLevel), ids=lambda m: m.name)
def test_message_level_is_transmitted(sdk: SdkSimulator, level: MessageLevel) -> None:
    """Every defined MessageLevel is sent with ReadMessages at start-up and accepted by the RC.

    UserData.MessageLevel shows the level. (The RC simulation sends no messages of its own, so the
    filtering of the PLC message log by level cannot be stimulated.)
    """

    def setup(h: RobotTaskHarness) -> None:
        h.cfg.Rob.Parameter.MessageLevel = level

    with _robot_with(sdk, setup) as h:
        _started(h)
        sent = sdk.last_command(int(CmdType.ReadMessages)) or {}
        assert sent.get("MessageLevel") == str(int(level))
        assert h.user_data.MessageLevel == level


@pytest.mark.parametrize(
    "timeout",
    [
        pytest.param(
            10,
            marks=pytest.mark.xfail(
                strict=True,
                reason="SDK-GAP: the SDK rejects LifeSignTimeOut values below 20 ms with 16#8D14; the "
                "spec (ExchangeConfiguration) only marks values < 10 ms as invalid.",
            ),
        ),
        50,
    ],
    ids=["minimum-10ms", "default-50ms"],
)
def test_lifesign_timeout_accepted(sdk: SdkSimulator, timeout: int) -> None:
    """A valid LifeSignTimeOut (10 ms minimum, 50 ms default) is accepted: start-up without error.

    ExchangeConfiguration carries the value, UserData.LifeSignTimeOut shows it.
    """

    def setup(h: RobotTaskHarness) -> None:
        h.cfg.Com.LifeSignTimeOut = timeout

    with _robot_with(sdk, setup) as h:
        _start(h)
        assert h.ag.State.CMDsEnabled and not h.rt.Error, hex(h.rt.ErrorID)
        assert (sdk.last_command(int(CmdType.ExchangeConfiguration)) or {}).get("LifeSignTimeOut") == str(
            timeout
        )
        assert h.user_data.LifeSignTimeOut == timeout


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated RC ignores DelayTime of ExchangeConfiguration; the first motion "
    "starts in the next cycle (spec 5.6.8 DelayTime).",
)
def test_delay_time_before_first_motion(sdk: SdkSimulator) -> None:
    """DelayTime 500 ms: the RC waits 500 ms after the first move command before the robot moves."""

    def setup(h: RobotTaskHarness) -> None:
        h.cfg.Rob.Parameter.DelayTime = 500

    with _robot_with(sdk, setup) as h:
        _started(h)
        assert h.user_data.DelayTime == 500
        enable(h)
        mv = move_axes(h, 10.0)
        mv.Execute = True
        h.run(40)  # 400 ms (cycle 10 ms)
        assert sdk.joints[0] == 0.0
        h.run(5 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done and sdk.joints[0] == pytest.approx(10.0)


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated RC ignores WaitForNrOfCmd of ExchangeConfiguration and starts "
    "every motion at once (spec 5.6.8 WaitForNrOfCmd / DelayTime).",
)
def test_wait_for_number_of_commands(sdk: SdkSimulator) -> None:
    """WaitForNrOfCmd 2 (DelayTime 500 ms): one buffered move waits; the robot starts with the 2nd command."""

    def setup(h: RobotTaskHarness) -> None:
        h.cfg.Rob.Parameter.WaitForNrOfCmd = 2
        h.cfg.Rob.Parameter.DelayTime = 500

    with _robot_with(sdk, setup) as h:
        _started(h)
        assert h.user_data.WaitForNrOfCmd == 2
        enable(h)
        first = move_axes(h, 10.0)
        first.Execute = True
        h.run(20)
        assert sdk.joints[0] == 0.0
        second = move_axes(h, 20.0)
        second.Execute = True
        h.run(10 * MOVE_CYCLES, until=lambda: bool(second.Done or second.Error))
        assert first.Done and second.Done and sdk.joints[0] == pytest.approx(20.0)


# ---------------------------------------------------------------- state


def test_connection_loss_clears_initialized_state(robot: RobotTaskHarness) -> None:
    """When the RC stops answering, Initialized, CMDsEnabled and the lifesign state drop; the RobotTask errors.

    Before: GroupReset Busy -> Done, UserData.Initialized TRUE. The RC telegram is then frozen (no
    lifesign change): RobotTask Error 16#80A5, UserData.Initialized FALSE, AliveOk FALSE.
    """
    seen = execute(robot, fb(robot, "MC_GroupResetFB"))
    assert order(seen, "Busy", "Done")
    assert robot.user_data.Initialized and robot.ag.State.AliveOk and robot.ag.State.CMDsEnabled

    class _Frozen:
        def __init__(self, data: bytes) -> None:
            self.data = data

        def exchange(self, telegram: bytes) -> bytes:
            return self.data

    robot.transport = _Frozen(bytes(robot.rin))  # type: ignore[assignment]
    robot.run(100, until=lambda: bool(robot.rt.Error))
    assert robot.rt.Error and robot.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_LIFESIGN_TIMEOUT_0x80A5
    assert not robot.user_data.Initialized and not robot.rt.Initialized
    assert not robot.ag.State.CMDsEnabled and not robot.ag.State.AliveOk


def test_state_during_motion(robot: RobotTaskHarness) -> None:
    """Reset, enable, stop, then a MoveLinear: the UserData state follows the RA state machine.

    After GroupReset no error pending; EnableRobot -> Enabled; GroupStop Done -> Idle. While the motion
    is Active: IsMoving, InPrimaryPos, Executing TRUE, Idle FALSE, operation mode Automatic External.
    """
    assert execute(robot, fb(robot, "MC_GroupResetFB")).final["Done"]
    assert not robot.user_data.ErrorPending
    enable(robot)
    assert robot.user_data.Enabled
    assert execute(robot, fb(robot, "MC_GroupStopFB")).final["Done"]
    robot.run(2)
    assert robot.user_data.Idle
    mv = _move_linear(robot, 120.0, VelocityRate=5.0)
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Active or mv.Error))
    robot.run(3)
    assert mv.Active, state(mv)
    assert _ud(robot, "IsMoving", "InPrimaryPos", "Executing", "Idle") == {
        "IsMoving": True,
        "InPrimaryPos": True,
        "Executing": True,
        "Idle": False,
    }
    assert robot.user_data.OperationMode == OperationMode.AUTO_EXT


def test_switch_to_secondary_sequence_state(robot: RobotTaskHarness) -> None:
    """SetSequence(secondary) from the idle primary sequence: secondary active, primary interrupted.

    UserData: SecondarySequenceActive and Interrupted TRUE, Idle and PrimarySequencePaused FALSE,
    InPrimaryPos TRUE, operation mode Automatic External.
    """
    assert not robot.user_data.SecondarySequenceActive
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert _ud(
        robot, "SecondarySequenceActive", "Interrupted", "Idle", "PrimarySequencePaused", "InPrimaryPos"
    ) == {
        "SecondarySequenceActive": True,
        "Interrupted": True,
        "Idle": False,
        "PrimarySequencePaused": False,
        "InPrimaryPos": True,
    }
    assert robot.user_data.OperationMode == OperationMode.AUTO_EXT


def test_interrupt_and_jog_away_from_path(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A motion interrupted by GroupInterrupt, then jogging in the secondary sequence leaves the path.

    GroupInterrupt Done, motion CommandInterrupted; while jogging the secondary sequence is active and
    executing; after the jog: secondary FALSE, Executing / IsMoving FALSE, Interrupted and
    PrimarySequencePaused TRUE, InPrimaryPos FALSE, robot still enabled.
    """
    enable(robot)
    _interrupt_running_motion(robot)
    jog = _jog(robot)
    jog.ParCmd.Control.X_J1_Pos = True
    robot.run(10)
    assert jog.OutCmd.MotionActive
    assert robot.user_data.SecondarySequenceActive and robot.user_data.Executing
    jog.ParCmd.Control.X_J1_Pos = False
    robot.run(5)
    jog.Enable = False
    robot.run(50, until=lambda: not jog.Enabled and not jog.Busy)
    robot.run(3)
    assert _ud(
        robot,
        "SecondarySequenceActive",
        "IsMoving",
        "Executing",
        "Interrupted",
        "PrimarySequencePaused",
        "InPrimaryPos",
        "Enabled",
    ) == {
        "SecondarySequenceActive": False,
        "IsMoving": False,
        "Executing": False,
        "Interrupted": True,
        "PrimarySequencePaused": True,
        "InPrimaryPos": False,
        "Enabled": True,
    }


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated RC does not set IsMoving in the status word while GroupJog moves "
    "the robot (spec RA status word: IsMoving while any motion is executed).",
)
def test_jog_sets_is_moving(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """While GroupJog moves the robot, UserData.IsMoving and Executing are TRUE."""
    enable(robot)
    jog = _jog(robot)
    jog.ParCmd.Control.Y_J2_Pos = True
    robot.run(10)
    assert jog.OutCmd.MotionActive and sdk.joints[1] != 0.0
    assert robot.user_data.Executing
    assert robot.user_data.IsMoving


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: no software limit check in the simulated RC; jogging continues beyond the "
    "limits (spec GroupJog: error 16#6C03 / 6C04 at the limit, robot stops).",
)
def test_jog_beyond_software_limit(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Jogging J1 towards the software limit (170 deg) stops the jog with an error before the limit."""
    enable(robot)
    jog = _jog(robot)
    jog.ParCmd.Control.X_J1_Pos = True
    robot.run(3000, until=lambda: bool(jog.Error))
    assert jog.Error and jog.ErrorID in (0x6C03, 0x6C04), state(jog)
    assert sdk.joints[0] <= 170.0


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: RestartController is answered Done at once; the status word never shows "
    "RestartInProgress and the RobotTask stays initialized (spec RA status word, RestartController).",
)
def test_restart_in_progress_after_restart(robot: RobotTaskHarness) -> None:
    """After new software limits a controller restart shows RestartInProgress in the UserData."""
    wl = fb(robot, "MC_WriteRobotSWLimitsFB")
    copy_into(wl.ParCmd.LimitValues, robot.sw_limits)
    wl.ParCmd.LimitValues.J1LowerLimit, wl.ParCmd.LimitValues.J1UpperLimit = -160.0, 160.0
    assert execute(robot, wl).final["Done"]
    rc = fb(robot, "MC_RestartControllerFB")
    rc.Execute = True
    seen = False
    for _ in range(400):
        robot.run(1)
        seen = seen or bool(robot.user_data.RestartInProgress)
        if rc.Done or rc.Error:
            break
    assert seen


def test_software_limits_written_and_read(robot: RobotTaskHarness) -> None:
    """New software limits (J1 -160 / +160) are written (Done) and read back unchanged.

    A restart request is vendor specific; RestartRequested is only reported, not required.
    """
    wl = fb(robot, "MC_WriteRobotSWLimitsFB")
    copy_into(wl.ParCmd.LimitValues, robot.sw_limits)
    wl.ParCmd.LimitValues.J1LowerLimit, wl.ParCmd.LimitValues.J1UpperLimit = -160.0, 160.0
    assert order(execute(robot, wl), "Busy", "Done")
    rd = fb(robot, "MC_ReadRobotSWLimitsFB")
    assert execute(robot, rd, reset=False).final["Done"]
    limits = rd.OutCmd.LimitValues
    assert (limits.J1LowerLimit, limits.J1UpperLimit) == (-160.0, 160.0)
    assert (limits.J2LowerLimit, limits.J2UpperLimit) == (-170.0, 170.0)


def test_enable_robot_state(robot: RobotTaskHarness) -> None:
    """EnableRobot (StepMode 0): Busy then Enabled; UserData Enabled, Automatic External, step modes off."""
    en = fb(robot, "MC_EnableRobotFB")
    en.ParCmd.StepMode = 0
    en.Enable = True
    robot.run(200, until=lambda: bool(en.Enabled or en.Error))
    assert en.Enabled and not en.Error, state(en)
    robot.run(2)
    assert robot.user_data.Enabled and robot.user_data.OperationMode == OperationMode.AUTO_EXT
    assert not robot.user_data.StepModeExactStopActive and not robot.user_data.StepModeBlendingActive


def test_move_while_disabled_runs_after_enable_and_continue(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """A move started while the robot is disabled waits; after EnableRobot and GroupContinue it runs to Done.

    While waiting: buffered, UserData Interrupted and PrimarySequencePaused TRUE, InPrimaryPos TRUE.
    After GroupContinue: Executing, not Interrupted, not Idle. After Done: Idle, not Executing / IsMoving.
    """
    mv = move_axes(robot, 30.0)
    mv.Execute = True
    robot.run(30)
    assert mv.Busy and mv.CommandBuffered and not mv.Error, state(mv)
    assert _ud(robot, "Interrupted", "PrimarySequencePaused", "InPrimaryPos") == {
        "Interrupted": True,
        "PrimarySequencePaused": True,
        "InPrimaryPos": True,
    }
    en = fb(robot, "MC_EnableRobotFB", Enable=True)
    robot.run(200, until=lambda: bool(en.Enabled or en.Error))
    assert en.Enabled and robot.user_data.Enabled and sdk.joints[0] == 0.0
    assert execute(robot, fb(robot, "MC_GroupContinueFB"), cycles=50).final["Done"]
    robot.run(3)
    assert _ud(robot, "Interrupted", "Executing", "Idle", "PrimarySequencePaused") == {
        "Interrupted": False,
        "Executing": True,
        "Idle": False,
        "PrimarySequencePaused": False,
    }
    robot.run(5 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
    robot.run(2)
    assert mv.Done and not mv.CommandInterrupted, state(mv)
    assert _ud(robot, "Interrupted", "Executing", "IsMoving", "Idle") == {
        "Interrupted": False,
        "Executing": False,
        "IsMoving": False,
        "Idle": True,
    }


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: a move buffered while the robot is disabled stays BUFFERED in the SDK; the "
    "command is not reported INTERRUPTED with 16#6F02 (a ReadActualPosition in the sequence is).",
)
def test_move_while_disabled_reports_interrupted(robot: RobotTaskHarness) -> None:
    """A move started while the robot is disabled reports CommandInterrupted with InfoID 16#6F02."""
    mv = move_axes(robot, 30.0)
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.CommandInterrupted or mv.Error))
    assert mv.CommandInterrupted and not mv.Error, state(mv)
    assert mv.InfoID == RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED


def test_operation_mode_switch_t1_and_back(robot: RobotTaskHarness) -> None:
    """SetOperationMode T1 External then Automatic External: Done; UserData shows the mode, robot disabled, idle."""
    enable(robot)
    om = fb(robot, "MC_SetOperationModeFB")
    for mode in (OperationMode.T1_EXT, OperationMode.AUTO_EXT):
        om.ParCmd.OperationMode = mode
        assert order(execute(robot, om, cycles=100), "Busy", "Done")
        robot.run(3)
        assert robot.user_data.OperationMode == mode
        assert not robot.user_data.Enabled and robot.user_data.Idle


@pytest.mark.parametrize("during_motion", [False, True], ids=["idle", "during-motion"])
def test_override_change_shown_in_user_data(
    robot: RobotTaskHarness, sdk: SdkSimulator, during_motion: bool
) -> None:
    """ChangeSpeedOverride 50 %: Done and UserData.ActualOverride = 50 (also while a motion is active)."""
    enable(robot)
    mv = None
    if during_motion:
        mv = move_axes(robot, 40.0)
        mv.Execute = True
        robot.run(100, until=lambda: bool(mv.Active))
        assert robot.user_data.IsMoving and robot.user_data.Executing
    co = fb(robot, "MC_ChangeSpeedOverrideFB")
    co.ParCmd.Override = 50.0
    assert execute(robot, co).final["Done"]
    assert robot.user_data.ActualOverride == pytest.approx(50.0)
    assert sdk.override == pytest.approx(50.0)
    if mv is not None:
        robot.run(10 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done, state(mv)


@pytest.mark.parametrize("motion", ["move", "jog"])
def test_motion_phase_flags_without_support(robot: RobotTaskHarness, motion: str) -> None:
    """The RC does not support the motion phase flags: Supported FALSE and Accelerating / Decelerating /
    ConstantVelocity stay FALSE during a MoveLinear and during jogging."""
    enable(robot)
    ud = robot.user_data
    assert not (ud.AcceleratingSupported or ud.DeceleratingSupported or ud.ConstantVelocitySupported)
    phases: set[bool] = set()

    def record() -> None:
        phases.update((ud.Accelerating, ud.Decelerating, ud.ConstantVelocity))

    if motion == "move":
        mv = _move_linear(robot, 90.0, VelocityRate=10.0)
        mv.Execute = True
        for _ in range(5 * MOVE_CYCLES):
            robot.run(1)
            record()
            if mv.Done or mv.Error:
                break
        assert mv.Done, state(mv)
    else:
        jog = _jog(robot)
        jog.ParCmd.Control.Y_J2_Pos = True
        for _ in range(20):
            robot.run(1)
            record()
        assert jog.OutCmd.MotionActive
    assert phases == {False}


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated RC executes blended moves one after another without blending "
    "and never sets IsBlending in the status word (spec RA status word, BlendingMode).",
)
def test_is_blending_between_two_moves(robot: RobotTaskHarness) -> None:
    """Two MoveLinear with blending (mode 3, 10 mm): UserData.IsBlending is TRUE during the transition."""
    enable(robot)
    first = _move_linear(robot, 30.0, VelocityRate=5.0, BlendingMode=3)
    first.ParCmd.BlendingParameter[0] = 10.0
    second = _move_linear(robot, 60.0, VelocityRate=5.0)
    first.Execute = second.Execute = True
    blending = False
    for _ in range(10 * MOVE_CYCLES):
        robot.run(1)
        blending = blending or bool(robot.user_data.IsBlending)
        if second.Done or second.Error:
            break
    assert first.Done and second.Done, (state(first), state(second))
    assert blending
