# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_group_interrupt
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of GroupInterrupt and GroupContinue against the SDK simulator.
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

"""Validation of GroupInterrupt and GroupContinue against the SDK simulator.

GroupInterrupt:

* the active motion is held (CommandInterrupted), buffered motions stay buffered
* works in the secondary sequence, without power and together with other commands of the cycle

GroupContinue:

* resumes an interrupted sequence; the RA sequence state goes back from Interrupted
* rejected when the robot left the path, in a manual mode or without power
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import JogMode, OperationMode, RobotLibraryErrorIdEnum, SequenceFlag
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


def _linear(h: RobotTaskHarness, x: float, **inputs: Any) -> Any:
    mv = cartesian(fb(h, "MC_MoveLinearAbsoluteFB", **inputs), x, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    return mv


def _moving(h: RobotTaskHarness, sdk: SdkSimulator, block: Any) -> None:
    block.Execute = True
    h.run(200, until=lambda: sdk.joints[0] > 5.0 or bool(block.Error))
    assert block.Active and sdk.joints[0] > 5.0, state(block)


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    s = execute(h, seq)
    assert s.final["Done"], s.final


def _jog_start(h: RobotTaskHarness, axis: str) -> Any:
    """GroupJog in joint mode, ``axis`` pressed (the simulator jogs 0.1 per cycle)."""
    j = fb(h, "MC_GroupJogFB", Enable=True)
    j.ParCmd.Mode = JogMode.JOG_AXES
    j.ParCmd.Override = 100
    h.run(50, until=lambda: bool(j.Enabled or j.Error))
    assert j.Enabled, state(j)
    setattr(j.ParCmd.Control, axis, True)
    return j


def _jog(h: RobotTaskHarness, axis: str, cycles: int) -> None:
    j = _jog_start(h, axis)
    h.run(cycles)
    setattr(j.ParCmd.Control, axis, False)
    h.run(5)
    j.Enable = False
    h.run(50, until=lambda: not j.Busy)


def _rc(h: RobotTaskHarness) -> dict[str, bool]:
    u = h.user_data
    return {
        "Idle": u.Idle,
        "Executing": u.Executing,
        "Interrupted": u.Interrupted,
        "Secondary": u.SecondarySequenceActive,
        "Enabled": u.Enabled,
    }


def _held(h: RobotTaskHarness, sdk: SdkSimulator, cycles: int = 20) -> bool:
    before = list(sdk.joints)
    h.run(cycles)
    return sdk.joints == before


# ---------------------------------------------------------------- GroupInterrupt


@pytest.mark.parametrize("hold", [True, False], ids=["execute-held", "execute-pulse"])
def test_interrupt_holds_linear_motion(robot: RobotTaskHarness, sdk: SdkSimulator, hold: bool) -> None:
    """GroupInterrupt during a linear motion ends Done, the motion is CommandInterrupted and the robot stands still.

    Execute held: Done stays TRUE until the falling edge; one-cycle pulse: Done is still shown."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    gi = fb(robot, "MC_GroupInterruptFB")
    gi.Execute = True
    if hold:
        seen = watch(robot, [gi], 100, lambda: finished(gi))[0]
        robot.run(5)
        assert gi.Done, state(gi)
        gi.Execute = False
        robot.run(2)
        assert not gi.Done, state(gi)
    else:
        robot.run(1)
        gi.Execute = False
        seen = watch(robot, [gi], 100, lambda: bool(gi.Done or gi.Error))[0]
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    robot.run(3)
    assert mv.CommandInterrupted and mv.Busy and not mv.Active and not mv.Done, state(mv)
    assert _rc(robot)["Interrupted"]
    assert _held(robot, sdk)


