"""SRCI structures - generated from the PLC library, DO NOT EDIT.

Source: third_party/robotlibrary/RobotLibrary.xml (sha256 6d064f48fb9cb9c5)
Regenerate with ``python -m tools.plcopen_gen``.
"""
# ruff: noqa
# fmt: off
from __future__ import annotations

from dataclasses import dataclass as _dataclass, field as _field
from typing import TYPE_CHECKING, Any, ClassVar

from srci.types import iec as _iec
from srci.types._generated import enums as _e

if TYPE_CHECKING:
    from srci.types._generated import structs as _s
else:  # self reference for annotations that clash with field names
    import sys as _sys

    _s = _sys.modules[__name__]

__all__ = [
    'AbortMeasuringInputOutCmd',
    'AbortMeasuringInputParCmd',
    'AbortMeasuringInputRecvData',
    'AbortMeasuringInputSendData',
    'ActivateConveyorTrackingOutCmd',
    'ActivateConveyorTrackingParCmd',
    'ActivateConveyorTrackingRecvData',
    'ActivateConveyorTrackingSendData',
    'ActivateNextCommandOutCmd',
    'ActivateNextCommandParCmd',
    'ActivateNextCommandRecvData',
    'ActivateNextCommandSendData',
    'ActivateWorkAreaOutCmd',
    'ActivateWorkAreaParCmd',
    'ActivateWorkAreaRecvData',
    'ActivateWorkAreaSendData',
    'AlarmMessage',
    'ArmConfigParameter',
    'AuxOffset',
    'AvoidSingularityOutCmd',
    'AvoidSingularityParCmd',
    'AvoidSingularityRecvData',
    'AvoidSingularitySendData',
    'AxesGroup',
    'AxesGroupAcyclic',
    'AxesGroupAcyclicAcrEntry',
    'AxesGroupAcyclicAcrEntryCmdBuffer',
    'AxesGroupAcyclicAcrEntryRspBuffer',
    'AxesGroupAcyclicExecutionOrderList',
    'AxesGroupCyclic',
    'AxesGroupCyclicOptionalData',
    'AxesGroupCyclicOptionalDataCartesianPosition',
    'AxesGroupCyclicOptionalDataCartesianPositionExt',
    'AxesGroupCyclicOptionalDataCurrent',
    'AxesGroupCyclicOptionalDataCurrentExt',
    'AxesGroupCyclicOptionalDataForce',
    'AxesGroupCyclicOptionalDataForceExt',
    'AxesGroupCyclicOptionalDataJointPosition',
    'AxesGroupCyclicOptionalDataJointPositionExt',
    'AxesGroupCyclicOptionalDataPlcToRob',
    'AxesGroupCyclicOptionalDataRobToPlc',
    'AxesGroupCyclicOptionalDataSubProgram',
    'AxesGroupCyclicPlcToRob',
    'AxesGroupCyclicRobToPlc',
    'AxesGroupMessageLog',
    'AxesGroupParameter',
    'AxesGroupParameterOptionalCyclic',
    'AxesGroupParameterOptionalCyclicPlcToRob',
    'AxesGroupParameterOptionalCyclicRobToPlc',
    'AxesGroupParameterPlc',
    'AxesGroupParameterPlcOptionalCyclic',
    'AxesGroupParameterPlcParameter',
    'AxesGroupParameterRob',
    'AxesGroupParameterRobOptionalCyclic',
    'AxesGroupParameterRobParameter',
    'AxesGroupState',
    'AxesGroupStateDataChanged',
    'AxesGroupStateSyncState',
    'AxesGroupStateSyncStateNo',
    'AxesGroupStateSyncStatePlc',
    'AxesGroupStateSyncStateRob',
    'AxesGroupStateSynchronizing',
    'AxisExternalUnit',
    'AxisExternalUsed',
    'AxisJointUnit',
    'AxisJointUsed',
    'BrakeTestOutCmd',
    'BrakeTestParCmd',
    'BrakeTestRecvData',
    'BrakeTestSendData',
    'CalculateCartesianPositionOutCmd',
    'CalculateCartesianPositionParCmd',
    'CalculateCartesianPositionRecvData',
    'CalculateCartesianPositionSendData',
    'CalculateForwardKinematicOutCmd',
    'CalculateForwardKinematicParCmd',
    'CalculateForwardKinematicRecvData',
    'CalculateForwardKinematicSendData',
    'CalculateFrameOutCmd',
    'CalculateFrameParCmd',
    'CalculateFrameRecvData',
    'CalculateFrameSendData',
    'CalculateInverseKinematicOutCmd',
    'CalculateInverseKinematicParCmd',
    'CalculateInverseKinematicRecvData',
    'CalculateInverseKinematicSendData',
    'CalculateToolOutCmd',
    'CalculateToolParCmd',
    'CalculateToolRecvData',
    'CalculateToolSendData',
    'CallSubprogramOutCmd',
    'CallSubprogramParCmd',
    'CallSubprogramRecvData',
    'CallSubprogramSendData',
    'ChangeSpeedOverrideOutCmd',
    'ChangeSpeedOverrideParCmd',
    'ChangeSpeedOverrideRecvData',
    'ChangeSpeedOverrideSendData',
    'CmdHeader',
    'CollisionDetectionOutCmd',
    'CollisionDetectionParCmd',
    'CollisionDetectionRecvData',
    'CollisionDetectionSendData',
    'ConfigureConveyorOutCmd',
    'ConfigureConveyorParCmd',
    'ConfigureConveyorRecvData',
    'ConfigureConveyorSendData',
    'CoordinateSystem',
    'CreateSplineOutCmd',
    'CreateSplineParCmd',
    'CreateSplineRecvData',
    'CreateSplineSendData',
    'CyclicStateData',
    'DHParameter',
    'DataEnableSync',
    'DataInSync',
    'DefaultDynamics',
    'DeleteSplineOutCmd',
    'DeleteSplineParCmd',
    'DeleteSplineRecvData',
    'DeleteSplineSendData',
    'DynamicSplineOutCmd',
    'DynamicSplineParCmd',
    'DynamicSplineRecvData',
    'DynamicSplineSendData',
    'EnableRobotOutCmd',
    'EnableRobotParCmd',
    'EnableRobotRecvData',
    'EnableRobotSendData',
    'ExchangeConfigurationOutCmd',
    'ExchangeConfigurationParCmd',
    'ExchangeConfigurationRecvData',
    'ExchangeConfigurationSendData',
    'ExecutionModeAllowed',
    'ExternalAxesFlags',
    'ForceControlOutCmd',
    'ForceControlParCmd',
    'ForceControlRecvData',
    'ForceControlSendData',
    'ForceLimitOutCmd',
    'ForceLimitParCmd',
    'ForceLimitRecvData',
    'ForceLimitSendData',
    'ForceStatus',
    'FragmentAction',
    'Frame',
    'FrameData',
    'FreeDriveOutCmd',
    'FreeDriveParCmd',
    'FreeDriveRecvData',
    'FreeDriveSendData',
    'GroupContinueOutCmd',
    'GroupContinueParCmd',
    'GroupContinueRecvData',
    'GroupContinueSendData',
    'GroupInterruptOutCmd',
    'GroupInterruptParCmd',
    'GroupInterruptRecvData',
    'GroupInterruptSendData',
    'GroupJogOutCmd',
    'GroupJogParCmd',
    'GroupJogRecvData',
    'GroupJogSendData',
    'GroupResetOutCmd',
    'GroupResetParCmd',
    'GroupResetRecvData',
    'GroupResetSendData',
    'GroupStopOutCmd',
    'GroupStopParCmd',
    'GroupStopRecvData',
    'GroupStopSendData',
    'IEC_TIMESTAMP',
    'JogControl',
    'Load',
    'LoadData',
    'LoadMeasurementAutomaticOutCmd',
    'LoadMeasurementAutomaticParCmd',
    'LoadMeasurementAutomaticRecvData',
    'LoadMeasurementAutomaticSendData',
    'LoadMeasurementSequentialOutCmd',
    'LoadMeasurementSequentialParCmd',
    'LoadMeasurementSequentialRecvData',
    'LoadMeasurementSequentialSendData',
    'LogParameter',
    'MeasuringInputOutCmd',
    'MeasuringInputParCmd',
    'MeasuringInputRecvData',
    'MeasuringInputResult',
    'MeasuringInputSendData',
    'MonitorWorkAreaOutCmd',
    'MonitorWorkAreaParCmd',
    'MonitorWorkAreaRecvData',
    'MonitorWorkAreaSendData',
    'MoveApproachDirectOutCmd',
    'MoveApproachDirectParCmd',
    'MoveApproachDirectRecvData',
    'MoveApproachDirectSendData',
    'MoveApproachLinearOutCmd',
    'MoveApproachLinearParCmd',
    'MoveApproachLinearRecvData',
    'MoveApproachLinearSendData',
    'MoveAxesAbsoluteOutCmd',
    'MoveAxesAbsoluteParCmd',
    'MoveAxesAbsoluteRecvData',
    'MoveAxesAbsoluteSendData',
    'MoveAxesRelativeOutCmd',
    'MoveAxesRelativeParCmd',
    'MoveAxesRelativeRecvData',
    'MoveAxesRelativeSendData',
    'MoveCircularAbsoluteOutCmd',
    'MoveCircularAbsoluteParCmd',
    'MoveCircularAbsoluteRecvData',
    'MoveCircularAbsoluteSendData',
    'MoveCircularCamOutCmd',
    'MoveCircularCamParCmd',
    'MoveCircularCamRecvData',
    'MoveCircularCamSendData',
    'MoveCircularRelativeOutCmd',
    'MoveCircularRelativeParCmd',
    'MoveCircularRelativeRecvData',
    'MoveCircularRelativeSendData',
    'MoveDepartDirectOutCmd',
    'MoveDepartDirectParCmd',
    'MoveDepartDirectRecvData',
    'MoveDepartDirectSendData',
    'MoveDepartLinearOutCmd',
    'MoveDepartLinearParCmd',
    'MoveDepartLinearRecvData',
    'MoveDepartLinearSendData',
    'MoveDirectAbsoluteOutCmd',
    'MoveDirectAbsoluteParCmd',
    'MoveDirectAbsoluteRecvData',
    'MoveDirectAbsoluteSendData',
    'MoveDirectOffsetOutCmd',
    'MoveDirectOffsetParCmd',
    'MoveDirectOffsetRecvData',
    'MoveDirectOffsetSendData',
    'MoveDirectRelativeOutCmd',
    'MoveDirectRelativeParCmd',
    'MoveDirectRelativeRecvData',
    'MoveDirectRelativeSendData',
    'MoveLinearAbsoluteJOutCmd',
    'MoveLinearAbsoluteJParCmd',
    'MoveLinearAbsoluteJRecvData',
    'MoveLinearAbsoluteJSendData',
    'MoveLinearAbsoluteOutCmd',
    'MoveLinearAbsoluteParCmd',
    'MoveLinearAbsoluteRecvData',
    'MoveLinearAbsoluteSendData',
    'MoveLinearCamOutCmd',
    'MoveLinearCamParCmd',
    'MoveLinearCamRecvData',
    'MoveLinearCamSendData',
    'MoveLinearOffsetOutCmd',
    'MoveLinearOffsetParCmd',
    'MoveLinearOffsetRecvData',
    'MoveLinearOffsetSendData',
    'MoveLinearRelativeOutCmd',
    'MoveLinearRelativeParCmd',
    'MoveLinearRelativeRecvData',
    'MoveLinearRelativeSendData',
    'MovePickPlaceDirectOutCmd',
    'MovePickPlaceDirectParCmd',
    'MovePickPlaceDirectRecvData',
    'MovePickPlaceDirectSendData',
    'MovePickPlaceLinearOutCmd',
    'MovePickPlaceLinearParCmd',
    'MovePickPlaceLinearRecvData',
    'MovePickPlaceLinearSendData',
    'MoveSplineOutCmd',
    'MoveSplineParCmd',
    'MoveSplineRecvData',
    'MoveSplineSendData',
    'MoveSuperImposedDynamicOutCmd',
    'MoveSuperImposedDynamicParCmd',
    'MoveSuperImposedDynamicRecvData',
    'MoveSuperImposedDynamicSendData',
    'MoveSuperImposedOutCmd',
    'MoveSuperImposedParCmd',
    'MoveSuperImposedRecvData',
    'MoveSuperImposedSendData',
    'OpenBrakeOutCmd',
    'OpenBrakeParCmd',
    'OpenBrakeRecvData',
    'OpenBrakeSendData',
    'PathAccuracyModeOutCmd',
    'PathAccuracyModeParCmd',
    'PathAccuracyModeRecvData',
    'PathAccuracyModeSendData',
    'ProcessingModeAllowed',
    'RCSupportedFunctions',
    'RaStatusWord',
    'ReactAtTriggerOutCmd',
    'ReactAtTriggerParCmd',
    'ReactAtTriggerRecvData',
    'ReactAtTriggerSendData',
    'ReadActualForceOutCmd',
    'ReadActualForceParCmd',
    'ReadActualForceRecvData',
    'ReadActualForceSendData',
    'ReadActualPositionCyclicOutCmd',
    'ReadActualPositionCyclicParCmd',
    'ReadActualPositionOutCmd',
    'ReadActualPositionParCmd',
    'ReadActualPositionRecvData',
    'ReadActualPositionSendData',
    'ReadActualTCPVelocityOutCmd',
    'ReadActualTCPVelocityParCmd',
    'ReadActualTCPVelocityRecvData',
    'ReadActualTCPVelocitySendData',
    'ReadAnalogInputOutCmd',
    'ReadAnalogInputParCmd',
    'ReadAnalogInputRecvData',
    'ReadAnalogInputSendData',
    'ReadCallSubprogramCyclicOutCmd',
    'ReadCallSubprogramCyclicParCmd',
    'ReadDHParameterOutCmd',
    'ReadDHParameterParCmd',
    'ReadDHParameterRecvData',
    'ReadDHParameterSendData',
    'ReadDigitalInputsOutCmd',
    'ReadDigitalInputsParCmd',
    'ReadDigitalInputsRecvData',
    'ReadDigitalInputsSendData',
    'ReadDigitalOutputsOutCmd',
    'ReadDigitalOutputsParCmd',
    'ReadDigitalOutputsRecvData',
    'ReadDigitalOutputsSendData',
    'ReadFrameDataOutCmd',
    'ReadFrameDataParCmd',
    'ReadFrameDataRecvData',
    'ReadFrameDataSendData',
    'ReadIntegersOutCmd',
    'ReadIntegersParCmd',
    'ReadIntegersRecvData',
    'ReadIntegersSendData',
    'ReadLoadDataOutCmd',
    'ReadLoadDataParCmd',
    'ReadLoadDataRecvData',
    'ReadLoadDataSendData',
    'ReadMessagesOutCmd',
    'ReadMessagesParCmd',
    'ReadMessagesRecvData',
    'ReadMessagesSendData',
    'ReadRealsOutCmd',
    'ReadRealsParCmd',
    'ReadRealsRecvData',
    'ReadRealsSendData',
    'ReadRobotDataOutCmd',
    'ReadRobotDataParCmd',
    'ReadRobotDataRecvData',
    'ReadRobotDataSendData',
    'ReadRobotDefaultDynamicsOutCmd',
    'ReadRobotDefaultDynamicsParCmd',
    'ReadRobotDefaultDynamicsRecvData',
    'ReadRobotDefaultDynamicsSendData',
    'ReadRobotReferenceDynamicsOutCmd',
    'ReadRobotReferenceDynamicsParCmd',
    'ReadRobotReferenceDynamicsRecvData',
    'ReadRobotReferenceDynamicsSendData',
    'ReadRobotSWLimitsOutCmd',
    'ReadRobotSWLimitsParCmd',
    'ReadRobotSWLimitsRecvData',
    'ReadRobotSWLimitsSendData',
    'ReadSystemVariableOutCmd',
    'ReadSystemVariableParCmd',
    'ReadSystemVariableRecvData',
    'ReadSystemVariableSendData',
    'ReadToolDataOutCmd',
    'ReadToolDataParCmd',
    'ReadToolDataRecvData',
    'ReadToolDataSendData',
    'ReadWorkAreaOutCmd',
    'ReadWorkAreaParCmd',
    'ReadWorkAreaRecvData',
    'ReadWorkAreaSendData',
    'RedefineTrackingPosOutCmd',
    'RedefineTrackingPosParCmd',
    'RedefineTrackingPosRecvData',
    'RedefineTrackingPosSendData',
    'ReferenceDynamics',
    'RestartControllerOutCmd',
    'RestartControllerParCmd',
    'RestartControllerRecvData',
    'RestartControllerSendData',
    'ReturnToPrimaryOutCmd',
    'ReturnToPrimaryParCmd',
    'ReturnToPrimaryRecvData',
    'ReturnToPrimarySendData',
    'RobotAxesFlags',
    'RobotCartesianForce',
    'RobotCartesianForceExt',
    'RobotCartesianForceShort',
    'RobotCartesianPosition',
    'RobotCartesianPositionBase',
    'RobotCartesianPositionExt',
    'RobotCartesianPositionShort',
    'RobotCoordinateSystemParameters',
    'RobotDynamics',
    'RobotJointCurrent',
    'RobotJointCurrentExt',
    'RobotJointCurrentShort',
    'RobotJointPosition',
    'RobotJointPositionExt',
    'RobotJointPositionShort',
    'RobotSubProgramData',
    'RobotTaskParCfg',
    'RobotTaskParCfgCom',
    'RobotTaskParCfgPlc',
    'RobotTaskParCfgPlcParameter',
    'RobotTaskParCfgRob',
    'RobotTaskParCfgRobParameter',
    'RobotWorkArea',
    'RobotWorkAreaData',
    'RobotWorkAreaDataLimitCartesian',
    'RobotWorkAreaDataLimitJoint',
    'RspHeader',
    'SWLimits',
    'SearchHardStopJOutCmd',
    'SearchHardStopJParCmd',
    'SearchHardStopJRecvData',
    'SearchHardStopJSendData',
    'SearchHardStopOutCmd',
    'SearchHardStopParCmd',
    'SearchHardStopRecvData',
    'SearchHardStopSendData',
    'SetOperationModeOutCmd',
    'SetOperationModeParCmd',
    'SetOperationModeRecvData',
    'SetOperationModeSendData',
    'SetSequenceOutCmd',
    'SetSequenceParCmd',
    'SetSequenceRecvData',
    'SetSequenceSendData',
    'SetTriggerErrorOutCmd',
    'SetTriggerErrorParCmd',
    'SetTriggerErrorRecvData',
    'SetTriggerErrorSendData',
    'SetTriggerLimitOutCmd',
    'SetTriggerLimitParCmd',
    'SetTriggerLimitRecvData',
    'SetTriggerLimitSendData',
    'SetTriggerMotionOutCmd',
    'SetTriggerMotionParCmd',
    'SetTriggerMotionRecvData',
    'SetTriggerMotionSendData',
    'SetTriggerRegisterOutCmd',
    'SetTriggerRegisterParCmd',
    'SetTriggerRegisterRecvData',
    'SetTriggerRegisterSendData',
    'SetTriggerUserOutCmd',
    'SetTriggerUserParCmd',
    'SetTriggerUserRecvData',
    'SetTriggerUserSendData',
    'ShiftPositionOutCmd',
    'ShiftPositionParCmd',
    'ShiftPositionRecvData',
    'ShiftPositionSendData',
    'SoftSwitchTcpOutCmd',
    'SoftSwitchTcpParCmd',
    'SoftSwitchTcpRecvData',
    'SoftSwitchTcpSendData',
    'SplineData',
    'SplineDataSend',
    'StopSubprogramOutCmd',
    'StopSubprogramParCmd',
    'StopSubprogramRecvData',
    'StopSubprogramSendData',
    'SwitchLanguageOutCmd',
    'SwitchLanguageParCmd',
    'SwitchLanguageRecvData',
    'SwitchLanguageSendData',
    'SyncToConveyorOutCmd',
    'SyncToConveyorParCmd',
    'SyncToConveyorRecvData',
    'SyncToConveyorSendData',
    'SyncUserInteraction',
    'SynchronizationModes',
    'SystemTime',
    'Telegram',
    'TelegramPlcToRob',
    'TelegramPlcToRobCommand',
    'TelegramPlcToRobCommandHeader',
    'TelegramPlcToRobCyclicData',
    'TelegramPlcToRobCyclicOptionalCartesianPosition',
    'TelegramPlcToRobCyclicOptionalCartesianPositionExt',
    'TelegramPlcToRobCyclicOptionalCurrent',
    'TelegramPlcToRobCyclicOptionalCurrentExt',
    'TelegramPlcToRobCyclicOptionalData',
    'TelegramPlcToRobCyclicOptionalForce',
    'TelegramPlcToRobCyclicOptionalForceExt',
    'TelegramPlcToRobCyclicOptionalJointPosition',
    'TelegramPlcToRobCyclicOptionalJointPositionExt',
    'TelegramPlcToRobCyclicOptionalSubProgramData',
    'TelegramPlcToRobFooter',
    'TelegramPlcToRobFragment',
    'TelegramPlcToRobFragmentHeader',
    'TelegramPlcToRobHeader',
    'TelegramPlcToRobSequence',
    'TelegramPlcToRobSequenceHeader',
    'TelegramRobToPlc',
    'TelegramRobToPlcCommand',
    'TelegramRobToPlcCommandHeader',
    'TelegramRobToPlcCyclicOptionalCartesianPosition',
    'TelegramRobToPlcCyclicOptionalCartesianPositionExt',
    'TelegramRobToPlcCyclicOptionalCurrent',
    'TelegramRobToPlcCyclicOptionalCurrentExt',
    'TelegramRobToPlcCyclicOptionalData',
    'TelegramRobToPlcCyclicOptionalForce',
    'TelegramRobToPlcCyclicOptionalForceExt',
    'TelegramRobToPlcCyclicOptionalJointPosition',
    'TelegramRobToPlcCyclicOptionalJointPositionExt',
    'TelegramRobToPlcCyclicOptionalSubProgramData',
    'TelegramRobToPlcFooter',
    'TelegramRobToPlcFragment',
    'TelegramRobToPlcFragmentHeader',
    'TelegramRobToPlcHeader',
    'TelegramRobToPlcSequence',
    'TelegramRobToPlcSequenceHeader',
    'Tool',
    'ToolData',
    'TrackingStatus',
    'TurnNumber',
    'UnitMeasurementOutCmd',
    'UnitMeasurementParCmd',
    'UnitMeasurementRecvData',
    'UnitMeasurementSendData',
    'UserData',
    'UserLoginOutCmd',
    'UserLoginParCmd',
    'UserLoginRecvData',
    'UserLoginSendData',
    'VersionStruct',
    'WaitForTriggerOutCmd',
    'WaitForTriggerParCmd',
    'WaitForTriggerRecvData',
    'WaitForTriggerSendData',
    'WaitTimeOutCmd',
    'WaitTimeParCmd',
    'WaitTimeRecvData',
    'WaitTimeSendData',
    'WriteAnalogOutputOutCmd',
    'WriteAnalogOutputParCmd',
    'WriteAnalogOutputRecvData',
    'WriteAnalogOutputSendData',
    'WriteCallSubprogramCyclicOutCmd',
    'WriteCallSubprogramCyclicParCmd',
    'WriteDigitalOutputsOutCmd',
    'WriteDigitalOutputsParCmd',
    'WriteDigitalOutputsRecvData',
    'WriteDigitalOutputsSendData',
    'WriteFrameDataOutCmd',
    'WriteFrameDataParCmd',
    'WriteFrameDataRecvData',
    'WriteFrameDataSendData',
    'WriteIntegersOutCmd',
    'WriteIntegersParCmd',
    'WriteIntegersRecvData',
    'WriteIntegersSendData',
    'WriteLoadDataOutCmd',
    'WriteLoadDataParCmd',
    'WriteLoadDataRecvData',
    'WriteLoadDataSendData',
    'WriteRealsOutCmd',
    'WriteRealsParCmd',
    'WriteRealsRecvData',
    'WriteRealsSendData',
    'WriteRobotDefaultDynamicsOutCmd',
    'WriteRobotDefaultDynamicsParCmd',
    'WriteRobotDefaultDynamicsRecvData',
    'WriteRobotDefaultDynamicsSendData',
    'WriteRobotReferenceDynamicsOutCmd',
    'WriteRobotReferenceDynamicsParCmd',
    'WriteRobotReferenceDynamicsRecvData',
    'WriteRobotReferenceDynamicsSendData',
    'WriteRobotSWLimitsOutCmd',
    'WriteRobotSWLimitsParCmd',
    'WriteRobotSWLimitsRecvData',
    'WriteRobotSWLimitsSendData',
    'WriteSystemVariableOutCmd',
    'WriteSystemVariableParCmd',
    'WriteSystemVariableRecvData',
    'WriteSystemVariableSendData',
    'WriteToolDataOutCmd',
    'WriteToolDataParCmd',
    'WriteToolDataRecvData',
    'WriteToolDataSendData',
    'WriteWorkAreaOutCmd',
    'WriteWorkAreaParCmd',
    'WriteWorkAreaRecvData',
    'WriteWorkAreaSendData',
]


@_dataclass(kw_only=True, slots=True)
class AbortMeasuringInputOutCmd:
    """AbortMeasuringInputOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class AbortMeasuringInputParCmd:
    """AbortMeasuringInputParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """
    Define an active measurement that is to be aborted. • 0: Abort all existing measurement • >0:
    Abort the measurement with the specific MeasuringID
    """


@_dataclass(kw_only=True, slots=True)
class RspHeader:
    """RspHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ParSeq: int = 0
    """
    Parameter Sequence, used to identify sets of CMD parameter - For more information see chapter
    5.6.4
    """
    State: _e.CmdMessageState = _e.CmdMessageState.EMPTY
    """Actual state of the command - For more information and examples, see chapter 5.6.3.2"""
    AlarmMessageSeverity: _e.Severity = _e.Severity.DEACTIVATE
    """Severity of returned message according to .Table 5-47."""
    AlarmMessageCode: int = 0
    """
    Message code for error/warning/info identification reported during execution of command
    according to • Error: Table 7-1 • Warning: Table 7-3 • Info: Table 7-5
    """


@_dataclass(kw_only=True, slots=True)
class AbortMeasuringInputRecvData(RspHeader):
    """AbortMeasuringInputRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class CmdHeader:
    """CmdHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CmdTyp: _e.CmdType = _e.CmdType.RobotTask
    """Type of command - For more information see chapter 5.6.4."""
    ExecMode: _e.ExecutionMode = _e.ExecutionMode.SEQUENCE_PRIMARY
    """Specifies target buffer and processing behavior - For more information see chapter 5.6.4.5"""
    ParSeq: int = 0
    """Parameter Sequence, used to identify sets of CMD parameter"""
    Priority: _e.PriorityLevel = _e.PriorityLevel.VERY_HIGH
    """Priority of this command"""


@_dataclass(kw_only=True, slots=True)
class AbortMeasuringInputSendData(CmdHeader):
    """AbortMeasuringInputSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """
    Define an active measurement that is to be aborted. • 0: Abort all existing measurement • >0:
    Abort the measurement with the specific MeasuringID
    """


@_dataclass(kw_only=True, slots=True)
class ActivateNextCommandOutCmd:
    """ActivateNextCommandOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class ActivateNextCommandParCmd:
    """ActivateNextCommandParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class ActivateNextCommandRecvData(RspHeader):
    """ActivateNextCommandRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class ActivateNextCommandSendData(CmdHeader):
    """ActivateNextCommandSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: Undefined (default) - If no EmitterID is
    defined, the function returns an error message For more information see chapter 5.5.12.4
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class AvoidSingularityOutCmd:
    """AvoidSingularityOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class AvoidSingularityParCmd:
    """AvoidSingularityParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.SingularityAvoidanceMode = _e.SingularityAvoidanceMode.NO_CHANGE
    """Define in which way the singularity should be avoided"""


@_dataclass(kw_only=True, slots=True)
class AvoidSingularityRecvData(RspHeader):
    """AvoidSingularityRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE when robot is set to RA power state "Enabled"."""


@_dataclass(kw_only=True, slots=True)
class AvoidSingularitySendData(CmdHeader):
    """AvoidSingularitySendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enable: bool = False
    """Set TRUE to activate avoid singularity mode"""
    Mode: _e.SingularityAvoidanceMode = _e.SingularityAvoidanceMode.NO_CHANGE
    """Define in which way the singularity should be avoided"""


@_dataclass(kw_only=True, slots=True)
class BrakeTestOutCmd:
    """BrakeTestOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotAxesStatus: RobotAxesFlags = _field(default_factory=lambda: RobotAxesFlags())
    """
    Indicates the result of the brake test of the robot axes related to the brake test. • TRUE: The
    brake test has been realized successfully. • FALSE: The brake test failed. See Table 6-735 for
    bit assignment.
    """
    ExternalAxesStatus: ExternalAxesFlags = _field(default_factory=lambda: ExternalAxesFlags())
    """
    Indicates the result of the brake test of the external robot axes related to the brake test. •
    TRUE: The brake test has been realized successfully. • FALSE: The brake test failed. See Table
    6-735 for bit assignment.
    """
    RobotAxesWarning: RobotAxesFlags = _field(default_factory=lambda: RobotAxesFlags())
    """
    Indicates the warning messages availability related to the brake functionality of the robot axes
    reported by the RC. • TRUE: One or more warning messages are available. • FALSE: No warning
    message is available. See Table 6-735 for bit assignment.
    """
    ExternalAxesWarning: ExternalAxesFlags = _field(default_factory=lambda: ExternalAxesFlags())
    """
    Indicates the warning messages availability related to the brake functionality of the external
    robot axis reported by the RC. • TRUE: One or more warning messages are available. • FALSE: No
    warning message is available. See Table 6-735 for bit assignment.
    """


@_dataclass(kw_only=True, slots=True)
class BrakeTestParCmd:
    """BrakeTestParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotAxesActive: RobotAxesFlags = _field(default_factory=lambda: RobotAxesFlags())
    """
    Defines which of the robot axis should be activated for the brake test. • TRUE (default): Axis
    activated. • FALSE: Axis deactivated. See Table 6-735 for bit assignment.
    """
    ExternalAxesActive: ExternalAxesFlags = _field(default_factory=lambda: ExternalAxesFlags())
    """
    Defines which of the external robot axis should be activated for the brake test. • TRUE: Axis
    activated. • FALSE (default): Axis deactivated. See Table 6-735 for bit assignment.
    """


@_dataclass(kw_only=True, slots=True)
class BrakeTestRecvData(RspHeader):
    """BrakeTestRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotAxesStatus: int = 0
    """
    Indicates the result of the brake test of the robot axes related to the brake test. • TRUE: The
    brake test has been realized successfully. • FALSE: The brake test failed. See Table 6-735 for
    bit assignment.
    """
    ExternalAxesStatus: int = 0
    """
    Indicates the result of the brake test of the external robot axes related to the brake test. •
    TRUE: The brake test has been realized successfully. • FALSE: The brake test failed. See Table
    6-735 for bit assignment.
    """
    RobotAxesWarning: int = 0
    """
    Indicates the warning messages availability related to the brake functionality of the robot axes
    reported by the RC. • TRUE: One or more warning messages are available. • FALSE: No warning
    message is available. See Table 6-735 for bit assignment.
    """
    ExternalAxesWarning: int = 0
    """
    Indicates the warning messages availability related to the brake functionality of the external
    robot axis reported by the RC. • TRUE: One or more warning messages are available. • FALSE: No
    warning message is available. See Table 6-735 for bit assignment.
    """


@_dataclass(kw_only=True, slots=True)
class BrakeTestSendData(CmdHeader):
    """BrakeTestSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotAxesActive: int = 0
    """
    Defines which of the robot axis should be activated for the brake test. • TRUE (default): Axis
    activated. • FALSE: Axis deactivated. See Table 6-735 for bit assignment.
    """
    ExternalAxesActive: int = 0
    """
    Defines which of the external robot axis should be activated for the brake test. • TRUE: Axis
    activated. • FALSE (default): Axis deactivated. See Table 6-735 for bit assignment.
    """


@_dataclass(kw_only=True, slots=True)
class CallSubprogramOutCmd:
    """CallSubprogramOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InstanceID: int = 0
    """
    Unique, system-generated ID of the instance of CallSubprogram. Can be used to specifically stop
    instance of a subprogram via the function Stop Subprogram (chapter 6.5.21) if multiinstancing is
    supported by RC
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    InProgress: bool = False
    """
    The requested subprogram on the RC is in progress. Movement of the axes trough this subprogram
    is possible.
    """
    ReturnData: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('SUB_PROGRAM_DATA_MAX')))
    """
    Acyclic output parameters of the subprogram Array length adjusts to transmitted data (max 190
    bytes)
    """


@_dataclass(kw_only=True, slots=True)
class CallSubprogramParCmd:
    """CallSubprogramParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JobID: int = 0
    """Program number of the subprogram in the RC"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) - No trigger related behavior • >0:
    Triggero - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Data: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('SUB_PROGRAM_DATA_MAX')))
    """
    Acyclic input parameters of the subprogram Array length adjusts to transmitted data (max 190
    bytes)
    """


@_dataclass(kw_only=True, slots=True)
class CallSubprogramRecvData(RspHeader):
    """CallSubprogramRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    InProgress: bool = False
    """
    The requested subprogram on the RC is in progress. Movement of the axes trough this subprogram
    is possible.
    """
    ReturnData: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('SUB_PROGRAM_DATA_MAX')))
    """
    Acyclic output parameters of the subprogram Array length adjusts to transmitted data (max 190
    bytes)
    """


@_dataclass(kw_only=True, slots=True)
class CallSubprogramSendData(CmdHeader):
    """CallSubprogramSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) - No trigger related behavior • >0:
    Triggero - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    JobID: int = 0
    """Program number of the subprogram in the RC"""
    Data: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('SUB_PROGRAM_DATA_MAX')))
    """
    Acyclic input parameters of the subprogram Array length adjusts to transmitted data (max 190
    bytes)
    """


@_dataclass(kw_only=True, slots=True)
class CollisionDetectionOutCmd:
    """CollisionDetectionOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class CollisionDetectionParCmd:
    """CollisionDetectionParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ProcessingMode: _e.ProcessingMode = _e.ProcessingMode.BUFFERED
    """Processing mode"""
    ReactionMode: _e.CollisionReactionMode = _e.CollisionReactionMode.STANDING_STILL
    """
    Defines the robot behavior after detecting the collision (at least one option must be
    supported):
    """
    ActivateMonitoring: bool = False
    """Set TRUE to activate and FALSE to deactivate "CollisionDetection". Default: TRUE"""
    ThresholdMode: _e.ThresholdMode = _e.ThresholdMode.AUTOMATIC
    """Defines the type of threshold setting (at least one option must be supported)"""
    Sensitivity: float = 0.0
    """
    Defines the level of sensitivity of all axes. • 0..99: Sensitivity lower than robot vendor
    default. At minimum value "0" there is no sensitivity. The lower the value, the lower the
    sensitivity at the collision detection. • 100 (default): The value is aligned with the robot
    vendor-specific default value. • 101..200: Sensitivity higher than robot vendor default. At
    maximum value "200" highest possible sensitivity at the collision detection.
    """
    SensitivityAxis: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """
    Defines the level of sensitivity of the respective axis. Values: • 0..99: Sensitivity lower than
    robot vendor default. At minimum value "0" there is no sensitivity and collision detection for
    the respective axis. The lower the value, the lower the sensitivity at the collision detection.
    • 100 (default): The value is aligned with the robot vendor-specific default value. • 101..200:
    Sensitivity higher than robot vendor default. At maximum value "200" highest possible
    sensitivity at the collision detection. Index: • [0]: J1 First joint of the robot. • [1]: J2
    Second joint of the robot. • [2] J3 Third joint of the robot. • [3] J4 Forth joint of the robot.
    • [4] J5 Fifth joint of the robot. • [5] J6 Six joint of the robot. • [6] J7 Seventh joint of
    the robot, if willbe used.
    """
    LimitAxis: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """
    Relates to "ThresholdMode" Manual. Defines the threshold of the torque for each robot axis. If
    the threshold is exceeded, the RA stops. Index: • [0] J1 First joint of the robot. • [1] J2
    Second joint of the robot. • [2] J3 Third joint of the robot. • [3] J4 Forth joint of the robot.
    • [4] J5 Fifth joint of the robot. • [5] J6 Six joint of the robot. • [6] J7 Seventh joint of
    the robot, if will be used
    """
    UnitLimitAxis: int = 0
    """
    Relates to "LimitAxis". Defines the unit of the threshold. • [0]: Percentage (%) (default) O •
    [1]: Newton meter (Nm). O • [2] Milliampere (mA).
    """
    SequenceFlag: _e.SequenceFlag = _e.SequenceFlag.NO_SEQUENCE
    """Defines the target sequence in which the command will be executed"""


@_dataclass(kw_only=True, slots=True)
class CollisionDetectionRecvData(RspHeader):
    """CollisionDetectionRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class CollisionDetectionSendData(CmdHeader):
    """CollisionDetectionSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActivateMonitoring: bool = False
    """Set TRUE to activate and FALSE to deactivate "CollisionDetection". Default: TRUE"""
    UnitLimitAxis: int = 0
    """
    Relates to "LimitAxis". Defines the unit of the threshold. • [0]: Percentage (%) (default) O •
    [1]: Newton meter (Nm). O • [2] Milliampere (mA).
    """
    ThresholdMode: _e.ThresholdMode = _e.ThresholdMode.AUTOMATIC
    """Defines the type of threshold setting (at least one option must be supported)"""
    ReactionMode: _e.CollisionReactionMode = _e.CollisionReactionMode.STANDING_STILL
    """
    Defines the robot behavior after detecting the collision (at least one option must be
    supported):
    """
    Sensitivity: int = 0
    """
    Defines the level of sensitivity of all axes. • 0..99: Sensitivity lower than robot vendor
    default. At minimum value "0" there is no sensitivity. The lower the value, the lower the
    sensitivity at the collision detection. • 100 (default): The value is aligned with the robot
    vendor-specific default value. • 101..200: Sensitivity higher than robot vendor default. At
    maximum value "200" highest possible sensitivity at the collision detection.
    """
    SensitivityAxis: list[int] = _field(default_factory=lambda: [0] * 7)
    """
    Defines the level of sensitivity of the respective axis. Values: • 0..99: Sensitivity lower than
    robot vendor default. At minimum value "0" there is no sensitivity and collision detection for
    the respective axis. The lower the value, the lower the sensitivity at the collision detection.
    • 100 (default): The value is aligned with the robot vendor-specific default value. • 101..200:
    Sensitivity higher than robot vendor default. At maximum value "200" highest possible
    sensitivity at the collision detection. Index: • [0]: J1 First joint of the robot. • [1]: J2
    Second joint of the robot. • [2] J3 Third joint of the robot. • [3] J4 Forth joint of the robot.
    • [4] J5 Fifth joint of the robot. • [5] J6 Six joint of the robot. • [6] J7 Seventh joint of
    the robot, if willbe used.
    """
    LimitAxis: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """
    Relates to "ThresholdMode" Manual. Defines the threshold of the torque for each robot axis. If
    the threshold is exceeded, the RA stops. Index: • [0] J1 First joint of the robot. • [1] J2
    Second joint of the robot. • [2] J3 Third joint of the robot. • [3] J4 Forth joint of the robot.
    • [4] J5 Fifth joint of the robot. • [5] J6 Six joint of the robot. • [6] J7 Seventh joint of
    the robot, if will be used
    """


@_dataclass(kw_only=True, slots=True)
class ExchangeConfigurationOutCmd:
    """ExchangeConfigurationOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LengthACR: int = 0
    """Returns a metric of how many CMDs it can receive and manage at the same time"""
    HighestToolIndex: int = 0
    """Highest index of available tools on the RC."""
    HighestFrameIndex: int = 0
    """Highest index of available frames on the RC."""
    HighestLoadIndex: int = 0
    """Highest index of available loads on the RC."""
    HighestWorkAreaIndex: int = 0
    """Highest index of available work areas on the RC."""
    DataInSync: _s.DataInSync = _field(default_factory=lambda: DataInSync())
    """Datas which are synchronized"""
    ChangeIndexTool: int = 0
    """Index of tool changed on RC"""
    ChangeIndexFrame: int = 0
    """Index of frame changed on RC"""
    ChangeIndexLoad: int = 0
    """Index of load changed on RC"""
    ChangeIndexWorkArea: int = 0
    """Index of work area changed on RC"""
    RAWorkingHours: int = 0
    """Working hours of an RA connected to the RC"""
    BrakeTestRequired: bool = False
    """Signals that a brake test is required in the defined monitoring time (see chapter 6.5.27)"""
    StepModeExactStopActive: bool = False
    """StepMode is active and set to ExactStop (see chapter 6.1.3)"""
    StepModeBlendingActive: bool = False
    """StepMode is active and set to Blending (see chapter 6.1.3)"""
    PathAccuracyMode: bool = False
    """PathAccuracyMode is active (see chapter 6.5.22)"""
    AvoidSingularity: bool = False
    """AvoidSingularity is active (see chapter 6.5.23)"""
    CollisionDetectionEnabled: bool = False
    """CollisionDetection is active (see chapter 6.5.35)"""
    AcceleratingSupported: bool = False
    """Cyclic dynamics status bit Accelerating is supported by RC (see chapter 5.5.3.2)"""
    DecceleratingSupported: bool = False
    """Cyclic dynamics status bit Decelerating is supported by RC (see chapter 5.5.3.2)"""
    ConstantVelocitySupported: bool = False
    """Cyclic dynamics status bit ConstantVelocity is supported by RC (see chapter 5.5.3.2)"""
    RCWorkingHours: int = 0
    """
    Total system hours of an RA connected to the RC. Must not be modifiable by the user. • 0:
    Invalid • >1: Total system hours
    """


@_dataclass(kw_only=True, slots=True)
class ExchangeConfigurationParCmd:
    """ExchangeConfigurationParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LogLevel: _e.Severity = _e.Severity.DEACTIVATE
    """Defines up to which level of severity messages will be logged in the RC's server log"""
    WaitAtBlendingZone: bool = False
    """
    Defines blending behavior for single move commands. One of the optional modes must be supported.
    • 0 (default): Move to end position Robot moves exactly the target position independently of the
    selected "BlendingMode" • 1: Wait at blending parameter Robot stops its movement when the
    specified blending parameter is reached
    """
    AllowSecSeqWhileSubprogram: bool = False
    """
    Allow a sequence switch from primary to secondary while a subprogram called via CallSubprogram
    (6.5.18) in the sequence is in progress
    """
    AllowDynamicBlending: bool = False
    """
    Allows blending when CallSubprogram is called in sequence and removed afterwards. For more
    information see chapter 6.5.21. • 0 (default): Dynamic blending is prevented • 1: Dynamic
    blending is allowed
    """
    DelayTime: int = 0
    """
    Defines waiting time of RC between receiving a first move command when motion queue is empty and
    starting the first movement. See also chapter 5.6.8.
    """
    WaitForNrOfCmd: int = 0
    """Define number of points required to calculate the blending. See also chapter 5.6.8."""
    LifeSignTimeOut: int = 0
    """
    Maximum allowed time between incrementation of LifeSign before communication error. • <10 ms:
    Invalid • 50 ms: default See also chapter 5.6.6.2.
    """
    SyncDelay: int = 0
    """
    Defines a delay time between detecting an inconsistency of configuration data between server and
    client and executing the defined SyncReaction. Always positive. Default: 0 ms
    """
    SyncReaction: _e.SyncReaction = _e.SyncReaction.NO_REACTION
    """
    Specifies system reaction in case inconsistency of synchronization data is detected according to
    Table 6-81. For more information refer to chapter 5.6.7.2
    """
    DataInSync: _s.DataInSync = _field(default_factory=lambda: DataInSync())
    """Datas which are synchronized"""
    DataEnableSync: _s.DataEnableSync = _field(default_factory=lambda: DataEnableSync())
    """Enable datas to synchronize"""


@_dataclass(kw_only=True, slots=True)
class ExchangeConfigurationRecvData(RspHeader):
    """ExchangeConfigurationRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE when function is exchanging data"""
    Reserve1: int = 0
    """Reserve"""
    LengthACR: int = 0
    """Returns a metric of how many CMDs it can receive and manage at the same time"""
    HighestToolIndex: int = 0
    """Highest index of available tools on the RC."""
    HighestFrameIndex: int = 0
    """Highest index of available frames on the RC."""
    HighestLoadIndex: int = 0
    """Highest index of available loads on the RC."""
    HighestWorkAreaIndex: int = 0
    """Highest index of available work areas on the RC."""
    DataInSync: _s.DataInSync = _field(default_factory=lambda: DataInSync())
    """Datas which are synchronized"""
    Reserve2: int = 0
    """Reserve"""
    ChangeIndexTool: int = 0
    """Index of tool changed on RC"""
    ChangeIndexFrame: int = 0
    """Index of frame changed on RC"""
    ChangeIndexLoad: int = 0
    """Index of load changed on RC"""
    ChangeIndexWorkArea: int = 0
    """Index of work area changed on RC"""
    RAWorkingHours: int = 0
    """Working hours of an RA connected to the RC"""
    StatusByte: int = 0
    """Status byte"""
    ConstantVelocitySupported: bool = False
    """Cyclic dynamics status bit ConstantVelocity is supported by RC (see chapter 5.5.3.2)"""
    RCWorkingHours: int = 0
    """
    Total system hours of an RA connected to the RC. Must not be modifiable by the user. • 0:
    Invalid • >1: Total system hours
    """


@_dataclass(kw_only=True, slots=True)
class ExchangeConfigurationSendData(CmdHeader):
    """ExchangeConfigurationSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LogLevel: _e.Severity = _e.Severity.DEACTIVATE
    """Defines up to which level of severity messages will be logged in the RC's server log"""
    CtrlByte: int = 0
    """Miscellaneous control bits"""
    DelayTime: int = 0
    """
    Defines waiting time of RC between receiving a first move command when motion queue is empty and
    starting the first movement. See also chapter 5.6.8.
    """
    WaitForNrOfCmd: int = 0
    """Define number of points required to calculate the blending. See also chapter 5.6.8."""
    LifeSignTimeOut: int = 0
    """
    Maximum allowed time between incrementation of LifeSign before communication error. • <10 ms:
    Invalid • 50 ms: default See also chapter 5.6.6.2.
    """
    SyncDelay: int = 0
    """
    Defines a delay time between detecting an inconsistency of configuration data between server and
    client and executing the defined SyncReaction. Always positive. Default: 0 ms
    """
    SyncReaction: _e.SyncReaction = _e.SyncReaction.NO_REACTION
    """
    Specifies system reaction in case inconsistency of synchronization data is detected according to
    Table 6-81. For more information refer to chapter 5.6.7.2
    """
    Reserve1: int = 0
    """Reserve"""
    DataInSync: _s.DataInSync = _field(default_factory=lambda: DataInSync())
    """Datas which are synchronized"""
    Reserve2: int = 0
    """Reserve"""
    DataEnableSync: _s.DataEnableSync = _field(default_factory=lambda: DataEnableSync())
    """Enable datas to synchronize"""
    Reserve3: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class FreeDriveOutCmd:
    """FreeDriveOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE while "FreeDrive" is active."""


@_dataclass(kw_only=True, slots=True)
class FreeDriveParCmd:
    """FreeDriveParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class FreeDriveRecvData(RspHeader):
    """FreeDriveRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE when function is exchanging data"""


@_dataclass(kw_only=True, slots=True)
class FreeDriveSendData(CmdHeader):
    """FreeDriveSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enable: bool = False
    """Set TRUE to activate "FreeDrive"."""


@_dataclass(kw_only=True, slots=True)
class MeasuringInputOutCmd:
    """MeasuringInputOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """FB is returning a unique ID for the called measurement."""
    Measurings: _iec.IecArray[MeasuringInputResult] = _field(default_factory=lambda: _iec.IecArray(1, [MeasuringInputResult() for _ in range(2)]))
    """
    Measured robot position value at the rising edge of the digital input in selected coordinate
    systems (see input parameters ToolNo and FrameNo).
    """


@_dataclass(kw_only=True, slots=True)
class MeasuringInputParCmd:
    """MeasuringInputParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringMode: _e.MeasuringIoMode = _e.MeasuringIoMode.MEASUREMENT_AT_NEXT_RISING_EDGE
    """Type of measurement (at least one option must be supported):"""
    Index: int = 0
    """
    Specifies the desired digital input register. More information about the different periphery
    register can be found in chapter 6.4
    """
    BitNumber: int = 0
    """
    Specifies the desired bit in the digital input register, that should be read. More information
    about the different periphery register can be found in chapter 6.4.
    """


@_dataclass(kw_only=True, slots=True)
class MeasuringInputRecvData(RspHeader):
    """MeasuringInputRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """FB is returning a unique ID for the called measurement."""
    Measurings: _iec.IecArray[MeasuringInputResult] = _field(default_factory=lambda: _iec.IecArray(1, [MeasuringInputResult() for _ in range(2)]))
    """
    Measured robot position value at the rising edge of the digital input in selected coordinate
    systems (see input parameters ToolNo and FrameNo).
    """


@_dataclass(kw_only=True, slots=True)
class MeasuringInputSendData(CmdHeader):
    """MeasuringInputSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringMode: _e.MeasuringIoMode = _e.MeasuringIoMode.MEASUREMENT_AT_NEXT_RISING_EDGE
    """Type of measurement (at least one option must be supported):"""
    Index: int = 0
    """
    Specifies the desired digital input register. More information about the different periphery
    register can be found in chapter 6.4
    """
    BitNumber: int = 0
    """
    Specifies the desired bit in the digital input register, that should be read. More information
    about the different periphery register can be found in chapter 6.4.
    """


@_dataclass(kw_only=True, slots=True)
class OpenBrakeOutCmd:
    """OpenBrakeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE when "OpenBrake" is active."""
    RobotAxesBrakeReleased: RobotAxesFlags = _field(default_factory=lambda: RobotAxesFlags())
    """
    Indicates the brake release status of the main robot axes. • TRUE: The brake of the axis is
    opened. • FALSE: The brake of the axis is closed. See Table 6-735 for bit assignment
    """
    ExternalAxesBrakeReleased: ExternalAxesFlags = _field(default_factory=lambda: ExternalAxesFlags())
    """
    Indicates the brake release status of the external robot axes. • TRUE: The brake of the axis is
    opened. • FALSE: The brake of the axis is closed/not supported See Table 6-735 for bit
    assignment
    """


@_dataclass(kw_only=True, slots=True)
class OpenBrakeParCmd:
    """OpenBrakeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotAxesBrakeRelease: RobotAxesFlags = _field(default_factory=lambda: RobotAxesFlags())
    """
    Defines which brake of the robot axes must be released. • TRUE: Open the brake of the axis. •
    FALSE (default): Close the brake of the axis.
    """
    ExternalAxesBrakeRelease: ExternalAxesFlags = _field(default_factory=lambda: ExternalAxesFlags())
    """
    Defines which brake of the external robot axis must be released. • TRUE: Open the brake of the
    axis. • FALSE (default): Close the brake of the axis. See Table 6-676 for bit assignment.
    """


@_dataclass(kw_only=True, slots=True)
class OpenBrakeRecvData(RspHeader):
    """OpenBrakeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: int = 0
    """TRUE when "OpenBrake" is active."""
    RobotAxesBrakeReleased: int = 0
    """
    Indicates the brake release status of the main robot axes. • TRUE: The brake of the axis is
    opened. • FALSE: The brake of the axis is closed. See Table 6-735 for bit assignment
    """
    ExternalAxesBrakeReleased: int = 0
    """
    Indicates the brake release status of the external robot axes. • TRUE: The brake of the axis is
    opened. • FALSE: The brake of the axis is closed/not supported See Table 6-735 for bit
    assignment
    """


@_dataclass(kw_only=True, slots=True)
class OpenBrakeSendData(CmdHeader):
    """OpenBrakeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotAxesBrakeRelease: int = 0
    """
    Defines which brake of the robot axes must be released. • TRUE: Open the brake of the axis. •
    FALSE (default): Close the brake of the axis.
    """
    ExternalAxesBrakeRelease: int = 0
    """
    Defines which brake of the external robot axis must be released. • TRUE: Open the brake of the
    axis. • FALSE (default): Close the brake of the axis. See Table 6-676 for bit assignment.
    """


@_dataclass(kw_only=True, slots=True)
class PathAccuracyModeOutCmd:
    """PathAccuracyModeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class PathAccuracyModeParCmd:
    """PathAccuracyModeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class PathAccuracyModeRecvData(RspHeader):
    """PathAccuracyModeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE while PathAccuracyMode is active"""


@_dataclass(kw_only=True, slots=True)
class PathAccuracyModeSendData(CmdHeader):
    """PathAccuracyModeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enable: bool = False
    """Set TRUE to activate monitoring of work areas"""


@_dataclass(kw_only=True, slots=True)
class ReadCallSubprogramCyclicOutCmd:
    """ReadCallSubprogramCyclicOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Data: list[int] = _field(default_factory=lambda: [0] * 26)
    """Cyclic input data of subprogram"""


@_dataclass(kw_only=True, slots=True)
class ReadCallSubprogramCyclicParCmd:
    """ReadCallSubprogramCyclicParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ShiftPositionOutCmd:
    """ShiftPositionOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TransformedPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Tool index"""


@_dataclass(kw_only=True, slots=True)
class ShiftPositionParCmd:
    """ShiftPositionParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.TransformMode = _e.TransformMode.MIRROR_AT_POINT
    """Define which method should be used to transform the position:"""
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute coordinates of the position that will be transformed in the selected coordinate systems
    (see input parameter CoordinateSystem).
    """
    FrameNo: int = 0
    """
    Defines the reference frame ID to which the "Position" that will be transformed is relative. •
    0: WCS (default) • 1..254: User frames
    """
    TargetFrameNo: int = 0
    """
    Defines the reference frame ID to which the "TransformedPosition" should be relative. • 0: WCS
    (default) • 1..254: User frames
    """
    TransformationParameter_1: FrameData = _field(default_factory=lambda: FrameData())
    """
    Defines the frame data relevant for the transformation of the "Position". Relates to all "Mode"
    settings. The parameter includes the Frame ID to which the origin of the shifting and rotation
    is relative and the cartesian position of the origin
    """
    TransformationParameter_2: _e.ReferenceElement = _e.ReferenceElement.NOT_USED
    """
    Relates to all "Mode" settings. Defines the enabled axis or plane as reference straight line or
    reference plain for the transformation
    """
    RotationAngle: float = 0.0
    """
    Defines the angle of rotation around the defined straight line. Related to "Mode" with the
    setting "Rotate around Straight Line".
    """


@_dataclass(kw_only=True, slots=True)
class ShiftPositionRecvData(RspHeader):
    """ShiftPositionRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TransformedPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Tool index"""


@_dataclass(kw_only=True, slots=True)
class ShiftPositionSendData(CmdHeader):
    """ShiftPositionSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TransformationParameter_1: FrameData = _field(default_factory=lambda: FrameData())
    """
    Defines the frame data relevant for the transformation of the "Position". Relates to all "Mode"
    settings. The parameter includes the Frame ID to which the origin of the shifting and rotation
    is relative and the cartesian position of the origin
    """
    TransformationParameter_2: _e.ReferenceElement = _e.ReferenceElement.NOT_USED
    """
    Relates to all "Mode" settings. Defines the enabled axis or plane as reference straight line or
    reference plain for the transformation
    """
    RotationAngle: float = 0.0
    """
    Defines the angle of rotation around the defined straight line. Related to "Mode" with the
    setting "Rotate around Straight Line".
    """
    Mode: _e.TransformMode = _e.TransformMode.MIRROR_AT_POINT
    """Define which method should be used to transform the position:"""
    FrameNo: int = 0
    """
    Defines the reference frame ID to which the "Position" that will be transformed is relative. •
    0: WCS (default) • 1..254: User frames
    """
    TargetFrameNo: int = 0
    """
    Defines the reference frame ID to which the "TransformedPosition" should be relative. • 0: WCS
    (default) • 1..254: User frames
    """
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute coordinates of the position that will be transformed in the selected coordinate systems
    (see input parameter CoordinateSystem).
    """


@_dataclass(kw_only=True, slots=True)
class SoftSwitchTcpOutCmd:
    """SoftSwitchTcpOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SoftMovement: bool = False
    """If TRUE, the RA is in a compliant movement."""


@_dataclass(kw_only=True, slots=True)
class SoftSwitchTcpParCmd:
    """SoftSwitchTcpParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """
    Defines type of reference coordinate system at which the robot can be moved in a compliant
    manner.
    """
    ReferenceNo: int = 0
    """
    Index of tool or frame according to ReferenceType. • 0 (default): Flange/WS • 1..254: Tool/User
    frames
    """
    CompliantAxes: int = 0
    """
    Relates to "LimitMode" with the setting "No limit defined". Defines for which cartesian axes the
    compliant motion is allowed. If TRUE, the direction is enabled. Default value is FALSE. See
    Table 6-744 for bit assignment.
    """
    LimitMode: _e.LimitMode = _e.LimitMode.NO_LIMIT_DEFINED
    """
    Defines which parameters will limit the space, where the robot complies (at least one option
    must be supported)
    """
    ResistanceForceMode: _e.ResistanceForceMode = _e.ResistanceForceMode.RESISTANCE_FORCE_TCP
    """Defines the type of the resistance force applied at the RA against the external force"""
    ResistanceForceTCP: float = 0.0
    """
    Relates to "ResistanceForceMode" with the setting "ResistanceForceTCP". Defines the resistance
    force level applied at the RA against the external force. • 0..99: Resistance is lower than
    robot vendor default. The lower the value, the easier the robot can be pushed away. • 100
    (default): The value is aligned with the robot vendor-specific default value. • 101..200:
    Resistance is higher than robot vendor default. At maximum value "200" highest possible
    resistance against external force
    """
    ResistanceForceAxis: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to "ResistanceForceMode" with the setting "ResistanceForceAxis". Defines the resistance
    force level of the RA at the respective cartesian axis. 0..99: Resistance is lower than robot
    vendor default. The lower the value, the easier the robot can be pushed away. • 100 (default):
    The value is aligned with the robot vendor-specific default value. • 101..200: Resistance is
    higher than robot vendor default. At maximum value "200" highest possible resistance against
    external force. Index: • [0]: X-Axis O • [1]: Y-axis O • [2]: Z-axis O • [3]: RX-Direction O •
    [4]: RY-direction O • [5]: RZ-direction
    """
    VectorData: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to "LimitMode" with the setting "Limit defined". Limit values in the selected cartesian
    coordinate system (see input parameters ReferenceType and ReferenceNo). "0" is (default) the
    origin of the vector, the TCP position, at the start position of the robot. See Table 6-742 for
    the parameter index assignment.
    """


@_dataclass(kw_only=True, slots=True)
class SoftSwitchTcpRecvData(RspHeader):
    """SoftSwitchTcpRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SoftMovement: bool = False
    """If TRUE, the RA is in a compliant movement."""


@_dataclass(kw_only=True, slots=True)
class SoftSwitchTcpSendData(CmdHeader):
    """SoftSwitchTcpSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LimitMode: _e.LimitMode = _e.LimitMode.NO_LIMIT_DEFINED
    """
    Defines which parameters will limit the space, where the robot complies (at least one option
    must be supported)
    """
    CompliantAxes: int = 0
    """
    Relates to "LimitMode" with the setting "No limit defined". Defines for which cartesian axes the
    compliant motion is allowed. If TRUE, the direction is enabled. Default value is FALSE. See
    Table 6-744 for bit assignment.
    """
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """
    Defines type of reference coordinate system at which the robot can be moved in a compliant
    manner.
    """
    ReferenceNo: int = 0
    """
    Index of tool or frame according to ReferenceType. • 0 (default): Flange/WS • 1..254: Tool/User
    frames
    """
    ResistanceForceTCP: int = 0
    """
    Relates to "ResistanceForceMode" with the setting "ResistanceForceTCP". Defines the resistance
    force level applied at the RA against the external force. • 0..99: Resistance is lower than
    robot vendor default. The lower the value, the easier the robot can be pushed away. • 100
    (default): The value is aligned with the robot vendor-specific default value. • 101..200:
    Resistance is higher than robot vendor default. At maximum value "200" highest possible
    resistance against external force
    """
    ResistanceForceAxis: list[int] = _field(default_factory=lambda: [0] * 6)
    """
    Relates to "ResistanceForceMode" with the setting "ResistanceForceAxis". Defines the resistance
    force level of the RA at the respective cartesian axis. 0..99: Resistance is lower than robot
    vendor default. The lower the value, the easier the robot can be pushed away. • 100 (default):
    The value is aligned with the robot vendor-specific default value. • 101..200: Resistance is
    higher than robot vendor default. At maximum value "200" highest possible resistance against
    external force. Index: • [0]: X-Axis O • [1]: Y-axis O • [2]: Z-axis O • [3]: RX-Direction O •
    [4]: RY-direction O • [5]: RZ-direction
    """
    VectorData: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to "LimitMode" with the setting "Limit defined". Limit values in the selected cartesian
    coordinate system (see input parameters ReferenceType and ReferenceNo). "0" is (default) the
    origin of the vector, the TCP position, at the start position of the robot. See Table 6-742 for
    the parameter index assignment.
    """
    ResistanceForceMode: _e.ResistanceForceMode = _e.ResistanceForceMode.RESISTANCE_FORCE_TCP
    """Defines the type of the resistance force applied at the RA against the external force"""


@_dataclass(kw_only=True, slots=True)
class StopSubprogramOutCmd:
    """StopSubprogramOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class StopSubprogramParCmd:
    """StopSubprogramParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    StopMode: _e.StopMode = _e.StopMode.STOP_JOB_ID
    """Defines how target subprogram is defined"""
    TargetID: int = 0
    """
    JobID or InstanceID of target subprogram according to selected StopMode • Refers to StopMode 0
    (Stop via JobID) and 1 (Stop via InstanceID). • -1: Invalid (default)
    """
    SequenceFlag: _e.SequenceFlag = _e.SequenceFlag.NO_SEQUENCE
    """Defines the target sequence in which the command will be executed"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) - No trigger related behavior • >0:
    Triggero - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class StopSubprogramRecvData(RspHeader):
    """StopSubprogramRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class StopSubprogramSendData(CmdHeader):
    """StopSubprogramSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) - No trigger related behavior • >0:
    Triggero - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    TargetID: int = 0
    """
    JobID or InstanceID of target subprogram according to selected StopMode • Refers to StopMode 0
    (Stop via JobID) and 1 (Stop via InstanceID). • -1: Invalid (default)
    """
    StopMode: int = 0
    """Defines how target subprogram is defined"""


@_dataclass(kw_only=True, slots=True)
class UnitMeasurementOutCmd:
    """UnitMeasurementOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasurementActive: bool = False
    """TRUE, while the measurement is active."""
    Result: float = 0.0
    """Measurement result depending on the measurement type setting of the "MeasuringMode"."""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class UnitMeasurementParCmd:
    """UnitMeasurementParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TriggerMode: _e.TriggerModeMeasurement = _e.TriggerModeMeasurement.NO_TRIGGER
    """
    Reaction type of measurement in relation to the trigger signal with the "ListenerID > 0" (at
    least one option must be supported):
    """
    NewMeasurement: bool = False
    """
    Relates to "TriggerMode" "No trigger related behavior". Set TRUE to start first measurement. Set
    TRUE again to receive new result data referring to previous rising edge of NewMeasurement.
    """
    MeasuringMode: _e.MeasuringUnitMode = _e.MeasuringUnitMode.VECTOR_LENGTH
    """
    Type of measurement (at least one option must be supported). If the parameter is changed during
    the active measurement, the RC returns an error
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class UnitMeasurementRecvData(RspHeader):
    """UnitMeasurementRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Result: float = 0.0
    """Measurement result depending on the measurement type setting of the "MeasuringMode"."""
    MeasurementActive: bool = False
    """TRUE, while the measurement is active."""
    ResultNo: int = 0
    """TRUE, when new result data was received from the RC."""


@_dataclass(kw_only=True, slots=True)
class UnitMeasurementSendData(CmdHeader):
    """UnitMeasurementSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    TriggerMode: _e.TriggerModeMeasurement = _e.TriggerModeMeasurement.NO_TRIGGER
    """
    Reaction type of measurement in relation to the trigger signal with the "ListenerID > 0" (at
    least one option must be supported):
    """
    MeasurementNo: int = 0
    """
    Relates to "TriggerMode" "No trigger related behavior". Set TRUE to start first measurement. Set
    TRUE again to receive new result data referring to previous rising edge of NewMeasurement.
    """
    MeasuringMode: _e.MeasuringUnitMode = _e.MeasuringUnitMode.VECTOR_LENGTH
    """
    Type of measurement (at least one option must be supported). If the parameter is changed during
    the active measurement, the RC returns an error
    """


@_dataclass(kw_only=True, slots=True)
class WriteCallSubprogramCyclicOutCmd:
    """WriteCallSubprogramCyclicOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteCallSubprogramCyclicParCmd:
    """WriteCallSubprogramCyclicParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Data: list[int] = _field(default_factory=lambda: [0] * 26)
    """Cyclic input data of subprogram"""


@_dataclass(kw_only=True, slots=True)
class MoveApproachDirectOutCmd:
    """MoveApproachDirectOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachDirectParCmd:
    """MoveApproachDirectParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachDirectRecvData(RspHeader):
    """MoveApproachDirectRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachDirectSendData(CmdHeader):
    """MoveApproachDirectSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachLinearOutCmd:
    """MoveApproachLinearOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachLinearParCmd:
    """MoveApproachLinearParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachLinearRecvData(RspHeader):
    """MoveApproachLinearRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveApproachLinearSendData(CmdHeader):
    """MoveApproachLinearSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveAxesRelativeOutCmd:
    """MoveAxesRelativeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveAxesRelativeParCmd:
    """MoveAxesRelativeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JointDistance: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Relative joint distance from the current or last target position to the end joint position"""
    VelocityRate: float = 0.0
    """
    Axes velocity in % of nominal velocity. • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveAxesRelativeRecvData(RspHeader):
    """MoveAxesRelativeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""


@_dataclass(kw_only=True, slots=True)
class MoveAxesRelativeSendData(CmdHeader):
    """MoveAxesRelativeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    Axes velocity in % of nominal velocity. • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    JointDistance: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Relative joint distance from the current or last target position to the end joint position"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve2: int = 0
    """Reserve"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularAbsoluteOutCmd:
    """MoveCircularAbsoluteOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularAbsoluteParCmd:
    """MoveCircularAbsoluteParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CircMode: _e.CircMode = _e.CircMode.BORDER
    """Specifies the meaning of the input parameter "AuxPoint"."""
    AuxPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Auxiliary position of the robot in the specified coordinate system, used in for the circle path
    calculation.
    """
    CircPlane: _e.CircPlane = _e.CircPlane.XZ_PLANE
    """Specifies the circle’s plane when CircMode = 2 is selected"""
    Tolerance: float = 0.0
    """
    Relates to CircMode =1: Permissible deviation of the distances from starting point to center
    point, from auxiliary point to center point and from end point to center point. These distances
    must be identical to travel a circular path. When the distance from a point to the center point
    is within the allowed deviation, the position of the center point is adjusted to the mean
    internally. If the deviation is greater than the specified Tolerance, the command returns an
    error. See also Figure 6-106.
    """
    EndPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute end position of the robot in the specified coordinate system. If "CircMode" = 2 this
    position is ignored
    """
    Angle: float = 0.0
    """
    Angle is only used when "CircMode" = 2. The circular angle defines the end position of the
    circular motion. The circular path is defined by the angle, the center point ("AuxPoint") and
    the actual position. Always positive
    """
    PathChoice: _e.PathChoice = _e.PathChoice.CLOCKWISE
    """Choice of the path"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularAbsoluteRecvData(RspHeader):
    """MoveCircularAbsoluteRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularAbsoluteSendData(CmdHeader):
    """MoveCircularAbsoluteSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Auxiliary position of the robot in the specified coordinate system, used in for the circle path
    calculation.
    """
    EndPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute end position of the robot in the specified coordinate system. If "CircMode" = 2 this
    position is ignored
    """
    CircMode: _e.CircMode = _e.CircMode.BORDER
    """Specifies the meaning of the input parameter "AuxPoint"."""
    CircPlane: _e.CircPlane = _e.CircPlane.XZ_PLANE
    """Specifies the circle’s plane when CircMode = 2 is selected"""
    Tolerance: float = 0.0
    """
    Relates to CircMode =1: Permissible deviation of the distances from starting point to center
    point, from auxiliary point to center point and from end point to center point. These distances
    must be identical to travel a circular path. When the distance from a point to the center point
    is within the allowed deviation, the position of the center point is adjusted to the mean
    internally. If the deviation is greater than the specified Tolerance, the command returns an
    error. See also Figure 6-106.
    """
    Angle: float = 0.0
    """
    Angle is only used when "CircMode" = 2. The circular angle defines the end position of the
    circular motion. The circular path is defined by the angle, the center point ("AuxPoint") and
    the actual position. Always positive
    """
    PathChoice: bool = False
    """Choice of the path"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Reserve2: int = 0
    """Reserve"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularCamOutCmd:
    """MoveCircularCamOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularCamParCmd:
    """MoveCircularCamParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CircMode: _e.CircMode = _e.CircMode.BORDER
    """Specifies the meaning of the input parameter "AuxPoint"."""
    AuxPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Auxiliary position of the robot in the specified coordinate system, used in for the circle path
    calculation.
    """
    CircPlane: _e.CircPlane = _e.CircPlane.XZ_PLANE
    """Specifies the circle’s plane when CircMode = 2 is selected"""
    Tolerance: float = 0.0
    """
    Relates to CircMode =1: Permissible deviation of the distances from starting point to center
    point, from auxiliary point to center point and from end point to center point. These distances
    must be identical to travel a circular path. When the distance from a point to the center point
    is within the allowed deviation, the position of the center point is adjusted to the mean
    internally. If the deviation is greater than the specified Tolerance, the command returns an
    error. See also Figure 6-106.
    """
    EndPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute end position of the robot in the specified coordinate system. If "CircMode" = 2 this
    position is ignored
    """
    Angle: float = 0.0
    """
    Angle is only used when "CircMode" = 2. The circular angle defines the end position of the
    circular motion. The circular path is defined by the angle, the center point ("AuxPoint") and
    the actual position. Always positive
    """
    PathChoice: _e.PathChoice = _e.PathChoice.CLOCKWISE
    """Choice of the path"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Index: int = 0
    """Specifies the desired byte address that shall be written"""
    OutputBitmask: int = 0
    """Specifies which output may be written"""
    Value: int = 0
    """Value of Digital Output"""
    RelativePosition: bool = False
    """
    Reference position for the trigger point (at least one option must be supported): • 0: Start
    position (default) O • 1: End position
    """
    TriggerDelay: int = 0
    """Time delay [ms] for the trigger point"""
    TriggerDistance: float = 0.0
    """
    Offset in percentage of the movement towards the trigger point in relation to the reference
    position
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularCamRecvData(RspHeader):
    """MoveCircularCamRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularCamSendData(CmdHeader):
    """MoveCircularCamSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Auxiliary position of the robot in the specified coordinate system, used in for the circle path
    calculation.
    """
    EndPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute end position of the robot in the specified coordinate system. If "CircMode" = 2 this
    position is ignored
    """
    TriggerDelay: int = 0
    """Time delay [ms] for the trigger point"""
    TriggerDistance: float = 0.0
    """
    Offset in percentage of the movement towards the trigger point in relation to the reference
    position
    """
    CircMode: _e.CircMode = _e.CircMode.BORDER
    """Specifies the meaning of the input parameter "AuxPoint"."""
    CircPlane: _e.CircPlane = _e.CircPlane.XZ_PLANE
    """Specifies the circle’s plane when CircMode = 2 is selected"""
    Tolerance: float = 0.0
    """
    Relates to CircMode =1: Permissible deviation of the distances from starting point to center
    point, from auxiliary point to center point and from end point to center point. These distances
    must be identical to travel a circular path. When the distance from a point to the center point
    is within the allowed deviation, the position of the center point is adjusted to the mean
    internally. If the deviation is greater than the specified Tolerance, the command returns an
    error. See also Figure 6-106.
    """
    Angle: float = 0.0
    """
    Angle is only used when "CircMode" = 2. The circular angle defines the end position of the
    circular motion. The circular path is defined by the angle, the center point ("AuxPoint") and
    the actual position. Always positive
    """
    PathChoice: bool = False
    """Choice of the path"""
    Index: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept Specifies the desired byte address that shall be written
    """
    RelativePosition: bool = False
    """
    Reference position for the trigger point (at least one option must be supported): • 0: Start
    position (default) O • 1: End position
    """
    OutputBitmask: int = 0
    """Specifies which output may be written"""
    Value: int = 0
    """Value of Digital Output"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Reserve: int = 0
    """Reseve"""
    MoveTime: int = 0
    """Time"""


@_dataclass(kw_only=True, slots=True)
class MoveCircularRelativeOutCmd:
    """MoveCircularRelativeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularRelativeParCmd:
    """MoveCircularRelativeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CircMode: _e.CircMode = _e.CircMode.BORDER
    """Specifies the meaning of the input parameter "AuxPoint"."""
    AuxPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Auxiliary position of the robot in the specified coordinate system, used in for the circle path
    calculation.
    """
    CircPlane: _e.CircPlane = _e.CircPlane.XZ_PLANE
    """Specifies the circle’s plane when CircMode = 2 is selected"""
    Tolerance: float = 0.0
    """
    Relates to CircMode =1: Permissible deviation of the distances from starting point to center
    point, from auxiliary point to center point and from end point to center point. These distances
    must be identical to travel a circular path. When the distance from a point to the center point
    is within the allowed deviation, the position of the center point is adjusted to the mean
    internally. If the deviation is greater than the specified Tolerance, the command returns an
    error. See also Figure 6-106.
    """
    EndPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute end position of the robot in the specified coordinate system. If "CircMode" = 2 this
    position is ignored
    """
    Angle: float = 0.0
    """
    Angle is only used when "CircMode" = 2. The circular angle defines the end position of the
    circular motion. The circular path is defined by the angle, the center point ("AuxPoint") and
    the actual position. Always positive
    """
    PathChoice: _e.PathChoice = _e.PathChoice.CLOCKWISE
    """Choice of the path"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularRelativeRecvData(RspHeader):
    """MoveCircularRelativeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveCircularRelativeSendData(CmdHeader):
    """MoveCircularRelativeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Auxiliary position of the robot in the specified coordinate system, used in for the circle path
    calculation.
    """
    EndPoint: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute end position of the robot in the specified coordinate system. If "CircMode" = 2 this
    position is ignored
    """
    CircMode: _e.CircMode = _e.CircMode.BORDER
    """Specifies the meaning of the input parameter "AuxPoint"."""
    CircPlane: _e.CircPlane = _e.CircPlane.XZ_PLANE
    """Specifies the circle’s plane when CircMode = 2 is selected"""
    Tolerance: float = 0.0
    """
    Relates to CircMode =1: Permissible deviation of the distances from starting point to center
    point, from auxiliary point to center point and from end point to center point. These distances
    must be identical to travel a circular path. When the distance from a point to the center point
    is within the allowed deviation, the position of the center point is adjusted to the mean
    internally. If the deviation is greater than the specified Tolerance, the command returns an
    error. See also Figure 6-106.
    """
    Angle: float = 0.0
    """
    Angle is only used when "CircMode" = 2. The circular angle defines the end position of the
    circular motion. The circular path is defined by the angle, the center point ("AuxPoint") and
    the actual position. Always positive
    """
    PathChoice: bool = False
    """Choice of the path"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: bool = False
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """Time"""


@_dataclass(kw_only=True, slots=True)
class MoveDepartDirectOutCmd:
    """MoveDepartDirectOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDepartDirectParCmd:
    """MoveDepartDirectParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDepartDirectRecvData(RspHeader):
    """MoveDepartDirectRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveDepartDirectSendData(CmdHeader):
    """MoveDepartDirectSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    ReferenceType: bool = False
    """Defines type of reference coordinate system of the offset position"""
    MoveTime: int = 0
    """Time"""


@_dataclass(kw_only=True, slots=True)
class MoveDepartLinearOutCmd:
    """MoveDepartLinearOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDepartLinearParCmd:
    """MoveDepartLinearParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDepartLinearRecvData(RspHeader):
    """MoveDepartLinearRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveDepartLinearSendData(CmdHeader):
    """MoveDepartLinearSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Offset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    AuxCornerDistance: float = 0.0
    """
    Define blending sphere with radius around auxiliary position. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the second segment of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity, Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    ReferenceType: bool = False
    """Defines type of reference coordinate system of the offset position"""
    MoveTime: int = 0
    """Time"""


@_dataclass(kw_only=True, slots=True)
class MoveDirectOffsetOutCmd:
    """MoveDirectOffsetOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectOffsetParCmd:
    """MoveDirectOffsetParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferencePosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute reference coordinates in the selected coordinate system (see input parameters ToolNo
    and FrameNo).
    """
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from ReferencePosition."""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement.
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectOffsetRecvData(RspHeader):
    """MoveDirectOffsetRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectOffsetSendData(CmdHeader):
    """MoveDirectOffsetSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    ReferencePosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute reference coordinates in the selected coordinate system (see input parameters ToolNo
    and FrameNo).
    """
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from ReferencePosition."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve2: int = 0
    """Reserve2"""
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectRelativeOutCmd:
    """MoveDirectRelativeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectRelativeParCmd:
    """MoveDirectRelativeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Distance: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from the current or last target position to the end point."""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectRelativeRecvData(RspHeader):
    """MoveDirectRelativeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectRelativeSendData(CmdHeader):
    """MoveDirectRelativeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    Reserve2: int = 0
    """Reserver"""
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    Distance: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from the current or last target position to the end point."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve3: int = 0
    """Reserve3"""
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteJOutCmd:
    """MoveLinearAbsoluteJOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteJParCmd:
    """MoveLinearAbsoluteJParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute end position of the robot in Joint position."""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteJRecvData(RspHeader):
    """MoveLinearAbsoluteJRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteJSendData(CmdHeader):
    """MoveLinearAbsoluteJSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute end position of the robot in Joint position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearCamOutCmd:
    """MoveLinearCamOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearCamParCmd:
    """MoveLinearCamParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Index: int = 0
    """Specifies the desired byte address that shall be written"""
    OutputBitmask: int = 0
    """Specifies which output may be written"""
    Value: int = 0
    """Value of Digital Output"""
    RelativePosition: bool = False
    """
    Reference position for the trigger point (at least one option must be supported): • 0: Start
    position (default) O • 1: End position
    """
    TriggerDelay: int = 0
    """Time delay [ms] for the trigger point"""
    TriggerDistance: float = 0.0
    """Offset in millimeters towards the trigger point in relation to the reference position"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearCamRecvData(RspHeader):
    """MoveLinearCamRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearCamSendData(CmdHeader):
    """MoveLinearCamSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    TriggerDelay: int = 0
    """Time delay [ms] for the trigger point"""
    TriggerDistance: float = 0.0
    """Offset in millimeters towards the trigger point in relation to the reference position"""
    Index: int = 0
    """Specifies the desired byte address that shall be written"""
    RelativePosition: bool = False
    """
    Reference position for the trigger point (at least one option must be supported): • 0: Start
    position (default) O • 1: End position
    """
    OutputBitmask: int = 0
    """Specifies which output may be written"""
    Value: int = 0
    """Value of Digital Output"""
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    TurnMode: int = 0
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearOffsetOutCmd:
    """MoveLinearOffsetOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearOffsetParCmd:
    """MoveLinearOffsetParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferencePosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute reference coordinates in the selected coordinate system (see input parameters ToolNo
    and FrameNo).
    """
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from ReferencePosition."""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position."""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearOffsetRecvData(RspHeader):
    """MoveLinearOffsetRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearOffsetSendData(CmdHeader):
    """MoveLinearOffsetSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    ReferencePosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute reference coordinates in the selected coordinate system (see input parameters ToolNo
    and FrameNo).
    """
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from ReferencePosition."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve2: int = 0
    """Reserve2"""
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearRelativeOutCmd:
    """MoveLinearRelativeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearRelativeParCmd:
    """MoveLinearRelativeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Distance: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from the current or last target position to the end point"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position."""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearRelativeRecvData(RspHeader):
    """MoveLinearRelativeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearRelativeSendData(CmdHeader):
    """MoveLinearRelativeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    Distance: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from the current or last target position to the end point"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceDirectOutCmd:
    """MovePickPlaceDirectOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceDirectParCmd:
    """MovePickPlaceDirectParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    ApproachOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    DepartOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from actual Position"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    AuxCornerDistance_1: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 1. For exact stop define
    AuxCornerDistance = 0
    """
    AuxCornerDistance_2: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 2. For exact stop define
    AuxCornerDistance = 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the linear segments of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity. Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    ReductionRate: float = 0.0
    """
    TCP velocity in % of the velocity set with VelocityRate to define the velocity for the linear
    motions. Always positive. • 0%: use the minimal velocity • 100%: use the velocity set with
    VelocityRate
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceDirectRecvData(RspHeader):
    """MovePickPlaceDirectRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceDirectSendData(CmdHeader):
    """MovePickPlaceDirectSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    ApproachOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    DepartOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from actual Position"""
    AuxCornerDistance_1: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 1. For exact stop define
    AuxCornerDistance = 0
    """
    AuxCornerDistance_2: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 2. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the linear segments of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity. Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceLinearOutCmd:
    """MovePickPlaceLinearOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceLinearParCmd:
    """MovePickPlaceLinearParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    ApproachOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    DepartOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from actual Position"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position"""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    AuxCornerDistance_1: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 1. For exact stop define
    AuxCornerDistance = 0
    """
    AuxCornerDistance_2: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 2. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the linear segments of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity. Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceLinearRecvData(RspHeader):
    """MovePickPlaceLinearRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MovePickPlaceLinearSendData(CmdHeader):
    """MovePickPlaceLinearSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    TargetPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    ApproachOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from TargetPosition"""
    DepartOffset: AuxOffset = _field(default_factory=lambda: AuxOffset())
    """Offset distance of auxiliary position from actual Position"""
    AuxCornerDistance_1: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 1. For exact stop define
    AuxCornerDistance = 0
    """
    AuxCornerDistance_2: float = 0.0
    """
    Define blending sphere with radius around auxiliary position 2. For exact stop define
    AuxCornerDistance = 0
    """
    VelocityCoefficient: float = 0.0
    """
    Factor by which VelocityRate is multiplied to define the velocity for the linear segments of the
    motion. Always positive. • 0: use the minimal velocity • 1: use the velocity set with
    VelocityRate Input values below 1 to reduce velocity. Input values above 1 to increase velocity.
    See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class ChangeSpeedOverrideOutCmd:
    """ChangeSpeedOverrideOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ChangeSpeedOverrideParCmd:
    """ChangeSpeedOverrideParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Override: float = 5.0
    """
    Set value for override • 0% No movement of the robot • 10% default • ≤100%: use input parameter
    value
    """


@_dataclass(kw_only=True, slots=True)
class ChangeSpeedOverrideRecvData(RspHeader):
    """ChangeSpeedOverrideRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ChangeSpeedOverrideSendData(CmdHeader):
    """ChangeSpeedOverrideSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Override: int = 0
    """
    Set value for override • 0% No movement of the robot • 10% default • ≤100%: use input parameter
    value
    """


@_dataclass(kw_only=True, slots=True)
class GroupContinueOutCmd:
    """GroupContinueOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupContinueParCmd:
    """GroupContinueParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupContinueRecvData(RspHeader):
    """GroupContinueRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupContinueSendData(CmdHeader):
    """GroupContinueSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupInterruptOutCmd:
    """GroupInterruptOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupInterruptParCmd:
    """GroupInterruptParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupInterruptRecvData(RspHeader):
    """GroupInterruptRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupInterruptSendData(CmdHeader):
    """GroupInterruptSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupJogOutCmd:
    """GroupJogOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DistanceReached: bool = False
    """
    Relates to Incremental mode ON: TRUE, when robot’s TCP or axes have traversed distance of
    "IncrementalTranslation" or "IncrementalRotation"
    """
    MotionActive: bool = False
    """The command takes control of the motion of the according axis group"""


@_dataclass(kw_only=True, slots=True)
class GroupJogParCmd:
    """GroupJogParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.JogMode = _e.JogMode.JOG_FRAME
    """Specifies in which mode the robot is jogged"""
    Override: int = 5
    """
    Velocity in % of monitoring speed or ReferenceVelocity, depending on the currently active
    operation mode (T1 External/T2 External: Monitoring speed; Automatic External: ReferenceVelocity
    ) • 0%: No movement of the robot • 10%: default • ≤100%: use input parameter value
    """
    Control: JogControl = _field(default_factory=lambda: JogControl())
    """Change to jog and define direction according to Mode. See Table 6-223"""
    ToolNo: int = 0
    """
    Relates to Mode 0 (JogFrame) and 1 (JogTool) Index of tool • 0: Flange (default): • 1..254: Tool
    frames
    """
    FrameNo: int = 0
    """Relates to Mode 0 (JogFrame) Index of frame • 0: WCS (default) • 1..254: User frames"""
    IncrementalTranslation: float = 0.0
    """
    Increments for jogging translational axes for defined distance • 0: Incremental mode OFF
    (default) - Movement is active until "Control" is reset, or error occurs. • >0: Incremental mode
    ON - Movement is active until distance defined by input value is reached without changes to
    "Control", "Control" is reset, or error occurs
    """
    IncrementalRotation: float = 0.0
    """
    Increments for jogging rotational axes for defined distance • 0: Incremental mode OFF (default)
    - Movement is active until "Control" is reset, or error occurs. • >0 Incremental mode ON: -
    Movement is active until distance defined by input value is reached without changes to
    "Control", "Control" is reset, or error occurs
    """


@_dataclass(kw_only=True, slots=True)
class GroupJogRecvData(RspHeader):
    """GroupJogRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Status: int = 0
    """Status"""


@_dataclass(kw_only=True, slots=True)
class GroupJogSendData(CmdHeader):
    """GroupJogSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enable: bool = False
    Reserve: int = 0
    """Reserve"""
    ToolNo: int = 0
    """
    Relates to Mode 0 (JogFrame) and 1 (JogTool) Index of tool • 0: Flange (default): • 1..254: Tool
    frames
    """
    FrameNo: int = 0
    """Relates to Mode 0 (JogFrame) Index of frame • 0: WCS (default) • 1..254: User frames"""
    Mode: _e.JogMode = _e.JogMode.JOG_FRAME
    """Specifies in which mode the robot is jogged"""
    Reserve2: int = 0
    """Reserve"""
    IncrementalTranslation: float = 0.0
    """
    Increments for jogging translational axes for defined distance • 0: Incremental mode OFF
    (default) - Movement is active until "Control" is reset, or error occurs. • >0: Incremental mode
    ON - Movement is active until distance defined by input value is reached without changes to
    "Control", "Control" is reset, or error occurs
    """
    IncrementalRotation: float = 0.0
    """
    Increments for jogging rotational axes for defined distance • 0: Incremental mode OFF (default)
    - Movement is active until "Control" is reset, or error occurs. • >0 Incremental mode ON: -
    Movement is active until distance defined by input value is reached without changes to
    "Control", "Control" is reset, or error occurs
    """
    Override: int = 0
    """
    Velocity in % of monitoring speed or ReferenceVelocity, depending on the currently active
    operation mode (T1 External/T2 External: Monitoring speed; Automatic External: ReferenceVelocity
    ) • 0%: No movement of the robot • 10%: default • ≤100%: use input parameter value
    """
    JogControl: list[int] = _field(default_factory=lambda: [0] * 3)
    """Change to jog and define direction according to Mode. See Table 6-223"""


@_dataclass(kw_only=True, slots=True)
class GroupStopOutCmd:
    """GroupStopOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupStopParCmd:
    """GroupStopParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupStopRecvData(RspHeader):
    """GroupStopRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupStopSendData(CmdHeader):
    """GroupStopSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class MoveAxesAbsoluteOutCmd:
    """MoveAxesAbsoluteOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveAxesAbsoluteParCmd:
    """MoveAxesAbsoluteParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute end position of the robot in Joint position."""
    VelocityRate: float = 0.0
    """
    Axes velocity in % of nominal velocity. • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveAxesAbsoluteRecvData(RspHeader):
    """MoveAxesAbsoluteRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""


@_dataclass(kw_only=True, slots=True)
class MoveAxesAbsoluteSendData(CmdHeader):
    """MoveAxesAbsoluteSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    Axes velocity in % of nominal velocity. • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute end position of the robot in Joint position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve2: int = 0
    """Reserve"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectAbsoluteOutCmd:
    """MoveDirectAbsoluteOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectAbsoluteParCmd:
    """MoveDirectAbsoluteParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectAbsoluteRecvData(RspHeader):
    """MoveDirectAbsoluteRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveDirectAbsoluteSendData(CmdHeader):
    """MoveDirectAbsoluteSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    Reserve2: int = 0
    """Reserve"""
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo).
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    Reserve3: int = 0
    """Reserve"""
    Reserve4: int = 0
    """Reserve"""
    MoveTime: int = 0
    """Time"""


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteOutCmd:
    """MoveLinearAbsoluteOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by the user. For
    more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteParCmd:
    """MoveLinearAbsoluteParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteRecvData(RspHeader):
    """MoveLinearAbsoluteRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveLinearAbsoluteSendData(CmdHeader):
    """MoveLinearAbsoluteSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [10.0, 0.0])
    """Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius"""
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Relative distance and rotation from the current or last target position to the end point."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    Reserve2: int = 0
    """Reserve2"""
    Reserve3: int = 0
    """Reserve3"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """


@_dataclass(kw_only=True, slots=True)
class ReturnToPrimaryOutCmd:
    """ReturnToPrimaryOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    PrimaryPosToolNo: int = 0
    """Tool index of target position of ReturnToPrimary • 0: Flange • 1..254: Tool frames"""
    PrimaryPosFrameNo: int = 0
    """Frame index of target position of ReturnToPrimary • 0: WCS • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class ReturnToPrimaryParCmd:
    """ReturnToPrimaryParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReturnMode: _e.ReturnMode = _e.ReturnMode.INTERRUPT_POSITION
    """
    Defines target position when function is executed: • 0: Interrupt position (default) - Returns
    to position active, when interrupt was executed • 1: End position - Returns to target position
    of interrupted segment
    """
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    DistanceLimit: float = 0.0
    """
    Parameter is used if it is greater than 0 (default): Maximum allowed distance between current
    position and target position according to ReturnMode. If calculated distance is beyond specified
    Limit, RC returns an error
    """
    TrajectoryMode: _e.TrajectoryMode = _e.TrajectoryMode.INVALID
    """Defines type of command movement. One of the optional modes must be supported"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    AllowDifferences: bool = False
    """
    Set TRUE to deactivate comparison of • ToolData and FrameData • ToolNo and PrimaryPosToolNo •
    FrameNo and PrimaryPosFrameNo
    """


@_dataclass(kw_only=True, slots=True)
class ReturnToPrimaryRecvData(RspHeader):
    """ReturnToPrimaryRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    PrimaryPosToolNo: int = 0
    """Tool index of target position of ReturnToPrimary • 0: Flange • 1..254: Tool frames"""
    PrimaryPosFrameNo: int = 0
    """Frame index of target position of ReturnToPrimary • 0: WCS • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class ReturnToPrimarySendData(CmdHeader):
    """ReturnToPrimarySendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    DistanceLimit: float = 0.0
    """
    Parameter is used if it is greater than 0 (default): Maximum allowed distance between current
    position and target position according to ReturnMode. If calculated distance is beyond specified
    Limit, RC returns an error
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default) • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC if the
    time cannot be kept
    """
    ReturnMode: bool = False
    """
    Defines target position when function is executed: • 0: Interrupt position (default) - Returns
    to position active, when interrupt was executed • 1: End position - Returns to target position
    of interrupted segment
    """
    TrajectoryMode: bool = False
    """Defines type of command movement. One of the optional modes must be supported"""
    Enable: bool = False
    AllowDifferences: bool = False


@_dataclass(kw_only=True, slots=True)
class CalculateCartesianPositionOutCmd:
    """CalculateCartesianPositionOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetToolNoReturn: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    TargetFrameNoReturn: int = 0
    """Index of target frame • 0: WCS • 1..254: User frames"""
    CartesianPositionReturn: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Calculated cartesian position"""


@_dataclass(kw_only=True, slots=True)
class CalculateCartesianPositionParCmd:
    """CalculateCartesianPositionParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FrameNo: int = 0
    """Index of initial frame • 0: WCS (default) • 1..254: User frames"""
    TargetFrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Robot cartesian position."""


@_dataclass(kw_only=True, slots=True)
class CalculateCartesianPositionRecvData(RspHeader):
    """CalculateCartesianPositionRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetToolNoReturn: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    TargetFrameNoReturn: int = 0
    """Index of target frame • 0: WCS • 1..254: User frames"""
    CartesianPositionReturn: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Calculated cartesian position"""


@_dataclass(kw_only=True, slots=True)
class CalculateCartesianPositionSendData(CmdHeader):
    """CalculateCartesianPositionSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FrameNo: int = 0
    """Index of source frame • 0: WCS (default) • 1..254: User frames"""
    TargetFrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Robot cartesian position."""


@_dataclass(kw_only=True, slots=True)
class CalculateForwardKinematicOutCmd:
    """CalculateForwardKinematicOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetToolNoReturn: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    TargetFrameNoReturn: int = 0
    """Index of target frame • 0: WCS • 1..254: User frames"""
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Calculated cartesian position"""


@_dataclass(kw_only=True, slots=True)
class CalculateForwardKinematicParCmd:
    """CalculateForwardKinematicParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Calculate joint position"""


@_dataclass(kw_only=True, slots=True)
class CalculateForwardKinematicRecvData(RspHeader):
    """CalculateForwardKinematicRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetToolNoReturn: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    TargetFrameNoReturn: int = 0
    """Index of target frame • 0: WCS • 1..254: User frames"""
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Calculated cartesian position"""


@_dataclass(kw_only=True, slots=True)
class CalculateForwardKinematicSendData(CmdHeader):
    """CalculateForwardKinematicSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Calculated joint position"""


@_dataclass(kw_only=True, slots=True)
class CalculateFrameOutCmd:
    """CalculateFrameOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    IEC_Date: int = 0
    """Date"""
    IEC_TIME: int = 0
    """Time"""
    ReferenceFrame: int = 0
    """
    Index of frame on which the calculated frame is depending • 0: WCS (default) • 1..254: User
    frames
    """
    Position: RobotCartesianPositionBase = _field(default_factory=lambda: RobotCartesianPositionBase())
    """Position"""


@_dataclass(kw_only=True, slots=True)
class CalculateFrameParCmd:
    """CalculateFrameParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.FrameCalculationMode = _e.FrameCalculationMode.THREE_POINT_METHOD
    """Define which method should be used to calculate the tool frame"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    Position_X: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Cartesian position in the positive direction of the X-Axis of the calculated frame coordinate
    system relative to the given frame
    """
    Position_XY: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Cartesian position in the XY-plane of the calculated frame coordinate system relative to the
    given frame.
    """
    Origin: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Cartesian position of the origin of the calculated frame coordinate system relative to the given
    frame.
    """
    OriginShift: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Cartesian position of the postponement of the origin of the calculated frame coordinate system
    relative to the given frame. Auxiliary position if the origin of the can’t be reached by the
    robot, i.e. because it is inside an object.
    """
    ReferenceFrame: int = 0
    """
    Index of frame on which the calculated frame is depending • 0: WCS (default) • 1..254: User
    frames
    """


@_dataclass(kw_only=True, slots=True)
class CalculateFrameRecvData(RspHeader):
    """CalculateFrameRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    IEC_Date: int = 0
    """Date"""
    IEC_TIME: int = 0
    """Time"""
    ReferenceFrame: int = 0
    """
    Index of frame on which the calculated frame is depending • 0: WCS (default) • 1..254: User
    frames
    """
    Reserve: int = 0
    """Reserve"""
    Position: RobotCartesianPositionBase = _field(default_factory=lambda: RobotCartesianPositionBase())
    """Position"""


@_dataclass(kw_only=True, slots=True)
class CalculateFrameSendData(CmdHeader):
    """CalculateFrameSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DataIndex: int = 0
    """
    Incremented with each position of the input parameter "PositionsArray" sent from the PLC to the
    RC. Default: 0
    """
    DataComplete: int = 0
    """
    Set TRUE by the client, when according to the user selected "Mode" the final position of the
    input parameter "PositionsArray" is sent to the RC. Default: FALSE
    """
    Reserve: int = 0
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    ReferenceFrame: int = 0
    """
    Index of frame on which the calculated frame is depending • 0: WCS (default) • 1..254: User
    frames
    """
    Mode: int = 0
    """
    Define which method should be used to calculate the frame coordinate system: M • 0: Three-Point-
    Method (default) O • 1: Four-Point-Method O • 2: One-Point-Method
    """
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Cartesian position"""


@_dataclass(kw_only=True, slots=True)
class CalculateInverseKinematicOutCmd:
    """CalculateInverseKinematicOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Calculated robot joint position"""


@_dataclass(kw_only=True, slots=True)
class CalculateInverseKinematicParCmd:
    """CalculateInverseKinematicParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """cartesian position"""
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class CalculateInverseKinematicRecvData(RspHeader):
    """CalculateInverseKinematicRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Calculated robot joint position"""


@_dataclass(kw_only=True, slots=True)
class CalculateInverseKinematicSendData(CmdHeader):
    """CalculateInverseKinematicSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """cartesian position"""
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class CalculateToolOutCmd:
    """CalculateToolOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolData: _s.ToolData = _field(default_factory=lambda: ToolData())
    """Tool data"""
    TCPMaxError: float = 0.0
    """
    Maximum error of deviation of the TCP position from the fix point in world coordinate system If
    not supported: • -1
    """
    TCPMeanError: float = 0.0
    """
    Average error of TCP position from the fix point in world coordinate system If not supported: •
    -1
    """


@_dataclass(kw_only=True, slots=True)
class CalculateToolParCmd:
    """CalculateToolParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.ToolCalculationMode = _e.ToolCalculationMode.TWO_POINT_Z_METHOD
    """Define which method should be used to calculate the tool frame"""
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    ExternalTCP: bool = False
    """• True: Tool fixed • False: Tool on flange (default)"""
    PositionsArray: list[RobotCartesianPosition] = _field(default_factory=lambda: [RobotCartesianPosition() for _ in range(6)])
    """Positions in cartesian coordinates for the tool frame calculation."""


@_dataclass(kw_only=True, slots=True)
class CalculateToolRecvData(RspHeader):
    """CalculateToolRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TCPMaxError: float = 0.0
    """
    Maximum error of deviation of the TCP position from the fix point in world coordinate system If
    not supported: • -1
    """
    TCPMeanError: float = 0.0
    """
    Average error of TCP position from the fix point in world coordinate system If not supported: •
    -1
    """
    ToolData: _s.ToolData = _field(default_factory=lambda: ToolData())
    """Tool data"""


@_dataclass(kw_only=True, slots=True)
class CalculateToolSendData(CmdHeader):
    """CalculateToolSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DataIndex: int = 0
    DataComplete: int = 0
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""
    Mode: _e.ToolCalculationMode = _e.ToolCalculationMode.TWO_POINT_Z_METHOD
    """Define which method should be used to calculate the tool frame"""
    ExternalTCP: int = 0
    """• True: Tool fixed • False: Tool on flange (default)"""
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Positions in cartesian coordinates for the tool frame calculation."""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementAutomaticOutCmd:
    """LoadMeasurementAutomaticOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """FB is returning a unique ID for the cal led measurement."""
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Measured load data (see chapter 5.5.6.4)"""
    LoadDataAvailable: bool = False
    """Load data available"""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementAutomaticParCmd:
    """LoadMeasurementAutomaticParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.LoadMeasurementMode = _e.LoadMeasurementMode.ONE_POSITION
    """Define which method should be used to measure the load data"""
    Mass: float = 0.0
    """Define which mass is expected as a result of the load measurement"""
    Area_J3: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 3. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Area_J4: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 4. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Area_J5: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 5. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Area_J6: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 6. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Position_1: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Define the first position for the load measurement. Only considered with "Mode" = 0, 1."""
    Position_2: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Define the second position for the load measurement. Only considered with "Mode" = 3."""
    ConfigurationAngle: float = 0.0
    """Define the configuration angle for the load measurement. Only considered with "Mode" = 1."""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementAutomaticRecvData(RspHeader):
    """LoadMeasurementAutomaticRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """FB is returning a unique ID for the cal led measurement."""
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Measured load data (see chapter 5.5.6.4)"""
    LoadDataAvailable: bool = False
    """Load data available"""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementAutomaticSendData(CmdHeader):
    """LoadMeasurementAutomaticSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mass: float = 0.0
    """Define which mass is expected as a result of the load measurement"""
    Mode: _e.LoadMeasurementMode = _e.LoadMeasurementMode.ONE_POSITION
    """Define which method should be used to measure the load data"""
    Reserved: int = 0
    """Reserved"""
    Area_J3: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 3. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Area_J4: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 4. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Area_J5: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 5. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    Area_J6: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Define the area for the allowed motion of the Joint 6. The order of the two limit values does
    not matter. Only considered with "Mode" = 0, 2.
    """
    ConfigurationAngle: float = 0.0
    """Define the configuration angle for the load measurement. Only considered with "Mode" = 1."""
    Position_1: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Define the first position for the load measurement. Only considered with "Mode" = 0, 1."""
    Position_2: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Define the second position for the load measurement. Only considered with "Mode" = 3."""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementSequentialOutCmd:
    """LoadMeasurementSequentialOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """FB is returning a unique ID for the cal led measurement."""
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Measured load data (see chapter 5.5.6.4)"""
    LoadDataAvailable: bool = False
    """Load data available"""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementSequentialParCmd:
    """LoadMeasurementSequentialParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.LoadMeasurementSteps = _e.LoadMeasurementSteps.RESET
    """Define which step of the load estimation should be executed:"""
    Mass: float = 0.0
    """Define which mass is expected as a result of the load measurement"""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementSequentialRecvData(RspHeader):
    """LoadMeasurementSequentialRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuringID: int = 0
    """FB is returning a unique ID for the cal led measurement."""
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Measured load data (see chapter 5.5.6.4)"""
    LoadDataAvailable: bool = False
    """Load data available"""


@_dataclass(kw_only=True, slots=True)
class LoadMeasurementSequentialSendData(CmdHeader):
    """LoadMeasurementSequentialSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mass: float = 0.0
    """Define which mass is expected as a result of the load measurement"""
    Mode: _e.LoadMeasurementSteps = _e.LoadMeasurementSteps.RESET
    """Define which step of the load estimation should be executed:"""


@_dataclass(kw_only=True, slots=True)
class ActivateConveyorTrackingOutCmd:
    """ActivateConveyorTrackingOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TrackingStatus: _s.TrackingStatus = _field(default_factory=lambda: TrackingStatus())
    """Current status of "ConveyorTracking" according to Table 6-432"""
    RCEncoderValue: float = 0.0
    """
    Relates to "ConnectionMode" 1 – "RC connected": Traveled distance of assigned conveyor since
    ConveyorTracking has been activated (offset)
    """


@_dataclass(kw_only=True, slots=True)
class ActivateConveyorTrackingParCmd:
    """ActivateConveyorTrackingParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    ConnectionMode: _e.ConnectionMode = _e.ConnectionMode.RC_CONNECTED
    """Specifies encoder connection setup (at least one option must be supported)"""
    PLCEncoderValue: float = 0.0
    """
    Relates to "ConnectionMode" 1 – "PLC connected": Value of the encoder connected to the conveyor
    belt
    """


@_dataclass(kw_only=True, slots=True)
class ActivateConveyorTrackingRecvData(RspHeader):
    """ActivateConveyorTrackingRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TrackingStatus: _s.TrackingStatus = _field(default_factory=lambda: TrackingStatus())
    """
    Maximum error of deviation of the TCP position from the fix point in world coordinate system If
    not supported: • -1
    """


@_dataclass(kw_only=True, slots=True)
class ActivateConveyorTrackingSendData(CmdHeader):
    """ActivateConveyorTrackingSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    ConnectionMode: int = 0
    """Specifies encoder connection setup (at least one option must be supported)"""


@_dataclass(kw_only=True, slots=True)
class ConfigureConveyorOutCmd:
    """ConfigureConveyorOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ConfigureConveyorParCmd:
    """ConfigureConveyorParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    ConveyorOrigin: FrameData = _field(default_factory=lambda: FrameData())
    """
    Define the origin coordinate system of the conveyor belt, with the X-Axis pointing in the
    direction of the movement of the conveyor belt.
    """
    ConveyorType: _e.ConveyorType = _e.ConveyorType.LINEAR_CONVEYOR_TRACKING
    """Define the type of the conveyor"""
    Radius: float = 0.0
    """Relates to "ConveyorType" "Circular Tracking": Define the radius of the circular conveyor"""
    StartDistance: float = 0.0
    """Distance [mm] from the origin of the conveyor belt to the beginning of the "SyncInZone" """
    EndDistance: float = 0.0
    """Distance [mm] from the origin of the conveyor belt to the end of the "SyncOutZone" """
    SyncInLength: float = 0.0
    """Define the length of the "SyncInZone" """
    SyncOutLength: float = 0.0
    """Define the length of the "SyncOutZone" """


@_dataclass(kw_only=True, slots=True)
class ConfigureConveyorRecvData(RspHeader):
    """ConfigureConveyorRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ConfigureConveyorSendData(CmdHeader):
    """ConfigureConveyorSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorOrigin: FrameData = _field(default_factory=lambda: FrameData())
    """
    Define the origin coordinate system of the conveyor belt, with the X-Axis pointing in the
    direction of the movement of the conveyor belt.
    """
    ConveyorOriginAvailable: bool = False
    """ConveyorOrigin available"""
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    ConveyorType: _e.ConveyorType = _e.ConveyorType.LINEAR_CONVEYOR_TRACKING
    """Define the type of the conveyor"""
    Radius: float = 0.0
    """Relates to "ConveyorType" "Circular Tracking": Define the radius of the circular conveyor"""
    StartDistance: float = 0.0
    """Distance [mm] from the origin of the conveyor belt to the beginning of the "SyncInZone" """
    EndDistance: float = 0.0
    """Distance [mm] from the origin of the conveyor belt to the end of the "SyncOutZone" """
    SyncInLength: float = 0.0
    """Define the length of the "SyncInZone" """
    SyncOutLength: float = 0.0
    """Define the length of the "SyncOutZone" """


@_dataclass(kw_only=True, slots=True)
class RedefineTrackingPosOutCmd:
    """RedefineTrackingPosOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class RedefineTrackingPosParCmd:
    """RedefineTrackingPosParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    InitObjectPosition: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ListenerID = 0: Define initial work piece position relative to the conveyor belt
    origin: • Origin (X, Y, Z in mm) • Orientation (RX, RY, RZ in degree) For more information refer
    to chapter 5.5.14.
    """
    TrackingOffset: float = 0.0
    """
    Relates to ListenerID = 0: Travel distance of assigned UCS between work piece detection
    (InitObjectPosition) and execution of this command.
    """
    StartIndexInitPosition: int = 0
    """
    Relates to ListenerID >0 Start index of real registers containing InitObjectPosition for
    trigger-based execution.
    """
    FrameNo: int = 0
    """
    Define the index number of the UCS that is assigned to the conveyor by the function
    "ConveyorTracking". For more information refer to chapter 5.5.14.
    """
    IndexTrackingOffset: int = 0
    """
    Relates to ListenerID >0 Index of real register containing TrackingOffset for trigger-based
    execution
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default): No trigger related behavior • >0:
    Trigger: o Start executing, when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class RedefineTrackingPosRecvData(RspHeader):
    """RedefineTrackingPosRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    Reserved: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class RedefineTrackingPosSendData(CmdHeader):
    """RedefineTrackingPosSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """EmitterID"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default): No trigger related behavior • >0:
    Trigger: o Start executing, when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    StartIndexInitPosition: int = 0
    """
    Relates to ListenerID >0 Start index of real registers containing InitObjectPosition for
    trigger-based execution.
    """
    TrackingOffset: float = 0.0
    """
    Relates to ListenerID = 0: Travel distance of assigned UCS between work piece detection
    (InitObjectPosition) and execution of this command.
    """
    FrameNo: int = 0
    """
    Define the index number of the UCS that is assigned to the conveyor by the function
    "ConveyorTracking". For more information refer to chapter 5.5.14.
    """
    IndexTrackingOffset: int = 0
    """
    Relates to ListenerID >0 Index of real register containing TrackingOffset for trigger-based
    execution
    """


@_dataclass(kw_only=True, slots=True)
class SyncToConveyorOutCmd:
    """SyncToConveyorOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InSync: bool = False
    """The TCP is in synchronization with the object on the conveyor belt."""


@_dataclass(kw_only=True, slots=True)
class SyncToConveyorParCmd:
    """SyncToConveyorParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    SyncInMode: _e.SyncInMode = _e.SyncInMode.IN_SYNC_IN_ZONE
    """Defines when synchronization starts."""
    SyncInParameter: float = 0.0
    """
    Relates to "SyncInMode" "After distance" (1) and "After time" (2): Parameter for the
    synchronization • "After distance" (1) • Distance in mm • "After time" (2) / • Time in ms
    """
    MaxVelocity: float = 0.0
    """
    Define the maximum adjustment velocity for the robot to catch up to the conveyor belt. The
    velocity must be greater than the velocity of the conveyor belt. • 0 (default): no limit o No
    conveyor tracking specific limit o RC internal limit applies • >0: use limit o Conveyor tracking
    specific limit applies
    """
    MaxAcceleration: float = 0.0
    """
    Define the maximum adjustment acceleration for the robot to catch up to the conveyor belt. • 0
    (default): no limit o No conveyor tracking specific limit o RC internal limit applies • >0: use
    limit o Conveyor tracking specific limit applies
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default): o No trigger related behavior •
    >0: Trigger: o Start executing, when the trigger function with the identical EmitterID is
    triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class SyncToConveyorRecvData(RspHeader):
    """SyncToConveyorRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    Reserved: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InSync: bool = False
    """The TCP is in synchronization with the object on the conveyor belt."""


@_dataclass(kw_only=True, slots=True)
class SyncToConveyorSendData(CmdHeader):
    """SyncToConveyorSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """EmitterID"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default): No trigger related behavior • >0:
    Trigger: o Start executing, when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    ConveyorNo: int = 0
    """Index of assigned conveyor"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    SyncInMode: _e.SyncInMode = _e.SyncInMode.IN_SYNC_IN_ZONE
    """Defines when synchronization starts"""
    SyncInParameter: float = 0.0
    """
    Relates to "SyncInMode" "After distance" (1) and "After time" (2): Parameter for the
    synchronization • "After distance" (1) - Distance in mm • "After time" (2) - Time in ms
    """
    MaxVelocity: float = 0.0
    """
    Define the maximum adjustment velocity for the robot to catch up to the conveyor belt. The
    velocity must be greater than the velocity of the conveyor belt. • 0 (default): no limit - No
    conveyor tracking specific limit - RC internal limit applies • >0: use limit - Conveyor tracking
    specific limit applies
    """
    MaxAcceleration: float = 0.0
    """
    Define the maximum adjustment acceleration for the robot to catch up to the conveyor belt. • 0
    (default): no limit - No conveyor tracking specific limit - RC internal limit applies • >0: use
    limit - Conveyor tracking specific limit applies
    """


@_dataclass(kw_only=True, slots=True)
class ForceControlOutCmd:
    """ForceControlOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ForceStatus: _s.ForceStatus = _field(default_factory=lambda: ForceStatus())
    """Current status of ForceControl and ForceLimit (chapter 6.5.25) according to Table 6-712"""


@_dataclass(kw_only=True, slots=True)
class ForceControlParCmd:
    """ForceControlParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference of Force and Torque (at least one option must be supported)"""
    SensorValue: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ConnectionMode 1 and 2 (Sensor connected to PLC). Currently applied force and torque
    detected by sensor according to ReferenceType, ToolNo and FrameNo. • [0]: X-Axis • [1]: Y-Axis •
    [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY) • [5]:
    Rotation around Z- Axis (RZ)
    """
    TargetValue: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ReferenceType 0 (Tool) and 1 (Frame): Force and torque to be applied by robot arm
    according to ReferenceType, ToolNo and FrameNo: • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis •
    [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY) • [5]: Rotation around Z-
    Axis (RZ) Set TargetValue <>-99999.9999 (default) to define setpoint
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    ConnectionMode: _e.SensorConnectionMode = _e.SensorConnectionMode.RC_SENSOR_ALGORITHM
    """
    Specifies encoder connection setup according to Table 6-713 (at least one option must be
    supported)
    """
    SensorFrame: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Position of sensor relative to flange (FixedSensor FALSE) or relative to WCS (FixedSensor TRUE)
    • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation
    around Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """
    CalibrationData: int = 0
    """
    Index of payload data containing mass, center of gravity, orientation and inertia relative to
    SensorFrame. Required to calibrate system for setting up gravity compensation and sensor offset.
    """
    TargetWindow: float = 0.0
    """
    Tolerance of TargetValue within which currently applied force/torque will return ForceStatus
    "Specified force/torque reached" TRUE.
    """
    CompliantAxes: int = 0
    """
    Define axes whose position may be adjusted by the robot to apply specified force according to
    Table 6-711.
    """
    MaxVelocity: int = 0
    """
    Maximum allowed TCP velocity for compliant axes in % of nominal velocity. • 0% (default): no
    limit - RC internal limit applies • >0% use limit - Specified limit applies • 100% use maximal
    reference velocity For more information on nominal dynamics see chapter 5.5.7 Robot dynamics
    """
    MaxDeviation: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Maximum allowed cartesian deviation according to ReferenceType, ToolNo and FrameNo. Set 0
    (default) to not specify a limit in this axis direction. • [0]: Deviation in X-Direction in mm •
    [1]: Deviation in Y- direction in mm • [2]: Deviation in Z- direction in mm • [3]: Deviation in
    RX- direction in ° • [4]: Deviation in RY- direction in ° • [5]: Deviation in RZ- direction in °
    """
    ErrorReaction: _e.ErrorReaction = _e.ErrorReaction.ABORT_AND_MOVE
    """
    Defines reaction in case ForceControl reports error during its execution Processing of active
    move command is continued without active ForceControl
    """
    ErrorReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """
    Relates to ErrorReaction 0 (Abort and move). Defines type of reference coordinate system of
    ErrorVector
    """
    ErrorVector: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ErrorReaction 0 (Abort and move). Vector defining robot’s movement in case of
    incoming error according to ErrorReferenceType, ErrorToolNo and ErrorFrameNo. • [0]: X-Axis •
    [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY)
    • [5]: Rotation around Z-Axis (RZ)
    """
    ErrorToolNo: int = 0
    """
    Relates to ErrorReaction 0 (Abort and move). Index of tool. • 0 (default): Flange • 1..254: Tool
    frames
    """
    ErrorFrameNo: int = 0
    """Relates to ErrorReferenceType 1 (Frame) • 0: WCS (default) • 1..254: User frames"""
    FixedSensor: bool = False
    """Defines sensor positioning: • FALSE (default): Sensor mounted on flange • TRUE: Sensor fixed"""


@_dataclass(kw_only=True, slots=True)
class ForceControlRecvData(RspHeader):
    """ForceControlRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ForceStatus: int = 0
    """Current status of ForceControl and ForceLimit (chapter 6.5.25) according to Table 6-712"""


@_dataclass(kw_only=True, slots=True)
class ForceControlSendData(CmdHeader):
    """ForceControlSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    ConnectionMode: _e.SensorConnectionMode = _e.SensorConnectionMode.RC_SENSOR_ALGORITHM
    """
    Specifies encoder connection setup according to Table 6-713 (at least one option must be
    supported)
    """
    FixedSensor: int = 0
    """Defines sensor positioning: • FALSE (default): Sensor mounted on flange • TRUE: Sensor fixed"""
    SensorFrame: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Position of sensor relative to flange (FixedSensor FALSE) or relative to WCS (FixedSensor TRUE)
    • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation
    around Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """
    CalibrationData: int = 0
    """
    Index of payload data containing mass, center of gravity, orientation and inertia relative to
    SensorFrame. Required to calibrate system for setting up gravity compensation and sensor offset.
    """
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference of Force and Torque (at least one option must be supported)"""
    SensorValue: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ConnectionMode 1 and 2 (Sensor connected to PLC). Currently applied force and torque
    detected by sensor according to ReferenceType, ToolNo and FrameNo. • [0]: X-Axis • [1]: Y-Axis •
    [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY) • [5]:
    Rotation around Z- Axis (RZ)
    """
    TargetValue: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ReferenceType 0 (Tool) and 1 (Frame): Force and torque to be applied by robot arm
    according to ReferenceType, ToolNo and FrameNo: • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis •
    [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY) • [5]: Rotation around Z-
    Axis (RZ) Set TargetValue <>-99999.9999 (default) to define setpoint
    """
    MaxVelocity: int = 0
    """
    Maximum allowed TCP velocity for compliant axes in % of nominal velocity. • 0% (default): no
    limit - RC internal limit applies • >0% use limit - Specified limit applies • 100% use maximal
    reference velocity For more information on nominal dynamics see chapter 5.5.7 Robot dynamics
    """
    MaxDeviation: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Maximum allowed cartesian deviation according to ReferenceType, ToolNo and FrameNo. Set 0
    (default) to not specify a limit in this axis direction. • [0]: Deviation in X-Direction in mm •
    [1]: Deviation in Y- direction in mm • [2]: Deviation in Z- direction in mm • [3]: Deviation in
    RX- direction in ° • [4]: Deviation in RY- direction in ° • [5]: Deviation in RZ- direction in °
    """
    ErrorReaction: _e.ErrorReaction = _e.ErrorReaction.ABORT_AND_MOVE
    """
    Defines reaction in case ForceControl reports error during its execution Processing of active
    move command is continued without active ForceControl
    """
    ErrorReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """
    Relates to ErrorReaction 0 (Abort and move). Defines type of reference coordinate system of
    ErrorVector
    """
    ErrorVector: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ErrorReaction 0 (Abort and move). Vector defining robot’s movement in case of
    incoming error according to ErrorReferenceType, ErrorToolNo and ErrorFrameNo. • [0]: X-Axis •
    [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY)
    • [5]: Rotation around Z-Axis (RZ)
    """
    ErrorToolNo: int = 0
    """
    Relates to ErrorReaction 0 (Abort and move). Index of tool. • 0 (default): Flange • 1..254: Tool
    frames
    """
    ErrorFrameNo: int = 0
    """Relates to ErrorReferenceType 1 (Frame) • 0: WCS (default) • 1..254: User frames"""
    CompliantAxes: int = 0
    """
    Define axes whose position may be adjusted by the robot to apply specified force according to
    Table 6-711.
    """


@_dataclass(kw_only=True, slots=True)
class ForceLimitOutCmd:
    """ForceLimitOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ForceStatus: _s.ForceStatus = _field(default_factory=lambda: ForceStatus())
    """Current status of ForceControl and ForceLimit (chapter 6.5.25) according to Table 6-712"""
    FollowID: int = 0
    """
    Relates to EmitterID <> 0: Unique system-generated ID of the trigger function when the function
    is called by user. For more information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class ForceLimitParCmd:
    """ForceLimitParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference of Force and Torque (at least one option must be supported)"""
    SensorValue: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ConnectionMode 1 and 2 (Sensor connected to PLC). Currently applied force and torque
    detected by sensor according to ReferenceType, ToolNo and FrameNo. • [0]: X-Axis • [1]: Y-Axis •
    [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY) • [5]:
    Rotation around Z- Axis (RZ)
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    ForceLimit: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Maximal allowed force and torque detected by the sensor according to ReferenceType and
    ToolNo/FrameNo before robot reacts according to ReactionMode. Set value <>0 (default) to monitor
    coordinate axes • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) •
    [4]: Rotation around Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """
    ConnectionMode: _e.ConnectionMode = _e.ConnectionMode.RC_CONNECTED
    """
    Specifies encoder connection setup according to Table 6-713 (at least one option must be
    supported)
    """
    SensorFrame: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Position of sensor relative to flange (FixedSensor FALSE) or relative to WCS (FixedSensor TRUE)
    • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation
    around Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """
    CalibrationData: int = 0
    """
    Index of payload data containing mass, center of gravity, orientation and inertia relative to
    SensorFrame. Required to calibrate system for setting up gravity compensation and sensor offset.
    """
    FixedSensor: bool = False
    """Defines sensor positioning: • FALSE (default): Sensor mounted on flange • TRUE: Sensor fixed"""
    EmitterID: int = 0
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: Undefined (default) - If no EmitterID is
    defined, the function returns an error message For more information see chapter 5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class ForceLimitRecvData(RspHeader):
    """ForceLimitRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    Reserved: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    ForceStatus: int = 0
    """Current status of ForceControl and ForceLimit (chapter 6.5.25) according to Table 6-712"""


@_dataclass(kw_only=True, slots=True)
class ForceLimitSendData(CmdHeader):
    """ForceLimitSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: Undefined (default) - If no EmitterID is
    defined, the function returns an error message For more information see chapter 5.5.12.4
    """
    ListenerID: int = 0
    """ID of associated trigger. Always 0."""
    Reserve: int = 0
    """Reserve"""
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    ConnectionMode: int = 0
    """
    Specifies encoder connection setup according to Table 6-713 (at least one option must be
    supported)
    """
    FixedSensor: int = 0
    """Defines sensor positioning: • FALSE (default): Sensor mounted on flange • TRUE: Sensor fixed"""
    SensorFrame: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Position of sensor relative to flange (FixedSensor FALSE) or relative to WCS (FixedSensor TRUE)
    • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation
    around Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """
    CalibrationData: int = 0
    """
    Index of payload data containing mass, center of gravity, orientation and inertia relative to
    SensorFrame. Required to calibrate system for setting up gravity compensation and sensor offset.
    """
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference of Force and Torque (at least one option must be supported)"""
    SensorValue: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Relates to ConnectionMode 1 and 2 (Sensor connected to PLC). Currently applied force and torque
    detected by sensor according to ReferenceType, ToolNo and FrameNo. • [0]: X-Axis • [1]: Y-Axis •
    [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around Y-Axis (RY) • [5]:
    Rotation around Z- Axis (RZ)
    """
    ForceLimit: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Maximal allowed force and torque detected by the sensor according to ReferenceType and
    ToolNo/FrameNo before robot reacts according to ReactionMode. Set value <>0 (default) to monitor
    coordinate axes • [0]: X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) •
    [4]: Rotation around Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualForceOutCmd:
    """ReadActualForceOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActualForce: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Currently detected force and torque according to ReferenceType, ToolNo and FrameNo. • [0]:
    X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around
    Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualForceParCmd:
    """ReadActualForceParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference of Force and Torque (at least one option must be supported )"""
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    CalibrationData: int = 0
    """
    Index of payload data containing mass, center of gravity, orientation and inertia relative to
    SensorFrame. Required to calibrate system for setting up gravity compensation and sensor offset.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualForceRecvData(RspHeader):
    """ReadActualForceRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    Reserved: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    ActualForce: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Currently detected force and torque according to ReferenceType, ToolNo and FrameNo. • [0]:
    X-Axis • [1]: Y-Axis • [2]: Z- Axis • [3]: Rotation around X-Axis (RX) • [4]: Rotation around
    Y-Axis (RY) • [5]: Rotation around Z- Axis (RZ)
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualForceSendData(CmdHeader):
    """ReadActualForceSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: Undefined (default) - If no EmitterID is
    defined, the function returns an error message For more information see chapter 5.5.12.4
    """
    ListenerID: int = 0
    """ListenerID"""
    Reserve: int = 0
    """Reserve"""
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """
    Define the index number of the UCS that will be assigned to the conveyor. For more information
    refer to chapter 5.5.14
    """
    CalibrationData: int = 0
    """
    Index of payload data containing mass, center of gravity, orientation and inertia relative to
    SensorFrame. Required to calibrate system for setting up gravity compensation and sensor offset.
    """
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference of Force and Torque (at least one option must be supported )"""


@_dataclass(kw_only=True, slots=True)
class EnableRobotOutCmd:
    """EnableRobotOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class EnableRobotParCmd:
    """EnableRobotParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    HoldToRun: bool = False
    """The robot will move while HoldToRun is set TRUE"""
    StepMode: _e.StepMode = _e.StepMode.DEACTIVATE
    """
    While activated the RI state switches to interrupted when a buffered command returns Done TRUE
    At least one of the optional modes must be supported
    """
    ManualStep: bool = False
    """
    Relates to StepMode 1 (Blending) and 2 (Exact stop) Start the next buffered command with the
    rising edge in T1 External or T2 External
    """


@_dataclass(kw_only=True, slots=True)
class EnableRobotRecvData(RspHeader):
    """EnableRobotRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """TRUE when robot is set to RA power state "Enabled"."""


@_dataclass(kw_only=True, slots=True)
class EnableRobotSendData(CmdHeader):
    """EnableRobotSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enable: bool = False
    """Set TRUE to change RA power state to "Enabled" """
    HoldToRun: bool = False
    """The robot will move while HoldToRun is set TRUE"""
    StepMode: _e.StepMode = _e.StepMode.DEACTIVATE
    """
    While activated the RI state switches to interrupted when a buffered command returns Done TRUE
    At least one of the optional modes must be supported
    """
    ManualStep: bool = False
    """
    Relates to StepMode 1 (Blending) and 2 (Exact stop) Start the next buffered command with the
    rising edge in T1 External or T2 External
    """


@_dataclass(kw_only=True, slots=True)
class GroupResetOutCmd:
    """GroupResetOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupResetParCmd:
    """GroupResetParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupResetRecvData(RspHeader):
    """GroupResetRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class GroupResetSendData(CmdHeader):
    """GroupResetSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class RestartControllerOutCmd:
    """RestartControllerOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RestartAccepted: bool = False
    """TRUE when execution of command has been confirmed by RC and restart is about to be initiated."""


@_dataclass(kw_only=True, slots=True)
class RestartControllerParCmd:
    """RestartControllerParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class RestartControllerRecvData(RspHeader):
    """RestartControllerRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RestartAccepted: bool = False
    """TRUE when execution of command has been confirmed by RC and restart is about to be initiated."""


@_dataclass(kw_only=True, slots=True)
class RestartControllerSendData(CmdHeader):
    """RestartControllerSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class RobotTaskParCfgCom:
    """RobotTaskParCfgCom"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LifeSignTimeOut: int = 50
    """
    Maximum allowed time between incrementation of LifeSign before communication error. • <10 ms:
    Invalid • 50 ms: default See also chapter 5.6.6.2.
    """
    TelegramLengthPlcToRob: int = 256
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction
    client to server
    """
    TelegramLengthRobToPlc: int = 256
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction
    server to client
    """
    TwoSequences: bool = False
    """Use two sequences in telegram ?"""


@_dataclass(kw_only=True, slots=True)
class RobotTaskParCfgPlc:
    """RobotTaskParCfgPlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CycleTime: int = 10
    """PLC cycle time"""
    Parameter: RobotTaskParCfgPlcParameter = _field(default_factory=lambda: RobotTaskParCfgPlcParameter())
    """parameter"""
    OptionalCyclic: AxesGroupParameterPlcOptionalCyclic = _field(default_factory=lambda: AxesGroupParameterPlcOptionalCyclic())
    """Configuration of optional cyclic data send to the Robot"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterPlcParameter:
    """AxesGroupParameterPlcParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ManufacturedID: int = 0
    """Manufactured ID"""
    OrderID: str = ''
    """Order ID"""
    SerialNumber: str = ''
    """Serial Number"""
    FirmwareVersion: str = ''
    """Firmware Version"""
    InterfaceVersion: str = ''
    """Client Interface Version"""
    SynchronizationModes: _s.SynchronizationModes = _field(default_factory=lambda: SynchronizationModes())
    """Synchronization Modes"""
    SyncUserInteraction: _s.SyncUserInteraction = _field(default_factory=lambda: SyncUserInteraction())
    """Synchronization needs user interaction"""


@_dataclass(kw_only=True, slots=True)
class RobotTaskParCfgPlcParameter(AxesGroupParameterPlcParameter):
    """RobotTaskParCfgPlcParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class RobotTaskParCfgRob:
    """RobotTaskParCfgRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Parameter: RobotTaskParCfgRobParameter = _field(default_factory=lambda: RobotTaskParCfgRobParameter())
    """Robot parameter"""
    OptionalCyclic: AxesGroupParameterRobOptionalCyclic = _field(default_factory=lambda: AxesGroupParameterRobOptionalCyclic())
    """Configuration of optional cyclic data received from the Robot"""


@_dataclass(kw_only=True, slots=True)
class RobotTaskParCfgRobParameter:
    """RobotTaskParCfgRobParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WaitAtBlendingZone: bool = False
    """
    Defines blending behavior for single move commands. One of the optional modes must be supported.
    • 0 (default): Move to end position Robot moves exactly the target position independently of the
    selected "BlendingMode" • 1: Wait at blending parameter Robot stops its movement when the
    specified blending parameter is reached
    """
    AllowSecSeqWhileSubprogram: bool = False
    """
    Allow a sequence switch from primary to secondary while a subprogram called via CallSubprogram
    (6.5.18) in the sequence is in progress
    """
    AllowDynamicBlending: bool = False
    """
    Allows blending when CallSubprogram is called in sequence and removed afterwards. For more
    information see chapter 6.5.21. • 0 (default): Dynamic blending is prevented • 1: Dynamic
    blending is allowed
    """
    DelayTime: int = 0
    """
    Defines waiting time of RC between receiving a first move command when motion queue is empty and
    starting the first movement. See also chapter 5.6.8.
    """
    WaitForNrOfCmd: int = 0
    """Define number of points required to calculate the blending. See also chapter 5.6.8."""
    SyncDelay: int = 0
    """
    Defines a delay time between detecting an inconsistency of configuration data between server and
    client and executing the defined SyncReaction. Always positive. Default: 0 ms
    """
    SyncReaction: _e.SyncReaction = _e.SyncReaction.NO_REACTION
    """
    Specifies system reaction in case inconsistency of synchronization data is detected according to
    Table 6-81. For more information refer to chapter 5.6.7.2
    """
    MessageLevel: _e.MessageLevel = _e.MessageLevel.WARNING
    """Defines up to which level of severity messages will be transmitted to the PLC’s message buffer"""


@_dataclass(kw_only=True, slots=True)
class RobotTaskParCfg:
    """RobotTaskParCfg"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Com: RobotTaskParCfgCom = _field(default_factory=lambda: RobotTaskParCfgCom())
    """Common parameter"""
    Plc: RobotTaskParCfgPlc = _field(default_factory=lambda: RobotTaskParCfgPlc())
    """PLC parameter"""
    Rob: RobotTaskParCfgRob = _field(default_factory=lambda: RobotTaskParCfgRob())
    """Robot parameter"""


@_dataclass(kw_only=True, slots=True)
class SetOperationModeOutCmd:
    """SetOperationModeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class SetOperationModeParCmd:
    """SetOperationModeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OperationMode: _e.OperationMode = _e.OperationMode.T1_LOCAL
    """Limits for joints and external axes according to Table 6-180."""


@_dataclass(kw_only=True, slots=True)
class SetOperationModeRecvData(RspHeader):
    """SetOperationModeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class SetOperationModeSendData(CmdHeader):
    """SetOperationModeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OperationMode: int = 0
    """Limits for joints and external axes according to Table 6-180."""


@_dataclass(kw_only=True, slots=True)
class SetSequenceOutCmd:
    """SetSequenceOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class SetSequenceParCmd:
    """SetSequenceParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetSequence: _e.SequenceFlag = _e.SequenceFlag.NO_SEQUENCE
    """Defines sequence to be activated when function is executed"""


@_dataclass(kw_only=True, slots=True)
class SetSequenceRecvData(RspHeader):
    """SetSequenceRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class SetSequenceSendData(CmdHeader):
    """SetSequenceSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TargetSequence: int = 0
    """Defines sequence to be activated when function is executed"""


@_dataclass(kw_only=True, slots=True)
class SwitchLanguageOutCmd:
    """SwitchLanguageOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActualLanguageCode: str = ''
    """Two letter code of actual language used at the original operating panel of the robot."""


@_dataclass(kw_only=True, slots=True)
class SwitchLanguageParCmd:
    """SwitchLanguageParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LanguageCode: str = ''
    """Two letter code of language to be set at the original operating panel of the robot (default: EN)"""


@_dataclass(kw_only=True, slots=True)
class SwitchLanguageRecvData(RspHeader):
    """SwitchLanguageRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActualLanguageCode: str = ''
    """Two letter code of actual language used at the original operating panel of the robot."""


@_dataclass(kw_only=True, slots=True)
class SwitchLanguageSendData(CmdHeader):
    """SwitchLanguageSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LanguageCode: str = ''
    """Two letter code of language to be set at the original operating panel of the robot (default: EN)"""


@_dataclass(kw_only=True, slots=True)
class UserLoginOutCmd:
    """UserLoginOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class UserLoginParCmd:
    """UserLoginParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.LogonMode = _e.LogonMode.PASSWORD_ONLY
    """Defines the logon type (at least one option must be supported)"""
    Password: str = ''
    """Defines the user password."""
    Username: str = ''
    """Defines the name of the operator"""
    LevelID: int = 0
    """Defines the level ID of the operator (default: 0)"""


@_dataclass(kw_only=True, slots=True)
class UserLoginRecvData(RspHeader):
    """UserLoginRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class UserLoginSendData(CmdHeader):
    """UserLoginSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.LogonMode = _e.LogonMode.PASSWORD_ONLY
    """Defines the logon type (at least one option must be supported)"""
    LevelID: int = 0
    """Defines the level ID of the operator (default: 0)"""
    Password: str = ''
    """Defines the user password."""
    Username: str = ''
    """Defines the name of the operator"""


@_dataclass(kw_only=True, slots=True)
class ReadActualPositionOutCmd:
    """ReadActualPositionOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    ToolNoReturn: int = 0
    """
    Index of tool of returned position • -1: Currently used tool on RC • 0: Flange (default) •
    1..254: Tool frames
    """
    FrameNoReturn: int = 0
    """
    Index of frame of returned position • -1: Currently used frame on RC • 0: WCS (default) •
    1..254: User frames
    """
    ActualCartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Absolute coordinates in the active coordinate system"""
    ActualJointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute position of the robot in Joint position."""


@_dataclass(kw_only=True, slots=True)
class ReadActualPositionParCmd:
    """ReadActualPositionParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """
    Index of tool of returned position • -1: Currently used tool on RC • 0: Flange (default) •
    1..254: Tool frames
    """
    FrameNo: int = 0
    """
    Index of frame of returned position • -1: Currently used frame on RC • 0: WCS (default) •
    1..254: User frames
    """
    ListenerID: int = 0
    """
    ID of associated trigger function • 0: No Trigger (default) -> No trigger related behavior • >0:
    Trigger -> Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualPositionRecvData(RspHeader):
    """ReadActualPositionRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    ToolNoReturn: int = 0
    """
    Index of tool of returned position • -1: Currently used tool on RC • 0: Flange (default) •
    1..254: Tool frames
    """
    FrameNoReturn: int = 0
    """
    Index of frame of returned position • -1: Currently used frame on RC • 0: WCS (default) •
    1..254: User frames
    """
    ActualCartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Absolute coordinates in the active coordinate system"""
    ActualJointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute position of the robot in Joint position."""


@_dataclass(kw_only=True, slots=True)
class ReadActualPositionSendData(CmdHeader):
    """ReadActualPositionSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    ToolNo: int = 0
    """
    Index of tool of returned position • -1: Currently used tool on RC • 0: Flange (default) •
    1..254: Tool frames
    """
    FrameNo: int = 0
    """
    Index of frame of returned position • -1: Currently used frame on RC • 0: WCS (default) •
    1..254: User frames
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualPositionCyclicOutCmd:
    """ReadActualPositionCyclicOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReadingCartesianPosition: bool = False
    """TRUE, while the output CartesianPosition returns valid values"""
    ReadingCartesianPositionExt: bool = False
    """TRUE, while the output ExtCartesianPosition returns valid values"""
    ReadingJointPosition: bool = False
    """TRUE, while the output JointPosition returns valid values"""
    ReadingJointPositionExt: bool = False
    """TRUE, while the output ExtJointPosition returns valid values"""
    CurrentCoordinateSystem: _s.CoordinateSystem = _field(default_factory=lambda: CoordinateSystem())
    """Tool and frame index of currently used tool and frame according to Table 6-40"""
    CartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Cyclically returned, absolute coordinates of current position in selected coordinate systems
    (see input parameters ToolNo and FrameNo)
    """
    CartesianPositionShort: RobotCartesianPositionShort = _field(default_factory=lambda: RobotCartesianPositionShort())
    """
    Cyclically returned, absolute coordinates of current position in selected coordinate systems
    (see input parameters ToolNo and FrameNo)
    """
    CartesianPositionExt: RobotCartesianPositionExt = _field(default_factory=lambda: RobotCartesianPositionExt())
    """Cyclically returned, absolute cartesian position of the external axes of the robot"""
    CoordinateSystem: _s.CoordinateSystem = _field(default_factory=lambda: CoordinateSystem())
    """Tool and frame index of returned position according to Table 6-40"""
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Cyclically returned, absolute joint position of the robot in Joint position"""
    JointPositionShort: RobotJointPositionShort = _field(default_factory=lambda: RobotJointPositionShort())
    """Cyclically returned, absolute short joint position of the robot in Joint position"""
    JointPositionExt: RobotJointPositionExt = _field(default_factory=lambda: RobotJointPositionExt())
    """Cyclically returned, absolute extended joint position of the external axes of the robot"""


@_dataclass(kw_only=True, slots=True)
class ReadActualPositionCyclicParCmd:
    """ReadActualPositionCyclicParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReadCartesianPosition: bool = False
    """Set TRUE (default) to activate cyclic transmission of cartesian position without external axes"""
    ReadCartesianPositionExt: bool = False
    """
    Set TRUE to activate cyclic transmission of external axes values of cartesian position -
    Default: False
    """
    ToolNo: int = 0
    """
    Index of tool of returned position • -1: Currently used tool on RC • 0: Flange (default) •
    1..254: Tool frames
    """
    FrameNo: int = 0
    """
    Index of frame of returned position • -1: Currently used frame on RC • 0: WCS (default) •
    1..254: User frames
    """
    ReadJointPosition: bool = False
    """Set TRUE (default) to activate cyclic transmission of joint position without external axes"""
    ReadJointPositionExt: bool = False
    """
    Set TRUE to activate cyclic transmission of external axes values of joint position - Default:
    False
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualTCPVelocityOutCmd:
    """ReadActualTCPVelocityOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActualTCPVelocity: float = 0.0
    """Absolute actual velocity of the robot’s TCP. [mm/s]"""
    ToolNoReturn: int = 0
    """Index of tool of returned velocity • 0: Flange • 1..254: Tool frames"""
    FrameNoReturn: int = 0
    """Index of frame of returned position • 0: WCS • 1..254: User frames"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualTCPVelocityParCmd:
    """ReadActualTCPVelocityParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Index of tool of returned velocity • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    ListenerID: int = 0
    """
    ID of associated trigger function • 0: No Trigger (default) -> No trigger related behavior • >0:
    Trigger -> Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadActualTCPVelocityRecvData(RspHeader):
    """ReadActualTCPVelocityRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    ActualTCPVelocity: float = 0.0
    """Absolute actual velocity of the robot’s TCP. [mm/s]"""
    ToolNoReturn: int = 0
    """Index of tool of returned velocity • 0: Flange • 1..254: Tool frames"""
    FrameNoReturn: int = 0
    """Index of frame of returned position • 0: WCS • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class ReadActualTCPVelocitySendData(CmdHeader):
    """ReadActualTCPVelocitySendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Index of tool of returned velocity • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class ReadAnalogInputOutCmd:
    """ReadAnalogInputOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Unit: _e.UnitType = _e.UnitType.VOLT
    """Returned values of digital inputs Returned values of digital inputs Unit of returned Value"""
    Value: float = 0.0
    """Returned value of analog input"""


@_dataclass(kw_only=True, slots=True)
class ReadAnalogInputParCmd:
    """ReadAnalogInputParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: int = 0
    """Number of the analog input 1..32"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadAnalogInputRecvData(RspHeader):
    """ReadAnalogInputRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Unit: int = 0
    """Returned values of digital inputs Returned values of digital inputs Unit of returned Value"""
    Value: float = 0.0
    """Returned value of analog input"""


@_dataclass(kw_only=True, slots=True)
class ReadAnalogInputSendData(CmdHeader):
    """ReadAnalogInputSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: int = 0
    """Number of the analog input 1..32"""


@_dataclass(kw_only=True, slots=True)
class ReadDHParameterOutCmd:
    """ReadDHParameterOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DHParameter: _s.DHParameter = _field(default_factory=lambda: DHParameter())
    """Denavit–Hartenberg parameter"""


@_dataclass(kw_only=True, slots=True)
class ReadDHParameterParCmd:
    """ReadDHParameterParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ModifiedConvention: bool = False
    """
    Determines if returned DH parameters use modified convention or classic convention. • 0: Classic
    convention (default) • 1: Modified convention
    """


@_dataclass(kw_only=True, slots=True)
class ReadDHParameterRecvData(RspHeader):
    """ReadDHParameterRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DHParameter: _s.DHParameter = _field(default_factory=lambda: DHParameter())
    """Denavit–Hartenberg parameter"""


@_dataclass(kw_only=True, slots=True)
class ReadDHParameterSendData(CmdHeader):
    """ReadDHParameterSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ModifiedConvention: bool = False
    """
    Determines if returned DH parameters use modified convention or classic convention. • 0: Classic
    convention (default) • 1: Modified convention
    """


@_dataclass(kw_only=True, slots=True)
class ReadDigitalInputsOutCmd:
    """ReadDigitalInputsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Values: list[int] = _field(default_factory=lambda: [0] * 5)
    """Returned values of digital inputs"""


@_dataclass(kw_only=True, slots=True)
class ReadDigitalInputsParCmd:
    """ReadDigitalInputsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies the desired byte addresses that shall be read"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadDigitalInputsRecvData(RspHeader):
    """ReadDigitalInputsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Values: list[int] = _field(default_factory=lambda: [0] * 5)
    """Returned values of digital inputs"""


@_dataclass(kw_only=True, slots=True)
class ReadDigitalInputsSendData(CmdHeader):
    """ReadDigitalInputsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies the desired byte addresses that shall be read"""


@_dataclass(kw_only=True, slots=True)
class ReadDigitalOutputsOutCmd:
    """ReadDigitalOutputsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Values: list[int] = _field(default_factory=lambda: [0] * 5)
    """Returned values of digital inputs"""


@_dataclass(kw_only=True, slots=True)
class ReadDigitalOutputsParCmd:
    """ReadDigitalOutputsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies the desired byte addresses that shall be read"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadDigitalOutputsRecvData(RspHeader):
    """ReadDigitalOutputsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Values: list[int] = _field(default_factory=lambda: [0] * 5)
    """Returned values of digital inputs"""


@_dataclass(kw_only=True, slots=True)
class ReadDigitalOutputsSendData(CmdHeader):
    """ReadDigitalOutputsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies the desired byte addresses that shall be read"""


@_dataclass(kw_only=True, slots=True)
class ReadFrameDataOutCmd:
    """ReadFrameDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FrameNoReturn: int = 0
    """Frame index"""
    FrameData: _s.FrameData = _field(default_factory=lambda: FrameData())
    """Frame data (see chapter 5.5.6.2)"""


@_dataclass(kw_only=True, slots=True)
class ReadFrameDataParCmd:
    """ReadFrameDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FrameNo: int = 0
    """Frame index • -1: Currently used frame on RC • 0: WCS • 1 (default)..254: UCS (User frames)"""


@_dataclass(kw_only=True, slots=True)
class ReadFrameDataRecvData(RspHeader):
    """ReadFrameDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    FrameNoReturn: int = 0
    """Frame index"""
    FrameData: _s.FrameData = _field(default_factory=lambda: FrameData())
    """Frame data (see chapter 5.5.6.2)"""
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadFrameDataSendData(CmdHeader):
    """ReadFrameDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FrameNo: int = 0
    """Frame index • -1: Currently used frame on RC • 0: WCS • 1 (default)..254: UCS (User frames)"""


@_dataclass(kw_only=True, slots=True)
class ReadIntegersOutCmd:
    """ReadIntegersOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Values: list[int] = _field(default_factory=lambda: [0] * 7)
    """Returned values of integer register"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class ReadIntegersParCmd:
    """ReadIntegersParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be read"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadIntegersRecvData(RspHeader):
    """ReadIntegersRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    Values: list[int] = _field(default_factory=lambda: [0] * 7)
    """Returned values of integer register"""


@_dataclass(kw_only=True, slots=True)
class ReadIntegersSendData(CmdHeader):
    """ReadIntegersSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be read"""


@_dataclass(kw_only=True, slots=True)
class ReadLoadDataOutCmd:
    """ReadLoadDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LoadNoReturn: int = 0
    """Tool index"""
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Load data (see chapter 5.5.6.4)"""


@_dataclass(kw_only=True, slots=True)
class ReadLoadDataParCmd:
    """ReadLoadDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LoadNo: int = 0
    """
    Load index • -1: Currently used load on RC • 0: Not possible to read • 1 (default)..254: Load
    data
    """


@_dataclass(kw_only=True, slots=True)
class ReadLoadDataRecvData(RspHeader):
    """ReadLoadDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LoadNoReturn: int = 0
    """Tool index"""
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Load data (see chapter 5.5.6.4)"""
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadLoadDataSendData(CmdHeader):
    """ReadLoadDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LoadNo: int = 0
    """
    Load index • -1: Currently used load on RC • 0: Not possible to read • 1 (default)..254: Load
    data
    """


@_dataclass(kw_only=True, slots=True)
class ReadMessagesOutCmd:
    """ReadMessagesOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MsgId: int = 0
    """ID for function specific acknowledgement mechanism"""
    NumberOfActiveErrors: int = 0
    """Number of pending errors on RC"""
    NumberOfActiveWarnings: int = 0
    """Number if pending warnings in RC"""
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    MsgType: _e.MessageType = _e.MessageType.RI
    """Message Type"""
    Severity: _e.Severity = _e.Severity.DEACTIVATE
    """Severity of returned message according to .Table 5-47."""
    ErrorCode: int = 0
    """ErrorCode"""
    Text: str = ''
    """Test"""


@_dataclass(kw_only=True, slots=True)
class ReadMessagesParCmd:
    """ReadMessagesParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MsgID: int = 0
    """ID for function specific acknowledgement mechanism"""
    MessageLevel: _e.MessageLevel = _e.MessageLevel.DEBUG
    """Defines up to which level of severity messages will be transmitted to the PLC’s message buffer"""


@_dataclass(kw_only=True, slots=True)
class ReadMessagesRecvData(RspHeader):
    """ReadMessagesRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enabled: bool = False
    """Set TRUE to read messages from RC."""
    MsgId: int = 0
    """ID for function specific acknowledgement mechanism"""
    NumberOfActiveErrors: int = 0
    """Number of pending errors on RC"""
    NumberOfActiveWarnings: int = 0
    """Number if pending warnings in RC"""
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    MsgType: int = 0
    """Message Type"""
    Severity: int = 0
    """Severity of returned message according to .Table 5-47."""
    ErrorCode: int = 0
    """ErrorCode"""
    Text: str = ''
    """Test"""


@_dataclass(kw_only=True, slots=True)
class ReadMessagesSendData(CmdHeader):
    """ReadMessagesSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MsgID: int = 0
    """ID for function specific acknowledgement mechanism"""
    Enable: bool = False
    """TRUE when function is returning messages from RC"""
    MessageLevel: int = 0
    """Defines up to which level of severity messages will be transmitted to the PLC’s message buffer"""


@_dataclass(kw_only=True, slots=True)
class ReadRealsOutCmd:
    """ReadRealsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    Values: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """Returned values of real register"""


@_dataclass(kw_only=True, slots=True)
class ReadRealsParCmd:
    """ReadRealsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be read"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadRealsRecvData(RspHeader):
    """ReadRealsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    Values: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """Returned values of real register"""


@_dataclass(kw_only=True, slots=True)
class ReadRealsSendData(CmdHeader):
    """ReadRealsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be read"""


@_dataclass(kw_only=True, slots=True)
class ReadRobotDataOutCmd:
    """ReadRobotDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RCManufacturer: str = ''
    """RC manufacturer name"""
    RCOrderID: str = ''
    """RC part number"""
    RCSerialNumber: str = ''
    """RC serial number"""
    RASerialNumber: str = ''
    """RA serial number"""
    RCFirmwareVersion: str = ''
    """Robot firmware version in manufacturer -specific format"""
    RCInterpreterVersion: str = ''
    AxisJointUsed: _s.AxisJointUsed = _field(default_factory=lambda: AxisJointUsed())
    """TRUE = Axis used in Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment"""
    AxisExternalUsed: _s.AxisExternalUsed = _field(default_factory=lambda: AxisExternalUsed())
    """TRUE = Axis used by Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment."""
    AxisJointUnit: _s.AxisJointUnit = _field(default_factory=lambda: AxisJointUnit())
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment."""
    AxisExternalUnit: _s.AxisExternalUnit = _field(default_factory=lambda: AxisExternalUnit())
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment"""
    RCSupportedFunctions: _s.RCSupportedFunctions = _field(default_factory=lambda: RCSupportedFunctions())
    """
    • TRUE: Function is supported by RC • FALSE: Function is not supported by RC See Table 6-14 for
    bit assignment.
    """
    RobotID: str = ''
    """Unique and unmodifiable identification of the RA."""
    InterpreterCycleTime: int = 0
    """Interpreter task cycle time of the RC [ms]"""


@_dataclass(kw_only=True, slots=True)
class ReadRobotDataParCmd:
    """ReadRobotDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotDataRecvData(RspHeader):
    """ReadRobotDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RCManufacturer: str = ''
    """RC manufacturer name"""
    RCOrderID: str = ''
    """RC part number"""
    RCSerialNumber: str = ''
    """RC serial number"""
    RASerialNumber: str = ''
    """RA serial number"""
    RCFirmwareVersion: str = ''
    """Robot firmware version in manufacturer -specific format"""
    RCInterpreterVersion: str = ''
    Reserve: int = 0
    """Reserve"""
    AxisJointUsed: int = 0
    """TRUE = Axis used in Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment"""
    AxisExternalUsed: int = 0
    """TRUE = Axis used by Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment."""
    AxisJointUnit: int = 0
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment."""
    AxisExternalUnit: int = 0
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment"""
    RCSupportedFunctions: list[int] = _field(default_factory=lambda: [0] * 19)
    """
    • TRUE: Function is supported by RC • FALSE: Function is not supported by RC See Table 6-14 for
    bit assignment.
    """
    Reserve2: int = 0
    """Reserve 2"""
    RobotID: str = ''
    """Unique and unmodifiable identification of the RA."""
    InterpreterCycleTime: int = 0
    """Interpreter task cycle time of the RC [ms]"""


@_dataclass(kw_only=True, slots=True)
class ReadRobotDataSendData(CmdHeader):
    """ReadRobotDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotDefaultDynamicsOutCmd:
    """ReadRobotDefaultDynamicsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DynamicValues: DefaultDynamics = _field(default_factory=lambda: DefaultDynamics())
    """Default dynamics values according to Table 6-148."""


@_dataclass(kw_only=True, slots=True)
class ReadRobotDefaultDynamicsParCmd:
    """ReadRobotDefaultDynamicsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotDefaultDynamicsRecvData(RspHeader):
    """ReadRobotDefaultDynamicsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    VelocityRate: int = 0
    """
    Maximum velocity for the axes. Range [%]: • <0% : Use default velocity given by the user • 0% :
    Use internal minimal velocity • 100% : Use the entire reference velocity, given by the user
    """
    AccelerationRate: int = 0
    """
    Maximum acceleration. Range [%]: • <0% : Use default acceleration given by the user • 0% : Use
    internal minimal acceleration • 100% : Use the entire reference acceleration, given by the user
    """
    DecelerationRate: int = 0
    """
    Maximum deceleration. Range [%] : • <0% : Use default deceleration given by the user • 0% : Use
    internal minimal deceleration • 100% : Use the entire reference deceleration, given by the user
    """
    JerkRate: int = 0
    """
    Maximum jerk Range [%] : • <0% : Use default jerk given by the user • 0% : Use internal minimal
    jerk • 100% : Use the entire reference jerk, given by the user (Trapezoidal if possible)
    """
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadRobotDefaultDynamicsSendData(CmdHeader):
    """ReadRobotDefaultDynamicsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotReferenceDynamicsOutCmd:
    """ReadRobotReferenceDynamicsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DynamicValues: ReferenceDynamics = _field(default_factory=lambda: ReferenceDynamics())
    """Reference dynamics values according to Table 6-109."""


@_dataclass(kw_only=True, slots=True)
class ReadRobotReferenceDynamicsParCmd:
    """ReadRobotReferenceDynamicsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotReferenceDynamicsRecvData(RspHeader):
    """ReadRobotReferenceDynamicsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    VelocityReference: float = 0.0
    """
    Path velocity [mm/s](tangent) at 100% • <0: (default) - Do not change values • ≥0: Change values
    according to input value
    """
    AccelerationReference: float = 0.0
    """
    Path acceleration [mm/s2] at 100% • <0: (default) - Do not change values • ≥0: Change values
    according to input value
    """
    DecelerationReference: float = 0.0
    """
    Path deceleration [mm/s2] at 100% • <0: (default) - Do not change values • ≥0: Change values
    according to input value
    """
    JerkReference: float = 0.0
    """
    Jerk [mm/s3] at 100% • <0: (default) - Do not change values • ≥0: Change values according to
    input value
    """
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadRobotReferenceDynamicsSendData(CmdHeader):
    """ReadRobotReferenceDynamicsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotSWLimitsOutCmd:
    """ReadRobotSWLimitsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LimitValues: SWLimits = _field(default_factory=lambda: SWLimits())
    """DLimits for joints and external axes according to Table 6-173."""


@_dataclass(kw_only=True, slots=True)
class ReadRobotSWLimitsParCmd:
    """ReadRobotSWLimitsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadRobotSWLimitsRecvData(RspHeader):
    """ReadRobotSWLimitsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LimitValues: SWLimits = _field(default_factory=lambda: SWLimits())
    """DLimits for joints and external axes according to Table 6-173."""
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadRobotSWLimitsSendData(CmdHeader):
    """ReadRobotSWLimitsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ReadSystemVariableOutCmd:
    """ReadSystemVariableOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    DataType: list[int] = _field(default_factory=lambda: [0] * 8)
    """Parameter data type as specified in Table 6-613."""
    Data_0: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[0] and SubParameterID[0]"""
    Data_1: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[1] and SubParameterID[1]"""
    Data_2: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[2] and SubParameterID[2]"""
    Data_3: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[3] and SubParameterID[3]"""
    Data_4: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[4] and SubParameterID[4]"""
    Data_5: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[5] and SubParameterID[5]"""
    Data_6: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[6] and SubParameterID[6]"""
    Data_7: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[7] and SubParameterID[7]"""


@_dataclass(kw_only=True, slots=True)
class ReadSystemVariableParCmd:
    """ReadSystemVariableParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RCParameter: bool = False
    """
    Defines the parameter list which should be used: • FALSE: Standardized parameter list (default):
    - Read parameters on the RC based on a standardized parameter list • TRUE: Manufacturer specific
    parameter list: - Read parameters on the RC based on robot manufacturers-specific parameter
    lists
    """
    ParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    Requested parameter ID in selected parameter list. • 0: undefined (default) • 1..65 535:
    Parameter ID
    """
    SubParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    ID of the requested sub parameter in selected parameter list. • 0: ID 0 (default) (relates only
    to parameters without sub parameters) • 1..255: Indices 1 to 255 (relates only to parameters
    with sub parameters)
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReadSystemVariableRecvData(RspHeader):
    """ReadSystemVariableRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    DataType: list[int] = _field(default_factory=lambda: [0] * 8)
    """Parameter data type as specified in Table 6-613."""
    Data_0: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[0] and SubParameterID[0]"""
    Data_1: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[1] and SubParameterID[1]"""
    Data_2: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[2] and SubParameterID[2]"""
    Data_3: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[3] and SubParameterID[3]"""
    Data_4: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[4] and SubParameterID[4]"""
    Data_5: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[5] and SubParameterID[5]"""
    Data_6: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[6] and SubParameterID[6]"""
    Data_7: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[7] and SubParameterID[7]"""


@_dataclass(kw_only=True, slots=True)
class ReadSystemVariableSendData(CmdHeader):
    """ReadSystemVariableSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    RCParameter: bool = False
    """
    Defines the parameter list which should be used: • FALSE: Standardized parameter list (default):
    - Read parameters on the RC based on a standardized parameter list • TRUE: Manufacturer specific
    parameter list: - Read parameters on the RC based on robot manufacturers-specific parameter
    lists
    """
    ParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    Requested parameter ID in selected parameter list. • 0: undefined (default) • 1..65 535:
    Parameter ID
    """
    SubParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    ID of the requested sub parameter in selected parameter list. • 0: ID 0 (default) (relates only
    to parameters without sub parameters) • 1..255: Indices 1 to 255 (relates only to parameters
    with sub parameters)
    """


@_dataclass(kw_only=True, slots=True)
class ReadToolDataOutCmd:
    """ReadToolDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNoReturn: int = 0
    """Tool index"""
    ToolData: _s.ToolData = _field(default_factory=lambda: ToolData())
    """Tool data (see chapter 5.5.6.3)"""


@_dataclass(kw_only=True, slots=True)
class ReadToolDataParCmd:
    """ReadToolDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """
    Tool index • -1: Currently used tool on RC • 0: Flange - Not possible to change • 1
    (default)..254: Tool Frame
    """


@_dataclass(kw_only=True, slots=True)
class ReadToolDataRecvData(RspHeader):
    """ReadToolDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    ToolNoReturn: int = 0
    """Tool index"""
    ToolData: _s.ToolData = _field(default_factory=lambda: ToolData())
    """Tool data (see chapter 5.5.6.3)"""
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadToolDataSendData(CmdHeader):
    """ReadToolDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """
    Tool index • -1: Currently used tool on RC • 0: Flange - Not possible to change • 1
    (default)..254: Tool Frame
    """


@_dataclass(kw_only=True, slots=True)
class SearchHardStopOutCmd:
    """SearchHardStopOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    InClamping: bool = False
    """The robot arm has detected an obstruction and stopped the movement"""


@_dataclass(kw_only=True, slots=True)
class SearchHardStopParCmd:
    """SearchHardStopParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    DetectionMode: _e.DetectionMode = _e.DetectionMode.TORQUE
    """Defines the type of collision detection, which parameter should be observed"""
    DetectionVector: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Additional parameter for the detection of an end position. Defines the limits for seven joints,
    where the robot stops when one of the limits is reached. Unit is depending on the
    "DetectionMode": • Torque (default) [Nm] - Only positive values accepted • Force [N] - Only
    positive values accepted • Electrical current [A] - Only positive values accepted • Following
    Error [mm] - >0: Robot stops when the following error reached positive limit - <0: Robot stops
    when the following error reaches the negative limit
    """
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    OriMode: _e.OriMode = _e.OriMode.LINEAR_INTERPOLATED
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    ConfigMode: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: _e.TurnMode = _e.TurnMode.USE_TURN_NUMBER
    """Defines the usage of the TurnNumber byte inside the position."""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """


@_dataclass(kw_only=True, slots=True)
class SearchHardStopRecvData(RspHeader):
    """SearchHardStopRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    InClamping: bool = False
    """The robot arm has detected an obstruction and stopped the movement"""


@_dataclass(kw_only=True, slots=True)
class SearchHardStopSendData(CmdHeader):
    """SearchHardStopSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Absolute target coordinates in the selected coordinate system (see input parameters ToolNo and
    FrameNo)
    """
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    DetectionMode: int = 0
    """Defines the type of collision detection, which parameter should be observed"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve: int = 0
    """Reserve"""
    DetectionVector: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Additional parameter for the detection of an end position. Defines the limits for seven joints,
    where the robot stops when one of the limits is reached. Unit is depending on the
    "DetectionMode": • Torque (default) [Nm] - Only positive values accepted • Force [N] - Only
    positive values accepted • Electrical current [A] - Only positive values accepted • Following
    Error [mm] - >0: Robot stops when the following error reached positive limit - <0: Robot stops
    when the following error reaches the negative limit
    """
    ConfigMode: list[int] = _field(default_factory=lambda: [0] * 2)
    """Defines the usage of the config byte inside the position according to Table 6-238"""
    TurnMode: int = 0
    """Defines the usage of the TurnNumber byte inside the position."""


@_dataclass(kw_only=True, slots=True)
class SearchHardStopJOutCmd:
    """SearchHardStopJOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    InClamping: bool = False
    """The robot arm has detected an obstruction and stopped the movement"""


@_dataclass(kw_only=True, slots=True)
class SearchHardStopJParCmd:
    """SearchHardStopJParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute end position of the robot in Joint position."""
    DetectionMode: _e.DetectionMode = _e.DetectionMode.TORQUE
    """Defines the type of collision detection, which parameter should be observed"""
    DetectionVector: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Additional parameter for the detection of an end position. Defines the limits for seven joints,
    where the robot stops when one of the limits is reached. Unit is depending on the
    "DetectionMode": • Torque (default) [Nm] - Only positive values accepted • Force [N] - Only
    positive values accepted • Electrical current [A] - Only positive values accepted • Following
    Error [mm] - >0: Robot stops when the following error reached positive limit - <0: Robot stops
    when the following error reaches the negative limit
    """
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """


@_dataclass(kw_only=True, slots=True)
class SearchHardStopJRecvData(RspHeader):
    """SearchHardStopJRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    InClamping: bool = False
    """The robot arm has detected an obstruction and stopped the movement"""


@_dataclass(kw_only=True, slots=True)
class SearchHardStopJSendData(CmdHeader):
    """SearchHardStopJSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity • <0%: (default) - Use default velocity • 0%: - Use
    internal minimal velocity • 100%: - Use maximal reference velocity See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration • <0%: (default) - Use default
    acceleration • 0%: - Use internal minimal acceleration • 100%: - Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration • <0%: (default) - Use default
    deceleration • 0%: - Use internal minimal deceleration • 100%: - Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk • <0%: (default) - Use default jerk • 0%: - Use
    internal minimal jerk • 100%: - Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    JointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Absolute end position of the robot in Joint position."""
    OriMode: int = 0
    """
    Parameter to describe how the orientation axes (RX, RY, RZ) will be interpolated during the
    movement
    """
    DetectionMode: int = 0
    """Defines the type of collision detection, which parameter should be observed"""
    Manipulation: bool = False
    """
    Set TRUE to allow manipulation of this move command through superimposing functions. For more
    information see chapter 5.5.9.5
    """
    Reserve: int = 0
    """Reserve"""
    DetectionVector: list[float] = _field(default_factory=lambda: [0.0] * 6)
    """
    Additional parameter for the detection of an end position. Defines the limits for seven joints,
    where the robot stops when one of the limits is reached. Unit is depending on the
    "DetectionMode": • Torque (default) [Nm] - Only positive values accepted • Force [N] - Only
    positive values accepted • Electrical current [A] - Only positive values accepted • Following
    Error [mm] - >0: Robot stops when the following error reached positive limit - <0: Robot stops
    when the following error reaches the negative limit
    """


@_dataclass(kw_only=True, slots=True)
class CreateSplineOutCmd:
    """CreateSplineOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class CreateSplineParCmd:
    """CreateSplineParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.SplineMode = _e.SplineMode.DISCRETE_POINTS
    """Define the method to calculate the path trajectory for the spline movement"""
    SplineID: int = 0
    """Index of the spline trajectory to be created"""
    SplineData: _iec.IecArray[_s.SplineData] = _field(default_factory=lambda: _iec.IecArray(1, [SplineData() for _ in range(_iec.array_len(1, _iec.Param('SPLINE_DATA_MAX')))]))
    """
    Contains all data relevant to the spline trajectory • Cartesian position • Coordinate systems •
    Dynamic parameters For more information refer to chapter 5.5.13.3
    """


@_dataclass(kw_only=True, slots=True)
class CreateSplineRecvData(RspHeader):
    """CreateSplineRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class CreateSplineSendData(CmdHeader):
    """CreateSplineSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: int = 0
    """Define the method to calculate the path trajectory for the spline movement"""
    SplineID: int = 0
    """Index of the spline trajectory to be created"""
    SplineData: _iec.IecArray[SplineDataSend] = _field(default_factory=lambda: _iec.IecArray(1, [SplineDataSend() for _ in range(_iec.array_len(1, _iec.Param('SPLINE_DATA_MAX')))]))
    """
    Contains all data relevant to the spline trajectory • Cartesian position • Coordinate systems •
    Dynamic parameters For more information refer to chapter 5.5.13.3
    """


@_dataclass(kw_only=True, slots=True)
class DeleteSplineOutCmd:
    """DeleteSplineOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class DeleteSplineParCmd:
    """DeleteSplineParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SplineID: int = 0
    """Index of the spline trajectory to be deleted"""


@_dataclass(kw_only=True, slots=True)
class DeleteSplineRecvData(RspHeader):
    """DeleteSplineRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class DeleteSplineSendData(CmdHeader):
    """DeleteSplineSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SplineID: int = 0
    """Index of the spline trajectory to be deleted"""


@_dataclass(kw_only=True, slots=True)
class DynamicSplineOutCmd:
    """DynamicSplineOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    SegmentProgress: float = 0.0
    """
    Percentage of already traversed distance of actual segment of spline trajectory. If not
    supported: -1
    """
    Buffered: int = 0
    """Number of buffered, consecutive segments of spline trajectory."""
    Calculated: int = 0
    """
    Number of calculated, consecutive segments of spline trajectory. Already calculated segments can
    no longer be modified.
    """
    ActiveIndex: int = 0
    """Index of the currently active segment of spline data set."""
    TrajectoryCompleted: bool = False
    """Spline movement has been finished successfully. New SplineData will start a new spline movement."""


@_dataclass(kw_only=True, slots=True)
class DynamicSplineParCmd:
    """DynamicSplineParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.SplineMode = _e.SplineMode.DISCRETE_POINTS
    """Define the method to calculate the path trajectory for the spline movement"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius
    • [0]: default 10 • [1]: default 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default): • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC, if the
    time cannot be kept.
    """
    SplineData: _iec.IecArray[_s.SplineData] = _field(default_factory=lambda: _iec.IecArray(1, [SplineData() for _ in range(_iec.array_len(1, _iec.Param('SPLINE_DATA_MAX')))]))
    """
    Contains all data relevant to the spline trajectory • Cartesian position • Coordinate systems •
    Dynamic parameters For more information refer to chapter 5.5.13.3
    """
    StartPosition: int = 0
    """
    Starts calculation and spline motion when equal or greater to number of buffered spline
    positions
    """


@_dataclass(kw_only=True, slots=True)
class DynamicSplineRecvData(RspHeader):
    """DynamicSplineRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    SegmentProgress: float = 0.0
    """
    Percentage of already traversed distance of actual segment of spline trajectory. If not
    supported: -1
    """
    Buffered: int = 0
    """Number of buffered, consecutive segments of spline trajectory."""
    Calculated: int = 0
    """
    Number of calculated, consecutive segments of spline trajectory. Already calculated segments can
    no longer be modified.
    """
    ActiveIndex: int = 0
    """Index of the currently active segment of spline data set."""
    TrajectoryCompleted: bool = False
    """Spline movement has been finished successfully. New SplineData will start a new spline movement."""


@_dataclass(kw_only=True, slots=True)
class DynamicSplineSendData(CmdHeader):
    """DynamicSplineSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: int = 0
    """Define the method to calculate the path trajectory for the spline movement"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius
    • [0]: default 10 • [1]: default 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default): • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC, if the
    time cannot be kept.
    """
    StartPosition: int = 0
    """
    Starts calculation and spline motion when equal or greater to number of buffered spline
    positions
    """
    SplineData: _iec.IecArray[SplineDataSend] = _field(default_factory=lambda: _iec.IecArray(1, [SplineDataSend() for _ in range(_iec.array_len(1, _iec.Param('SPLINE_DATA_MAX')))]))
    """
    Contains all data relevant to the spline trajectory • Cartesian position • Coordinate systems •
    Dynamic parameters For more information refer to chapter 5.5.13.3
    """


@_dataclass(kw_only=True, slots=True)
class MoveSplineOutCmd:
    """MoveSplineOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActualIndex: int = 0
    """Index of the currently active segment of spline data set."""
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveSplineParCmd:
    """MoveSplineParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SplineID: int = 0
    """Index of the spline data set, on which the spline trajectory is based"""
    BlendingMode: _e.BlendingMode = _e.BlendingMode.EXACT_STOP
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius
    • [0]: default 10 • [1]: default 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default): • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC, if the
    time cannot be kept.
    """


@_dataclass(kw_only=True, slots=True)
class MoveSplineRecvData(RspHeader):
    """MoveSplineRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveSplineSendData(CmdHeader):
    """MoveSplineSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SplineID: int = 0
    """Index of the spline data set, on which the spline trajectory is based"""
    BlendingMode: int = 0
    """
    Parameter which determines the transition behavior at the end of the movement to be sent to the
    next command. The user can choose a transition type between exact stop and different blend
    possibilities.
    """
    BlendingParameter: list[float] = _field(default_factory=lambda: [0.0] * 2)
    """
    Additional parameter for the blending mode, to define i.e. velocity limit (%) or blending radius
    • [0]: default 10 • [1]: default 0
    """
    MoveTime: int = 0
    """
    Parameter is used if it is greater than 0 (default): • Velocity input is ignored • Parameter
    defines the time for the movement to reach the target position Error is sent by the RC, if the
    time cannot be kept.
    """


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedOutCmd:
    """MoveSuperImposedOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedParCmd:
    """MoveSuperImposedParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Additional distance and orientation for superimposed positioning:"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position."""
    VelocityDiffRate: float = 0.0
    """
    Value of the maximum velocity difference of the additional motion (not necessary reached). • >
    0% Use specified value. • ≤ 0% Use the velocity defined by the move command that is
    superimposed. If no motion is active, use internal minimal velocity. (default) See chapter 5.5.7
    Robot dynamics
    """
    AccelerationDiffRate: float = 0.0
    """
    Value of the maximum acceleration difference of the additional motion (not necessary reached). •
    <0% Use default acceleration (default) • 0% Use internal minimal acceleration • 100% Use maximal
    reference acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationDiffRate: float = 0.0
    """
    Value of the maximum deceleration difference of the additional motion (not necessary reached). •
    <0% Use default deceleration (default) • 0% Use internal minimal deceleration • 100% Use maximal
    reference deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkDiffRate: float = 0.0
    """
    Value of the maximum jerk difference of the additional motion (not necessary reached). • <0% Use
    default jerk (default) • 0% Use internal minimal jerk • 100% Use maximal reference jerk See
    chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default) - Start executing
    this function immediately. • >0: Trigger - Start executing when the trigger function with the
    identical positive EmitterID is called - Stop executing when the trigger function with the
    identical negative EmitterID is called. For more information see chapter 5.5.12.4.
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedRecvData(RspHeader):
    """MoveSuperImposedRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedSendData(CmdHeader):
    """MoveSuperImposedSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of the trigger function that may be triggered: • 0: Immediately (default). - Start executing
    THIS function immediately. • >0: Triggero Start executing when the trigger function with the
    identical EmitterID is called. For more information see chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    VelocityDiffRate: int = 0
    """
    Value of the maximum velocity difference of the additional motion (not necessary reached). • >
    0% Use specified value. • ≤ 0% Use the velocity defined by the move command that is
    superimposed. If no motion is active, use internal minimal velocity. (default) See chapter 5.5.7
    Robot dynamics
    """
    AccelerationDiffRate: int = 0
    """
    Value of the maximum acceleration difference of the additional motion (not necessary reached). •
    <0% Use default acceleration (default) • 0% Use internal minimal acceleration • 100% Use maximal
    reference acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationDiffRate: int = 0
    """
    Value of the maximum deceleration difference of the additional motion (not necessary reached). •
    <0% Use default deceleration (default) • 0% Use internal minimal deceleration • 100% Use maximal
    reference deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkDiffRate: int = 0
    """
    Value of the maximum jerk difference of the additional motion (not necessary reached). • <0% Use
    default jerk (default) • 0% Use internal minimal jerk • 100% Use maximal reference jerk See
    chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Additional distance and orientation for superimposed positioning:"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position"""
    Reserve2: int = 0
    """Reserve2"""


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedDynamicOutCmd:
    """MoveSuperImposedDynamicOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RemainingDistance: float = 0.0
    """
    Distance-to-go [mm] of the current job • -1: No valid value because move command is not yet
    active (valid values are pending) or not supported by RC • >0: Actual distance between current
    and target position • 0: Target position reached
    """
    Progress: float = 0.0
    """Percentage of already traversed superimposed offset. If not supported : • -1"""
    OffsetReached: bool = False
    """TRUE if the offset for superimposed positioning is reached."""


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedDynamicParCmd:
    """MoveSuperImposedDynamicParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Additional distance and orientation for superimposed positioning"""
    ReferenceType: _e.ReferenceType = _e.ReferenceType.TOOL
    """Defines type of reference coordinate system of the offset position."""
    VelocityDiffRate: float = 0.0
    """
    Value of the maximum velocity difference of the additional motion (not necessary reached). • >
    0% Use specified value. • ≤ 0% Use the velocity defined by the move command that is
    superimposed. If no motion is active, use internal minimal velocity. (default) See chapter 5.5.7
    Robot dynamics
    """
    AccelerationDiffRate: float = 0.0
    """
    Value of the maximum acceleration difference of the additional motion (not necessary reached). •
    <0% Use default acceleration (default) • 0% Use internal minimal acceleration • 100% Use maximal
    reference acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationDiffRate: float = 0.0
    """
    Value of the maximum deceleration difference of the additional motion (not necessary reached). •
    <0% Use default deceleration (default) • 0% Use internal minimal deceleration • 100% Use maximal
    reference deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkDiffRate: float = 0.0
    """
    Value of the maximum jerk difference of the additional motion (not necessary reached). • <0% Use
    default jerk (default) • 0% Use internal minimal jerk • 100% Use maximal reference jerk See
    chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    InterpolationMode: _e.InterpolationMode = _e.InterpolationMode.Linear_interpolation
    """Define the interpolation mode for the superimposed motion"""


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedDynamicRecvData(RspHeader):
    """MoveSuperImposedDynamicRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Progress: int = 0
    """Percentage of already traversed distance of current job. If not supported : • -1"""
    RemainingDistance: float = 0.0
    """
    Distance-to-go of the current job. • -1: No valid value because move command is not yet active
    (valid values are pending) or not supported by RC • >0: Actual distance between current and
    target position • 0: Target position reached
    """
    OffsetReached: bool = False
    """TRUE if the offset for superimposed positioning is reached."""


@_dataclass(kw_only=True, slots=True)
class MoveSuperImposedDynamicSendData(CmdHeader):
    """MoveSuperImposedDynamicSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityDiffRate: int = 0
    """
    Value of the maximum velocity difference of the additional motion (not necessary reached). • >
    0% Use specified value. • ≤ 0% Use the velocity defined by the move command that is
    superimposed. If no motion is active, use internal minimal velocity. (default) See chapter 5.5.7
    Robot dynamics
    """
    AccelerationDiffRate: int = 0
    """
    Value of the maximum acceleration difference of the additional motion (not necessary reached). •
    <0% Use default acceleration (default) • 0% Use internal minimal acceleration • 100% Use maximal
    reference acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationDiffRate: int = 0
    """
    Value of the maximum deceleration difference of the additional motion (not necessary reached). •
    <0% Use default deceleration (default) • 0% Use internal minimal deceleration • 100% Use maximal
    reference deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkDiffRate: int = 0
    """
    Value of the maximum jerk difference of the additional motion (not necessary reached). • <0% Use
    default jerk (default) • 0% Use internal minimal jerk • 100% Use maximal reference jerk See
    chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame • 0: WCS (default) • 1..254: User frames"""
    Reserve_X: float = 0.0
    """Reserve X"""
    Offset: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Additional distance and orientation for superimposed positioning"""
    ReferenceType: int = 0
    """Defines type of reference coordinate system of the offset position."""
    InterpolationMode: int = 0
    """Define the interpolation mode for the superimposed motion"""


@_dataclass(kw_only=True, slots=True)
class ReactAtTriggerOutCmd:
    """ReactAtTriggerOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class ReactAtTriggerParCmd:
    """ReactAtTriggerParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReactionMode: _e.TriggerReactionMode = _e.TriggerReactionMode.NO_REACTION
    """Defines RC’s and robot’s behavior when the"Action" is executed."""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class ReactAtTriggerRecvData(RspHeader):
    """ReactAtTriggerRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class ReactAtTriggerSendData(CmdHeader):
    """ReactAtTriggerSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    ReactionMode: _e.TriggerReactionMode = _e.TriggerReactionMode.NO_REACTION
    """Defines RC’s and robot’s behavior when the"Action" is executed."""


@_dataclass(kw_only=True, slots=True)
class SetTriggerErrorOutCmd:
    """SetTriggerErrorOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by user. For more
    information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerErrorParCmd:
    """SetTriggerErrorParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Mode: _e.ErrorTriggerMode = _e.ErrorTriggerMode.ANY_COMMAND
    """Defines error origin through which the associated Action will be triggered"""
    MessageCodes: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('MESSAGE_CODES_MAX')))
    """
    Defines message codes through which the associated Action will be triggered (relates to Mode 6
    and 7)
    """
    IncludeParameterValidation: bool = False
    """
    Defines if parametrization messages are included (relates to Mode 0 to 5) • FALSE (default): Do
    not include incorrect parametrization • TRUE: Include incorrect parametrization
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    EmitterID: int = 0
    """
    ID of the Action function that will be executed when the trigger condition is met • >0: Start
    Action - Start executing the Action function with the identical ListenerID. • <0: Stop Action -
    Stop executing the Action function with the identical ListenerID. • 0: Undefined (default) - If
    no EmitterID is defined, the function returns an error message For more information see chapter
    5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerErrorRecvData(RspHeader):
    """SetTriggerErrorRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerErrorSendData(CmdHeader):
    """SetTriggerErrorSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Mode: int = 0
    """Defines error origin through which the associated Action will be triggered"""
    IncludeParameterValidation: bool = False
    """
    Defines if parametrization messages are included (relates to Mode 0 to 5) • FALSE (default): Do
    not include incorrect parametrization • TRUE: Include incorrect parametrization
    """
    MessageCodes: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('MESSAGE_CODES_MAX')))
    """
    Defines message codes through which the associated Action will be triggered (relates to Mode 6
    and 7)
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerLimitOutCmd:
    """SetTriggerLimitOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by user. For more
    information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerLimitParCmd:
    """SetTriggerLimitParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TriggerMode: _e.TriggerModeLimit = _e.TriggerModeLimit.INVALID
    """
    Specifies the trigger event by exceeding of the following limit values (one of the following
    options must be supported)
    """
    EvaluateStartCondition: bool = False
    """
    Determines whether the start condition is evaluated or not. • FALSE: Start condition is not
    evaluated (default). • TRUE: Start condition is evaluated
    """
    Data_1: list[float] = _field(default_factory=lambda: [0.0] * 12)
    """
    If the tolerance limits for the respective actual data values from the RC are exceeded, the
    Action function that will be executed. For "TriggerMode" 1, 2 and 4 the tolerance limits must be
    entered as follows: • [0..5]: relates to axes 1 to 6 • [6..11]: relates to external axes 1 to 6.
    For "TriggerMode" 3 the tolerance limits must be entered as follows: • [0]: Following Error in
    mm. • [1..11]: Undefined and not relevant. For all array entries default: 999999
    """
    Data_2: list[float] = _field(default_factory=lambda: [0.0] * 12)
    """
    If the respective actual data values from the RC are under the defined limit, the Action
    function will be stopped. For "TriggerMode" 1, 2 and 4 the tolerance limits must be entered as
    follows: • [0..5]: relates to axes 1 to 6. • [6..11]: relates to external axes 1 to 6. For
    "TriggerMode" 3 the tolerance limits must be entered as follows: • [0]: Following Error in mm. •
    [1..11]: Undefined and not relevant. For all array entries default: 999999
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    EmitterID: int = 0
    """
    ID of the Action function that will be executed when the trigger condition is met • >0: Start
    Action - Start executing the Action function with the identical ListenerID. • <0: Stop Action -
    Stop executing the Action function with the identical ListenerID. • 0: Undefined (default) - If
    no EmitterID is defined, the function returns an error message For more information see chapter
    5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerLimitRecvData(RspHeader):
    """SetTriggerLimitRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    Data: list[float] = _field(default_factory=lambda: [0.0] * 12)
    """The respective actual data values from the RC that depend on "TriggerMode"."""


@_dataclass(kw_only=True, slots=True)
class SetTriggerLimitSendData(CmdHeader):
    """SetTriggerLimitSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Data_1: list[float] = _field(default_factory=lambda: [0.0] * 12)
    """
    If the tolerance limits for the respective actual data values from the RC are exceeded, the
    Action function that will be executed. For "TriggerMode" 1, 2 and 4 the tolerance limits must be
    entered as follows: • [0..5]: relates to axes 1 to 6 • [6..11]: relates to external axes 1 to 6.
    For "TriggerMode" 3 the tolerance limits must be entered as follows: • [0]: Following Error in
    mm. • [1..11]: Undefined and not relevant. For all array entries default: 999999
    """
    Data_2: list[float] = _field(default_factory=lambda: [0.0] * 12)
    """
    If the respective actual data values from the RC are under the defined limit, the Action
    function will be stopped. For "TriggerMode" 1, 2 and 4 the tolerance limits must be entered as
    follows: • [0..5]: relates to axes 1 to 6. • [6..11]: relates to external axes 1 to 6. For
    "TriggerMode" 3 the tolerance limits must be entered as follows: • [0]: Following Error in mm. •
    [1..11]: Undefined and not relevant. For all array entries default: 999999
    """
    TriggerMode: int = 0
    """
    Specifies the trigger event by exceeding of the following limit values (one of the following
    options must be supported)
    """
    EvaluateStartCondition: bool = False
    """
    Determines whether the start condition is evaluated or not. • FALSE: Start condition is not
    evaluated (default). • TRUE: Start condition is evaluated
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerMotionOutCmd:
    """SetTriggerMotionOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by user. For more
    information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerMotionParCmd:
    """SetTriggerMotionParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TriggerMode_1: _e.TriggerCondition = _e.TriggerCondition.TARGET_POSITION_TIME_MS
    """Defines the trigger condition on which the related Action function will be started:"""
    TriggerParameter_1: float = 0.0
    """
    This parameter depends on the input parameter "TriggerMode_1": • 1: Distance value of trajectory
    in %. • 2: Distance value of trajectory in mm. • 3: TCP velocity value of reference velocity in
    % • 4: TCP velocity value of reference velocity in mm. • 5: Time in ms The value of the
    parameter must be positive
    """
    TriggerMode_2: _e.TriggerCondition = _e.TriggerCondition.TARGET_POSITION_TIME_MS
    """Defines the trigger condition on which the related Action function will be started:"""
    TriggerParameter_2: float = 0.0
    """
    This parameter depends on the input parameter "TriggerMode_1": • 1: Distance value of trajectory
    in %. • 2: Distance value of trajectory in mm. • 3: TCP velocity value of reference velocity in
    % • 4: TCP velocity value of reference velocity in mm. • 5: Time in ms The value of the
    parameter must be positive
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of the Action function that will be executed when the trigger condition is met • >0: Start
    Action - Start executing the Action function with the identical ListenerID. • <0: Stop Action -
    Stop executing the Action function with the identical ListenerID. • 0: Undefined (default) - If
    no EmitterID is defined, the function returns an error message For more information see chapter
    5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerMotionRecvData(RspHeader):
    """SetTriggerMotionRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerMotionSendData(CmdHeader):
    """SetTriggerMotionSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    TriggerMode_1: int = 0
    """
    If the tolerance limits for the respective actual data values from the RC are exceeded, the
    Action function that will be executed. For "TriggerMode" 1, 2 and 4 the tolerance limits must be
    entered as follows: • [0..5]: relates to axes 1 to 6 • [6..11]: relates to external axes 1 to 6.
    For "TriggerMode" 3 the tolerance limits must be entered as follows: • [0]: Following Error in
    mm. • [1..11]: Undefined and not relevant. For all array entries default: 999999 Defines the
    trigger condition on which the related Action function will be started:
    """
    TriggerMode_2: int = 0
    """Defines the trigger condition on which the related Action function will be started:"""
    TriggerParameter_1: float = 0.0
    """
    This parameter depends on the input parameter "TriggerMode_1": • 1: Distance value of trajectory
    in %. • 2: Distance value of trajectory in mm. • 3: TCP velocity value of reference velocity in
    % • 4: TCP velocity value of reference velocity in mm. • 5: Time in ms The value of the
    parameter must be positive
    """
    TriggerParameter_2: float = 0.0
    """
    This parameter depends on the input parameter "TriggerMode_1": • 1: Distance value of trajectory
    in %. • 2: Distance value of trajectory in mm. • 3: TCP velocity value of reference velocity in
    % • 4: TCP velocity value of reference velocity in mm. • 5: Time in ms The value of the
    parameter must be positive
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerRegisterOutCmd:
    """SetTriggerRegisterOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by user. For more
    information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerRegisterParCmd:
    """SetTriggerRegisterParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    TriggerMode: _e.TriggerModeIo = _e.TriggerModeIo.INVALID
    """
    Specifies the trigger event according to Table 6-574. For more information about registers on
    the RC see chapters 6.4.4 and 6.4.5.
    """
    EvaluateStartCondition: bool = False
    """
    Determines whether the start condition is evaluated or not. • FALSE: Start condition is not
    evaluated (default). • TRUE: Start condition is evaluated.
    """
    Index: int = 0
    """
    Depending on "TriggerMode": • Digital (refers to "TriggerMode" 10-13, 20-23): Specifies the
    desired byte address of the input or output signal that shall be read. • Analog/Integer/Real
    (refers to "TriggerMode" 30-37, 40-47, 50-57, 60- 67): Specifies the target values that shall be
    read. For more information about registers refer to Figure 6-206.
    """
    BitIndex: int = 0
    """
    Depending on "TriggerMode": • Digital (refers to TriggerMode 10-13,20-23): Specifies the desired
    bit address of the input or output signal that shall be read. • Analog/Integer/Real (refers to
    TriggerMode 30-37, 40-47, 50-57, 60- 67): Not relevant and deactivated for user input. For more
    information about registers refer to Figure 6-206
    """
    IntValue: _iec.IecArray[int] = _field(default_factory=lambda: _iec.IecArray(1, [0] * 2))
    """
    Reference integer value, for triggering the Action function with the EmitterID. • Relates to
    "TriggerMode" 50-57
    """
    RealValue: _iec.IecArray[float] = _field(default_factory=lambda: _iec.IecArray(1, [0.0] * 2))
    """
    Reference real value, analog input or output value, for triggering the Action function with the
    EmitterID. • Relates to "TriggerMode" 30-37, 40-47,60-67
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default). - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    EmitterID: int = 0
    """
    ID of the Action function that will be executed when the trigger condition is met • >0: Start
    Action - Start executing the Action function with the identical ListenerID. • <0: Stop Action -
    Stop executing the Action function with the identical ListenerID. • 0: Undefined (default) - If
    no EmitterID is defined, the function returns an error message For more information see chapter
    5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerRegisterRecvData(RspHeader):
    """SetTriggerRegisterRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerRegisterSendData(CmdHeader):
    """SetTriggerRegisterSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    IntValue: _iec.IecArray[int] = _field(default_factory=lambda: _iec.IecArray(1, [0] * 2))
    """
    Reference integer value, for triggering the Action function with the EmitterID. • Relates to
    "TriggerMode" 50-57
    """
    RealValue: _iec.IecArray[float] = _field(default_factory=lambda: _iec.IecArray(1, [0.0] * 2))
    """
    Reference real value, analog input or output value, for triggering the Action function with the
    EmitterID. • Relates to "TriggerMode" 30-37, 40-47,60-67
    """
    TriggerMode: int = 0
    """
    Specifies the trigger event according to Table 6-574. For more information about registers on
    the RC see chapters 6.4.4 and 6.4.5.
    """
    Index: int = 0
    """
    Depending on "TriggerMode": • Digital (refers to "TriggerMode" 10-13, 20-23): Specifies the
    desired byte address of the input or output signal that shall be read. • Analog/Integer/Real
    (refers to "TriggerMode" 30-37, 40-47, 50-57, 60- 67): Specifies the target values that shall be
    read. For more information about registers refer to Figure 6-206.
    """
    BitIndex: int = 0
    """
    Depending on "TriggerMode": • Digital (refers to TriggerMode 10-13,20-23): Specifies the desired
    bit address of the input or output signal that shall be read. • Analog/Integer/Real (refers to
    TriggerMode 30-37, 40-47, 50-57, 60- 67): Not relevant and deactivated for user input. For more
    information about registers refer to Figure 6-206
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerUserOutCmd:
    """SetTriggerUserOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    FollowID: int = 0
    """
    Unique system-generated ID of the trigger function when the function is called by user. For more
    information see chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerUserParCmd:
    """SetTriggerUserParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: int = 0
    """
    ID of the Action function that will be executed when the trigger condition is met • >0: Start
    Action - Start executing the Action function with the identical ListenerID. • <0: Stop Action -
    Stop executing the Action function with the identical ListenerID. • 0: Undefined (default) - If
    no EmitterID is defined, the function returns an error message For more information see chapter
    5.5.12.4
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerUserRecvData(RspHeader):
    """SetTriggerUserRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class SetTriggerUserSendData(CmdHeader):
    """SetTriggerUserSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    IntValue: _iec.IecArray[int] = _field(default_factory=lambda: _iec.IecArray(1, [0] * 2))
    """
    Reference integer value, for triggering the Action function with the EmitterID. • Relates to
    "TriggerMode" 50-57
    """
    RealValue: _iec.IecArray[float] = _field(default_factory=lambda: _iec.IecArray(1, [0.0] * 2))
    """
    Reference real value, analog input or output value, for triggering the Action function with the
    EmitterID. • Relates to "TriggerMode" 30-37, 40-47,60-67
    """
    TriggerMode: int = 0
    """
    Specifies the trigger event according to Table 6-574. For more information about registers on
    the RC see chapters 6.4.4 and 6.4.5.
    """
    Index: int = 0
    """
    Depending on "TriggerMode": • Digital (refers to "TriggerMode" 10-13, 20-23): Specifies the
    desired byte address of the input or output signal that shall be read. • Analog/Integer/Real
    (refers to "TriggerMode" 30-37, 40-47, 50-57, 60- 67): Specifies the target values that shall be
    read. For more information about registers refer to Figure 6-206.
    """
    BitIndex: int = 0
    """
    Depending on "TriggerMode": • Digital (refers to TriggerMode 10-13,20-23): Specifies the desired
    bit address of the input or output signal that shall be read. • Analog/Integer/Real (refers to
    TriggerMode 30-37, 40-47, 50-57, 60- 67): Not relevant and deactivated for user input. For more
    information about registers refer to Figure 6-206
    """


@_dataclass(kw_only=True, slots=True)
class WaitForTriggerOutCmd:
    """WaitForTriggerOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class WaitForTriggerParCmd:
    """WaitForTriggerParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    ConditionalWait: bool = False
    """
    Defines the time at which the trigger can be reacted to • 0: Conditional - Trigger signal
    accepted as soon as the function is BUFFERED • 1: Absolute - Trigger signal accepted as soon as
    the function is ACTIVE
    """


@_dataclass(kw_only=True, slots=True)
class WaitForTriggerRecvData(RspHeader):
    """WaitForTriggerRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class WaitForTriggerSendData(CmdHeader):
    """WaitForTriggerSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: Immediately (default) - Start executing this function
    immediately. • >0: Trigger - Start executing, when the trigger function with the identical
    EmitterID is triggered. Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    ConditionalWait: bool = False
    """
    Defines the time at which the trigger can be reacted to • 0: Conditional - Trigger signal
    accepted as soon as the function is BUFFERED • 1: Absolute - Trigger signal accepted as soon as
    the function is ACTIVE
    """


@_dataclass(kw_only=True, slots=True)
class WaitTimeOutCmd:
    """WaitTimeOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ElapsedTime: int = 0
    """Current value of time [ms] that has elapsed since processing of the command has started."""


@_dataclass(kw_only=True, slots=True)
class WaitTimeParCmd:
    """WaitTimeParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WaitTime: int = 0
    """Duration [ms] of the waiting time. The value of the parameter must be positive"""


@_dataclass(kw_only=True, slots=True)
class WaitTimeRecvData(RspHeader):
    """WaitTimeRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ElapsedTime: int = 0
    """Current value of time [ms] that has elapsed since processing of the command has started."""
    Reserve1: int = 0
    """Reserve"""
    Reserve2: int = 0
    """Reserve"""
    Reserve3: int = 0
    """Reserve"""
    Reserve4: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class WaitTimeSendData(CmdHeader):
    """WaitTimeSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WaitTime: int = 0
    """Duration [ms] of the waiting time. The value of the parameter must be positive"""
    Reserve1: int = 0
    """Reserve"""
    Reserve2: int = 0
    """Reserve"""
    Reserve3: int = 0
    """Reserve"""
    Reserve4: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class ActivateWorkAreaOutCmd:
    """ActivateWorkAreaOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ActivateWorkAreaParCmd:
    """ActivateWorkAreaParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNo: int = 0
    """Index of the robot work area to be activated • 0 (default)..254"""
    ActivateArea: bool = False
    """Set to activate work area defined by Index. Reset to deactivate work area defined by Index."""


@_dataclass(kw_only=True, slots=True)
class ActivateWorkAreaRecvData(RspHeader):
    """ActivateWorkAreaRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class ActivateWorkAreaSendData(CmdHeader):
    """ActivateWorkAreaSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNo: int = 0
    """Index of the robot work area to be activated • 0 (default)..254"""
    ActivateArea: bool = False
    """Set to activate work area defined by Index. Reset to deactivate work area defined by Index."""


@_dataclass(kw_only=True, slots=True)
class MonitorWorkAreaOutCmd:
    """MonitorWorkAreaOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActivationState: int = 0
    """Bits return TRUE when work area defined by Index is active"""
    MonitoringState: int = 0
    """Bits return TRUE when violation is reported."""


@_dataclass(kw_only=True, slots=True)
class MonitorWorkAreaParCmd:
    """MonitorWorkAreaParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNo: int = 0
    """Index of robot work area to be monitored • 0 (default)..254"""


@_dataclass(kw_only=True, slots=True)
class MonitorWorkAreaRecvData(RspHeader):
    """MonitorWorkAreaRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActivationState: int = 0
    """Bits return TRUE when work area defined by Index is active"""
    MonitoringState: int = 0
    """Bits return TRUE when violation is reported."""


@_dataclass(kw_only=True, slots=True)
class MonitorWorkAreaSendData(CmdHeader):
    """MonitorWorkAreaSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Enable: bool = False
    """Set TRUE to activate monitoring of work areas"""
    WorkAreaNo: int = 0
    """Index of robot work area to be monitored • 0 (default)..254"""


@_dataclass(kw_only=True, slots=True)
class ReadWorkAreaOutCmd:
    """ReadWorkAreaOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNoReturn: int = 0
    """Index of the robot work area"""
    WorkAreaData: RobotWorkAreaData = _field(default_factory=lambda: RobotWorkAreaData())
    """Data specific to the work area requested by Index."""


@_dataclass(kw_only=True, slots=True)
class ReadWorkAreaParCmd:
    """ReadWorkAreaParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNo: int = 0
    """Index of the robot work area • 0 (default)..254"""


@_dataclass(kw_only=True, slots=True)
class ReadWorkAreaRecvData(RspHeader):
    """ReadWorkAreaRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    WorkAreaNoReturn: int = 0
    """Index of the robot work area"""
    WorkAreaData: RobotWorkAreaData = _field(default_factory=lambda: RobotWorkAreaData())
    """Data specific to the work area requested by Index."""
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class ReadWorkAreaSendData(CmdHeader):
    """ReadWorkAreaSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNo: int = 0
    """Index of the robot work area • 0 (default)..254"""


@_dataclass(kw_only=True, slots=True)
class WriteWorkAreaOutCmd:
    """WriteWorkAreaOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteWorkAreaParCmd:
    """WriteWorkAreaParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    WorkAreaNo: int = 0
    """Index of the robot work area • 0 (default)..254"""
    WorkAreaData: RobotWorkAreaData = _field(default_factory=lambda: RobotWorkAreaData())
    """Data specific to the work area requested by Index."""


@_dataclass(kw_only=True, slots=True)
class WriteWorkAreaRecvData(RspHeader):
    """WriteWorkAreaRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteWorkAreaSendData(CmdHeader):
    """WriteWorkAreaSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    WorkAreaNo: int = 0
    """Index of the robot work area • 0 (default)..254"""
    WorkAreaData: RobotWorkAreaData = _field(default_factory=lambda: RobotWorkAreaData())
    """Data specific to the work area requested by Index."""
    DataChanged: bool = False
    """The status bit "DataChanged" represents the modification state"""


@_dataclass(kw_only=True, slots=True)
class WriteAnalogOutputOutCmd:
    """WriteAnalogOutputOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class WriteAnalogOutputParCmd:
    """WriteAnalogOutputParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: int = 0
    """Number of the analog input 1..32"""
    Value: float = 0.0
    """Value of analog output"""
    Unit: _e.UnitType = _e.UnitType.VOLT
    """Unit of set Value:"""
    HighPriority: bool = False
    """Set TRUE to prioritize the execution of this command in the defined target sequence."""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class WriteAnalogOutputRecvData(RspHeader):
    """WriteAnalogOutputRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class WriteAnalogOutputSendData(CmdHeader):
    """WriteAnalogOutputSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    Reserve: int = 0
    """Reserve"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Index: int = 0
    """Number of the analog input 1..32"""
    Unit: int = 0
    """Unit of set Value:"""
    Value: float = 0.0
    """Value of analog output"""


@_dataclass(kw_only=True, slots=True)
class WriteDigitalOutputsOutCmd:
    """WriteDigitalOutputsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class WriteDigitalOutputsParCmd:
    """WriteDigitalOutputsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies the desired byte addresses that shall be read"""
    OutputBitmask: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies which outputs may be written"""
    Values: list[int] = _field(default_factory=lambda: [0] * 5)
    """Array value of Digital Output"""
    HighPriority: bool = False
    """Set TRUE to prioritize the execution of this command in the defined target sequence."""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class WriteDigitalOutputsRecvData(RspHeader):
    """WriteDigitalOutputsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class WriteDigitalOutputsSendData(CmdHeader):
    """WriteDigitalOutputsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies the desired byte addresses that shall be read"""
    OutputBitmask: list[int] = _field(default_factory=lambda: [0] * 5)
    """Specifies which outputs may be written"""
    Values: list[int] = _field(default_factory=lambda: [0] * 5)
    """Array value of Digital Output"""


@_dataclass(kw_only=True, slots=True)
class WriteFrameDataOutCmd:
    """WriteFrameDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteFrameDataParCmd:
    """WriteFrameDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FrameNo: int = 0
    """Frame index M • 0: WCS (default) O • 1..254: UCS (User frames)"""
    FrameData: _s.FrameData = _field(default_factory=lambda: FrameData())
    """Frame data (see chapter 5.5.6.2)"""


@_dataclass(kw_only=True, slots=True)
class WriteFrameDataRecvData(RspHeader):
    """WriteFrameDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteFrameDataSendData(CmdHeader):
    """WriteFrameDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    FrameData: _s.FrameData = _field(default_factory=lambda: FrameData())
    """Frame data (see chapter 5.5.6.2)"""
    FrameNo: int = 0
    """Frame index M • 0: WCS (default) O • 1..254: UCS (User frames)"""


@_dataclass(kw_only=True, slots=True)
class WriteIntegersOutCmd:
    """WriteIntegersOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class WriteIntegersParCmd:
    """WriteIntegersParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be written"""
    Values: list[int] = _field(default_factory=lambda: [0] * 7)
    """Array value of integers"""
    HighPriority: bool = False
    """Set TRUE to prioritize the execution of this command in the defined target sequence."""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class WriteIntegersRecvData(RspHeader):
    """WriteIntegersRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class WriteIntegersSendData(CmdHeader):
    """WriteIntegersSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be written"""
    Values: list[int] = _field(default_factory=lambda: [0] * 7)
    """Array value of integers"""


@_dataclass(kw_only=True, slots=True)
class WriteLoadDataOutCmd:
    """WriteLoadDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteLoadDataParCmd:
    """WriteLoadDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LoadNo: int = 0
    """
    Specifies the desired target values that shall be written Load index • 0: (default) - Not
    possible to write • 1..254: Load data
    """
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Load data (see chapter 5.5.6.4)"""


@_dataclass(kw_only=True, slots=True)
class WriteLoadDataRecvData(RspHeader):
    """WriteLoadDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteLoadDataSendData(CmdHeader):
    """WriteLoadDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LoadNo: int = 0
    """
    Specifies the desired target values that shall be written Load index • 0: (default) - Not
    possible to write • 1..254: Load data
    """
    LoadData: _s.LoadData = _field(default_factory=lambda: LoadData())
    """Load data (see chapter 5.5.6.4)"""


@_dataclass(kw_only=True, slots=True)
class WriteRealsOutCmd:
    """WriteRealsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4.
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """


@_dataclass(kw_only=True, slots=True)
class WriteRealsParCmd:
    """WriteRealsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be written"""
    Values: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """Array value of reas"""
    HighPriority: bool = False
    """Set TRUE to prioritize the execution of this command in the defined target sequence."""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class WriteRealsRecvData(RspHeader):
    """WriteRealsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """


@_dataclass(kw_only=True, slots=True)
class WriteRealsSendData(CmdHeader):
    """WriteRealsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    Index: list[int] = _field(default_factory=lambda: [0] * 7)
    """Specifies the desired target values that shall be written"""
    Values: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """Array value of reas"""


@_dataclass(kw_only=True, slots=True)
class WriteRobotDefaultDynamicsOutCmd:
    """WriteRobotDefaultDynamicsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DefaultDynamicValues: DefaultDynamics = _field(default_factory=lambda: DefaultDynamics())
    """Commanded dynamics values according to Table 6-141."""


@_dataclass(kw_only=True, slots=True)
class WriteRobotDefaultDynamicsParCmd:
    """WriteRobotDefaultDynamicsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DynamicValues: DefaultDynamics = _field(default_factory=lambda: DefaultDynamics())
    """Default dynamics values according to Table 6-141."""


@_dataclass(kw_only=True, slots=True)
class WriteRobotDefaultDynamicsRecvData(RspHeader):
    """WriteRobotDefaultDynamicsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: int = 0
    """
    Maximum velocity for the axes. Range [%]: • <0% : Use default velocity given by the user • 0% :
    Use internal minimal velocity • 100% : Use the entire reference velocity, given by the user
    """
    AccelerationRate: int = 0
    """
    Maximum acceleration. Range [%]: • <0% : Use default acceleration given by the user • 0% : Use
    internal minimal acceleration • 100% : Use the entire reference acceleration, given by the user
    """
    DecelerationRate: int = 0
    """
    Maximum deceleration. Range [%] : • <0% : Use default deceleration given by the user • 0% : Use
    internal minimal deceleration • 100% : Use the entire reference deceleration, given by the user
    """
    JerkRate: int = 0
    """
    Maximum jerk Range [%] : • <0% : Use default jerk given by the user • 0% : Use internal minimal
    jerk • 100% : Use the entire reference jerk, given by the user (Trapezoidal if possible)
    """


@_dataclass(kw_only=True, slots=True)
class WriteRobotDefaultDynamicsSendData(CmdHeader):
    """WriteRobotDefaultDynamicsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    VelocityRate: int = 0
    """
    Maximum velocity for the axes. Range [%]: • <0% : Use default velocity given by the user • 0% :
    Use internal minimal velocity • 100% : Use the entire reference velocity, given by the user
    """
    AccelerationRate: int = 0
    """
    Maximum acceleration. Range [%]: • <0% : Use default acceleration given by the user • 0% : Use
    internal minimal acceleration • 100% : Use the entire reference acceleration, given by the user
    """
    DecelerationRate: int = 0
    """
    Maximum deceleration. Range [%] : • <0% : Use default deceleration given by the user • 0% : Use
    internal minimal deceleration • 100% : Use the entire reference deceleration, given by the user
    """
    JerkRate: int = 0
    """
    Maximum jerk Range [%] : • <0% : Use default jerk given by the user • 0% : Use internal minimal
    jerk • 100% : Use the entire reference jerk, given by the user (Trapezoidal if possible)
    """


@_dataclass(kw_only=True, slots=True)
class WriteRobotReferenceDynamicsOutCmd:
    """WriteRobotReferenceDynamicsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferenceDynamicValues: ReferenceDynamics = _field(default_factory=lambda: ReferenceDynamics())
    """Commanded reference dynamics values according to Table 6-134"""


@_dataclass(kw_only=True, slots=True)
class WriteRobotReferenceDynamicsParCmd:
    """WriteRobotReferenceDynamicsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DynamicValues: ReferenceDynamics = _field(default_factory=lambda: ReferenceDynamics())
    """Reference dynamics values according TO Table 6-134."""


@_dataclass(kw_only=True, slots=True)
class WriteRobotReferenceDynamicsRecvData(RspHeader):
    """WriteRobotReferenceDynamicsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ReferenceDynamicValues: ReferenceDynamics = _field(default_factory=lambda: ReferenceDynamics())
    """Commanded reference dynamics values according to Table 6-134"""


@_dataclass(kw_only=True, slots=True)
class WriteRobotReferenceDynamicsSendData(CmdHeader):
    """WriteRobotReferenceDynamicsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    DynamicValues: ReferenceDynamics = _field(default_factory=lambda: ReferenceDynamics())


@_dataclass(kw_only=True, slots=True)
class WriteRobotSWLimitsOutCmd:
    """WriteRobotSWLimitsOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RestartRequested: bool = False
    """TRUE, when Software limits were overwritten but not activated on RC until a restart of the RC"""


@_dataclass(kw_only=True, slots=True)
class WriteRobotSWLimitsParCmd:
    """WriteRobotSWLimitsParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LimitValues: SWLimits = _field(default_factory=lambda: SWLimits())
    """Limits for joints and external axes according to Table 6-180."""
    ResetToFactoryDefaults: bool = False
    """Reset limits to RC specific factory settings"""


@_dataclass(kw_only=True, slots=True)
class WriteRobotSWLimitsRecvData(RspHeader):
    """WriteRobotSWLimitsRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RestartRequested: bool = False
    """TRUE, when Software limits were overwritten but not activated on RC until a restart of the RC"""


@_dataclass(kw_only=True, slots=True)
class WriteRobotSWLimitsSendData(CmdHeader):
    """WriteRobotSWLimitsSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LimitValues: SWLimits = _field(default_factory=lambda: SWLimits())
    """Limits for joints and external axes according to Table 6-180."""
    ResetToFactoryDefaults: bool = False
    """Reset limits to RC specific factory settings"""


@_dataclass(kw_only=True, slots=True)
class WriteSystemVariableOutCmd:
    """WriteSystemVariableOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger function with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger -based command invocations For more
    information refer to chapter 5.5.12.4.
    """
    RestartRequested: bool = False
    """TRUE, when Software limits were overwritten but not activated on RC until a restart of the RC"""


@_dataclass(kw_only=True, slots=True)
class WriteSystemVariableParCmd:
    """WriteSystemVariableParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RCParameter: bool = False
    """
    Defines the parameter list which should be used: • FALSE: Standardized parameter list (default):
    - Read parameters on the RC based on a standardized parameter list • TRUE: Manufacturer specific
    parameter list: - Read parameters on the RC based on robot manufacturers-specific parameter
    lists
    """
    ParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    Requested parameter ID in selected parameter list. • 0: undefined (default) • 1..65 535:
    Parameter ID
    """
    SubParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    ID of the requested sub parameter in selected parameter list. • 0: ID 0 (default) (relates only
    to parameters without sub parameters) • 1..255: Indices 1 to 255 (relates only to parameters
    with sub parameters)
    """
    DataType: list[_e.DataType] = _field(default_factory=lambda: [_e.DataType.TYPE_BOOL] * 8)
    """Parameter data type as specified in Table 6-621."""
    Data_0: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[0] and SubParameterID[0]"""
    Data_1: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[1] and SubParameterID[1]"""
    Data_2: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[2] and SubParameterID[2]"""
    Data_3: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[3] and SubParameterID[3]"""
    Data_4: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[4] and SubParameterID[4]"""
    Data_5: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[5] and SubParameterID[5]"""
    Data_6: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[6] and SubParameterID[6]"""
    Data_7: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[7] and SubParameterID[7]"""
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """


@_dataclass(kw_only=True, slots=True)
class WriteSystemVariableRecvData(RspHeader):
    """WriteSystemVariableRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InvocationCounter: int = 0
    """
    Relates to ListenerID >0 Number of successful trigger-based command invocations - For more
    information refer TO chapter 5.5.12.4
    """
    Reserve: int = 0
    """Reserve"""
    OriginID: int = 0
    """
    Unique system-generated ID of the "Action" when the function is triggered. • >0: The "Action" is
    started by the trigger funcrion with identical FollowID. • <0: The "Action" is stopped by the
    trigger function with identical FollowID. For more information see chapter 5.5.12.4 EmitterID,
    ListenerID, FollowID and OriginID
    """
    RestartRequested: bool = False
    """TRUE, when Software limits were overwritten but not activated on RC until a restart of the RC"""


@_dataclass(kw_only=True, slots=True)
class WriteSystemVariableSendData(CmdHeader):
    """WriteSystemVariableSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EmitterID: list[int] = _field(default_factory=lambda: [0] * 4)
    """
    ID of Action that will be executed when this command is active • >0: Start Action - Start
    executing the Action function with the identical ListenerID. • <0: Stop Action - Stop executing
    the Action function with the identical ListenerID. • 0: No trigger (default)- If no EmitterID is
    defined, the function will not trigger any Action during its execution For more information see
    section Triggers of this chapter or chapter 5.5.12.4.
    """
    ListenerID: int = 0
    """
    ID of associated trigger function: • 0: No Trigger (default) No trigger related behavior • >0:
    Trigger - Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    Reserve: int = 0
    """Reserve"""
    ParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    Requested parameter ID in selected parameter list. • 0: undefined (default) • 1..65 535:
    Parameter ID
    """
    SubParameterID: list[int] = _field(default_factory=lambda: [0] * 8)
    """
    ID of the requested sub parameter in selected parameter list. • 0: ID 0 (default) (relates only
    to parameters without sub parameters) • 1..255: Indices 1 to 255 (relates only to parameters
    with sub parameters)
    """
    DataType: list[int] = _field(default_factory=lambda: [0] * 8)
    """Parameter data type as specified in Table 6-621."""
    Data_0: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[0] and SubParameterID[0]"""
    Data_1: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[1] and SubParameterID[1]"""
    Data_2: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[2] and SubParameterID[2]"""
    Data_3: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[3] and SubParameterID[3]"""
    Data_4: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[4] and SubParameterID[4]"""
    Data_5: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[5] and SubParameterID[5]"""
    Data_6: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[6] and SubParameterID[6]"""
    Data_7: list[int] = _field(default_factory=lambda: [0] * 4)
    """Parameter data addressed by input values of ParameterID[7] and SubParameterID[7]"""
    RCParameter: bool = False
    """
    • FALSE: Standardized parameter list (default): - Read parameters on the RC based on a
    standardized parameter list • TRUE: Manufacturer specific parameter list: - Read parameters on
    the RC based on robot manufacturers-specific parameter lists
    """


@_dataclass(kw_only=True, slots=True)
class WriteToolDataOutCmd:
    """WriteToolDataOutCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteToolDataParCmd:
    """WriteToolDataParCmd"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Tool index • 0: Flange (default) Not possible to change • 1..254: Tool Frame"""
    ToolData: _s.ToolData = _field(default_factory=lambda: ToolData())
    """Tool data (see chapter 5.5.6.3)"""


@_dataclass(kw_only=True, slots=True)
class WriteToolDataRecvData(RspHeader):
    """WriteToolDataRecvData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]


@_dataclass(kw_only=True, slots=True)
class WriteToolDataSendData(CmdHeader):
    """WriteToolDataSendData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    ToolNo: int = 0
    """Tool index • 0: Flange (default) Not possible to change • 1..254: Tool Frame"""
    ToolData: _s.ToolData = _field(default_factory=lambda: ToolData())
    """Tool data (see chapter 5.5.6.3)"""


@_dataclass(kw_only=True, slots=True)
class SplineDataSend:
    """SplineDataSend"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Absolute target coordinates in the selected coordinate system (see ToolNo and FrameNo)."""
    VelocityRate: int = 0
    """
    TCP velocity in % of nominal velocity. • <0% : Use default velocity (default) • 0% : Use
    internal minimal velocity • 100% : Use maximal reference velocity • See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: int = 0
    """
    Acceleration for movement in % of nominal acceleration. • <0% : Use default acceleration
    (default) • 0% : Use internal minimal acceleration • 100% : Use maximal reference acceleration •
    See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: int = 0
    """
    Deceleration for movement in % of nominal deceleration. • <0% : Use default deceleration
    (default) • 0% : Use internal minimal deceleration • 100% : Use maximal reference deceleration •
    See chapter 5.5.7 Robot dynamics
    """
    JerkRate: int = 0
    """
    Jerk of the movement in % of nominal jerk. <0% o Use default jerk (default) 0% o Use internal
    minimal jerk 100% o Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool 0: Flange (default) 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame 0: WCS (default) 1..254: User frames"""
    MoveTime: int = 0
    """
    [ms] Parameter is used if it is greater than 0 (default): Parameter defines the time for the
    movement to reach the target position Velocity input can be ignored Acceleration, Deceleration
    and jerk will be ignored Define two consecutive points with identical positions and specified
    Time to realize waiting time on spline. Error is sent by the RC, if the time cannot be kept.
    """


@_dataclass(kw_only=True, slots=True)
class AxesGroupAcyclic:
    """AxesGroupAcyclic"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ActiveCommandRegister: Any = _field(default_factory=lambda: _iec.new_instance('ActiveCommandRegisterFB'))
    """Active command register"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupAcyclicAcrEntry:
    """AxesGroupAcyclicAcrEntry"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    UniqueID: int = 0
    """Unique indentifier"""
    State: _e.ActiveCommandRegisterState = _e.ActiveCommandRegisterState.IS_FREE
    """State of the command entry"""
    Command: _iec.IecArray[AxesGroupAcyclicAcrEntryCmdBuffer] = _field(default_factory=lambda: _iec.IecArray(1, [AxesGroupAcyclicAcrEntryCmdBuffer() for _ in range(2)]))
    """Command data ( 1 = DataToSend 2 = DataInBuffer )"""
    Response: _iec.IecArray[AxesGroupAcyclicAcrEntryRspBuffer] = _field(default_factory=lambda: _iec.IecArray(1, [AxesGroupAcyclicAcrEntryRspBuffer() for _ in range(2)]))
    """response data ( 1 = DataRecv 2 = DataInRecvBuffer )"""
    pCommandFB: object | None = None
    """Pointer to the corresponding command-FB to enable a callback mechanism"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupAcyclicAcrEntryCmdBuffer:
    """AxesGroupAcyclicAcrEntryCmdBuffer"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: SystemTime = _field(default_factory=lambda: SystemTime())
    """Timestamp"""
    State: _e.BufferStateCmd = _e.BufferStateCmd.EMPTY
    """Buffer state"""
    Payload: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('PARAMETER_PAYLOAD_MAX')))
    """Payload defined by type per CMD definition. Processed by Appl. Layer Task."""
    PayloadLen: int = 0
    """Payload length"""
    PayLoadPtr: int = 0
    """Payload poiner position"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupAcyclicAcrEntryRspBuffer:
    """AxesGroupAcyclicAcrEntryRspBuffer"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: SystemTime = _field(default_factory=lambda: SystemTime())
    """Timestamp"""
    State: _e.BufferStateRsp = _e.BufferStateRsp.EMPTY
    Payload: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('RESPONSE_PAYLOAD_MAX')))
    """Payload defined by type per CMD definition. Processed by Appl. Layer Task."""
    PayloadLen: int = 0
    """Payload length"""
    PayLoadPtr: int = 0
    """Payload poiner"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupAcyclicExecutionOrderList:
    """AxesGroupAcyclicExecutionOrderList"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Command: _iec.IecArray[int] = _field(default_factory=lambda: _iec.IecArray(1, [0] * _iec.array_len(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'))))
    """Command"""
    Response: _iec.IecArray[int] = _field(default_factory=lambda: _iec.IecArray(1, [0] * _iec.array_len(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'))))
    """Response"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclic:
    """AxesGroupCyclic"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    PlcToRob: AxesGroupCyclicPlcToRob = _field(default_factory=lambda: AxesGroupCyclicPlcToRob())
    """Cyclic data from PLC to Robot"""
    RobToPlc: AxesGroupCyclicRobToPlc = _field(default_factory=lambda: AxesGroupCyclicRobToPlc())
    """Cyclic data from Robot to PLC"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicPlcToRob:
    """AxesGroupCyclicPlcToRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SRCIVersion: VersionStruct = _field(default_factory=lambda: VersionStruct())
    """
    Version of SRCI specification Bit 0-4 : Minor version = Features (0..31) Bit 5-7 : Major version
    = Breaking change (0..07)
    """
    FastStop: int = 0
    """Fast stop trigger"""
    LifeSign: int = 0
    """Connection alive signal"""
    TelegramLengthPlcToRob: int = 0
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction
    client to server
    """
    TelegramLengthRobToPlc: int = 0
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction
    server to client
    """
    AxesGroupID: int = 0
    """Control AxesGroupID Telegtam state control"""
    Control: _e.ControlHalfByte = _e.ControlHalfByte.NONE
    """Telegram state control"""
    Reserved: int = 0
    """Reserved for later versions"""
    TelegramNumberPlcToRob: int = 0
    """Configuration of the optional cyclic data. Direction client to server"""
    TelegramNumberRobToPlc: int = 0
    """Configuration of the optional cyclic data. Direction server to client"""
    ClientDate: int = 0
    """Date of the client in the format days since 1990.01.01"""
    ClientTime: int = 0
    """Time in the clients time zone in the format milliseconds since start of day"""
    ToolNo: int = 0
    """
    Index of tool of returned position • -1: Currently used tool on RC • 0: Flange (default) •
    1..254: Tool frames
    """
    FrameNo: int = 0
    """
    Index of frame of returned position • -1: Currently used frame on RC • 0: WCS (default) •
    1..254: User frames
    """


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicRobToPlc:
    """AxesGroupCyclicRobToPlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SRCIVersion: VersionStruct = _field(default_factory=lambda: VersionStruct())
    """
    Version of SRCI specification Bit 0-4 : Minor version = Features (0..31) Bit 5-7 : Major version
    = Breaking change (0..07)
    """
    LifeSign: int = 0
    """Connection alive signal"""
    Reserved: int = 0
    """Reserved byte"""
    TelegramState: _e.TelegramState = _e.TelegramState.UNDEFINED
    """Initialization and Telegram control state"""
    StatusRobotArm: RaStatusWord = _field(default_factory=lambda: RaStatusWord())
    """Combination of various RA related states."""
    Override: int = 0
    """Actual override in percentage encoding"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianPositionBase:
    """RobotCartesianPositionBase"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """TCP Position on the X-Axis"""
    Y: float = 0.0
    """TCP Position on the Y-Axis"""
    Z: float = 0.0
    """TCP Position on the Z-Axis"""
    Rx: float = 0.0
    """Rotation around the X-Axis (RX)"""
    Ry: float = 0.0
    """Rotation around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Rotation around the Z-Axis (RZ)"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianPositionShort(RobotCartesianPositionBase):
    """RobotCartesianPositionShort"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Config: ArmConfigParameter = _field(default_factory=lambda: ArmConfigParameter())
    """Configuration data of the robot (Config)"""
    TurnNumber: _s.TurnNumber = _field(default_factory=lambda: TurnNumber())
    """Turn number of the axes (TurnNumber)"""
    E1: float = 0.0
    """Position of first external axis"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataCartesianPosition(RobotCartesianPositionShort):
    """AxesGroupCyclicOptionalDataCartesianPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""
    CoordinateSystem: RobotCoordinateSystemParameters = _field(default_factory=lambda: RobotCoordinateSystemParameters())
    """corresponding coordinate systems"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianPositionExt:
    """RobotCartesianPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataCartesianPositionExt(RobotCartesianPositionExt):
    """AxesGroupCyclicOptionalDataCartesianPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotJointCurrentShort:
    """RobotJointCurrentShort"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Current of first joint of the robot"""
    J2: float = 0.0
    """Current of second joint of the robot"""
    J3: float = 0.0
    """Current of third joint of the robot"""
    J4: float = 0.0
    """Current of fourth joint of the robot"""
    J5: float = 0.0
    """Current of fifth joint of the robot"""
    J6: float = 0.0
    """Current of sixth joint of the robot"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataCurrent(RobotJointCurrentShort):
    """AxesGroupCyclicOptionalDataCurrent"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotJointCurrentExt:
    """RobotJointCurrentExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: float = 0.0
    """Current of first external joint of the robot"""
    E2: float = 0.0
    """Current of second external axis"""
    E3: float = 0.0
    """Current of third external axis"""
    E4: float = 0.0
    """Current of fourth external axis"""
    E5: float = 0.0
    """Current of fifth external axis"""
    E6: float = 0.0
    """Current of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataCurrentExt(RobotJointCurrentExt):
    """AxesGroupCyclicOptionalDataCurrentExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianForceShort:
    """RobotCartesianForceShort"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """Force on the X-Axis"""
    Y: float = 0.0
    """Force on the Y-Axis"""
    Z: float = 0.0
    """Force on the Z-Axis"""
    Rx: float = 0.0
    """Force around the X-Axis (RX)"""
    Ry: float = 0.0
    """Force around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Force around the Z-Axis (RZ)"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataForce(RobotCartesianForceShort):
    """AxesGroupCyclicOptionalDataForce"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianForceExt:
    """RobotCartesianForceExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: float = 0.0
    """Force on the first external axis"""
    E2: float = 0.0
    """Force of second external axis"""
    E3: float = 0.0
    """Force of third external axis"""
    E4: float = 0.0
    """Force of fourth external axis"""
    E5: float = 0.0
    """Force of fifth external axis"""
    E6: float = 0.0
    """Force of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataForceExt(RobotCartesianForceExt):
    """AxesGroupCyclicOptionalDataForceExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotJointPositionShort:
    """RobotJointPositionShort"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Position of first joint of the robot"""
    J2: float = 0.0
    """Position of second joint of the robot"""
    J3: float = 0.0
    """Position of third joint of the robot"""
    J4: float = 0.0
    """Position of fourth joint of the robot"""
    J5: float = 0.0
    """Position of fifth joint of the robot"""
    J6: float = 0.0
    """Position of sixth joint of the robot"""
    E1: float = 0.0
    """Position of first external axis"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataJointPosition(RobotJointPositionShort):
    """AxesGroupCyclicOptionalDataJointPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotJointPositionExt:
    """RobotJointPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataJointPositionExt(RobotJointPositionExt):
    """AxesGroupCyclicOptionalDataJointPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class RobotSubProgramData:
    """RobotSubProgramData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Data: list[int] = _field(default_factory=lambda: [0] * 26)
    """Sub program data"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataSubProgram(RobotSubProgramData):
    """AxesGroupCyclicOptionalDataSubProgram"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Active: bool = False
    """indicates that this optional parameter will be used"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalData:
    """AxesGroupCyclicOptionalData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    PlcToRob: AxesGroupCyclicOptionalDataPlcToRob = _field(default_factory=lambda: AxesGroupCyclicOptionalDataPlcToRob())
    """Optional cyclic data from PLC to Robot"""
    RobToPlc: AxesGroupCyclicOptionalDataRobToPlc = _field(default_factory=lambda: AxesGroupCyclicOptionalDataRobToPlc())
    """Optional cyclic data from Robot to PLC"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataPlcToRob:
    """AxesGroupCyclicOptionalDataPlcToRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SubProgramData: AxesGroupCyclicOptionalDataSubProgram = _field(default_factory=lambda: AxesGroupCyclicOptionalDataSubProgram())
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via the
    function “CallSubprogram”
    """
    CartesianPosition: AxesGroupCyclicOptionalDataCartesianPosition = _field(default_factory=lambda: AxesGroupCyclicOptionalDataCartesianPosition())
    """
    short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ), configuration bytes
    (Config, TurnNumber), position of first external axis (E1) and corresponding coordinate systems
    (ToolNo, FrameNo)
    """
    CartesianPositionExt: AxesGroupCyclicOptionalDataCartesianPositionExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataCartesianPositionExt())
    """
    the external axis values for an extended cartesian position (E2, E3, E4, E5, E6) When selected,
    Tool and Frame will automatically cyclically be sent from client to server.
    """
    JointPosition: AxesGroupCyclicOptionalDataJointPosition = _field(default_factory=lambda: AxesGroupCyclicOptionalDataJointPosition())
    """
    short axes position with joint values (J1, J2, J3,J4, J5, J6) and position of first external
    axis (E1)
    """
    JointPositionExt: AxesGroupCyclicOptionalDataJointPositionExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataJointPositionExt())
    """the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    Force: AxesGroupCyclicOptionalDataForce = _field(default_factory=lambda: AxesGroupCyclicOptionalDataForce())
    """force with the divided forces in the individual directions (X, Y, Z, RX, RY, RZ)"""
    ForceExt: AxesGroupCyclicOptionalDataForceExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataForceExt())
    """current force for the external axis (E1, E2, E3, E4, E5, E6)"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupCyclicOptionalDataRobToPlc:
    """AxesGroupCyclicOptionalDataRobToPlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SubProgramData: AxesGroupCyclicOptionalDataSubProgram = _field(default_factory=lambda: AxesGroupCyclicOptionalDataSubProgram())
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via the
    function “CallSubprogram”
    """
    CartesianPosition: AxesGroupCyclicOptionalDataCartesianPosition = _field(default_factory=lambda: AxesGroupCyclicOptionalDataCartesianPosition())
    """
    short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ), configuration bytes
    (Config, TurnNumber), position of first external axis (E1) and corresponding coordinate systems
    (ToolNo, FrameNo)
    """
    CartesianPositionExt: AxesGroupCyclicOptionalDataCartesianPositionExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataCartesianPositionExt())
    """
    the external axis values for an extended cartesian position (E2, E3, E4, E5, E6) When selected,
    Tool and Frame will automatically cyclically be sent from client to server.
    """
    JointPosition: AxesGroupCyclicOptionalDataJointPosition = _field(default_factory=lambda: AxesGroupCyclicOptionalDataJointPosition())
    """
    short axes position with joint values (J1, J2, J3,J4, J5, J6) and position of first external
    axis (E1)
    """
    JointPositionExt: AxesGroupCyclicOptionalDataJointPositionExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataJointPositionExt())
    """the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    Force: AxesGroupCyclicOptionalDataForce = _field(default_factory=lambda: AxesGroupCyclicOptionalDataForce())
    """force with the divided forces in the individual directions (X, Y, Z, RX, RY, RZ)"""
    ForceExt: AxesGroupCyclicOptionalDataForceExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataForceExt())
    """current force for the external axis (E1, E2, E3, E4, E5, E6)"""
    Current: AxesGroupCyclicOptionalDataCurrent = _field(default_factory=lambda: AxesGroupCyclicOptionalDataCurrent())
    """ctual axes current of individual axes (J1, J2, J3, J4, J5, J6)"""
    CurrentExt: AxesGroupCyclicOptionalDataCurrentExt = _field(default_factory=lambda: AxesGroupCyclicOptionalDataCurrentExt())
    """actual current for the external axis (E1, E2,E3, E4, E5, E6)"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupMessageLog:
    """AxesGroupMessageLog"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SystemLogEntries: int = 32
    """Amount of system log entries"""
    MessagesEntries: int = 100
    """Amount of message log entries"""
    LogLevel: _e.Severity = _e.Severity.DEACTIVATE
    """Logging level"""
    SystemLog: list[str] = _field(default_factory=lambda: [''] * _iec.array_len(0, _iec.Param('SYSTEM_LOG_MAX')))
    """System log"""
    Messages: list[AlarmMessage] = _field(default_factory=lambda: [AlarmMessage() for _ in range(_iec.array_len(0, _iec.Param('MESSAGE_LOG_MAX')))])
    """Message Log"""
    ExternalLogger: Any = None
    """Interface to an external logger"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterOptionalCyclic:
    """AxesGroupParameterOptionalCyclic"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    PlcToRob: AxesGroupParameterOptionalCyclicPlcToRob = _field(default_factory=lambda: AxesGroupParameterOptionalCyclicPlcToRob())
    """Configuration of optional cyclic data send to the Robot"""
    RobToPlc: AxesGroupParameterOptionalCyclicRobToPlc = _field(default_factory=lambda: AxesGroupParameterOptionalCyclicRobToPlc())
    """Configuration of optional cyclic data received from the Robot"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterOptionalCyclicPlcToRob:
    """AxesGroupParameterOptionalCyclicPlcToRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    UseCallSubprogram: bool = False
    """
    Bit 00: Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via
    the function “CallSubprogram”
    """
    UseCartesianPosition: bool = False
    """
    Bit 01: Send a short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1) and corresponding
    coordinate systems (ToolNo, FrameNo)
    """
    UseJointPosition: bool = False
    """
    Bit 02: Send a short axes position with joint values (J1, J2, J3, J4, J5, J6) and position of
    first external axis (E1)
    """
    UseForce: bool = False
    """
    Bit 03: Send the force with the divided forces in the individual directions (X, Y, Z, RX, RY,
    RZ)
    """
    Bit04: bool = False
    """Bit 04:"""
    Bit05: bool = False
    """Bit 05:"""
    Bit06: bool = False
    """Bit 06:"""
    Bit07: bool = False
    """Bit 07:"""
    UseTwoSequences: bool = False
    """
    Bit 08: Set to 1 to define two Sequences in one Telegram. If activated, 2 sequences also has to
    be activated in the ServerClient direction
    """
    UseCartesianPositionExt: bool = False
    """Bit 09: Send the external axis values for an extended cartesian position (E2, E3, E4, E5, E6)"""
    UseJointPositionExt: bool = False
    """Bit 10: Send the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    Bit11: bool = False
    """Bit 11:"""
    Bit12: bool = False
    """Bit 12:"""
    Bit13: bool = False
    """Bit 13:"""
    Bit14: bool = False
    """Bit 14:"""
    Bit15: bool = False
    """Bit 15:"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterOptionalCyclicRobToPlc:
    """AxesGroupParameterOptionalCyclicRobToPlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    UseCallSubprogram: bool = False
    """
    Bit 00: Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via
    the function “CallSubprogram”
    """
    UseCartesianPosition: bool = False
    """
    Bit 01: Send a short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1) and corresponding
    coordinate systems (ToolNo, FrameNo)
    """
    UseJointPosition: bool = False
    """
    Bit 02: Send a short axes position with joint values (J1, J2, J3, J4, J5, J6) and position of
    first external axis (E1)
    """
    UseForce: bool = False
    """
    Bit 03: Send the force with the divided forces in the individual directions (X, Y, Z, RX, RY,
    RZ)
    """
    UseCurrent: bool = False
    """Bit 04: Transmit actual axes current of individual axes (J1, J2, J3, J4, J5, J6)"""
    Bit05: bool = False
    """Bit 05:"""
    Bit06: bool = False
    """Bit 06:"""
    Bit07: bool = False
    """Bit 07:"""
    UseTwoSequences: bool = False
    """
    Bit 08: Set to 1 to define two Sequences in one Telegram. If activated, 2 sequences also has to
    be activated in the ServerClient direction
    """
    UseCartesianPositionExt: bool = False
    """Bit 09: Send the external axis values for an extended cartesian position (E2, E3, E4, E5, E6)"""
    UseJointPositionExt: bool = False
    """Bit 10: Send the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    UseForceExt: bool = False
    """Bit 11: Transmit the current force for the external axis (E1, E2, E3, E4, E5, E6)"""
    UseCurrentExt: bool = False
    """Bit 12: Transmit the actual current for the external axis (E1, E2, E3, E4, E5, E6)"""
    Bit13: bool = False
    """Bit 13:"""
    Bit14: bool = False
    """Bit 14:"""
    Bit15: bool = False
    """Bit 15:"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterPlc:
    """AxesGroupParameterPlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Parameter: AxesGroupParameterPlcParameter = _field(default_factory=lambda: AxesGroupParameterPlcParameter())
    """Parameter"""
    OptionalCyclic: AxesGroupParameterPlcOptionalCyclic = _field(default_factory=lambda: AxesGroupParameterPlcOptionalCyclic())
    """Optional cyclic"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterPlcOptionalCyclic:
    """AxesGroupParameterPlcOptionalCyclic"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    UseCallSubprogram: bool = False
    """
    Bit 00: Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via
    the function “CallSubprogram”
    """
    UseCartesianPosition: bool = False
    """
    Bit 01: Send a short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1) and corresponding
    coordinate systems (ToolNo, FrameNo)
    """
    UseJointPosition: bool = False
    """
    Bit 02: Send a short axes position with joint values (J1, J2, J3, J4, J5, J6) and position of
    first external axis (E1)
    """
    UseForce: bool = False
    """
    Bit 03: Send the force with the divided forces in the individual directions (X, Y, Z, RX, RY,
    RZ)
    """
    Bit04: bool = False
    """Bit 04:"""
    Bit05: bool = False
    """Bit 05:"""
    Bit06: bool = False
    """Bit 06:"""
    Bit07: bool = False
    """Bit 07:"""
    UseTwoSequences: bool = False
    """
    Bit 08: Set to 1 to define two Sequences in one Telegram. If activated, 2 sequences also has to
    be activated in the ServerClient direction
    """
    UseCartesianPositionExt: bool = False
    """Bit 09: Send the external axis values for an extended cartesian position (E2, E3, E4, E5, E6)"""
    UseJointPositionExt: bool = False
    """Bit 10: Send the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    Bit11: bool = False
    """Bit 11:"""
    Bit12: bool = False
    """Bit 12:"""
    Bit13: bool = False
    """Bit 13:"""
    Bit14: bool = False
    """Bit 14:"""
    Bit15: bool = False
    """Bit 15:"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterRob:
    """AxesGroupParameterRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Parameter: AxesGroupParameterRobParameter = _field(default_factory=lambda: AxesGroupParameterRobParameter())
    """Parameter"""
    OptionalCyclic: AxesGroupParameterRobOptionalCyclic = _field(default_factory=lambda: AxesGroupParameterRobOptionalCyclic())
    """Optional cyclic"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterRobOptionalCyclic:
    """AxesGroupParameterRobOptionalCyclic"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    UseCallSubprogram: bool = False
    """
    Bit 00: Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via
    the function “CallSubprogram”
    """
    UseCartesianPosition: bool = False
    """
    Bit 01: Send a short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1) and corresponding
    coordinate systems (ToolNo, FrameNo)
    """
    UseJointPosition: bool = False
    """
    Bit 02: Send a short axes position with joint values (J1, J2, J3, J4, J5, J6) and position of
    first external axis (E1)
    """
    UseForce: bool = False
    """
    Bit 03: Send the force with the divided forces in the individual directions (X, Y, Z, RX, RY,
    RZ)
    """
    UseCurrent: bool = False
    """Bit 04: Transmit actual axes current of individual axes (J1, J2, J3, J4, J5, J6)"""
    Bit05: bool = False
    """Bit 05:"""
    Bit06: bool = False
    """Bit 06:"""
    Bit07: bool = False
    """Bit 07:"""
    UseTwoSequences: bool = False
    """
    Bit 08: Set to 1 to define two Sequences in one Telegram. If activated, 2 sequences also has to
    be activated in the ServerClient direction
    """
    UseCartesianPositionExt: bool = False
    """Bit 09: Send the external axis values for an extended cartesian position (E2, E3, E4, E5, E6)"""
    UseJointPositionExt: bool = False
    """Bit 10: Send the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    UseForceExt: bool = False
    """Bit 11: Transmit the current force for the external axis (E1, E2, E3, E4, E5, E6)"""
    UseCurrentExt: bool = False
    """Bit 12: Transmit the actual current for the external axis (E1, E2, E3, E4, E5, E6)"""
    Bit13: bool = False
    """Bit 13:"""
    Bit14: bool = False
    """Bit 14:"""
    Bit15: bool = False
    """Bit 15:"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameterRobParameter:
    """AxesGroupParameterRobParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    RobotName: str = ''
    """User defined robot name"""
    LengthACR: int = 50
    """
    Returns a metric of how many CMDs it can receive and manage at the same time must be initialized
    with a value > 3, because during the interface initialization at least 3 commands are executed
    after ReadRobotData command the value is set to the correct ACR length wich is supported by the
    RC.
    """
    HighestToolIndex: int = 0
    """Highest index of available tools on the RC."""
    HighestFrameIndex: int = 0
    """Highest index of available frames on the RC."""
    HighestLoadIndex: int = 0
    """Highest index of available loads on the RC."""
    HighestWorkAreaIndex: int = 0
    """Highest index of available work areas on the RC."""
    DataInSync: _s.DataInSync = _field(default_factory=lambda: DataInSync())
    """Datas which are synchronized"""
    ChangeIndexTool: int = 0
    """Index of tool changed on RC"""
    ChangeIndexFrame: int = 0
    """Index of frame changed on RC"""
    ChangeIndexLoad: int = 0
    """Index of load changed on RC"""
    ChangeIndexWorkArea: int = 0
    """Index of work area changed on RC"""
    RAWorkingHours: int = 0
    """Working hours of an RA connected to the RC"""
    BrakeTestRequired: bool = False
    """Signals that a brake test is required in the defined monitoring time (see chapter 6.5.27)"""
    StepModeExactStopActive: bool = False
    """StepMode is active and set to ExactStop (see chapter 6.1.3)"""
    StepModeBlendingActive: bool = False
    """StepMode is active and set to Blending (see chapter 6.1.3)"""
    PathAccuracyMode: bool = False
    """PathAccuracyMode is active (see chapter 6.5.22)"""
    AvoidSingularity: bool = False
    """AvoidSingularity is active (see chapter 6.5.23)"""
    CollisionDetectionEnabled: bool = False
    """CollisionDetection is active (see chapter 6.5.35)"""
    AcceleratingSupported: bool = False
    """Cyclic dynamics status bit Accelerating is supported by RC (see chapter 5.5.3.2)"""
    DecceleratingSupported: bool = False
    """Cyclic dynamics status bit Decelerating is supported by RC (see chapter 5.5.3.2)"""
    ConstantVelocitySupported: bool = False
    """Cyclic dynamics status bit ConstantVelocity is supported by RC (see chapter 5.5.3.2)"""
    RCWorkingHours: int = 0
    """
    Total system hours of an RA connected to the RC. Must not be modifiable by the user. • 0:
    Invalid • >1: Total system hours
    """


@_dataclass(kw_only=True, slots=True)
class AxesGroupParameter:
    """AxesGroupParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Plc: AxesGroupParameterPlc = _field(default_factory=lambda: AxesGroupParameterPlc())
    """PLC specific data"""
    Rob: AxesGroupParameterRob = _field(default_factory=lambda: AxesGroupParameterRob())
    """RC data read by the function "ReadRobotData" (see chapter 6.1.2)"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupStateDataChanged:
    """AxesGroupStateDataChanged"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Tool: list[bool] = _field(default_factory=lambda: [False] * _iec.array_len(0, _iec.Param('TOOL_MAX', -1)))
    """indicates that tool data has changed"""
    Frame: list[bool] = _field(default_factory=lambda: [False] * _iec.array_len(0, _iec.Param('FRAME_MAX', -1)))
    """indicates that frame data has changed"""
    Load: list[bool] = _field(default_factory=lambda: [False] * _iec.array_len(0, _iec.Param('LOAD_MAX', -1)))
    """indicates that load data has changed"""
    WorkArea: list[bool] = _field(default_factory=lambda: [False] * _iec.array_len(0, _iec.Param('WORK_AREAS_MAX', -1)))
    """indicates that work area has changed"""
    DefaultDynamics: bool = False
    """indicates that default dynamic has changed"""
    ReferenceDynamics: bool = False
    """indicates that reference dynamic has changed"""
    SwLimits: bool = False
    """indicates that software limits has changed"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupStateSynchronizing:
    """AxesGroupStateSynchronizing"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Tool: bool = False
    """indicates that the tooldata are synchronized"""
    Frame: bool = False
    """indicates that the framedata are synchronized"""
    Load: bool = False
    """indicates that the loaddata are synchronized"""
    WorkAreas: bool = False
    """indicates that the work areas are synchronized"""
    ReferenceDynamics: bool = False
    """indicates that the reference-dynamics are synchronized"""
    DefaultDynamics: bool = False
    """indicates that the default-dynamics are synchronized"""
    SwLimits: bool = False
    """indicates that the software limits are synchronized"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupStateSyncState:
    """AxesGroupStateSyncState"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Tool: bool = False
    """Bit 00: Tool"""
    Frame: bool = False
    """Bit 01: Frame"""
    Load: bool = False
    """Bit 02: Load"""
    WorkArea: bool = False
    """Bit 03: WorkArea"""
    SwLimits: bool = False
    """Bit 04: SwLimits"""
    DefaultDynamics: bool = False
    """Bit 05: DefaultDynamics"""
    ReferenceDynamics: bool = False
    """Bit 06: ReferenceDynamics"""
    Bit07: bool = False
    """Bit 07:"""
    Bit08: bool = False
    """Bit 08:"""
    Bit09: bool = False
    """Bit 09:"""
    Bit10: bool = False
    """Bit 10:"""
    Bit11: bool = False
    """Bit 11:"""
    Bit12: bool = False
    """Bit 12:"""
    Bit13: bool = False
    """Bit 13:"""
    Bit14: bool = False
    """Bit 14:"""
    Bit15: bool = False
    """Bit 15:"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupStateSyncStateNo:
    """AxesGroupStateSyncStateNo"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Tool: int = 0
    """Ammount of unsynchronized tool data"""
    Frame: int = 0
    """Ammount of unsynchronized frame data"""
    Load: int = 0
    """Ammount of unsynchronized load data"""
    WorkArea: int = 0
    """Ammount of unsynchronized word areas"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupStateSyncStatePlc:
    """AxesGroupStateSyncStatePlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InSync: AxesGroupStateSyncState = _field(default_factory=lambda: AxesGroupStateSyncState())
    """Synchronisation state of the datasets"""
    UnSyncNo: AxesGroupStateSyncStateNo = _field(default_factory=lambda: AxesGroupStateSyncStateNo())
    """Number of the dataset which has been changed locally"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupStateSyncStateRob:
    """AxesGroupStateSyncStateRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    InSync: AxesGroupStateSyncState = _field(default_factory=lambda: AxesGroupStateSyncState())
    """Synchronisation state of the datasets"""
    UnSyncNo: AxesGroupStateSyncStateNo = _field(default_factory=lambda: AxesGroupStateSyncStateNo())
    """Number of the dataset which has been changed locally"""


@_dataclass(kw_only=True, slots=True)
class AxesGroupState:
    """AxesGroupState"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    FatalErrorClient: bool = False
    """Client reports a fatal error"""
    InvalidFrames: int = 0
    """Invalid frames counter"""
    Synchronized: bool = False
    """PLC and RC are synchronized"""
    Synchronizing: AxesGroupStateSynchronizing = _field(default_factory=lambda: AxesGroupStateSynchronizing())
    """Synchronizing is running"""
    AliveOk: bool = False
    """Data exchange is running ( Liftebit toggles )"""
    CMDsEnabled: bool = False
    """Bit that indicated that is possible to execute commands"""
    ConfigExchanged: bool = False
    """Configuration is exchanged"""
    UnifiedToolIndex: int = 0
    """Highest available tool index of RC and PLC in combination"""
    UnifiedFrameIndex: int = 0
    """Highest available frame index of RC and PLC in combination"""
    UnifiedLoadIndex: int = 0
    """Highest available load index of RC and PLC in combination"""
    UnifiedWorkAreaIndex: int = 0
    """Highest available workarea index of RC and PLC in combination"""
    DataEnableSync: _s.DataEnableSync = _field(default_factory=lambda: DataEnableSync())
    """Enable datas to synchronize"""
    DataChanged: AxesGroupStateDataChanged = _field(default_factory=lambda: AxesGroupStateDataChanged())
    """Flags that indicates which element has changed"""
    SyncStatePlc: AxesGroupStateSyncStatePlc = _field(default_factory=lambda: AxesGroupStateSyncStatePlc())
    """Synchronization state of the PLC"""
    SyncStateRc: AxesGroupStateSyncStateRob = _field(default_factory=lambda: AxesGroupStateSyncStateRob())
    """Synchronization state of the RC"""
    SystemTime: _s.SystemTime = _field(default_factory=lambda: SystemTime())
    """Current System Time"""
    RobotData: ReadRobotDataOutCmd = _field(default_factory=lambda: ReadRobotDataOutCmd())
    """Read Robot data"""
    StatusRobotArm: RaStatusWord = _field(default_factory=lambda: RaStatusWord())
    """Status of Robot Arm"""
    ConfigurationData: ExchangeConfigurationOutCmd = _field(default_factory=lambda: ExchangeConfigurationOutCmd())
    """Read configuration data"""
    ReadingCartesianPosition: bool = False
    """TRUE, while the CartesianPosition is returned cyclically"""
    ReadingCartesianPositionExt: bool = False
    """TRUE, while the ExtCartesianPosition is returned cyclically"""
    ReadingJointPosition: bool = False
    """TRUE, while the JointPosition is returned cyclically"""
    ReadingJointPositionExt: bool = False
    """TRUE, while the ExtJointPosition is returned cyclically"""
    Initialized: bool = False
    """Robot is initialized"""
    OnlineChange: bool = False
    """Online Change detected"""
    OnlineChange_R: Any = _field(default_factory=lambda: _iec.new_instance('R_TRIG'))
    """Rising edge for Online Change detected"""
    OnlineChange_F: Any = _field(default_factory=lambda: _iec.new_instance('F_TRIG'))
    """Falling edge for Online Change detected"""
    GroupReset: bool = False
    """GroupReset active"""
    GroupReset_R: Any = _field(default_factory=lambda: _iec.new_instance('R_TRIG'))
    """Rising edge for GroupReset"""
    GroupReset_F: Any = _field(default_factory=lambda: _iec.new_instance('F_TRIG'))
    """Falling edge for GroupReset"""
    SequenceCountSend: int = 0
    """Counter of sequences to send"""
    SequenceCountRecv: int = 0
    """Counter of sequences received"""
    FragmentCountSend: list[int] = _field(default_factory=lambda: [0] * 2)
    """Counter of fragments to send"""
    FragmentCountRecv: list[int] = _field(default_factory=lambda: [0] * 2)
    """Counter of fragments received"""
    CurrentSEQ: list[int] = _field(default_factory=lambda: [0] * 2)
    """Current Sequence ID"""
    CurrentACK: list[int] = _field(default_factory=lambda: [0] * 2)
    """Current acknowledge ID"""
    NewSEQ: list[bool] = _field(default_factory=lambda: [False] * 2)
    """Current Sequence ID has changed -> send new data"""
    LastACK: list[int] = _field(default_factory=lambda: [0] * 2)
    """Last received acknowledge ID"""


@_dataclass(kw_only=True, slots=True)
class AxesGroup:
    """AxesGroup"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Parameter: AxesGroupParameter = _field(default_factory=lambda: AxesGroupParameter())
    """Parameter"""
    State: AxesGroupState = _field(default_factory=lambda: AxesGroupState())
    """RI state information (see chapter 5.5.3)"""
    MessageLog: Any = _field(default_factory=lambda: _iec.new_instance('AxesGroupMessageLogFB'))
    """RC, RA, RI, and CMD warnings and errors (see chapter 5.5.11)"""
    Cyclic: AxesGroupCyclic = _field(default_factory=lambda: AxesGroupCyclic())
    """Cyclic data exchanged between server and client (see chapter 5.6.6.5)"""
    CyclicOptional: AxesGroupCyclicOptionalData = _field(default_factory=lambda: AxesGroupCyclicOptionalData())
    """Optional cyclic data exchanged between server and client (see chapter 5.6.6.2)"""
    Acyclic: AxesGroupAcyclic = _field(default_factory=lambda: AxesGroupAcyclic())
    """Execution order list and ACR entries (see chapter 5.6.4.2)"""
    SystemData: Any = _field(default_factory=lambda: _iec.new_instance('AxesGroupSystemDataFB'))
    """System data like ToolData, FrameData, LoadData etc."""


@_dataclass(kw_only=True, slots=True)
class AxisExternalUnit:
    """AxisExternalUnit"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: _e.AxisUnit = _e.AxisUnit.DEG
    """External Axis 1 used"""
    E2: _e.AxisUnit = _e.AxisUnit.DEG
    """External Axis 2 used"""
    E3: _e.AxisUnit = _e.AxisUnit.DEG
    """External Axis 3 used"""
    E4: _e.AxisUnit = _e.AxisUnit.DEG
    """External Axis 4 used"""
    E5: _e.AxisUnit = _e.AxisUnit.DEG
    """External Axis 5 used"""
    E6: _e.AxisUnit = _e.AxisUnit.DEG
    """External Axis 6 used"""


@_dataclass(kw_only=True, slots=True)
class AxisExternalUsed:
    """AxisExternalUsed"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: bool = False
    """External Axis 1 used"""
    E2: bool = False
    """External Axis 2 used"""
    E3: bool = False
    """External Axis 3 used"""
    E4: bool = False
    """External Axis 4 used"""
    E5: bool = False
    """External Axis 5 used"""
    E6: bool = False
    """External Axis 6 used"""


@_dataclass(kw_only=True, slots=True)
class AxisJointUnit:
    """AxisJointUnit"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: _e.AxisUnit = _e.AxisUnit.DEG
    """Joint Axis 1 unit"""
    J2: _e.AxisUnit = _e.AxisUnit.DEG
    """Joint Axis 2 unit"""
    J3: _e.AxisUnit = _e.AxisUnit.DEG
    """Joint Axis 3 unit"""
    J4: _e.AxisUnit = _e.AxisUnit.DEG
    """Joint Axis 4 unit"""
    J5: _e.AxisUnit = _e.AxisUnit.DEG
    """Joint Axis 5 unit"""
    J6: _e.AxisUnit = _e.AxisUnit.DEG
    """Joint Axis 6 unit"""


@_dataclass(kw_only=True, slots=True)
class AxisJointUsed:
    """AxisJointUsed"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: bool = False
    """Joint Axis 1 used"""
    J2: bool = False
    """Joint Axis 2 used"""
    J3: bool = False
    """Joint Axis 3 used"""
    J4: bool = False
    """Joint Axis 4 used"""
    J5: bool = False
    """Joint Axis 5 used"""
    J6: bool = False
    """Joint Axis 6 used"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianForce:
    """RobotCartesianForce"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """Force on the X-Axis"""
    Y: float = 0.0
    """Force on the Y-Axis"""
    Z: float = 0.0
    """Force on the Z-Axis"""
    Rx: float = 0.0
    """Force around the X-Axis (RX)"""
    Ry: float = 0.0
    """Force around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Force around the Z-Axis (RZ)"""
    E1: float = 0.0
    """Force of first external axis"""
    E2: float = 0.0
    """Force of second external axis"""
    E3: float = 0.0
    """Force of third external axis"""
    E4: float = 0.0
    """Force of fourth external axis"""
    E5: float = 0.0
    """Force of fifth external axis"""
    E6: float = 0.0
    """Force of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class RobotCartesianPosition(RobotCartesianPositionShort):
    """RobotCartesianPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class LogParameter:
    """LogParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CreateCmd: _e.Severity = _e.Severity.DEACTIVATE
    """Log level setting for creating commands"""
    UpdateCmd: _e.Severity = _e.Severity.DEACTIVATE
    """Log level setting for updating commands"""
    GenSeq: _e.Severity = _e.Severity.DEACTIVATE
    """Log level setting for generating sequence"""
    DecSeq: _e.Severity = _e.Severity.DEACTIVATE
    """Log level for ??? sequence"""


@_dataclass(kw_only=True, slots=True)
class RobotCoordinateSystemParameters:
    """RobotCoordinateSystemParameters"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Index of target tool • 0: Flange (default) • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of target frame • 0: WCS (default) • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class Frame:
    """Frame"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Available: bool = False
    """Frame is available"""
    Data: FrameData = _field(default_factory=lambda: FrameData())
    """Frame data"""


@_dataclass(kw_only=True, slots=True)
class FrameData:
    """FrameData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    ReferenceFrame: int = 0
    """Frame to which the shifting and rotation is relative M"""
    X: float = 0.0
    """Origin of the coordinate system relative to the BCS/WCS/UCS X value [mm]"""
    Y: float = 0.0
    """Origin of the coordinate system relative to the BCS/WCS/UCS Y value [mm]"""
    Z: float = 0.0
    """Origin of the coordinate system relative to the BCS/WCS/UCS Z value [mm]"""
    Rx: float = 0.0
    """Orientation of the coordinate system relative to the BCS/WCS/UCS Rx value [°]"""
    Ry: float = 0.0
    """Rx value [°]"""
    Rz: float = 0.0
    """Rx value [°]"""


@_dataclass(kw_only=True, slots=True)
class Load:
    """Load"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Available: bool = False
    """Load is available"""
    Data: LoadData = _field(default_factory=lambda: LoadData())
    """Load data"""


@_dataclass(kw_only=True, slots=True)
class LoadData:
    """LoadData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    X: float = 0.0
    """Position of the center of gravity relative to the flange. X value [mm]"""
    Y: float = 0.0
    """Position of the center of gravity relative to the flange. Y value [mm]"""
    Z: float = 0.0
    """Position of the center of gravity relative to the flange. Z value [mm]"""
    Rx: float = 0.0
    """Orientation of the principal inertia axes relative to the flange. O Rx value [°]"""
    Ry: float = 0.0
    """Ry value [°]"""
    Rz: float = 0.0
    """Rz value [°]"""
    Mass: float = 0.0
    """The mass of the tool and workpiece being gripped. [kg]"""
    Ix: float = 0.0
    """The moment of inertia of the load around the resulting inertia X-Axis [kg/m²]"""
    Iy: float = 0.0
    """The moment of inertia of the load around the resulting inertia y-axis [kg/m²]"""
    Iz: float = 0.0
    """The moment of inertia of the load around the resulting inertia z-axis [kg/m²]"""


@_dataclass(kw_only=True, slots=True)
class SplineData:
    """SplineData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Position: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """Absolute target coordinates in the selected coordinate system (see ToolNo and FrameNo)."""
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity. • <0% : Use default velocity (default) • 0% : Use
    internal minimal velocity • 100% : Use maximal reference velocity • See chapter 5.5.7 Robot
    dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration. • <0% : Use default acceleration
    (default) • 0% : Use internal minimal acceleration • 100% : Use maximal reference acceleration •
    See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration. • <0% : Use default deceleration
    (default) • 0% : Use internal minimal deceleration • 100% : Use maximal reference deceleration •
    See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk. <0% o Use default jerk (default) 0% o Use internal
    minimal jerk 100% o Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """
    ToolNo: int = 0
    """Index of tool 0: Flange (default) 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame 0: WCS (default) 1..254: User frames"""
    MoveTime: int = 0
    """
    [ms] Parameter is used if it is greater than 0 (default): Parameter defines the time for the
    movement to reach the target position Velocity input can be ignored Acceleration, Deceleration
    and jerk will be ignored Define two consecutive points with identical positions and specified
    Time to realize waiting time on spline. Error is sent by the RC, if the time cannot be kept.
    """


@_dataclass(kw_only=True, slots=True)
class Tool:
    """Tool"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Available: bool = False
    """Tool is available"""
    Data: ToolData = _field(default_factory=lambda: ToolData())
    """Tool data"""


@_dataclass(kw_only=True, slots=True)
class ToolData:
    """ToolData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    ID: int = 0
    """Identification of physical tool Default: 0"""
    ExternalTCP: bool = False
    """True: Tool fixed False: Tool on flange"""
    X: float = 0.0
    """Origin of the tool coordinate system relative to the flange coordinate system. X value [mm]"""
    Y: float = 0.0
    """Origin of the tool coordinate system relative to the flange coordinate system. Y value [mm]"""
    Z: float = 0.0
    """Origin of the tool coordinate system relative to the flange coordinate system. Z value [mm]"""
    Rx: float = 0.0
    """Orientation of the tool coordinate system relative to the flange coordinate system RX value[°]"""
    Ry: float = 0.0
    """Orientation of the tool coordinate system relative to the flange coordinate system RX value[°]"""
    Rz: float = 0.0
    """Orientation of the tool coordinate system relative to the flange coordinate system RX value[°]"""
    LoadNo: int = 0
    """Index of the payload Information of tool and workpiece weight, center of gravity and inertia"""


@_dataclass(kw_only=True, slots=True)
class UserData:
    """UserData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EnableSync: DataEnableSync = _field(default_factory=lambda: DataEnableSync())
    """state of the synchronizationrelated comparison mechanism"""
    ActivateTwoSequences: bool = False
    """TRUE if two sequences in one Telegram are active"""
    SynchronizationModes: _s.SynchronizationModes = _field(default_factory=lambda: SynchronizationModes())
    """Synchronisation modes"""
    DelayTime: int = 0
    """
    Defines waiting time [ms] of RC between receiving a first move command when motion queue is
    empty and starting the first movement. See also chapter 5.6.8.
    """
    WaitForNrOfCmd: int = 0
    """Define number of points required to calculate the blending. See also chapter 5.6.8"""
    WaitAtBlendingZone: bool = False
    """
    Defines blending behavior for single move commands • 0 (default): Move to end position : Robot
    moves exactly the target position independently of the selected "BlendingMode" • 1: Wait at
    blending parameter : Robot stops its movement when the specified blending parameter is reached
    """
    AllowSecSeqWhileSubprogram: bool = False
    """
    Allow a sequence switch from primary to secondary while a subprogram called via CallSubprogram
    (6.5.18) in the sequence is in progress
    """
    AllowDynamicBlending: bool = False
    """
    Allows blending when CallSubprogram is called in sequence and removed afterwards. For more
    information see chapter 6.5.21. • 0 (default): Dynamic blending is prevented • 1: Dynamic
    blending is allowed
    """
    LifeSignTimeOut: int = 0
    """
    Maximum allowed time [ms] between incrementation of LifeSign before communication error. • <10
    ms: Invalid • 50 ms: default See also chapter 5.6.6.2.
    """
    SyncReaction: int = 0
    """
    Specifies system reaction in case inconsistency of synchronization data is detected according to
    Table 6-81. For more information refer to chapter 5.6.7.2
    """
    SyncDelay: int = 0
    """
    Defines a delay time [ms] between detecting an inconsistency of configuration data between
    server and client an executing the defined SyncReaction. Always positive. • Default: 0 ms
    """
    LogLevel: _e.Severity = _e.Severity.DEACTIVATE
    """Defines up to which level of severity messages will be logged in the RC's server log"""
    MessageLevel: _e.MessageLevel = _e.MessageLevel.DEBUG
    """Defines up to which level of severity messages will be transmitted to the PLC’s message buffer"""
    PLCManufacturedID: int = 0
    """Manufactured ID"""
    PLCOrderID: str = ''
    """Order ID"""
    PLCSerialNumber: str = ''
    """Serial Number"""
    PLCFirmwareVersion: str = ''
    """Firmware Version"""
    PLCInterfaceVersion: str = ''
    """Client Interface Version"""
    PLCLibraryVersion: VersionStruct = _field(default_factory=lambda: VersionStruct())
    """Version of client implementation in format (X.X.X)"""
    RCManufacturer: str = ''
    """RC manufacturer name"""
    RCOrderID: str = ''
    """RC part number"""
    RCSerialNumber: str = ''
    """RC serial number"""
    RASerialNumber: str = ''
    """RA serial number"""
    RCFirmwareVersion: str = ''
    """Robot firmware version in manufacturer-specific format"""
    RCInterpreterVersion: VersionStruct = _field(default_factory=lambda: VersionStruct())
    """Version of server implementation in format (X.X.X)"""
    RCSRCIVersion: VersionStruct = _field(default_factory=lambda: VersionStruct())
    """Version of SRCI specification on which server implementation is based in format (X.X.X)"""
    AxisJointUsed: _s.AxisJointUsed = _field(default_factory=lambda: AxisJointUsed())
    """TRUE = Axis used in Robot, FALSE = Axis NOT used. See Table 6-13 for bit assignment."""
    AxisExternalUsed: _s.AxisExternalUsed = _field(default_factory=lambda: AxisExternalUsed())
    """TRUE = Axis used by Robot, FALSE = Axis NOT used. See Table 6-13 for bit assignment."""
    AxisJointUnit: _s.AxisJointUnit = _field(default_factory=lambda: AxisJointUnit())
    """TRUE = mm, FALSE = °. See Table 6-13 for bit assignment."""
    AxisExternalUnit: _s.AxisExternalUnit = _field(default_factory=lambda: AxisExternalUnit())
    """TRUE = mm, FALSE = °. See Table 6-13 for bit assignment."""
    Initialized: bool = False
    """Interface is initialized and ready to process commands."""
    Synchronized: bool = False
    """All synchronization-related configuration data between client and server is synchronized."""
    ToolDataSynchronizing: bool = False
    """ToolData synchronization is activated."""
    FrameDataSynchronizing: bool = False
    """FrameData synchronization is activated."""
    LoadDataSynchronizing: bool = False
    """LoadData synchronization is activated."""
    WorkAreaDataSynchronizing: bool = False
    """WorkAreaData synchronization is activated."""
    SWLimitsSynchronizing: bool = False
    """SWLimits synchronization is activated."""
    DefaultDynamicsSynchronizing: bool = False
    """DefaultDynamics synchronization is activated."""
    ReferenceDynamicsSynchronizing: bool = False
    """ReferenceDynamics synchronization is activated."""
    IsMoving: bool = False
    """
    TRUE, when robot’s axes values change due to physical movement of axes. Can only be TRUE in
    sequence state "Executing". Default: FALSE
    """
    PrimarySequencePaused: bool = False
    """
    TRUE, when move commands buffered by the primary sequence are currently not processed. Default:
    FALSE
    """
    InPrimaryPos: bool = False
    """
    TRUE, when robot is moving in the primary sequence. FALSE, when robot leaves its position by
    other means than move commands in the primary sequence. Default: FALSE
    """
    SecondarySequenceActive: bool = False
    """TRUE, when secondary sequence is active. Default: FALSE"""
    ErrorPending: bool = False
    """Shows that an error acknowledgement by the client is necessary. Default: FALSE"""
    RestartInProgress: bool = False
    """TRUE, when RC is restarting. Default: FALSE"""
    BrakeTestRequired: bool = False
    """Signals that a brake test is required in the defined monitoring time (see chapter 6.5.27)."""
    Enabled: bool = False
    """RA power state. Default: FALSE"""
    Idle: bool = False
    """TRUE, while RA sequence states returns Idle. Default: FALSE"""
    Executing: bool = False
    """TRUE, while RA sequence states returns Executing. Default: FALSE"""
    Interrupted: bool = False
    """TRUE, while RA sequence states returns Interrupted. Default: FALSE"""
    IsBlending: bool = False
    """
    TRUE, when robot is currently blending between to move commands. Can only be TRUE in sequence
    state "Executing". Default: FALSE
    """
    OperationMode: _e.OperationMode = _e.OperationMode.T1_LOCAL
    """Operation Mode (see chapter 5.5.1)"""
    PathAccuracyMode: bool = False
    """PathAccuracyMode is active (see chapter 6.5.22)"""
    AvoidSingularity: bool = False
    """AvoidSingularity is active (see chapter 6.5.23)"""
    CollisionDetectionEnabled: bool = False
    """TRUE, while CollisionDetection is enabled (see chapter 6.5.35) Default: FALSE"""
    CollisionDetected: bool = False
    """
    TRUE, when a collision was detected while CollisionDetection is enabled (see chapter 6.5.35)
    Default: FALSE
    """
    RestartRequested: bool = False
    """
    TRUE, when the RC requests a restart of the RC induced through the functions
    "WriteRobotSWLimits" (chapter 6.2.16) or "WriteSystemVariable" (chapter 6.5.8) Default: FALSE
    """
    ActualOverride: float = 0.0
    """Actual override"""
    StepModeExactStopActive: bool = False
    """StepMode is active and set to ExactStop (see chapter 6.1.3)"""
    StepModeBlendingActive: bool = False
    """StepMode is active and set to Blending (see chapter 6.1.3)"""
    AcceleratingSupported: bool = False
    """Cyclic dynamics status bit Accelerating is supported by RC (see chapter 5.5.3.2)"""
    Accelerating: bool = False
    """TRUE, when the robot is currently accelerating Default: FALSE"""
    DeceleratingSupported: bool = False
    """Cyclic dynamics status bit Decelerating is supported by RC (see chapter 5.5.3.2)"""
    Decelerating: bool = False
    """TRUE, when the robot is currently decelerating Default: FALSE"""
    ConstantVelocitySupported: bool = False
    """Cyclic dynamics status bit ConstantVelocity is supported by RC (see chapter 5.5.3.2)"""
    ConstantVelocity: bool = False
    """TRUE, while the robot velocity is constant Default: FALSE"""
    ReadingCartesianPosition: bool = False
    """TRUE, while the CartesianPosition is returned cyclically"""
    ReadingExtCartesianPosition: bool = False
    """TRUE, while the ExtCartesianPosition is returned cyclically"""
    ReadingJointPosition: bool = False
    """TRUE, while the JointPosition is returned cyclically"""
    ReadingExtJointPosition: bool = False
    """TRUE, while the ExtJointPosition is returned cyclically"""
    CartesianPosition: RobotCartesianPositionShort = _field(default_factory=lambda: RobotCartesianPositionShort())
    """
    Cyclically returned, absolute coordinates of current position in selected coordinate systems
    (see input parameters ToolNo and FrameNo of function ReadActualPositionCyclic 6.1.6)
    """
    ExtCartesianPosition: RobotCartesianPositionExt = _field(default_factory=lambda: RobotCartesianPositionExt())
    """
    Cyclically returned, absolute cartesian position of the external axes of the robot in selected
    coordinate systems (see input parameters ToolNo and FrameNo of function ReadActualPositionCyclic
    6.1.6)
    """
    JointPosition: RobotJointPositionShort = _field(default_factory=lambda: RobotJointPositionShort())
    """Cyclically returned, absolute position of the robot in Joint position"""
    ExtJointPosition: RobotJointPositionExt = _field(default_factory=lambda: RobotJointPositionExt())
    """Cyclically returned, absolute joint position of the external axes of the robot"""
    RCSupportedFunctions: _s.RCSupportedFunctions = _field(default_factory=lambda: RCSupportedFunctions())
    """
    TRUE: Function is supported by RC FALSE: Function is not supported by RC See Table 6-14 for bit
    assignment.
    """


@_dataclass(kw_only=True, slots=True)
class RobotWorkArea:
    """RobotWorkArea"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Available: bool = False
    """Workarea is available"""
    Data: RobotWorkAreaData = _field(default_factory=lambda: RobotWorkAreaData())
    """Workarea data"""


@_dataclass(kw_only=True, slots=True)
class RobotWorkAreaData:
    """RobotWorkAreaData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    AreaType: _e.AreaType = _e.AreaType.AXES
    """Defines type of work area"""
    AreaMode: bool = False
    """
    Defines violation condition • FALSE (default) : Robot must not leave defined area • TRUE : Robot
    must not enter defined area
    """
    ReactionMode: _e.WorkAreaReactionMode = _e.WorkAreaReactionMode.NO_REACTION
    """Defines RC’s and robot’s behavior when robot violates work area"""
    ActiveModification: bool = False
    """
    Specifies whether an active work area can be edited by function WriteWorkArea TRUE :
    Modification of active work area possible FALSE (default) : Modification of active work areas
    not possible
    """
    DefinitionMode: _e.DefinitionMode = _e.DefinitionMode.Center
    """Relates to AreaType Box, Cylinder and Sphere."""
    FrameNo: int = 0
    """
    Relates to AreaType Box, Cylinder and Sphere. Index of reference frame • 0: WCS (default) •
    1..254: User frames
    """
    ZeroPointX: float = 0.0
    """
    Relates to AreaType Box, Cylinder and Sphere. X-value of reference point in specified frame -
    Default: 0
    """
    ZeroPointY: float = 0.0
    """
    Relates to AreaType Box, Cylinder and Sphere. Y-value of reference point in specified frame -
    Default: 0
    """
    ZeroPointZ: float = 0.0
    """
    Relates to AreaType Box, Cylinder and Sphere. Z-value of reference point in specified frame -
    Default: 0
    """
    X: RobotWorkAreaDataLimitCartesian = _field(default_factory=lambda: RobotWorkAreaDataLimitCartesian())
    """Limit for cartesian X"""
    Y: RobotWorkAreaDataLimitCartesian = _field(default_factory=lambda: RobotWorkAreaDataLimitCartesian())
    """Limit for cartesian Y"""
    Z: RobotWorkAreaDataLimitCartesian = _field(default_factory=lambda: RobotWorkAreaDataLimitCartesian())
    """Limit for cartesian Z"""
    Radius: float = 0.0
    """Relates to AreaType Sphere. Radius of cylinder or sphere - Default 0"""
    J1Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint J1"""
    J2Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint J2"""
    J3Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint J3"""
    J4Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint J4"""
    J5Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint J5"""
    J6Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint J6"""
    E1Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint E1"""
    E2Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint E2"""
    E3Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint E3"""
    E4Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint E4"""
    E5Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint E5"""
    E6Limit: RobotWorkAreaDataLimitJoint = _field(default_factory=lambda: RobotWorkAreaDataLimitJoint())
    """Limits for Joint E6"""


@_dataclass(kw_only=True, slots=True)
class RobotWorkAreaDataLimitCartesian:
    """RobotWorkAreaDataLimitCartesian"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LowerLimit: float = 0.0
    """Relates to AreaType Box, Cylinder and Sphere. Distance in negative Direction - Default 0"""
    UpperLimit: float = 0.0
    """Relates to AreaType Box, Cylinder and Sphere. Distance in positive Direction - Default 0"""


@_dataclass(kw_only=True, slots=True)
class RobotWorkAreaDataLimitJoint:
    """RobotWorkAreaDataLimitJoint"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LowerLimit: float = 0.0
    """
    Relates to AreaType Axes. Negative work area limit for Joint • 0 (default) : No work area
    restriction of joint if lower and upper limit are set to 0 • 16#FFFF_FFFF: No lower work area
    restrictions for Joint
    """
    UpperLimit: float = 0.0
    """
    Relates to AreaType Axes. positive work area limit for Joint • 0 (default) : No work area
    restriction of joint if lower and upper limit of are set to 0 • 16#FFFF_FFFF: No lower work area
    restrictions for Joint
    """


@_dataclass(kw_only=True, slots=True)
class CyclicStateData:
    """CyclicStateData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    StatusWord: RaStatusWord = _field(default_factory=lambda: RaStatusWord())
    """Combination of various RA related states."""
    Override: int = 0
    """
    Actual override in percentage multiplied by 100 (see chapter 5.6.2 for more information about
    the percentage encoding)
    """


@_dataclass(kw_only=True, slots=True)
class IEC_TIMESTAMP:
    """IEC_TIMESTAMP"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    IEC_DATE: int = 0
    """Date"""
    IEC_TIME: int = 0
    """Time"""


@_dataclass(kw_only=True, slots=True)
class SystemTime:
    """SystemTime"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SystemDate: int = 0
    """Date of the system"""
    SystemTime: int = 0
    """Time of the system"""


@_dataclass(kw_only=True, slots=True)
class DefaultDynamics:
    """DefaultDynamics"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    VelocityRate: float = 0.0
    """
    Maximum velocity for the axes. Range [%]: • <0% : Use default velocity given by the user • 0% :
    Use internal minimal velocity • 100% : Use the entire reference velocity, given by the user
    """
    AccelerationRate: float = 0.0
    """
    Maximum acceleration. Range [%]: • <0% : Use default acceleration given by the user • 0% : Use
    internal minimal acceleration • 100% : Use the entire reference acceleration, given by the user
    """
    DecelerationRate: float = 0.0
    """
    Maximum deceleration. Range [%] : • <0% : Use default deceleration given by the user • 0% : Use
    internal minimal deceleration • 100% : Use the entire reference deceleration, given by the user
    """
    JerkRate: float = 0.0
    """
    Maximum jerk Range [%] : • <0% : Use default jerk given by the user • 0% : Use internal minimal
    jerk • 100% : Use the entire reference jerk, given by the user (Trapezoidal if possible)
    """


@_dataclass(kw_only=True, slots=True)
class ReferenceDynamics:
    """ReferenceDynamics"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    VelocityReference: float = 0.0
    """
    Path velocity [mm/s](tangent) at 100% • <0: (default) - Do not change values • ≥0: Change values
    according to input value
    """
    AccelerationReference: float = 0.0
    """
    Path acceleration [mm/s2] at 100% • <0: (default) - Do not change values • ≥0: Change values
    according to input value
    """
    DecelerationReference: float = 0.0
    """
    Path deceleration [mm/s2] at 100% • <0: (default) - Do not change values • ≥0: Change values
    according to input value
    """
    JerkReference: float = 0.0
    """
    Jerk [mm/s3] at 100% • <0: (default) - Do not change values • ≥0: Change values according to
    input value
    """


@_dataclass(kw_only=True, slots=True)
class RobotDynamics:
    """RobotDynamics"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    VelocityRate: float = 0.0
    """
    TCP velocity in % of nominal velocity • <0% (default) o Use default velocity • 0% o Use internal
    minimal velocity • 100% o Use maximal reference velocity See chapter 5.5.7 Robot dynamics
    """
    AccelerationRate: float = 0.0
    """
    Acceleration for movement in % of nominal acceleration • <0% (default) o Use default
    acceleration • 0% o Use internal minimal acceleration • 100%: o Use maximal reference
    acceleration See chapter 5.5.7 Robot dynamics
    """
    DecelerationRate: float = 0.0
    """
    Deceleration for movement in % of nominal deceleration • <0% (default) o Use default
    deceleration • 0% o Use internal minimal deceleration • 100% o Use maximal reference
    deceleration See chapter 5.5.7 Robot dynamics
    """
    JerkRate: float = 0.0
    """
    Jerk of the movement in % of nominal jerk • <0% (default) o Use default jerk • 0% o Use internal
    minimal jerk • 100% o Use maximal reference jerk See chapter 5.5.7 Robot dynamics
    """


@_dataclass(kw_only=True, slots=True)
class RobotJointCurrent:
    """RobotJointCurrent"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Current of first joint of the robot"""
    J2: float = 0.0
    """Current of second joint of the robot"""
    J3: float = 0.0
    """Current of third joint of the robot"""
    J4: float = 0.0
    """Current of fourth joint of the robot"""
    J5: float = 0.0
    """Current of fifth joint of the robot"""
    J6: float = 0.0
    """Current of sixth joint of the robot"""
    E1: float = 0.0
    """Current of first external joint of the robot"""
    E2: float = 0.0
    """Current of second external axis"""
    E3: float = 0.0
    """Current of third external axis"""
    E4: float = 0.0
    """Current of fourth external axis"""
    E5: float = 0.0
    """Current of fifth external axis"""
    E6: float = 0.0
    """Current of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class RobotJointPosition:
    """RobotJointPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Position [°] of first joint of the robot"""
    J2: float = 0.0
    """Position [°] of second joint of the robot"""
    J3: float = 0.0
    """Position [°] of third joint of the robot"""
    J4: float = 0.0
    """Position [°] of fourth joint of the robot"""
    J5: float = 0.0
    """Position [°] of fifth joint of the robot"""
    J6: float = 0.0
    """Position [°] of sixth joint of the robot"""
    E1: float = 0.0
    """Position [°] of first external axis"""
    E2: float = 0.0
    """Position [°] of second external axis"""
    E3: float = 0.0
    """Position [°] of third external axis"""
    E4: float = 0.0
    """Position [°] of fourth external axis"""
    E5: float = 0.0
    """Position [°] of fifth external axis"""
    E6: float = 0.0
    """Position [°] of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class AlarmMessage:
    """AlarmMessage"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: SystemTime = _field(default_factory=lambda: SystemTime())
    """Timestamp"""
    MessageType: _e.MessageType = _e.MessageType.RI
    """Type of message according to Table 5-46:"""
    Severity: _e.Severity = _e.Severity.DEACTIVATE
    """Severity of message according to Table 5-47: Debug, Info, Warning, Error, Fatal error"""
    MessageCode: int = 0
    """Code of messages"""
    MessageText: str = ''
    """Static text of message"""


@_dataclass(kw_only=True, slots=True)
class ArmConfigParameter:
    """ArmConfigParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Shoulder: _e.ArmConfigShoulder = _e.ArmConfigShoulder.USE_CONFIG
    """Configuration of shoulder"""
    Elbow: _e.ArmConfigElbow = _e.ArmConfigElbow.USE_CONFIG
    """Configuration of elbow"""
    Wrist: _e.ArmConfigWrist = _e.ArmConfigWrist.USE_CONFIG
    """Configuration of wrist"""


@_dataclass(kw_only=True, slots=True)
class AuxOffset:
    """AuxOffset"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """Offset in X-Direction"""
    Y: float = 0.0
    """Offset in Y-direction"""
    Z: float = 0.0
    """Offset in Z-direction"""
    Rx: float = 0.0
    """Offset in Rx-Direction"""
    Ry: float = 0.0
    """Offset in Ry-direction"""
    Rz: float = 0.0
    """Offset in Rz-direction"""


@_dataclass(kw_only=True, slots=True)
class CoordinateSystem:
    """CoordinateSystem"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Tool index • 0: Flange • 1..254: Tool frames"""
    FrameNo: int = 0
    """Frame index • 0: WCS • 1..254: User frames"""


@_dataclass(kw_only=True, slots=True)
class DataEnableSync:
    """DataEnableSync"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    EnableSyncTool: bool = True
    """Set TRUE (default), to activate the synchronizationrelated comparison mechanism for tool data"""
    EnableSyncFrame: bool = True
    """Set TRUE (default), to activate the synchronizationrelated comparison mechanism for frame data"""
    EnableSyncLoad: bool = True
    """Set TRUE (default), to activate the synchronizationrelated comparison mechanism for load data"""
    EnableSyncWorkArea: bool = True
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for work area
    data
    """
    EnableSyncSWLimits: bool = True
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for software
    limits
    """
    EnableSyncDefaultDynamics: bool = True
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for default
    dynamics
    """
    EnableSyncReferenceDynamics: bool = True
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for reference
    dynamics
    """


@_dataclass(kw_only=True, slots=True)
class DataInSync:
    """DataInSync"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolsInSync: bool = False
    """TRUE, if no tool has been modified"""
    FramesInSync: bool = False
    """TRUE, if no frame has been modified"""
    LoadsInSync: bool = False
    """TRUE, if no load has been modified"""
    WorkAreasInSync: bool = False
    """TRUE, if no work area has been modified"""
    SoftwareLimitsInSync: bool = False
    """TRUE, if no software limit has been modified"""
    DefaultDynamicsInSync: bool = False
    """TRUE, if no default dynamic parameter has been modified"""
    ReferenceDynamicsInSync: bool = False
    """TRUE, if no reference dynamic parameter has been modified"""


@_dataclass(kw_only=True, slots=True)
class DHParameter:
    """DHParameter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Alpha: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """DH parameter α for each joint - 0 If not supported"""
    A: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """DH parameters A for each joint - 0 If not supported"""
    D: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """DH parameters D for each joint - 0 If not supported"""
    Theta: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """DH parameters Theta for each joint - 0 If not supported"""
    PositiveJointDirection: list[bool] = _field(default_factory=lambda: [False] * 7)
    """
    Positive joint direction of each joint. TRUE when positive joint direction points to the right.
    See also Figure 6-16.
    """
    JointZeroPosition: list[float] = _field(default_factory=lambda: [0.0] * 7)
    """Offset of zero position of joint to zero position suggested by Figure 6-17."""


@_dataclass(kw_only=True, slots=True)
class ExecutionModeAllowed:
    """ExecutionModeAllowed"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    PRIMARY_SEQ: bool = False
    PRIMARY_SEQ_ABORT: bool = False
    SECONDARY_SEQ: bool = False
    SECONDARY_SEQ_ABORT: bool = False
    PAR: bool = True
    PAR_TASK: bool = False
    PAR_TRIGGER: bool = False
    PAR_TRIGGER_TASK: bool = False


@_dataclass(kw_only=True, slots=True)
class ExternalAxesFlags:
    """ExternalAxesFlags"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Bit00: bool = False
    """Bit 00 : Not used"""
    AxisE1: bool = False
    """Bit 01 : External axis E1 - property depends of usage"""
    AxisE2: bool = False
    """Bit 02 : External axis E2 - property depends of usage"""
    AxisE3: bool = False
    """Bit 03 : External axis E3 - property depends of usage"""
    AxisE4: bool = False
    """Bit 04 : External axis E4 - property depends of usage"""
    AxisE5: bool = False
    """Bit 05 : External axis E5 - property depends of usage"""
    AxisE6: bool = False
    """Bit 06 : External axis E6 - property depends of usage"""
    Bit07: bool = False
    """Bit 00 : Not used"""


@_dataclass(kw_only=True, slots=True)
class ForceStatus:
    """ForceStatus"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ForceControlEnabled: bool = False
    """TRUE, while a "ForceControl" function is enabled"""
    ForceLimitEnabled: bool = False
    """TRUE, while a "ForceLimit" function is enabled"""
    ApplyingForce: bool = False
    """TRUE, while robot is adjusting its movement to apply specified force"""
    MaxDeviationReached: bool = False
    """TRUE, while maximum deviation according to input parameter "MaxDeviation" is reached"""
    SpecifiedForceTorqueReached: bool = False
    """TRUE, while currently applied force/torque is identical to specified force/torque"""
    SpecifiedForceLimitReached: bool = False
    """TRUE, while currently detected force is identical to specified force limit"""
    Bit06: bool = False
    """Bit 06 Reserve"""
    Bit07: bool = False
    """Bit 07 Reserve"""


@_dataclass(kw_only=True, slots=True)
class FragmentAction:
    """FragmentAction"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Complete: bool = False
    """Bit 00 : Command Message is completely received – Flag to trigger processing of the payload"""
    Reset: bool = False
    """
    Bit 01 :(only client->server): The first message fragment of a new CMD resets (set all ACR
    values of this CMD ID to 0) the ACR entry
    """
    Clear: bool = False
    """Bit 02: Clears the receiving buffer by setting all of its Bytes to 0."""
    BIT03: bool = False
    """Bit 03"""
    BIT04: bool = False
    """Bit 04"""
    BIT05: bool = False
    """Bit 05"""
    BIT06: bool = False
    """Bit 06"""
    BIT07: bool = False
    """Bit 07"""


@_dataclass(kw_only=True, slots=True)
class JogControl:
    """JogControl"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X_J1_Pos: bool = False
    """
    Mode Frame : Movement in positive direction X of selected frame Mode Tool : Movement in positive
    direction X of selected tool Mode Axes : Movement in positive direction joint 1
    """
    X_J1_Neg: bool = False
    """
    Mode Frame : Movement in negative direction X of selected frame Mode Tool : Movement in negative
    direction X of selected tool Mode Axes : Movement in negative direction joint 1
    """
    Y_J2_Pos: bool = False
    """
    Mode Frame : Movement in positive direction Y of selected frame Mode Tool : Movement in positive
    direction Y of selected tool Mode Axes : Movement in positive direction joint 2
    """
    Y_J2_Neg: bool = False
    """
    Mode Frame : Movement in negative direction Y of selected frame Mode Tool : Movement in negative
    direction Y of selected tool Mode Axes : Movement in negative direction joint 2
    """
    Z_J3_Pos: bool = False
    """
    Mode Frame : Movement in positive direction Z of selected frame Mode Tool : Movement in positive
    direction Z of selected tool Mode Axes : Movement in positive direction joint 3
    """
    Z_J3_Neg: bool = False
    """
    Mode Frame : Movement in negative direction Z of selected frame Mode Tool : Movement in negative
    direction Z of selected tool Mode Axes : Movement in negative direction joint 3
    """
    Rx_J4_Pos: bool = False
    """
    Mode Frame : Movement in positive direction Rx of selected frame Mode Tool : Movement in
    positive direction Rx of selected tool Mode Axes : Movement in positive direction joint 4
    """
    Rx_J4_Neg: bool = False
    """
    Mode Frame : Movement in negative direction Rx of selected frame Mode Tool : Movement in
    negative direction Rx of selected tool Mode Axes : Movement in negative direction joint 4
    """
    Ry_J5_Pos: bool = False
    """
    Mode Frame : Movement in positive direction Ry of selected frame Mode Tool : Movement in
    positive direction Ry of selected tool Mode Axes : Movement in positive direction joint 5
    """
    Ry_J5_Neg: bool = False
    """
    Mode Frame : Movement in negative direction Ry of selected frame Mode Tool : Movement in
    negative direction Ry of selected tool Mode Axes : Movement in negative direction joint 5
    """
    Rz_J6_Pos: bool = False
    """
    Mode Frame : Movement in positive direction Rz of selected frame Mode Tool : Movement in
    positive direction Rz of selected tool Mode Axes : Movement in positive direction joint 6
    """
    Rz_J6_Neg: bool = False
    """
    Mode Frame : Movement in negative direction Rz of selected frame Mode Tool : Movement in
    negative direction Rz of selected tool Mode Axes : Movement in negative direction joint 6
    """
    E1_Pos: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in positive direction
    first external axis
    """
    E1_Neg: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in negative direction
    first external axis
    """
    E2_Pos: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in positive direction
    second external axis
    """
    E2_Neg: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in negative direction
    second external axis
    """
    E3_Pos: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in positive direction
    third external axis
    """
    E3_Neg: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in negative direction
    third external axis
    """
    E4_Pos: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in positive direction
    fourth external axis
    """
    E4_Neg: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in negative direction
    fourth external axis
    """
    E5_Pos: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in positive direction
    fifth external axis
    """
    E5_Neg: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in negative direction
    fifth external axis
    """
    E6_Pos: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in positive direction
    sixth external axis
    """
    E6_Neg: bool = False
    """
    Mode Frame : not supported Mode Tool : not supported Mode Axes : Movement in negative direction
    sixts external axis
    """


@_dataclass(kw_only=True, slots=True)
class MeasuringInputResult:
    """MeasuringInputResult"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MeasuredCartesianPosition: RobotCartesianPosition = _field(default_factory=lambda: RobotCartesianPosition())
    """
    Measured robot position value at the rising edge of the digital input in selected coordinate
    systems (see input parameters ToolNo and FrameNo).
    """
    ToolNo: int = 0
    """Index of tool of returned position • 0: Flange • 1..254: Tool frames"""
    FrameNo: int = 0
    """Index of frame of returned position • 0: WCS • 1..254: User frames"""
    MeasuredJointPosition: RobotJointPosition = _field(default_factory=lambda: RobotJointPosition())
    """Measured robot position value at the rising edge of the digital input in Joint position."""


@_dataclass(kw_only=True, slots=True)
class ProcessingModeAllowed:
    """ProcessingModeAllowed"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    BUFFERED: bool = False
    """Command is buffered in sequence buffer and executed once"""
    ABORTING: bool = False
    """
    Command is buffered in sequence buffer, aborts and empties previous commands in sequence buffer,
    and is executed once
    """
    PARALLEL: bool = False
    """Command is buffered in parallel buffer and executed once"""
    CONTINUOUS: bool = False
    """
    Command is buffered in parallel buffer and executed repeatedly until deliberate deactivation by
    user
    """
    DEACTIVATE: bool = False
    """CMD execution is stopped and/or CMD is removed from the buffer"""
    TRIGGER_BUFFERED: bool = False
    """Command is buffered in sequence buffer and executed once (Trigger based)"""
    TRIGGER_ABORTING: bool = False
    """
    Command is buffered in sequence buffer, aborts and empties previous commands in sequence buffer,
    and is executed once (Trigger based)
    """
    TRIGGER_ONCE: bool = False
    """Command is buffered in parallel buffer and executed once (Trigger based)"""
    TRIGGER_CONTINUOUS: bool = False
    """
    Command is buffered in parallel buffer and executed repeatedly until deliberate deactivation by
    user (Trigger based)
    """
    TRIGGER_MULTIPLE: bool = False
    """
    Command is buffered and executed multiple times when triggered. The CMD remains in the buffer
    until removed by the user.
    """


@_dataclass(kw_only=True, slots=True)
class RaStatusWord:
    """RaStatusWord"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    IsMoving: bool = False
    """Bit 00: TRUE, when robot’s axes values change due to physical movement of axes"""
    PrimarySequencePaused: bool = False
    """Bit 01: TRUE, when move commands buffered by the primary sequence are currently not processed"""
    InPrimaryPos: bool = False
    """
    Bit 02: TRUE, when robot is moving in the primary sequence, FALSE when robot leaves its position
    by other means Switches back to TRUE in the following two scenarios: 1. During a change to the
    primary sequence the current TCP position is equal to - position when the primary sequence was
    left - target position of an interrupted move command of the primary sequence (see
    "ReturnToPrimary": "ReturnMode" "End position" chapter 6.3.11) 2. The primary sequence is
    active, and the buffer is empty while a new command is buffered by the primary sequence
    Independent of RA state
    """
    SecondarySequenceActive: bool = False
    """Bit 03: Secondary sequence is active, either by user selection or by implicit behavior"""
    IsBlending: bool = False
    """Bit 04: TRUE, when robot is currently blending between two move commands"""
    ErrorPending: bool = False
    """Bit 05: Shows that an error acknowledgement by the client is necessary"""
    RestartInProgress: bool = False
    """Bit 06: RC is restarting"""
    Enabled: bool = False
    """Bit 07: RA power state"""
    RaSequenceState: _e.RaSequenceState = _e.RaSequenceState.IDLE
    """Bit 08 - 09: RA sequence states: Idle, Interrupt active, Axes controlled"""
    OperationMode: _e.OperationMode = _e.OperationMode.T1_LOCAL
    """Bit 10 - Bit 12: Operation Mode: T1 Local, T2 Local, Auto, Auto Ext, T1 Ext, T2 Ext"""
    CollisionDetectedEnabled: bool = False
    """Bit 13: TRUE, while CollisionDetection is enabled (see chapter 6.5.35)"""
    CollisionDetected: bool = False
    """Bit 14: TRUE, when a collision was detected while CollisionDetection is enabled"""
    RestartRequested: bool = False
    """
    Bit 15: TRUE, when the RC request a restart of the RCinduced through the functions
    "WriteRobotSWLimits" or "WriteSystemVariable"
    """
    Accelerating: bool = False
    """Bit 16: RA is currently accelerating. Support of this value is returned via exchangeConfig."""
    Decelerating: bool = False
    """Bit 17: RA is currently decelerating. Support of this value is returned via exchangeConfig."""
    ConstantVelocity: bool = False
    """
    Bit 18: RA is currently not accelerating nor decelerating. Support of this value is returned via
    exchangeConfig.
    """
    Bit19: bool = False
    """Bit 19"""
    Bit20: bool = False
    """Bit 20"""
    Bit21: bool = False
    """Bit 21"""
    Bit22: bool = False
    """Bit 22"""
    Bit23: bool = False
    """Bit 23"""
    Bit24: bool = False
    """Bit 24"""
    Bit25: bool = False
    """Bit 25"""
    Bit26: bool = False
    """Bit 26"""
    Bit27: bool = False
    """Bit 27"""
    Bit28: bool = False
    """Bit 28"""
    Bit29: bool = False
    """Bit 29"""
    Bit30: bool = False
    """Bit 30"""
    Bit31: bool = False
    """Bit 31"""


@_dataclass(kw_only=True, slots=True)
class RCSupportedFunctions:
    """RCSupportedFunctions"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserved: bool = False
    """Byte 00 - Bit 0"""
    ReadRobotData: bool = True
    """
    Byte 00 - Bit 1 -> must be initialized with true, because this command is part of the interface
    initialization
    """
    EnableRobot: bool = False
    """Byte 00 - Bit 2"""
    GroupReset: bool = False
    """Byte 00 - Bit 3"""
    ReadActualPosition: bool = False
    """Byte 00 - Bit 4"""
    ReadActualPositionCyclic: bool = False
    """Byte 00 - Bit 5"""
    ExchangeConfiguration: bool = True
    """
    Byte 00 - Bit 6 -> must be initialized with true, because this command is part of the interface
    initialization
    """
    SetSequence: bool = False
    """Byte 00 - Bit 7"""
    ChangeSpeedOverride: bool = False
    """Byte 01 - Bit 0"""
    ReadMessages: bool = True
    """
    Byte 01 - Bit 1 -> must be initialized with true, because this command is part of the interface
    initialization
    """
    ReadRobotReferenceDynamics: bool = False
    """Byte 01 - Bit 2"""
    WriteFrameData: bool = False
    """Byte 01 - Bit 3"""
    WriteToolData: bool = False
    """Byte 01 - Bit 4"""
    WriteLoadData: bool = False
    """Byte 01 - Bit 5"""
    WriteRobotReferenceDynamics: bool = False
    """Byte 01 - Bit 6"""
    WriteRobotDefaultDynamics: bool = False
    """Byte 01 - Bit 7"""
    ReadRobotDefaultDynamics: bool = False
    """Byte 02 - Bit 0"""
    ReadFrameData: bool = False
    """Byte 02 - Bit 1"""
    ReadToolData: bool = False
    """Byte 02 - Bit 2"""
    ReadLoadData: bool = False
    """Byte 02 - Bit 3"""
    ReadRobotSWLimits: bool = False
    """Byte 02 - Bit 4"""
    GroupJog: bool = False
    """Byte 02 - Bit 5"""
    MoveLinearAbsolute: bool = False
    """Byte 02 - Bit 6"""
    MoveDirectAbsolute: bool = False
    """Byte 02 - Bit 7"""
    MoveAxesAbsolute: bool = False
    """Byte 03 - Bit 0"""
    GroupStop: bool = False
    """Byte 03 - Bit 1"""
    GroupContinue: bool = False
    """Byte 03 - Bit 2"""
    GroupInterrupt: bool = False
    """Byte 03 - Bit 3"""
    ReturnToPrimary: bool = False
    """Byte 03 - Bit 4"""
    MoveLinearAbsoluteJ: bool = False
    """Byte 03 - Bit 5"""
    MoveDirectRelative: bool = False
    """Byte 03 - Bit 6"""
    MoveAxesRelative: bool = False
    """Byte 03 - Bit 7"""
    MoveCircularAbsolute: bool = False
    """Byte 04 - Bit 0"""
    MoveCircularRelative: bool = False
    """Byte 04 - Bit 1"""
    MoveLinearOffset: bool = False
    """Byte 04 - Bit 2"""
    MoveDirectOffset: bool = False
    """Byte 04 - Bit 3"""
    WaitTime: bool = False
    """Byte 04 - Bit 4"""
    ReadDigitalInputs: bool = False
    """Byte 04 - Bit 5"""
    ReadDigitalOutputs: bool = False
    """Byte 04 - Bit 6"""
    WriteDigitalOutputs: bool = False
    """Byte 04 - Bit 7"""
    ReadIntegers: bool = False
    """Byte 05 - Bit 0"""
    ReadReals: bool = False
    """Byte 05 - Bit 1"""
    WriteIntegers: bool = False
    """Byte 05 - Bit 2"""
    WriteReals: bool = False
    """Byte 05 - Bit 3"""
    MoveLinearCam: bool = False
    """Byte 05 - Bit 4"""
    MoveDirectCam: bool = False
    """Byte 05 - Bit 5"""
    MoveCircularCam: bool = False
    """Byte 05 - Bit 6"""
    SetTriggerRegister: bool = False
    """Byte 05 - Bit 7"""
    SetTriggerLimit: bool = False
    """Byte 06 - Bit 0"""
    SetTriggerUser: bool = False
    """Byte 06 - Bit 1"""
    SetTriggerError: bool = False
    """Byte 06 - Bit 2"""
    ReactAtTrigger: bool = False
    """Byte 06 - Bit 3"""
    WaitForTrigger: bool = False
    """Byte 06 - Bit 4"""
    ReadSystemVariable: bool = False
    """Byte 06 - Bit 5"""
    WriteSystemVariable: bool = False
    """Byte 06 - Bit 6"""
    CalculateForwardKinematic: bool = False
    """Byte 06 - Bit 7"""
    CalculateInverseKinematic: bool = False
    """Byte 07 - Bit 0"""
    CalculateCartesianPosition: bool = False
    """Byte 07 - Bit 1"""
    CalculateTool: bool = False
    """Byte 07 - Bit 2"""
    CalculateFrame: bool = False
    """Byte 07 - Bit 3"""
    ActivateNextCommand: bool = False
    """Byte 07 - Bit 4"""
    ShiftPosition: bool = False
    """Byte 07 - Bit 5"""
    CallSubprogram: bool = False
    """Byte 07 - Bit 6"""
    MoveLinearRelative: bool = False
    """Byte 07 - Bit 7"""
    WriteCallSubprogramCyclic: bool = False
    """Byte 08 - Bit 0"""
    ReadCallSubprogramCyclic: bool = False
    """Byte 08 - Bit 1"""
    StopSubprogram: bool = False
    """Byte 08 - Bit 2"""
    ReadDHParameter: bool = False
    """Byte 08 - Bit 3"""
    RestartController: bool = False
    """Byte 08 - Bit 4"""
    ReadActualTCPVelocity: bool = False
    """Byte 08 - Bit 5"""
    UserLogin: bool = False
    """Byte 08 - Bit 6"""
    SwitchLanguage: bool = False
    """Byte 08 - Bit 7"""
    WriteRobotSWLimits: bool = False
    """Byte 09 - Bit 0"""
    SetOperationMode: bool = False
    """Byte 09 - Bit 1"""
    ReadWorkArea: bool = False
    """Byte 09 - Bit 2"""
    WriteWorkArea: bool = False
    """Byte 09 - Bit 3"""
    ActivateWorkArea: bool = False
    """Byte 09 - Bit 4"""
    MonitorWorkArea: bool = False
    """Byte 09 - Bit 5"""
    MoveApproachLinear: bool = False
    """Byte 09 - Bit 6"""
    MoveDepartLinear: bool = False
    """Byte 09 - Bit 7"""
    MoveApproachDirect: bool = False
    """Byte 10 - Bit 0"""
    MoveDepartDirect: bool = False
    """Byte 10 - Bit 1"""
    SearchHardstop: bool = False
    """Byte 10 - Bit 2"""
    SearchHardstopJ: bool = False
    """Byte 10 - Bit 3"""
    MovePickPlaceLinear: bool = False
    """Byte 10 - Bit 4"""
    MovePickPlaceDirect: bool = False
    """Byte 10 - Bit 5"""
    ActivateConveyorTracking: bool = False
    """Byte 10 - Bit 6"""
    RedefineTrackingPosition: bool = False
    """Byte 10 - Bit 7"""
    SyncToConveyor: bool = False
    """Byte 11 - Bit 0"""
    ConfigureConveyor: bool = False
    """Byte 11 - Bit 1"""
    MoveSuperImposed: bool = False
    """Byte 11 - Bit 2"""
    MoveSuperImposedDynamic: bool = False
    """Byte 11 - Bit 3"""
    ReadAnalogInput: bool = False
    """Byte 11 - Bit 4"""
    ReadAnalogOutput: bool = False
    """Byte 11 - Bit 5"""
    WriteAnalogOutput: bool = False
    """Byte 11 - Bit 6"""
    MeasuringInput: bool = False
    """Byte 11 - Bit 7"""
    AbortMeasuringInput: bool = False
    """Byte 12 - Bit 0"""
    SetTriggerMotion: bool = False
    """Byte 12 - Bit 1"""
    OpenBrake: bool = False
    """Byte 12 - Bit 2"""
    PathAccuracyMode: bool = False
    """Byte 12 - Bit 3"""
    AvoidSingularity: bool = False
    """Byte 12 - Bit 4"""
    ForceControl: bool = False
    """Byte 12 - Bit 5"""
    ForceLimit: bool = False
    """Byte 12 - Bit 6"""
    ReadActualForce: bool = False
    """Byte 12 - Bit 7"""
    BrakeTest: bool = False
    """Byte 13 - Bit 0"""
    SoftSwitchTCP: bool = False
    """Byte 13 - Bit 1"""
    CreateSpline: bool = False
    """Byte 13 - Bit 2"""
    DeleteSpline: bool = False
    """Byte 13 - Bit 3"""
    MoveSpline: bool = False
    """Byte 13 - Bit 4"""
    DynamicSpline: bool = False
    """Byte 13 - Bit 5"""
    LoadMeasurementAutomatic: bool = False
    """Byte 13 - Bit 6"""
    LoadMeasurementSequential: bool = False
    """Byte 13 - Bit 7"""
    CollisionDetection: bool = False
    """Byte 14 - Bit 0"""
    FreeDrive: bool = False
    """Byte 14 - Bit 1"""
    UnitMeasurement: bool = False
    """Byte 14 - Bit 2"""
    Byte14Bit03: bool = False
    """Byte 14 - Bit 3"""
    Byte14Bit04: bool = False
    """Byte 14 - Bit 4"""
    Byte14Bit05: bool = False
    """Byte 14 - Bit 5"""
    Byte14Bit06: bool = False
    """Byte 14 - Bit 6"""
    Byte14Bit07: bool = False
    """Byte 14 - Bit 7"""
    Byte15Bit00: bool = False
    """Byte 15 - Bit 0"""
    Byte15Bit01: bool = False
    """Byte 15 - Bit 1"""
    Byte15Bit02: bool = False
    """Byte 15 - Bit 2"""
    Byte15Bit03: bool = False
    """Byte 15 - Bit 3"""
    Byte15Bit04: bool = False
    """Byte 15 - Bit 4"""
    Byte15Bit05: bool = False
    """Byte 15 - Bit 5"""
    Byte15Bit06: bool = False
    """Byte 15 - Bit 6"""
    Byte15Bit07: bool = False
    """Byte 15 - Bit 7"""
    Byte16Bit00: bool = False
    """Byte 16 - Bit 0"""
    Byte16Bit01: bool = False
    """Byte 15 - Bit 1"""
    Byte16Bit02: bool = False
    """Byte 15 - Bit 2"""
    Byte16Bit03: bool = False
    """Byte 15 - Bit 3"""
    Byte16Bit04: bool = False
    """Byte 15 - Bit 4"""
    Byte16Bit05: bool = False
    """Byte 15 - Bit 5"""
    Byte16Bit06: bool = False
    """Byte 15 - Bit 6"""
    Byte16Bit07: bool = False
    """Byte 15 - Bit 7"""
    Byte17Bit00: bool = False
    """Byte 17 - Bit 0"""
    Byte17Bit01: bool = False
    """Byte 17 - Bit 1"""
    Byte17Bit02: bool = False
    """Byte 17 - Bit 2"""
    Byte17Bit03: bool = False
    """Byte 17 - Bit 3"""
    Byte17Bit04: bool = False
    """Byte 17 - Bit 4"""
    Byte17Bit05: bool = False
    """Byte 17 - Bit 5"""
    Byte17Bit06: bool = False
    """Byte 17 - Bit 6"""
    Byte17Bit07: bool = False
    """Byte 17 - Bit 7"""
    Byte18Bit00: bool = False
    """Byte 18 - Bit 0"""
    Byte18Bit01: bool = False
    """Byte 18 - Bit 1"""
    Byte18Bit02: bool = False
    """Byte 18 - Bit 2"""
    Byte18Bit03: bool = False
    """Byte 18 - Bit 3"""
    Byte18Bit04: bool = False
    """Byte 18 - Bit 4"""
    Byte18Bit05: bool = False
    """Byte 18 - Bit 5"""
    Byte18Bit06: bool = False
    """Byte 18 - Bit 6"""
    Byte18Bit07: bool = False
    """Byte 18 - Bit 7"""


@_dataclass(kw_only=True, slots=True)
class RobotAxesFlags:
    """RobotAxesFlags"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Bit00: bool = False
    """Bit00 : Not used"""
    AxisJ1: bool = False
    """Bit01 : Robot axis J1 - property depends of usage"""
    AxisJ2: bool = False
    """Bit02 : Robot axis J2 - property depends of usage"""
    AxisJ3: bool = False
    """Bit03 : Robot axis J3 - property depends of usage"""
    AxisJ4: bool = False
    """Bit04 : Robot axis J4 - property depends of usage"""
    AxisJ5: bool = False
    """Bit05 : Robot axis J5 - property depends of usage"""
    AxisJ6: bool = False
    """Bit06 : Robot axis J6 - property depends of usage"""
    Bit07: bool = False
    """Bit07 : Not used"""


@_dataclass(kw_only=True, slots=True)
class SWLimits:
    """SWLimits"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Timestamp: IEC_TIMESTAMP = _field(default_factory=lambda: IEC_TIMESTAMP())
    """Timestamp"""
    J1LowerLimit: float = 0.0
    """Negative software limit for Joint J1 [mm/°]"""
    J1UpperLimit: float = 0.0
    """Positive software limit for Joint J1 [mm/°]"""
    J2LowerLimit: float = 0.0
    """Negative software limit for Joint J2 [mm/°]"""
    J2UpperLimit: float = 0.0
    """Positive software limit for Joint J2 [mm/°]"""
    J3LowerLimit: float = 0.0
    """Negative software limit for Joint J3 [mm/°]"""
    J3UpperLimit: float = 0.0
    """Positive software limit for Joint J3 [mm/°]"""
    J4LowerLimit: float = 0.0
    """Negative software limit for Joint J4 [mm/°]"""
    J4UpperLimit: float = 0.0
    """Positive software limit for Joint J4 [mm/°]"""
    J5LowerLimit: float = 0.0
    """Negative software limit for Joint J5 [mm/°]"""
    J5UpperLimit: float = 0.0
    """Positive software limit for Joint J5 [mm/°]"""
    J6LowerLimit: float = 0.0
    """Negative software limit for Joint J6 [mm/°]"""
    J6UpperLimit: float = 0.0
    """Positive software limit for Joint J6 [mm/°]"""
    E1LowerLimit: float = 0.0
    """Negative software limit for axis E1 [mm/°]"""
    E1UpperLimit: float = 0.0
    """Positive software limit for axis E1 [mm/°]"""
    E2LowerLimit: float = 0.0
    """Negative software limit for axis E2 [mm/°]"""
    E2UpperLimit: float = 0.0
    """Positive software limit for axis E2 [mm/°]"""
    E3LowerLimit: float = 0.0
    """Negative software limit for axis E3 [mm/°]"""
    E3UpperLimit: float = 0.0
    """Positive software limit for axis E3 [mm/°]"""
    E4LowerLimit: float = 0.0
    """Negative software limit for axis E4 [mm/°]"""
    E4UpperLimit: float = 0.0
    """Positive software limit for axis E4 [mm/°]"""
    E5LowerLimit: float = 0.0
    """Negative software limit for axis E5 [mm/°]"""
    E5UpperLimit: float = 0.0
    """Positive software limit for axis E5 [mm/°]"""
    E6LowerLimit: float = 0.0
    """Negative software limit for axis E6 [mm/°]"""
    E6UpperLimit: float = 0.0
    """Positive software limit for axis E6 [mm/°]"""


@_dataclass(kw_only=True, slots=True)
class SynchronizationModes:
    """SynchronizationModes"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Tool: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for tool"""
    Frame: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for frame"""
    Load: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for load"""
    WorkAreas: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for work areas"""
    SWLimits: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for SW limits"""
    DefaultDynamics: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for defaul dynamics"""
    ReferenceDynamics: list[_e.SyncMode] = _field(default_factory=lambda: [_e.SyncMode.NO_SYNCHRONIZATION] * 2)
    """synchronization direction for reference dynamics"""


@_dataclass(kw_only=True, slots=True)
class SyncUserInteraction:
    """SyncUserInteraction"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Tool: bool = False
    """synchronization of tool needs user interaction"""
    Frame: bool = False
    """synchronization of frame needs user interaction"""
    Load: bool = False
    """synchronization of load needs user interaction"""
    WorkAreas: bool = False
    """synchronization of work areas needs user interaction"""
    SWLimits: bool = False
    """synchronization of SW limits needs user interaction"""
    DefaultDynamics: bool = False
    """synchronization of defaul dynamics needs user interaction"""
    ReferenceDynamics: bool = False
    """synchronization of reference dynamics needs user interaction"""


@_dataclass(kw_only=True, slots=True)
class TrackingStatus:
    """TrackingStatus"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ConveyorTrackingEnabled: bool = False
    """TRUE, while a "ConveyorTracking" function is enabled"""
    WaitingForSynchronization: bool = False
    """
    TRUE, while robot is waiting for condition defined by "SyncInMode" after "SyncToConveyor" has
    been executed
    """
    Synchronizing: bool = False
    """TRUE, while robot is matching the TCP’s velocity to the conveyor’s velocity"""
    Synchronous: bool = False
    """TRUE, while TCP is moving synchronously to conveyor"""
    Desynchronizing: bool = False
    """TRUE, while robot is terminating synchronous movement"""
    SyncOutZoneEntered: bool = False
    """TRUE, while assigned UCS is within "SyncOutZone" """
    SyncOutZoneLeft: bool = False
    """
    TRUE, when assigned UCS leaves "SyncOutZone" Reset, when robot’s synchronous movement has been
    stopped
    """
    NotUsed: bool = False
    """Not used"""


@_dataclass(kw_only=True, slots=True)
class TurnNumber:
    """TurnNumber"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1Turns: int = 0
    """Turn number of J1"""
    J2Turns: int = 0
    """Turn number of J2"""
    J3Turns: int = 0
    """Turn number of J3"""
    J4Turns: int = 0
    """Turn number of J4"""
    J5Turns: int = 0
    """Turn number of J5"""
    J6Turns: int = 0
    """Turn number of J6"""
    E1Turns: int = 0
    """Turn number of E1"""


@_dataclass(kw_only=True, slots=True)
class VersionStruct:
    """VersionStruct"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    MajorVersion: int = 0
    """Major version"""
    MinorVersion: int = 0
    """Minor version"""
    PatchVersion: int = 0
    """Patch version"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCommand:
    """TelegramPlcToRobCommand"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramPlcToRobCommandHeader = _field(default_factory=lambda: TelegramPlcToRobCommandHeader())
    """Header"""
    Payload: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('PARAMETER_PAYLOAD_MAX')))
    """Payload"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCommandHeader:
    """TelegramPlcToRobCommandHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CmdType: _e.CmdType = _e.CmdType.RobotTask
    """Command type"""
    Prio: _e.PriorityLevel = _e.PriorityLevel.VERY_HIGH
    """CMD priority level"""
    ExecMode: _e.ExecutionMode = _e.ExecutionMode.SEQUENCE_PRIMARY
    """Execution Mode"""
    ParSequence: int = 0
    """Parameter Sequence"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicData:
    """TelegramPlcToRobCyclicData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ToolNo: int = 0
    """Current Tool"""
    FrameNo: int = 0
    """Current Frame"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalCartesianPosition:
    """TelegramPlcToRobCyclicOptionalCartesianPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """TCP Position on the X-Axis"""
    Y: float = 0.0
    """TCP Position on the Y-Axis"""
    Z: float = 0.0
    """TCP Position on the Z-Axis"""
    Rx: float = 0.0
    """Rotation around the X-Axis (RX)"""
    Ry: float = 0.0
    """Rotation around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Rotation around the Z-Axis (RZ)"""
    Config: int = 0
    """Configuration"""
    Turns_J2_J1: int = 0
    """Turns of J1 and J2"""
    Turns_J4_J3: int = 0
    """Turns of J3 and J4"""
    Turns_J6_J5: int = 0
    """Turns of J6 and J5"""
    Turns_E1: int = 0
    """Turns of E1"""
    E1: float = 0.0
    """Position of first external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalCartesianPositionExt:
    """TelegramPlcToRobCyclicOptionalCartesianPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalCurrent:
    """TelegramPlcToRobCyclicOptionalCurrent"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Current of first joint of the robot"""
    J2: float = 0.0
    """Current of second joint of the robot"""
    J3: float = 0.0
    """Current of third joint of the robot"""
    J4: float = 0.0
    """Current of fourth joint of the robot"""
    J5: float = 0.0
    """Current of fifth joint of the robot"""
    J6: float = 0.0
    """Current of sixth joint of the robot"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalCurrentExt:
    """TelegramPlcToRobCyclicOptionalCurrentExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: float = 0.0
    """Current of first external joint of the robot"""
    E2: float = 0.0
    """Current of second external axis"""
    E3: float = 0.0
    """Current of third external axis"""
    E4: float = 0.0
    """Current of fourth external axis"""
    E5: float = 0.0
    """Current of fifth external axis"""
    E6: float = 0.0
    """Current of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalForce:
    """TelegramPlcToRobCyclicOptionalForce"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """Force on the X-Axis"""
    Y: float = 0.0
    """Force on the Y-Axis"""
    Z: float = 0.0
    """Force on the Z-Axis"""
    Rx: float = 0.0
    """Force around the X-Axis (RX)"""
    Ry: float = 0.0
    """Force around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Force around the Z-Axis (RZ)"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalForceExt:
    """TelegramPlcToRobCyclicOptionalForceExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: float = 0.0
    """Force on the external axis 1"""
    E2: float = 0.0
    """Force on the external axis 2"""
    E3: float = 0.0
    """Force on the external axis 3"""
    E4: float = 0.0
    """Force om the external axis 4"""
    E5: float = 0.0
    """Force on the external axis 5"""
    E6: float = 0.0
    """Force on the external axis 6"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalJointPosition:
    """TelegramPlcToRobCyclicOptionalJointPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Position of first joint of the robot"""
    J2: float = 0.0
    """Position of second joint of the robot"""
    J3: float = 0.0
    """Position of third joint of the robot"""
    J4: float = 0.0
    """Position of fourth joint of the robot"""
    J5: float = 0.0
    """Position of fifth joint of the robot"""
    J6: float = 0.0
    """Position of sixth joint of the robot"""
    E1: float = 0.0
    """Position of first external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalJointPositionExt:
    """TelegramPlcToRobCyclicOptionalJointPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalSubProgramData:
    """TelegramPlcToRobCyclicOptionalSubProgramData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Data: list[int] = _field(default_factory=lambda: [0] * 26)
    """Sub program data"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobCyclicOptionalData:
    """TelegramPlcToRobCyclicOptionalData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SubProgramData: TelegramPlcToRobCyclicOptionalSubProgramData = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalSubProgramData())
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via the
    function “CallSubprogram”
    """
    CartesianPosition: TelegramPlcToRobCyclicOptionalCartesianPosition = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalCartesianPosition())
    """
    short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ), configuration bytes
    (Config, TurnNumber), position of first external axis (E1) and corresponding coordinate systems
    (ToolNo, FrameNo)
    """
    CartesianPositionExt: TelegramPlcToRobCyclicOptionalCartesianPositionExt = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalCartesianPositionExt())
    """
    the external axis values for an extended cartesian position (E2, E3, E4, E5, E6) When selected,
    Tool and Frame will automatically cyclically be sent from client to server.
    """
    JointPosition: TelegramPlcToRobCyclicOptionalJointPosition = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalJointPosition())
    """
    short axes position with joint values (J1, J2, J3,J4, J5, J6) and position of first external
    axis (E1)
    """
    JointPositionExt: TelegramPlcToRobCyclicOptionalJointPositionExt = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalJointPositionExt())
    """the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    Force: TelegramPlcToRobCyclicOptionalForce = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalForce())
    """force with the divided forces in the individual directions (X, Y, Z, RX, RY, RZ)"""
    ForceExt: TelegramPlcToRobCyclicOptionalForceExt = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalForceExt())
    """current force for the external axis (E1, E2, E3, E4, E5, E6)"""
    Current: TelegramPlcToRobCyclicOptionalCurrent = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalCurrent())
    """ctual axes current of individual axes (J1, J2, J3, J4, J5, J6)"""
    CurrentExt: TelegramPlcToRobCyclicOptionalCurrentExt = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalCurrentExt())
    """actual current for the external axis (E1, E2,E3, E4, E5, E6)"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobFooter:
    """TelegramPlcToRobFooter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    LifeSign: int = 0
    """Life Sign"""
    Reserve: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobFragment:
    """TelegramPlcToRobFragment"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramPlcToRobFragmentHeader = _field(default_factory=lambda: TelegramPlcToRobFragmentHeader())
    """Header"""
    Command: TelegramPlcToRobCommand = _field(default_factory=lambda: TelegramPlcToRobCommand())
    """Command"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobFragmentHeader:
    """TelegramPlcToRobFragmentHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CmdID: int = 0
    """Command Instance Identifier used to assign the CMD payload to a specific CMD instance"""
    Reserve: int = 0
    """Empty reserve byte"""
    FragmentAction: int = 0
    """Fragment Action Byte"""
    PayloadPointer: int = 0
    """Append received payload in the receive buffer at this position"""
    PayloadLength: int = 0
    """Length of the CMD payload"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobHeader:
    """TelegramPlcToRobHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SRCIVersion: int = 0
    """
    Version of SRCI specification Bit 0-4 : Minor version = Features (0..31) Bit 5-7 : Major version
    = Breaking change (0..07)
    """
    FastStop_LifeSign: int = 0
    """Fast stop trigger | LifeSign"""
    TelegramLengthPlcToRob: int = 0
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction
    client to server
    """
    TelegramLengthRobToPlc: int = 0
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction
    server to client
    """
    AxesGroupID_Control: int = 0
    """Control AxesGroupID | Telegtam state control"""
    Reserved: int = 0
    """Reserved for later versions"""
    TelegramNumberPlcToRob: int = 0
    """Configuration of the optional cyclic data. Direction client to server"""
    TelegramNumberRobToPlc: int = 0
    """Configuration of the optional cyclic data. Direction server to client"""
    ClientDate: int = 0
    """Date of the client in the format days since 1990.01.01"""
    ClientTime: int = 0
    """Time in the clients time zone in the format milliseconds since start of day"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobSequence:
    """TelegramPlcToRobSequence"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramPlcToRobSequenceHeader = _field(default_factory=lambda: TelegramPlcToRobSequenceHeader())
    """Header"""
    Fragment: list[TelegramPlcToRobFragment] = _field(default_factory=lambda: [TelegramPlcToRobFragment() for _ in range(_iec.array_len(0, _iec.Param('FRAGMENT_MAX')))])
    """Fragment"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRobSequenceHeader:
    """TelegramPlcToRobSequenceHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SEQ_ACK: int = 0
    """Telegram Sequence and Acknowledgement number"""
    PayloadLength: int = 0
    """Length of the Telegram Sequence excluding this Telegram Sequence Header"""


@_dataclass(kw_only=True, slots=True)
class TelegramPlcToRob:
    """TelegramPlcToRob"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramPlcToRobHeader = _field(default_factory=lambda: TelegramPlcToRobHeader())
    """Header"""
    Cyclic: TelegramPlcToRobCyclicData = _field(default_factory=lambda: TelegramPlcToRobCyclicData())
    """Cyclic optional data"""
    CyclicOptional: TelegramPlcToRobCyclicOptionalData = _field(default_factory=lambda: TelegramPlcToRobCyclicOptionalData())
    """Cyclic optional data"""
    Sequence: list[TelegramPlcToRobSequence] = _field(default_factory=lambda: [TelegramPlcToRobSequence() for _ in range(2)])
    """Sequence Data"""
    Footer: TelegramPlcToRobFooter = _field(default_factory=lambda: TelegramPlcToRobFooter())
    """Footer"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCommand:
    """TelegramRobToPlcCommand"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramRobToPlcCommandHeader = _field(default_factory=lambda: TelegramRobToPlcCommandHeader())
    """Header"""
    Payload: list[int] = _field(default_factory=lambda: [0] * _iec.array_len(0, _iec.Param('RESPONSE_PAYLOAD_MAX')))
    """Payload"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCommandHeader:
    """TelegramRobToPlcCommandHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    ParSeq: int = 0
    """Parameter squence"""
    State: _e.CmdMessageState = _e.CmdMessageState.EMPTY
    """message Staet"""
    AlarmMessageSeverity: int = 0
    """Alarm Message Severity"""
    AlarmMessageCode: int = 0
    """Alarm Message Code"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalCartesianPosition:
    """TelegramRobToPlcCyclicOptionalCartesianPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """TCP Position on the X-Axis"""
    Y: float = 0.0
    """TCP Position on the Y-Axis"""
    Z: float = 0.0
    """TCP Position on the Z-Axis"""
    Rx: float = 0.0
    """Rotation around the X-Axis (RX)"""
    Ry: float = 0.0
    """Rotation around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Rotation around the Z-Axis (RZ)"""
    Config: int = 0
    """Configuration"""
    Turns_J2_J1: int = 0
    """Turns of J1 and J2"""
    Turns_J4_J3: int = 0
    """Turns of J3 and J4"""
    Turns_J6_J5: int = 0
    """Turns of J6 and J5"""
    Turns_E1: int = 0
    """Turns of E1"""
    E1: float = 0.0
    """Position of first external axis"""
    ToolNo: int = 0
    """Tool Number"""
    FrameNo: int = 0
    """Frane Number"""
    CurrentlyUsedToolNo: int = 0
    """Currently used tool number"""
    CurrentlyUsedFrameNo: int = 0
    """Currently used frame number"""
    Reserve_1: int = 0
    """Reserve"""
    Reserve_2: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalCartesianPositionExt:
    """TelegramRobToPlcCyclicOptionalCartesianPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalCurrent:
    """TelegramRobToPlcCyclicOptionalCurrent"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Current of first joint of the robot"""
    J2: float = 0.0
    """Current of second joint of the robot"""
    J3: float = 0.0
    """Current of third joint of the robot"""
    J4: float = 0.0
    """Current of fourth joint of the robot"""
    J5: float = 0.0
    """Current of fifth joint of the robot"""
    J6: float = 0.0
    """Current of sixth joint of the robot"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalCurrentExt:
    """TelegramRobToPlcCyclicOptionalCurrentExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: float = 0.0
    """Current of first external joint of the robot"""
    E2: float = 0.0
    """Current of second external axis"""
    E3: float = 0.0
    """Current of third external axis"""
    E4: float = 0.0
    """Current of fourth external axis"""
    E5: float = 0.0
    """Current of fifth external axis"""
    E6: float = 0.0
    """Current of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalForce:
    """TelegramRobToPlcCyclicOptionalForce"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    X: float = 0.0
    """Force on the X-Axis"""
    Y: float = 0.0
    """Force on the Y-Axis"""
    Z: float = 0.0
    """Force on the Z-Axis"""
    Rx: float = 0.0
    """Force around the X-Axis (RX)"""
    Ry: float = 0.0
    """Force around the Y-Axis (RY)"""
    Rz: float = 0.0
    """Force around the Z-Axis (RZ)"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalForceExt:
    """TelegramRobToPlcCyclicOptionalForceExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E1: float = 0.0
    """Force on the external axis 1"""
    E2: float = 0.0
    """Force on the external axis 2"""
    E3: float = 0.0
    """Force on the external axis 3"""
    E4: float = 0.0
    """Force om the external axis 4"""
    E5: float = 0.0
    """Force on the external axis 5"""
    E6: float = 0.0
    """Force on the external axis 6"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalJointPosition:
    """TelegramRobToPlcCyclicOptionalJointPosition"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    J1: float = 0.0
    """Position of first joint of the robot"""
    J2: float = 0.0
    """Position of second joint of the robot"""
    J3: float = 0.0
    """Position of third joint of the robot"""
    J4: float = 0.0
    """Position of fourth joint of the robot"""
    J5: float = 0.0
    """Position of fifth joint of the robot"""
    J6: float = 0.0
    """Position of sixth joint of the robot"""
    E1: float = 0.0
    """Position of first external axis"""
    E1_Reserve: int = 0
    """Reserve"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalJointPositionExt:
    """TelegramRobToPlcCyclicOptionalJointPositionExt"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    E2: float = 0.0
    """Position of second external axis"""
    E3: float = 0.0
    """Position of third external axis"""
    E4: float = 0.0
    """Position of fourth external axis"""
    E5: float = 0.0
    """Position of fifth external axis"""
    E6: float = 0.0
    """Position of sixth external axis"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalSubProgramData:
    """TelegramRobToPlcCyclicOptionalSubProgramData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Data: list[int] = _field(default_factory=lambda: [0] * 26)
    """Sub program data"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcCyclicOptionalData:
    """TelegramRobToPlcCyclicOptionalData"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SubProgramData: TelegramRobToPlcCyclicOptionalSubProgramData = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalSubProgramData())
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via the
    function “CallSubprogram”
    """
    CartesianPosition: TelegramRobToPlcCyclicOptionalCartesianPosition = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalCartesianPosition())
    """
    cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ), configuration bytes
    (Config, TurnNumber), position of first external axis (E1) and corresponding coordinate systems
    (ToolNo, FrameNo)
    """
    JointPosition: TelegramRobToPlcCyclicOptionalJointPosition = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalJointPosition())
    """axes position with joint values (J1, J2, J3,J4, J5, J6) and position of first external axis (E1)"""
    Force: TelegramRobToPlcCyclicOptionalForce = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalForce())
    """force with the divided forces in the individual directions (X, Y, Z, RX, RY, RZ)"""
    Current: TelegramRobToPlcCyclicOptionalCurrent = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalCurrent())
    """Transmit actual axes current of individual axes (J1, J2, J3, J4, J5, J6)"""
    TwoSequences: int = 0
    """
    Set to 1 to define two Sequences in one Telegram. If activated, 2 sequences also has to be
    activated in the ClientServer direction.
    """
    CartesianPositionExt: TelegramRobToPlcCyclicOptionalCartesianPositionExt = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalCartesianPositionExt())
    """
    Transmit the external axis values for an extended cartesian position (E2, E3, E4, E5, E6) When
    selected, Tool and Frame will automatically cyclically be sent from client to server.
    """
    JointPositionExt: TelegramRobToPlcCyclicOptionalJointPositionExt = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalJointPositionExt())
    """Transmit the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""
    ForceExt: TelegramRobToPlcCyclicOptionalCurrentExt = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalCurrentExt())
    """Transmit actual axes force of individual axes (E1, E2, E3, E4, E5, E6)"""
    CurrentExt: TelegramRobToPlcCyclicOptionalCurrentExt = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalCurrentExt())
    """Transmit actual axes current of individual axes (E1, E2, E3, E4, E5, E6)"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcFooter:
    """TelegramRobToPlcFooter"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Reserve: int = 0
    """Reserve"""
    LifeSign: int = 0
    """Life Sign"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcFragment:
    """TelegramRobToPlcFragment"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramRobToPlcFragmentHeader = _field(default_factory=lambda: TelegramRobToPlcFragmentHeader())
    """Header"""
    Command: TelegramRobToPlcCommand = _field(default_factory=lambda: TelegramRobToPlcCommand())
    """Command"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcFragmentHeader:
    """TelegramRobToPlcFragmentHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    CmdID: int = 0
    """Command Instance Identifier used to assign the CMD payload to a specific CMD instance"""
    Reserve: int = 0
    """Empty reserve byte"""
    FragmentAction: int = 0
    """Fragment Action Byte"""
    PayloadPointer: int = 0
    """Append received payload in the receive buffer at this position"""
    PayloadLength: int = 0
    """Length of the CMD payload"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcHeader:
    """TelegramRobToPlcHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SRCIVersion: VersionStruct = _field(default_factory=lambda: VersionStruct())
    """
    Version of SRCI specification Bit 0-4 : Minor version = Features (0..31) Bit 5-7 : Major version
    = Breaking change (0..07)
    """
    LifeSign: int = 0
    """Connection alive signal"""
    Reserved: int = 0
    """Reserved byte"""
    TelegramState: _e.TelegramState = _e.TelegramState.UNDEFINED
    """Initialization and Telegram control state"""
    StatusRobotArm: int = 0
    """Combination of various RA related states."""
    Override: int = 0
    """Actual override in percentage encoding"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcSequence:
    """TelegramRobToPlcSequence"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramRobToPlcSequenceHeader = _field(default_factory=lambda: TelegramRobToPlcSequenceHeader())
    """Header"""
    Fragment: list[TelegramRobToPlcFragment] = _field(default_factory=lambda: [TelegramRobToPlcFragment() for _ in range(_iec.array_len(0, _iec.Param('FRAGMENT_MAX')))])
    """Fragment"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlcSequenceHeader:
    """TelegramRobToPlcSequenceHeader"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    SEQ_ACK: int = 0
    """Telegram Sequence and Acknowledgement number"""
    PayloadLength: int = 0
    """Length of the Telegram Sequence excluding this Telegram Sequence Header"""


@_dataclass(kw_only=True, slots=True)
class TelegramRobToPlc:
    """TelegramRobToPlc"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    Header: TelegramRobToPlcHeader = _field(default_factory=lambda: TelegramRobToPlcHeader())
    """Telegram Header"""
    CyclicOptional: TelegramRobToPlcCyclicOptionalData = _field(default_factory=lambda: TelegramRobToPlcCyclicOptionalData())
    """Cyclic optional data"""
    Sequence: list[TelegramRobToPlcSequence] = _field(default_factory=lambda: [TelegramRobToPlcSequence() for _ in range(2)])
    """Sequence Data"""
    Footer: TelegramRobToPlcFooter = _field(default_factory=lambda: TelegramRobToPlcFooter())
    """Footer"""


@_dataclass(kw_only=True, slots=True)
class Telegram:
    """Telegram"""

    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]
    PlcToRob: TelegramPlcToRob = _field(default_factory=lambda: TelegramPlcToRob())
    """PLC to Robot"""
    RobToPlc: TelegramRobToPlc = _field(default_factory=lambda: TelegramRobToPlc())
    """Robot to PLC"""


# ---- IEC layout information (used by srci.codec) ----
AbortMeasuringInputOutCmd._IEC_FIELDS_ = (
)
AbortMeasuringInputParCmd._IEC_FIELDS_ = (
    _iec.IecField('MeasuringID', _iec.UINT),
)
RspHeader._IEC_FIELDS_ = (
    _iec.IecField('ParSeq', _iec.USINT),
    _iec.IecField('State', _iec.EnumType(_e.CmdMessageState)),
    _iec.IecField('AlarmMessageSeverity', _iec.EnumType(_e.Severity)),
    _iec.IecField('AlarmMessageCode', _iec.UINT),
)
AbortMeasuringInputRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
CmdHeader._IEC_FIELDS_ = (
    _iec.IecField('CmdTyp', _iec.EnumType(_e.CmdType)),
    _iec.IecField('ExecMode', _iec.EnumType(_e.ExecutionMode)),
    _iec.IecField('ParSeq', _iec.BYTE),
    _iec.IecField('Priority', _iec.EnumType(_e.PriorityLevel)),
)
AbortMeasuringInputSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('MeasuringID', _iec.UINT),
)
ActivateNextCommandOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
ActivateNextCommandParCmd._IEC_FIELDS_ = (
    _iec.IecField('ListenerID', _iec.SINT),
)
ActivateNextCommandRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
ActivateNextCommandSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
)
AvoidSingularityOutCmd._IEC_FIELDS_ = (
)
AvoidSingularityParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.SingularityAvoidanceMode)),
)
AvoidSingularityRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BOOL),
)
AvoidSingularitySendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Enable', _iec.BOOL),
    _iec.IecField('Mode', _iec.EnumType(_e.SingularityAvoidanceMode)),
)
BrakeTestOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RobotAxesStatus', _iec.StructType(RobotAxesFlags)),
    _iec.IecField('ExternalAxesStatus', _iec.StructType(ExternalAxesFlags)),
    _iec.IecField('RobotAxesWarning', _iec.StructType(RobotAxesFlags)),
    _iec.IecField('ExternalAxesWarning', _iec.StructType(ExternalAxesFlags)),
)
BrakeTestParCmd._IEC_FIELDS_ = (
    _iec.IecField('RobotAxesActive', _iec.StructType(RobotAxesFlags)),
    _iec.IecField('ExternalAxesActive', _iec.StructType(ExternalAxesFlags)),
)
BrakeTestRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('RobotAxesStatus', _iec.BYTE),
    _iec.IecField('ExternalAxesStatus', _iec.BYTE),
    _iec.IecField('RobotAxesWarning', _iec.BYTE),
    _iec.IecField('ExternalAxesWarning', _iec.BYTE),
)
BrakeTestSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('RobotAxesActive', _iec.BYTE),
    _iec.IecField('ExternalAxesActive', _iec.BYTE),
)
CallSubprogramOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InstanceID', _iec.DINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('InProgress', _iec.BOOL),
    _iec.IecField('ReturnData', _iec.ArrayType(0, _iec.Param('SUB_PROGRAM_DATA_MAX'), _iec.BYTE)),
)
CallSubprogramParCmd._IEC_FIELDS_ = (
    _iec.IecField('JobID', _iec.UINT),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Data', _iec.ArrayType(0, _iec.Param('SUB_PROGRAM_DATA_MAX'), _iec.BYTE)),
)
CallSubprogramRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('InProgress', _iec.BOOL),
    _iec.IecField('ReturnData', _iec.ArrayType(0, _iec.Param('SUB_PROGRAM_DATA_MAX'), _iec.BYTE)),
)
CallSubprogramSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('JobID', _iec.UINT),
    _iec.IecField('Data', _iec.ArrayType(0, _iec.Param('SUB_PROGRAM_DATA_MAX'), _iec.BYTE)),
)
CollisionDetectionOutCmd._IEC_FIELDS_ = (
)
CollisionDetectionParCmd._IEC_FIELDS_ = (
    _iec.IecField('ProcessingMode', _iec.EnumType(_e.ProcessingMode)),
    _iec.IecField('ReactionMode', _iec.EnumType(_e.CollisionReactionMode)),
    _iec.IecField('ActivateMonitoring', _iec.BOOL),
    _iec.IecField('ThresholdMode', _iec.EnumType(_e.ThresholdMode)),
    _iec.IecField('Sensitivity', _iec.REAL),
    _iec.IecField('SensitivityAxis', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('LimitAxis', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('UnitLimitAxis', _iec.USINT),
    _iec.IecField('SequenceFlag', _iec.EnumType(_e.SequenceFlag)),
)
CollisionDetectionRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
CollisionDetectionSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ActivateMonitoring', _iec.BOOL),
    _iec.IecField('UnitLimitAxis', _iec.USINT),
    _iec.IecField('ThresholdMode', _iec.EnumType(_e.ThresholdMode)),
    _iec.IecField('ReactionMode', _iec.EnumType(_e.CollisionReactionMode)),
    _iec.IecField('Sensitivity', _iec.INT),
    _iec.IecField('SensitivityAxis', _iec.ArrayType(0, 6, _iec.INT)),
    _iec.IecField('LimitAxis', _iec.ArrayType(0, 6, _iec.REAL)),
)
ExchangeConfigurationOutCmd._IEC_FIELDS_ = (
    _iec.IecField('LengthACR', _iec.UINT),
    _iec.IecField('HighestToolIndex', _iec.USINT),
    _iec.IecField('HighestFrameIndex', _iec.USINT),
    _iec.IecField('HighestLoadIndex', _iec.USINT),
    _iec.IecField('HighestWorkAreaIndex', _iec.USINT),
    _iec.IecField('DataInSync', _iec.StructType(DataInSync)),
    _iec.IecField('ChangeIndexTool', _iec.USINT),
    _iec.IecField('ChangeIndexFrame', _iec.USINT),
    _iec.IecField('ChangeIndexLoad', _iec.USINT),
    _iec.IecField('ChangeIndexWorkArea', _iec.USINT),
    _iec.IecField('RAWorkingHours', _iec.UDINT),
    _iec.IecField('BrakeTestRequired', _iec.BOOL),
    _iec.IecField('StepModeExactStopActive', _iec.BOOL),
    _iec.IecField('StepModeBlendingActive', _iec.BOOL),
    _iec.IecField('PathAccuracyMode', _iec.BOOL),
    _iec.IecField('AvoidSingularity', _iec.BOOL),
    _iec.IecField('CollisionDetectionEnabled', _iec.BOOL),
    _iec.IecField('AcceleratingSupported', _iec.BOOL),
    _iec.IecField('DecceleratingSupported', _iec.BOOL),
    _iec.IecField('ConstantVelocitySupported', _iec.BOOL),
    _iec.IecField('RCWorkingHours', _iec.UDINT),
)
ExchangeConfigurationParCmd._IEC_FIELDS_ = (
    _iec.IecField('LogLevel', _iec.EnumType(_e.Severity)),
    _iec.IecField('WaitAtBlendingZone', _iec.BOOL),
    _iec.IecField('AllowSecSeqWhileSubprogram', _iec.BOOL),
    _iec.IecField('AllowDynamicBlending', _iec.BOOL),
    _iec.IecField('DelayTime', _iec.UINT),
    _iec.IecField('WaitForNrOfCmd', _iec.UINT),
    _iec.IecField('LifeSignTimeOut', _iec.UINT),
    _iec.IecField('SyncDelay', _iec.UINT),
    _iec.IecField('SyncReaction', _iec.EnumType(_e.SyncReaction)),
    _iec.IecField('DataInSync', _iec.StructType(DataInSync)),
    _iec.IecField('DataEnableSync', _iec.StructType(DataEnableSync)),
)
ExchangeConfigurationRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BOOL),
    _iec.IecField('Reserve1', _iec.BYTE),
    _iec.IecField('LengthACR', _iec.UINT),
    _iec.IecField('HighestToolIndex', _iec.USINT),
    _iec.IecField('HighestFrameIndex', _iec.USINT),
    _iec.IecField('HighestLoadIndex', _iec.USINT),
    _iec.IecField('HighestWorkAreaIndex', _iec.USINT),
    _iec.IecField('DataInSync', _iec.StructType(DataInSync)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('ChangeIndexTool', _iec.USINT),
    _iec.IecField('ChangeIndexFrame', _iec.USINT),
    _iec.IecField('ChangeIndexLoad', _iec.USINT),
    _iec.IecField('ChangeIndexWorkArea', _iec.USINT),
    _iec.IecField('RAWorkingHours', _iec.UDINT),
    _iec.IecField('StatusByte', _iec.BYTE),
    _iec.IecField('ConstantVelocitySupported', _iec.BOOL),
    _iec.IecField('RCWorkingHours', _iec.UDINT),
)
ExchangeConfigurationSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('LogLevel', _iec.EnumType(_e.Severity)),
    _iec.IecField('CtrlByte', _iec.BYTE),
    _iec.IecField('DelayTime', _iec.UINT),
    _iec.IecField('WaitForNrOfCmd', _iec.UINT),
    _iec.IecField('LifeSignTimeOut', _iec.UINT),
    _iec.IecField('SyncDelay', _iec.UINT),
    _iec.IecField('SyncReaction', _iec.EnumType(_e.SyncReaction)),
    _iec.IecField('Reserve1', _iec.BYTE),
    _iec.IecField('DataInSync', _iec.StructType(DataInSync)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('DataEnableSync', _iec.StructType(DataEnableSync)),
    _iec.IecField('Reserve3', _iec.BYTE),
)
FreeDriveOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Enabled', _iec.BOOL),
)
FreeDriveParCmd._IEC_FIELDS_ = (
)
FreeDriveRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BOOL),
)
FreeDriveSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Enable', _iec.BOOL),
)
MeasuringInputOutCmd._IEC_FIELDS_ = (
    _iec.IecField('MeasuringID', _iec.UINT),
    _iec.IecField('Measurings', _iec.ArrayType(1, 2, _iec.StructType(MeasuringInputResult))),
)
MeasuringInputParCmd._IEC_FIELDS_ = (
    _iec.IecField('MeasuringMode', _iec.EnumType(_e.MeasuringIoMode)),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('BitNumber', _iec.USINT),
)
MeasuringInputRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('MeasuringID', _iec.UINT),
    _iec.IecField('Measurings', _iec.ArrayType(1, 2, _iec.StructType(MeasuringInputResult))),
)
MeasuringInputSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('MeasuringMode', _iec.EnumType(_e.MeasuringIoMode)),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('BitNumber', _iec.USINT),
)
OpenBrakeOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Enabled', _iec.BOOL),
    _iec.IecField('RobotAxesBrakeReleased', _iec.StructType(RobotAxesFlags)),
    _iec.IecField('ExternalAxesBrakeReleased', _iec.StructType(ExternalAxesFlags)),
)
OpenBrakeParCmd._IEC_FIELDS_ = (
    _iec.IecField('RobotAxesBrakeRelease', _iec.StructType(RobotAxesFlags)),
    _iec.IecField('ExternalAxesBrakeRelease', _iec.StructType(ExternalAxesFlags)),
)
OpenBrakeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BYTE),
    _iec.IecField('RobotAxesBrakeReleased', _iec.BYTE),
    _iec.IecField('ExternalAxesBrakeReleased', _iec.BYTE),
)
OpenBrakeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('RobotAxesBrakeRelease', _iec.BYTE),
    _iec.IecField('ExternalAxesBrakeRelease', _iec.BYTE),
)
PathAccuracyModeOutCmd._IEC_FIELDS_ = (
)
PathAccuracyModeParCmd._IEC_FIELDS_ = (
)
PathAccuracyModeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BOOL),
)
PathAccuracyModeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Enable', _iec.BOOL),
)
ReadCallSubprogramCyclicOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Data', _iec.ArrayType(0, 25, _iec.BYTE)),
)
ReadCallSubprogramCyclicParCmd._IEC_FIELDS_ = (
)
ShiftPositionOutCmd._IEC_FIELDS_ = (
    _iec.IecField('TransformedPosition', _iec.StructType(RobotCartesianPosition)),
)
ShiftPositionParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.TransformMode)),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('TargetFrameNo', _iec.USINT),
    _iec.IecField('TransformationParameter_1', _iec.StructType(FrameData)),
    _iec.IecField('TransformationParameter_2', _iec.EnumType(_e.ReferenceElement)),
    _iec.IecField('RotationAngle', _iec.REAL),
)
ShiftPositionRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('TransformedPosition', _iec.StructType(RobotCartesianPosition)),
)
ShiftPositionSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('TransformationParameter_1', _iec.StructType(FrameData)),
    _iec.IecField('TransformationParameter_2', _iec.EnumType(_e.ReferenceElement)),
    _iec.IecField('RotationAngle', _iec.REAL),
    _iec.IecField('Mode', _iec.EnumType(_e.TransformMode)),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('TargetFrameNo', _iec.USINT),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
)
SoftSwitchTcpOutCmd._IEC_FIELDS_ = (
    _iec.IecField('SoftMovement', _iec.BOOL),
)
SoftSwitchTcpParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('ReferenceNo', _iec.USINT),
    _iec.IecField('CompliantAxes', _iec.BYTE),
    _iec.IecField('LimitMode', _iec.EnumType(_e.LimitMode)),
    _iec.IecField('ResistanceForceMode', _iec.EnumType(_e.ResistanceForceMode)),
    _iec.IecField('ResistanceForceTCP', _iec.REAL),
    _iec.IecField('ResistanceForceAxis', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('VectorData', _iec.ArrayType(0, 5, _iec.REAL)),
)
SoftSwitchTcpRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('SoftMovement', _iec.BOOL),
)
SoftSwitchTcpSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('LimitMode', _iec.EnumType(_e.LimitMode)),
    _iec.IecField('CompliantAxes', _iec.BYTE),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('ReferenceNo', _iec.USINT),
    _iec.IecField('ResistanceForceTCP', _iec.INT),
    _iec.IecField('ResistanceForceAxis', _iec.ArrayType(0, 5, _iec.UINT)),
    _iec.IecField('VectorData', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ResistanceForceMode', _iec.EnumType(_e.ResistanceForceMode)),
)
StopSubprogramOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
StopSubprogramParCmd._IEC_FIELDS_ = (
    _iec.IecField('StopMode', _iec.EnumType(_e.StopMode)),
    _iec.IecField('TargetID', _iec.DINT),
    _iec.IecField('SequenceFlag', _iec.EnumType(_e.SequenceFlag)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
StopSubprogramRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
StopSubprogramSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('TargetID', _iec.UINT),
    _iec.IecField('StopMode', _iec.USINT),
)
UnitMeasurementOutCmd._IEC_FIELDS_ = (
    _iec.IecField('MeasurementActive', _iec.BOOL),
    _iec.IecField('Result', _iec.REAL),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
UnitMeasurementParCmd._IEC_FIELDS_ = (
    _iec.IecField('TriggerMode', _iec.EnumType(_e.TriggerModeMeasurement)),
    _iec.IecField('NewMeasurement', _iec.BOOL),
    _iec.IecField('MeasuringMode', _iec.EnumType(_e.MeasuringUnitMode)),
    _iec.IecField('ListenerID', _iec.SINT),
)
UnitMeasurementRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Result', _iec.REAL),
    _iec.IecField('MeasurementActive', _iec.BOOL),
    _iec.IecField('ResultNo', _iec.USINT),
)
UnitMeasurementSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('TriggerMode', _iec.EnumType(_e.TriggerModeMeasurement)),
    _iec.IecField('MeasurementNo', _iec.USINT),
    _iec.IecField('MeasuringMode', _iec.EnumType(_e.MeasuringUnitMode)),
)
WriteCallSubprogramCyclicOutCmd._IEC_FIELDS_ = (
)
WriteCallSubprogramCyclicParCmd._IEC_FIELDS_ = (
    _iec.IecField('Data', _iec.ArrayType(0, 25, _iec.BYTE)),
)
MoveApproachDirectOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveApproachDirectParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveApproachDirectRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveApproachDirectSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveApproachLinearOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveApproachLinearParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveApproachLinearRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveApproachLinearSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveAxesRelativeOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveAxesRelativeParCmd._IEC_FIELDS_ = (
    _iec.IecField('JointDistance', _iec.StructType(RobotJointPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveAxesRelativeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
)
MoveAxesRelativeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('JointDistance', _iec.StructType(RobotJointPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveCircularAbsoluteOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveCircularAbsoluteParCmd._IEC_FIELDS_ = (
    _iec.IecField('CircMode', _iec.EnumType(_e.CircMode)),
    _iec.IecField('AuxPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('CircPlane', _iec.EnumType(_e.CircPlane)),
    _iec.IecField('Tolerance', _iec.REAL),
    _iec.IecField('EndPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Angle', _iec.REAL),
    _iec.IecField('PathChoice', _iec.EnumType(_e.PathChoice)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveCircularAbsoluteRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveCircularAbsoluteSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('EndPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('CircMode', _iec.EnumType(_e.CircMode)),
    _iec.IecField('CircPlane', _iec.EnumType(_e.CircPlane)),
    _iec.IecField('Tolerance', _iec.REAL),
    _iec.IecField('Angle', _iec.REAL),
    _iec.IecField('PathChoice', _iec.BOOL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveCircularCamOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveCircularCamParCmd._IEC_FIELDS_ = (
    _iec.IecField('CircMode', _iec.EnumType(_e.CircMode)),
    _iec.IecField('AuxPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('CircPlane', _iec.EnumType(_e.CircPlane)),
    _iec.IecField('Tolerance', _iec.REAL),
    _iec.IecField('EndPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Angle', _iec.REAL),
    _iec.IecField('PathChoice', _iec.EnumType(_e.PathChoice)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('OutputBitmask', _iec.BYTE),
    _iec.IecField('Value', _iec.BYTE),
    _iec.IecField('RelativePosition', _iec.BOOL),
    _iec.IecField('TriggerDelay', _iec.UINT),
    _iec.IecField('TriggerDistance', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
)
MoveCircularCamRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveCircularCamSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('EndPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('TriggerDelay', _iec.UINT),
    _iec.IecField('TriggerDistance', _iec.REAL),
    _iec.IecField('CircMode', _iec.EnumType(_e.CircMode)),
    _iec.IecField('CircPlane', _iec.EnumType(_e.CircPlane)),
    _iec.IecField('Tolerance', _iec.REAL),
    _iec.IecField('Angle', _iec.REAL),
    _iec.IecField('PathChoice', _iec.BOOL),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('RelativePosition', _iec.BOOL),
    _iec.IecField('OutputBitmask', _iec.BYTE),
    _iec.IecField('Value', _iec.BYTE),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveCircularRelativeOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveCircularRelativeParCmd._IEC_FIELDS_ = (
    _iec.IecField('CircMode', _iec.EnumType(_e.CircMode)),
    _iec.IecField('AuxPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('CircPlane', _iec.EnumType(_e.CircPlane)),
    _iec.IecField('Tolerance', _iec.REAL),
    _iec.IecField('EndPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Angle', _iec.REAL),
    _iec.IecField('PathChoice', _iec.EnumType(_e.PathChoice)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveCircularRelativeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveCircularRelativeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('EndPoint', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('CircMode', _iec.EnumType(_e.CircMode)),
    _iec.IecField('CircPlane', _iec.EnumType(_e.CircPlane)),
    _iec.IecField('Tolerance', _iec.REAL),
    _iec.IecField('Angle', _iec.REAL),
    _iec.IecField('PathChoice', _iec.BOOL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.BOOL),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveDepartDirectOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveDepartDirectParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveDepartDirectRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveDepartDirectSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('ReferenceType', _iec.BOOL),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveDepartLinearOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveDepartLinearParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveDepartLinearRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveDepartLinearSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(AuxOffset)),
    _iec.IecField('AuxCornerDistance', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('ReferenceType', _iec.BOOL),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveDirectOffsetOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveDirectOffsetParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferencePosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveDirectOffsetRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveDirectOffsetSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('ReferencePosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveDirectRelativeOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveDirectRelativeParCmd._IEC_FIELDS_ = (
    _iec.IecField('Distance', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveDirectRelativeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveDirectRelativeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Distance', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve3', _iec.BYTE),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveLinearAbsoluteJOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveLinearAbsoluteJParCmd._IEC_FIELDS_ = (
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveLinearAbsoluteJRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveLinearAbsoluteJSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveLinearCamOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveLinearCamParCmd._IEC_FIELDS_ = (
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('OutputBitmask', _iec.BYTE),
    _iec.IecField('Value', _iec.BYTE),
    _iec.IecField('RelativePosition', _iec.BOOL),
    _iec.IecField('TriggerDelay', _iec.UINT),
    _iec.IecField('TriggerDistance', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
)
MoveLinearCamRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveLinearCamSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('TriggerDelay', _iec.UINT),
    _iec.IecField('TriggerDistance', _iec.REAL),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('RelativePosition', _iec.BOOL),
    _iec.IecField('OutputBitmask', _iec.BYTE),
    _iec.IecField('Value', _iec.BYTE),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('TurnMode', _iec.USINT),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveLinearOffsetOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveLinearOffsetParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferencePosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveLinearOffsetRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveLinearOffsetSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('ReferencePosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveLinearRelativeOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveLinearRelativeParCmd._IEC_FIELDS_ = (
    _iec.IecField('Distance', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveLinearRelativeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveLinearRelativeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Distance', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MovePickPlaceDirectOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MovePickPlaceDirectParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ApproachOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('DepartOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('AuxCornerDistance_1', _iec.REAL),
    _iec.IecField('AuxCornerDistance_2', _iec.REAL),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('ReductionRate', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MovePickPlaceDirectRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MovePickPlaceDirectSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ApproachOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('DepartOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('AuxCornerDistance_1', _iec.REAL),
    _iec.IecField('AuxCornerDistance_2', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MovePickPlaceLinearOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MovePickPlaceLinearParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ApproachOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('DepartOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('AuxCornerDistance_1', _iec.REAL),
    _iec.IecField('AuxCornerDistance_2', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MovePickPlaceLinearRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MovePickPlaceLinearSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('TargetPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ApproachOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('DepartOffset', _iec.StructType(AuxOffset)),
    _iec.IecField('AuxCornerDistance_1', _iec.REAL),
    _iec.IecField('AuxCornerDistance_2', _iec.REAL),
    _iec.IecField('VelocityCoefficient', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('MoveTime', _iec.UINT),
)
ChangeSpeedOverrideOutCmd._IEC_FIELDS_ = (
)
ChangeSpeedOverrideParCmd._IEC_FIELDS_ = (
    _iec.IecField('Override', _iec.REAL),
)
ChangeSpeedOverrideRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
ChangeSpeedOverrideSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Override', _iec.UINT),
)
GroupContinueOutCmd._IEC_FIELDS_ = (
)
GroupContinueParCmd._IEC_FIELDS_ = (
)
GroupContinueRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
GroupContinueSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
GroupInterruptOutCmd._IEC_FIELDS_ = (
)
GroupInterruptParCmd._IEC_FIELDS_ = (
)
GroupInterruptRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
GroupInterruptSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
GroupJogOutCmd._IEC_FIELDS_ = (
    _iec.IecField('DistanceReached', _iec.BOOL),
    _iec.IecField('MotionActive', _iec.BOOL),
)
GroupJogParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.JogMode)),
    _iec.IecField('Override', _iec.UINT),
    _iec.IecField('Control', _iec.StructType(JogControl)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('IncrementalTranslation', _iec.REAL),
    _iec.IecField('IncrementalRotation', _iec.REAL),
)
GroupJogRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Status', _iec.BYTE),
)
GroupJogSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Enable', _iec.BOOL),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('Mode', _iec.EnumType(_e.JogMode)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('IncrementalTranslation', _iec.REAL),
    _iec.IecField('IncrementalRotation', _iec.REAL),
    _iec.IecField('Override', _iec.UINT),
    _iec.IecField('JogControl', _iec.ArrayType(0, 2, _iec.BYTE)),
)
GroupStopOutCmd._IEC_FIELDS_ = (
)
GroupStopParCmd._IEC_FIELDS_ = (
)
GroupStopRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
GroupStopSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
MoveAxesAbsoluteOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveAxesAbsoluteParCmd._IEC_FIELDS_ = (
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveAxesAbsoluteRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
)
MoveAxesAbsoluteSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveDirectAbsoluteOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveDirectAbsoluteParCmd._IEC_FIELDS_ = (
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveDirectAbsoluteRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveDirectAbsoluteSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('Reserve3', _iec.BYTE),
    _iec.IecField('Reserve4', _iec.BYTE),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveLinearAbsoluteOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('FollowID', _iec.DINT),
)
MoveLinearAbsoluteParCmd._IEC_FIELDS_ = (
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveLinearAbsoluteRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveLinearAbsoluteSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('Reserve3', _iec.BYTE),
    _iec.IecField('MoveTime', _iec.UINT),
)
ReturnToPrimaryOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('PrimaryPosToolNo', _iec.USINT),
    _iec.IecField('PrimaryPosFrameNo', _iec.USINT),
)
ReturnToPrimaryParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReturnMode', _iec.EnumType(_e.ReturnMode)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('DistanceLimit', _iec.REAL),
    _iec.IecField('TrajectoryMode', _iec.EnumType(_e.TrajectoryMode)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('AllowDifferences', _iec.BOOL),
)
ReturnToPrimaryRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('PrimaryPosToolNo', _iec.USINT),
    _iec.IecField('PrimaryPosFrameNo', _iec.USINT),
)
ReturnToPrimarySendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('DistanceLimit', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('MoveTime', _iec.UINT),
    _iec.IecField('ReturnMode', _iec.BOOL),
    _iec.IecField('TrajectoryMode', _iec.BOOL),
    _iec.IecField('Enable', _iec.BOOL),
    _iec.IecField('AllowDifferences', _iec.BOOL),
)
CalculateCartesianPositionOutCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetToolNoReturn', _iec.USINT),
    _iec.IecField('TargetFrameNoReturn', _iec.USINT),
    _iec.IecField('CartesianPositionReturn', _iec.StructType(RobotCartesianPosition)),
)
CalculateCartesianPositionParCmd._IEC_FIELDS_ = (
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('TargetFrameNo', _iec.USINT),
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
)
CalculateCartesianPositionRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('TargetToolNoReturn', _iec.USINT),
    _iec.IecField('TargetFrameNoReturn', _iec.USINT),
    _iec.IecField('CartesianPositionReturn', _iec.StructType(RobotCartesianPosition)),
)
CalculateCartesianPositionSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('TargetFrameNo', _iec.USINT),
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
)
CalculateForwardKinematicOutCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetToolNoReturn', _iec.USINT),
    _iec.IecField('TargetFrameNoReturn', _iec.USINT),
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
)
CalculateForwardKinematicParCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
)
CalculateForwardKinematicRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('TargetToolNoReturn', _iec.USINT),
    _iec.IecField('TargetFrameNoReturn', _iec.USINT),
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
)
CalculateForwardKinematicSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
)
CalculateFrameOutCmd._IEC_FIELDS_ = (
    _iec.IecField('IEC_Date', _iec.UINT),
    _iec.IecField('IEC_TIME', _iec.TOD),
    _iec.IecField('ReferenceFrame', _iec.USINT),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPositionBase)),
)
CalculateFrameParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.FrameCalculationMode)),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('Position_X', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Position_XY', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('Origin', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('OriginShift', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceFrame', _iec.USINT),
)
CalculateFrameRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('IEC_Date', _iec.UINT),
    _iec.IecField('IEC_TIME', _iec.TOD),
    _iec.IecField('ReferenceFrame', _iec.USINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPositionBase)),
)
CalculateFrameSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('DataIndex', _iec.USINT),
    _iec.IecField('DataComplete', _iec.BYTE),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ReferenceFrame', _iec.USINT),
    _iec.IecField('Mode', _iec.SINT),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
)
CalculateInverseKinematicOutCmd._IEC_FIELDS_ = (
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
)
CalculateInverseKinematicParCmd._IEC_FIELDS_ = (
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
)
CalculateInverseKinematicRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
)
CalculateInverseKinematicSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
)
CalculateToolOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolData', _iec.StructType(ToolData)),
    _iec.IecField('TCPMaxError', _iec.REAL),
    _iec.IecField('TCPMeanError', _iec.REAL),
)
CalculateToolParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.ToolCalculationMode)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ExternalTCP', _iec.BOOL),
    _iec.IecField('PositionsArray', _iec.ArrayType(0, 5, _iec.StructType(RobotCartesianPosition))),
)
CalculateToolRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('TCPMaxError', _iec.REAL),
    _iec.IecField('TCPMeanError', _iec.REAL),
    _iec.IecField('ToolData', _iec.StructType(ToolData)),
)
CalculateToolSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('DataIndex', _iec.USINT),
    _iec.IecField('DataComplete', _iec.BYTE),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('Mode', _iec.EnumType(_e.ToolCalculationMode)),
    _iec.IecField('ExternalTCP', _iec.USINT),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
)
LoadMeasurementAutomaticOutCmd._IEC_FIELDS_ = (
    _iec.IecField('MeasuringID', _iec.UINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
    _iec.IecField('LoadDataAvailable', _iec.BOOL),
)
LoadMeasurementAutomaticParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.LoadMeasurementMode)),
    _iec.IecField('Mass', _iec.REAL),
    _iec.IecField('Area_J3', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Area_J4', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Area_J5', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Area_J6', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Position_1', _iec.StructType(RobotJointPosition)),
    _iec.IecField('Position_2', _iec.StructType(RobotJointPosition)),
    _iec.IecField('ConfigurationAngle', _iec.REAL),
)
LoadMeasurementAutomaticRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('MeasuringID', _iec.UINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
    _iec.IecField('LoadDataAvailable', _iec.BOOL),
)
LoadMeasurementAutomaticSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Mass', _iec.REAL),
    _iec.IecField('Mode', _iec.EnumType(_e.LoadMeasurementMode)),
    _iec.IecField('Reserved', _iec.BYTE),
    _iec.IecField('Area_J3', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Area_J4', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Area_J5', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('Area_J6', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('ConfigurationAngle', _iec.REAL),
    _iec.IecField('Position_1', _iec.StructType(RobotJointPosition)),
    _iec.IecField('Position_2', _iec.StructType(RobotJointPosition)),
)
LoadMeasurementSequentialOutCmd._IEC_FIELDS_ = (
    _iec.IecField('MeasuringID', _iec.UINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
    _iec.IecField('LoadDataAvailable', _iec.BOOL),
)
LoadMeasurementSequentialParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.LoadMeasurementSteps)),
    _iec.IecField('Mass', _iec.REAL),
)
LoadMeasurementSequentialRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('MeasuringID', _iec.UINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
    _iec.IecField('LoadDataAvailable', _iec.BOOL),
)
LoadMeasurementSequentialSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Mass', _iec.REAL),
    _iec.IecField('Mode', _iec.EnumType(_e.LoadMeasurementSteps)),
)
ActivateConveyorTrackingOutCmd._IEC_FIELDS_ = (
    _iec.IecField('TrackingStatus', _iec.StructType(TrackingStatus)),
    _iec.IecField('RCEncoderValue', _iec.REAL),
)
ActivateConveyorTrackingParCmd._IEC_FIELDS_ = (
    _iec.IecField('ConveyorNo', _iec.SINT),
    _iec.IecField('ConnectionMode', _iec.EnumType(_e.ConnectionMode)),
    _iec.IecField('PLCEncoderValue', _iec.REAL),
)
ActivateConveyorTrackingRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('TrackingStatus', _iec.StructType(TrackingStatus)),
)
ActivateConveyorTrackingSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ConveyorNo', _iec.SINT),
    _iec.IecField('ConnectionMode', _iec.SINT),
)
ConfigureConveyorOutCmd._IEC_FIELDS_ = (
)
ConfigureConveyorParCmd._IEC_FIELDS_ = (
    _iec.IecField('ConveyorNo', _iec.USINT),
    _iec.IecField('ConveyorOrigin', _iec.StructType(FrameData)),
    _iec.IecField('ConveyorType', _iec.EnumType(_e.ConveyorType)),
    _iec.IecField('Radius', _iec.REAL),
    _iec.IecField('StartDistance', _iec.REAL),
    _iec.IecField('EndDistance', _iec.REAL),
    _iec.IecField('SyncInLength', _iec.REAL),
    _iec.IecField('SyncOutLength', _iec.REAL),
)
ConfigureConveyorRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
ConfigureConveyorSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ConveyorOrigin', _iec.StructType(FrameData)),
    _iec.IecField('ConveyorOriginAvailable', _iec.BOOL),
    _iec.IecField('ConveyorNo', _iec.USINT),
    _iec.IecField('ConveyorType', _iec.EnumType(_e.ConveyorType)),
    _iec.IecField('Radius', _iec.REAL),
    _iec.IecField('StartDistance', _iec.REAL),
    _iec.IecField('EndDistance', _iec.REAL),
    _iec.IecField('SyncInLength', _iec.REAL),
    _iec.IecField('SyncOutLength', _iec.REAL),
)
RedefineTrackingPosOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
RedefineTrackingPosParCmd._IEC_FIELDS_ = (
    _iec.IecField('ConveyorNo', _iec.USINT),
    _iec.IecField('InitObjectPosition', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('TrackingOffset', _iec.REAL),
    _iec.IecField('StartIndexInitPosition', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('IndexTrackingOffset', _iec.USINT),
    _iec.IecField('ListenerID', _iec.SINT),
)
RedefineTrackingPosRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserved', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
RedefineTrackingPosSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ConveyorNo', _iec.USINT),
    _iec.IecField('StartIndexInitPosition', _iec.USINT),
    _iec.IecField('TrackingOffset', _iec.REAL),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('IndexTrackingOffset', _iec.USINT),
)
SyncToConveyorOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InSync', _iec.BOOL),
)
SyncToConveyorParCmd._IEC_FIELDS_ = (
    _iec.IecField('ConveyorNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('SyncInMode', _iec.EnumType(_e.SyncInMode)),
    _iec.IecField('SyncInParameter', _iec.REAL),
    _iec.IecField('MaxVelocity', _iec.REAL),
    _iec.IecField('MaxAcceleration', _iec.REAL),
    _iec.IecField('ListenerID', _iec.SINT),
)
SyncToConveyorRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserved', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InSync', _iec.BOOL),
)
SyncToConveyorSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ConveyorNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('SyncInMode', _iec.EnumType(_e.SyncInMode)),
    _iec.IecField('SyncInParameter', _iec.REAL),
    _iec.IecField('MaxVelocity', _iec.REAL),
    _iec.IecField('MaxAcceleration', _iec.REAL),
)
ForceControlOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ForceStatus', _iec.StructType(ForceStatus)),
)
ForceControlParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('SensorValue', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('TargetValue', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ConnectionMode', _iec.EnumType(_e.SensorConnectionMode)),
    _iec.IecField('SensorFrame', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('CalibrationData', _iec.USINT),
    _iec.IecField('TargetWindow', _iec.REAL),
    _iec.IecField('CompliantAxes', _iec.BYTE),
    _iec.IecField('MaxVelocity', _iec.UINT),
    _iec.IecField('MaxDeviation', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ErrorReaction', _iec.EnumType(_e.ErrorReaction)),
    _iec.IecField('ErrorReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('ErrorVector', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ErrorToolNo', _iec.USINT),
    _iec.IecField('ErrorFrameNo', _iec.USINT),
    _iec.IecField('FixedSensor', _iec.BOOL),
)
ForceControlRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('ForceStatus', _iec.BYTE),
)
ForceControlSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ConnectionMode', _iec.EnumType(_e.SensorConnectionMode)),
    _iec.IecField('FixedSensor', _iec.BYTE),
    _iec.IecField('SensorFrame', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('CalibrationData', _iec.USINT),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('SensorValue', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('TargetValue', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('MaxVelocity', _iec.UINT),
    _iec.IecField('MaxDeviation', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ErrorReaction', _iec.EnumType(_e.ErrorReaction)),
    _iec.IecField('ErrorReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('ErrorVector', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ErrorToolNo', _iec.USINT),
    _iec.IecField('ErrorFrameNo', _iec.USINT),
    _iec.IecField('CompliantAxes', _iec.BYTE),
)
ForceLimitOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ForceStatus', _iec.StructType(ForceStatus)),
    _iec.IecField('FollowID', _iec.DINT),
)
ForceLimitParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('SensorValue', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ForceLimit', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ConnectionMode', _iec.EnumType(_e.ConnectionMode)),
    _iec.IecField('SensorFrame', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('CalibrationData', _iec.USINT),
    _iec.IecField('FixedSensor', _iec.BOOL),
    _iec.IecField('EmitterID', _iec.SINT),
)
ForceLimitRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserved', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('ForceStatus', _iec.BYTE),
)
ForceLimitSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ConnectionMode', _iec.USINT),
    _iec.IecField('FixedSensor', _iec.BYTE),
    _iec.IecField('SensorFrame', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('CalibrationData', _iec.USINT),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('SensorValue', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ForceLimit', _iec.ArrayType(0, 5, _iec.REAL)),
)
ReadActualForceOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ActualForce', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
ReadActualForceParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('CalibrationData', _iec.USINT),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadActualForceRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserved', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('ActualForce', _iec.ArrayType(0, 5, _iec.REAL)),
)
ReadActualForceSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('CalibrationData', _iec.USINT),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
)
EnableRobotOutCmd._IEC_FIELDS_ = (
)
EnableRobotParCmd._IEC_FIELDS_ = (
    _iec.IecField('HoldToRun', _iec.BOOL),
    _iec.IecField('StepMode', _iec.EnumType(_e.StepMode)),
    _iec.IecField('ManualStep', _iec.BOOL),
)
EnableRobotRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BOOL),
)
EnableRobotSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Enable', _iec.BOOL),
    _iec.IecField('HoldToRun', _iec.BOOL),
    _iec.IecField('StepMode', _iec.EnumType(_e.StepMode)),
    _iec.IecField('ManualStep', _iec.BOOL),
)
GroupResetOutCmd._IEC_FIELDS_ = (
)
GroupResetParCmd._IEC_FIELDS_ = (
)
GroupResetRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
GroupResetSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
RestartControllerOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RestartAccepted', _iec.BOOL),
)
RestartControllerParCmd._IEC_FIELDS_ = (
)
RestartControllerRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('RestartAccepted', _iec.BOOL),
)
RestartControllerSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
RobotTaskParCfgCom._IEC_FIELDS_ = (
    _iec.IecField('LifeSignTimeOut', _iec.TIME),
    _iec.IecField('TelegramLengthPlcToRob', _iec.UINT),
    _iec.IecField('TelegramLengthRobToPlc', _iec.UINT),
    _iec.IecField('TwoSequences', _iec.BOOL),
)
RobotTaskParCfgPlc._IEC_FIELDS_ = (
    _iec.IecField('CycleTime', _iec.TIME),
    _iec.IecField('Parameter', _iec.StructType(RobotTaskParCfgPlcParameter)),
    _iec.IecField('OptionalCyclic', _iec.StructType(AxesGroupParameterPlcOptionalCyclic)),
)
AxesGroupParameterPlcParameter._IEC_FIELDS_ = (
    _iec.IecField('ManufacturedID', _iec.UINT),
    _iec.IecField('OrderID', _iec.StringType(20)),
    _iec.IecField('SerialNumber', _iec.StringType(16)),
    _iec.IecField('FirmwareVersion', _iec.StringType(8)),
    _iec.IecField('InterfaceVersion', _iec.StringType(8)),
    _iec.IecField('SynchronizationModes', _iec.StructType(SynchronizationModes)),
    _iec.IecField('SyncUserInteraction', _iec.StructType(SyncUserInteraction)),
)
RobotTaskParCfgPlcParameter._IEC_FIELDS_ = AxesGroupParameterPlcParameter._IEC_FIELDS_ + (
)
RobotTaskParCfgRob._IEC_FIELDS_ = (
    _iec.IecField('Parameter', _iec.StructType(RobotTaskParCfgRobParameter)),
    _iec.IecField('OptionalCyclic', _iec.StructType(AxesGroupParameterRobOptionalCyclic)),
)
RobotTaskParCfgRobParameter._IEC_FIELDS_ = (
    _iec.IecField('WaitAtBlendingZone', _iec.BOOL),
    _iec.IecField('AllowSecSeqWhileSubprogram', _iec.BOOL),
    _iec.IecField('AllowDynamicBlending', _iec.BOOL),
    _iec.IecField('DelayTime', _iec.UINT),
    _iec.IecField('WaitForNrOfCmd', _iec.UINT),
    _iec.IecField('SyncDelay', _iec.UINT),
    _iec.IecField('SyncReaction', _iec.EnumType(_e.SyncReaction)),
    _iec.IecField('MessageLevel', _iec.EnumType(_e.MessageLevel)),
)
RobotTaskParCfg._IEC_FIELDS_ = (
    _iec.IecField('Com', _iec.StructType(RobotTaskParCfgCom)),
    _iec.IecField('Plc', _iec.StructType(RobotTaskParCfgPlc)),
    _iec.IecField('Rob', _iec.StructType(RobotTaskParCfgRob)),
)
SetOperationModeOutCmd._IEC_FIELDS_ = (
)
SetOperationModeParCmd._IEC_FIELDS_ = (
    _iec.IecField('OperationMode', _iec.EnumType(_e.OperationMode)),
)
SetOperationModeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
SetOperationModeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('OperationMode', _iec.USINT),
)
SetSequenceOutCmd._IEC_FIELDS_ = (
)
SetSequenceParCmd._IEC_FIELDS_ = (
    _iec.IecField('TargetSequence', _iec.EnumType(_e.SequenceFlag)),
)
SetSequenceRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
SetSequenceSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('TargetSequence', _iec.USINT),
)
SwitchLanguageOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ActualLanguageCode', _iec.StringType(2)),
)
SwitchLanguageParCmd._IEC_FIELDS_ = (
    _iec.IecField('LanguageCode', _iec.StringType(2)),
)
SwitchLanguageRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('ActualLanguageCode', _iec.StringType(2)),
)
SwitchLanguageSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('LanguageCode', _iec.StringType(2)),
)
UserLoginOutCmd._IEC_FIELDS_ = (
)
UserLoginParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.LogonMode)),
    _iec.IecField('Password', _iec.StringType(50)),
    _iec.IecField('Username', _iec.StringType(50)),
    _iec.IecField('LevelID', _iec.SINT),
)
UserLoginRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
UserLoginSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Mode', _iec.EnumType(_e.LogonMode)),
    _iec.IecField('LevelID', _iec.SINT),
    _iec.IecField('Password', _iec.StringType(50)),
    _iec.IecField('Username', _iec.StringType(50)),
)
ReadActualPositionOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('ToolNoReturn', _iec.INT),
    _iec.IecField('FrameNoReturn', _iec.INT),
    _iec.IecField('ActualCartesianPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ActualJointPosition', _iec.StructType(RobotJointPosition)),
)
ReadActualPositionParCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.INT),
    _iec.IecField('FrameNo', _iec.INT),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadActualPositionRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('ToolNoReturn', _iec.INT),
    _iec.IecField('FrameNoReturn', _iec.INT),
    _iec.IecField('ActualCartesianPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ActualJointPosition', _iec.StructType(RobotJointPosition)),
)
ReadActualPositionSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
)
ReadActualPositionCyclicOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ReadingCartesianPosition', _iec.BOOL),
    _iec.IecField('ReadingCartesianPositionExt', _iec.BOOL),
    _iec.IecField('ReadingJointPosition', _iec.BOOL),
    _iec.IecField('ReadingJointPositionExt', _iec.BOOL),
    _iec.IecField('CurrentCoordinateSystem', _iec.StructType(CoordinateSystem)),
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('CartesianPositionShort', _iec.StructType(RobotCartesianPositionShort)),
    _iec.IecField('CartesianPositionExt', _iec.StructType(RobotCartesianPositionExt)),
    _iec.IecField('CoordinateSystem', _iec.StructType(CoordinateSystem)),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('JointPositionShort', _iec.StructType(RobotJointPositionShort)),
    _iec.IecField('JointPositionExt', _iec.StructType(RobotJointPositionExt)),
)
ReadActualPositionCyclicParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReadCartesianPosition', _iec.BOOL),
    _iec.IecField('ReadCartesianPositionExt', _iec.BOOL),
    _iec.IecField('ToolNo', _iec.INT),
    _iec.IecField('FrameNo', _iec.INT),
    _iec.IecField('ReadJointPosition', _iec.BOOL),
    _iec.IecField('ReadJointPositionExt', _iec.BOOL),
)
ReadActualTCPVelocityOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ActualTCPVelocity', _iec.REAL),
    _iec.IecField('ToolNoReturn', _iec.USINT),
    _iec.IecField('FrameNoReturn', _iec.USINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
ReadActualTCPVelocityParCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadActualTCPVelocityRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('ActualTCPVelocity', _iec.REAL),
    _iec.IecField('ToolNoReturn', _iec.USINT),
    _iec.IecField('FrameNoReturn', _iec.USINT),
)
ReadActualTCPVelocitySendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
)
ReadAnalogInputOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Unit', _iec.EnumType(_e.UnitType)),
    _iec.IecField('Value', _iec.REAL),
)
ReadAnalogInputParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadAnalogInputRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Unit', _iec.USINT),
    _iec.IecField('Value', _iec.REAL),
)
ReadAnalogInputSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.USINT),
)
ReadDHParameterOutCmd._IEC_FIELDS_ = (
    _iec.IecField('DHParameter', _iec.StructType(DHParameter)),
)
ReadDHParameterParCmd._IEC_FIELDS_ = (
    _iec.IecField('ModifiedConvention', _iec.BOOL),
)
ReadDHParameterRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('DHParameter', _iec.StructType(DHParameter)),
)
ReadDHParameterSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ModifiedConvention', _iec.BOOL),
)
ReadDigitalInputsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 4, _iec.BYTE)),
)
ReadDigitalInputsParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 4, _iec.USINT)),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadDigitalInputsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 4, _iec.BYTE)),
)
ReadDigitalInputsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.ArrayType(0, 4, _iec.USINT)),
)
ReadDigitalOutputsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 4, _iec.BYTE)),
)
ReadDigitalOutputsParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 4, _iec.USINT)),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadDigitalOutputsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 4, _iec.BYTE)),
)
ReadDigitalOutputsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.ArrayType(0, 4, _iec.USINT)),
)
ReadFrameDataOutCmd._IEC_FIELDS_ = (
    _iec.IecField('FrameNoReturn', _iec.USINT),
    _iec.IecField('FrameData', _iec.StructType(FrameData)),
)
ReadFrameDataParCmd._IEC_FIELDS_ = (
    _iec.IecField('FrameNo', _iec.INT),
)
ReadFrameDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('FrameNoReturn', _iec.USINT),
    _iec.IecField('FrameData', _iec.StructType(FrameData)),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadFrameDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('FrameNo', _iec.USINT),
)
ReadIntegersOutCmd._IEC_FIELDS_ = (
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.INT)),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
ReadIntegersParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadIntegersRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.INT)),
)
ReadIntegersSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
)
ReadLoadDataOutCmd._IEC_FIELDS_ = (
    _iec.IecField('LoadNoReturn', _iec.USINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
)
ReadLoadDataParCmd._IEC_FIELDS_ = (
    _iec.IecField('LoadNo', _iec.INT),
)
ReadLoadDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('LoadNoReturn', _iec.USINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadLoadDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('LoadNo', _iec.USINT),
)
ReadMessagesOutCmd._IEC_FIELDS_ = (
    _iec.IecField('MsgId', _iec.USINT),
    _iec.IecField('NumberOfActiveErrors', _iec.USINT),
    _iec.IecField('NumberOfActiveWarnings', _iec.USINT),
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('MsgType', _iec.EnumType(_e.MessageType)),
    _iec.IecField('Severity', _iec.EnumType(_e.Severity)),
    _iec.IecField('ErrorCode', _iec.DWORD),
    _iec.IecField('Text', _iec.StringType(255)),
)
ReadMessagesParCmd._IEC_FIELDS_ = (
    _iec.IecField('MsgID', _iec.USINT),
    _iec.IecField('MessageLevel', _iec.EnumType(_e.MessageLevel)),
)
ReadMessagesRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Enabled', _iec.BOOL),
    _iec.IecField('MsgId', _iec.USINT),
    _iec.IecField('NumberOfActiveErrors', _iec.USINT),
    _iec.IecField('NumberOfActiveWarnings', _iec.USINT),
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('MsgType', _iec.USINT),
    _iec.IecField('Severity', _iec.SINT),
    _iec.IecField('ErrorCode', _iec.DWORD),
    _iec.IecField('Text', _iec.StringType(255)),
)
ReadMessagesSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('MsgID', _iec.USINT),
    _iec.IecField('Enable', _iec.BOOL),
    _iec.IecField('MessageLevel', _iec.USINT),
)
ReadRealsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.REAL)),
)
ReadRealsParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadRealsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.REAL)),
)
ReadRealsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
)
ReadRobotDataOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RCManufacturer', _iec.StringType(20)),
    _iec.IecField('RCOrderID', _iec.StringType(20)),
    _iec.IecField('RCSerialNumber', _iec.StringType(16)),
    _iec.IecField('RASerialNumber', _iec.StringType(16)),
    _iec.IecField('RCFirmwareVersion', _iec.StringType(12)),
    _iec.IecField('RCInterpreterVersion', _iec.StringType(5)),
    _iec.IecField('AxisJointUsed', _iec.StructType(AxisJointUsed)),
    _iec.IecField('AxisExternalUsed', _iec.StructType(AxisExternalUsed)),
    _iec.IecField('AxisJointUnit', _iec.StructType(AxisJointUnit)),
    _iec.IecField('AxisExternalUnit', _iec.StructType(AxisExternalUnit)),
    _iec.IecField('RCSupportedFunctions', _iec.StructType(RCSupportedFunctions)),
    _iec.IecField('RobotID', _iec.StringType(16)),
    _iec.IecField('InterpreterCycleTime', _iec.UINT),
)
ReadRobotDataParCmd._IEC_FIELDS_ = (
)
ReadRobotDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('RCManufacturer', _iec.StringType(20)),
    _iec.IecField('RCOrderID', _iec.StringType(20)),
    _iec.IecField('RCSerialNumber', _iec.StringType(16)),
    _iec.IecField('RASerialNumber', _iec.StringType(16)),
    _iec.IecField('RCFirmwareVersion', _iec.StringType(12)),
    _iec.IecField('RCInterpreterVersion', _iec.StringType(5)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('AxisJointUsed', _iec.BYTE),
    _iec.IecField('AxisExternalUsed', _iec.BYTE),
    _iec.IecField('AxisJointUnit', _iec.BYTE),
    _iec.IecField('AxisExternalUnit', _iec.BYTE),
    _iec.IecField('RCSupportedFunctions', _iec.ArrayType(0, 18, _iec.BYTE)),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('RobotID', _iec.StringType(16)),
    _iec.IecField('InterpreterCycleTime', _iec.UINT),
)
ReadRobotDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
ReadRobotDefaultDynamicsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('DynamicValues', _iec.StructType(DefaultDynamics)),
)
ReadRobotDefaultDynamicsParCmd._IEC_FIELDS_ = (
)
ReadRobotDefaultDynamicsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadRobotDefaultDynamicsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
ReadRobotReferenceDynamicsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('DynamicValues', _iec.StructType(ReferenceDynamics)),
)
ReadRobotReferenceDynamicsParCmd._IEC_FIELDS_ = (
)
ReadRobotReferenceDynamicsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('VelocityReference', _iec.REAL),
    _iec.IecField('AccelerationReference', _iec.REAL),
    _iec.IecField('DecelerationReference', _iec.REAL),
    _iec.IecField('JerkReference', _iec.REAL),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadRobotReferenceDynamicsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
ReadRobotSWLimitsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('LimitValues', _iec.StructType(SWLimits)),
)
ReadRobotSWLimitsParCmd._IEC_FIELDS_ = (
)
ReadRobotSWLimitsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('LimitValues', _iec.StructType(SWLimits)),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadRobotSWLimitsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
)
ReadSystemVariableOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('DataType', _iec.ArrayType(0, 7, _iec.USINT)),
    _iec.IecField('Data_0', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_1', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_2', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_3', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_4', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_5', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_6', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_7', _iec.ArrayType(0, 3, _iec.BYTE)),
)
ReadSystemVariableParCmd._IEC_FIELDS_ = (
    _iec.IecField('RCParameter', _iec.BOOL),
    _iec.IecField('ParameterID', _iec.ArrayType(0, 7, _iec.UINT)),
    _iec.IecField('SubParameterID', _iec.ArrayType(0, 7, _iec.USINT)),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReadSystemVariableRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('DataType', _iec.ArrayType(0, 7, _iec.USINT)),
    _iec.IecField('Data_0', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_1', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_2', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_3', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_4', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_5', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_6', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_7', _iec.ArrayType(0, 3, _iec.BYTE)),
)
ReadSystemVariableSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('RCParameter', _iec.BOOL),
    _iec.IecField('ParameterID', _iec.ArrayType(0, 7, _iec.UINT)),
    _iec.IecField('SubParameterID', _iec.ArrayType(0, 7, _iec.USINT)),
)
ReadToolDataOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolNoReturn', _iec.USINT),
    _iec.IecField('ToolData', _iec.StructType(ToolData)),
)
ReadToolDataParCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.INT),
)
ReadToolDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ToolNoReturn', _iec.USINT),
    _iec.IecField('ToolData', _iec.StructType(ToolData)),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadToolDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('ToolNo', _iec.USINT),
)
SearchHardStopOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('InClamping', _iec.BOOL),
)
SearchHardStopParCmd._IEC_FIELDS_ = (
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('DetectionMode', _iec.EnumType(_e.DetectionMode)),
    _iec.IecField('DetectionVector', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('OriMode', _iec.EnumType(_e.OriMode)),
    _iec.IecField('ConfigMode', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnMode', _iec.EnumType(_e.TurnMode)),
    _iec.IecField('Manipulation', _iec.BOOL),
)
SearchHardStopRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('InClamping', _iec.BOOL),
)
SearchHardStopSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('DetectionMode', _iec.USINT),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('DetectionVector', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('ConfigMode', _iec.ArrayType(0, 1, _iec.BYTE)),
    _iec.IecField('TurnMode', _iec.USINT),
)
SearchHardStopJOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('InClamping', _iec.BOOL),
)
SearchHardStopJParCmd._IEC_FIELDS_ = (
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('DetectionMode', _iec.EnumType(_e.DetectionMode)),
    _iec.IecField('DetectionVector', _iec.ArrayType(0, 5, _iec.REAL)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('Manipulation', _iec.BOOL),
)
SearchHardStopJRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('InClamping', _iec.BOOL),
)
SearchHardStopJSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPosition)),
    _iec.IecField('OriMode', _iec.USINT),
    _iec.IecField('DetectionMode', _iec.USINT),
    _iec.IecField('Manipulation', _iec.BOOL),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('DetectionVector', _iec.ArrayType(0, 5, _iec.REAL)),
)
CreateSplineOutCmd._IEC_FIELDS_ = (
)
CreateSplineParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.SplineMode)),
    _iec.IecField('SplineID', _iec.SINT),
    _iec.IecField('SplineData', _iec.ArrayType(1, _iec.Param('SPLINE_DATA_MAX'), _iec.StructType(SplineData))),
)
CreateSplineRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
CreateSplineSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Mode', _iec.UINT),
    _iec.IecField('SplineID', _iec.SINT),
    _iec.IecField('SplineData', _iec.ArrayType(1, _iec.Param('SPLINE_DATA_MAX'), _iec.StructType(SplineDataSend))),
)
DeleteSplineOutCmd._IEC_FIELDS_ = (
)
DeleteSplineParCmd._IEC_FIELDS_ = (
    _iec.IecField('SplineID', _iec.SINT),
)
DeleteSplineRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
DeleteSplineSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('SplineID', _iec.SINT),
)
DynamicSplineOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('SegmentProgress', _iec.REAL),
    _iec.IecField('Buffered', _iec.INT),
    _iec.IecField('Calculated', _iec.INT),
    _iec.IecField('ActiveIndex', _iec.SINT),
    _iec.IecField('TrajectoryCompleted', _iec.BOOL),
)
DynamicSplineParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.SplineMode)),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
    _iec.IecField('SplineData', _iec.ArrayType(1, _iec.Param('SPLINE_DATA_MAX'), _iec.StructType(SplineData))),
    _iec.IecField('StartPosition', _iec.INT),
)
DynamicSplineRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('SegmentProgress', _iec.REAL),
    _iec.IecField('Buffered', _iec.INT),
    _iec.IecField('Calculated', _iec.INT),
    _iec.IecField('ActiveIndex', _iec.SINT),
    _iec.IecField('TrajectoryCompleted', _iec.BOOL),
)
DynamicSplineSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Mode', _iec.UINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.UINT),
    _iec.IecField('StartPosition', _iec.INT),
    _iec.IecField('SplineData', _iec.ArrayType(1, _iec.Param('SPLINE_DATA_MAX'), _iec.StructType(SplineDataSend))),
)
MoveSplineOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ActualIndex', _iec.SINT),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveSplineParCmd._IEC_FIELDS_ = (
    _iec.IecField('SplineID', _iec.SINT),
    _iec.IecField('BlendingMode', _iec.EnumType(_e.BlendingMode)),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.TIME),
)
MoveSplineRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveSplineSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('SplineID', _iec.SINT),
    _iec.IecField('BlendingMode', _iec.USINT),
    _iec.IecField('BlendingParameter', _iec.ArrayType(0, 1, _iec.REAL)),
    _iec.IecField('MoveTime', _iec.UINT),
)
MoveSuperImposedOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('OriginID', _iec.DINT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
MoveSuperImposedParCmd._IEC_FIELDS_ = (
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityDiffRate', _iec.REAL),
    _iec.IecField('AccelerationDiffRate', _iec.REAL),
    _iec.IecField('DecelerationDiffRate', _iec.REAL),
    _iec.IecField('JerkDiffRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
MoveSuperImposedRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
)
MoveSuperImposedSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('VelocityDiffRate', _iec.UINT),
    _iec.IecField('AccelerationDiffRate', _iec.UINT),
    _iec.IecField('DecelerationDiffRate', _iec.UINT),
    _iec.IecField('JerkDiffRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('Reserve2', _iec.BYTE),
)
MoveSuperImposedDynamicOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('Progress', _iec.REAL),
    _iec.IecField('OffsetReached', _iec.BOOL),
)
MoveSuperImposedDynamicParCmd._IEC_FIELDS_ = (
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.EnumType(_e.ReferenceType)),
    _iec.IecField('VelocityDiffRate', _iec.REAL),
    _iec.IecField('AccelerationDiffRate', _iec.REAL),
    _iec.IecField('DecelerationDiffRate', _iec.REAL),
    _iec.IecField('JerkDiffRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('InterpolationMode', _iec.EnumType(_e.InterpolationMode)),
)
MoveSuperImposedDynamicRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Progress', _iec.UINT),
    _iec.IecField('RemainingDistance', _iec.REAL),
    _iec.IecField('OffsetReached', _iec.BOOL),
)
MoveSuperImposedDynamicSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityDiffRate', _iec.UINT),
    _iec.IecField('AccelerationDiffRate', _iec.UINT),
    _iec.IecField('DecelerationDiffRate', _iec.UINT),
    _iec.IecField('JerkDiffRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('Reserve_X', _iec.REAL),
    _iec.IecField('Offset', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ReferenceType', _iec.USINT),
    _iec.IecField('InterpolationMode', _iec.USINT),
)
ReactAtTriggerOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
ReactAtTriggerParCmd._IEC_FIELDS_ = (
    _iec.IecField('ReactionMode', _iec.EnumType(_e.TriggerReactionMode)),
    _iec.IecField('ListenerID', _iec.SINT),
)
ReactAtTriggerRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
ReactAtTriggerSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('ReactionMode', _iec.EnumType(_e.TriggerReactionMode)),
)
SetTriggerErrorOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('FollowID', _iec.DINT),
)
SetTriggerErrorParCmd._IEC_FIELDS_ = (
    _iec.IecField('Mode', _iec.EnumType(_e.ErrorTriggerMode)),
    _iec.IecField('MessageCodes', _iec.ArrayType(0, _iec.Param('MESSAGE_CODES_MAX'), _iec.DWORD)),
    _iec.IecField('IncludeParameterValidation', _iec.BOOL),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('EmitterID', _iec.SINT),
)
SetTriggerErrorRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
SetTriggerErrorSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('Mode', _iec.SINT),
    _iec.IecField('IncludeParameterValidation', _iec.BOOL),
    _iec.IecField('MessageCodes', _iec.ArrayType(0, _iec.Param('MESSAGE_CODES_MAX'), _iec.DWORD)),
)
SetTriggerLimitOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('FollowID', _iec.DINT),
)
SetTriggerLimitParCmd._IEC_FIELDS_ = (
    _iec.IecField('TriggerMode', _iec.EnumType(_e.TriggerModeLimit)),
    _iec.IecField('EvaluateStartCondition', _iec.BOOL),
    _iec.IecField('Data_1', _iec.ArrayType(0, 11, _iec.REAL)),
    _iec.IecField('Data_2', _iec.ArrayType(0, 11, _iec.REAL)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('EmitterID', _iec.SINT),
)
SetTriggerLimitRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('Data', _iec.ArrayType(0, 11, _iec.REAL)),
)
SetTriggerLimitSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Data_1', _iec.ArrayType(0, 11, _iec.REAL)),
    _iec.IecField('Data_2', _iec.ArrayType(0, 11, _iec.REAL)),
    _iec.IecField('TriggerMode', _iec.SINT),
    _iec.IecField('EvaluateStartCondition', _iec.BOOL),
)
SetTriggerMotionOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('FollowID', _iec.DINT),
)
SetTriggerMotionParCmd._IEC_FIELDS_ = (
    _iec.IecField('TriggerMode_1', _iec.EnumType(_e.TriggerCondition)),
    _iec.IecField('TriggerParameter_1', _iec.REAL),
    _iec.IecField('TriggerMode_2', _iec.EnumType(_e.TriggerCondition)),
    _iec.IecField('TriggerParameter_2', _iec.REAL),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
)
SetTriggerMotionRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
SetTriggerMotionSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('TriggerMode_1', _iec.SINT),
    _iec.IecField('TriggerMode_2', _iec.SINT),
    _iec.IecField('TriggerParameter_1', _iec.REAL),
    _iec.IecField('TriggerParameter_2', _iec.REAL),
)
SetTriggerRegisterOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('FollowID', _iec.DINT),
)
SetTriggerRegisterParCmd._IEC_FIELDS_ = (
    _iec.IecField('TriggerMode', _iec.EnumType(_e.TriggerModeIo)),
    _iec.IecField('EvaluateStartCondition', _iec.BOOL),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('BitIndex', _iec.USINT),
    _iec.IecField('IntValue', _iec.ArrayType(1, 2, _iec.INT)),
    _iec.IecField('RealValue', _iec.ArrayType(1, 2, _iec.REAL)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('EmitterID', _iec.SINT),
)
SetTriggerRegisterRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
SetTriggerRegisterSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('IntValue', _iec.ArrayType(1, 2, _iec.INT)),
    _iec.IecField('RealValue', _iec.ArrayType(1, 2, _iec.REAL)),
    _iec.IecField('TriggerMode', _iec.SINT),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('BitIndex', _iec.USINT),
)
SetTriggerUserOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('FollowID', _iec.DINT),
)
SetTriggerUserParCmd._IEC_FIELDS_ = (
    _iec.IecField('EmitterID', _iec.SINT),
)
SetTriggerUserRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
SetTriggerUserSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('IntValue', _iec.ArrayType(1, 2, _iec.INT)),
    _iec.IecField('RealValue', _iec.ArrayType(1, 2, _iec.REAL)),
    _iec.IecField('TriggerMode', _iec.SINT),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('BitIndex', _iec.USINT),
)
WaitForTriggerOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
WaitForTriggerParCmd._IEC_FIELDS_ = (
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('ConditionalWait', _iec.BOOL),
)
WaitForTriggerRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
WaitForTriggerSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('ConditionalWait', _iec.BOOL),
)
WaitTimeOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ElapsedTime', _iec.UDINT),
)
WaitTimeParCmd._IEC_FIELDS_ = (
    _iec.IecField('WaitTime', _iec.UDINT),
)
WaitTimeRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('ElapsedTime', _iec.UDINT),
    _iec.IecField('Reserve1', _iec.BYTE),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('Reserve3', _iec.BYTE),
    _iec.IecField('Reserve4', _iec.BYTE),
)
WaitTimeSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('WaitTime', _iec.UDINT),
    _iec.IecField('Reserve1', _iec.BYTE),
    _iec.IecField('Reserve2', _iec.BYTE),
    _iec.IecField('Reserve3', _iec.BYTE),
    _iec.IecField('Reserve4', _iec.BYTE),
)
ActivateWorkAreaOutCmd._IEC_FIELDS_ = (
)
ActivateWorkAreaParCmd._IEC_FIELDS_ = (
    _iec.IecField('WorkAreaNo', _iec.USINT),
    _iec.IecField('ActivateArea', _iec.BOOL),
)
ActivateWorkAreaRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
ActivateWorkAreaSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('WorkAreaNo', _iec.USINT),
    _iec.IecField('ActivateArea', _iec.BOOL),
)
MonitorWorkAreaOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ActivationState', _iec.WORD),
    _iec.IecField('MonitoringState', _iec.WORD),
)
MonitorWorkAreaParCmd._IEC_FIELDS_ = (
    _iec.IecField('WorkAreaNo', _iec.USINT),
)
MonitorWorkAreaRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('ActivationState', _iec.WORD),
    _iec.IecField('MonitoringState', _iec.WORD),
)
MonitorWorkAreaSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Enable', _iec.BOOL),
    _iec.IecField('WorkAreaNo', _iec.USINT),
)
ReadWorkAreaOutCmd._IEC_FIELDS_ = (
    _iec.IecField('WorkAreaNoReturn', _iec.USINT),
    _iec.IecField('WorkAreaData', _iec.StructType(RobotWorkAreaData)),
)
ReadWorkAreaParCmd._IEC_FIELDS_ = (
    _iec.IecField('WorkAreaNo', _iec.USINT),
)
ReadWorkAreaRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('WorkAreaNoReturn', _iec.USINT),
    _iec.IecField('WorkAreaData', _iec.StructType(RobotWorkAreaData)),
    _iec.IecField('DataChanged', _iec.BOOL),
)
ReadWorkAreaSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('WorkAreaNo', _iec.USINT),
)
WriteWorkAreaOutCmd._IEC_FIELDS_ = (
)
WriteWorkAreaParCmd._IEC_FIELDS_ = (
    _iec.IecField('WorkAreaNo', _iec.USINT),
    _iec.IecField('WorkAreaData', _iec.StructType(RobotWorkAreaData)),
)
WriteWorkAreaRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
WriteWorkAreaSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('WorkAreaNo', _iec.USINT),
    _iec.IecField('WorkAreaData', _iec.StructType(RobotWorkAreaData)),
    _iec.IecField('DataChanged', _iec.BOOL),
)
WriteAnalogOutputOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
WriteAnalogOutputParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('Value', _iec.REAL),
    _iec.IecField('Unit', _iec.EnumType(_e.UnitType)),
    _iec.IecField('HighPriority', _iec.BOOL),
    _iec.IecField('ListenerID', _iec.SINT),
)
WriteAnalogOutputRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
WriteAnalogOutputSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Index', _iec.USINT),
    _iec.IecField('Unit', _iec.USINT),
    _iec.IecField('Value', _iec.REAL),
)
WriteDigitalOutputsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
WriteDigitalOutputsParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 4, _iec.USINT)),
    _iec.IecField('OutputBitmask', _iec.ArrayType(0, 4, _iec.BYTE)),
    _iec.IecField('Values', _iec.ArrayType(0, 4, _iec.BYTE)),
    _iec.IecField('HighPriority', _iec.BOOL),
    _iec.IecField('ListenerID', _iec.SINT),
)
WriteDigitalOutputsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
WriteDigitalOutputsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.ArrayType(0, 4, _iec.USINT)),
    _iec.IecField('OutputBitmask', _iec.ArrayType(0, 4, _iec.BYTE)),
    _iec.IecField('Values', _iec.ArrayType(0, 4, _iec.BYTE)),
)
WriteFrameDataOutCmd._IEC_FIELDS_ = (
)
WriteFrameDataParCmd._IEC_FIELDS_ = (
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('FrameData', _iec.StructType(FrameData)),
)
WriteFrameDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
WriteFrameDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('FrameData', _iec.StructType(FrameData)),
    _iec.IecField('FrameNo', _iec.USINT),
)
WriteIntegersOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
WriteIntegersParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.INT)),
    _iec.IecField('HighPriority', _iec.BOOL),
    _iec.IecField('ListenerID', _iec.SINT),
)
WriteIntegersRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
WriteIntegersSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.INT)),
)
WriteLoadDataOutCmd._IEC_FIELDS_ = (
)
WriteLoadDataParCmd._IEC_FIELDS_ = (
    _iec.IecField('LoadNo', _iec.USINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
)
WriteLoadDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
WriteLoadDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('LoadNo', _iec.USINT),
    _iec.IecField('LoadData', _iec.StructType(LoadData)),
)
WriteRealsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
)
WriteRealsParCmd._IEC_FIELDS_ = (
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('HighPriority', _iec.BOOL),
    _iec.IecField('ListenerID', _iec.SINT),
)
WriteRealsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
)
WriteRealsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('Index', _iec.ArrayType(0, 6, _iec.USINT)),
    _iec.IecField('Values', _iec.ArrayType(0, 6, _iec.REAL)),
)
WriteRobotDefaultDynamicsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('DefaultDynamicValues', _iec.StructType(DefaultDynamics)),
)
WriteRobotDefaultDynamicsParCmd._IEC_FIELDS_ = (
    _iec.IecField('DynamicValues', _iec.StructType(DefaultDynamics)),
)
WriteRobotDefaultDynamicsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
)
WriteRobotDefaultDynamicsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
)
WriteRobotReferenceDynamicsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('ReferenceDynamicValues', _iec.StructType(ReferenceDynamics)),
)
WriteRobotReferenceDynamicsParCmd._IEC_FIELDS_ = (
    _iec.IecField('DynamicValues', _iec.StructType(ReferenceDynamics)),
)
WriteRobotReferenceDynamicsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('ReferenceDynamicValues', _iec.StructType(ReferenceDynamics)),
)
WriteRobotReferenceDynamicsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('DynamicValues', _iec.StructType(ReferenceDynamics)),
)
WriteRobotSWLimitsOutCmd._IEC_FIELDS_ = (
    _iec.IecField('RestartRequested', _iec.BOOL),
)
WriteRobotSWLimitsParCmd._IEC_FIELDS_ = (
    _iec.IecField('LimitValues', _iec.StructType(SWLimits)),
    _iec.IecField('ResetToFactoryDefaults', _iec.BOOL),
)
WriteRobotSWLimitsRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('RestartRequested', _iec.BOOL),
)
WriteRobotSWLimitsSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('LimitValues', _iec.StructType(SWLimits)),
    _iec.IecField('ResetToFactoryDefaults', _iec.BOOL),
)
WriteSystemVariableOutCmd._IEC_FIELDS_ = (
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('RestartRequested', _iec.BOOL),
)
WriteSystemVariableParCmd._IEC_FIELDS_ = (
    _iec.IecField('RCParameter', _iec.BOOL),
    _iec.IecField('ParameterID', _iec.ArrayType(0, 7, _iec.UINT)),
    _iec.IecField('SubParameterID', _iec.ArrayType(0, 7, _iec.USINT)),
    _iec.IecField('DataType', _iec.ArrayType(0, 7, _iec.EnumType(_e.DataType))),
    _iec.IecField('Data_0', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_1', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_2', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_3', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_4', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_5', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_6', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_7', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('ListenerID', _iec.SINT),
)
WriteSystemVariableRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
    _iec.IecField('InvocationCounter', _iec.USINT),
    _iec.IecField('Reserve', _iec.SINT),
    _iec.IecField('OriginID', _iec.INT),
    _iec.IecField('RestartRequested', _iec.BOOL),
)
WriteSystemVariableSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('EmitterID', _iec.ArrayType(0, 3, _iec.SINT)),
    _iec.IecField('ListenerID', _iec.SINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ParameterID', _iec.ArrayType(0, 7, _iec.UINT)),
    _iec.IecField('SubParameterID', _iec.ArrayType(0, 7, _iec.USINT)),
    _iec.IecField('DataType', _iec.ArrayType(0, 7, _iec.USINT)),
    _iec.IecField('Data_0', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_1', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_2', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_3', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_4', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_5', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_6', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('Data_7', _iec.ArrayType(0, 3, _iec.BYTE)),
    _iec.IecField('RCParameter', _iec.BOOL),
)
WriteToolDataOutCmd._IEC_FIELDS_ = (
)
WriteToolDataParCmd._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('ToolData', _iec.StructType(ToolData)),
)
WriteToolDataRecvData._IEC_FIELDS_ = RspHeader._IEC_FIELDS_ + (
)
WriteToolDataSendData._IEC_FIELDS_ = CmdHeader._IEC_FIELDS_ + (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('ToolData', _iec.StructType(ToolData)),
)
SplineDataSend._IEC_FIELDS_ = (
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('VelocityRate', _iec.UINT),
    _iec.IecField('AccelerationRate', _iec.UINT),
    _iec.IecField('DecelerationRate', _iec.UINT),
    _iec.IecField('JerkRate', _iec.UINT),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('MoveTime', _iec.UINT),
)
AxesGroupAcyclic._IEC_FIELDS_ = (
    _iec.IecField('ActiveCommandRegister', _iec.InstanceType('ActiveCommandRegisterFB')),
)
AxesGroupAcyclicAcrEntry._IEC_FIELDS_ = (
    _iec.IecField('UniqueID', _iec.UINT),
    _iec.IecField('State', _iec.EnumType(_e.ActiveCommandRegisterState)),
    _iec.IecField('Command', _iec.ArrayType(1, 2, _iec.StructType(AxesGroupAcyclicAcrEntryCmdBuffer))),
    _iec.IecField('Response', _iec.ArrayType(1, 2, _iec.StructType(AxesGroupAcyclicAcrEntryRspBuffer))),
    _iec.IecField('pCommandFB', _iec.PointerType('RobotLibraryBaseFB')),
)
AxesGroupAcyclicAcrEntryCmdBuffer._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(SystemTime)),
    _iec.IecField('State', _iec.EnumType(_e.BufferStateCmd)),
    _iec.IecField('Payload', _iec.ArrayType(0, _iec.Param('PARAMETER_PAYLOAD_MAX'), _iec.BYTE)),
    _iec.IecField('PayloadLen', _iec.UDINT),
    _iec.IecField('PayLoadPtr', _iec.UINT),
)
AxesGroupAcyclicAcrEntryRspBuffer._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(SystemTime)),
    _iec.IecField('State', _iec.EnumType(_e.BufferStateRsp)),
    _iec.IecField('Payload', _iec.ArrayType(0, _iec.Param('RESPONSE_PAYLOAD_MAX'), _iec.BYTE)),
    _iec.IecField('PayloadLen', _iec.UDINT),
    _iec.IecField('PayLoadPtr', _iec.DWORD),
)
AxesGroupAcyclicExecutionOrderList._IEC_FIELDS_ = (
    _iec.IecField('Command', _iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.UINT)),
    _iec.IecField('Response', _iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.UINT)),
)
AxesGroupCyclic._IEC_FIELDS_ = (
    _iec.IecField('PlcToRob', _iec.StructType(AxesGroupCyclicPlcToRob)),
    _iec.IecField('RobToPlc', _iec.StructType(AxesGroupCyclicRobToPlc)),
)
AxesGroupCyclicPlcToRob._IEC_FIELDS_ = (
    _iec.IecField('SRCIVersion', _iec.StructType(VersionStruct)),
    _iec.IecField('FastStop', _iec.BYTE),
    _iec.IecField('LifeSign', _iec.BYTE),
    _iec.IecField('TelegramLengthPlcToRob', _iec.UINT),
    _iec.IecField('TelegramLengthRobToPlc', _iec.UINT),
    _iec.IecField('AxesGroupID', _iec.BYTE),
    _iec.IecField('Control', _iec.EnumType(_e.ControlHalfByte)),
    _iec.IecField('Reserved', _iec.BYTE),
    _iec.IecField('TelegramNumberPlcToRob', _iec.UINT),
    _iec.IecField('TelegramNumberRobToPlc', _iec.UINT),
    _iec.IecField('ClientDate', _iec.UINT),
    _iec.IecField('ClientTime', _iec.TOD),
    _iec.IecField('ToolNo', _iec.INT),
    _iec.IecField('FrameNo', _iec.INT),
)
AxesGroupCyclicRobToPlc._IEC_FIELDS_ = (
    _iec.IecField('SRCIVersion', _iec.StructType(VersionStruct)),
    _iec.IecField('LifeSign', _iec.BYTE),
    _iec.IecField('Reserved', _iec.BYTE),
    _iec.IecField('TelegramState', _iec.EnumType(_e.TelegramState)),
    _iec.IecField('StatusRobotArm', _iec.StructType(RaStatusWord)),
    _iec.IecField('Override', _iec.UINT),
)
RobotCartesianPositionBase._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
)
RobotCartesianPositionShort._IEC_FIELDS_ = RobotCartesianPositionBase._IEC_FIELDS_ + (
    _iec.IecField('Config', _iec.StructType(ArmConfigParameter)),
    _iec.IecField('TurnNumber', _iec.StructType(TurnNumber)),
    _iec.IecField('E1', _iec.REAL),
)
AxesGroupCyclicOptionalDataCartesianPosition._IEC_FIELDS_ = RobotCartesianPositionShort._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
    _iec.IecField('CoordinateSystem', _iec.StructType(RobotCoordinateSystemParameters)),
)
RobotCartesianPositionExt._IEC_FIELDS_ = (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
AxesGroupCyclicOptionalDataCartesianPositionExt._IEC_FIELDS_ = RobotCartesianPositionExt._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotJointCurrentShort._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
)
AxesGroupCyclicOptionalDataCurrent._IEC_FIELDS_ = RobotJointCurrentShort._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotJointCurrentExt._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
AxesGroupCyclicOptionalDataCurrentExt._IEC_FIELDS_ = RobotJointCurrentExt._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotCartesianForceShort._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
)
AxesGroupCyclicOptionalDataForce._IEC_FIELDS_ = RobotCartesianForceShort._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotCartesianForceExt._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
AxesGroupCyclicOptionalDataForceExt._IEC_FIELDS_ = RobotCartesianForceExt._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotJointPositionShort._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
    _iec.IecField('E1', _iec.REAL),
)
AxesGroupCyclicOptionalDataJointPosition._IEC_FIELDS_ = RobotJointPositionShort._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotJointPositionExt._IEC_FIELDS_ = (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
AxesGroupCyclicOptionalDataJointPositionExt._IEC_FIELDS_ = RobotJointPositionExt._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
RobotSubProgramData._IEC_FIELDS_ = (
    _iec.IecField('Data', _iec.ArrayType(0, 25, _iec.BYTE)),
)
AxesGroupCyclicOptionalDataSubProgram._IEC_FIELDS_ = RobotSubProgramData._IEC_FIELDS_ + (
    _iec.IecField('Active', _iec.BOOL),
)
AxesGroupCyclicOptionalData._IEC_FIELDS_ = (
    _iec.IecField('PlcToRob', _iec.StructType(AxesGroupCyclicOptionalDataPlcToRob)),
    _iec.IecField('RobToPlc', _iec.StructType(AxesGroupCyclicOptionalDataRobToPlc)),
)
AxesGroupCyclicOptionalDataPlcToRob._IEC_FIELDS_ = (
    _iec.IecField('SubProgramData', _iec.StructType(AxesGroupCyclicOptionalDataSubProgram)),
    _iec.IecField('CartesianPosition', _iec.StructType(AxesGroupCyclicOptionalDataCartesianPosition)),
    _iec.IecField('CartesianPositionExt', _iec.StructType(AxesGroupCyclicOptionalDataCartesianPositionExt)),
    _iec.IecField('JointPosition', _iec.StructType(AxesGroupCyclicOptionalDataJointPosition)),
    _iec.IecField('JointPositionExt', _iec.StructType(AxesGroupCyclicOptionalDataJointPositionExt)),
    _iec.IecField('Force', _iec.StructType(AxesGroupCyclicOptionalDataForce)),
    _iec.IecField('ForceExt', _iec.StructType(AxesGroupCyclicOptionalDataForceExt)),
)
AxesGroupCyclicOptionalDataRobToPlc._IEC_FIELDS_ = (
    _iec.IecField('SubProgramData', _iec.StructType(AxesGroupCyclicOptionalDataSubProgram)),
    _iec.IecField('CartesianPosition', _iec.StructType(AxesGroupCyclicOptionalDataCartesianPosition)),
    _iec.IecField('CartesianPositionExt', _iec.StructType(AxesGroupCyclicOptionalDataCartesianPositionExt)),
    _iec.IecField('JointPosition', _iec.StructType(AxesGroupCyclicOptionalDataJointPosition)),
    _iec.IecField('JointPositionExt', _iec.StructType(AxesGroupCyclicOptionalDataJointPositionExt)),
    _iec.IecField('Force', _iec.StructType(AxesGroupCyclicOptionalDataForce)),
    _iec.IecField('ForceExt', _iec.StructType(AxesGroupCyclicOptionalDataForceExt)),
    _iec.IecField('Current', _iec.StructType(AxesGroupCyclicOptionalDataCurrent)),
    _iec.IecField('CurrentExt', _iec.StructType(AxesGroupCyclicOptionalDataCurrentExt)),
)
AxesGroupMessageLog._IEC_FIELDS_ = (
    _iec.IecField('SystemLogEntries', _iec.UINT),
    _iec.IecField('MessagesEntries', _iec.UINT),
    _iec.IecField('LogLevel', _iec.EnumType(_e.Severity)),
    _iec.IecField('SystemLog', _iec.ArrayType(0, _iec.Param('SYSTEM_LOG_MAX'), _iec.StringType(255))),
    _iec.IecField('Messages', _iec.ArrayType(0, _iec.Param('MESSAGE_LOG_MAX'), _iec.StructType(AlarmMessage))),
    _iec.IecField('ExternalLogger', _iec.InstanceType('IMessageLogger')),
)
AxesGroupParameterOptionalCyclic._IEC_FIELDS_ = (
    _iec.IecField('PlcToRob', _iec.StructType(AxesGroupParameterOptionalCyclicPlcToRob)),
    _iec.IecField('RobToPlc', _iec.StructType(AxesGroupParameterOptionalCyclicRobToPlc)),
)
AxesGroupParameterOptionalCyclicPlcToRob._IEC_FIELDS_ = (
    _iec.IecField('UseCallSubprogram', _iec.BOOL),
    _iec.IecField('UseCartesianPosition', _iec.BOOL),
    _iec.IecField('UseJointPosition', _iec.BOOL),
    _iec.IecField('UseForce', _iec.BOOL),
    _iec.IecField('Bit04', _iec.BOOL),
    _iec.IecField('Bit05', _iec.BOOL),
    _iec.IecField('Bit06', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
    _iec.IecField('UseTwoSequences', _iec.BOOL),
    _iec.IecField('UseCartesianPositionExt', _iec.BOOL),
    _iec.IecField('UseJointPositionExt', _iec.BOOL),
    _iec.IecField('Bit11', _iec.BOOL),
    _iec.IecField('Bit12', _iec.BOOL),
    _iec.IecField('Bit13', _iec.BOOL),
    _iec.IecField('Bit14', _iec.BOOL),
    _iec.IecField('Bit15', _iec.BOOL),
)
AxesGroupParameterOptionalCyclicRobToPlc._IEC_FIELDS_ = (
    _iec.IecField('UseCallSubprogram', _iec.BOOL),
    _iec.IecField('UseCartesianPosition', _iec.BOOL),
    _iec.IecField('UseJointPosition', _iec.BOOL),
    _iec.IecField('UseForce', _iec.BOOL),
    _iec.IecField('UseCurrent', _iec.BOOL),
    _iec.IecField('Bit05', _iec.BOOL),
    _iec.IecField('Bit06', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
    _iec.IecField('UseTwoSequences', _iec.BOOL),
    _iec.IecField('UseCartesianPositionExt', _iec.BOOL),
    _iec.IecField('UseJointPositionExt', _iec.BOOL),
    _iec.IecField('UseForceExt', _iec.BOOL),
    _iec.IecField('UseCurrentExt', _iec.BOOL),
    _iec.IecField('Bit13', _iec.BOOL),
    _iec.IecField('Bit14', _iec.BOOL),
    _iec.IecField('Bit15', _iec.BOOL),
)
AxesGroupParameterPlc._IEC_FIELDS_ = (
    _iec.IecField('Parameter', _iec.StructType(AxesGroupParameterPlcParameter)),
    _iec.IecField('OptionalCyclic', _iec.StructType(AxesGroupParameterPlcOptionalCyclic)),
)
AxesGroupParameterPlcOptionalCyclic._IEC_FIELDS_ = (
    _iec.IecField('UseCallSubprogram', _iec.BOOL),
    _iec.IecField('UseCartesianPosition', _iec.BOOL),
    _iec.IecField('UseJointPosition', _iec.BOOL),
    _iec.IecField('UseForce', _iec.BOOL),
    _iec.IecField('Bit04', _iec.BOOL),
    _iec.IecField('Bit05', _iec.BOOL),
    _iec.IecField('Bit06', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
    _iec.IecField('UseTwoSequences', _iec.BOOL),
    _iec.IecField('UseCartesianPositionExt', _iec.BOOL),
    _iec.IecField('UseJointPositionExt', _iec.BOOL),
    _iec.IecField('Bit11', _iec.BOOL),
    _iec.IecField('Bit12', _iec.BOOL),
    _iec.IecField('Bit13', _iec.BOOL),
    _iec.IecField('Bit14', _iec.BOOL),
    _iec.IecField('Bit15', _iec.BOOL),
)
AxesGroupParameterRob._IEC_FIELDS_ = (
    _iec.IecField('Parameter', _iec.StructType(AxesGroupParameterRobParameter)),
    _iec.IecField('OptionalCyclic', _iec.StructType(AxesGroupParameterRobOptionalCyclic)),
)
AxesGroupParameterRobOptionalCyclic._IEC_FIELDS_ = (
    _iec.IecField('UseCallSubprogram', _iec.BOOL),
    _iec.IecField('UseCartesianPosition', _iec.BOOL),
    _iec.IecField('UseJointPosition', _iec.BOOL),
    _iec.IecField('UseForce', _iec.BOOL),
    _iec.IecField('UseCurrent', _iec.BOOL),
    _iec.IecField('Bit05', _iec.BOOL),
    _iec.IecField('Bit06', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
    _iec.IecField('UseTwoSequences', _iec.BOOL),
    _iec.IecField('UseCartesianPositionExt', _iec.BOOL),
    _iec.IecField('UseJointPositionExt', _iec.BOOL),
    _iec.IecField('UseForceExt', _iec.BOOL),
    _iec.IecField('UseCurrentExt', _iec.BOOL),
    _iec.IecField('Bit13', _iec.BOOL),
    _iec.IecField('Bit14', _iec.BOOL),
    _iec.IecField('Bit15', _iec.BOOL),
)
AxesGroupParameterRobParameter._IEC_FIELDS_ = (
    _iec.IecField('RobotName', _iec.StringType(20)),
    _iec.IecField('LengthACR', _iec.UINT),
    _iec.IecField('HighestToolIndex', _iec.USINT),
    _iec.IecField('HighestFrameIndex', _iec.USINT),
    _iec.IecField('HighestLoadIndex', _iec.USINT),
    _iec.IecField('HighestWorkAreaIndex', _iec.USINT),
    _iec.IecField('DataInSync', _iec.StructType(DataInSync)),
    _iec.IecField('ChangeIndexTool', _iec.USINT),
    _iec.IecField('ChangeIndexFrame', _iec.USINT),
    _iec.IecField('ChangeIndexLoad', _iec.USINT),
    _iec.IecField('ChangeIndexWorkArea', _iec.USINT),
    _iec.IecField('RAWorkingHours', _iec.UDINT),
    _iec.IecField('BrakeTestRequired', _iec.BOOL),
    _iec.IecField('StepModeExactStopActive', _iec.BOOL),
    _iec.IecField('StepModeBlendingActive', _iec.BOOL),
    _iec.IecField('PathAccuracyMode', _iec.BOOL),
    _iec.IecField('AvoidSingularity', _iec.BOOL),
    _iec.IecField('CollisionDetectionEnabled', _iec.BOOL),
    _iec.IecField('AcceleratingSupported', _iec.BOOL),
    _iec.IecField('DecceleratingSupported', _iec.BOOL),
    _iec.IecField('ConstantVelocitySupported', _iec.BOOL),
    _iec.IecField('RCWorkingHours', _iec.UDINT),
)
AxesGroupParameter._IEC_FIELDS_ = (
    _iec.IecField('Plc', _iec.StructType(AxesGroupParameterPlc)),
    _iec.IecField('Rob', _iec.StructType(AxesGroupParameterRob)),
)
AxesGroupStateDataChanged._IEC_FIELDS_ = (
    _iec.IecField('Tool', _iec.ArrayType(0, _iec.Param('TOOL_MAX', -1), _iec.BOOL)),
    _iec.IecField('Frame', _iec.ArrayType(0, _iec.Param('FRAME_MAX', -1), _iec.BOOL)),
    _iec.IecField('Load', _iec.ArrayType(0, _iec.Param('LOAD_MAX', -1), _iec.BOOL)),
    _iec.IecField('WorkArea', _iec.ArrayType(0, _iec.Param('WORK_AREAS_MAX', -1), _iec.BOOL)),
    _iec.IecField('DefaultDynamics', _iec.BOOL),
    _iec.IecField('ReferenceDynamics', _iec.BOOL),
    _iec.IecField('SwLimits', _iec.BOOL),
)
AxesGroupStateSynchronizing._IEC_FIELDS_ = (
    _iec.IecField('Tool', _iec.BOOL),
    _iec.IecField('Frame', _iec.BOOL),
    _iec.IecField('Load', _iec.BOOL),
    _iec.IecField('WorkAreas', _iec.BOOL),
    _iec.IecField('ReferenceDynamics', _iec.BOOL),
    _iec.IecField('DefaultDynamics', _iec.BOOL),
    _iec.IecField('SwLimits', _iec.BOOL),
)
AxesGroupStateSyncState._IEC_FIELDS_ = (
    _iec.IecField('Tool', _iec.BOOL),
    _iec.IecField('Frame', _iec.BOOL),
    _iec.IecField('Load', _iec.BOOL),
    _iec.IecField('WorkArea', _iec.BOOL),
    _iec.IecField('SwLimits', _iec.BOOL),
    _iec.IecField('DefaultDynamics', _iec.BOOL),
    _iec.IecField('ReferenceDynamics', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
    _iec.IecField('Bit08', _iec.BOOL),
    _iec.IecField('Bit09', _iec.BOOL),
    _iec.IecField('Bit10', _iec.BOOL),
    _iec.IecField('Bit11', _iec.BOOL),
    _iec.IecField('Bit12', _iec.BOOL),
    _iec.IecField('Bit13', _iec.BOOL),
    _iec.IecField('Bit14', _iec.BOOL),
    _iec.IecField('Bit15', _iec.BOOL),
)
AxesGroupStateSyncStateNo._IEC_FIELDS_ = (
    _iec.IecField('Tool', _iec.USINT),
    _iec.IecField('Frame', _iec.USINT),
    _iec.IecField('Load', _iec.USINT),
    _iec.IecField('WorkArea', _iec.USINT),
)
AxesGroupStateSyncStatePlc._IEC_FIELDS_ = (
    _iec.IecField('InSync', _iec.StructType(AxesGroupStateSyncState)),
    _iec.IecField('UnSyncNo', _iec.StructType(AxesGroupStateSyncStateNo)),
)
AxesGroupStateSyncStateRob._IEC_FIELDS_ = (
    _iec.IecField('InSync', _iec.StructType(AxesGroupStateSyncState)),
    _iec.IecField('UnSyncNo', _iec.StructType(AxesGroupStateSyncStateNo)),
)
AxesGroupState._IEC_FIELDS_ = (
    _iec.IecField('FatalErrorClient', _iec.BOOL),
    _iec.IecField('InvalidFrames', _iec.UDINT),
    _iec.IecField('Synchronized', _iec.BOOL),
    _iec.IecField('Synchronizing', _iec.StructType(AxesGroupStateSynchronizing)),
    _iec.IecField('AliveOk', _iec.BOOL),
    _iec.IecField('CMDsEnabled', _iec.BOOL),
    _iec.IecField('ConfigExchanged', _iec.BOOL),
    _iec.IecField('UnifiedToolIndex', _iec.USINT),
    _iec.IecField('UnifiedFrameIndex', _iec.USINT),
    _iec.IecField('UnifiedLoadIndex', _iec.USINT),
    _iec.IecField('UnifiedWorkAreaIndex', _iec.USINT),
    _iec.IecField('DataEnableSync', _iec.StructType(DataEnableSync)),
    _iec.IecField('DataChanged', _iec.StructType(AxesGroupStateDataChanged)),
    _iec.IecField('SyncStatePlc', _iec.StructType(AxesGroupStateSyncStatePlc)),
    _iec.IecField('SyncStateRc', _iec.StructType(AxesGroupStateSyncStateRob)),
    _iec.IecField('SystemTime', _iec.StructType(SystemTime)),
    _iec.IecField('RobotData', _iec.StructType(ReadRobotDataOutCmd)),
    _iec.IecField('StatusRobotArm', _iec.StructType(RaStatusWord)),
    _iec.IecField('ConfigurationData', _iec.StructType(ExchangeConfigurationOutCmd)),
    _iec.IecField('ReadingCartesianPosition', _iec.BOOL),
    _iec.IecField('ReadingCartesianPositionExt', _iec.BOOL),
    _iec.IecField('ReadingJointPosition', _iec.BOOL),
    _iec.IecField('ReadingJointPositionExt', _iec.BOOL),
    _iec.IecField('Initialized', _iec.BOOL),
    _iec.IecField('OnlineChange', _iec.BOOL),
    _iec.IecField('OnlineChange_R', _iec.InstanceType('R_TRIG')),
    _iec.IecField('OnlineChange_F', _iec.InstanceType('F_TRIG')),
    _iec.IecField('GroupReset', _iec.BOOL),
    _iec.IecField('GroupReset_R', _iec.InstanceType('R_TRIG')),
    _iec.IecField('GroupReset_F', _iec.InstanceType('F_TRIG')),
    _iec.IecField('SequenceCountSend', _iec.DINT),
    _iec.IecField('SequenceCountRecv', _iec.DINT),
    _iec.IecField('FragmentCountSend', _iec.ArrayType(0, 1, _iec.DINT)),
    _iec.IecField('FragmentCountRecv', _iec.ArrayType(0, 1, _iec.DINT)),
    _iec.IecField('CurrentSEQ', _iec.ArrayType(0, 1, _iec.UINT)),
    _iec.IecField('CurrentACK', _iec.ArrayType(0, 1, _iec.UINT)),
    _iec.IecField('NewSEQ', _iec.ArrayType(0, 1, _iec.BOOL)),
    _iec.IecField('LastACK', _iec.ArrayType(0, 1, _iec.UINT)),
)
AxesGroup._IEC_FIELDS_ = (
    _iec.IecField('Parameter', _iec.StructType(AxesGroupParameter)),
    _iec.IecField('State', _iec.StructType(AxesGroupState)),
    _iec.IecField('MessageLog', _iec.InstanceType('AxesGroupMessageLogFB')),
    _iec.IecField('Cyclic', _iec.StructType(AxesGroupCyclic)),
    _iec.IecField('CyclicOptional', _iec.StructType(AxesGroupCyclicOptionalData)),
    _iec.IecField('Acyclic', _iec.StructType(AxesGroupAcyclic)),
    _iec.IecField('SystemData', _iec.InstanceType('AxesGroupSystemDataFB')),
)
AxisExternalUnit._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('E2', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('E3', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('E4', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('E5', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('E6', _iec.EnumType(_e.AxisUnit)),
)
AxisExternalUsed._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.BOOL),
    _iec.IecField('E2', _iec.BOOL),
    _iec.IecField('E3', _iec.BOOL),
    _iec.IecField('E4', _iec.BOOL),
    _iec.IecField('E5', _iec.BOOL),
    _iec.IecField('E6', _iec.BOOL),
)
AxisJointUnit._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('J2', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('J3', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('J4', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('J5', _iec.EnumType(_e.AxisUnit)),
    _iec.IecField('J6', _iec.EnumType(_e.AxisUnit)),
)
AxisJointUsed._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.BOOL),
    _iec.IecField('J2', _iec.BOOL),
    _iec.IecField('J3', _iec.BOOL),
    _iec.IecField('J4', _iec.BOOL),
    _iec.IecField('J5', _iec.BOOL),
    _iec.IecField('J6', _iec.BOOL),
)
RobotCartesianForce._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
RobotCartesianPosition._IEC_FIELDS_ = RobotCartesianPositionShort._IEC_FIELDS_ + (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
LogParameter._IEC_FIELDS_ = (
    _iec.IecField('CreateCmd', _iec.EnumType(_e.Severity)),
    _iec.IecField('UpdateCmd', _iec.EnumType(_e.Severity)),
    _iec.IecField('GenSeq', _iec.EnumType(_e.Severity)),
    _iec.IecField('DecSeq', _iec.EnumType(_e.Severity)),
)
RobotCoordinateSystemParameters._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
)
Frame._IEC_FIELDS_ = (
    _iec.IecField('Available', _iec.BOOL),
    _iec.IecField('Data', _iec.StructType(FrameData)),
)
FrameData._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('ReferenceFrame', _iec.USINT),
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
)
Load._IEC_FIELDS_ = (
    _iec.IecField('Available', _iec.BOOL),
    _iec.IecField('Data', _iec.StructType(LoadData)),
)
LoadData._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
    _iec.IecField('Mass', _iec.REAL),
    _iec.IecField('Ix', _iec.REAL),
    _iec.IecField('Iy', _iec.REAL),
    _iec.IecField('Iz', _iec.REAL),
)
SplineData._IEC_FIELDS_ = (
    _iec.IecField('Position', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('MoveTime', _iec.TIME),
)
Tool._IEC_FIELDS_ = (
    _iec.IecField('Available', _iec.BOOL),
    _iec.IecField('Data', _iec.StructType(ToolData)),
)
ToolData._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('ID', _iec.USINT),
    _iec.IecField('ExternalTCP', _iec.BOOL),
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
    _iec.IecField('LoadNo', _iec.USINT),
)
UserData._IEC_FIELDS_ = (
    _iec.IecField('EnableSync', _iec.StructType(DataEnableSync)),
    _iec.IecField('ActivateTwoSequences', _iec.BOOL),
    _iec.IecField('SynchronizationModes', _iec.StructType(SynchronizationModes)),
    _iec.IecField('DelayTime', _iec.UINT),
    _iec.IecField('WaitForNrOfCmd', _iec.UINT),
    _iec.IecField('WaitAtBlendingZone', _iec.BOOL),
    _iec.IecField('AllowSecSeqWhileSubprogram', _iec.BOOL),
    _iec.IecField('AllowDynamicBlending', _iec.BOOL),
    _iec.IecField('LifeSignTimeOut', _iec.TIME),
    _iec.IecField('SyncReaction', _iec.USINT),
    _iec.IecField('SyncDelay', _iec.UINT),
    _iec.IecField('LogLevel', _iec.EnumType(_e.Severity)),
    _iec.IecField('MessageLevel', _iec.EnumType(_e.MessageLevel)),
    _iec.IecField('PLCManufacturedID', _iec.UINT),
    _iec.IecField('PLCOrderID', _iec.StringType(20)),
    _iec.IecField('PLCSerialNumber', _iec.StringType(16)),
    _iec.IecField('PLCFirmwareVersion', _iec.StringType(8)),
    _iec.IecField('PLCInterfaceVersion', _iec.StringType(8)),
    _iec.IecField('PLCLibraryVersion', _iec.StructType(VersionStruct)),
    _iec.IecField('RCManufacturer', _iec.StringType(20)),
    _iec.IecField('RCOrderID', _iec.StringType(20)),
    _iec.IecField('RCSerialNumber', _iec.StringType(16)),
    _iec.IecField('RASerialNumber', _iec.StringType(16)),
    _iec.IecField('RCFirmwareVersion', _iec.StringType(12)),
    _iec.IecField('RCInterpreterVersion', _iec.StructType(VersionStruct)),
    _iec.IecField('RCSRCIVersion', _iec.StructType(VersionStruct)),
    _iec.IecField('AxisJointUsed', _iec.StructType(AxisJointUsed)),
    _iec.IecField('AxisExternalUsed', _iec.StructType(AxisExternalUsed)),
    _iec.IecField('AxisJointUnit', _iec.StructType(AxisJointUnit)),
    _iec.IecField('AxisExternalUnit', _iec.StructType(AxisExternalUnit)),
    _iec.IecField('Initialized', _iec.BOOL),
    _iec.IecField('Synchronized', _iec.BOOL),
    _iec.IecField('ToolDataSynchronizing', _iec.BOOL),
    _iec.IecField('FrameDataSynchronizing', _iec.BOOL),
    _iec.IecField('LoadDataSynchronizing', _iec.BOOL),
    _iec.IecField('WorkAreaDataSynchronizing', _iec.BOOL),
    _iec.IecField('SWLimitsSynchronizing', _iec.BOOL),
    _iec.IecField('DefaultDynamicsSynchronizing', _iec.BOOL),
    _iec.IecField('ReferenceDynamicsSynchronizing', _iec.BOOL),
    _iec.IecField('IsMoving', _iec.BOOL),
    _iec.IecField('PrimarySequencePaused', _iec.BOOL),
    _iec.IecField('InPrimaryPos', _iec.BOOL),
    _iec.IecField('SecondarySequenceActive', _iec.BOOL),
    _iec.IecField('ErrorPending', _iec.BOOL),
    _iec.IecField('RestartInProgress', _iec.BOOL),
    _iec.IecField('BrakeTestRequired', _iec.BOOL),
    _iec.IecField('Enabled', _iec.BOOL),
    _iec.IecField('Idle', _iec.BOOL),
    _iec.IecField('Executing', _iec.BOOL),
    _iec.IecField('Interrupted', _iec.BOOL),
    _iec.IecField('IsBlending', _iec.BOOL),
    _iec.IecField('OperationMode', _iec.EnumType(_e.OperationMode)),
    _iec.IecField('PathAccuracyMode', _iec.BOOL),
    _iec.IecField('AvoidSingularity', _iec.BOOL),
    _iec.IecField('CollisionDetectionEnabled', _iec.BOOL),
    _iec.IecField('CollisionDetected', _iec.BOOL),
    _iec.IecField('RestartRequested', _iec.BOOL),
    _iec.IecField('ActualOverride', _iec.REAL),
    _iec.IecField('StepModeExactStopActive', _iec.BOOL),
    _iec.IecField('StepModeBlendingActive', _iec.BOOL),
    _iec.IecField('AcceleratingSupported', _iec.BOOL),
    _iec.IecField('Accelerating', _iec.BOOL),
    _iec.IecField('DeceleratingSupported', _iec.BOOL),
    _iec.IecField('Decelerating', _iec.BOOL),
    _iec.IecField('ConstantVelocitySupported', _iec.BOOL),
    _iec.IecField('ConstantVelocity', _iec.BOOL),
    _iec.IecField('ReadingCartesianPosition', _iec.BOOL),
    _iec.IecField('ReadingExtCartesianPosition', _iec.BOOL),
    _iec.IecField('ReadingJointPosition', _iec.BOOL),
    _iec.IecField('ReadingExtJointPosition', _iec.BOOL),
    _iec.IecField('CartesianPosition', _iec.StructType(RobotCartesianPositionShort)),
    _iec.IecField('ExtCartesianPosition', _iec.StructType(RobotCartesianPositionExt)),
    _iec.IecField('JointPosition', _iec.StructType(RobotJointPositionShort)),
    _iec.IecField('ExtJointPosition', _iec.StructType(RobotJointPositionExt)),
    _iec.IecField('RCSupportedFunctions', _iec.StructType(RCSupportedFunctions)),
)
RobotWorkArea._IEC_FIELDS_ = (
    _iec.IecField('Available', _iec.BOOL),
    _iec.IecField('Data', _iec.StructType(RobotWorkAreaData)),
)
RobotWorkAreaData._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('AreaType', _iec.EnumType(_e.AreaType)),
    _iec.IecField('AreaMode', _iec.BOOL),
    _iec.IecField('ReactionMode', _iec.EnumType(_e.WorkAreaReactionMode)),
    _iec.IecField('ActiveModification', _iec.BOOL),
    _iec.IecField('DefinitionMode', _iec.EnumType(_e.DefinitionMode)),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('ZeroPointX', _iec.REAL),
    _iec.IecField('ZeroPointY', _iec.REAL),
    _iec.IecField('ZeroPointZ', _iec.REAL),
    _iec.IecField('X', _iec.StructType(RobotWorkAreaDataLimitCartesian)),
    _iec.IecField('Y', _iec.StructType(RobotWorkAreaDataLimitCartesian)),
    _iec.IecField('Z', _iec.StructType(RobotWorkAreaDataLimitCartesian)),
    _iec.IecField('Radius', _iec.REAL),
    _iec.IecField('J1Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('J2Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('J3Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('J4Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('J5Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('J6Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('E1Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('E2Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('E3Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('E4Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('E5Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
    _iec.IecField('E6Limit', _iec.StructType(RobotWorkAreaDataLimitJoint)),
)
RobotWorkAreaDataLimitCartesian._IEC_FIELDS_ = (
    _iec.IecField('LowerLimit', _iec.REAL),
    _iec.IecField('UpperLimit', _iec.REAL),
)
RobotWorkAreaDataLimitJoint._IEC_FIELDS_ = (
    _iec.IecField('LowerLimit', _iec.REAL),
    _iec.IecField('UpperLimit', _iec.REAL),
)
CyclicStateData._IEC_FIELDS_ = (
    _iec.IecField('StatusWord', _iec.StructType(RaStatusWord)),
    _iec.IecField('Override', _iec.UINT),
)
IEC_TIMESTAMP._IEC_FIELDS_ = (
    _iec.IecField('IEC_DATE', _iec.UINT),
    _iec.IecField('IEC_TIME', _iec.TOD),
)
SystemTime._IEC_FIELDS_ = (
    _iec.IecField('SystemDate', _iec.DATE),
    _iec.IecField('SystemTime', _iec.TOD),
)
DefaultDynamics._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
)
ReferenceDynamics._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('VelocityReference', _iec.REAL),
    _iec.IecField('AccelerationReference', _iec.REAL),
    _iec.IecField('DecelerationReference', _iec.REAL),
    _iec.IecField('JerkReference', _iec.REAL),
)
RobotDynamics._IEC_FIELDS_ = (
    _iec.IecField('VelocityRate', _iec.REAL),
    _iec.IecField('AccelerationRate', _iec.REAL),
    _iec.IecField('DecelerationRate', _iec.REAL),
    _iec.IecField('JerkRate', _iec.REAL),
)
RobotJointCurrent._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
RobotJointPosition._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
AlarmMessage._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(SystemTime)),
    _iec.IecField('MessageType', _iec.EnumType(_e.MessageType)),
    _iec.IecField('Severity', _iec.EnumType(_e.Severity)),
    _iec.IecField('MessageCode', _iec.DWORD),
    _iec.IecField('MessageText', _iec.StringType(255)),
)
ArmConfigParameter._IEC_FIELDS_ = (
    _iec.IecField('Shoulder', _iec.EnumType(_e.ArmConfigShoulder)),
    _iec.IecField('Elbow', _iec.EnumType(_e.ArmConfigElbow)),
    _iec.IecField('Wrist', _iec.EnumType(_e.ArmConfigWrist)),
)
AuxOffset._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
)
CoordinateSystem._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
)
DataEnableSync._IEC_FIELDS_ = (
    _iec.IecField('EnableSyncTool', _iec.BOOL),
    _iec.IecField('EnableSyncFrame', _iec.BOOL),
    _iec.IecField('EnableSyncLoad', _iec.BOOL),
    _iec.IecField('EnableSyncWorkArea', _iec.BOOL),
    _iec.IecField('EnableSyncSWLimits', _iec.BOOL),
    _iec.IecField('EnableSyncDefaultDynamics', _iec.BOOL),
    _iec.IecField('EnableSyncReferenceDynamics', _iec.BOOL),
)
DataInSync._IEC_FIELDS_ = (
    _iec.IecField('ToolsInSync', _iec.BOOL),
    _iec.IecField('FramesInSync', _iec.BOOL),
    _iec.IecField('LoadsInSync', _iec.BOOL),
    _iec.IecField('WorkAreasInSync', _iec.BOOL),
    _iec.IecField('SoftwareLimitsInSync', _iec.BOOL),
    _iec.IecField('DefaultDynamicsInSync', _iec.BOOL),
    _iec.IecField('ReferenceDynamicsInSync', _iec.BOOL),
)
DHParameter._IEC_FIELDS_ = (
    _iec.IecField('Alpha', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('A', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('D', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('Theta', _iec.ArrayType(0, 6, _iec.REAL)),
    _iec.IecField('PositiveJointDirection', _iec.ArrayType(0, 6, _iec.BOOL)),
    _iec.IecField('JointZeroPosition', _iec.ArrayType(0, 6, _iec.REAL)),
)
ExecutionModeAllowed._IEC_FIELDS_ = (
    _iec.IecField('PRIMARY_SEQ', _iec.BOOL),
    _iec.IecField('PRIMARY_SEQ_ABORT', _iec.BOOL),
    _iec.IecField('SECONDARY_SEQ', _iec.BOOL),
    _iec.IecField('SECONDARY_SEQ_ABORT', _iec.BOOL),
    _iec.IecField('PAR', _iec.BOOL),
    _iec.IecField('PAR_TASK', _iec.BOOL),
    _iec.IecField('PAR_TRIGGER', _iec.BOOL),
    _iec.IecField('PAR_TRIGGER_TASK', _iec.BOOL),
)
ExternalAxesFlags._IEC_FIELDS_ = (
    _iec.IecField('Bit00', _iec.BOOL),
    _iec.IecField('AxisE1', _iec.BOOL),
    _iec.IecField('AxisE2', _iec.BOOL),
    _iec.IecField('AxisE3', _iec.BOOL),
    _iec.IecField('AxisE4', _iec.BOOL),
    _iec.IecField('AxisE5', _iec.BOOL),
    _iec.IecField('AxisE6', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
)
ForceStatus._IEC_FIELDS_ = (
    _iec.IecField('ForceControlEnabled', _iec.BOOL),
    _iec.IecField('ForceLimitEnabled', _iec.BOOL),
    _iec.IecField('ApplyingForce', _iec.BOOL),
    _iec.IecField('MaxDeviationReached', _iec.BOOL),
    _iec.IecField('SpecifiedForceTorqueReached', _iec.BOOL),
    _iec.IecField('SpecifiedForceLimitReached', _iec.BOOL),
    _iec.IecField('Bit06', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
)
FragmentAction._IEC_FIELDS_ = (
    _iec.IecField('Complete', _iec.BOOL),
    _iec.IecField('Reset', _iec.BOOL),
    _iec.IecField('Clear', _iec.BOOL),
    _iec.IecField('BIT03', _iec.BOOL),
    _iec.IecField('BIT04', _iec.BOOL),
    _iec.IecField('BIT05', _iec.BOOL),
    _iec.IecField('BIT06', _iec.BOOL),
    _iec.IecField('BIT07', _iec.BOOL),
)
JogControl._IEC_FIELDS_ = (
    _iec.IecField('X_J1_Pos', _iec.BOOL),
    _iec.IecField('X_J1_Neg', _iec.BOOL),
    _iec.IecField('Y_J2_Pos', _iec.BOOL),
    _iec.IecField('Y_J2_Neg', _iec.BOOL),
    _iec.IecField('Z_J3_Pos', _iec.BOOL),
    _iec.IecField('Z_J3_Neg', _iec.BOOL),
    _iec.IecField('Rx_J4_Pos', _iec.BOOL),
    _iec.IecField('Rx_J4_Neg', _iec.BOOL),
    _iec.IecField('Ry_J5_Pos', _iec.BOOL),
    _iec.IecField('Ry_J5_Neg', _iec.BOOL),
    _iec.IecField('Rz_J6_Pos', _iec.BOOL),
    _iec.IecField('Rz_J6_Neg', _iec.BOOL),
    _iec.IecField('E1_Pos', _iec.BOOL),
    _iec.IecField('E1_Neg', _iec.BOOL),
    _iec.IecField('E2_Pos', _iec.BOOL),
    _iec.IecField('E2_Neg', _iec.BOOL),
    _iec.IecField('E3_Pos', _iec.BOOL),
    _iec.IecField('E3_Neg', _iec.BOOL),
    _iec.IecField('E4_Pos', _iec.BOOL),
    _iec.IecField('E4_Neg', _iec.BOOL),
    _iec.IecField('E5_Pos', _iec.BOOL),
    _iec.IecField('E5_Neg', _iec.BOOL),
    _iec.IecField('E6_Pos', _iec.BOOL),
    _iec.IecField('E6_Neg', _iec.BOOL),
)
MeasuringInputResult._IEC_FIELDS_ = (
    _iec.IecField('MeasuredCartesianPosition', _iec.StructType(RobotCartesianPosition)),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('MeasuredJointPosition', _iec.StructType(RobotJointPosition)),
)
ProcessingModeAllowed._IEC_FIELDS_ = (
    _iec.IecField('BUFFERED', _iec.BOOL),
    _iec.IecField('ABORTING', _iec.BOOL),
    _iec.IecField('PARALLEL', _iec.BOOL),
    _iec.IecField('CONTINUOUS', _iec.BOOL),
    _iec.IecField('DEACTIVATE', _iec.BOOL),
    _iec.IecField('TRIGGER_BUFFERED', _iec.BOOL),
    _iec.IecField('TRIGGER_ABORTING', _iec.BOOL),
    _iec.IecField('TRIGGER_ONCE', _iec.BOOL),
    _iec.IecField('TRIGGER_CONTINUOUS', _iec.BOOL),
    _iec.IecField('TRIGGER_MULTIPLE', _iec.BOOL),
)
RaStatusWord._IEC_FIELDS_ = (
    _iec.IecField('IsMoving', _iec.BOOL),
    _iec.IecField('PrimarySequencePaused', _iec.BOOL),
    _iec.IecField('InPrimaryPos', _iec.BOOL),
    _iec.IecField('SecondarySequenceActive', _iec.BOOL),
    _iec.IecField('IsBlending', _iec.BOOL),
    _iec.IecField('ErrorPending', _iec.BOOL),
    _iec.IecField('RestartInProgress', _iec.BOOL),
    _iec.IecField('Enabled', _iec.BOOL),
    _iec.IecField('RaSequenceState', _iec.EnumType(_e.RaSequenceState)),
    _iec.IecField('OperationMode', _iec.EnumType(_e.OperationMode)),
    _iec.IecField('CollisionDetectedEnabled', _iec.BOOL),
    _iec.IecField('CollisionDetected', _iec.BOOL),
    _iec.IecField('RestartRequested', _iec.BOOL),
    _iec.IecField('Accelerating', _iec.BOOL),
    _iec.IecField('Decelerating', _iec.BOOL),
    _iec.IecField('ConstantVelocity', _iec.BOOL),
    _iec.IecField('Bit19', _iec.BOOL),
    _iec.IecField('Bit20', _iec.BOOL),
    _iec.IecField('Bit21', _iec.BOOL),
    _iec.IecField('Bit22', _iec.BOOL),
    _iec.IecField('Bit23', _iec.BOOL),
    _iec.IecField('Bit24', _iec.BOOL),
    _iec.IecField('Bit25', _iec.BOOL),
    _iec.IecField('Bit26', _iec.BOOL),
    _iec.IecField('Bit27', _iec.BOOL),
    _iec.IecField('Bit28', _iec.BOOL),
    _iec.IecField('Bit29', _iec.BOOL),
    _iec.IecField('Bit30', _iec.BOOL),
    _iec.IecField('Bit31', _iec.BOOL),
)
RCSupportedFunctions._IEC_FIELDS_ = (
    _iec.IecField('Reserved', _iec.BOOL),
    _iec.IecField('ReadRobotData', _iec.BOOL),
    _iec.IecField('EnableRobot', _iec.BOOL),
    _iec.IecField('GroupReset', _iec.BOOL),
    _iec.IecField('ReadActualPosition', _iec.BOOL),
    _iec.IecField('ReadActualPositionCyclic', _iec.BOOL),
    _iec.IecField('ExchangeConfiguration', _iec.BOOL),
    _iec.IecField('SetSequence', _iec.BOOL),
    _iec.IecField('ChangeSpeedOverride', _iec.BOOL),
    _iec.IecField('ReadMessages', _iec.BOOL),
    _iec.IecField('ReadRobotReferenceDynamics', _iec.BOOL),
    _iec.IecField('WriteFrameData', _iec.BOOL),
    _iec.IecField('WriteToolData', _iec.BOOL),
    _iec.IecField('WriteLoadData', _iec.BOOL),
    _iec.IecField('WriteRobotReferenceDynamics', _iec.BOOL),
    _iec.IecField('WriteRobotDefaultDynamics', _iec.BOOL),
    _iec.IecField('ReadRobotDefaultDynamics', _iec.BOOL),
    _iec.IecField('ReadFrameData', _iec.BOOL),
    _iec.IecField('ReadToolData', _iec.BOOL),
    _iec.IecField('ReadLoadData', _iec.BOOL),
    _iec.IecField('ReadRobotSWLimits', _iec.BOOL),
    _iec.IecField('GroupJog', _iec.BOOL),
    _iec.IecField('MoveLinearAbsolute', _iec.BOOL),
    _iec.IecField('MoveDirectAbsolute', _iec.BOOL),
    _iec.IecField('MoveAxesAbsolute', _iec.BOOL),
    _iec.IecField('GroupStop', _iec.BOOL),
    _iec.IecField('GroupContinue', _iec.BOOL),
    _iec.IecField('GroupInterrupt', _iec.BOOL),
    _iec.IecField('ReturnToPrimary', _iec.BOOL),
    _iec.IecField('MoveLinearAbsoluteJ', _iec.BOOL),
    _iec.IecField('MoveDirectRelative', _iec.BOOL),
    _iec.IecField('MoveAxesRelative', _iec.BOOL),
    _iec.IecField('MoveCircularAbsolute', _iec.BOOL),
    _iec.IecField('MoveCircularRelative', _iec.BOOL),
    _iec.IecField('MoveLinearOffset', _iec.BOOL),
    _iec.IecField('MoveDirectOffset', _iec.BOOL),
    _iec.IecField('WaitTime', _iec.BOOL),
    _iec.IecField('ReadDigitalInputs', _iec.BOOL),
    _iec.IecField('ReadDigitalOutputs', _iec.BOOL),
    _iec.IecField('WriteDigitalOutputs', _iec.BOOL),
    _iec.IecField('ReadIntegers', _iec.BOOL),
    _iec.IecField('ReadReals', _iec.BOOL),
    _iec.IecField('WriteIntegers', _iec.BOOL),
    _iec.IecField('WriteReals', _iec.BOOL),
    _iec.IecField('MoveLinearCam', _iec.BOOL),
    _iec.IecField('MoveDirectCam', _iec.BOOL),
    _iec.IecField('MoveCircularCam', _iec.BOOL),
    _iec.IecField('SetTriggerRegister', _iec.BOOL),
    _iec.IecField('SetTriggerLimit', _iec.BOOL),
    _iec.IecField('SetTriggerUser', _iec.BOOL),
    _iec.IecField('SetTriggerError', _iec.BOOL),
    _iec.IecField('ReactAtTrigger', _iec.BOOL),
    _iec.IecField('WaitForTrigger', _iec.BOOL),
    _iec.IecField('ReadSystemVariable', _iec.BOOL),
    _iec.IecField('WriteSystemVariable', _iec.BOOL),
    _iec.IecField('CalculateForwardKinematic', _iec.BOOL),
    _iec.IecField('CalculateInverseKinematic', _iec.BOOL),
    _iec.IecField('CalculateCartesianPosition', _iec.BOOL),
    _iec.IecField('CalculateTool', _iec.BOOL),
    _iec.IecField('CalculateFrame', _iec.BOOL),
    _iec.IecField('ActivateNextCommand', _iec.BOOL),
    _iec.IecField('ShiftPosition', _iec.BOOL),
    _iec.IecField('CallSubprogram', _iec.BOOL),
    _iec.IecField('MoveLinearRelative', _iec.BOOL),
    _iec.IecField('WriteCallSubprogramCyclic', _iec.BOOL),
    _iec.IecField('ReadCallSubprogramCyclic', _iec.BOOL),
    _iec.IecField('StopSubprogram', _iec.BOOL),
    _iec.IecField('ReadDHParameter', _iec.BOOL),
    _iec.IecField('RestartController', _iec.BOOL),
    _iec.IecField('ReadActualTCPVelocity', _iec.BOOL),
    _iec.IecField('UserLogin', _iec.BOOL),
    _iec.IecField('SwitchLanguage', _iec.BOOL),
    _iec.IecField('WriteRobotSWLimits', _iec.BOOL),
    _iec.IecField('SetOperationMode', _iec.BOOL),
    _iec.IecField('ReadWorkArea', _iec.BOOL),
    _iec.IecField('WriteWorkArea', _iec.BOOL),
    _iec.IecField('ActivateWorkArea', _iec.BOOL),
    _iec.IecField('MonitorWorkArea', _iec.BOOL),
    _iec.IecField('MoveApproachLinear', _iec.BOOL),
    _iec.IecField('MoveDepartLinear', _iec.BOOL),
    _iec.IecField('MoveApproachDirect', _iec.BOOL),
    _iec.IecField('MoveDepartDirect', _iec.BOOL),
    _iec.IecField('SearchHardstop', _iec.BOOL),
    _iec.IecField('SearchHardstopJ', _iec.BOOL),
    _iec.IecField('MovePickPlaceLinear', _iec.BOOL),
    _iec.IecField('MovePickPlaceDirect', _iec.BOOL),
    _iec.IecField('ActivateConveyorTracking', _iec.BOOL),
    _iec.IecField('RedefineTrackingPosition', _iec.BOOL),
    _iec.IecField('SyncToConveyor', _iec.BOOL),
    _iec.IecField('ConfigureConveyor', _iec.BOOL),
    _iec.IecField('MoveSuperImposed', _iec.BOOL),
    _iec.IecField('MoveSuperImposedDynamic', _iec.BOOL),
    _iec.IecField('ReadAnalogInput', _iec.BOOL),
    _iec.IecField('ReadAnalogOutput', _iec.BOOL),
    _iec.IecField('WriteAnalogOutput', _iec.BOOL),
    _iec.IecField('MeasuringInput', _iec.BOOL),
    _iec.IecField('AbortMeasuringInput', _iec.BOOL),
    _iec.IecField('SetTriggerMotion', _iec.BOOL),
    _iec.IecField('OpenBrake', _iec.BOOL),
    _iec.IecField('PathAccuracyMode', _iec.BOOL),
    _iec.IecField('AvoidSingularity', _iec.BOOL),
    _iec.IecField('ForceControl', _iec.BOOL),
    _iec.IecField('ForceLimit', _iec.BOOL),
    _iec.IecField('ReadActualForce', _iec.BOOL),
    _iec.IecField('BrakeTest', _iec.BOOL),
    _iec.IecField('SoftSwitchTCP', _iec.BOOL),
    _iec.IecField('CreateSpline', _iec.BOOL),
    _iec.IecField('DeleteSpline', _iec.BOOL),
    _iec.IecField('MoveSpline', _iec.BOOL),
    _iec.IecField('DynamicSpline', _iec.BOOL),
    _iec.IecField('LoadMeasurementAutomatic', _iec.BOOL),
    _iec.IecField('LoadMeasurementSequential', _iec.BOOL),
    _iec.IecField('CollisionDetection', _iec.BOOL),
    _iec.IecField('FreeDrive', _iec.BOOL),
    _iec.IecField('UnitMeasurement', _iec.BOOL),
    _iec.IecField('Byte14Bit03', _iec.BOOL),
    _iec.IecField('Byte14Bit04', _iec.BOOL),
    _iec.IecField('Byte14Bit05', _iec.BOOL),
    _iec.IecField('Byte14Bit06', _iec.BOOL),
    _iec.IecField('Byte14Bit07', _iec.BOOL),
    _iec.IecField('Byte15Bit00', _iec.BOOL),
    _iec.IecField('Byte15Bit01', _iec.BOOL),
    _iec.IecField('Byte15Bit02', _iec.BOOL),
    _iec.IecField('Byte15Bit03', _iec.BOOL),
    _iec.IecField('Byte15Bit04', _iec.BOOL),
    _iec.IecField('Byte15Bit05', _iec.BOOL),
    _iec.IecField('Byte15Bit06', _iec.BOOL),
    _iec.IecField('Byte15Bit07', _iec.BOOL),
    _iec.IecField('Byte16Bit00', _iec.BOOL),
    _iec.IecField('Byte16Bit01', _iec.BOOL),
    _iec.IecField('Byte16Bit02', _iec.BOOL),
    _iec.IecField('Byte16Bit03', _iec.BOOL),
    _iec.IecField('Byte16Bit04', _iec.BOOL),
    _iec.IecField('Byte16Bit05', _iec.BOOL),
    _iec.IecField('Byte16Bit06', _iec.BOOL),
    _iec.IecField('Byte16Bit07', _iec.BOOL),
    _iec.IecField('Byte17Bit00', _iec.BOOL),
    _iec.IecField('Byte17Bit01', _iec.BOOL),
    _iec.IecField('Byte17Bit02', _iec.BOOL),
    _iec.IecField('Byte17Bit03', _iec.BOOL),
    _iec.IecField('Byte17Bit04', _iec.BOOL),
    _iec.IecField('Byte17Bit05', _iec.BOOL),
    _iec.IecField('Byte17Bit06', _iec.BOOL),
    _iec.IecField('Byte17Bit07', _iec.BOOL),
    _iec.IecField('Byte18Bit00', _iec.BOOL),
    _iec.IecField('Byte18Bit01', _iec.BOOL),
    _iec.IecField('Byte18Bit02', _iec.BOOL),
    _iec.IecField('Byte18Bit03', _iec.BOOL),
    _iec.IecField('Byte18Bit04', _iec.BOOL),
    _iec.IecField('Byte18Bit05', _iec.BOOL),
    _iec.IecField('Byte18Bit06', _iec.BOOL),
    _iec.IecField('Byte18Bit07', _iec.BOOL),
)
RobotAxesFlags._IEC_FIELDS_ = (
    _iec.IecField('Bit00', _iec.BOOL),
    _iec.IecField('AxisJ1', _iec.BOOL),
    _iec.IecField('AxisJ2', _iec.BOOL),
    _iec.IecField('AxisJ3', _iec.BOOL),
    _iec.IecField('AxisJ4', _iec.BOOL),
    _iec.IecField('AxisJ5', _iec.BOOL),
    _iec.IecField('AxisJ6', _iec.BOOL),
    _iec.IecField('Bit07', _iec.BOOL),
)
SWLimits._IEC_FIELDS_ = (
    _iec.IecField('Timestamp', _iec.StructType(IEC_TIMESTAMP)),
    _iec.IecField('J1LowerLimit', _iec.REAL),
    _iec.IecField('J1UpperLimit', _iec.REAL),
    _iec.IecField('J2LowerLimit', _iec.REAL),
    _iec.IecField('J2UpperLimit', _iec.REAL),
    _iec.IecField('J3LowerLimit', _iec.REAL),
    _iec.IecField('J3UpperLimit', _iec.REAL),
    _iec.IecField('J4LowerLimit', _iec.REAL),
    _iec.IecField('J4UpperLimit', _iec.REAL),
    _iec.IecField('J5LowerLimit', _iec.REAL),
    _iec.IecField('J5UpperLimit', _iec.REAL),
    _iec.IecField('J6LowerLimit', _iec.REAL),
    _iec.IecField('J6UpperLimit', _iec.REAL),
    _iec.IecField('E1LowerLimit', _iec.REAL),
    _iec.IecField('E1UpperLimit', _iec.REAL),
    _iec.IecField('E2LowerLimit', _iec.REAL),
    _iec.IecField('E2UpperLimit', _iec.REAL),
    _iec.IecField('E3LowerLimit', _iec.REAL),
    _iec.IecField('E3UpperLimit', _iec.REAL),
    _iec.IecField('E4LowerLimit', _iec.REAL),
    _iec.IecField('E4UpperLimit', _iec.REAL),
    _iec.IecField('E5LowerLimit', _iec.REAL),
    _iec.IecField('E5UpperLimit', _iec.REAL),
    _iec.IecField('E6LowerLimit', _iec.REAL),
    _iec.IecField('E6UpperLimit', _iec.REAL),
)
SynchronizationModes._IEC_FIELDS_ = (
    _iec.IecField('Tool', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
    _iec.IecField('Frame', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
    _iec.IecField('Load', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
    _iec.IecField('WorkAreas', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
    _iec.IecField('SWLimits', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
    _iec.IecField('DefaultDynamics', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
    _iec.IecField('ReferenceDynamics', _iec.ArrayType(0, 1, _iec.EnumType(_e.SyncMode))),
)
SyncUserInteraction._IEC_FIELDS_ = (
    _iec.IecField('Tool', _iec.BOOL),
    _iec.IecField('Frame', _iec.BOOL),
    _iec.IecField('Load', _iec.BOOL),
    _iec.IecField('WorkAreas', _iec.BOOL),
    _iec.IecField('SWLimits', _iec.BOOL),
    _iec.IecField('DefaultDynamics', _iec.BOOL),
    _iec.IecField('ReferenceDynamics', _iec.BOOL),
)
TrackingStatus._IEC_FIELDS_ = (
    _iec.IecField('ConveyorTrackingEnabled', _iec.BOOL),
    _iec.IecField('WaitingForSynchronization', _iec.BOOL),
    _iec.IecField('Synchronizing', _iec.BOOL),
    _iec.IecField('Synchronous', _iec.BOOL),
    _iec.IecField('Desynchronizing', _iec.BOOL),
    _iec.IecField('SyncOutZoneEntered', _iec.BOOL),
    _iec.IecField('SyncOutZoneLeft', _iec.BOOL),
    _iec.IecField('NotUsed', _iec.BOOL),
)
TurnNumber._IEC_FIELDS_ = (
    _iec.IecField('J1Turns', _iec.SINT),
    _iec.IecField('J2Turns', _iec.SINT),
    _iec.IecField('J3Turns', _iec.SINT),
    _iec.IecField('J4Turns', _iec.SINT),
    _iec.IecField('J5Turns', _iec.SINT),
    _iec.IecField('J6Turns', _iec.SINT),
    _iec.IecField('E1Turns', _iec.SINT),
)
VersionStruct._IEC_FIELDS_ = (
    _iec.IecField('MajorVersion', _iec.USINT),
    _iec.IecField('MinorVersion', _iec.USINT),
    _iec.IecField('PatchVersion', _iec.USINT),
)
TelegramPlcToRobCommand._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramPlcToRobCommandHeader)),
    _iec.IecField('Payload', _iec.ArrayType(0, _iec.Param('PARAMETER_PAYLOAD_MAX'), _iec.BYTE)),
)
TelegramPlcToRobCommandHeader._IEC_FIELDS_ = (
    _iec.IecField('CmdType', _iec.EnumType(_e.CmdType)),
    _iec.IecField('Prio', _iec.EnumType(_e.PriorityLevel)),
    _iec.IecField('ExecMode', _iec.EnumType(_e.ExecutionMode)),
    _iec.IecField('ParSequence', _iec.BYTE),
)
TelegramPlcToRobCyclicData._IEC_FIELDS_ = (
    _iec.IecField('ToolNo', _iec.BYTE),
    _iec.IecField('FrameNo', _iec.BYTE),
)
TelegramPlcToRobCyclicOptionalCartesianPosition._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
    _iec.IecField('Config', _iec.WORD),
    _iec.IecField('Turns_J2_J1', _iec.BYTE),
    _iec.IecField('Turns_J4_J3', _iec.BYTE),
    _iec.IecField('Turns_J6_J5', _iec.BYTE),
    _iec.IecField('Turns_E1', _iec.BYTE),
    _iec.IecField('E1', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalCartesianPositionExt._IEC_FIELDS_ = (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalCurrent._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalCurrentExt._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalForce._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalForceExt._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalJointPosition._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
    _iec.IecField('E1', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalJointPositionExt._IEC_FIELDS_ = (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramPlcToRobCyclicOptionalSubProgramData._IEC_FIELDS_ = (
    _iec.IecField('Data', _iec.ArrayType(0, 25, _iec.BYTE)),
)
TelegramPlcToRobCyclicOptionalData._IEC_FIELDS_ = (
    _iec.IecField('SubProgramData', _iec.StructType(TelegramPlcToRobCyclicOptionalSubProgramData)),
    _iec.IecField('CartesianPosition', _iec.StructType(TelegramPlcToRobCyclicOptionalCartesianPosition)),
    _iec.IecField('CartesianPositionExt', _iec.StructType(TelegramPlcToRobCyclicOptionalCartesianPositionExt)),
    _iec.IecField('JointPosition', _iec.StructType(TelegramPlcToRobCyclicOptionalJointPosition)),
    _iec.IecField('JointPositionExt', _iec.StructType(TelegramPlcToRobCyclicOptionalJointPositionExt)),
    _iec.IecField('Force', _iec.StructType(TelegramPlcToRobCyclicOptionalForce)),
    _iec.IecField('ForceExt', _iec.StructType(TelegramPlcToRobCyclicOptionalForceExt)),
    _iec.IecField('Current', _iec.StructType(TelegramPlcToRobCyclicOptionalCurrent)),
    _iec.IecField('CurrentExt', _iec.StructType(TelegramPlcToRobCyclicOptionalCurrentExt)),
)
TelegramPlcToRobFooter._IEC_FIELDS_ = (
    _iec.IecField('LifeSign', _iec.BYTE),
    _iec.IecField('Reserve', _iec.BYTE),
)
TelegramPlcToRobFragment._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramPlcToRobFragmentHeader)),
    _iec.IecField('Command', _iec.StructType(TelegramPlcToRobCommand)),
)
TelegramPlcToRobFragmentHeader._IEC_FIELDS_ = (
    _iec.IecField('CmdID', _iec.UINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('FragmentAction', _iec.BYTE),
    _iec.IecField('PayloadPointer', _iec.UINT),
    _iec.IecField('PayloadLength', _iec.UINT),
)
TelegramPlcToRobHeader._IEC_FIELDS_ = (
    _iec.IecField('SRCIVersion', _iec.BYTE),
    _iec.IecField('FastStop_LifeSign', _iec.BYTE),
    _iec.IecField('TelegramLengthPlcToRob', _iec.UINT),
    _iec.IecField('TelegramLengthRobToPlc', _iec.UINT),
    _iec.IecField('AxesGroupID_Control', _iec.BYTE),
    _iec.IecField('Reserved', _iec.BYTE),
    _iec.IecField('TelegramNumberPlcToRob', _iec.UINT),
    _iec.IecField('TelegramNumberRobToPlc', _iec.UINT),
    _iec.IecField('ClientDate', _iec.UINT),
    _iec.IecField('ClientTime', _iec.TOD),
)
TelegramPlcToRobSequence._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramPlcToRobSequenceHeader)),
    _iec.IecField('Fragment', _iec.ArrayType(0, _iec.Param('FRAGMENT_MAX'), _iec.StructType(TelegramPlcToRobFragment))),
)
TelegramPlcToRobSequenceHeader._IEC_FIELDS_ = (
    _iec.IecField('SEQ_ACK', _iec.UINT),
    _iec.IecField('PayloadLength', _iec.UINT),
)
TelegramPlcToRob._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramPlcToRobHeader)),
    _iec.IecField('Cyclic', _iec.StructType(TelegramPlcToRobCyclicData)),
    _iec.IecField('CyclicOptional', _iec.StructType(TelegramPlcToRobCyclicOptionalData)),
    _iec.IecField('Sequence', _iec.ArrayType(0, 1, _iec.StructType(TelegramPlcToRobSequence))),
    _iec.IecField('Footer', _iec.StructType(TelegramPlcToRobFooter)),
)
TelegramRobToPlcCommand._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramRobToPlcCommandHeader)),
    _iec.IecField('Payload', _iec.ArrayType(0, _iec.Param('RESPONSE_PAYLOAD_MAX'), _iec.BYTE)),
)
TelegramRobToPlcCommandHeader._IEC_FIELDS_ = (
    _iec.IecField('ParSeq', _iec.BYTE),
    _iec.IecField('State', _iec.EnumType(_e.CmdMessageState)),
    _iec.IecField('AlarmMessageSeverity', _iec.SINT),
    _iec.IecField('AlarmMessageCode', _iec.UINT),
)
TelegramRobToPlcCyclicOptionalCartesianPosition._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
    _iec.IecField('Config', _iec.WORD),
    _iec.IecField('Turns_J2_J1', _iec.BYTE),
    _iec.IecField('Turns_J4_J3', _iec.BYTE),
    _iec.IecField('Turns_J6_J5', _iec.BYTE),
    _iec.IecField('Turns_E1', _iec.BYTE),
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('ToolNo', _iec.USINT),
    _iec.IecField('FrameNo', _iec.USINT),
    _iec.IecField('CurrentlyUsedToolNo', _iec.USINT),
    _iec.IecField('CurrentlyUsedFrameNo', _iec.USINT),
    _iec.IecField('Reserve_1', _iec.BYTE),
    _iec.IecField('Reserve_2', _iec.BYTE),
)
TelegramRobToPlcCyclicOptionalCartesianPositionExt._IEC_FIELDS_ = (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramRobToPlcCyclicOptionalCurrent._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
)
TelegramRobToPlcCyclicOptionalCurrentExt._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramRobToPlcCyclicOptionalForce._IEC_FIELDS_ = (
    _iec.IecField('X', _iec.REAL),
    _iec.IecField('Y', _iec.REAL),
    _iec.IecField('Z', _iec.REAL),
    _iec.IecField('Rx', _iec.REAL),
    _iec.IecField('Ry', _iec.REAL),
    _iec.IecField('Rz', _iec.REAL),
)
TelegramRobToPlcCyclicOptionalForceExt._IEC_FIELDS_ = (
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramRobToPlcCyclicOptionalJointPosition._IEC_FIELDS_ = (
    _iec.IecField('J1', _iec.REAL),
    _iec.IecField('J2', _iec.REAL),
    _iec.IecField('J3', _iec.REAL),
    _iec.IecField('J4', _iec.REAL),
    _iec.IecField('J5', _iec.REAL),
    _iec.IecField('J6', _iec.REAL),
    _iec.IecField('E1', _iec.REAL),
    _iec.IecField('E1_Reserve', _iec.WORD),
)
TelegramRobToPlcCyclicOptionalJointPositionExt._IEC_FIELDS_ = (
    _iec.IecField('E2', _iec.REAL),
    _iec.IecField('E3', _iec.REAL),
    _iec.IecField('E4', _iec.REAL),
    _iec.IecField('E5', _iec.REAL),
    _iec.IecField('E6', _iec.REAL),
)
TelegramRobToPlcCyclicOptionalSubProgramData._IEC_FIELDS_ = (
    _iec.IecField('Data', _iec.ArrayType(0, 25, _iec.BYTE)),
)
TelegramRobToPlcCyclicOptionalData._IEC_FIELDS_ = (
    _iec.IecField('SubProgramData', _iec.StructType(TelegramRobToPlcCyclicOptionalSubProgramData)),
    _iec.IecField('CartesianPosition', _iec.StructType(TelegramRobToPlcCyclicOptionalCartesianPosition)),
    _iec.IecField('JointPosition', _iec.StructType(TelegramRobToPlcCyclicOptionalJointPosition)),
    _iec.IecField('Force', _iec.StructType(TelegramRobToPlcCyclicOptionalForce)),
    _iec.IecField('Current', _iec.StructType(TelegramRobToPlcCyclicOptionalCurrent)),
    _iec.IecField('TwoSequences', _iec.BYTE),
    _iec.IecField('CartesianPositionExt', _iec.StructType(TelegramRobToPlcCyclicOptionalCartesianPositionExt)),
    _iec.IecField('JointPositionExt', _iec.StructType(TelegramRobToPlcCyclicOptionalJointPositionExt)),
    _iec.IecField('ForceExt', _iec.StructType(TelegramRobToPlcCyclicOptionalCurrentExt)),
    _iec.IecField('CurrentExt', _iec.StructType(TelegramRobToPlcCyclicOptionalCurrentExt)),
)
TelegramRobToPlcFooter._IEC_FIELDS_ = (
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('LifeSign', _iec.BYTE),
)
TelegramRobToPlcFragment._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramRobToPlcFragmentHeader)),
    _iec.IecField('Command', _iec.StructType(TelegramRobToPlcCommand)),
)
TelegramRobToPlcFragmentHeader._IEC_FIELDS_ = (
    _iec.IecField('CmdID', _iec.UINT),
    _iec.IecField('Reserve', _iec.BYTE),
    _iec.IecField('FragmentAction', _iec.BYTE),
    _iec.IecField('PayloadPointer', _iec.UINT),
    _iec.IecField('PayloadLength', _iec.UINT),
)
TelegramRobToPlcHeader._IEC_FIELDS_ = (
    _iec.IecField('SRCIVersion', _iec.StructType(VersionStruct)),
    _iec.IecField('LifeSign', _iec.BYTE),
    _iec.IecField('Reserved', _iec.BYTE),
    _iec.IecField('TelegramState', _iec.EnumType(_e.TelegramState)),
    _iec.IecField('StatusRobotArm', _iec.DWORD),
    _iec.IecField('Override', _iec.UINT),
)
TelegramRobToPlcSequence._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramRobToPlcSequenceHeader)),
    _iec.IecField('Fragment', _iec.ArrayType(0, _iec.Param('FRAGMENT_MAX'), _iec.StructType(TelegramRobToPlcFragment))),
)
TelegramRobToPlcSequenceHeader._IEC_FIELDS_ = (
    _iec.IecField('SEQ_ACK', _iec.UINT),
    _iec.IecField('PayloadLength', _iec.UINT),
)
TelegramRobToPlc._IEC_FIELDS_ = (
    _iec.IecField('Header', _iec.StructType(TelegramRobToPlcHeader)),
    _iec.IecField('CyclicOptional', _iec.StructType(TelegramRobToPlcCyclicOptionalData)),
    _iec.IecField('Sequence', _iec.ArrayType(0, 1, _iec.StructType(TelegramRobToPlcSequence))),
    _iec.IecField('Footer', _iec.StructType(TelegramRobToPlcFooter)),
)
Telegram._IEC_FIELDS_ = (
    _iec.IecField('PlcToRob', _iec.StructType(TelegramPlcToRob)),
    _iec.IecField('RobToPlc', _iec.StructType(TelegramRobToPlc)),
)
