# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_sequence_set
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of SetSequence against the SDK simulator (robot controller side).
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

"""Validation of SetSequence against the SDK simulator (robot controller side).

* switching to the secondary sequence interrupts the primary sequence (RA state Interrupted,
  SecondarySequenceActive TRUE) and holds a running primary motion
* switching back to the primary sequence: a held primary motion resumes only with
  GroupContinue, buffered secondary motions are aborted
* switching is rejected while a jog or a ReturnToPrimary uses the secondary sequence
* a jog activates the secondary sequence implicitly
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import JogMode, OperationMode, RobotLibraryErrorIdEnum, SequenceFlag, TrajectoryMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    cartesian,
    enable,
    execute,
    fb,
    finished,
    move_axes,
    order,
    state,
    watch,
)

E = RobotLibraryErrorIdEnum


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag, reset: bool = True) -> Any:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    return execute(h, seq, reset=reset)


def _rc(h: RobotTaskHarness) -> dict[str, bool]:
    u = h.user_data
    return {"Idle": u.Idle, "Interrupted": u.Interrupted, "Secondary": u.SecondarySequenceActive}


def _motion(h: RobotTaskHarness, kind: str, target: float, **inputs: Any) -> Any:
    if kind == "MC_MoveAxesAbsoluteFB":
        return move_axes(h, target, **inputs)
    mv = cartesian(fb(h, kind, **inputs), target, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    return mv


def _moving(h: RobotTaskHarness, sdk: SdkSimulator, block: Any) -> None:
    block.Execute = True
    h.run(200, until=lambda: sdk.joints[0] > 5.0 or bool(block.Error))
    assert block.Active and sdk.joints[0] > 5.0, state(block)


def _jog_start(h: RobotTaskHarness, axis: str) -> Any:
    j = fb(h, "MC_GroupJogFB", Enable=True)
    j.ParCmd.Mode = JogMode.JOG_AXES
    j.ParCmd.Override = 100
    h.run(50, until=lambda: bool(j.Enabled or j.Error))
    assert j.Enabled, state(j)
    setattr(j.ParCmd.Control, axis, True)
    return j


def _jog_stop(h: RobotTaskHarness, j: Any, axis: str) -> None:
    setattr(j.ParCmd.Control, axis, False)
    h.run(5)
    j.Enable = False
    h.run(50, until=lambda: not j.Busy)


def _held(h: RobotTaskHarness, sdk: SdkSimulator, cycles: int = 20) -> bool:
    before = list(sdk.joints)
    h.run(cycles)
    return sdk.joints == before


@pytest.mark.parametrize("hold", [True, False], ids=["execute-held", "execute-pulse"])
def test_switch_to_secondary(robot: RobotTaskHarness, hold: bool) -> None:
    """SetSequence(secondary) ends Done (Busy, Active, Done); the RA state is Interrupted and the secondary sequence is active.

    Execute held: Done stays TRUE until the falling edge; one-cycle pulse: Done is still shown."""
    enable(robot)
    assert _rc(robot) == {"Idle": True, "Interrupted": False, "Secondary": False}
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    seq.Execute = True
    if hold:
        seen = watch(robot, [seq], 100, lambda: finished(seq))[0]
        robot.run(5)
        assert seq.Done, state(seq)
        seq.Execute = False
        robot.run(2)
        assert not seq.Done, state(seq)
    else:
        robot.run(1)
        seq.Execute = False
        seen = watch(robot, [seq], 100, lambda: bool(seq.Done or seq.Error))[0]
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    assert _rc(robot)["Interrupted"] and _rc(robot)["Secondary"]


def test_switch_to_primary_while_primary(robot: RobotTaskHarness) -> None:
    """SetSequence(primary) while the primary sequence is active ends Done; the RA state stays Idle."""
    enable(robot)
    seen = _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    assert order(seen, "Busy", "Done") and not seen.final["Error"], (seen.flags, seen.final)
    assert _rc(robot) == {"Idle": True, "Interrupted": False, "Secondary": False}


def test_switch_back_to_primary(robot: RobotTaskHarness) -> None:
    """SetSequence(secondary) and then SetSequence(primary) without motions: both Done, the primary sequence is active and idle."""
    enable(robot)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE).final["Done"]
    assert _rc(robot)["Interrupted"] and _rc(robot)["Secondary"]
    back = _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    assert back.final["Done"], back.final
    assert _rc(robot) == {"Idle": True, "Interrupted": False, "Secondary": False}


def test_switch_to_primary_without_power(robot: RobotTaskHarness) -> None:
    """Without power, SetSequence(primary) from the secondary sequence ends Done and the primary sequence is active."""
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE).final["Done"]
    assert not robot.user_data.Enabled and _rc(robot)["Secondary"]
    seen = _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    assert order(seen, "Busy", "Done"), seen.flags
    assert not _rc(robot)["Secondary"]


def test_switch_in_manual_mode(robot: RobotTaskHarness) -> None:
    """In operation mode T1 external SetSequence(secondary) ends Done and the secondary sequence is active."""
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.T1_EXT
    assert execute(robot, om).final["Done"]
    seen = _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    assert seen.final["Done"], seen.final
    assert _rc(robot)["Secondary"]


def test_secondary_then_continue(robot: RobotTaskHarness) -> None:
    """SetSequence(secondary) and GroupContinue: both Done, the RA state is Idle in the secondary sequence."""
    enable(robot)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE).final["Done"]
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    assert _rc(robot) == {"Idle": True, "Interrupted": False, "Secondary": True}


def test_switch_and_interrupt_in_one_cycle(robot: RobotTaskHarness) -> None:
    """SetSequence(secondary) and GroupInterrupt in the same cycle: both Done, secondary sequence active and RA state Interrupted."""
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    gi = fb(robot, "MC_GroupInterruptFB")
    seq.Execute = gi.Execute = True
    watch(robot, [seq, gi], 100, lambda: finished(seq) and finished(gi))
    assert seq.Done and gi.Done, (state(seq), state(gi))
    assert _rc(robot)["Secondary"] and _rc(robot)["Interrupted"]


@pytest.mark.parametrize(
    "kind", ["MC_MoveDirectAbsoluteFB", "MC_MoveLinearAbsoluteFB", "MC_MoveAxesAbsoluteFB"]
)
def test_switch_interrupts_primary_motion(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str) -> None:
    """SetSequence(secondary) during a primary motion: Done, the motion is CommandInterrupted and the robot holds.

    The motion is neither Active nor Done nor aborted."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _motion(robot, kind, 100.0)
    _moving(robot, sdk, mv)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE).final["Done"]
    robot.run(3)
    assert (
        mv.CommandInterrupted and mv.Busy and not (mv.Active or mv.Done or mv.Error or mv.CommandAborted)
    ), state(mv)
    assert _held(robot, sdk)


