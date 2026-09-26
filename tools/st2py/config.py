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
    mixins: dict[str, Mixin] = field(default_factory=dict)  # POU name -> mixin

    @property
    def hand_methods(self) -> dict[str, dict[str, Mixin]]:
        return {pou: {m.upper(): mix for m in mix.methods} for pou, mix in self.mixins.items()}


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
