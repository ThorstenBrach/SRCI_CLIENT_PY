# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_safety
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Parameter checks of the client for SafeReferencing and
#    ReadSafeReferencePosition, command names in the message log.
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

"""Parameter checks of the client (PLC side) for SafeReferencing and ReadSafeReferencePosition.

* dynamic rates above 100 % are rejected with the matching error ID, nothing is sent to the RC
* a tool number above the highest configured tool is rejected
* reference position index 0 is rejected
* the user defined command name appears in the message of an RC error
"""

from __future__ import annotations

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import CmdType, RobotLibraryErrorIdEnum
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb


@pytest.mark.parametrize(
    ("rate", "err"),
    [
        ("VelocityRate", RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID),
        ("AccelerationRate", RobotLibraryErrorIdEnum.ERR_ACCELERATION_INVALID),
        ("DecelerationRate", RobotLibraryErrorIdEnum.ERR_DECELERATION_INVALID),
        ("JerkRate", RobotLibraryErrorIdEnum.ERR_JERK_INVALID),
    ],
    ids=["velocity", "acceleration", "deceleration", "jerk"],
)
def test_safe_referencing_rate_above_100_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, err: int
) -> None:
    """SafeReferencing with a dynamic rate of 101 %: Error with the matching ID without Busy, no command reaches the RC."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    setattr(s.ParCmd, rate, 101.0)
    seen = execute(robot, s)
    assert seen.final["Error"] and seen.final["ErrorID"] == err and "Done" not in seen.flags, seen.final
    assert sdk.last_command(int(CmdType.SafeReferencing)) is None


def test_safe_referencing_unknown_tool_rejected(robot: RobotTaskHarness) -> None:
    """SafeReferencing with a tool number above the highest configured tool: Error ERR_TOOLNO_UNAVAILABLE."""
    enable(robot)
    s = fb(robot, "MC_SafeReferencingFB")
    s.ParCmd.ToolNo = 22
    seen = execute(robot, s)
    assert seen.final["Error"] and seen.final["ErrorID"] == RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE, (
        seen.final
    )


def test_read_reference_position_index_zero_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReadSafeReferencePosition with index 0: Error ERR_INVALID_PAR_CMD, no command reaches the RC."""
    r = fb(robot, "MC_ReadSafeReferencePositionFB")
    r.ParCmd.Index = 0
    seen = execute(robot, r)
    assert seen.final["Error"] and seen.final["ErrorID"] == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, (
        seen.final
    )
    assert sdk.last_command(int(CmdType.ReadSafeReferencePosition)) is None


@pytest.mark.parametrize(
    ("name", "cmd", "needs_enable"),
    [
        ("MC_SafeReferencingFB", CmdType.SafeReferencing, True),
        ("MC_ReadSafeReferencePositionFB", CmdType.ReadSafeReferencePosition, False),
    ],
    ids=["safe_ref", "read_ref_position"],
)
def test_command_name_in_error_message(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, cmd: CmdType, needs_enable: bool
) -> None:
    """The user defined command name is part of the message written for an RC error of the command."""
    if needs_enable:
        enable(robot)
    sdk.set_command_error(int(cmd), 0x8C68)
    b = fb(robot, name, Name="RefCheck")
    assert execute(robot, b, reset=False).final["Error"]
    robot.run(3)
    texts = [m.MessageText for m in robot.ag.MessageLog.Messages if m.MessageText]
    assert any("[RefCheck]" in t for t in texts), texts
