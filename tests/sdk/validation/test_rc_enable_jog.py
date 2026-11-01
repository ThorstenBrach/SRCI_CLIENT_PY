# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_enable_jog
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    EnableRobot against the SDK simulator: power on / off, power loss by
#    errors and operation mode changes, HoldToRun, StepMode, ManualStep.
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

"""EnableRobot against the SDK simulator (robot controller behaviour).

* switching the drives on and off, outputs and RC power state
* the RC switches the power off on an error or an operation mode change (16#8C04)
* HoldToRun in automatic external mode (continue of an interrupted sequence, release)
* HoldToRun / StepMode / ManualStep in T1 external (single point of control by the PLC)
* EnableRobot in the secondary sequence, repeated enable / disable requests

Several T1 / StepMode tests are strict xfail: the simulated RC never completes the interruption
of a sequence started from idle in T1 external or with an active StepMode (sequence state stays
"interrupting"), so HoldToRun / ManualStep / GroupContinue cannot start the buffered motion.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import CmdType, OperationMode, RobotLibraryErrorIdEnum, SequenceFlag, StepMode
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import MOVE_CYCLES, enable, execute, fb, move_axes, order, state, watch

E = RobotLibraryErrorIdEnum

ERR_DISABLED_BY_RC = 0x8C04  # robot disabled by the RC (error / operation mode change)
ERR_MANUAL_STEP_IN_AUTO = 0x8C20
ERR_MANUAL_STEP_WITHOUT_STEP_MODE = 0x8C21
ERR_CONTINUE_NOT_ALLOWED = 0x8C10
INFO_INTERRUPTED_NOT_ENABLED = 0x6F02
SEQ_IDLE, SEQ_EXECUTING, SEQ_INTERRUPT_ACTIVE = 91, 92, 93

GAP_T1 = (
    "SDK-GAP: in T1 external (and with an active StepMode) a command buffered from sequence state idle "
    "leaves the RC in sequence state 'interrupting' (95) for ever - the interruption is never completed, "
    "so the command never reports CommandInterrupted and HoldToRun / ManualStep / GroupContinue cannot "
    "start it (spec 6.1.3 EnableRobot HoldToRun / StepMode, 5.6.3 RA sequence states)"
)


# ---------------------------------------------------------------- helpers


def _set_mode(h: RobotTaskHarness, mode: OperationMode) -> None:
    om = fb(h, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    s = execute(h, om)
    assert s.final["Done"] and not s.final["Error"], s.final
    h.run(3)


def _moving(sdk: SdkSimulator, h: RobotTaskHarness, cycles: int = 5) -> bool:
    before = list(sdk.joints)
    h.run(cycles)
    return sdk.joints != before


def _wait(h: RobotTaskHarness, cond: Any, cycles: int = 300) -> bool:
    h.run(cycles, until=lambda: bool(cond()))
    return bool(cond())


# ---------------------------------------------------------------- power on / off


def test_enable_and_disable_switch_drives(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """EnableRobot with default parameters switches the drives on and Enable FALSE switches them off again.

    While enabled the RC reports power state enabled and sequence state idle; after the disable
    all outputs of the block are FALSE / 0 and the RC power state is not enabled."""
    execute(robot, fb(robot, "MC_GroupResetFB"))
    en = fb(robot, "MC_EnableRobotFB", Enable=True)
    s = watch(robot, [en], 200, lambda: bool(en.Enabled or en.Error))[0]
    assert order(s, "Busy", "Enabled") and not en.Error, s.flags
    assert sdk.enabled and sdk.states.ra_sequence_state == SEQ_IDLE
    assert robot.user_data.Enabled and robot.user_data.Idle
    en.Enable = False
    robot.run(100, until=lambda: not en.Enabled and not en.Busy)
    assert state(en) == {k: (0 if k == "ErrorID" else False) for k in state(en)}, state(en)
    assert en.WarningID == 0 and en.InfoID == 0
    robot.run(5)  # the cyclic status follows
    assert not sdk.enabled and not robot.user_data.Enabled


def test_enable_for_one_cycle_only(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Enable TRUE for a single cycle: afterwards all outputs are reset and the drives stay off."""
    execute(robot, fb(robot, "MC_GroupResetFB"))
    en = fb(robot, "MC_EnableRobotFB", Enable=True)
    robot.run(1)
    assert en.Busy, state(en)
    en.Enable = False
    robot.run(50)
    assert not any(v for k, v in state(en).items()), state(en)
    assert not sdk.enabled


