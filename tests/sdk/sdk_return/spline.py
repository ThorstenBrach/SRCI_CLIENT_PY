# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_return.spline
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    SDK return, group SPLINE: CreateSpline, DeleteSpline, DynamicSpline, MoveSpline
#    (18_Application_Spline.cpp).
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

"""SDK return, group SPLINE: CreateSpline, DeleteSpline, DynamicSpline, MoveSpline (18_Application_Spline.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (2600, 2601, 2602, 2603)

# Mode, BlendingMode, SplineID, StartPosition < 0, ToolNo / FrameNo > 254 and dynamics rates > 100 %:
# checked by the client; MoveSpline without spline data set: tests/sdk/test_sdk_return_spline.py
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_CreateSplineFB", (("SplineData[1].ToolNo", 20),), 0x8D35, 0),
    ("MC_CreateSplineFB", (("SplineData[1].FrameNo", 20),), 0x8D08, 0),
    ("MC_DynamicSplineFB", (("SplineData[1].FrameNo", 20),), 0x8D08, 0),
]

# MoveSpline needs a spline data set created with CreateSpline: tests/sdk/test_sdk_return_spline.py
KNOWN: dict[str, str] = {
    "MC_MoveSplineFB": "precondition: needs a spline created with CreateSpline (test_sdk_return_spline.py)",
}
