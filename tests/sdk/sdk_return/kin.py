# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_return.kin
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    SDK return, group KIN: kinematic calculations (12_Application_Kinematics.cpp).
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

"""SDK return, group KIN: kinematic calculations (12_Application_Kinematics.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (7203, 7204, 7205)

# ShiftPosition: RotationAngle (distinct value) is only allowed in mode 3 "Rotate around Straight
# Line", which needs an axis as TransformationParameter_2 (3: Z axis); ReferenceFrame: a frame of the
# simulated RC (0..19)
PARCMD: dict[str, dict[str, Any]] = {
    "MC_ShiftPositionFB": {
        "Mode": 3,
        "TransformationParameter_2": 3,
        "TransformationParameter_1.ReferenceFrame": 2,
    },
}
# ArmConfig of the response: the response tables give no value (bit names repeat); ShiftPosition:
# table 6-691 has "Shoulder" as a BYTE of its own (byte 28) and Elbow/Wrist in byte 29
_CONFIG = {"Shoulder": 1, "Elbow": 0, "Wrist": 1}
RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_CalculateForwardKinematicFB": dict(_CONFIG),
    "MC_ShiftPositionFB": dict(_CONFIG),
}

# client checks (not sent): ShiftPosition Mode 5, TransformationParameter_2 7 (16#0008), FrameNo of
# a frame not available on the RC (16#8415), ToolNo / FrameNo of CalculateForward/InverseKinematic
# (16#8413 / 16#8415) - the SDK checks of these values are not reachable with the client.
# ReferenceFrame / TargetFrameNo 20: not checked by the client, the simulated RC has the frames 0..19.
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_ShiftPositionFB", (("Mode", 0), ("TransformationParameter_2", 0)), 0x8D67, 0),
    ("MC_ShiftPositionFB", (("TransformationParameter_2", 4),), 0x8D68, 0),
    ("MC_ShiftPositionFB", (("TransformationParameter_1.ReferenceFrame", 20),), 0x8D88, 0),
    ("MC_ShiftPositionFB", (("TargetFrameNo", 20),), 0x8D08, 0),
]
