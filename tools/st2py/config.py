# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.config
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Documented deviations of the transpiled code from the ST source.
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

"""Documented deviations of the transpiled code from the ST source.

Every entry names its reason (and the finding in docs/ST_FINDINGS.md). Source patches
fail when the ST text no longer contains the old text, so obsolete patches get noticed.

Since the export of 2026-10-17 the PLC library contains all fixes F1 ... F103: no source patch is
left (the patches of F1 ... F103 are in the git history, see docs/ST_FINDINGS.md). New findings
are added here again as ``SourcePatch`` until they are in the PLC library.
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


# F28: CheckAddParameter omits a parameter when the bytes of the command structure behind the
# payload position are zero. That only works when the payload has the order of the structure;
# for these function blocks it has not (e.g. ToolNo is the last parameter of WriteToolData but
# the first element of the structure) -> non-zero parameters are omitted. Python always sends
# the complete payload (fixed in the PLC library).
# tests/unit/tools/test_st2py_f28.py checks this list against the code.
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


# ---------------------------------------------------------------- findings after the export of 2026-10-17

_F104 = (
    "F104: a CONTINUOUS / triggered command could not be ended - F50 holds Execute while Busy, so the "
    "new rising edge with ProcessingMode DEACTIVATE never reached the block; now the edge of the "
    "Execute input while Busy sends the same command again with execution mode Stop (spec 5.5.12.4, "
    "5.6.4.5, table 5-77)"
)
_F104_POUS = (
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
    "MC_WriteWorkAreaFB",
)
_F104_STEP1 = (
    "\\1\n       // ST-FIX F104: ProcessingMode DEACTIVATE + new rising edge of Execute while the command runs\n"
    "       // (continuous / triggered): the same command again with execution mode Stop, the RC ends it with DONE\n"
    "       IF ( _executeRestart_R.Q ) AND ( ProcessingMode = ProcessingModeEnum.DEACTIVATE )\n"
    "       THEN\n"
    "         // inc parameter sequence\n"
    "        _command.ParSeq := _command.ParSeq + 1;\n"
    "         // update command data (execution mode Stop)\n"
    "         CommandData := CreateCommandPayload(AxesGroup := AxesGroup);\n"
    "         // notify active command register\n"
    "         AxesGroup.Acyclic.ActiveCommandRegister.NotifyParameterChanged := _uniqueID;\n"
    "       END_IF\n"
    "      "
)
_F105 = (
    "F105: the user defined command name (Name) was not part of the message in the message buffer "
    "(spec 5.5.11, table 5-47)"
)
_F106 = (
    "F106: an error response has no payload (only the header) - Enabled kept the value of the last "
    "response (e.g. power switched off by the RC: Error and Enabled TRUE at the same time)"
)
_F106_POUS = (
    "MC_ActivateConveyorTrackingFB",
    "MC_AvoidSingularityFB",
    "MC_EnableRobotFB",
    "MC_ExchangeConfigurationFB",
    "MC_ForceControlFB",
    "MC_ForceLimitFB",
    "MC_FreeDriveFB",
    "MC_GroupJogFB",
    "MC_PathAccuracyModeFB",
    "MC_ReadMessagesFB",
)

_F107 = (
    "F107: AUTOMATIC - PLC data changed while the client read the data changed on the RC were "
    "overwritten with the older RC data (and written back to the RC): the newer PLC change was lost "
    "(spec 5.6.7.2 'Automatic': the most recently changed data win)"
)
# method, item of SynchronizationModes, compare function, PLC data, internal copy
_F107_SETS = (
    (
        "HandleSyncToolData",
        "Tool",
        "IsToolDataEqual",
        "ToolData[_rSyncIdx].Data",
        "_toolData[_rSyncIdx].Data",
    ),
    (
        "HandleSyncFrameData",
        "Frame",
        "IsFrameDataEqual",
        "FrameData[_rSyncIdx].Data",
        "_frameData[_rSyncIdx].Data",
    ),
    (
        "HandleSyncLoadData",
        "Load",
        "IsLoadDataEqual",
        "LoadData[_rSyncIdx].Data",
        "_loadData[_rSyncIdx].Data",
    ),
    (
        "HandleSyncWorkArea",
        "WorkAreas",
        "IsWorkAreaEqual",
        "WorkAreas[_rSyncIdx].Data",
        "_workAreas[_rSyncIdx].Data",
    ),
    ("HandleSyncRobotSWLimits", "SWLimits", "IsSwLimitsEqual", "SwLimits", "_swLimits"),
    (
        "HandleSyncRobotDefaultDynamics",
        "DefaultDynamics",
        "IsDefaultDynamicsEqual",
        "DefaultDynamics",
        "_defaultDynamics",
    ),
    (
        "HandleSyncRobotReferenceDynamics",
        "ReferenceDynamics",
        "IsReferenceDynamicsEqual",
        "ReferenceDynamics",
        "_referenceDynamics",
    ),
)


def _f107(item: str, compare: str, plc: str, internal: str) -> str:
    return (
        "\\1"
        "         // ST-FIX F107: AUTOMATIC - the PLC data were changed while the RC data were read: the PLC\n"
        "         // change is the most recent one and is written to the RC instead of being overwritten\n"
        f"         IF ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.{item}[SyncTime.AFTER_START_UP] = SyncMode.AUTOMATIC ) AND\n"
        f"            ( NOT {compare}( Data1 := {plc}, Data2 := {internal}, IgnoreTimestamp := TRUE ))\n"
        "         THEN\n"
        "           // set timeout\n"
        "           SetTimeout(PT := _rTimeout, rTimer := _rTimer);\n"
        "           // -> write PLC data to RC\n"
        "          _rStep := 30;\n"
        "           RETURN;\n"
        "         END_IF\n"
    )


_PATCHES_AFTER_EXPORT = [
    SourcePatch(
        "RobotLibraryBaseExecuteFB",
        None,
        "_executeIn := Execute;\n",
        "_executeIn := Execute;\n"
        "// ST-FIX F104: rising edge of the Execute input also while Busy (Execute is held, F50)\n"
        "_executeRestart_R(CLK := Execute);\n",
        _F104,
    ),
    *(
        SourcePatch(pou, "OnExecRun", r"(\n[ \t]*01:)", _F104_STEP1, _F104, regex=True, template=True)
        for pou in _F104_POUS
    ),
    SourcePatch(
        "RobotLibraryBaseFB",
        "OnCall",
        "// ST-FIX F74: every message of the command",
        "// ST-FIX F105: the user defined command name belongs into the message text (spec 5.5.11,\n"
        '// table 5-47 "[Robot] [Client] [MoveLinAbs] [MoveToP1] [text]")\n'
        "_messageSource := MyType;\n"
        "IF ( Name <> '' )\n"
        "THEN\n"
        "  _messageSource := CONCAT(MyType, CONCAT(' [', CONCAT(Name, ']')));\n"
        "END_IF\n"
        "\n"
        "// ST-FIX F74: every message of the command",
        _F105,
    ),
    *(
        SourcePatch(
            "RobotLibraryBaseFB",
            "OnCall",
            f"_alarmMessage.MessageText := CONCAT(MyType, CONCAT(' : ', MESSAGE_CODE_TO_STRING({code})));",
            f"_alarmMessage.MessageText := CONCAT(_messageSource, CONCAT(' : ', MESSAGE_CODE_TO_STRING({code}))); // ST-FIX F105",
            _F105,
        )
        for code in ("ErrorID", "WarningID", "InfoID")
    ),
    *(
        SourcePatch(
            pou,
            "OnUpdateStateFlags",
            r"(CmdMessageState\.ERROR\s*:\s*Error\s*:= TRUE;\s*Busy\s*:= FALSE;)",
            "\\1\n                                        // ST-FIX F106: error response without payload\n"
            "                                        Enabled            := FALSE;",
            _F106,
            regex=True,
            template=True,
        )
        for pou in _F106_POUS
    ),
    *(
        SourcePatch(
            "MC_RobotTaskFB",
            method,
            r"(?s)(\n[ \t]*21 : IF \(\( NOT _read\w+\.Busy.*?_read\w+\.Execute := FALSE;[^\n]*\n)",
            _f107(item, compare, plc, internal),
            _F107,
            regex=True,
            template=True,
        )
        for method, item, compare, plc, internal in _F107_SETS
    ),
    SourcePatch(
        "MC_EnableRobotFB",
        "OnUpdateStateFlags",
        "CmdMessageState.ABORTED             : Busy               := FALSE;",
        "CmdMessageState.ABORTED             : Busy               := FALSE;\n"
        "                                        Enabled            := FALSE; // ST-FIX F106",
        _F106,
    ),
]

_VARIABLES_AFTER_EXPORT = [
    VarAppend(
        "RobotLibraryBaseExecuteFB",
        "VAR\n  /// ST-FIX F104: rising edge of the Execute input (also while Busy)\n  _executeRestart_R : R_TRIG;\nEND_VAR",
        _F104,
    ),
    VarAppend(
        "RobotLibraryBaseFB",
        "VAR\n  /// ST-FIX F105: block type and command name for the messages\n  _messageSource : STRING;\nEND_VAR",
        _F105,
    ),
]


CONFIG = Config(
    patches=_PATCHES_AFTER_EXPORT,
    variables=_VARIABLES_AFTER_EXPORT,
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
