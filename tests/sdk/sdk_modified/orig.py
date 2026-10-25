# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_modified.orig
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Modified SDK by Thorsten, group ORIG: commands of the original SDK answered by the SDK itself
#    (01_Application.cpp).
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

"""Modified SDK by Thorsten, group ORIG: commands of the original SDK answered by the SDK itself (01_Application.cpp).

The original SDK implements these commands, the simulated robot of the harness implements their
firmware functions (srci_py_harness/sim_robot_orig.cpp). ReadSafeReferencePosition (7009) and
SafeReferencing (7010) have no function block in the SRCI library (not tested end to end).
CallSubprogram (7001) stays with the harness (C-007): the SDK reports no Progress / InProgress while
the subprogram runs (tests/sdk/test_subprogram.py).
"""

from __future__ import annotations

from typing import Any

ADDED = (2106, 2111, 2112, 5109, 6100, 6101, 6104, 7009, 7010, 7101, 7200, 7201, 7202)


def _no_ext(*positions: str) -> dict[str, Any]:
    """E2..E6 = 0: the simulated robot has the external axis E1 only (16#8C34 for the others)."""
    return {f"{p}.E{i}": 0.0 for p in positions for i in range(2, 7)}


# the simulation supports the blending modes 3, 4, 11 and no MoveTime (16#8E05 / 16#8E06 otherwise)
_MOTION: dict[str, Any] = {"BlendingMode": 3, "MoveTime": 0}
_INDEX = {f"Index[{i}]": i + 1 for i in range(5)}

PARCMD: dict[str, dict[str, Any]] = {
    # CircMode 1 (Center): Angle only for CircMode 2 (16#8D64), CircPlane XZ (16#8D61), no tolerance
    "MC_MoveCircularAbsoluteFB": {
        **_MOTION,
        "Angle": 0.0,
        "CircPlane": 0,
        "Tolerance": 0.0,
        **_no_ext("AuxPoint", "EndPoint"),
    },
    "MC_MoveDirectOffsetFB": {**_MOTION, **_no_ext("ReferencePosition", "Offset")},
    "MC_MoveLinearOffsetFB": {**_MOTION, **_no_ext("ReferencePosition", "Offset")},
    "MC_ReadDigitalInputsFB": dict(_INDEX),
    "MC_ReadDigitalOutputsFB": dict(_INDEX),
    "MC_WriteDigitalOutputsFB": dict(_INDEX),
    "MC_CalculateCartesianPositionFB": {"FrameNo": 2, "TargetFrameNo": 3},
    # one position (Mode 2 "1-Point" / 5 "ABC World"): the SDK answers the telegrams before the last one
    # ACTIVE and the library waits for DONE (see KNOWN of test_methodology)
    "MC_CalculateFrameFB": {"Mode": 2, "FrameNo": 2, "ReferenceFrame": 3},
    "MC_CalculateToolFB": {"Mode": 5, "FrameNo": 2, "ToolNo": 3},
}

# motions: Progress and RemainingDistance come from getMoveCmdState of the simulated robot (Done:
# 100 %, no remaining distance: -1 = not supported), not from the probe
_DONE = {"Progress": 10000, "RemainingDistance": -1.0}
RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_MoveCircularAbsoluteFB": dict(_DONE),
    "MC_MoveDirectOffsetFB": dict(_DONE),
    "MC_MoveLinearOffsetFB": dict(_DONE),
    "MC_CalculateCartesianPositionFB": {"TargetFrameNoReturn": 3, "TargetToolNoReturn": 0},
}

# ConfigMode: applied by the SDK to the configuration of the position (moveHelper); Manipulation: not
# in the firmware interface of the original SDK (initiateMoveCircular / initiateMove*Offset);
# Offset: api::MoveOffsetParameters has only the pose (X..RZ) - TurnNumber, E1..E6 are dropped;
# DataIndex / DataComplete: the SDK collects the positions and calls calcFrame / calcTool once
_OFFSET = ("ConfigMode", "Manipulation", "Offset.TurnNumber", "Offset.E")
FW_NOT_PASSED: dict[str, tuple[str, ...]] = {
    "MC_MoveCircularAbsoluteFB": ("ConfigMode", "Manipulation"),
    "MC_MoveDirectOffsetFB": _OFFSET,
    "MC_MoveLinearOffsetFB": _OFFSET,
    "MC_CalculateFrameFB": ("DataIndex", "DataComplete"),
    "MC_CalculateToolFB": ("DataIndex", "DataComplete"),
}

