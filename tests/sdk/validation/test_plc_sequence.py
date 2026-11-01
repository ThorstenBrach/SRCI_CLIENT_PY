# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_sequence
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the client side of SetSequence, ChangeSpeedOverride and
#    ReturnToPrimary.
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

"""Validation of the client side of SetSequence, ChangeSpeedOverride and ReturnToPrimary.

* a block on an axes group that no RobotTask serves ends with an error
* parameter checks of the blocks (target sequence, override range, dynamics rates of
  ReturnToPrimary): Error, nothing is sent to the RC
* default value of the override
* Enable FALSE of an active ReturnToPrimary
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import AxesGroup, CmdType, JogMode, RobotLibraryErrorIdEnum, TrajectoryMode
from srci.types.iec import new_instance
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, move_axes, state

E = RobotLibraryErrorIdEnum


@pytest.mark.parametrize("name", ["MC_SetSequenceFB", "MC_ChangeSpeedOverrideFB", "MC_ReturnToPrimaryFB"])
def test_unlinked_axes_group_rejected(name: str) -> None:
    """The block on an axes group that is not served by a RobotTask ends with ERR_COMMANDS_NOT_ENABLED and is not left Busy."""
    group = AxesGroup()
    block = new_instance(name)
    setattr(block, "Enable" if name == "MC_ReturnToPrimaryFB" else "Execute", True)
    for _ in range(5):
        block(AxesGroup=group)
    assert block.Error and block.ErrorID == E.ERR_COMMANDS_NOT_ENABLED, state(block)
    assert not block.Busy and not block.Done


# ---------------------------------------------------------------- SetSequence


@pytest.mark.parametrize("target", [0, 3, 5, 255])
def test_set_sequence_undefined_target_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, target: int
) -> None:
    """SetSequence with a target sequence other than 1 or 2 ends with ERR_INVALID_PAR_CMD and nothing is sent; the sequence is unchanged."""
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    seen = execute(robot, seq)
    assert seen.flags == ["Error"] or seen.flags[-1] == "Error", seen.flags
    assert seen.final["ErrorID"] == E.ERR_INVALID_PAR_CMD, seen.final
    assert sdk.last_command(int(CmdType.SetSequence)) is None
    assert not robot.user_data.SecondarySequenceActive and robot.user_data.Idle


# ---------------------------------------------------------------- ChangeSpeedOverride


@pytest.mark.parametrize("value", [-50.0, -0.01, 100.01, 150.0, float("nan")])
def test_override_out_of_range_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, value: float) -> None:
    """ChangeSpeedOverride outside 0..100 % ends with ERR_OVERRIDE_INVALID, nothing is sent and the actual override stays 50 %."""
    enable(robot)
    ok = fb(robot, "MC_ChangeSpeedOverrideFB")
    ok.ParCmd.Override = 50.0
    assert execute(robot, ok).final["Done"]
    sent_before = sdk.last_command(int(CmdType.ChangeSpeedOverride))
    ov = fb(robot, "MC_ChangeSpeedOverrideFB")
    ov.ParCmd.Override = value
    seen = execute(robot, ov)
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_OVERRIDE_INVALID, seen.final
    assert "Done" not in seen.flags
    assert sdk.last_command(int(CmdType.ChangeSpeedOverride)) == sent_before
    robot.run(5)
    assert robot.user_data.ActualOverride == pytest.approx(50.0)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "LIB-BUG F117: ChangeSpeedOverrideParCmd.Override defaults to 5.0 although its field documentation "
        "(parameter table of spec 6.2.3) names 10 % as the default (src/srci/types/_generated/structs.py, ST DUT ChangeSpeedOverrideParCmd)"
    ),
)
def test_override_default_value(robot: RobotTaskHarness) -> None:
    """ChangeSpeedOverride executed with the default parameters sets the actual override to 10 %."""
    enable(robot)
    seen = execute(robot, fb(robot, "MC_ChangeSpeedOverrideFB"))
    assert seen.final["Done"], seen.final
    robot.run(2)
    assert robot.user_data.ActualOverride == pytest.approx(10.0)


# ---------------------------------------------------------------- ReturnToPrimary


def _interrupted_and_away(h: RobotTaskHarness, sdk: SdkSimulator, jog_cycles: int = 100) -> list[float]:
    """Joint motion interrupted at J1 > 10, J2 jogged away; returns the interrupt position."""
    sdk.set_move_cycles(100)
    enable(h)
    mv = move_axes(h, 50.0)
    mv.Execute = True
    h.run(100, until=lambda: sdk.joints[0] > 10.0)
    execute(h, fb(h, "MC_GroupInterruptFB"))
    at = list(sdk.joints)
    j = fb(h, "MC_GroupJogFB", Enable=True)
    j.ParCmd.Mode = JogMode.JOG_AXES
    j.ParCmd.Override = 100
    h.run(50, until=lambda: bool(j.Enabled or j.Error))
    j.ParCmd.Control.Y_J2_Pos = True
    h.run(jog_cycles)
    j.ParCmd.Control.Y_J2_Pos = False
    h.run(5)
    j.Enable = False
    h.run(50, until=lambda: not j.Busy)
    return at


def _rtp(h: RobotTaskHarness, **par: Any) -> Any:
    block = fb(h, "MC_ReturnToPrimaryFB")
    block.ParCmd.TrajectoryMode = TrajectoryMode.LINEAR_MOVEMENT
    for name, value in par.items():
        setattr(block.ParCmd, name, value)
    return block


RATE_ERRORS = {
    "VelocityRate": E.ERR_VELOCITY_INVALID,
    "AccelerationRate": E.ERR_ACCELERATION_INVALID,
    "DecelerationRate": E.ERR_DECELERATION_INVALID,
    "JerkRate": E.ERR_JERK_INVALID,
}


@pytest.mark.parametrize("value", [100.01, 200.0, 655.36])
@pytest.mark.parametrize("rate", list(RATE_ERRORS))
def test_return_rate_above_range_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, value: float
) -> None:
    """A ReturnToPrimary dynamics rate above 100 % is rejected by the block with the rate's error ID.

    Nothing is sent and the robot stays where it is."""
    _interrupted_and_away(robot, sdk)
    away_at = list(sdk.joints)
    block = _rtp(robot, **{rate: value})
    block.Enable = True
    robot.run(10, until=lambda: bool(block.Error or block.Active))
    assert block.Error and block.ErrorID == RATE_ERRORS[rate] and not block.Busy, state(block)
    assert sdk.last_command(int(CmdType.ReturnToPrimary)) is None
    robot.run(20)
    assert sdk.joints == away_at


@pytest.mark.xfail(
    strict=True,
    reason=(
        "LIB-BUG F118: MC_ReturnToPrimaryFB.OnExecRun resets the block on the falling edge of Enable "
        "(src/srci/fb/BasicMove/MC_ReturnToPrimary/MC_ReturnToPrimaryFB.py, 'if self._enable_R.Q or "
        "self._enable_F.Q: self.Reset()') without sending the Enable bit FALSE to the RC (spec 6.3.11, "
        "payload bit Enable); the robot keeps returning and CommandAborted is never shown"
    ),
)
def test_return_disabled_while_active_stops(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Enable FALSE during an active ReturnToPrimary stops the robot and shows CommandAborted for one cycle.

    Afterwards all outputs are FALSE."""
    _interrupted_and_away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = _rtp(robot)
    block.Enable = True
    robot.run(100, until=lambda: bool(block.Active and block.OutCmd.Progress > 10.0))
    assert block.Active, state(block)
    block.Enable = False
    aborted = []
    for _ in range(20):
        robot.run(1)
        aborted.append(bool(block.CommandAborted))
    assert not (block.Busy or block.Active or block.Done or block.Error), state(block)
    held = list(sdk.joints)
    robot.run(30)
    assert sdk.joints == held, "the robot keeps returning after Enable FALSE"
    assert aborted.count(True) == 1, aborted
