# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_modified.wa
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Modified SDK by Thorsten, group WA: work areas (14_Application_WorkAreas.cpp).
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

"""Modified SDK by Thorsten, group WA: work areas (14_Application_WorkAreas.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (7500, 7501, 7502, 7503)

# ReadWorkArea: the SDK returns the requested WorkAreaNo (not a value of the firmware)
PARCMD: dict[str, dict[str, Any]] = {"MC_ReadWorkAreaFB": {"WorkAreaNo": 3}}
RSP_VALUES: dict[str, dict[str, object]] = {"MC_ReadWorkAreaFB": {"WorkAreaNo": 3}}

FW_NOT_PASSED: dict[str, tuple[str, ...]] = {
    # Enable is evaluated by the SDK (getWorkAreaState is called while enabled)
    "MC_MonitorWorkAreaFB": ("Enable",),
    # DataChanged of the WriteWorkArea telegram (table 6-229) has no meaning for the RC
    "MC_WriteWorkAreaFB": ("DataChanged",),
}

# WorkAreaNo > HighestWorkAreaIndex: checked by the client (not sent)
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    # reference frame 30 of a Box does not exist on the RC (the client checks 0..254 only)
    ("MC_WriteWorkAreaFB", (("WorkAreaData.AreaType", 1), ("WorkAreaData.FrameNo", 30)), 0x8D08, 0),
]
