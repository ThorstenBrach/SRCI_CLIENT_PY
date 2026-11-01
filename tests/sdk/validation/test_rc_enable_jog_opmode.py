# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_enable_jog_opmode
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    SetOperationMode against the SDK simulator: transitions between the
#    external operation modes, output flags, power off, rejected transitions.
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

"""SetOperationMode against the SDK simulator (robot controller behaviour).

* allowed transitions between the external modes: Busy then Done, Done stays while Execute is
  TRUE and is reset with Execute FALSE, the operation mode of the cyclic status follows
* the active mode once more: Done, nothing changes
* a change while enabled switches the drives off
* auto external <-> T2 external directly is rejected (the RC requires T1 external in between)
* a local mode selected at the robot blocks every change by the PLC (stimulated by an RC error)
"""

from __future__ import annotations

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import CmdType, OperationMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, order, state

ERR_MUST_PASS_T1 = 0x8C08
ERR_CHANGE_NOT_POSSIBLE_LOCAL = 0x8C56


def _mode(h: RobotTaskHarness) -> int:
    return int(h.ag.Cyclic.RobToPlc.StatusRobotArm.OperationMode)


def _set_mode(h: RobotTaskHarness, mode: OperationMode) -> None:
    om = fb(h, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    s = execute(h, om)
    assert s.final["Done"] and not s.final["Error"], s.final
    h.run(3)


@pytest.mark.parametrize("enabled", [False, True], ids=["disabled", "enabled"])
@pytest.mark.parametrize(
    ("first", "target"),
    [
        (OperationMode.AUTO_EXT, OperationMode.T1_EXT),
        (OperationMode.T1_EXT, OperationMode.AUTO_EXT),
        (OperationMode.T1_EXT, OperationMode.T2_EXT),
        (OperationMode.T2_EXT, OperationMode.T1_EXT),
    ],
    ids=["auto_to_t1", "t1_to_auto", "t1_to_t2", "t2_to_t1"],
)
def test_mode_change_done_and_reset(
    robot: RobotTaskHarness, sdk: SdkSimulator, first: OperationMode, target: OperationMode, enabled: bool
) -> None:
    """An allowed mode change ends with Busy then Done; Done stays while Execute is TRUE, is reset with
    Execute FALSE, and the mode follows.
    """
    if first == OperationMode.T2_EXT:
        _set_mode(robot, OperationMode.T1_EXT)
    _set_mode(robot, first)
    if enabled:
        enable(robot)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = target
    s = execute(robot, om, reset=False)
    assert order(s, "Busy", "Done") and not om.Error, s.flags
    robot.run(10)
    assert om.Done and not om.Busy, state(om)
    om.Execute = False
    robot.run(2)
    assert not any(v for v in state(om).values()), state(om)
    assert _mode(robot) == target == sdk.states.operation_mode
    assert int(robot.user_data.OperationMode) == target


def test_auto_to_t1_while_enabled_switches_power_off(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Auto external to T1 external while enabled: Busy then Done, the mode is T1 external and the RC switches the drives off."""
    _set_mode(robot, OperationMode.AUTO_EXT)
    enable(robot)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.T1_EXT
    s = execute(robot, om)
    assert order(s, "Busy", "Done") and not s.final["Error"], s.flags
    robot.run(10)
    assert _mode(robot) == OperationMode.T1_EXT
    assert not sdk.enabled and not robot.user_data.Enabled


def test_same_mode_again_is_done_without_change(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Selecting the active auto external mode once more ends with Done; the mode and the power state stay unchanged."""
    _set_mode(robot, OperationMode.AUTO_EXT)
    enable(robot)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.AUTO_EXT
    s = execute(robot, om)
    assert order(s, "Busy", "Done") and not s.final["Error"], s.flags
    robot.run(10)
    assert _mode(robot) == OperationMode.AUTO_EXT and sdk.enabled


@pytest.mark.parametrize(
    ("first", "target"),
    [(OperationMode.AUTO_EXT, OperationMode.T2_EXT), (OperationMode.T2_EXT, OperationMode.AUTO_EXT)],
    ids=["auto_to_t2", "t2_to_auto"],
)
def test_direct_switch_between_auto_and_t2_rejected(
    robot: RobotTaskHarness, first: OperationMode, target: OperationMode
) -> None:
    """Auto external and T2 external cannot be switched directly: Error 16#8C08 (T1 external first), the mode stays."""
    if first == OperationMode.T2_EXT:
        _set_mode(robot, OperationMode.T1_EXT)
    _set_mode(robot, first)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = target
    s = execute(robot, om)
    assert order(s, "Busy", "Error") and s.final["ErrorID"] == ERR_MUST_PASS_T1, s.final
    assert _mode(robot) == first


def test_change_rejected_in_local_mode(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """While a local mode is active at the robot the RC rejects a change by the PLC (16#8C56): Busy then Error, the mode stays.

    The simulator cannot select a local mode; the RC answer is stimulated by a forced command error."""
    active = _mode(robot)
    sdk.set_command_error(int(CmdType.SetOperationMode), ERR_CHANGE_NOT_POSSIBLE_LOCAL)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = OperationMode.T1_EXT
    s = execute(robot, om)
    assert order(s, "Busy", "Error") and s.final["ErrorID"] == ERR_CHANGE_NOT_POSSIBLE_LOCAL, s.final
    assert not s.final["Done"] and _mode(robot) == active