def test_interrupt_then_buffer_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A motion started while interrupted is buffered; GroupContinue finishes the interrupted and then the new motion."""
    sdk.set_move_cycles(200)
    enable(robot)
    first = _linear(robot, 100.0)
    _moving(robot, sdk, first)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    second = _linear(robot, 20.0)
    second.Execute = True
    robot.run(10)
    assert second.CommandBuffered and not second.Active, state(second)
    assert _held(robot, sdk)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(800, until=lambda: finished(second))
    assert first.Done and second.Done, (state(first), state(second))
    assert sdk.joints[0] == pytest.approx(20.0)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: GroupInterrupt during an active jog stays Busy/Active and the jog keeps moving; "
        "GroupInterrupt (spec 6.3.6) must interrupt every motion, so the jog has to be aborted"
    ),
)
def test_interrupt_aborts_jog(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt while jogging ends Done, the jog is aborted and the robot stands still."""
    enable(robot)
    jog = _jog_start(robot, "X_J1_Pos")
    robot.run(20)
    assert jog.OutCmd.MotionActive
    gi = fb(robot, "MC_GroupInterruptFB")
    gi.Execute = True
    robot.run(100, until=lambda: finished(gi))
    assert gi.Done, state(gi)
    robot.run(5)
    assert jog.CommandAborted and not jog.Active, state(jog)
    assert _held(robot, sdk)


def test_interrupt_secondary_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt during a motion of the secondary sequence interrupts that motion."""
    sdk.set_move_cycles(200)
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    mv = _linear(robot, 100.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    mv.Execute = True
    robot.run(5)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(200, until=lambda: sdk.joints[0] > 5.0)
    assert mv.Active, state(mv)
    seen = execute(robot, fb(robot, "MC_GroupInterruptFB"))
    assert seen.final["Done"], seen.final
    robot.run(3)
    assert mv.CommandInterrupted and not mv.Active, state(mv)
    assert _rc(robot)["Interrupted"] and _rc(robot)["Secondary"]
    assert _held(robot, sdk)


def test_continue_and_interrupt_in_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupContinue followed by GroupInterrupt in the same cycle: the interrupt wins, the motion is held."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    gc = fb(robot, "MC_GroupContinueFB")
    gi = fb(robot, "MC_GroupInterruptFB")
    gc.Execute = gi.Execute = True
    watch(robot, [gc, gi], 100, lambda: finished(gc) and finished(gi))
    assert gi.Done, state(gi)
    robot.run(3)
    assert mv.CommandInterrupted, state(mv)
    assert _rc(robot)["Interrupted"]
    assert _held(robot, sdk)


def test_stop_and_interrupt_in_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop and GroupInterrupt in the same cycle: both Done, the motion is aborted and the RA state is Interrupted."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    gs = fb(robot, "MC_GroupStopFB")
    gi = fb(robot, "MC_GroupInterruptFB")
    gs.Execute = gi.Execute = True
    watch(robot, [gs, gi], 100, lambda: finished(gs) and finished(gi))
    assert gs.Done and gi.Done, (state(gs), state(gi))
    robot.run(5)
    assert mv.CommandAborted and not mv.Done, state(mv)
    assert _rc(robot)["Interrupted"]


def test_interrupt_without_power(robot: RobotTaskHarness) -> None:
    """GroupInterrupt without power ends Done and the RA sequence state changes to Interrupted."""
    assert not robot.user_data.Enabled
    seen = execute(robot, fb(robot, "MC_GroupInterruptFB"))
    assert order(seen, "Busy", "Done") and not seen.final["Error"], (seen.flags, seen.final)
    assert _rc(robot)["Interrupted"]


def test_interrupts_and_motions_in_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Motion, interrupt, motion, interrupt, motion in one cycle: both interrupts Done, no motion runs.

    Every GroupInterrupt increases the stop counter by one; the motions stay buffered."""
    sdk.set_move_cycles(100)
    enable(robot)
    counter = robot.ag.Cyclic.PlcToRob.FastStop
    blocks = [
        _linear(robot, 30.0),
        fb(robot, "MC_GroupInterruptFB"),
        _linear(robot, 60.0),
        fb(robot, "MC_GroupInterruptFB"),
        _linear(robot, 90.0),
    ]
    for b in blocks:
        b.Execute = True
    m0, i0, m1, i1, m2 = blocks
    watch(robot, blocks, 200, lambda: finished(i0) and finished(i1))
    robot.run(50)
    assert i0.Done and i1.Done, (state(i0), state(i1))
    for m in (m0, m1, m2):
        assert m.Busy and m.CommandBuffered and not (m.Done or m.Error or m.Active), state(m)
    assert sdk.joints[0] == 0.0
    assert robot.ag.Cyclic.PlcToRob.FastStop == counter + 2
    assert _rc(robot)["Interrupted"]


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: 16 stopping commands in one cycle overflow the 4-bit stop counter (spec 5.6.6.2.1); "
        "the SDK only logs a warning and answers every GroupInterrupt Done, no error is reported"
    ),
)
def test_more_than_15_interrupts_in_one_cycle(robot: RobotTaskHarness) -> None:
    """Sixteen GroupInterrupt blocks started in the same cycle end with an error of the RC."""
    blocks = [fb(robot, "MC_GroupInterruptFB") for _ in range(16)]
    for b in blocks:
        b.Execute = True
    robot.run(300, until=lambda: all(finished(b) for b in blocks))
    assert any(b.Error and b.ErrorID for b in blocks), [state(b) for b in blocks]


