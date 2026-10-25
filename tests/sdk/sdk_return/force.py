# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_return.force
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    SDK return, group FORCE: ForceControl, ForceLimit (19_Application_Force.cpp).
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

"""SDK return, group FORCE: ForceControl, ForceLimit (19_Application_Force.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (7301, 7302)

# valid numbers (the distinct values of the test exceed the 20 tools / frames / loads of the SDK)
_SENSOR = {"ToolNo": 1, "FrameNo": 2, "CalibrationData": 3}
PARCMD: dict[str, dict[str, Any]] = {
    "MC_ForceControlFB": {**_SENSOR, "MaxVelocity": 50, "ErrorToolNo": 4, "ErrorFrameNo": 5},
    "MC_ForceLimitFB": _SENSOR,
}

# load 20 / ErrorToolNo 20 / ErrorFrameNo 20 pass the client (ToolNo / FrameNo 20: checked by the
# client), the SDK has 0..19; MaxVelocity in 0.01 % (> 100 %)
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_ForceControlFB", (("CalibrationData", 20),), 0x8D17, 0),
    ("MC_ForceControlFB", (("MaxVelocity", 10001),), 0x8D38, 0),
    ("MC_ForceControlFB", (("ErrorReaction", 0), ("ErrorToolNo", 20)), 0x8D35, 0),
    ("MC_ForceControlFB", (("ErrorReaction", 0), ("ErrorReferenceType", 1), ("ErrorFrameNo", 20)), 0x8D08, 0),
    ("MC_ForceLimitFB", (("CalibrationData", 20),), 0x8D17, 0),
]
