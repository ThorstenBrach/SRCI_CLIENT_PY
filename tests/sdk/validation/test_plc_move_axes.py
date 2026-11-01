# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_move_axes
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of MoveAxesAbsolute: behaviour of the client library.
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

"""Validation tests of MoveAxesAbsolute: behaviour of the client library.

Parameter checks of the function block (rates, enum inputs, tool number, sequence flag), the
reaction to a new rising edge of Execute while the command is still running, and the parameter
check of SetSequence used together with the motion. A command rejected by the client is never
sent to the RC and the robot does not move.
"""

from __future__ import annotations

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import RobotLibraryErrorIdEnum
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    MOVE_CYCLES,
    enable,
    execute,
    fb,
    finished,
    move_axes,
    state,
    watch,
)

MOVE_AXES_ABSOLUTE = 2101
E = RobotLibraryErrorIdEnum


def _sent(sdk: SdkSimulator, since: int = 0) -> int:
    """MoveAxesAbsolute commands the SDK accepted (buffered) since log entry ``since``."""
    return sum(
        1
        for log in sdk.logs[since:]
        if f"({MOVE_AXES_ABSOLUTE}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _rejected(robot: RobotTaskHarness, sdk: SdkSimulator, mv: object, error_id: int) -> None:
    """Execute ``mv`` and check: Error with ``error_id``, nothing sent, no motion."""
    since = len(sdk.logs)
    seen = execute(robot, mv)
    assert seen.final["Error"] and seen.final["ErrorID"] == error_id, seen.final
    assert not any(f in seen.flags for f in ("CommandBuffered", "Active", "Done")), seen.flags
    assert _sent(sdk, since) == 0
    assert sdk.joints[:7] == [0.0] * 7


@pytest.mark.parametrize(
    ("name", "value", "error_id"),
    [
        ("VelocityRate", 200.0, E.ERR_VELOCITY_INVALID),
        ("VelocityRate", 655.36, E.ERR_VELOCITY_INVALID),
        ("AccelerationRate", 200.0, E.ERR_ACCELERATION_INVALID),
        ("AccelerationRate", 655.36, E.ERR_ACCELERATION_INVALID),
        ("DecelerationRate", 200.0, E.ERR_DECELERATION_INVALID),
        ("DecelerationRate", 655.36, E.ERR_DECELERATION_INVALID),
        ("JerkRate", 200.0, E.ERR_JERK_INVALID),
        ("JerkRate", 655.36, E.ERR_JERK_INVALID),
    ],
    ids=lambda v: v.name.lower() if isinstance(v, E) else str(v),
)
def test_rate_above_100_percent_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, value: float, error_id: int
) -> None:
    """A dynamic rate above 100 % is rejected by the block with the error of that rate; nothing is sent and the robot does not move.

    100 % is the maximal reference value (spec 5.5.7); the block checks the range before sending.
    """
    enable(robot)
    mv = move_axes(robot, 30.0)
    setattr(mv.ParCmd, name, value)
    _rejected(robot, sdk, mv, error_id)


@pytest.mark.parametrize("mode", [1, 22, 99], ids=lambda v: f"mode_{v}")
def test_undefined_blending_mode_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, mode: int) -> None:
    """An undefined BlendingMode is rejected by the block with ERR_INVALID_PAR_CMD; nothing is sent and the robot does not move."""
    enable(robot)
    mv = move_axes(robot, 30.0)
    mv.ParCmd.BlendingMode = mode
    mv.ParCmd.BlendingParameter = [10.0, 30.0]
    _rejected(robot, sdk, mv, E.ERR_INVALID_PAR_CMD)


@pytest.mark.parametrize("mode", [12, 18], ids=lambda v: f"mode_{v}")
def test_undefined_aborting_mode_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, mode: int) -> None:
    """An undefined AbortingMode is rejected by the block with ERR_ABORTINGMODE_INVALID; nothing is sent and the robot does not move."""
    enable(robot)
    mv = move_axes(robot, 30.0)
    mv.AbortingMode = mode
    _rejected(robot, sdk, mv, E.ERR_ABORTINGMODE_INVALID)


