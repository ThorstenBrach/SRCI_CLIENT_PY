"""Documented deviations of the transpiled code from the ST source.

Every entry names its reason (and the finding in docs/ST_FINDINGS.md). Source patches
fail when the ST text no longer contains the old text, so obsolete patches get noticed.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourcePatch:
    pou: str
    method: str | None  # None: body of the POU
    old: str
    new: str
    reason: str
    regex: bool = False  # old is a regular expression (must match at least once)


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
        "  _command.ExecMode := ExecMode;\n"
        "END_CASE",
        "F51: ProcessingMode/SequenceFlag had no effect on the ExecutionMode of the telegram",
        regex=True,
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
        *(_exec_mode_from_aborting(pou) for pou in F51_ABORTING_POUS),
        *(_exec_mode_from_processing(pou, seq) for pou, seq in F51_PROCESSING_POUS),
        *_swap_no_and_data_changed("MC_ReadToolDataFB", "ToolData.ToolNoReturn", "ToolNoReturn", "6-190"),
        *_swap_no_and_data_changed("MC_ReadFrameDataFB", "FrameNoReturn", "FrameNoReturn", "6-184"),
    ],
    appends=[
        BodyAppend(
            pou,
            "CheckAddParameter",
            "// ST-FIX F28: payload order differs from the structure layout -> always add the parameter\n"
            "CheckAddParameter := TRUE;\n",
            "F28: CheckAddParameter omits non-zero parameters when the payload order differs from _command",
        )
        for pou in F28_POUS
    ],
    variables=[
        VarAppend(
            "RobotLibraryBaseExecuteFB",
            "VAR\n  _executeIn : BOOL;\n  _executeHold : BOOL;\nEND_VAR",
            "F50: Execute of the caller and internal hold of Execute while Busy",
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
