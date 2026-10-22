# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_return_to_primary
#  Author:      Thorsten Brach
#  Date:        2026-10-22
#
#  Description:
#    ReturnToPrimary against the SRCI SDK: progress, interruption, stop, disable.
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

"""ReturnToPrimary against the SRCI SDK (SDK-RTP).

Every test interrupts a motion of the primary sequence, jogs away in the secondary sequence and
returns with ReturnToPrimary (``away`` helper).
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import ReturnMode, TrajectoryMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import enable, execute, fb, jog, move_axes, robot, sdk_parameters, state

__all__ = ["robot", "sdk_parameters"]  # fixtures

RETURN_TO_PRIMARY = 2104


def away(h: RobotTaskHarness, sdk: SdkSimulator, jog_cycles: int = 100) -> tuple[Any, list[float]]:
    """Motion to J1 = 50 interrupted, J2 jogged away; returns the motion and the interrupt position."""
    sdk.set_move_cycles(100)
    enable(h, sdk)
    mv = move_axes(h, 50.0)
    mv.Execute = True
    h.run(100, until=lambda: sdk.joints[0] > 10.0)
    execute(h, fb(h, "MC_GroupInterruptFB"))
    at = list(sdk.joints)
    jog(h, "Y_J2_Pos", jog_cycles)
    return mv, at


def rtp(h: RobotTaskHarness, Enable: bool = False, **par: Any) -> Any:
    block = fb(h, "MC_ReturnToPrimaryFB")
    block.ParCmd.VelocityRate = block.ParCmd.AccelerationRate = 100.0
    block.ParCmd.DecelerationRate = block.ParCmd.JerkRate = -1.0
    block.ParCmd.TrajectoryMode = TrajectoryMode.LINEAR_MOVEMENT
    for name, value in par.items():
        setattr(block.ParCmd, name, value)
    block.Enable = Enable
    return block


def flags(block: Any) -> dict[str, Any]:
    return {**state(block), "Active": block.Active, "Progress": block.OutCmd.Progress}


def test_progress_and_done(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Active with rising Progress and falling RemainingDistance, then Done at the interrupt
    position; the interrupted motion finishes after GroupContinue."""
    mv, at = away(robot, sdk)
    block = rtp(robot, Enable=True)
    progress, remaining = [], []
    for _ in range(300):
        robot.run(1)
        if block.Active:
            progress.append(float(block.OutCmd.Progress))
            remaining.append(float(block.OutCmd.RemainingDistance))
        if block.Done or block.Error:
            break
    assert block.Done and block.OutCmd.Progress == 100.0, flags(block)
    assert len(progress) > 3 and progress == sorted(progress), progress
    assert remaining == sorted(remaining, reverse=True), remaining
    assert sdk.joints == pytest.approx(at)
    block.Enable = False
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(300, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done and sdk.joints[0] == 50.0, state(mv)


def test_parameters_sent(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReturnMode, TrajectoryMode, DistanceLimit, MoveTime and AllowDifferences arrive at the RC."""
    away(robot, sdk)
    block = rtp(
        robot,
        Enable=True,
        ReturnMode=ReturnMode.INTERRUPT_POSITION,
        DistanceLimit=250.0,
        MoveTime=0,
        AllowDifferences=True,
    )
    robot.run(300, until=lambda: bool(block.Done or block.Error))
    sent = sdk.last_command(RETURN_TO_PRIMARY) or {}
    assert sent, "ReturnToPrimary not decoded by the harness"
    assert sent.get("AllowDifferences") == "1", sent
    assert float(sent.get("Limit", "0")) == pytest.approx(250.0), sent
    assert sent.get("ReturnMode") == "0" and sent.get("TrajectoryMode") == "0", sent  # bit: 0 linear


def test_trajectory_mode_ptp_sent(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """TrajectoryMode PTP is sent as bit 1 = 1 (spec 6.3.11.3) and ends Done."""
    _, at = away(robot, sdk)
    block = rtp(robot, Enable=True, TrajectoryMode=TrajectoryMode.PTP_MOVEMENT)
    robot.run(300, until=lambda: bool(block.Done or block.Error))
    assert block.Done, flags(block)
    assert (sdk.last_command(RETURN_TO_PRIMARY) or {}).get("TrajectoryMode") == "1"
    assert sdk.joints == pytest.approx(at)


def test_interrupt_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt while it returns: CommandInterrupted, Active FALSE, the robot stands still;
    GroupContinue: Done at the interrupt position."""
    _, at = away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = rtp(robot, Enable=True)
    robot.run(100, until=lambda: bool(block.Active and block.OutCmd.Progress > 10.0))
    assert block.Active, flags(block)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    robot.run(3)
    assert block.CommandInterrupted and not block.Active and not block.Done, flags(block)
    held = list(sdk.joints)
    robot.run(20)
    assert sdk.joints == held
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(400, until=lambda: bool(block.Done or block.Error))
    assert block.Done and not block.CommandInterrupted, flags(block)
    assert sdk.joints == pytest.approx(at)


def test_group_stop(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop while it returns: CommandAborted, not Done."""
    away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = rtp(robot, Enable=True)
    robot.run(100, until=lambda: bool(block.Active and block.OutCmd.Progress > 10.0))
    execute(robot, fb(robot, "MC_GroupStopFB"))
    robot.run(50, until=lambda: bool(block.CommandAborted or block.Done or block.Error))
    assert block.CommandAborted and not block.Done, flags(block)


def test_disable_while_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Enable FALSE while it returns: the outputs are reset (Active, Busy FALSE), no error."""
    away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = rtp(robot, Enable=True)
    robot.run(100, until=lambda: bool(block.Active and block.OutCmd.Progress > 10.0))
    block.Enable = False
    robot.run(100, until=lambda: not block.Busy and not block.Active)
    assert not (block.Active or block.Busy or block.Done or block.Error), flags(block)


def test_parameter_change_while_active(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Inputs changed while it returns: the return ends with Done at the interrupt position."""
    _, at = away(robot, sdk)
    block = rtp(robot, Enable=True)
    robot.run(100, until=lambda: bool(block.Active))
    block.ParCmd.VelocityRate = 50.0
    robot.run(300, until=lambda: bool(block.Done or block.Error))
    assert block.Done, flags(block)
    assert sdk.joints == pytest.approx(at)


def test_trajectory_mode_invalid(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """TrajectoryMode 0 (default, invalid): Error 16#8409 from the client (ST-FIX F99)."""
    away(robot, sdk)
    block = rtp(robot, TrajectoryMode=TrajectoryMode.INVALID, Enable=True)
    robot.run(10, until=lambda: bool(block.Error))
    assert block.Error and block.ErrorID == 0x8409, flags(block)


@pytest.mark.parametrize("rate", [655.36, 1000.0])
def test_rate_out_of_range(robot: RobotTaskHarness, sdk: SdkSimulator, rate: float) -> None:
    """A rate above the range: Error from the client, nothing sent."""
    away(robot, sdk)
    block = rtp(robot, VelocityRate=rate)
    block.Enable = True
    robot.run(10, until=lambda: bool(block.Error or block.Active))
    assert block.Error and not block.Active, flags(block)