@pytest.mark.parametrize("flag", [0, 3], ids=lambda v: f"flag_{v}")
def test_undefined_sequence_flag_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, flag: int) -> None:
    """A SequenceFlag other than primary or secondary is rejected by the block with ERR_SEQFLAG_NOT_ALLOWED; nothing is sent."""
    enable(robot)
    mv = move_axes(robot, 30.0)
    mv.SequenceFlag = flag
    _rejected(robot, sdk, mv, E.ERR_SEQFLAG_NOT_ALLOWED)


def test_unavailable_tool_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A ToolNo above the highest tool index of the RC is rejected by the block with ERR_TOOLNO_UNAVAILABLE; nothing is sent."""
    enable(robot)
    assert robot.ag.State.ConfigurationData.HighestToolIndex < 22
    mv = move_axes(robot, 30.0)
    mv.ParCmd.ToolNo = 22
    _rejected(robot, sdk, mv, E.ERR_TOOLNO_UNAVAILABLE)


def test_set_sequence_undefined_target_rejected(robot: RobotTaskHarness) -> None:
    """SetSequence with the undefined target sequence 3 ends with Error; the primary sequence stays active."""
    enable(robot)
    ss = fb(robot, "MC_SetSequenceFB")
    ss.ParCmd.TargetSequence = 3
    seen = execute(robot, ss)
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_INVALID_PAR_CMD, seen.final
    assert "Done" not in seen.flags
    assert not robot.ag.State.StatusRobotArm.SecondarySequenceActive


def test_execute_reset_while_active_keeps_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A falling edge of Execute while the motion is active does not cancel it: the block stays Busy and
    Active and the robot reaches the target.
    """
    enable(robot)
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    mv = move_axes(robot, 60.0)
    mv.Execute = True
    robot.run(4 * MOVE_CYCLES, until=lambda: bool(mv.Active))
    mv.Execute = False
    robot.run(3)
    assert mv.Busy and mv.CommandBuffered and mv.Active, state(mv)
    seen = watch(robot, [mv], 4 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert "Done" in seen.flags and not mv.Error, seen.flags
    assert sdk.joints[0] == pytest.approx(60.0)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F113: a new rising edge of Execute while MoveAxesAbsolute is still Busy is ignored (no new "
    "command, new target not used); PLCopen part 1 / spec 5.5.10 Execute behaviour: a new Execute on a "
    "running instance starts the command again with the current inputs (RobotLibraryBaseExecuteFB F50 hold, "
    "F104 restart only for ProcessingMode blocks)",
)
@pytest.mark.parametrize("second_target", [80.0, 40.0], ids=["same_target", "new_target"])
def test_new_rising_edge_while_active_restarts(
    robot: RobotTaskHarness, sdk: SdkSimulator, second_target: float
) -> None:
    """A new rising edge of Execute while the motion is active sends the command again with the current
    target; the robot ends there with Done.

    The block stays Busy, CommandBuffered falls and rises again with the new command.
    """
    enable(robot)
    sdk.set_move_cycles(4 * MOVE_CYCLES)
    mv = move_axes(robot, 80.0)
    since = len(sdk.logs)
    mv.Execute = True
    robot.run(8 * MOVE_CYCLES, until=lambda: bool(mv.Active) and sdk.joints[0] > 10.0)
    mv.Execute = False
    robot.run(2)
    mv.ParCmd.JointPosition.J1 = second_target
    mv.Execute = True
    history: list[tuple[bool, bool]] = []
    watch(
        robot, [mv], 16 * MOVE_CYCLES, lambda: history.append((mv.Busy, mv.CommandBuffered)) or finished(mv)
    )
    assert mv.Done and not mv.Error, state(mv)
    assert _sent(sdk, since) == 2
    assert all(busy for busy, _ in history[:-1])
    assert (True, False) in history
    assert sdk.joints[0] == pytest.approx(second_target)