def test_primary_motion_resumes_with_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After secondary and back to primary the held motion does not continue by itself; GroupContinue makes it Active and Done."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _motion(robot, "MC_MoveLinearAbsoluteFB", 100.0)
    _moving(robot, sdk, mv)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE).final["Done"]
    assert _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE).final["Done"]
    assert _held(robot, sdk) and mv.Busy and not mv.Active, state(mv)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    seen = watch(robot, [mv], 500, lambda: finished(mv))[0]
    assert order(seen, "Active", "Done"), seen.flags
    assert sdk.joints[0] == pytest.approx(100.0)


def test_secondary_motion_aborted_on_switch_to_primary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A buffered motion of the secondary sequence is aborted when the primary sequence is selected; GroupContinue does not start it."""
    enable(robot)
    assert _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE).final["Done"]
    mv = move_axes(robot, 30.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    mv.Execute = True
    robot.run(20)
    assert mv.CommandBuffered and not mv.Active, state(mv)
    assert _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE).final["Done"]
    robot.run(5)
    assert mv.CommandAborted and not mv.Busy, state(mv)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(20)
    assert sdk.joints[0] == 0.0 and not mv.Done


@pytest.mark.parametrize(
    "target",
    [SequenceFlag.SECONDARY_SEQUENCE, SequenceFlag.PRIMARY_SEQUENCE],
    ids=["to-secondary", "to-primary"],
)
def test_switch_rejected_while_jogging(robot: RobotTaskHarness, target: SequenceFlag) -> None:
    """SetSequence while a jog moves the robot is rejected with ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD; the jog stays active."""
    enable(robot)
    jog = _jog_start(robot, "X_J1_Pos")
    robot.run(20)
    seen = _set_sequence(robot, target)
    assert order(seen, "Busy", "Error"), seen.flags
    assert seen.final["ErrorID"] == E.ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD, seen.final
    assert jog.Active and jog.OutCmd.MotionActive, state(jog)


def test_switch_rejected_while_returning(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SetSequence while a ReturnToPrimary is active is rejected with ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD; the return finishes."""
    sdk.set_move_cycles(100)
    enable(robot)
    mv = move_axes(robot, 50.0)
    _moving(robot, sdk, mv)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    jog = _jog_start(robot, "Y_J2_Pos")
    robot.run(200)
    _jog_stop(robot, jog, "Y_J2_Pos")
    sdk.set_move_cycles(200)
    rtp = fb(robot, "MC_ReturnToPrimaryFB", Enable=True)
    rtp.ParCmd.TrajectoryMode = TrajectoryMode.LINEAR_MOVEMENT
    robot.run(100, until=lambda: bool(rtp.Active))
    seen = _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD, (
        seen.final
    )
    robot.run(400, until=lambda: bool(rtp.Done or rtp.Error))
    assert rtp.Done, state(rtp)


def test_jog_activates_secondary_sequence(robot: RobotTaskHarness) -> None:
    """GroupJog activates the secondary sequence while it runs; after the jog the flag is FALSE again."""
    enable(robot)
    assert not _rc(robot)["Secondary"]
    jog = _jog_start(robot, "X_J1_Pos")
    robot.run(20)
    assert _rc(robot)["Secondary"]
    _jog_stop(robot, jog, "X_J1_Pos")
    robot.run(5)
    assert not _rc(robot)["Secondary"]
