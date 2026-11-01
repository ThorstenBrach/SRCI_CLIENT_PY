# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_move_linear
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    MoveLinearAbsolute: parameter checks of the client library.
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

"""MoveLinearAbsolute: parameter checks of the client library (spec 6.3.2, client error codes).

Invalid inputs are rejected by the function block before a command is sent: the block shows Error
with the client ErrorID, the RC never receives the command and the robot does not move.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import RobotLibraryErrorIdEnum
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import cartesian, enable, execute, fb

MOVE_LINEAR = 2103  # command type MoveLinearAbsolute
E = RobotLibraryErrorIdEnum


def _move_linear(h: RobotTaskHarness, **inputs: Any) -> Any:
    """MoveLinearAbsolute to a reachable target; ``inputs`` are block inputs (AbortingMode) or ParCmd fields."""
    mv = fb(h, "MC_MoveLinearAbsoluteFB")
    cartesian(mv, 200.0, 50.0, 0.0)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    for name, value in inputs.items():
        setattr(mv if name == "AbortingMode" else mv.ParCmd, name, value)
    return mv


def _expect_rejected_by_client(h: RobotTaskHarness, sdk: SdkSimulator, mv: Any) -> Any:
    """Execute; the block ends with Error, nothing is sent, the robot does not move. Returns the ErrorID."""
    seen = execute(h, mv)
    assert seen.final["Error"], (seen.flags, seen.final)
    assert not {"CommandBuffered", "Active", "Done"} & set(seen.flags), seen.flags
    assert sdk.last_command(MOVE_LINEAR) is None
    assert sdk.joints[:3] == [0.0, 0.0, 0.0]
    return seen.final["ErrorID"]


RATE_ERRORS = {
    "VelocityRate": E.ERR_VELOCITY_INVALID,
    "AccelerationRate": E.ERR_ACCELERATION_INVALID,
    "DecelerationRate": E.ERR_DECELERATION_INVALID,
    "JerkRate": E.ERR_JERK_INVALID,
}


@pytest.mark.parametrize(
    "value", [655.36, 200.0, 100.01], ids=["beyond-telegram-range", "double", "just-above"]
)
@pytest.mark.parametrize("rate", list(RATE_ERRORS))
def test_dynamics_rate_above_100_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, value: float
) -> None:
    """A dynamics rate above 100 % is rejected by the block with the rate specific ErrorID (16#8401..16#8404); nothing is sent."""
    enable(robot)
    mv = _move_linear(robot, **{rate: value})
    assert _expect_rejected_by_client(robot, sdk, mv) == RATE_ERRORS[rate]


@pytest.mark.parametrize(
    ("name", "value", "error"),
    [
        ("AbortingMode", 12, E.ERR_ABORTINGMODE_INVALID),
        ("BlendingMode", 99, E.ERR_INVALID_PAR_CMD),
        ("BlendingMode", 1, E.ERR_INVALID_PAR_CMD),
        ("OriMode", 22, E.ERR_INVALID_PAR_CMD),
        ("TurnMode", 55, E.ERR_INVALID_PAR_CMD),
        ("ToolNo", 255, E.ERR_TOOLNO_RANGE),
        ("FrameNo", 255, E.ERR_FRAMENO_RANGE),
    ],
    ids=[
        "aborting-mode-12",
        "blending-mode-99",
        "blending-mode-1",
        "ori-mode-22",
        "turn-mode-55",
        "tool-255",
        "frame-255",
    ],
)
def test_undefined_parameter_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, value: int, error: E
) -> None:
    """An undefined AbortingMode, BlendingMode, OriMode or TurnMode or a tool / frame number outside 0..254 is
    rejected by the block with its ErrorID; nothing is sent.
    """
    enable(robot)
    mv = _move_linear(robot, **{name: value})
    assert _expect_rejected_by_client(robot, sdk, mv) == error


CONFIG_AXES = ["Shoulder", "Elbow", "Wrist"]
CONFIG_ERRORS = {
    "Shoulder": E.ERR_CONFIGMODE_SHOULDER_INVALID,
    "Elbow": E.ERR_CONFIGMODE_ELBOW_INVALID,
    "Wrist": E.ERR_CONFIGMODE_WRIST_INVALID,
}


def _config_mode(h: RobotTaskHarness, axes: list[str], value: int) -> Any:
    mv = _move_linear(h)
    for axis in axes:
        setattr(mv.ParCmd.ConfigMode, axis, value)
    return mv


@pytest.mark.parametrize("value", [12, 14])
@pytest.mark.parametrize(
    "axes", [["Shoulder"], ["Elbow"], ["Wrist"], CONFIG_AXES], ids=["shoulder", "elbow", "wrist", "all"]
)
def test_undefined_config_mode_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, axes: list[str], value: int
) -> None:
    """An undefined ConfigMode for shoulder, elbow, wrist or all three axes is rejected by the block; nothing is sent."""
    enable(robot)
    assert _expect_rejected_by_client(robot, sdk, _config_mode(robot, axes, value)) != 0


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F111: CheckParameterValid of MC_MoveLinearAbsoluteFB reports an undefined ParCmd.ConfigMode "
    "with ERR_INVALID_PAR_CMD (16#0008); the client codes 16#8405 / 16#8406 / 16#8407 (ConfigMode "
    "elbow / shoulder / wrist) are used for ParCmd.Position.Config instead (spec client error table, 6.3.2).",
)
@pytest.mark.parametrize("axis", CONFIG_AXES)
def test_undefined_config_mode_error_id(robot: RobotTaskHarness, sdk: SdkSimulator, axis: str) -> None:
    """An undefined ConfigMode of one axis is rejected with the axis specific ErrorID ERR_CONFIGMODE_<axis>_INVALID."""
    enable(robot)
    assert _expect_rejected_by_client(robot, sdk, _config_mode(robot, [axis], 14)) == CONFIG_ERRORS[axis]
