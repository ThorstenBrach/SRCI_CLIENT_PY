# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_sequence_override
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of ChangeSpeedOverride against the SDK simulator.
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

"""Validation of ChangeSpeedOverride against the SDK simulator (robot controller side).

* the RC starts with 5 % after the initialization
* every value 0..100 % is applied and reported as ActualOverride (also without power and in
  the external manual modes)
* 0 % holds a motion, a higher value lets it finish; a change during a motion is applied at once

For the motion tests the simulated robot scales its motion with the override
(``set_override_motion``).
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import OperationMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import cartesian, enable, execute, fb, finished, order, state, watch


def _override(h: RobotTaskHarness, value: float) -> Any:
    ov = fb(h, "MC_ChangeSpeedOverrideFB")
    ov.ParCmd.Override = value
    return ov


def _apply(h: RobotTaskHarness, value: float) -> None:
    s = execute(h, _override(h, value))
    assert s.final["Done"], s.final


def _direct(h: RobotTaskHarness, x: float, velocity: float = 100.0) -> Any:
    mv = cartesian(fb(h, "MC_MoveDirectAbsoluteFB"), x, 0.0, 0.0)
    mv.ParCmd.VelocityRate = velocity
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    return mv


def test_initial_override_after_initialization(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After the initialization of the interface the RC reports an actual override of 5 %."""
    assert robot.user_data.ActualOverride == pytest.approx(5.0)
    assert sdk.override == pytest.approx(5.0)


@pytest.mark.parametrize("hold", [True, False], ids=["execute-held", "execute-pulse"])
def test_override_applied(robot: RobotTaskHarness, sdk: SdkSimulator, hold: bool) -> None:
    """ChangeSpeedOverride from 50 % to 10 % ends Done and the actual override is 10 %.

    Execute held: Done stays TRUE until the falling edge; one-cycle pulse: Done is still shown."""
    enable(robot)
    _apply(robot, 50.0)
    assert robot.user_data.ActualOverride == pytest.approx(50.0)
    ov = _override(robot, 10.0)
    ov.Execute = True
    if hold:
        seen = watch(robot, [ov], 100, lambda: finished(ov))[0]
        robot.run(5)
        assert ov.Done, state(ov)
        ov.Execute = False
        robot.run(2)
        assert not ov.Done, state(ov)
    else:
        robot.run(1)
        ov.Execute = False
        seen = watch(robot, [ov], 100, lambda: bool(ov.Done or ov.Error))[0]
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    robot.run(2)
    assert robot.user_data.ActualOverride == pytest.approx(10.0) and sdk.override == pytest.approx(10.0)


@pytest.mark.parametrize("value", [0.0, 0.01, 10.0, 35.5, 50.0, 99.99, 100.0])
def test_override_values(robot: RobotTaskHarness, sdk: SdkSimulator, value: float) -> None:
    """ChangeSpeedOverride with a value in 0..100 % ends Done and the RC reports exactly this value (resolution 0.01 %)."""
    enable(robot)
    _apply(robot, 50.0 if value != 50.0 else 20.0)
    _apply(robot, value)
    robot.run(2)
    assert robot.user_data.ActualOverride == pytest.approx(value, abs=0.005)
    assert sdk.override == pytest.approx(value, abs=0.005)


def test_override_values_in_a_row(robot: RobotTaskHarness) -> None:
    """One ChangeSpeedOverride instance executed again for several values: every run ends Done with the new value applied."""
    enable(robot)
    ov = _override(robot, 10.0)
    for value in (10.0, 25.0, 50.0, 75.0, 100.0, 5.0):
        ov.ParCmd.Override = value
        seen = execute(robot, ov)
        assert seen.final["Done"] and not seen.final["Error"], (value, seen.final)
        robot.run(2)
        assert robot.user_data.ActualOverride == pytest.approx(value), value
    assert not (ov.Busy or ov.Done or ov.Error or ov.CommandBuffered), state(ov)


def test_override_without_power(robot: RobotTaskHarness) -> None:
    """ChangeSpeedOverride without power ends Done and the value is applied."""
    assert not robot.user_data.Enabled
    seen = execute(robot, _override(robot, 10.0))
    assert order(seen, "Busy", "Done"), seen.flags
    robot.run(2)
    assert robot.user_data.ActualOverride == pytest.approx(10.0)


@pytest.mark.parametrize(
    "mode", [OperationMode.T1_EXT, OperationMode.T2_EXT], ids=["t1-external", "t2-external"]
)
def test_override_in_external_manual_modes(robot: RobotTaskHarness, mode: OperationMode) -> None:
    """In T1 external and T2 external ChangeSpeedOverride 10 % ends Done and the actual override is 10 %."""
    for m in (OperationMode.T1_EXT, mode):
        om = fb(robot, "MC_SetOperationModeFB")
        om.ParCmd.OperationMode = m
        assert execute(robot, om).final["Done"]
    enable(robot)
    _apply(robot, 50.0)
    _apply(robot, 10.0)
    robot.run(2)
    assert robot.user_data.ActualOverride == pytest.approx(10.0)


def test_override_zero_holds_new_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """With override 0 % a MoveDirect becomes Active but the robot does not move; 10 % lets it reach its target (Done)."""
    sdk.set_override_motion(True)
    sdk.set_move_cycles(20)
    enable(robot)
    _apply(robot, 0.0)
    mv = _direct(robot, 30.0)
    mv.Execute = True
    seen = watch(robot, [mv], 100, lambda: bool(mv.Active or mv.Error))[0]
    robot.run(50)
    assert order(seen, "Busy", "CommandBuffered", "Active"), seen.flags
    assert mv.Active and not (mv.Done or mv.Error), state(mv)
    assert sdk.joints[0] == 0.0
    _apply(robot, 10.0)
    robot.run(1000, until=lambda: finished(mv))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(30.0)


def test_override_change_during_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ChangeSpeedOverride from 20 % to 50 % during a motion ends Done, the new value is active at once and the motion finishes."""
    sdk.set_override_motion(True)
    sdk.set_move_cycles(50)
    enable(robot)
    _apply(robot, 20.0)
    mv = _direct(robot, 50.0, velocity=5.0)
    mv.Execute = True
    robot.run(200, until=lambda: sdk.joints[0] > 2.0)
    assert mv.Active, state(mv)
    at_20 = sdk.joints[0]
    robot.run(10)
    step_20 = sdk.joints[0] - at_20
    _apply(robot, 50.0)
    assert robot.user_data.ActualOverride == pytest.approx(50.0) and mv.Active, state(mv)
    at_50 = sdk.joints[0]
    robot.run(10)
    assert sdk.joints[0] - at_50 > step_20  # faster with the higher override
    robot.run(1000, until=lambda: finished(mv))
    assert mv.Done, state(mv)