def test_rc_error_disables_robot(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A motion error of the RC switches the drives off: EnableRobot reports Error 16#8C04 and Enabled FALSE."""
    sdk.set_move_cycles(200)
    en = enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(5)
    sdk.set_motion_error(0x6C02)
    assert _wait(robot, lambda: en.Error), state(en)
    assert en.ErrorID == ERR_DISABLED_BY_RC and not en.Enabled, state(en)
    assert not sdk.enabled


def test_enable_rejected_while_error_pending(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """While the RC reports a pending error a new enable request ends with Busy then Error and the drives stay off."""
    sdk.set_move_cycles(200)
    en = enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(5)
    sdk.set_motion_error(0x6C02)
    assert _wait(robot, lambda: robot.user_data.ErrorPending and en.Error)
    en.Enable = False
    robot.run(10)
    en.Enable = True
    s = watch(robot, [en], 100, lambda: bool(en.Error or en.Enabled))[0]
    assert order(s, "Busy", "Error") and not en.Enabled, s.flags
    assert not sdk.enabled


@pytest.mark.parametrize(
    ("first", "target"),
    [(OperationMode.AUTO_EXT, OperationMode.T1_EXT), (OperationMode.T1_EXT, OperationMode.AUTO_EXT)],
    ids=["auto_to_t1", "t1_to_auto"],
)
def test_operation_mode_change_disables_robot(
    robot: RobotTaskHarness, sdk: SdkSimulator, first: OperationMode, target: OperationMode
) -> None:
    """A change of the operation mode while enabled switches the drives off: EnableRobot Error 16#8C04, Enabled FALSE."""
    _set_mode(robot, first)
    en = enable(robot)
    _set_mode(robot, target)
    assert _wait(robot, lambda: en.Error), state(en)
    assert en.ErrorID == ERR_DISABLED_BY_RC and not en.Enabled, state(en)
    assert not sdk.enabled and not robot.user_data.Enabled
    assert int(robot.user_data.OperationMode) == target


def test_enable_after_failed_configuration(sdk: SdkSimulator) -> None:
    """The RC rejects the configuration of the initialization: the axes group is not initialized and EnableRobot fails.

    GroupReset and EnableRobot end with Error ERR_COMMANDS_NOT_ENABLED, the drives stay off."""
    sdk.set_move_cycles(MOVE_CYCLES)
    sdk.set_command_error(int(CmdType.ExchangeConfiguration), 0x8E05)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.run(200, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))
        assert h.rt.Error and not h.ag.State.CMDsEnabled and not h.user_data.Initialized
        en = fb(h, "MC_EnableRobotFB", Enable=True)
        h.run(200, until=lambda: bool(en.Error or en.Enabled))
        assert en.Error and en.ErrorID == E.ERR_COMMANDS_NOT_ENABLED and not en.Enabled, state(en)
        assert not sdk.enabled


@pytest.mark.parametrize("busy", [False, True], ids=["after_each_state", "while_busy"])
def test_repeated_enable_requests(robot: RobotTaskHarness, sdk: SdkSimulator, busy: bool) -> None:
    """Alternating enable / disable requests are processed one after the other; the last request (enable) wins."""
    execute(robot, fb(robot, "MC_GroupResetFB"))
    en = fb(robot, "MC_EnableRobotFB", Enable=True)
    robot.run(1)
    assert en.Busy, state(en)
    for target in (False, True, False, True):
        if busy:
            robot.run(1)  # the next request one cycle later, the previous one is still in process
        else:
            assert _wait(robot, lambda: en.Enabled != target and not en.Busy, 100), state(en)  # noqa: B023
        en.Enable = target
    assert _wait(robot, lambda: en.Enabled or en.Error, 200), state(en)
    assert en.Enabled and not en.Error and en.ErrorID == 0, state(en)
    assert sdk.enabled


def test_enable_in_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """EnableRobot works while the secondary sequence is active and the robot can be disabled after the switch back."""
    execute(robot, fb(robot, "MC_GroupResetFB"))
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert robot.user_data.SecondarySequenceActive
    en = fb(robot, "MC_EnableRobotFB", Enable=True)
    s = watch(robot, [en], 200, lambda: bool(en.Enabled or en.Error))[0]
    assert order(s, "Busy", "Enabled") and sdk.enabled, s.flags
    seq.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert not robot.user_data.SecondarySequenceActive
    en.Enable = False
    assert _wait(robot, lambda: not en.Enabled and not en.Busy, 100)
    assert not en.Error and not sdk.enabled


# ---------------------------------------------------------------- HoldToRun in automatic external


def test_hold_to_run_continues_interrupted_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Auto external: a rising edge of HoldToRun continues an interrupted sequence; the move runs Active then Done."""
    en = enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(3)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    assert _wait(robot, lambda: mv.CommandInterrupted, 20), state(mv)
    assert robot.user_data.Interrupted and not _moving(sdk, robot)
    en.ParCmd.HoldToRun = True
    s = watch(robot, [mv], 300, lambda: bool(mv.Done or mv.Error))[0]
    assert order(s, "CommandInterrupted", "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(10.0)


def test_hold_to_run_release_without_press_has_no_effect(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Auto external: HoldToRun pulsed while a move is executing does not stop it; the move reaches Done."""
    en = enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    assert _wait(robot, lambda: mv.Active, 20)
    en.ParCmd.HoldToRun = True
    robot.run(10)
    en.ParCmd.HoldToRun = False
    s = watch(robot, [mv], 300, lambda: bool(mv.Done or mv.Error))[0]
    assert mv.Done and "CommandInterrupted" not in s.flags, s.flags
    assert sdk.joints[0] == pytest.approx(10.0) and en.ErrorID == 0


def test_hold_to_run_release_interrupts_after_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Auto external: after a continue by HoldToRun, releasing HoldToRun interrupts the move; pressing it again finishes it."""
    sdk.set_move_cycles(100)
    en = enable(robot)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(10)
    assert not mv.Active and sdk.joints[0] == 0.0, state(mv)
    en.ParCmd.HoldToRun = True
    assert _wait(robot, lambda: mv.Active, 30) and _moving(sdk, robot)
    en.ParCmd.HoldToRun = False
    assert _wait(robot, lambda: mv.CommandInterrupted, 30), state(mv)
    assert not _moving(sdk, robot, 10) and not mv.Done
    en.ParCmd.HoldToRun = True
    assert _wait(robot, lambda: mv.Done or mv.Error), state(mv)
    assert mv.Done and sdk.joints[0] == pytest.approx(10.0)


@pytest.mark.parametrize("hold_to_run", [False, True], ids=["released", "pressed"])
@pytest.mark.parametrize("count", [2, 4])
def test_moves_run_without_hold_to_run_in_auto(
    robot: RobotTaskHarness, sdk: SdkSimulator, count: int, hold_to_run: bool
) -> None:
    """Auto external: buffered moves are executed one after the other independent of HoldToRun, each Active then Done."""
    en = enable(robot)
    en.ParCmd.HoldToRun = hold_to_run
    moves = [move_axes(robot, 2.0 * (i + 1)) for i in range(count)]
    for mv in moves:
        mv.Execute = True
    seen = watch(robot, moves, 200 * count, lambda: all(m.Done or m.Error for m in moves))
    for s in seen:
        assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(2.0 * count)


def test_hold_to_run_continues_after_sequence_switch(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A move interrupted by switching to the secondary sequence and back is continued by HoldToRun and reaches Done."""
    sdk.set_move_cycles(200)
    en = enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    assert _wait(robot, lambda: mv.Active, 20)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert _wait(robot, lambda: mv.CommandInterrupted, 20), state(mv)
    seq.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert not _moving(sdk, robot, 10) and not mv.Done
    en.ParCmd.HoldToRun = True
    s = watch(robot, [mv], 400, lambda: bool(mv.Done or mv.Error))[0]
    assert order(s, "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(10.0)


# ---------------------------------------------------------------- ManualStep / StepMode errors


@pytest.mark.parametrize(
    ("mode", "step_mode", "error"),
    [
        (OperationMode.AUTO_EXT, StepMode.DEACTIVATE, ERR_MANUAL_STEP_IN_AUTO),
        (OperationMode.AUTO_EXT, StepMode.BLENDING, ERR_MANUAL_STEP_IN_AUTO),
        (OperationMode.T1_EXT, StepMode.DEACTIVATE, ERR_MANUAL_STEP_WITHOUT_STEP_MODE),
    ],
    ids=["auto", "auto_step_mode", "t1_without_step_mode"],
)
def test_manual_step_rejected(
    robot: RobotTaskHarness, mode: OperationMode, step_mode: StepMode, error: int
) -> None:
    """ManualStep is rejected by the RC in auto external (16#8C20) and in T1 without StepMode (16#8C21)."""
    _set_mode(robot, mode)
    en = enable(robot)
    en.ParCmd.StepMode = step_mode
    robot.run(5)
    en.ParCmd.ManualStep = True
    assert _wait(robot, lambda: en.Error, 50), state(en)
    assert en.ErrorID == error, hex(en.ErrorID)


def test_continue_rejected_in_t1(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """T1 external: GroupContinue is not allowed (16#8C10); the buffered move does not start."""
    _set_mode(robot, OperationMode.T1_EXT)
    enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    robot.run(10)
    gc = fb(robot, "MC_GroupContinueFB")
    s = execute(robot, gc)
    assert s.final["Error"] and s.final["ErrorID"] == ERR_CONTINUE_NOT_ALLOWED, s.final
    assert not mv.Active and not mv.Done and sdk.joints[0] == 0.0


# ---------------------------------------------------------------- HoldToRun / StepMode in T1 (SDK gap)


@pytest.mark.xfail(strict=True, reason=GAP_T1)
@pytest.mark.parametrize("pressed_before", [False, True], ids=["press_after_buffer", "press_before_buffer"])
def test_t1_move_runs_only_with_hold_to_run(
    robot: RobotTaskHarness, sdk: SdkSimulator, pressed_before: bool
) -> None:
    """T1 external: a buffered move waits interrupted without HoldToRun and runs Active then Done while HoldToRun is TRUE."""
    _set_mode(robot, OperationMode.T1_EXT)
    en = enable(robot)
    if pressed_before:
        en.ParCmd.HoldToRun = True
        robot.run(3)
        en.ParCmd.HoldToRun = False
        robot.run(3)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    assert _wait(robot, lambda: mv.CommandInterrupted, 30), state(mv)
    assert robot.user_data.Interrupted and sdk.joints[0] == 0.0
    en.ParCmd.HoldToRun = True
    s = watch(robot, [mv], 300, lambda: bool(mv.Done or mv.Error))[0]
    assert order(s, "Busy", "CommandBuffered", "CommandInterrupted", "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(10.0) and robot.user_data.Idle


@pytest.mark.xfail(strict=True, reason=GAP_T1)
def test_t1_release_hold_to_run_interrupts(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """T1 external: releasing HoldToRun while moving interrupts the move; pressing it again finishes the move."""
    sdk.set_move_cycles(100)
    _set_mode(robot, OperationMode.T1_EXT)
    en = enable(robot)
    mv = move_axes(robot, 10.0)
    mv.Execute = True
    assert _wait(robot, lambda: mv.CommandInterrupted, 30), state(mv)
    en.ParCmd.HoldToRun = True
    assert _wait(robot, lambda: mv.Active, 30) and _moving(sdk, robot)
    en.ParCmd.HoldToRun = False
    assert _wait(robot, lambda: mv.CommandInterrupted and not mv.Active, 30), state(mv)
    assert not _moving(sdk, robot, 10)
    en.ParCmd.HoldToRun = True
    assert _wait(robot, lambda: mv.Done or mv.Error) and mv.Done, state(mv)


@pytest.mark.xfail(strict=True, reason=GAP_T1)
@pytest.mark.parametrize("pressed_before", [False, True], ids=["press_after_buffer", "press_before_buffer"])
def test_t1_several_moves_with_hold_to_run(
    robot: RobotTaskHarness, sdk: SdkSimulator, pressed_before: bool
) -> None:
    """T1 external: four buffered moves wait interrupted and run one after the other in order while HoldToRun is TRUE."""
    _set_mode(robot, OperationMode.T1_EXT)
    en = enable(robot)
    moves = [move_axes(robot, 2.0 * (i + 1)) for i in range(4)]
    if pressed_before:
        en.ParCmd.HoldToRun = True
    for mv in moves:
        mv.Execute = True
        robot.run(2)
    if pressed_before:
        en.ParCmd.HoldToRun = False
        robot.run(3)
    assert _wait(robot, lambda: all(m.CommandInterrupted for m in moves), 30), [state(m) for m in moves]
    en.ParCmd.HoldToRun = True
    seen = watch(robot, moves, 1000, lambda: all(m.Done or m.Error for m in moves))
    assert all(order(s, "CommandInterrupted", "Active", "Done") for s in seen), [s.flags for s in seen]
    assert sdk.joints[0] == pytest.approx(8.0) and robot.user_data.Idle


@pytest.mark.xfail(strict=True, reason=GAP_T1)
@pytest.mark.parametrize(
    ("mode", "step_mode", "trigger"),
    [
        (OperationMode.T1_EXT, StepMode.BLENDING, "hold_to_run"),
        (OperationMode.T1_EXT, StepMode.BLENDING, "manual_step"),
        (OperationMode.T1_EXT, StepMode.EXACT_STOP, "manual_step"),
        (OperationMode.AUTO_EXT, StepMode.BLENDING, "hold_to_run"),
        (OperationMode.AUTO_EXT, StepMode.BLENDING, "continue"),
    ],
    ids=[
        "t1_blending_hold_to_run",
        "t1_blending_manual_step",
        "t1_exact_stop_manual_step",
        "auto_blending_hold_to_run",
        "auto_blending_continue",
    ],
)
def test_step_mode_stops_after_each_command(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: OperationMode, step_mode: StepMode, trigger: str
) -> None:
    """With StepMode active the RC interrupts before every command; each trigger (HoldToRun edge, ManualStep,
    continue) runs exactly one command.
    """
    _set_mode(robot, mode)
    en = enable(robot)
    en.ParCmd.StepMode = step_mode
    robot.run(5)
    moves = [move_axes(robot, 2.0 * (i + 1)) for i in range(3)]
    for mv in moves:
        mv.Execute = True
        robot.run(2)
    assert _wait(robot, lambda: moves[0].CommandInterrupted, 30), state(moves[0])
    for i, mv in enumerate(moves):
        if trigger == "continue":
            assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
        else:
            name = "HoldToRun" if trigger == "hold_to_run" else "ManualStep"
            setattr(en.ParCmd, name, True)
            robot.run(3)
            if trigger == "manual_step":
                setattr(en.ParCmd, name, False)
        assert _wait(robot, lambda: mv.Done or mv.Error), state(mv)  # noqa: B023
        assert mv.Done, state(mv)
        if trigger == "hold_to_run":
            en.ParCmd.HoldToRun = False
        for later in moves[i + 1 :]:
            assert not later.Active and not later.Done, state(later)
        robot.run(5)
    assert sdk.joints[0] == pytest.approx(6.0) and not en.Error


@pytest.mark.xfail(strict=True, reason=GAP_T1)
def test_step_mode_and_group_interrupt_with_hold_to_run(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """StepMode active: a GroupInterrupt during the first move holds it, HoldToRun edges finish both moves one by one."""
    en = enable(robot)
    en.ParCmd.StepMode = StepMode.BLENDING
    robot.run(5)
    moves = [move_axes(robot, 5.0), move_axes(robot, 10.0)]
    for mv in moves:
        mv.Execute = True
        robot.run(2)
    en.ParCmd.HoldToRun = True
    assert _wait(robot, lambda: moves[0].Active, 30), state(moves[0])
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    assert _wait(robot, lambda: moves[0].CommandInterrupted, 30)
    for mv in moves:
        en.ParCmd.HoldToRun = False
        robot.run(2)
        en.ParCmd.HoldToRun = True
        assert _wait(robot, lambda: mv.Done or mv.Error) and mv.Done, state(mv)  # noqa: B023
    assert sdk.joints[0] == pytest.approx(10.0)


@pytest.mark.xfail(strict=True, reason=GAP_T1)
def test_step_mode_switched_off_runs_remaining_commands(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """StepMode switched off after the first continue: the remaining buffered moves run without further interruption."""
    en = enable(robot)
    en.ParCmd.StepMode = StepMode.BLENDING
    robot.run(5)
    moves = [move_axes(robot, 2.0 * (i + 1)) for i in range(3)]
    for mv in moves:
        mv.Execute = True
        robot.run(2)
    assert _wait(robot, lambda: moves[0].CommandInterrupted, 30), state(moves[0])
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    en.ParCmd.StepMode = StepMode.DEACTIVATE
    robot.run(5)
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    assert _wait(robot, lambda: all(m.Done or m.Error for m in moves), 1000)
    assert all(m.Done for m in moves) and sdk.joints[0] == pytest.approx(6.0)


def test_step_mode_switched_on_while_moving(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """StepMode switched on during the first move interrupts the sequence; GroupContinue finishes the first move and the next waits."""
    sdk.set_move_cycles(100)
    en = enable(robot)
    moves = [move_axes(robot, 2.0 * (i + 1)) for i in range(3)]
    for mv in moves:
        mv.Execute = True
    assert _wait(robot, lambda: moves[0].Active, 30)
    en.ParCmd.StepMode = StepMode.BLENDING
    assert _wait(robot, lambda: moves[0].CommandInterrupted, 30), state(moves[0])
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    assert _wait(robot, lambda: moves[0].Done or moves[0].Error) and moves[0].Done, state(moves[0])
    robot.run(20)
    assert not moves[1].Active and not moves[1].Done, state(moves[1])
    assert sdk.joints[0] == pytest.approx(2.0)
