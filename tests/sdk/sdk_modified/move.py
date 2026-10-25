# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_modified.move
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Modified SDK by Thorsten, group MOVE: motion commands (15_Application_Motion.cpp).
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

"""Modified SDK by Thorsten, group MOVE: motion commands (15_Application_Motion.cpp).

Relative motions (2105, 2107, 2108, 2110), MoveLinearAbsoluteJ (2109), approach / depart / pick and
place (2200..2205): motions of the planner of the SDK; cam motions (2400..2402) and SearchHardStop
(2500, 2501): motions of the sequence (the SDK does not prebuffer the types 24xx / 25xx);
MoveSuperImposed (2502) / MoveSuperImposedDynamic (2503): asynchronous firmware functions.
MoveDirectCam (2401) has no function block in the SRCI library (only built, not tested end to end).
"""

from __future__ import annotations

from typing import Any

ADDED = (
    2105,
    2107,
    2108,
    2109,
    2110,
    2200,
    2201,
    2202,
    2203,
    2204,
    2205,
    2400,
    2401,
    2402,
    2500,
    2501,
    2502,
    2503,
)


def _no_ext(*positions: str) -> dict[str, Any]:
    """E2..E6 = 0: the simulated robot has the external axis E1 only (16#8C34 for the others)."""
    return {f"{p}.E{i}": 0.0 for p in positions for i in range(2, 7)}


# the simulation supports the blending modes 3, 4, 11 and no MoveTime (16#8E05 / 16#8E06 otherwise)
_MOTION: dict[str, Any] = {"BlendingMode": 3, "MoveTime": 0}
# CircMode 1 (Center): Angle only for CircMode 2 (16#8D64), CircPlane XZ (16#8D61)
_CIRC: dict[str, Any] = {"Angle": 0.0, "CircPlane": 0}

PARCMD: dict[str, dict[str, Any]] = {
    "MC_MoveAxesRelativeFB": {**_MOTION, **_no_ext("JointDistance")},
    "MC_MoveCircularRelativeFB": {**_MOTION, **_CIRC, **_no_ext("AuxPoint", "EndPoint")},
    "MC_MoveDirectRelativeFB": {**_MOTION, **_no_ext("Distance")},
    "MC_MoveLinearAbsoluteJFB": {**_MOTION, **_no_ext("JointPosition")},
    "MC_MoveLinearRelativeFB": {**_MOTION, **_no_ext("Distance")},
    "MC_MoveApproachDirectFB": {**_MOTION, **_no_ext("TargetPosition")},
    "MC_MoveApproachLinearFB": {**_MOTION, **_no_ext("TargetPosition")},
    "MC_MoveDepartDirectFB": {**_MOTION, **_no_ext("TargetPosition")},
    "MC_MoveDepartLinearFB": {**_MOTION, **_no_ext("TargetPosition")},
    "MC_MovePickPlaceDirectFB": {**_MOTION, **_no_ext("TargetPosition")},
    "MC_MovePickPlaceLinearFB": {**_MOTION, **_no_ext("TargetPosition")},
    # absolute circle with Tolerance: the aux point must be the center (16#8D99) -> no tolerance
    "MC_MoveCircularCamFB": {**_MOTION, **_CIRC, "Tolerance": 0.0, **_no_ext("AuxPoint", "EndPoint")},
    "MC_MoveLinearCamFB": {**_MOTION, **_no_ext("Position")},
    "MC_MoveDirectCamFB": {**_MOTION, **_no_ext("Position")},
    "MC_SearchHardStopFB": _no_ext("Position"),
    "MC_SearchHardStopJFB": _no_ext("JointPosition"),
    "MC_MoveSuperImposedFB": _no_ext("Offset"),
    "MC_MoveSuperImposedDynamicFB": _no_ext("Offset"),
}

# motions of the planner / sequence: Progress and RemainingDistance come from getMoveCmdState of the
# simulated robot (Done: 100 %, no remaining distance: -1 = not supported), not from the probe
_DONE = {"Progress": 10000, "RemainingDistance": -1.0}
RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_MoveAxesRelativeFB": {"Progress": 10000},
    **{
        name: dict(_DONE)
        for name in (
            "MC_MoveCircularRelativeFB",
            "MC_MoveDirectRelativeFB",
            "MC_MoveLinearAbsoluteJFB",
            "MC_MoveLinearRelativeFB",
            "MC_MoveApproachDirectFB",
            "MC_MoveApproachLinearFB",
            "MC_MoveDepartDirectFB",
            "MC_MoveDepartLinearFB",
            "MC_MovePickPlaceDirectFB",
            "MC_MovePickPlaceLinearFB",
            "MC_MoveCircularCamFB",
            "MC_MoveLinearCamFB",
            "MC_MoveDirectCamFB",
        )
    },
    "MC_SearchHardStopFB": {**_DONE, "InClamping": 1},
    "MC_SearchHardStopJFB": {**_DONE, "InClamping": 1},
    # superimposed motions: asynchronous firmware function, values of the probe
    "MC_MoveSuperImposedFB": {"Progress": 5000, "RemainingDistance": 12.5},
    "MC_MoveSuperImposedDynamicFB": {"Progress": 2500, "RemainingDistance": 7.5, "OffsetReached": 1},
}