# ---------------------------------------------------------------- GroupContinue


def test_continue_after_interrupt_returns_to_idle(robot: RobotTaskHarness) -> None:
    """GroupInterrupt then GroupContinue at standstill: the RA state goes Idle -> Interrupted -> Idle, both blocks Done."""
    enable(robot)
    assert _rc(robot)["Idle"]
    gi = execute(robot, fb(robot, "MC_GroupInterruptFB"))
    assert gi.final["Done"] and _rc(robot)["Interrupted"], (gi.final, _rc(robot))
    gc = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert order(gc, "Busy", "Done") and gc.final["Done"], (gc.flags, gc.final)
    assert _rc(robot)["Idle"] and not _rc(robot)["Interrupted"]


def test_continue_off_path_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupContinue after jogging away from the interrupted path is rejected with ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_IN_PRIMARY_POS."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    _jog(robot, "Y_J2_Pos", 50)
    assert not robot.user_data.InPrimaryPos
    seen = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert order(seen, "Busy", "Error"), seen.flags
    assert seen.final["ErrorID"] == E.ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_IN_PRIMARY_POS, seen.final
    assert _held(robot, sdk) and mv.Busy and not mv.Active


def test_continue_off_path_in_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Off the path, GroupContinue is accepted after switching to the secondary sequence (Done, RA state Idle)."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    _jog(robot, "Y_J2_Pos", 50)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    seen = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    assert _rc(robot)["Idle"] and _rc(robot)["Secondary"]
    assert mv.Busy and not mv.Active, state(mv)


def test_continue_in_manual_mode_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupContinue in operation mode T1 external is rejected with ERR_CONTINUE_NOT_POSSIBLE_BY_MANUAL_MODE, the robot does not move."""
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.T1_EXT
    assert execute(robot, om).final["Done"]
    enable(robot)
    mv = move_axes(robot, 30.0)
    mv.Execute = True
    robot.run(20)
    assert mv.CommandBuffered and not mv.Active, state(mv)
    seen = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_CONTINUE_NOT_POSSIBLE_BY_MANUAL_MODE, (
        seen.final
    )
    assert _held(robot, sdk) and sdk.joints[0] == 0.0


def test_continue_when_not_interrupted(robot: RobotTaskHarness) -> None:
    """GroupContinue while the robot is idle and not interrupted ends Done and changes nothing (RA state stays Idle)."""
    enable(robot)
    seen = execute(robot, fb(robot, "MC_GroupContinueFB"), reset=False)
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    assert _rc(robot)["Idle"] and not _rc(robot)["Interrupted"]


def test_continue_interrupted_secondary_sequence(robot: RobotTaskHarness) -> None:
    """After SetSequence(secondary) the RA state is Interrupted; GroupContinue ends Done and the state is Idle."""
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    assert _rc(robot)["Interrupted"] and _rc(robot)["Secondary"]
    seen = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert seen.final["Done"], seen.final
    assert _rc(robot)["Idle"] and _rc(robot)["Secondary"]


@pytest.mark.parametrize("interrupted", [True, False], ids=["interrupted", "not-interrupted"])
def test_continue_without_power_rejected(robot: RobotTaskHarness, interrupted: bool) -> None:
    """GroupContinue without power is rejected with ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_ENABLED."""
    if interrupted:
        execute(robot, fb(robot, "MC_GroupInterruptFB"))
        assert _rc(robot)["Interrupted"]
    seen = execute(robot, fb(robot, "MC_GroupContinueFB"))
    assert order(seen, "Busy", "Error"), seen.flags
    assert seen.final["ErrorID"] == E.ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_ENABLED, seen.final
