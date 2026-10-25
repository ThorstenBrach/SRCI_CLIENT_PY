# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_modified.misc
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Modified SDK by Thorsten, group MISC: measurements, sequence and subprogram control
#    (20_Application_Misc.cpp).
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

"""Modified SDK by Thorsten, group MISC: measurements, sequence and subprogram control (20_Application_Misc.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (6000, 6001, 7000, 7004, 7006, 7007, 7008)

PARCMD: dict[str, dict[str, Any]] = {
    "MC_LoadMeasurementAutomaticFB": {"Mode": 0},
    "MC_StopSubprogramFB": {"StopMode": 0, "TargetID": 5},
}

# modes (MeasuringInput, UnitMeasurement, LoadMeasurement*) and StopMode are checked by the client;
# StopSubprogram TargetID -1 = 16#FFFF in the telegram; MeasuringInput BitNumber 0..7
_POS = tuple((f"Position_{n}.{a}", 0.0) for n in (1, 2) for a in ("J1", "J2", "J3", "J4", "J5", "J6", "E1"))
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_LoadMeasurementAutomaticFB", (("Mode", 1), ("ConfigurationAngle", -29.5)), 0x8D64, 0),
    (
        "MC_LoadMeasurementAutomaticFB",
        (("Mode", 3), *_POS, ("Position_2.J5", 180.0), ("Position_2.J1", 1.0)),
        0x8D24,
        0,
    ),
    ("MC_LoadMeasurementAutomaticFB", (("Mode", 3), *_POS, ("Position_2.J5", 90.0)), 0x8D24, 0),
    ("MC_StopSubprogramFB", (("StopMode", 2), ("TargetID", 5)), 0x8D44, 0),
    ("MC_StopSubprogramFB", (("StopMode", 0), ("TargetID", -1)), 0x8D45, 0),
    ("MC_StopSubprogramFB", (("StopMode", 1), ("TargetID", -1)), 0x8D46, 0),
    ("MC_StopSubprogramFB", (("StopMode", 0), ("TargetID", 5)), 0, 0x6C11),
    ("MC_StopSubprogramFB", (("StopMode", 1), ("TargetID", 5)), 0, 0x6C12),
    ("MC_StopSubprogramFB", (("StopMode", 2), ("TargetID", -1)), 0, 0x6C09),
    ("MC_MeasuringInputFB", (("BitNumber", 8),), 0x8D55, 0),
]
