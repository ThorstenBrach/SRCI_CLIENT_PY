"""SDK return, group TRIG: trigger functions and "Actions" (16_Application_Triggers.cpp, trigger engine).

The trigger functions are emitters (ListenerID 0); their condition is made to occur by a companion
function block started once the trigger function is buffered (``COMPANIONS``). ReactAtTrigger /
WaitForTrigger have ListenerID 1 (tests.sdk.test_methodology.PARCMD_INPUTS) and are released by an
MC_SetTriggerUserFB (tests.sdk.trigger_pump.attach_listener_trigger). The emitted triggers have no
"Action" -> warning 16#7C12, the command is Done.
"""

from __future__ import annotations

from typing import Any

from tests.sdk.trigger_pump import when_buffered

ADDED = (3000, 3001, 3002, 3003, 3004, 3005, 3006)

EMITTER = 7  # EmitterID of the trigger functions under test (no "Action" listens to it)
MOVE_EMITTER = 3  # EmitterID of the move command SetTriggerMotion refers to

_NO_CODES = {f"MessageCodes[{i}]": 0 for i in range(16)}

PARCMD: dict[str, dict[str, Any]] = {
    "MC_ReactAtTriggerFB": {"ReactionMode": 1},  # Interrupt (the RA is idle: nothing to interrupt)
    "MC_SetTriggerUserFB": {"EmitterID": EMITTER},
    # integer register 1 exceeds 50 (written by the companion WriteIntegers)
    "MC_SetTriggerRegisterFB": {
        "EmitterID": EMITTER,
        "ListenerID": 0,
        "TriggerMode": 50,
        "Index": 1,
        "BitIndex": 0,
        "IntValue[1]": 50,  # IntValue_1
        "IntValue[2]": 0,
        "RealValue[1]": 0.0,
        "RealValue[2]": 0.0,
    },
    # every monitored value (RSP_VALUES Data) exceeds Data_1, the start condition is evaluated
    "MC_SetTriggerLimitFB": {
        "EmitterID": EMITTER,
        "ListenerID": 0,
        "TriggerMode": 1,
        "EvaluateStartCondition": True,
        **{f"Data_1[{i}]": -100.0 for i in range(12)},
        **{f"Data_2[{i}]": -200.0 for i in range(12)},
    },
    # the error 16#8D50 of the companion ReadIntegers (all indexes 0)
    "MC_SetTriggerErrorFB": {
        "EmitterID": EMITTER,
        "ListenerID": 0,
        "Mode": 6,
        "IncludeParameterValidation": True,
        **_NO_CODES,
        "MessageCodes[0]": 0x8D50,
    },
    # on the move command with EmitterID 3: start at 10 % from the start, stop 10 % before the target
    "MC_SetTriggerMotionFB": {
        "ListenerID": MOVE_EMITTER,
        "EmitterID[0]": EMITTER,
        "EmitterID[1]": 0,
        "EmitterID[2]": 0,
        "EmitterID[3]": 0,
        "TriggerMode_1": 1,
        "TriggerParameter_1": 10.0,
        "TriggerMode_2": -1,
        "TriggerParameter_2": 10.0,
    },
}

RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_SetTriggerLimitFB": {f"Data[{i}]": 10.0 + i for i in range(12)},
}


def _write_register(fb: Any) -> None:
    fb.ParCmd.Index[0] = 1
    fb.ParCmd.Values[0] = 100


def _read_no_register(fb: Any) -> None:
    for i in range(7):
        fb.ParCmd.Index[i] = 0  # 16#8D50: at least one index must not be 0


def _move(fb: Any) -> None:
    fb.ParCmd.JointPosition.J1 = 10.0
    fb.ParCmd.VelocityRate = 100.0
    fb.ParCmd.AccelerationRate = 100.0
    fb.ParCmd.DecelerationRate = -1.0
    fb.ParCmd.JerkRate = -1.0
    fb.ParCmd.EmitterID[0] = MOVE_EMITTER


COMPANIONS: dict[str, tuple[Any, ...]] = {
    "MC_SetTriggerRegisterFB": (when_buffered("MC_WriteIntegersFB", _write_register),),
    "MC_SetTriggerErrorFB": (when_buffered("MC_ReadIntegersFB", _read_no_register),),
    "MC_SetTriggerMotionFB": (when_buffered("MC_MoveAxesAbsoluteFB", _move),),
}

# fields the SDK evaluates itself (the trigger engine), not passed to the firmware: none - every
# trigger function hands its condition to a firmware function (check* / getTriggerLimitValues)
FW_NOT_PASSED: dict[str, tuple[str, ...]] = {}

# parameter checks of the SDK (the client does not check them; ReactionMode 16#8D60 and the
# SetTriggerError Mode 16#8D59 are enums checked by the client)
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_SetTriggerRegisterFB", (("TriggerMode", 10), ("BitIndex", 9)), 0x8D55, 0),
    ("MC_SetTriggerRegisterFB", (("Index", 21),), 0x8D47, 0),
    ("MC_SetTriggerRegisterFB", (("TriggerMode", 54), ("IntValue[1]", 10), ("IntValue[2]", 5)), 0x8D57, 0),
    ("MC_SetTriggerRegisterFB", (("ListenerID", EMITTER),), 0x8D52, 0),
    ("MC_SetTriggerLimitFB", (("Data_1[0]", 1.0), ("Data_2[0]", 5.0)), 0x8D57, 0),
    ("MC_SetTriggerMotionFB", (("TriggerMode_1", 3),), 0x8E28, 0),
    (
        "MC_SetTriggerMotionFB",
        (
            ("TriggerMode_1", 1),
            ("TriggerParameter_1", 80.0),
            ("TriggerMode_2", 1),
            ("TriggerParameter_2", 20.0),
        ),
        0x8D58,
        0,
    ),
    ("MC_SetTriggerMotionFB", (("TriggerParameter_1", 120.0),), 0x8D57, 0),
    ("MC_SetTriggerUserFB", (("EmitterID", 0),), 0x8F04, 0),
]