_CONFIG_MODE = ("ConfigMode",)  # the SDK applies ConfigMode to the config of the position (as moveHelper)
FW_NOT_PASSED: dict[str, tuple[str, ...]] = {
    **{
        name: _CONFIG_MODE
        for name in (
            "MC_MoveCircularRelativeFB",
            "MC_MoveDirectRelativeFB",
            "MC_MoveLinearRelativeFB",
            "MC_MoveApproachDirectFB",
            "MC_MoveApproachLinearFB",
            "MC_MoveDepartDirectFB",
            "MC_MoveDepartLinearFB",
            "MC_MovePickPlaceDirectFB",
            "MC_MovePickPlaceLinearFB",
            "MC_MoveCircularCamFB",
            "MC_MoveLinearCamFB",
            "MC_MoveDirectCamFB",
            "MC_SearchHardStopFB",
        )
    },
    # table 6-492: byte 14 "X" has no meaning (the library sends 0, Offset.X .. Offset.RY follow)
    "MC_MoveSuperImposedDynamicFB": ("X",),
}

# 16#8C34: target / distance for an axis the robot does not have; 16#8E05 / 16#8E06: optional
# BlendingMode / MoveTime not supported by the RC; circular parameters; cam output index; aux segment
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_MoveAxesRelativeFB", (("JointDistance.E2", 1.0),), 0x8C34, 0),
    ("MC_MoveCircularRelativeFB", (("Angle", 5.0),), 0x8D64, 0),
    ("MC_MoveCircularRelativeFB", (("CircPlane", 1),), 0x8D61, 0),
    ("MC_MoveDirectRelativeFB", (("MoveTime", 100),), 0x8E06, 0),
    ("MC_MoveLinearAbsoluteJFB", (("JointPosition.E3", 1.0),), 0x8C34, 0),
    ("MC_MoveLinearRelativeFB", (("BlendingMode", 2),), 0x8E05, 0),
    ("MC_MoveLinearRelativeFB", (("Distance.E4", 1.0),), 0x8C34, 0),
    ("MC_MoveApproachDirectFB", (("AuxCornerDistance", -1.0),), 0x8D04, 0),
    ("MC_MoveApproachLinearFB", (("VelocityCoefficient", -1.0),), 0x8D38, 0),
    ("MC_MoveDepartDirectFB", (("TargetPosition.E2", 1.0),), 0x8C34, 0),
    ("MC_MoveDepartLinearFB", (("AuxCornerDistance", -1.0),), 0x8D04, 0),
    ("MC_MovePickPlaceDirectFB", (("AuxCornerDistance_2", -1.0),), 0x8D04, 0),
    ("MC_MovePickPlaceLinearFB", (("VelocityCoefficient", -1.0),), 0x8D38, 0),
    ("MC_MoveCircularCamFB", (("Index", 21),), 0x8D47, 0),
    ("MC_MoveCircularCamFB", (("Tolerance", 5.0),), 0x8D99, 0),
    ("MC_MoveLinearCamFB", (("Index", 30),), 0x8D47, 0),
    ("MC_MoveLinearCamFB", (("OutputBitmask", 0),), 0, 0x6D52),
    ("MC_MoveLinearCamFB", (("Index", 0),), 0, 0x6D53),
    ("MC_MoveDirectCamFB", (("Index", 30),), 0x8D47, 0),
    ("MC_SearchHardStopFB", (("Position.E2", 1.0),), 0x8C34, 0),
    ("MC_SearchHardStopJFB", (("JointPosition.E5", 1.0),), 0x8C34, 0),
    ("MC_MoveSuperImposedFB", (("Offset.E2", 1.0),), 0x8C34, 0),
]

KNOWN: dict[str, str] = {
    "MC_MoveSuperImposedDynamicFB": "spec: table 6-492 has X + Offset.X..RY (no Offset.RZ), the library sends "
    "X + Offset.X..RZ (4 bytes more); the SDK decodes the table -> ReferenceType / InterpolationMode shifted",
}
