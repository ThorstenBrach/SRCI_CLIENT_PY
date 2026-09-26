"""Documented deviations of the transpiled code from the ST source.

Every entry names its reason (and the finding in docs/ST_FINDINGS.md). Source patches
fail when the ST text no longer contains the old text, so obsolete patches get noticed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourcePatch:
    pou: str
    method: str | None  # None: body of the POU
    old: str
    new: str
    reason: str
    regex: bool = False  # old is a regular expression (must match at least once)
    template: bool = False  # regex: new is a replacement template (group references \\1)


@dataclass(frozen=True)
class BodyAppend:
    """ST text appended to the body of a method (e.g. to override its result)."""

    pou: str
    method: str
    text: str
    reason: str


@dataclass(frozen=True)
class VarAppend:
    """Variables added to a POU (ST declaration text, e.g. ``"VAR\\n _x : BOOL;\\nEND_VAR"``)."""

    pou: str
    decl: str
    reason: str


@dataclass(frozen=True)
class PouClone:
    """Replace a POU by a copy of another POU with text replacements (declarations and code).

    Used when the ST implementation of a block has the wrong base behavior (e.g. Execute
    instead of Enable) and a similar block implements the right one."""

    target: str
    source: str
    replacements: tuple[tuple[str, str], ...]
    reason: str
    keep_methods: tuple[str, ...] = ()  # methods of the target that are kept
    target_decl: tuple[tuple[str, str], ...] | None = (
        None  # declaration of the target with these replacements
    )


@dataclass(frozen=True)
class Mixin:
    """Hand written methods of a POU (``ST-FIX`` or Python specific)."""

    module: str
    name: str
    methods: tuple[str, ...]
    reason: str


@dataclass
class Config:
    patches: list[SourcePatch] = field(default_factory=list)
    appends: list[BodyAppend] = field(default_factory=list)
    variables: list[VarAppend] = field(default_factory=list)
    clones: list[PouClone] = field(default_factory=list)
    mixins: dict[str, Mixin] = field(default_factory=dict)  # POU name -> mixin

    @property
    def hand_methods(self) -> dict[str, dict[str, Mixin]]:
        return {pou: {m.upper(): mix for m in mix.methods} for pou, mix in self.mixins.items()}


def _swap_no_and_data_changed(
    pou: str, comment: str, var: str, table: str
) -> tuple[SourcePatch, SourcePatch]:
    """F27: the response has the index (USINT) before the DataChanged byte, the ST code parses them swapped."""
    reason = f"F27: index before DataChanged in the response (spec table {table}), ST parses them swapped"
    return (
        SourcePatch(
            pou,
            "ParseResponsePayload",
            f"  // Get Response.{comment}\n _response.{var} := ResponseData.GetUsint();",
            "  // Get Response.DataChanged (ST-FIX F27)\n _response.DataChanged := ResponseData.GetBool();",
            reason,
        ),
        SourcePatch(
            pou,
            "ParseResponsePayload",
            "  // Get Response.DataChanged\n _response.DataChanged := ResponseData.GetBool();",
            f"  // Get Response.{comment} (ST-FIX F27)\n _response.{var} := ResponseData.GetUsint();",
            reason,
        ),
    )


# F28: CheckAddParameter omits a parameter when the bytes of the command structure behind the
# payload position are zero. That only works when the payload has the order of the structure;
# for these function blocks it has not (e.g. ToolNo is the last parameter of WriteToolData but
# the first element of the structure) -> non-zero parameters are omitted. Python always sends
# the complete payload. tests/unit/tools/test_st2py_f28.py checks this list against the code.
F28_POUS = (
    "MC_CalculateInverseKinematicFB",
    "MC_LoadMeasurementAutomaticFB",  # after ST-FIX F33 (Position_1.E2..E6 moved)
    "MC_EnableRobotFB",
    "MC_MoveApproachDirectFB",
    "MC_MoveApproachLinearFB",
    "MC_MoveAxesAbsoluteFB",
    "MC_MoveAxesRelativeFB",
    "MC_MoveCircularAbsoluteFB",
    "MC_MoveCircularCamFB",
    "MC_MoveCircularRelativeFB",
    "MC_MoveDepartDirectFB",
    "MC_MoveDepartLinearFB",
    "MC_MoveDirectAbsoluteFB",
    "MC_MoveDirectOffsetFB",
    "MC_MoveDirectRelativeFB",
    "MC_MoveLinearAbsoluteFB",
    "MC_MoveLinearAbsoluteJFB",
    "MC_MoveLinearCamFB",
    "MC_MoveLinearOffsetFB",
    "MC_MoveLinearRelativeFB",
    "MC_MovePickPlaceDirectFB",
    "MC_MovePickPlaceLinearFB",
    "MC_MoveSuperImposedDynamicFB",
    "MC_MoveSuperImposedFB",
    "MC_ReadSystemVariableFB",
    "MC_SearchHardStopFB",
    "MC_SearchHardStopJFB",
    "MC_WriteIntegersFB",
    "MC_WriteLoadDataFB",
    "MC_WriteRealsFB",
    "MC_WriteRobotSWLimitsFB",
    "MC_WriteToolDataFB",
    "MC_WriteWorkAreaFB",
)


# F51: the inputs AbortingMode / SequenceFlag / ProcessingMode were checked but not used - the
# telegram always had the ExecutionMode of the base input ExecMode. Python derives the
# ExecutionMode from them (spec table 5-77 "ProcessingModes - ExecutionModes mapping").
F51_ABORTING_POUS = (
    "MC_BrakeTestFB",
    "MC_DynamicSplineFB",  # spec table 5-77: AbortingMode/SequenceFlag (the library had CONTINUOUS)
    "MC_LoadMeasurementAutomaticFB",
    "MC_MoveApproachDirectFB",
    "MC_MoveApproachLinearFB",
    "MC_MoveAxesAbsoluteFB",
    "MC_MoveAxesRelativeFB",
    "MC_MoveCircularAbsoluteFB",
    "MC_MoveCircularCamFB",
    "MC_MoveCircularRelativeFB",
    "MC_MoveDepartDirectFB",
    "MC_MoveDepartLinearFB",
    "MC_MoveDirectAbsoluteFB",
    "MC_MoveDirectOffsetFB",
    "MC_MoveDirectRelativeFB",
    "MC_MoveLinearAbsoluteFB",
    "MC_MoveLinearAbsoluteJFB",
    "MC_MoveLinearCamFB",
    "MC_MoveLinearOffsetFB",
    "MC_MoveLinearRelativeFB",
    "MC_MovePickPlaceDirectFB",
    "MC_MovePickPlaceLinearFB",
    "MC_MoveSplineFB",
    "MC_SearchHardStopFB",
    "MC_SearchHardStopJFB",
    "MC_SoftSwitchTcpFB",
    "MC_WaitTimeFB",
)
# (POU, has input SequenceFlag)
F51_PROCESSING_POUS = (
    ("MC_ActivateNextCommandFB", False),
    ("MC_CallSubprogramFB", True),
    ("MC_CollisionDetectionFB", True),
    ("MC_LoadMeasurementSequentialFB", True),
    ("MC_MoveSuperImposedFB", False),
    ("MC_ReactAtTriggerFB", False),
    ("MC_ReadActualForceFB", False),
    ("MC_ReadActualPositionFB", True),
    ("MC_ReadActualTCPVelocityFB", True),
    ("MC_ReadAnalogInputFB", True),
    ("MC_ReadDigitalInputsFB", True),
    ("MC_ReadDigitalOutputsFB", True),
    ("MC_ReadIntegersFB", True),
    ("MC_ReadRealsFB", True),
    ("MC_ReadSystemVariableFB", True),
    ("MC_RedefineTrackingPosFB", False),
    ("MC_SetTriggerErrorFB", False),
    ("MC_SetTriggerLimitFB", False),
    ("MC_SetTriggerMotionFB", False),
    ("MC_SetTriggerRegisterFB", False),
    ("MC_SetTriggerUserFB", True),
    ("MC_StopSubprogramFB", True),
    ("MC_WaitForTriggerFB", True),
    ("MC_WriteAnalogOutputFB", True),
    ("MC_WriteDigitalOutputsFB", True),
    ("MC_WriteFrameDataFB", True),
    ("MC_WriteIntegersFB", True),
    ("MC_WriteLoadDataFB", True),
    ("MC_WriteRealsFB", True),
    ("MC_WriteSystemVariableFB", True),
    ("MC_WriteToolDataFB", True),
    ("MC_WriteWorkAreaFB", False),
)
_EXEC_MODE = r"_command\.ExecMode\s*:=\s*ExecMode\s*;"


def _exec_mode_from_aborting(pou: str) -> SourcePatch:
    return SourcePatch(
        pou,
        "CreateCommandPayload",
        _EXEC_MODE,
        "// ST-FIX F51: ExecutionMode from AbortingMode and SequenceFlag (spec table 5-77)\n"
        "IF ( SequenceFlag = SequenceFlag.SECONDARY_SEQUENCE ) THEN\n"
        "  IF ( AbortingMode = AbortingMode.ABORT ) THEN\n"
        "    _command.ExecMode := ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY;\n"
        "  ELSE\n"
        "    _command.ExecMode := ExecutionMode.SEQUENCE_SECONDARY;\n"
        "  END_IF\n"
        "ELSE\n"
        "  IF ( AbortingMode = AbortingMode.ABORT ) THEN\n"
        "    _command.ExecMode := ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY;\n"
        "  ELSE\n"
        "    _command.ExecMode := ExecutionMode.SEQUENCE_PRIMARY;\n"
        "  END_IF\n"
        "END_IF",
        "F51: AbortingMode/SequenceFlag had no effect on the ExecutionMode of the telegram",
        regex=True,
    )


def _exec_mode_from_processing(pou: str, sequence_flag: bool) -> SourcePatch:
    secondary = "SequenceFlag = SequenceFlag.SECONDARY_SEQUENCE" if sequence_flag else "FALSE"
    return SourcePatch(
        pou,
        "CreateCommandPayload",
        _EXEC_MODE,
        "// ST-FIX F51: ExecutionMode from ProcessingMode (and SequenceFlag), spec table 5-77\n"
        "CASE ProcessingMode OF\n"
        "  ProcessingMode.BUFFERED, ProcessingMode.TRIGGER_BUFFERED:\n"
        f"    IF ( {secondary} ) THEN _command.ExecMode := ExecutionMode.SEQUENCE_SECONDARY;\n"
        "    ELSE _command.ExecMode := ExecutionMode.SEQUENCE_PRIMARY; END_IF\n"
        "  ProcessingMode.ABORTING, ProcessingMode.TRIGGER_ABORTING:\n"
        f"    IF ( {secondary} ) THEN _command.ExecMode := ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY;\n"
        "    ELSE _command.ExecMode := ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY; END_IF\n"
        "  ProcessingMode.PARALLEL, ProcessingMode.TRIGGER_ONCE:\n"
        "    _command.ExecMode := ExecutionMode.PARALLEL;\n"
        "  ProcessingMode.CONTINUOUS, ProcessingMode.TRIGGER_CONTINUOUS:\n"
        "    _command.ExecMode := ExecutionMode.CONTINUOUS;\n"
        "  ProcessingMode.TRIGGER_MULTIPLE:\n"
        "    _command.ExecMode := ExecutionMode.TRIGGER_MULTIPLE;\n"
        "  ProcessingMode.DEACTIVATE:\n"
        "    _command.ExecMode := ExecutionMode.STOP_PARALLEL_CONTINUOUS_TRIGGER;\n"
        "ELSE\n"
        "  // undefined ProcessingMode -> error, not sent (ST-FIX F49)\n"
        "  _command.ExecMode := ExecMode;\n"
        "  SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite := TRUE );\n"
        "  OnUpdateStateFlags( State := CmdMessageState.ERROR );\n"
        "END_CASE",
        "F51: ProcessingMode/SequenceFlag had no effect on the ExecutionMode of the telegram",
        regex=True,
    )


F26_POUS = (
    "MC_ActivateNextCommandFB",
    "MC_CallSubprogramFB",
    "MC_CollisionDetectionFB",
    "MC_LoadMeasurementSequentialFB",
    "MC_MoveSuperImposedFB",
    "MC_ReactAtTriggerFB",
    "MC_ReadActualForceFB",
    "MC_ReadActualPositionFB",
    "MC_ReadActualTCPVelocityFB",
    "MC_ReadAnalogInputFB",
    "MC_ReadDigitalInputsFB",
    "MC_ReadDigitalOutputsFB",
    "MC_ReadIntegersFB",
    "MC_ReadRealsFB",
    "MC_ReadSystemVariableFB",
    "MC_RedefineTrackingPosFB",
    "MC_SetTriggerErrorFB",
    "MC_SetTriggerLimitFB",
    "MC_SetTriggerMotionFB",
    "MC_SetTriggerRegisterFB",
    "MC_SetTriggerUserFB",
    "MC_StopSubprogramFB",
    "MC_WaitForTriggerFB",
    "MC_WriteAnalogOutputFB",
    "MC_WriteDigitalOutputsFB",
    "MC_WriteFrameDataFB",
    "MC_WriteIntegersFB",
    "MC_WriteLoadDataFB",
    "MC_WriteRealsFB",
    "MC_WriteSystemVariableFB",
    "MC_WriteToolDataFB",
)


def _range_or(pou: str) -> SourcePatch:
    return SourcePatch(
        pou,
        "CheckParameterValid",
        r"(\(\s*(?:ParCmd\.)?ProcessingMode\s*<\s*ProcessingModeEnum\.BUFFERED\s*\)\s*)AND"
        r"(\s*\n\s*\(\s*(?:ParCmd\.)?ProcessingMode\s*>\s*ProcessingModeEnum\.TRIGGER_MULTIPLE\s*\))",
        r"\1OR // ST-FIX F26\2",
        "F26: range check with AND is never TRUE",
        regex=True,
        template=True,
    )


# F25: output Valid was never set to TRUE
F25_POUS = (
    "MC_ActivateConveyorTrackingFB",
    "MC_CallSubprogramFB",
    "MC_ReadActualForceFB",
    "MC_ReadActualPositionFB",
    "MC_ReadActualTCPVelocityFB",
    "MC_ReadAnalogInputFB",
    "MC_ReadDigitalInputsFB",
    "MC_ReadDigitalOutputsFB",
    "MC_ReadIntegersFB",
    "MC_ReadRealsFB",
    "MC_ReadSystemVariableFB",
    "MC_SetTriggerLimitFB",
)


def _valid(pou: str) -> BodyAppend:
    return BodyAppend(
        pou,
        "OnUpdateStateFlags",
        "// ST-FIX F25: output data are valid while the command is active (continuous) or done\n"
        "Valid := ( State = CmdMessageState.ACTIVE ) OR ( State = CmdMessageState.DONE );\n",
        "F25: Valid was never set (spec 5.5.x: TRUE while the presented output data are valid)",
    )


def _bits_in_one_byte(pou: str, bit0: str, bit1: str, table: str) -> tuple[SourcePatch, SourcePatch]:
    """F37: two BOOLs that are bit 0 and 1 of one byte were sent as two bytes."""
    reason = f"F37: {bit0}/{bit1} are bit 0/1 of one byte (spec table {table}), ST sent 2 bytes"
    return (
        SourcePatch(
            pou,
            "CreateCommandPayload",
            f"CreateCommandPayload.AddBool(_command.{bit0});",
            f"CreateCommandPayload.AddByte(BOOL_TO_BYTE(_command.{bit0}) OR SHL(BOOL_TO_BYTE(_command.{bit1}), 1));"
            " // ST-FIX F37",
            reason,
        ),
        SourcePatch(
            pou,
            "CreateCommandPayload",
            f"CreateCommandPayload.AddBool(_command.{bit1});",
            "CreateCommandPayload.AddByte(0); // ST-FIX F37: reserved byte, the value is bit 1 of the byte before",
            reason,
        ),
    )


# ---------------------------------------------------------------- F33 payload layout helpers
_ADD_BLOCK = (
    r"//\s*Check parameter must be added \?[^\n]*\n\s*IF\s*\(\s*CheckAddParameter\(CreateCommandPayload\.PayloadPtr\)\s*\)"
    r"[^\n]*\n\s*THEN[^\n]*\n\s*//\s*add command\.{field}[ \t]*\n(?:(?!END_IF)[\s\S])*?END_IF[^\n]*\n"
)
_GET_BLOCK = (
    r"//\s*Check payload remaining \?[^\n]*\n\s*IF\s*\(\s*ResponseData\.IsPayloadRemaining\s*\)"
    r"[^\n]*\n\s*THEN[^\n]*\n\s*//\s*Get Response\.{field}[ \t]*\n(?:(?!END_IF)[\s\S])*?END_IF[^\n]*\n"
)


def _block(method: str, field: str) -> str:
    pattern = _ADD_BLOCK if method == "CreateCommandPayload" else _GET_BLOCK
    return pattern.replace("{field}", re.escape(field))


def _payload(
    pou: str, method: str, field: str, action: str, st: str, reason: str, context: str | None = None
) -> SourcePatch:
    """Payload fix at the parameter block of ``field`` (comment ``// add command.<field>`` /
    ``// Get Response.<field>``): action ``before``, ``after``, ``replace`` (``st`` replaces the
    block, empty: removed)."""
    text = (
        f"// ST-FIX {reason.split(':')[0]}\n{st}\n"
        if st
        else f"// ST-FIX {reason.split(':')[0]}: {field} removed\n"
    )
    text = text.replace("\\", "\\\\")
    pattern = f"(?P<block>{_block(method, field)})"
    prefix = ""
    if context is not None:  # the block directly after the block containing ``context``
        pattern = r"(?P<ctx>" + context + r"(?:(?!END_IF)[\s\S])*?END_IF[^\n]*\n\s*)" + pattern
        prefix = r"\g<ctx>"
    if action == "before":
        new = prefix + text + r"\g<block>"
    elif action == "after":
        new = prefix + r"\g<block>" + text
    else:
        new = prefix + text
    return SourcePatch(pou, method, pattern, new, reason, regex=True, template=True)


def _add(field_st: str, method: str = "AddByte") -> str:
    return f"CreateCommandPayload.{method}({field_st});\n_parameterCnt := _parameterCnt + 1;"


def _after_loop(pou: str, call: str, st: str, reason: str) -> SourcePatch:
    """ST text inserted after the FOR loop that contains ``call``."""
    return SourcePatch(
        pou,
        "CreateCommandPayload",
        r"(" + re.escape(call) + r"[\s\S]*?END_FOR)",
        r"\1\n// ST-FIX " + reason.split(":")[0] + "\n" + st,
        reason,
        regex=True,
        template=True,
    )


_LOG = "// Create logging\nCreateCommandPayloadLog(AxesGroup := AxesGroup, ParameterCnt := _parameterCnt);"


def _append_payload(pou: str, st: str, reason: str) -> SourcePatch:
    """Parameters added at the end of the command payload."""
    return SourcePatch(
        pou, "CreateCommandPayload", _LOG, f"// ST-FIX {reason.split(':')[0]}\n{st}\n\n{_LOG}", reason
    )


F33_PATCHES = (
    _payload(
        "MC_MoveApproachDirectFB",
        "CreateCommandPayload",
        "Reserve",
        "replace",
        "",
        "F33: AddArmConfig writes 2 bytes (config + reserved), the additional Reserve byte shifted E1..E6",
        context=r"AddArmConfig\(",
    ),
    *(
        _payload(
            "MC_WaitTimeFB",
            method,
            f"Reserve{i}",
            "replace",
            "",
            "F33: 4 bytes after Time are not in the spec",
        )
        for method in ("CreateCommandPayload", "ParseResponsePayload")
        for i in range(1, 5)
    ),
    _payload(
        "MC_MoveLinearRelativeFB",
        "CreateCommandPayload",
        "MoveTime",
        "before",
        _add("0"),
        "F33: Reserved byte before Time (spec table 6-310) was missing",
    ),
    _payload(
        "MC_SetTriggerLimitFB",
        "CreateCommandPayload",
        "ListenerID",
        "after",
        _add("0"),
        "F33: Reserved byte after ListenerID (spec table 6-607) was missing",
    ),
    _payload(
        "MC_SetTriggerMotionFB",
        "CreateCommandPayload",
        "ListenerID",
        "after",
        _add("0"),
        "F33: Reserved byte after ListenerID (spec table 6-696) was missing",
    ),
    *_bits_in_one_byte("MC_MoveCircularAbsoluteFB", "PathChoice", "Manipulation", "6-348"),
    _payload(
        "MC_MoveCircularAbsoluteFB",
        "CreateCommandPayload",
        "Reserve2",
        "replace",
        _add("_command.ConfigMode[0]")
        + "\n"
        + _add("_command.ConfigMode[1]")
        + "\n"
        + _add("_command.TurnMode", "AddUsint")
        + "\n"
        + _add("0")
        + "\n"
        + _add("_command.MoveTime", "AddUint"),
        "F33: ConfigMode, TurnMode, Reserved and Time (spec table 6-348) were missing",
    ),
    _payload(
        "MC_MoveCircularCamFB",
        "CreateCommandPayload",
        "Reserve",
        "after",
        _add("_command.MoveTime", "AddUint"),
        "F33: Time (spec table 6-563) was missing",
    ),
    _payload(
        "MC_MoveLinearCamFB",
        "CreateCommandPayload",
        "Manipulation",
        "replace",
        "",
        "F33: Manipulation was sent before BlendingParameter (spec table 6-545: byte 70)",
    ),
    _payload(
        "MC_MoveLinearCamFB",
        "CreateCommandPayload",
        "MoveTime",
        "replace",
        "\n".join(
            (
                _add("_command.TriggerDelay", "AddUint"),
                _add("_command.TriggerDistance", "AddReal"),
                _add("_command.Index", "AddUsint"),
                _add("_command.RelativePosition", "AddBool"),
                _add("_command.OutputBitmask"),
                _add("_command.Value"),
                _add("_command.ConfigMode[0]"),
                _add("_command.ConfigMode[1]"),
                _add("_command.Manipulation", "AddBool"),
                _add("_command.TurnMode", "AddUsint"),
                _add("_command.MoveTime", "AddUint"),
            )
        ),
        "F33: TriggerDelay .. TurnMode (spec table 6-545 bytes 58..71) were not sent",
    ),
    SourcePatch(
        "MC_ForceControlFB",
        "CreateCommandPayload",
        "CreateCommandPayload.AddUInt(_command.ReferenceType);",
        "CreateCommandPayload.AddUsint(_command.ReferenceType); // ST-FIX F33: USINT (spec table 6-741)",
        "F33: ReferenceType was sent as UINT",
    ),
    _payload(
        "MC_MoveLinearCamFB",
        "CreateCommandPayload",
        "Position.E1",
        "before",
        "CreateCommandPayload.AddArmConfig(_command.Position.Config);\n_parameterCnt := _parameterCnt + 1;\n"
        "CreateCommandPayload.AddTurnNumber(_command.Position.TurnNumber);\n_parameterCnt := _parameterCnt + 1;",
        "F33: Config and TurnNumber of Position (spec table 6-545 bytes 48..53) were not sent",
    ),
    _payload(
        "MC_ForceControlFB",
        "CreateCommandPayload",
        "MaxVelocity",
        "before",
        _add("_parCmd.TargetWindow", "AddReal"),
        "F33: TargetWindow (spec table 6-741 byte 82) was not sent",
    ),
    _after_loop(
        "MC_WriteDigitalOutputsFB",
        "AddUsint(_command.Index[_idx]);",
        _add("0"),
        "F33: Reserved byte 15 after Index (spec table 6-512) was missing",
    ),
    _after_loop(
        "MC_WriteDigitalOutputsFB",
        "AddByte(_command.OutputBitmask[_idx]);",
        _add("0"),
        "F33: Reserved byte 21 after OutputBitmask (spec table 6-512) was missing",
    ),
    SourcePatch(
        "MC_WriteDigitalOutputsFB",
        "CreateCommandPayload",
        "CreateCommandPayload.AddReal(_command.Values[_idx]);",
        "CreateCommandPayload.AddByte(_command.Values[_idx]); // ST-FIX F33: BYTE (spec table 6-512)",
        "F33: Values were sent as REAL",
    ),
    SourcePatch(
        "MC_WriteIntegersFB",
        "CreateCommandPayload",
        "FOR _idx := 1 TO 6",
        "FOR _idx := 0 TO 6 // ST-FIX F33",
        "F33: Values/Index are [0..6] (spec table 6-530), the loops ran from 1",
    ),
    _payload(
        "MC_WriteWorkAreaFB",
        "CreateCommandPayload",
        "WorkAreaData.DefinitionMode",
        "replace",
        "",
        "F33: DefinitionMode was removed from the work area data in the spec (change log, table 6-229)",
    ),
    _payload(
        "MC_ReadWorkAreaFB",
        "ParseResponsePayload",
        "WorkAreaData.DefinitionMode",
        "replace",
        "",
        "F33: DefinitionMode was removed from the work area data in the spec (change log)",
    ),
    _payload(
        "MC_CalculateToolFB",
        "ParseResponsePayload",
        "IEC_Date",
        "replace",
        "",
        "F33: ToolData.Date follows TCPMaxError/TCPMeanError (spec table 6-673)",
    ),
    _payload(
        "MC_CalculateToolFB",
        "ParseResponsePayload",
        "TCPMeanError",
        "after",
        "_response.ToolData.Timestamp.IEC_Date := ResponseData.GetIecDate();\n_parameterCnt := _parameterCnt + 1;",
        "F33: ToolData.Date follows TCPMaxError/TCPMeanError (spec table 6-673)",
    ),
    SourcePatch(
        "MC_ForceLimitFB",
        "ParseResponsePayload",
        _block("ParseResponsePayload", "ForceStatus")
        + r"(?=\s*//\s*Check payload remaining[^\n]*\n[^\n]*\n[^\n]*\n\s*//\s*Get Response\.InvocationCounter)",
        "// ST-FIX F33: ForceStatus is the last value (byte 8, spec table 6-750), it was read twice\n",
        "F33: ForceStatus was read before InvocationCounter as well",
        regex=True,
    ),
    SourcePatch(
        "MC_ReadDHParameterFB",
        "ParseResponsePayload",
        r"FOR _idx := 0 TO 6(?:(?!FOR _idx)[\s\S])*?PositiveJointDirection\[_idx\] := ResponseData\.GetBool\(\);[\s\S]*?END_FOR",
        "// ST-FIX F33: PositiveJointDirection[0..6] are the bits 0..6 of one byte (spec table)\n"
        "IF ( ResponseData.IsPayloadRemaining )\nTHEN\n"
        "  _directionBits := ResponseData.GetByte();\n"
        "  FOR _idx := 0 TO 6\n  DO\n"
        "    _response.DHParameter.PositiveJointDirection[_idx] := ( ( SHR(_directionBits, _idx) AND 1 ) = 1 );\n"
        "  END_FOR\n"
        "  _parameterCnt := _parameterCnt + 1;\nEND_IF",
        "F33: PositiveJointDirection was read as 7 bytes, the spec has 7 bits of one byte",
        regex=True,
    ),
    _payload(
        "MC_MonitorWorkAreaFB",
        "ParseResponsePayload",
        "MonitoringState",
        "replace",
        "",
        "F33: ActivationState/MonitoringState are bit 0/1 of one WORD (spec table 6-242)",
    ),
    _payload(
        "MC_MonitorWorkAreaFB",
        "ParseResponsePayload",
        "ActivationState",
        "replace",
        "IF ( ResponseData.IsPayloadRemaining )\nTHEN\n"
        "  _response.ActivationState := ResponseData.GetWord();\n"
        "  _response.MonitoringState := SHR(_response.ActivationState, 1) AND 1;\n"
        "  _response.ActivationState := _response.ActivationState AND 1;\n"
        "  _parameterCnt := _parameterCnt + 1;\nEND_IF",
        "F33: ActivationState/MonitoringState are bit 0/1 of one WORD (spec table 6-242)",
    ),
    SourcePatch(
        "MC_CallSubprogramFB",
        "ParseResponsePayload",
        _block("ParseResponsePayload", "InProgress") + r"(?=\s*FOR _idx)",
        r"\g<0>// ST-FIX F33: Reserved byte 11 before ReturnData (spec table 6-710)\n"
        "IF ( ResponseData.IsPayloadRemaining )\nTHEN\n  ResponseData.GetByte();\nEND_IF\n",
        "F33: the Reserved byte before ReturnData was not skipped -> ReturnData shifted by one",
        regex=True,
        template=True,
    ),
    *(
        _payload(
            "MC_LoadMeasurementAutomaticFB",
            "CreateCommandPayload",
            f"Position_1.E{i}",
            "replace",
            "",
            "F33: Position_1.E2..E6 follow Position_2.E1 (spec: J1..E1 of both positions, then E2..E6)",
        )
        for i in range(2, 7)
    ),
    _payload(
        "MC_LoadMeasurementAutomaticFB",
        "CreateCommandPayload",
        "Position_2.E1",
        "after",
        "\n".join(_add(f"_command.Position_1.E{i}", "AddReal") for i in range(2, 7)),
        "F33: Position_1.E2..E6 follow Position_2.E1 (spec: J1..E1 of both positions, then E2..E6)",
    ),
    _append_payload(
        "MC_WriteSystemVariableFB",
        "_command.RCParameter := _parCmd.RCParameter;\n" + _add("_command.RCParameter", "AddBool"),
        "F33: RCParameter (last byte, spec table 6-648) was never sent",
    ),
)


_RSP_LOG = (
    "// Create logging\n"
    "ParseResponsePayloadLog(ResponseData := ResponseData, Timestamp := Timestamp, ParameterCnt := _parameterCnt);"
)


def _append_response(pou: str, field_st: str, get: str, reason: str) -> SourcePatch:
    """Value read at the end of the response payload."""
    return SourcePatch(
        pou,
        "ParseResponsePayload",
        _RSP_LOG,
        f"// ST-FIX {reason.split(':')[0]}\nIF ( ResponseData.IsPayloadRemaining )\nTHEN\n"
        f"  {field_st} := ResponseData.{get}();\n  _parameterCnt := _parameterCnt + 1;\nEND_IF\n\n{_RSP_LOG}",
        reason,
    )


F32_PATCHES = (
    _append_response(
        "MC_GroupStopFB", "_response.AbortedSequence", "GetSint", "F32: AbortedSequence (byte 4) was not read"
    ),
    BodyAppend(
        "MC_GroupStopFB",
        "OnUpdateStateFlags",
        "// ST-FIX F32: output AbortedSequence\nAbortedSequence := _response.AbortedSequence;\n",
        "F32: AbortedSequence",
    ),
    _append_response(
        "MC_ExchangeConfigurationFB",
        "_response.NumberOfServerLogs",
        "GetUint",
        "F32: NumberOfServerLogs (bytes 28..29) was not read",
    ),
    BodyAppend(
        "MC_ExchangeConfigurationFB",
        "OnApplyOutCmd",
        "// ST-FIX F32\nOutCmd.NumberOfServerLogs := _response.NumberOfServerLogs;\n",
        "F32: NumberOfServerLogs",
    ),
    _append_response(
        "MC_ReadRobotSWLimitsFB",
        "_response.DataChanged",
        "GetBool",
        "F32: DataChanged (byte 106) was not read",
    ),
    BodyAppend(
        "MC_ReadRobotSWLimitsFB",
        "OnApplyOutCmd",
        "// ST-FIX F32\nOutCmd.DataChanged := _response.DataChanged;\n",
        "F32: DataChanged",
    ),
    SourcePatch(
        "MC_ReadMessagesFB",
        "ParseResponsePayload",
        "ResponseData.GetDataBlock(pData := ADR(_response.Text) , SIZEOF(_response.Text) , IsString := TRUE );",
        "ResponseData.GetDataBlock(pData := ADR(_response.Text) , 151 , IsString := TRUE ); // ST-FIX F32: 150 chars + terminator",
        "F32: the message text has 150 characters (spec, SDK); 255 were read",
    ),
)


def _pad_string(pou: str, field: str, length: int, table: str) -> SourcePatch:
    """F34: fixed length string fields (padded with 0)."""
    return SourcePatch(
        pou,
        "CreateCommandPayload",
        f"CreateCommandPayload.AddString(_command.{field});",
        f"// ST-FIX F34: {field} is a field of {length} characters (spec table {table}), padded with 0\n"
        f"CreateCommandPayload.AddDataBlock(pValue := ADR(_command.{field}), Size := {length});",
        f"F34: {field} was sent with its actual length instead of the field length {length}",
    )


F34_PATCHES = (
    _pad_string("MC_UserLoginFB", "Password", 50, "6-69"),
    _pad_string("MC_UserLoginFB", "Username", 50, "6-69"),
    _pad_string("MC_SwitchLanguageFB", "LanguageCode", 2, "6-76"),
)


SPLINE_PATCHES: tuple[SourcePatch, ...] = (
    SourcePatch(
        "MC_CreateSplineFB",
        "CreateCommandPayload",
        r"(SUPER\^\.CreateCommandPayload[\s\S]*?)FOR _idx := 1 TO RobotLibraryParameter\.SPLINE_DATA_MAX",
        r"\1FOR _idx := _pointIndex TO _pointIndex // ST-FIX F33: one spline point per command",
        "F33: the payload of CreateSpline has one SplineData (spec table 6-776); all 64 points were "
        "written into one payload (> 255 bytes, behind the buffer)",
        regex=True,
        template=True,
    ),
    SourcePatch(
        "MC_CreateSplineFB",
        "OnExecRun",
        "_command.ParSeq := 1;",
        "_command.ParSeq := 1;\n// ST-FIX F33: first spline point\n_pointIndex := 1;",
        "F33: one command per spline point",
    ),
    SourcePatch(
        "MC_CreateSplineFB",
        "OnExecRun",
        "_responseReceived := FALSE;",
        "_responseReceived := FALSE;\n"
        "// ST-FIX F33: the next spline point is sent when the last one is done\n"
        "IF ( _response.State = CmdMessageState.DONE ) AND ( _pointIndex < _pointCount )\nTHEN\n"
        "  _pointIndex := _pointIndex + 1;\n"
        "  _rspHeader.State := CmdMessageState.EMPTY;\n"
        "  CommandData := CreateCommandPayload(AxesGroup := AxesGroup);\n"
        "  _uniqueID := AxesGroup.Acyclic.ActiveCommandRegister.AddCmd( pCommandFB := ADR(THIS^ ));\n"
        "  SetTimeout(PT := _timeoutCmd, rTimer := _timerCmd);\n"
        "  RETURN;\n"
        "END_IF",
        "F33: one command per spline point",
    ),
)
SPLINE_PATCHES = (
    *SPLINE_PATCHES,
    SourcePatch(
        "MC_DynamicSplineFB",
        "CreateCommandPayload",
        r"(SUPER\^\.CreateCommandPayload[\s\S]*?)FOR _idx := 1 TO RobotLibraryParameter\.SPLINE_DATA_MAX",
        r"\1FOR _idx := _pointIndex TO _pointIndex // ST-FIX F33: one spline point per command",
        "F33: the payload of DynamicSpline has one SplineData (spec); all 64 points were written",
        regex=True,
        template=True,
    ),
)
SPLINE_PATCHES = (
    *SPLINE_PATCHES,
    *(
        SourcePatch(
            pou,
            "CheckParameterValid",
            "FOR _idx := 0 TO RobotLibraryParameter.SPLINE_DATA_MAX",
            "FOR _idx := 1 TO RobotLibraryParameter.SPLINE_DATA_MAX // ST-FIX F54",
            "F54: loop 0..SPLINE_DATA_MAX over SplineData[1..SPLINE_DATA_MAX] (reads before the array)",
        )
        for pou in ("MC_CreateSplineFB", "MC_DynamicSplineFB")
    ),
)
SPLINE_PATCHES = (
    *SPLINE_PATCHES,
    *(
        SourcePatch(
            pou,
            "CreateCommandPayload",
            "_command.SplineData[_idx].FrameNo          :=              _parCmd.SplineData[_idx].FrameNo;",
            "_command.SplineData[_idx].FrameNo          :=              _parCmd.SplineData[_idx].FrameNo;\n"
            "  _command.SplineData[_idx].Position         :=              _parCmd.SplineData[_idx].Position; "
            "// ST-FIX F55",
            "F55: the positions of the spline points were never copied into the command (always 0 sent)",
        )
        for pou in ("MC_CreateSplineFB", "MC_DynamicSplineFB")
    ),
)
SPLINE_APPENDS = (
    BodyAppend(
        "MC_CreateSplineFB",
        "CheckParameterValid",
        "// ST-FIX F33: number of spline points = highest index of a point that is not empty\n"
        "_pointCount := 0;\n"
        "FOR _idx := 1 TO RobotLibraryParameter.SPLINE_DATA_MAX\nDO\n"
        "  IF ( SysDepMemCmp(pData1 := ADR(ParCmd.SplineData[_idx]), pData2 := ADR(_emptyPoint), "
        "DataLen := SIZEOF(_emptyPoint)) <> RobotLibraryConstants.OK )\n"
        "  THEN\n    _pointCount := _idx;\n  END_IF\nEND_FOR\n"
        "IF ( _pointCount = 0 )\nTHEN\n"
        "  CheckParameterValid := FALSE;\n"
        "  SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite := TRUE );\n"
        "  RETURN;\nEND_IF\n",
        "F33: number of spline points (one command per point)",
    ),
    BodyAppend(
        "MC_DynamicSplineFB",
        "CheckParameterValid",
        "// ST-FIX F33: number of spline points = highest index of a point that is not empty\n"
        "_pointCount := 0;\n"
        "FOR _idx := 1 TO RobotLibraryParameter.SPLINE_DATA_MAX\nDO\n"
        "  IF ( SysDepMemCmp(pData1 := ADR(ParCmd.SplineData[_idx]), pData2 := ADR(_emptyPoint), "
        "DataLen := SIZEOF(_emptyPoint)) <> RobotLibraryConstants.OK )\n"
        "  THEN\n    _pointCount := _idx;\n  END_IF\nEND_FOR\n",
        "F33: number of spline points (one parameter update per point)",
    ),
)


def _state_output(pou: str, output: str, expr: str) -> tuple[VarAppend, BodyAppend, BodyAppend]:
    """F45: output of the spec that the block did not have (set from the command state)."""
    return (
        VarAppend(pou, f"VAR_OUTPUT\n  {output} : BOOL;\nEND_VAR", f"F45: output {output} of the spec"),
        BodyAppend(
            pou,
            "OnUpdateStateFlags",
            f"// ST-FIX F45: output {output}\n{output} := {expr};\n",
            f"F45: output {output} of the spec",
        ),
        BodyAppend(pou, "Reset", f"// ST-FIX F45\n{output} := FALSE;\n", f"F45: output {output} of the spec"),
    )


F45_OUTPUTS = (
    *_state_output("MC_GroupStopFB", "Active", "( State = CmdMessageState.ACTIVE )"),
    *_state_output("MC_SetSequenceFB", "Active", "( State = CmdMessageState.ACTIVE )"),
    *_state_output("MC_MeasuringInputFB", "CommandAborted", "( State = CmdMessageState.ABORTED )"),
    *_state_output(
        "MC_ReadRealsFB",
        "ParameterAccepted",
        "ParameterAccepted OR ( State = CmdMessageState.BUFFERED ) OR ( State = CmdMessageState.ACTIVE ) OR "
        "( State = CmdMessageState.DONE )",
    ),
    BodyAppend(
        "MC_CallSubprogramFB",
        "OnApplyOutCmd",
        "// ST-FIX F45\nOutCmd.Progress := _response.Progress;\n",
        "F45: output Progress",
    ),
    BodyAppend(
        "MC_SetTriggerLimitFB",
        "OnApplyOutCmd",
        "// ST-FIX F45\nOutCmd.Data := _response.Data;\n",
        "F45: output Data",
    ),
)


def _enum_check(pou: str, expr: str, enum: str, values: tuple[str, ...], error: str) -> BodyAppend:
    """F49: an enum parameter was not checked -> undefined values were sent to the RC."""
    cond = " AND\n    ".join(f"( {expr} <> {enum}.{v} )" for v in values)
    return BodyAppend(
        pou,
        "CheckParameterValid",
        f"// ST-FIX F49: {expr} was not checked\n"
        f"IF ( {cond} )\nTHEN\n"
        "  CheckParameterValid := FALSE;\n"
        f"  SetError( ErrorID := RobotLibraryErrorIdEnum.{error}, Overwrite := TRUE );\n"
        "  RETURN;\nEND_IF\n",
        f"F49: undefined values of {expr} were not rejected",
    )


_BLENDING = (
    "EXACT_STOP",
    "DEFINED_VELOCITY",
    "CORNER_DISTANCE",
    "MAX_CORNER_DEVIATION",
    "CORNER_DISTANCE_2R",
    "RAMP_OVERLAP",
    "CORNER_DISTANCE_1R",
)
_PROCESSING = (
    "BUFFERED",
    "ABORTING",
    "PARALLEL",
    "CONTINUOUS",
    "DEACTIVATE",
    "TRIGGER_BUFFERED",
    "TRIGGER_ABORTING",
    "TRIGGER_ONCE",
    "TRIGGER_CONTINUOUS",
    "TRIGGER_MULTIPLE",
)
_SEQUENCE = ("NO_SEQUENCE", "PRIMARY_SEQUENCE", "SECONDARY_SEQUENCE")
F49_CHECKS = (
    _enum_check(
        "MC_StopSubprogramFB", "ParCmd.SequenceFlag", "SequenceFlag", _SEQUENCE, "ERR_SEQFLAG_NOT_ALLOWED"
    ),
    _enum_check(
        "MC_MoveLinearRelativeFB",
        "ParCmd.ReferenceType",
        "ReferenceType",
        ("TOOL", "FRAME"),
        "ERR_INVALID_PAR_CMD",
    ),
    _enum_check(
        "MC_MovePickPlaceDirectFB", "ParCmd.BlendingMode", "BlendingMode", _BLENDING, "ERR_INVALID_PAR_CMD"
    ),
    _enum_check(
        "MC_MovePickPlaceLinearFB", "ParCmd.BlendingMode", "BlendingMode", _BLENDING, "ERR_INVALID_PAR_CMD"
    ),
    _enum_check(
        "MC_WriteAnalogOutputFB", "ParCmd.Unit", "UnitType", ("VOLT", "AMPERE"), "ERR_INVALID_PAR_CMD"
    ),
    _enum_check(
        "MC_CollisionDetectionFB",
        "ParCmd.ProcessingMode",
        "ProcessingMode",
        _PROCESSING,
        "ERR_PROCESSINGMODE_NOT_DEFINED",
    ),
    _enum_check(
        "MC_CollisionDetectionFB", "ParCmd.SequenceFlag", "SequenceFlag", _SEQUENCE, "ERR_SEQFLAG_NOT_ALLOWED"
    ),
)


CONFIG = Config(
    patches=[
        SourcePatch(
            "MC_MeasuringInputFB",
            "CheckParameterValid",
            "SetError( ErrorID := ErrorID := RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD",
            "SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD",
            "F12: duplicated 'ErrorID :=' in the argument list (assignment expression)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupSystemData",
            "AxesGroup.SystemData.FrameDataPtr      := LoadData;",
            "AxesGroup.SystemData.FrameDataPtr      := FrameData;",
            "F14: FrameData of the system data pointed to LoadData (copy & paste)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupSystemData",
            "AxesGroup.SystemData.FrameDataMin      := LOWER_BOUND  (LoadData,1)",
            "AxesGroup.SystemData.FrameDataMin      := LOWER_BOUND  (FrameData,1)",
            "F14: FrameData of the system data pointed to LoadData (copy & paste)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupSystemData",
            "AxesGroup.SystemData.FrameDataMax      := UPPER_BOUND  (LoadData,1)",
            "AxesGroup.SystemData.FrameDataMax      := UPPER_BOUND  (FrameData,1)",
            "F14: FrameData of the system data pointed to LoadData (copy & paste)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupSystemData",
            "AxesGroup.SystemData.WorkAreasPtr      := LoadData;",
            "AxesGroup.SystemData.WorkAreasPtr      := WorkAreas;",
            "F14: WorkAreas of the system data pointed to LoadData (copy & paste)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupSystemData",
            "AxesGroup.SystemData.WorkAreasMin      := LOWER_BOUND  (LoadData,1)",
            "AxesGroup.SystemData.WorkAreasMin      := LOWER_BOUND  (WorkAreas,1)",
            "F14: WorkAreas of the system data pointed to LoadData (copy & paste)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupSystemData",
            "AxesGroup.SystemData.WorkAreasMax      := UPPER_BOUND  (LoadData,1)",
            "AxesGroup.SystemData.WorkAreasMax      := UPPER_BOUND  (WorkAreas,1)",
            "F14: WorkAreas of the system data pointed to LoadData (copy & paste)",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupState",
            "RobotLibraryParameter.FRAME_MAX     )",
            "RobotLibraryParameter.FRAME_MAX - 1)",
            "F17: internal arrays are [0..FRAME_MAX-1], the unified index must not exceed FRAME_MAX-1",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupState",
            "RobotLibraryParameter.TOOL_MAX      )",
            "RobotLibraryParameter.TOOL_MAX - 1)",
            "F17: internal arrays are [0..TOOL_MAX-1], the unified index must not exceed TOOL_MAX-1",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupState",
            "RobotLibraryParameter.LOAD_MAX      )",
            "RobotLibraryParameter.LOAD_MAX - 1)",
            "F17: internal arrays are [0..LOAD_MAX-1], the unified index must not exceed LOAD_MAX-1",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleAxesGroupState",
            "RobotLibraryParameter.WORK_AREAS_MAX)",
            "RobotLibraryParameter.WORK_AREAS_MAX - 1)",
            "F17: internal arrays are [0..WORK_AREAS_MAX-1], the unified index must not exceed WORK_AREAS_MAX-1",
        ),
        SourcePatch(
            "ActiveCommandRegisterFB",
            "AddRsp",
            "FOR _idx := Rsp.Header.PayloadPointer TO  Rsp.Header.PayloadLength -1",
            "FOR _idx := Rsp.Header.PayloadPointer TO  Rsp.Header.PayloadPointer + Rsp.Header.PayloadLength -1",
            "F19: fragments after the first one (PayloadPointer > 0) were not copied into the response buffer",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "OnExecRun",
            "       Initialized := NOT Synchronized;\n",
            "       // ST-FIX F29: the next line overwrote the error check above\n"
            "       // Initialized := NOT Synchronized;\n",
            "F29: Initialized (and CMDsEnabled) became TRUE again after an error (init lost)",
        ),
        SourcePatch(
            "MC_ReadRobotDataFB",
            "ParseResponsePayload",
            "_response.InterpreterCycleTime := ResponseData.GetUsint();",
            "_response.InterpreterCycleTime := ResponseData.GetUint(); // ST-FIX F30",
            "F30: InterpreterCycleTime is UINT (spec table 6-18, SDK), read as USINT -> 0 / wrong value",
        ),
        SourcePatch(
            "MC_WriteRobotSWLimitsFB",
            "CreateCommandPayload",
            "// Create logging\nCreateCommandPayloadLog(AxesGroup := AxesGroup, ParameterCnt := _parameterCnt);",
            "// ST-FIX F31: ResetToFactoryDefaults (byte 106, spec table 6-209) was not sent\n"
            "IF ( CheckAddParameter(CreateCommandPayload.PayloadPtr))\n"
            "THEN\n"
            "  CreateCommandPayload.AddBool(_command.ResetToFactoryDefaults);\n"
            " _parameterCnt := _parameterCnt + 1;\n"
            "END_IF\n\n"
            "// Create logging\nCreateCommandPayloadLog(AxesGroup := AxesGroup, ParameterCnt := _parameterCnt);",
            "F31: WriteRobotSWLimits never sent ResetToFactoryDefaults",
        ),
        SourcePatch(
            "MC_MoveLinearAbsoluteJFB",
            "CreateCommandPayload",
            "_command.CmdTyp            :=  CmdType.MoveLinearAbsolute;",
            "_command.CmdTyp            :=  CmdType.MoveLinearAbsoluteJ; // ST-FIX F35",
            "F35: MoveLinearAbsoluteJ was sent as MoveLinearAbsolute (joint target read as Cartesian!)",
        ),
        SourcePatch(
            "MC_SoftSwitchTcpFB",
            "CreateCommandPayload",
            "_command.CmdTyp                    :=  CmdType.ShiftPosition;",
            "_command.CmdTyp                    :=  CmdType.SoftSwitchTcp; // ST-FIX F35",
            "F35: SoftSwitchTcp was sent as ShiftPosition",
        ),
        SourcePatch(
            "MC_SearchHardStopFB",
            "CheckParameterValid",
            "FOR _idx := 0 TO 6\nDO\n  // Check ParCmd.DetectionVector[x] valid ?",
            "FOR _idx := 0 TO 5 // ST-FIX F36\nDO\n  // Check ParCmd.DetectionVector[x] valid ?",
            "F36: loop 0..6 over DetectionVector[0..5] (reads behind the array)",
        ),
        SourcePatch(
            "MC_SearchHardStopJFB",
            "CheckParameterValid",
            "FOR _idx := 0 TO 6\nDO\n  // Check ParCmd.DetectionVector[x] valid ?",
            "FOR _idx := 0 TO 5 // ST-FIX F36\nDO\n  // Check ParCmd.DetectionVector[x] valid ?",
            "F36: loop 0..6 over DetectionVector[0..5] (reads behind the array)",
        ),
        *_bits_in_one_byte("MC_EnableRobotFB", "HoldToRun", "ManualStep", "6-25"),
        *_bits_in_one_byte("MC_MoveCircularRelativeFB", "PathChoice", "Manipulation", "6-357"),
        SourcePatch(
            "MC_ReturnToPrimaryFB",
            "CreateCommandPayload",
            "_command.MoveTime          :=  TIME_TO_UINT(_parCmd.MoveTime);",
            "_command.MoveTime          :=  TIME_TO_UINT(_parCmd.MoveTime);\n"
            "_command.AllowDifferences  :=  _parCmd.AllowDifferences; // ST-FIX F38",
            "F38: AllowDifferences was never copied into the command -> always sent as FALSE",
        ),
        SourcePatch(
            "RobotLibraryBaseFB",
            None,
            "OnExecRun            (AxesGroup := AxesGroup);\n",
            "OnExecRun            (AxesGroup := AxesGroup);\n"
            "// ST-FIX F53: no response of the RC within _timeoutCmd after the command was added\n"
            "// -> error (before: _timerCmd was started but never evaluated, the FB stayed Busy)\n"
            "IF ( _uniqueID <> 0 ) AND ( _rspHeader.State = CmdMessageState.EMPTY ) AND ( NOT Error )\n"
            "THEN\n"
            "  IF ( CheckTimeout( rTimer := _timerCmd ) = RobotLibraryConstants.OK )\n"
            "  THEN\n"
            "    AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd( UniqueID := _uniqueID );\n"
            "    SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite := TRUE );\n"
            "    OnUpdateStateFlags( State := CmdMessageState.ERROR );\n"
            "  END_IF\n"
            "END_IF\n",
            "F53: the command timeout was set but never evaluated",
        ),
        SourcePatch(
            "RobotLibraryBaseFB",
            "Reset",
            "_uniqueId := 0;",
            "_uniqueId := 0;\n_rspHeader.State := CmdMessageState.EMPTY; // ST-FIX F53: no response yet",
            "F53: response state of the last execution must not count for the next one",
        ),
        SourcePatch(
            "RobotLibraryBaseExecuteFB",
            None,
            "SUPER^(AxesGroup := AxesGroup);",
            '// ST-FIX F50: a falling edge of Execute must not cancel the command (spec 5.5.x "Output\n'
            '// status"): Execute is held internally while Busy; Done/Error/CommandAborted of a command\n'
            "// whose Execute is already FALSE are shown for one cycle, then the block resets\n"
            "_executeIn := Execute;\n"
            "Execute     := Execute OR _executeHold;\n"
            "SUPER^(AxesGroup := AxesGroup);\n"
            "_executeHold := Busy;\n"
            "Execute      := _executeIn;",
            "F50: a falling edge of Execute before the end cancelled the command / hid Done",
        ),
        *(_range_or(pou) for pou in F26_POUS),
        *F33_PATCHES,
        *F34_PATCHES,
        *SPLINE_PATCHES,
        *(
            SourcePatch(
                pou,
                "OnApplyOutCmd",
                r"IF \( State = CmdMessageState\.ACTIVE \)[ \t]*\n",
                "IF ( State = CmdMessageState.ACTIVE ) OR ( State = CmdMessageState.DONE ) // ST-FIX F40\n",
                "F40: OutCmd was only updated in state ACTIVE - the values of a response that is DONE at once were lost",
                regex=True,
            )
            for pou in ("MC_UnitMeasurementFB", "MC_SyncToConveyorFB")
        ),
        *(p for p in F32_PATCHES if isinstance(p, SourcePatch)),
        *(_exec_mode_from_aborting(pou) for pou in F51_ABORTING_POUS),
        *(_exec_mode_from_processing(pou, seq) for pou, seq in F51_PROCESSING_POUS),
        SourcePatch(
            "MC_OpenBrakeFB",
            "CreateCommandPayload",
            "CreateCommandPayload := SUPER^.CreateCommandPayload(AxesGroup := AxesGroup);",
            "CreateCommandPayload := SUPER^.CreateCommandPayload(AxesGroup := AxesGroup);\n"
            "// ST-FIX F42: byte 4 Enable (spec table of OpenBrake)\n"
            "CreateCommandPayload.AddBool(Enable);\n"
            "_parameterCnt := _parameterCnt + 1;",
            "F42: Enable byte of the OpenBrake command",
        ),
        SourcePatch(
            "MC_OpenBrakeFB",
            "ParseResponsePayload",
            "// Check payload remaining ? \nIF ( ResponseData.IsPayloadRemaining)\nTHEN\n  // Get RobotAxesStatus",
            "// ST-FIX F42: byte 4 Enabled\n"
            "IF ( ResponseData.IsPayloadRemaining)\nTHEN\n"
            " _response.Enabled := ResponseData.GetByte();\n"
            " _parameterCnt := _parameterCnt + 1;\nEND_IF\n\n"
            "// Check payload remaining ? \nIF ( ResponseData.IsPayloadRemaining)\nTHEN\n  // Get RobotAxesStatus",
            "F42: Enabled byte of the OpenBrake response",
        ),
        SourcePatch(
            "MC_OpenBrakeFB",
            "OnApplyOutCmd",
            "IF ( State = CmdMessageState.DONE ) ",
            "IF ( State = CmdMessageState.ACTIVE ) OR ( State = CmdMessageState.DONE ) // ST-FIX F42",
            "F42: the results of an enable block are updated while it is active",
        ),
        SourcePatch(
            "MC_FreeDriveFB",
            "OnUpdateStateFlags",
            "OutCmd.Enabled := _response.Enabled;",
            "OutCmd.Enabled := _response.Enabled;\nEnabled        := _response.Enabled; // ST-FIX F43",
            "F43: the output Enabled was never set",
        ),
        SourcePatch(
            "MC_ForceControlFB",
            "CheckParameterValid",
            "IF (( ParCmd.ErrorReaction <> ErrorReaction.ABORT       ) AND  \n"
            "    ( ParCmd.ErrorReaction <> ErrorReaction.NO_REACTION ))",
            "IF (( ParCmd.ErrorReaction <> ErrorReaction.ABORT_AND_MOVE ) AND // ST-FIX F44\n"
            "    ( ParCmd.ErrorReaction <> ErrorReaction.ABORT       ) AND  \n"
            "    ( ParCmd.ErrorReaction <> ErrorReaction.NO_REACTION ))",
            "F44: ErrorReaction 0 'Abort and move' (spec table 6-736, default) was rejected",
        ),
        SourcePatch(
            "MC_MoveSplineFB",
            "CheckParameterValid",
            "IF ( ParCmd.MoveTime <= T#0S ) ",
            "IF ( ParCmd.MoveTime < T#0S ) // ST-FIX F44: 0 = not used (default)",
            "F44: MoveTime 0 = 'not used' is the default (spec table 6-784), it was rejected",
        ),
        SourcePatch(
            "ActiveCommandRegisterFB",
            "AddCmd",
            "// calculate the used length of the ACR \n",
            "// ST-FIX F48: a command with a parameter error of the block is not added\n"
            "IF ( pCommandFB <> 0 )\nTHEN\n"
            "  IF (( pCommandFB^.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_EXECUTION_MODE ) OR\n"
            "      ( pCommandFB^.ErrorID = RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED   ))\n"
            "  THEN\n    AddCmd := 0;\n    RETURN;\n  END_IF\nEND_IF\n\n"
            "// calculate the used length of the ACR \n",
            "F48: undefined ExecutionMode was sent to the RC",
        ),
        SourcePatch(
            "MC_RobotTaskFB",
            "HandleSeqAck",
            "      AxesGroup.State.CurrentSEQ[_idx] := 0;",
            "      AxesGroup.State.CurrentSEQ[_idx] := 1; // ST-FIX F56: 0 only on the first exchange (spec 5.6.5.3)",
            "F56: the Seq number wrapped from 254 to 0; an Ack of 0 equals the Ack of the telegrams "
            "without new data -> the response of that sequence was ignored (command lost)",
        ),
        *_swap_no_and_data_changed("MC_ReadToolDataFB", "ToolData.ToolNoReturn", "ToolNoReturn", "6-190"),
        *_swap_no_and_data_changed("MC_ReadFrameDataFB", "FrameNoReturn", "FrameNoReturn", "6-184"),
    ],
    appends=[
        *F49_CHECKS,
        *(p for p in F45_OUTPUTS if isinstance(p, BodyAppend)),
        *SPLINE_APPENDS,
        *(p for p in F32_PATCHES if isinstance(p, BodyAppend)),
        *(_valid(pou) for pou in F25_POUS),
        BodyAppend(
            "RobotLibraryBaseFB",
            "CreateCommandPayload",
            "// ST-FIX F48: undefined ExecutionMode (spec table 5-75) -> error, not sent\n"
            "CASE _cmdHeader.ExecMode OF\n"
            "  ExecutionMode.SEQUENCE_PRIMARY, ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY,\n"
            "  ExecutionMode.PARALLEL, ExecutionMode.CONTINUOUS, ExecutionMode.TRIGGER_MULTIPLE,\n"
            "  ExecutionMode.SEQUENCE_SECONDARY, ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY,\n"
            "  ExecutionMode.STOP_PARALLEL_CONTINUOUS_TRIGGER: ;\n"
            "ELSE\n"
            "  SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_EXECUTION_MODE, Overwrite := TRUE );\n"
            "  OnUpdateStateFlags( State := CmdMessageState.ERROR );\n"
            "END_CASE\n",
            "F48: an undefined ExecMode was neither checked by the block nor rejected by the RC",
        ),
        BodyAppend(
            "MC_OpenBrakeFB",
            "OnApplyOutCmd",
            "// ST-FIX F42: output Enabled of the enable block\nEnabled := OutCmd.Enabled;\n",
            "F42: Enabled output of the enable block",
        ),
        *(
            BodyAppend(
                pou,
                "CheckAddParameter",
                "// ST-FIX F28: payload order differs from the structure layout -> always add the parameter\n"
                "CheckAddParameter := TRUE;\n",
                "F28: CheckAddParameter omits non-zero parameters when the payload order differs from _command",
            )
            for pou in F28_POUS
        ),
    ],
    variables=[
        *(p for p in F45_OUTPUTS if isinstance(p, VarAppend)),
        VarAppend(
            "MC_DynamicSplineFB",
            "VAR\n  _pointIndex : DINT := 1;\n  _pointCount : DINT;\n  _emptyPoint : SplineData;\nEND_VAR",
            "F33: one spline point per parameter update",
        ),
        VarAppend(
            "MC_CreateSplineFB",
            "VAR\n  _pointIndex : DINT := 1;\n  _pointCount : DINT;\n  _emptyPoint : SplineData;\nEND_VAR",
            "F33: one command per spline point",
        ),
        VarAppend(
            "MC_ReadDHParameterFB",
            "VAR\n  _directionBits : BYTE;\nEND_VAR",
            "F33: bits of PositiveJointDirection",
        ),
        VarAppend(
            "RobotLibraryBaseExecuteFB",
            "VAR\n  _executeIn : BOOL;\n  _executeHold : BOOL;\nEND_VAR",
            "F50: Execute of the caller and internal hold of Execute while Busy",
        ),
    ],
    clones=[
        PouClone(
            "MC_OpenBrakeFB",
            "MC_FreeDriveFB",
            (
                ("MC_FreeDriveFB", "MC_OpenBrakeFB"),
                ("Move the robot axes by hand", "Release robot arm's brakes (Enable block, ST-FIX F42)"),
                ("FreeDriveParCmd", "OpenBrakeParCmd"),
                ("FreeDriveOutCmd", "OpenBrakeOutCmd"),
                ("FreeDriveSendData", "OpenBrakeSendData"),
                ("FreeDriveRecvData", "OpenBrakeRecvData"),
                ("OutCmd.Enabled := _response.Enabled;", "// Enabled: see OnApplyOutCmd (ST-FIX F42)"),
            ),
            "F42: OpenBrake is an Enable block in the spec (brakes open while Enable), the ST block "
            "was an Execute block; state machine of MC_FreeDriveFB, payload of MC_OpenBrakeFB",
            keep_methods=(
                "CheckFunctionSupported",
                "FB_init",
                "CheckParameterValid",
                "CheckParameterChanged",
                "CreateCommandPayload",
                "CreateCommandPayloadLog",
                "OnApplyOutCmd",
                "ParseResponsePayload",
                "ParseResponsePayloadLog",
            ),
        ),
        PouClone(
            "MC_DynamicSplineFB",
            "MC_FreeDriveFB",
            (
                ("MC_FreeDriveFB", "MC_DynamicSplineFB"),
                ("FreeDriveParCmd", "DynamicSplineParCmd"),
                ("FreeDriveOutCmd", "DynamicSplineOutCmd"),
                ("FreeDriveSendData", "DynamicSplineSendData"),
                ("FreeDriveRecvData", "DynamicSplineRecvData"),
                (
                    "OutCmd.Enabled := _response.Enabled;",
                    "// ST-FIX F33/F45: enable block, spline points are sent one by one\n"
                    "Enabled := ( State = CmdMessageState.ACTIVE ) OR ( State = CmdMessageState.BUFFERED );\n"
                    "Active  := ( State = CmdMessageState.ACTIVE );\n"
                    "// next spline point (the point after the last one is empty: end of the trajectory)\n"
                    "IF ( _response.ParSeq = _command.ParSeq ) AND ( _pointIndex <= _pointCount ) AND\n"
                    "   ( _pointIndex < RobotLibraryParameter.SPLINE_DATA_MAX ) AND\n"
                    "   (( State = CmdMessageState.ACTIVE ) OR ( State = CmdMessageState.BUFFERED ))\nTHEN\n"
                    "  _pointIndex := _pointIndex + 1;\n"
                    "  _parameterUpdateInternal := TRUE;\n"
                    "END_IF",
                ),
                ("_command.ParSeq := 1;", "_command.ParSeq := 1;\n_pointIndex := 1;"),
            ),
            "F33/F45: DynamicSpline is an Enable block in the spec that transmits one spline point per "
            "parameter update (ParSeq); the ST block sent all points in one payload (> 255 bytes) "
            "with Execute; state machine of MC_FreeDriveFB, payload of MC_DynamicSplineFB",
            keep_methods=(
                "CheckFunctionSupported",
                "FB_init",
                "CheckParameterValid",
                "CreateCommandPayload",
                "CreateCommandPayloadLog",
                "OnApplyOutCmd",
                "ParseResponsePayload",
                "ParseResponsePayloadLog",
            ),
            target_decl=(
                ("EXTENDS RobotLibraryBaseFB", "EXTENDS RobotLibraryBaseEnableFB"),
                ("  /// Start of the command at the rising edge\n  Execute            : BOOL;\n", ""),
                ("  /// FB is being processed\n  Busy               : BOOL;\n", ""),
                (
                    "  /// Function is enabled and new input values will be transmitted.\n  Enabled            : BOOL;\n",
                    "",
                ),
            ),
        ),
    ],
    mixins={
        "MC_RobotTaskFB": Mixin(
            "srci.fb.General.MC_RobotTask.MC_RobotTaskFB_Telegram",
            "MC_RobotTaskFB_Telegram",
            (
                "CreateSendPayload",
                "CreateSendPayloadHeader",
                "CreateSendPayloadCyclic",
                "CreateSendPayloadCyclicOptional",
                "CreateSendPayloadSequence",
                "CreateSendPayloadFooter",
                "CreateSendPayloadLogging",
                "ParseRecvPayload",
                "ParseRecvPayloadHeader",
                "ParseRecvPayloadCyclic",
                "ParseRecvPayloadCyclicOptional",
                "ParseRecvPayloadSequence",
                "ParseRecvPayloadFooter",
                "ParseRecvPayloadLogging",
                "CalculateCyclicDataLength",
                "CalculateSequencePayloadMax",
                "CalculateSequencePayloadStartAdr",
                "CalculateTelegramLengthPlcToRob",
            ),
            "telegram coding with ST-FIX F1, F2, F5 (hand ported in M2)",
        ),
    },
)
