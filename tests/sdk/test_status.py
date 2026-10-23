# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_status
#  Author:      Thorsten Brach
#  Date:        2026-10-22
#
#  Description:
#    Continuous position read, operation mode, unlinked axes group and command name against
#    the SRCI SDK.
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

"""Continuous position read, operation mode, unlinked axes group and command name (SDK-STAT).

* ReadActualPosition CONTINUOUS: Valid while running, values follow the motion, Done stays
  FALSE also after Execute FALSE; ended by ProcessingMode DEACTIVATE and a new rising edge
  (ST-FIX F104)
* ReadActualPosition parameter checks end to end (sequence flag, trigger without listener,
  tool/frame number out of range)
* SetOperationMode: the operation mode of the cyclic status follows, a change switches the
  power off (SDK harness: the simulated RC applies the mode)
* a block on an axes group that no RobotTask serves ends with 16#8612
* the user defined command name is part of the message text (ST-FIX F105)
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import AxesGroup, OperationMode, ProcessingMode, RobotLibraryErrorIdEnum, SequenceFlag
from srci.types.iec import new_instance
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import enable, execute, fb, move_axes, robot, sdk_parameters, state

__all__ = ["robot", "sdk_parameters"]  # fixtures

E = RobotLibraryErrorIdEnum


def read_position(h: RobotTaskHarness, **inputs: Any) -> Any:
    return fb(h, "MC_ReadActualPositionFB", **inputs)


def continuous(h: RobotTaskHarness) -> Any:
    rp = read_position(h, ProcessingMode=ProcessingMode.CONTINUOUS, Execute=True)
    h.run(20, until=lambda: bool(rp.Valid or rp.Error))
    assert rp.Valid and rp.Busy and not rp.Error, state(rp)
    return rp


def deactivate(h: RobotTaskHarness, rp: Any) -> None:
    """ProcessingMode DEACTIVATE + new rising edge on the same instance (spec 5.5.12.4)."""
    rp.Execute = False
    h.run(2)
    rp.ProcessingMode = ProcessingMode.DEACTIVATE
    rp.Execute = True
    h.run(50, until=lambda: bool(rp.Done or rp.Error))


# ---------------------------------------------------------------- ReadActualPosition


def test_read_position_continuous_follows_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """CONTINUOUS: Valid TRUE, Done FALSE, the values follow the motion."""
    enable(robot, sdk)
    rp = continuous(robot)
    mv = move_axes(robot, 20.0)
    mv.Execute = True
    seen = set()
    for _ in range(40):
        robot.run(1)
        seen.add(round(rp.OutCmd.ActualJointPosition.J1, 1))
        assert rp.Valid and rp.Busy and not rp.Done, state(rp)
    assert len(seen) > 5 and max(seen) == 20.0, sorted(seen)


def test_read_position_continuous_after_execute_false(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A falling edge of Execute does not end a continuous read (it runs until DEACTIVATE)."""
    rp = continuous(robot)
    rp.Execute = False
    robot.run(5)
    sdk.joints = [7.0] + [0.0] * 11
    robot.run(5)
    assert rp.Busy and rp.Valid and not rp.Done, state(rp)
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(7.0)


