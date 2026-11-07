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

Since the export of 2026-10-23 (library 1.5.2 + CreateServerLog / ReadServerLog, F108) the PLC
library contains all fixes F1 ... F108: no source patch is left (the patches are in the git
history, see docs/ST_FINDINGS.md). New findings are added here again as ``SourcePatch`` until they
are in the PLC library.
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
    "MC_MoveDirectCamFB",  # F109: new block, template MoveLinearCam
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
    "MC_SafeReferencingFB",  # F109: new block
    "MC_WriteIntegersFB",
    "MC_WriteLoadDataFB",
    "MC_WriteRealsFB",
    "MC_WriteRobotSWLimitsFB",
    "MC_WriteToolDataFB",
    "MC_WriteWorkAreaFB",
)


CONFIG = Config(
    patches=[
        # F153: at the start of a RobotTask no telegram has been read yet, so the check of F23 sees
        # TelegramState UNDEFINED. An RC that is still INITIALIZED from the previous connection is
        # taken as initialized without a reset; the RC drops to READY_FOR_INITIALIZATION a moment
        # later and the start-up ends with ERR_TIMEOUT_CMD. INITIALIZED while no control request
        # is pending can only come from an earlier connection -> reset the interface first.
        SourcePatch(
            "MC_RobotTaskFB",
            "OnExecRun",
            "// ST-FIX F23: wait until the RC left the state INITIALIZED of the previous enable",
            "// ST-FIX F153: INITIALIZED without a request of this RobotTask: the RC is still\n"
            "// initialized from an earlier connection -> reset the interface on the RC first\n"
            "IF ( AxesGroup.Cyclic.RobToPlc.TelegramState = TelegramState.INITIALIZED )\n"
            "AND ( AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.NONE )\n"
            "AND ( NOT _restartReset )\n"
            "THEN\n"
            "  AxesGroup.Cyclic.PlcToRob.Control := ControlHalfByte.RESET;\n"
            "  _restartReset := TRUE;\n"
            "END_IF\n\n"
            "// ST-FIX F23: wait until the RC left the state INITIALIZED of the previous enable",
            "F153: restart with an RC that is still initialized",
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
