# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_return.func
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    SDK return, group FUNC: robot functions (13_Application_RobotFunctions.cpp).
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

"""SDK return, group FUNC: robot functions (13_Application_RobotFunctions.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (7002, 7003, 7100, 7300, 7400, 7401)

# SoftSwitchTcp: function_name() gives "SoftSwitchTcp", the spec table is "SoftSwitchTCP" (no response
# values from the table) -> the response value of the test
RSP_VALUES: dict[str, dict[str, object]] = {"MC_SoftSwitchTcpFB": {"SoftMovement": 1}}

ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    # bit 7 of RobotAxesBrakeRelease is not used (no axis)
    ("MC_OpenBrakeFB", (("RobotAxesBrakeRelease.Bit07", True),), 0x8D0D, 0),
    # ReferenceNo: tool 30 / frame 30 does not exist on the RC (the client checks 0..254 only)
    ("MC_SoftSwitchTcpFB", (("ReferenceType", 0), ("ReferenceNo", 30)), 0x8D35, 0),
    ("MC_SoftSwitchTcpFB", (("ReferenceType", 1), ("ReferenceNo", 30)), 0x8D08, 0),
]
