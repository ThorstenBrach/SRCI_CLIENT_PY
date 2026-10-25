# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_modified.conv
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Modified SDK by Thorsten, group CONV: conveyor tracking (17_Application_Conveyor.cpp).
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

"""Modified SDK by Thorsten, group CONV: conveyor tracking (17_Application_Conveyor.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (2300, 2301, 2302, 2303)

# valid commands: conveyor 0..7 (MAX_CONVEYOR_NO), zones of the conveyor inside EndDistance
PARCMD: dict[str, dict[str, Any]] = {
    "MC_ActivateConveyorTrackingFB": {"ConveyorNo": 1},
    "MC_ConfigureConveyorFB": {
        "ConveyorNo": 2,
        "ConveyorOrigin.ReferenceFrame": 3,
        "Radius": 500.0,
        "StartDistance": 100.0,
        "SyncInLength": 200.0,
        "SyncOutLength": 300.0,
        "EndDistance": 1500.0,
    },
    "MC_RedefineTrackingPosFB": {
        "ConveyorNo": 3,
        "FrameNo": 4,
        "StartIndexInitPosition": 2,
        "IndexTrackingOffset": 5,
    },
    "MC_SyncToConveyorFB": {"ConveyorNo": 4, "FrameNo": 5, "SyncInParameter": 250.0},
}

# TrackingStatusByte bit 0 (ConveyorTrackingEnabled) = Enabled of the block
RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_ActivateConveyorTrackingFB": {"TrackingStatusByte": 0x0B},
    "MC_SyncToConveyorFB": {"InSync": 1},
}

# ConveyorNo > 255, FrameNo > highest frame index, SyncInMode / ConveyorType / ConnectionMode out of
# range: checked by the client (not sent)
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_ActivateConveyorTrackingFB", (("ConveyorNo", 8),), 0x8D47, 0),
    ("MC_ConfigureConveyorFB", (("ConveyorNo", 20),), 0x8D47, 0),
    ("MC_ConfigureConveyorFB", (("ConveyorOrigin.ReferenceFrame", 25),), 0x8D88, 0),
    ("MC_ConfigureConveyorFB", (("StartDistance", -1.0),), 0x8D24, 0),
    ("MC_ConfigureConveyorFB", (("EndDistance", 400.0),), 0x8D24, 0),
    ("MC_RedefineTrackingPosFB", (("FrameNo", 0),), 0x8D08, 0),
    ("MC_RedefineTrackingPosFB", (("StartIndexInitPosition", 0),), 0x8D47, 0),
    ("MC_SyncToConveyorFB", (("FrameNo", 0),), 0x8D08, 0),
    ("MC_SyncToConveyorFB", (("ConveyorNo", 9),), 0x8D47, 0),
    ("MC_SyncToConveyorFB", (("MaxVelocity", -1.0),), 0x8D29, 0),
    ("MC_SyncToConveyorFB", (("MaxAcceleration", -2.0),), 0x8D26, 0),
]
