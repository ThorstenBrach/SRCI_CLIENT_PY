# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_enable_jog
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Parameter checks of the client for EnableRobot, SetOperationMode and
#    GroupJog, run against the SDK simulator.
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

"""Parameter checks of the client (PLC side) for EnableRobot, SetOperationMode and GroupJog.

* undefined StepMode: Error, the drives are not switched on (or stay on while already enabled)
* undefined operation mode: Error, the mode stays
* GroupJog with a tool / frame number out of range or an unknown tool: Error, no motion
* GroupJog with the positive and the negative key of the same axis: Error, no motion
* library bugs (strict xfail): Active after Enable FALSE, jog keeps moving after a parameter error
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import JogMode, RobotLibraryErrorIdEnum
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, state

UNDEFINED_STEP_MODE = 55


def _jog(h: RobotTaskHarness, mode: JogMode = JogMode.JOG_FRAME, **par: Any) -> Any:
    j = fb(h, "MC_GroupJogFB")
    j.ParCmd.Mode = mode
    j.ParCmd.Override = 100
    for k, v in par.items():
        setattr(j.ParCmd, k, v)
    j.Enable = True
    h.run(50, until=lambda: bool(j.Enabled or j.Error))
    return j


# ---------------------------------------------------------------- EnableRobot


def test_undefined_step_mode_at_enable(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """EnableRobot with an undefined StepMode: Error with ERR_INVALID_PAR_CMD and the drives stay off."""
    e = fb(robot, "MC_EnableRobotFB")
    e.ParCmd.StepMode = UNDEFINED_STEP_MODE
    e.Enable = True
    robot.run(20)
    assert e.Error and e.ErrorID == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, state(e)
    assert not e.Enabled and not sdk.enabled
    e.Enable = False
    robot.run(10)
    assert not e.Error, state(e)


def test_undefined_step_mode_while_enabled(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Changing StepMode to an undefined value while enabled: Error with ERR_INVALID_PAR_CMD, the robot stays enabled."""
    e = enable(robot)
    e.ParCmd.StepMode = UNDEFINED_STEP_MODE
    robot.run(20)
    assert e.Error and e.ErrorID == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, state(e)
    assert sdk.enabled


# ---------------------------------------------------------------- SetOperationMode


@pytest.mark.parametrize("mode", [0, 7], ids=["below_range", "above_range"])
def test_undefined_operation_mode_rejected(robot: RobotTaskHarness, mode: int) -> None:
    """SetOperationMode with an undefined mode: Error with ERR_INVALID_PAR_CMD without Done, the mode stays."""
    before = int(robot.ag.Cyclic.RobToPlc.StatusRobotArm.OperationMode)
    om = fb(robot, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    s = execute(robot, om)
    assert s.final["Error"] and not s.final["Done"], s.final
    assert s.final["ErrorID"] == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD
    robot.run(5)
    assert int(robot.ag.Cyclic.RobToPlc.StatusRobotArm.OperationMode) == before


# ---------------------------------------------------------------- GroupJog


@pytest.mark.parametrize(
    ("par", "err"),
    [
        ({"ToolNo": 255}, RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE),
        ({"FrameNo": 255}, RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE),
        ({"ToolNo": 22}, RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE),
    ],
    ids=["tool_out_of_range", "frame_out_of_range", "tool_above_highest"],
)
def test_jog_invalid_tool_or_frame_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, par: dict[str, int], err: int
) -> None:
    """GroupJog with an invalid tool or frame number: Error with the matching ID, not Enabled, a key press does not move."""
    enable(robot)
    j = _jog(robot, **par)
    assert j.Error and j.ErrorID == err and not j.Enabled, state(j)
    j.ParCmd.Control.X_J1_Pos = True
    robot.run(20)
    assert sdk.joints[0] == 0.0


@pytest.mark.parametrize("mode", [JogMode.JOG_FRAME, JogMode.JOG_AXES], ids=["frame_x", "axes_j1"])
def test_jog_both_directions_of_one_axis_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: JogMode
) -> None:
    """GroupJog with the positive and the negative key of the same axis pressed together: Error and no motion.

    The client reports ERR_VELOCITY_INVALID (see report: the ID is questionable)."""
    enable(robot)
    j = _jog(robot, mode)
    assert j.Enabled, state(j)
    j.ParCmd.Control.X_J1_Pos = True
    j.ParCmd.Control.X_J1_Neg = True
    robot.run(20)
    assert j.Error and j.ErrorID != 0, state(j)
    assert sdk.joints[0] == 0.0


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F127: MC_GroupJogFB.Reset does not clear Active, it stays TRUE after Enable FALSE",
)
def test_jog_outputs_reset_after_disable(robot: RobotTaskHarness) -> None:
    """After Enable FALSE all GroupJog outputs are FALSE, Active included."""
    enable(robot)
    j = _jog(robot)
    assert j.Active and j.Enabled, state(j)
    j.Enable = False
    robot.run(20)
    assert not any(v for k, v in state(j).items() if k != "ErrorID"), state(j)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F128: invalid ToolNo while jogging sets Error at once but the RC jog keeps moving until Enable FALSE",
)
def test_jog_invalid_tool_while_jogging(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """An invalid ToolNo while a direction key is pressed: the FB reports Error and the robot no longer moves."""
    enable(robot)
    j = _jog(robot)
    j.ParCmd.Control.X_J1_Pos = True
    robot.run(20)
    j.ParCmd.ToolNo = 255
    robot.run(5)
    assert j.Error and j.ErrorID == RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE, state(j)
    before = sdk.joints[0]
    robot.run(20)
    assert sdk.joints[0] == before