def test_read_position_continuous_deactivate(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ST-FIX F104: DEACTIVATE + new rising edge ends the continuous read: Done, Busy FALSE;
    after Execute FALSE also Valid FALSE; the values are no longer updated."""
    start_log = len(sdk.logs)
    rp = continuous(robot)
    deactivate(robot, rp)
    assert rp.Done and not rp.Busy and not rp.Error, state(rp)
    assert any(
        "ACTIVE -> DONE" in log.text and "ReadActualPosition" in log.text for log in sdk.logs[start_log:]
    )
    rp.Execute = False
    robot.run(3)
    assert not (rp.Valid or rp.Busy or rp.Done or rp.CommandBuffered), state(rp)
    sdk.joints = [9.0] + [0.0] * 11
    robot.run(5)
    assert rp.OutCmd.ActualJointPosition.J1 != pytest.approx(9.0)


def test_read_position_continuous_restart_after_deactivate(
    robot: RobotTaskHarness, sdk: SdkSimulator
) -> None:
    """After DEACTIVATE the same instance starts a new continuous read."""
    rp = continuous(robot)
    deactivate(robot, rp)
    rp.Execute = False
    robot.run(2)
    rp.ProcessingMode = ProcessingMode.CONTINUOUS
    rp.Execute = True
    robot.run(20, until=lambda: bool(rp.Valid or rp.Error))
    assert rp.Valid and rp.Busy and not rp.Error, state(rp)
    sdk.joints = [3.0] + [0.0] * 11
    robot.run(5)
    assert rp.OutCmd.ActualJointPosition.J1 == pytest.approx(3.0)


def test_read_position_deactivate_without_running_command(robot: RobotTaskHarness) -> None:
    """DEACTIVATE as a new command (nothing running): the RC answers Done."""
    rp = read_position(robot, ProcessingMode=ProcessingMode.DEACTIVATE)
    execute(robot, rp)


def test_deactivate_parallel_read_inputs(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ST-FIX F104 on another block: continuous ReadDigitalInputs ended by DEACTIVATE."""
    di = fb(robot, "MC_ReadDigitalInputsFB", ProcessingMode=ProcessingMode.CONTINUOUS, Execute=True)
    robot.run(20, until=lambda: bool(di.Valid or di.Error))
    assert di.Valid and di.Busy, state(di)
    deactivate(robot, di)
    assert di.Done and not di.Busy and not di.Error, state(di)


@pytest.mark.parametrize(
    ("mode", "flag", "error"),
    [
        (ProcessingMode.PARALLEL, SequenceFlag.PRIMARY_SEQUENCE, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (ProcessingMode.CONTINUOUS, SequenceFlag.SECONDARY_SEQUENCE, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (ProcessingMode.BUFFERED, SequenceFlag.NO_SEQUENCE, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
    ],
)
def test_read_position_sequence_flag(
    robot: RobotTaskHarness, mode: ProcessingMode, flag: SequenceFlag, error: int
) -> None:
    """The client rejects a sequence flag that does not fit the ProcessingMode (nothing sent)."""
    rp = read_position(robot, ProcessingMode=mode, SequenceFlag=flag, Execute=True)
    robot.run(10, until=lambda: bool(rp.Error))
    assert rp.Error and rp.ErrorID == error, state(rp)


def test_read_position_secondary_while_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SequenceFlag SECONDARY while the primary sequence is active: rejected by the RC."""
    enable(robot, sdk)
    rp = read_position(
        robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE
    )
    rp.Execute = True
    robot.run(50, until=lambda: bool(rp.Done or rp.Error))
    assert rp.Error and rp.ErrorID == 0x8F16, state(rp)


def test_read_position_in_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SequenceFlag SECONDARY inside the active secondary sequence: Done with valid values."""
    enable(robot, sdk)
    sdk.joints = [4.0] + [0.0] * 11
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    execute(robot, seq)
    rp = read_position(
        robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE
    )
    execute(robot, rp, reset=False)
    assert rp.Valid and rp.OutCmd.ActualJointPosition.J1 == pytest.approx(4.0)


def test_read_position_trigger_without_listener(robot: RobotTaskHarness) -> None:
    """A trigger ProcessingMode needs a ListenerID > 0."""
    rp = read_position(robot, ProcessingMode=ProcessingMode.TRIGGER_ONCE, Execute=True)
    robot.run(10, until=lambda: bool(rp.Error))
    assert rp.Error and not rp.Busy, state(rp)


@pytest.mark.parametrize("field", ["ToolNo", "FrameNo"])
def test_read_position_number_out_of_range(robot: RobotTaskHarness, field: str) -> None:
    """Tool / frame number 255 is outside the range (-1..254 resp. the configured maximum)."""
    rp = read_position(robot)
    setattr(rp.ParCmd, field, 255)
    rp.Execute = True
    robot.run(50, until=lambda: bool(rp.Done or rp.Error))
    assert rp.Error and not rp.Done, state(rp)


# ---------------------------------------------------------------- SetOperationMode


def set_mode(h: RobotTaskHarness, mode: OperationMode, *, reset: bool = True) -> Any:
    om = fb(h, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    execute(h, om, reset=reset)
    h.run(3)
    return om


def mode_of(h: RobotTaskHarness) -> int:
    return int(h.ag.Cyclic.RobToPlc.StatusRobotArm.OperationMode)


@pytest.mark.parametrize("target", [OperationMode.T1_EXT, OperationMode.T2_EXT, OperationMode.AUTO_EXT])
def test_set_operation_mode_follows(
    robot: RobotTaskHarness, sdk: SdkSimulator, target: OperationMode
) -> None:
    """External modes: Done, the operation mode of the cyclic status (and the user data) follows.
    T2 extern is reached from T1 extern (AUTO extern -> T2 extern: test_set_operation_mode_auto_to_t2_rejected)."""
    first = OperationMode.AUTO_EXT if target == OperationMode.T1_EXT else OperationMode.T1_EXT
    set_mode(robot, first)
    assert mode_of(robot) == first
    set_mode(robot, target)
    assert mode_of(robot) == target and sdk.states.operation_mode == target
    assert int(robot.user_data.OperationMode) == target


def test_set_operation_mode_auto_to_t2_rejected(robot: RobotTaskHarness) -> None:
    """AUTO extern -> T2 extern directly: the RC rejects it (16#8C08, SDK 1.1), the mode stays."""
    set_mode(robot, OperationMode.AUTO_EXT)
    om = fb(robot, "MC_SetOperationModeFB", Execute=True)
    om.ParCmd.OperationMode = OperationMode.T2_EXT
    robot.run(50, until=lambda: bool(om.Done or om.Error))
    assert om.Error and om.ErrorID == 0x8C08 and not om.Done, state(om)
    assert mode_of(robot) == OperationMode.AUTO_EXT


def test_set_operation_mode_transitions(robot: RobotTaskHarness) -> None:
    """T1 extern -> T2 extern -> T1 extern -> auto extern."""
    for target in (OperationMode.T1_EXT, OperationMode.T2_EXT, OperationMode.T1_EXT, OperationMode.AUTO_EXT):
        set_mode(robot, target)
        assert mode_of(robot) == target


def test_set_operation_mode_unchanged(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """The active mode again: Done, the mode and the power stay unchanged."""
    enable(robot, sdk)
    active = mode_of(robot)
    set_mode(robot, OperationMode(active))
    assert mode_of(robot) == active and sdk.enabled


def test_set_operation_mode_switches_power_off(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Auto extern -> T1 extern while enabled: Done, the RC switches the power off and EnableRobot
    reports Enabled FALSE."""
    en = enable(robot, sdk)
    set_mode(robot, OperationMode.T1_EXT)
    robot.run(50, until=lambda: not en.Enabled)
    assert not sdk.enabled and not en.Enabled, state(en)


def test_set_operation_mode_done_while_execute(robot: RobotTaskHarness) -> None:
    """Done stays TRUE while Execute is TRUE and is reset with the falling edge."""
    om = set_mode(robot, OperationMode.T1_EXT, reset=False)
    robot.run(10)
    assert om.Done and not om.Busy, state(om)
    om.Execute = False
    robot.run(2)
    assert not om.Done, state(om)


def test_set_operation_mode_execute_reset_while_busy(robot: RobotTaskHarness) -> None:
    """Execute FALSE right after the start: the command still ends with Done for one cycle."""
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.T1_EXT
    om.Execute = True
    robot.run(1)
    assert om.Busy, state(om)
    om.Execute = False
    done = []
    for _ in range(50):
        robot.run(1)
        done.append(bool(om.Done))
    assert done.count(True) == 1 and not om.Error, done
    assert mode_of(robot) == OperationMode.T1_EXT


@pytest.mark.parametrize("target", [OperationMode.T1_LOCAL, OperationMode.T2_LOCAL, OperationMode.AUTO])
def test_set_operation_mode_local_rejected(robot: RobotTaskHarness, target: OperationMode) -> None:
    """Local modes cannot be selected by the PLC: Error, the mode stays."""
    active = mode_of(robot)
    om = fb(robot, "MC_SetOperationModeFB", Execute=True)
    om.ParCmd.OperationMode = target
    robot.run(50, until=lambda: bool(om.Done or om.Error))
    assert om.Error and not om.Done, state(om)
    assert mode_of(robot) == active


def test_set_operation_mode_in_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SetOperationMode while the secondary sequence is active (parallel command): Done."""
    enable(robot, sdk)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    execute(robot, seq)
    set_mode(robot, OperationMode.T1_EXT)
    assert mode_of(robot) == OperationMode.T1_EXT


# ---------------------------------------------------------------- unlinked axes group


UNLINKED = [
    "MC_EnableRobotFB",
    "MC_GroupResetFB",
    "MC_GroupInterruptFB",
    "MC_GroupContinueFB",
    "MC_MoveLinearAbsoluteFB",
    "MC_WriteLoadDataFB",
    "MC_WriteRobotSWLimitsFB",
]


@pytest.mark.parametrize("name", UNLINKED)
def test_unlinked_axes_group(name: str) -> None:
    """A block on an axes group that no RobotTask serves: Error 16#8612, nothing else happens."""
    group = AxesGroup()
    block = new_instance(name)
    start = "Enable" if hasattr(block, "Enable") and not hasattr(block, "Execute") else "Execute"
    setattr(block, start, True)
    for _ in range(5):
        block(AxesGroup=group)
    assert block.Error and block.ErrorID == E.ERR_COMMANDS_NOT_ENABLED, state(block)
    assert not getattr(block, "Busy", False)


# ---------------------------------------------------------------- command name


def test_command_name_in_message(robot: RobotTaskHarness) -> None:
    """ST-FIX F105: the user defined command name is part of the message in the message buffer
    (spec 5.5.11, table 5-47)."""
    seq = fb(robot, "MC_SetSequenceFB", Name="ToSecondary", Execute=True)
    robot.run(10, until=lambda: bool(seq.Error))
    assert seq.Error
    robot.run(3)  # the message is created in the next call
    texts = [m.MessageText for m in robot.ag.MessageLog.Messages if m.MessageText]
    assert any("MC_SetSequenceFB [ToSecondary] : " in t for t in texts), texts


def test_command_name_in_rc_error_message(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """The name is also in the message of an error reported by the RC."""
    enable(robot, sdk)
    mv = move_axes(robot, 10.0, Name="MoveToP1")
    mv.ParCmd.DecelerationRate = 0.5  # rejected by the RC
    mv.Execute = True
    robot.run(100, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Error, state(mv)
    robot.run(3)
    texts = [m.MessageText for m in robot.ag.MessageLog.Messages if m.MessageText]
    assert any("[MoveToP1]" in t for t in texts), texts


def test_without_command_name(robot: RobotTaskHarness) -> None:
    """Without a name the message keeps the block type only."""
    seq = fb(robot, "MC_SetSequenceFB", Execute=True)
    robot.run(10, until=lambda: bool(seq.Error))
    robot.run(3)
    texts = [m.MessageText for m in robot.ag.MessageLog.Messages if m.MessageText]
    assert any(t.startswith("MC_SetSequenceFB : ") for t in texts), texts