_ZERO5 = tuple((f"Index[{i}]", 0) for i in range(5))
_NO_MASK = tuple((f"OutputBitmask[{i}]", 0) for i in range(5))
# standard system variables (RCParameter FALSE, spec appendix 7.7), all eight entries unused
_SYSVAR = (
    ("RCParameter", False),
    *((f"ParameterID[{i}]", 0) for i in range(8)),
    *((f"SubParameterID[{i}]", 0) for i in range(8)),
)
_ROBOT_AXES = tuple((f"RobotAxesActive.AxisJ{i}", False) for i in range(1, 7))
# FrameNo / ToolNo of CalculateCartesianPosition / CalculateTool (16#8415 / 16#8413): client checks
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_ReadDigitalInputsFB", (("Index[4]", 21),), 0x8D47, 0),
    ("MC_ReadDigitalInputsFB", (("Index[1]", 1),), 0x8D48, 0),
    ("MC_ReadDigitalInputsFB", _ZERO5, 0x8D50, 0),
    ("MC_ReadDigitalOutputsFB", (("Index[0]", 30),), 0x8D47, 0),
    ("MC_ReadDigitalOutputsFB", _ZERO5, 0x8D50, 0),
    ("MC_WriteDigitalOutputsFB", (("Index[2]", 1),), 0x8D48, 0),
    ("MC_WriteDigitalOutputsFB", (*_ZERO5, *_NO_MASK), 0x8D50, 0),
    ("MC_ReadSystemVariableFB", _SYSVAR, 0x8D74, 0),
    ("MC_ReadSystemVariableFB", (*_SYSVAR, ("ParameterID[0]", 35)), 0x8D74, 0),
    ("MC_ReadSystemVariableFB", (*_SYSVAR, ("ParameterID[0]", 2), ("SubParameterID[0]", 9)), 0x8D75, 0),
    ("MC_ReadSystemVariableFB", (*_SYSVAR, ("ParameterID[0]", 7), ("SubParameterID[0]", 1)), 0x8D76, 0),
    ("MC_ReadSystemVariableFB", (*_SYSVAR, ("ParameterID[0]", 2)), 0x8D77, 0),
    ("MC_CalculateFrameFB", (("ReferenceFrame", 20),), 0x8D88, 0),
]

# SDK 16#8D0C (no axis active) is not in table 7-1 of the specification (spec defines no code)
_BRAKE_ORDER = (
    "SDK BrakeTest (BrakeTestParameters::setActiveFromBitActive, response in SRCI::brakeTest): bit order "
    "reversed, J1/E1 = bit 6 .. J6/E6 = bit 1 instead of bit 1 .. 6 (spec table 6-757); ExternalAxesActive "
    "E1 (bit 1) is evaluated as E6 -> 16#8D0D, RobotAxesActive J1 reaches the firmware as J6"
)
KNOWN: dict[str, str] = {
    "MC_BrakeTestFB": _BRAKE_ORDER,
    "MC_SafeReferencingFB": "SDK CMD::SafeReferencing has a reserved byte after ToolNo: MaximumDistance and all "
    "following fields one byte later than in spec table 6-838 (MaximumDistance at byte 13)",
    "MC_ReadSafeReferencePositionFB": "spec table 6-832 is a copy of ReadActualPosition (E2..E6 twice, joint "
    "axes E1..E6 at bytes 50..73); the SDK sends J1..J6, E1..E6 from byte 6 - the library follows the table",
    "MC_ReadSystemVariableFB": "SDK readSystemVariable copies only Data_0 .. Data_5 of the firmware into the "
    "response, Data_6 / Data_7 stay 0 (spec ReadSystemVariable: eight parameters, Data_0 .. Data_7)",
}

KNOWN_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int, str]] = [
    (
        "MC_WriteDigitalOutputsFB",
        (("Index[3]", 0),),
        0,
        0x6D51,
        "SDK writeDigitalOutput: info code 16#6D51 (table 7-5, value for index 0) is reported as ErrorID, the "
        "command fails instead of being executed with an info",
    ),
    (
        "MC_WriteDigitalOutputsFB",
        (("OutputBitmask[3]", 0),),
        0,
        0x6D52,
        "SDK writeDigitalOutput: info code 16#6D52 (table 7-5, no bitmask for a non zero index) is reported as "
        "ErrorID, the command fails instead of being executed with an info",
    ),
    (
        "MC_ReadSystemVariableFB",
        (*_SYSVAR, ("ParameterID[0]", 2), ("SubParameterID[0]", 5)),
        0,
        0,
        "SDK readSystemVariable validSubParameter: maximum SubParameterID of standardSystemVariablesList[id - 1] "
        "(the previous variable): RCManufacturerName (2) SubParameterID 5 -> 16#8D75",
    ),
    (
        "MC_CalculateCartesianPositionFB",
        (("TargetFrameNo", 20),),
        0x8D72,
        0,
        "SDK calculateCartesianPosition writes the response states only when the firmware is called: a "
        "parameter error is never reported (the command hangs); code 16#8D73 instead of 16#8D72 (table 7-1)",
    ),
    (
        "MC_BrakeTestFB",
        (*_ROBOT_AXES, ("RobotAxesActive.AxisJ1", True), ("ExternalAxesActive.AxisE1", True)),
        0,
        0,
        _BRAKE_ORDER,
    ),
]
