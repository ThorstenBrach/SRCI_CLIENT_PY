# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_CollisionDetectionFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Turn on/off the collision detection
#
#  Copyright:
#    (C) 2024 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Turn on/off the collision detection

ST-Source: POUs/Additional/MC_CollisionDetection/MC_CollisionDetectionFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from srci.fb._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from srci.functions.Common import SetTimeout
from srci.functions.Convert.Misc import REAL_TO_PERCENT_INT
from srci.functions.Convert.TO_STRING.COLLISION_REACTION_MODE_TO_STRING import COLLISION_REACTION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.PROCESSING_MODE_TO_STRING import PROCESSING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.SEQUENCE_FLAG_TO_STRING import SEQUENCE_FLAG_TO_STRING
from srci.functions.Convert.TO_STRING.THRESHOLD_MODE_TO_STRING import THRESHOLD_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING, INT_TO_STRING, REAL_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, st_for_end, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, CollisionDetectionOutCmd, CollisionDetectionParCmd, CollisionDetectionRecvData, CollisionDetectionSendData, CollisionReactionMode, ExecutionMode, MessageType, PriorityLevel, ProcessingMode, ProcessingModeEnum, RobotLibraryConstants, RobotLibraryErrorIdEnum, SequenceFlag, SequenceFlagEnum, Severity, SystemTime, ThresholdMode, UnitLimitAxis

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_CollisionDetectionFB']


class MC_CollisionDetectionFB(RobotLibraryBaseExecuteFB):
    """Turn on/off the collision detection"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Processing mode
        self.ProcessingMode: ProcessingMode = ProcessingMode.BUFFERED
        # Defines the target sequence in which the command will be executed
        self.SequenceFlag: SequenceFlag = SequenceFlag.NO_SEQUENCE
        # Command parameter
        self.ParCmd: CollisionDetectionParCmd = CollisionDetectionParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The command was aborted by another command.
        self.CommandAborted: bool = False
        # TRUE, while command is interrupted during execution and can be continued
        self.CommandInterrupted: bool = False
        # command results
        self.OutCmd: CollisionDetectionOutCmd = CollisionDetectionOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: CollisionDetectionParCmd = CollisionDetectionParCmd()
        # command data to send
        self._command: CollisionDetectionSendData = CollisionDetectionSendData()
        # response data received
        self._response: CollisionDetectionRecvData = CollisionDetectionRecvData()

    def __call__(self, *, ProcessingMode: ProcessingMode | None = None, SequenceFlag: SequenceFlag | None = None, ParCmd: CollisionDetectionParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ProcessingMode is not None:
            self.ProcessingMode = ProcessingMode(ProcessingMode)
        if SequenceFlag is not None:
            self.SequenceFlag = SequenceFlag(SequenceFlag)
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
        if Execute is not None:
            self.Execute = Execute
        if Name is not None:
            self.Name = trunc_str(Name, 80)
        if ExecMode is not None:
            self.ExecMode = ExecutionMode(ExecMode)
        if Priority is not None:
            self.Priority = PriorityLevel(Priority)
        if AxesGroup is not None:
            self.AxesGroup = AxesGroup
        if InternalLogger is not None:
            self.InternalLogger = InternalLogger
        if ExternalLogger is not None:
            self.ExternalLogger = ExternalLogger
        if LogLevel is not None:
            self.LogLevel = Severity(LogLevel)
        self.__body()

    def __body(self) -> None:
        super().__call__(AxesGroup=self.AxesGroup)

    def CheckAddParameter(self, *, PayloadPtr: int = 0) -> bool:  # INTERNAL
        CheckAddParameter: bool = False
        # Payload as byte array
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 53)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 53)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 53 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 53, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(CollisionDetectionSendData)), DataLen=53)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 53 - PayloadPtr, 53)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 53, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 53, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.CollisionDetection

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 66 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(CollisionDetectionParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(CollisionDetectionParCmd)), DataLen=66) != RobotLibraryConstants.OK

        # check parameter valid ?
        self._parameterValid = self.CheckParameterValid(AxesGroup=AxesGroup)

        if self._parameterChanged and self._parameterValid or self._parameterUpdateInternal:
            # Create log entry for parameter changed event
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='NotifyParameterChanged Event {1}', Para1='')

            # reset internal flag for send parameter update
            self._parameterUpdateInternal = False
            # update internal copy of parameters
            copy_into(self._parCmd, self.ParCmd)
            # inc parameter sequence
            self._command.ParSeq = wrap(self._command.ParSeq + 1, 'BYTE')
            # update command data
            self.CommandData = self.CreateCommandPayload(AxesGroup=AxesGroup)  # ( Access via reference to rCommandFB in ACR )
            # notify active command register
            AxesGroup.Acyclic.ActiveCommandRegister.NotifyParameterChanged = self._uniqueID
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False
        # internal index for loops
        _idx: int = 0

        CheckParameterValid = True

        # Check ParCmd.ProcessingMode defined ?
        # ST-FIX F26
        if self.ProcessingMode < ProcessingMode.BUFFERED or self.ProcessingMode > ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check ProcessingMode valid ?
        if (self.ProcessingMode != ProcessingMode.BUFFERED and self.ProcessingMode != ProcessingMode.ABORTING) and self.ProcessingMode != ProcessingMode.PARALLEL:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check SequenceFlag valid ?
        # ST-FIX F69: default with Parallel
        if (self.SequenceFlag != SequenceFlag.NO_SEQUENCE and self.SequenceFlag != SequenceFlag.PRIMARY_SEQUENCE) and self.SequenceFlag != SequenceFlag.SECONDARY_SEQUENCE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter SequenceFlag = {1}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.SequenceFlag))
            return CheckParameterValid

        # Check ParCmd.ReactionMode valid ?
        if self.ParCmd.ReactionMode < CollisionReactionMode.STANDING_STILL or self.ParCmd.ReactionMode > CollisionReactionMode.REVERSED_MOVEMENT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReactionMode = {1}', Para1=COLLISION_REACTION_MODE_TO_STRING(Value=self.ParCmd.ReactionMode))
            return CheckParameterValid

        # Check ParCmd.ThresholdMode valid ?
        if self.ParCmd.ThresholdMode != ThresholdMode.AUTOMATIC and self.ParCmd.ThresholdMode != ThresholdMode.MANUAL:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ThresholdMode = {1}', Para1=THRESHOLD_MODE_TO_STRING(Value=self.ParCmd.ThresholdMode))
            return CheckParameterValid

        # Check ParCmd.Sensitivity valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.Sensitivity) == False or self.ParCmd.Sensitivity < 0) or self.ParCmd.Sensitivity > 200:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Sensitivity = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Sensitivity))
            return CheckParameterValid

        for _idx in range(0, 7):
            # Check ParCmd.SensitivityAxis valid ?
            if (SysDepIsValidReal(Value=self.ParCmd.SensitivityAxis[_idx]) == False or self.ParCmd.SensitivityAxis[_idx] < 0) or self.ParCmd.SensitivityAxis[_idx] > 200:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SensitivityAxis[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SensitivityAxis[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 6)

        for _idx in range(0, 7):
            # Check ParCmd.LimitAxis valid ?
            if SysDepIsValidReal(Value=self.ParCmd.LimitAxis[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitAxis[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitAxis[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

        # Check ParCmd.UnitLimitAxis valid ?
        if (self.ParCmd.UnitLimitAxis != UnitLimitAxis.PERCENTAGE and self.ParCmd.UnitLimitAxis != UnitLimitAxis.NEWTONMETER) and self.ParCmd.UnitLimitAxis != UnitLimitAxis.MILLIAMPERE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.UnitLimitAxis = {1}', Para1=THRESHOLD_MODE_TO_STRING(Value=ThresholdMode(self.ParCmd.UnitLimitAxis)))
            return CheckParameterValid

        # ST-FIX F69: trigger IDs and SequenceFlag (table 7-1, 5.5.12.4, e.g. table 6-496)
        if CheckParameterValid and (((self.ProcessingMode == ProcessingMode.BUFFERED or self.ProcessingMode == ProcessingMode.ABORTING) or self.ProcessingMode == ProcessingMode.TRIGGER_BUFFERED) or self.ProcessingMode == ProcessingMode.TRIGGER_ABORTING) == (self.SequenceFlag == SequenceFlag.NO_SEQUENCE):
            CheckParameterValid = False
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SEQFLAG_INVALID_IN_PROC_MODE, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter SequenceFlag = {1} with ProcessingMode = {2}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.SequenceFlag), Para2=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # ST-FIX F49: ParCmd.ProcessingMode was not checked
        if ((((((((self.ParCmd.ProcessingMode != ProcessingMode.BUFFERED and self.ParCmd.ProcessingMode != ProcessingMode.ABORTING) and self.ParCmd.ProcessingMode != ProcessingMode.PARALLEL) and self.ParCmd.ProcessingMode != ProcessingMode.CONTINUOUS) and self.ParCmd.ProcessingMode != ProcessingMode.DEACTIVATE) and self.ParCmd.ProcessingMode != ProcessingMode.TRIGGER_BUFFERED) and self.ParCmd.ProcessingMode != ProcessingMode.TRIGGER_ABORTING) and self.ParCmd.ProcessingMode != ProcessingMode.TRIGGER_ONCE) and self.ParCmd.ProcessingMode != ProcessingMode.TRIGGER_CONTINUOUS) and self.ParCmd.ProcessingMode != ProcessingMode.TRIGGER_MULTIPLE:
            CheckParameterValid = False
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ParCmd.ProcessingMode))
            return CheckParameterValid

        # ST-FIX F49: ParCmd.SequenceFlag was not checked
        if (self.ParCmd.SequenceFlag != SequenceFlag.NO_SEQUENCE and self.ParCmd.SequenceFlag != SequenceFlag.PRIMARY_SEQUENCE) and self.ParCmd.SequenceFlag != SequenceFlag.SECONDARY_SEQUENCE:
            CheckParameterValid = False
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SequenceFlag = {1}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.ParCmd.SequenceFlag))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0
        # internal index for loops
        _idx: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.CollisionDetection
        # ST-FIX F51: ExecutionMode from ProcessingMode (and SequenceFlag), spec table 5-77
        match self.ProcessingMode:
            case ProcessingMode.BUFFERED | ProcessingMode.TRIGGER_BUFFERED:
                if self.SequenceFlag == SequenceFlag.SECONDARY_SEQUENCE:
                    self._command.ExecMode = ExecutionMode.SEQUENCE_SECONDARY
                else:
                    self._command.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
            case ProcessingMode.ABORTING | ProcessingMode.TRIGGER_ABORTING:
                if self.SequenceFlag == SequenceFlag.SECONDARY_SEQUENCE:
                    self._command.ExecMode = ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY
                else:
                    self._command.ExecMode = ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY
            case ProcessingMode.PARALLEL | ProcessingMode.TRIGGER_ONCE:
                self._command.ExecMode = ExecutionMode.PARALLEL
            case ProcessingMode.CONTINUOUS | ProcessingMode.TRIGGER_CONTINUOUS:
                self._command.ExecMode = ExecutionMode.CONTINUOUS
            case ProcessingMode.TRIGGER_MULTIPLE:
                self._command.ExecMode = ExecutionMode.TRIGGER_MULTIPLE
            case ProcessingMode.DEACTIVATE:
                self._command.ExecMode = ExecutionMode.STOP_PARALLEL_CONTINUOUS_TRIGGER
            case _:
                # undefined ProcessingMode -> error, not sent (ST-FIX F49)
                self._command.ExecMode = self.ExecMode
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
                self.OnUpdateStateFlags(State=CmdMessageState.ERROR)
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        self._command.ActivateMonitoring = self._parCmd.ActivateMonitoring
        self._command.UnitLimitAxis = self._parCmd.UnitLimitAxis
        self._command.ThresholdMode = self._parCmd.ThresholdMode
        self._command.ReactionMode = self._parCmd.ReactionMode
        self._command.Sensitivity = REAL_TO_PERCENT_INT(Value=self._parCmd.Sensitivity, IsOptional=True)
        self._command.SensitivityAxis[0] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[0], IsOptional=True)
        self._command.SensitivityAxis[1] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[1], IsOptional=True)
        self._command.SensitivityAxis[2] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[2], IsOptional=True)
        self._command.SensitivityAxis[3] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[3], IsOptional=True)
        self._command.SensitivityAxis[4] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[4], IsOptional=True)
        self._command.SensitivityAxis[5] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[5], IsOptional=True)
        self._command.SensitivityAxis[6] = REAL_TO_PERCENT_INT(Value=self._parCmd.SensitivityAxis[6], IsOptional=True)
        self._command.LimitAxis[0] = self._parCmd.LimitAxis[0]
        self._command.LimitAxis[1] = self._parCmd.LimitAxis[1]
        self._command.LimitAxis[2] = self._parCmd.LimitAxis[2]
        self._command.LimitAxis[3] = self._parCmd.LimitAxis[3]
        self._command.LimitAxis[4] = self._parCmd.LimitAxis[4]
        self._command.LimitAxis[5] = self._parCmd.LimitAxis[5]
        self._command.LimitAxis[6] = self._parCmd.LimitAxis[6]

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ActivateMonitoring
            CreateCommandPayload.AddBool(Value=self._command.ActivateMonitoring)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.UnitLimitAxis
            CreateCommandPayload.AddUsint(Value=self._command.UnitLimitAxis)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ThresholdMode
            CreateCommandPayload.AddUsint(Value=self._command.ThresholdMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ReactionMode
            CreateCommandPayload.AddUsint(Value=self._command.ReactionMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Sensitivity
            CreateCommandPayload.AddInt(Value=self._command.Sensitivity)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        for _idx in range(0, 7):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SensitivityAxis[x]
                CreateCommandPayload.AddInt(Value=self._command.SensitivityAxis[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 6)

        for _idx in range(0, 7):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.LimitAxis[x]
                CreateCommandPayload.AddReal(Value=self._command.LimitAxis[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

        # Create logging
        self.CreateCommandPayloadLog(AxesGroup=AxesGroup, ParameterCnt=_parameterCnt)
        return CreateCommandPayload

    def CreateCommandPayloadLog(self, *, AxesGroup: _T.AxesGroup, ParameterCnt: int = 0) -> None:  # INTERNAL
        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Create command payload with {1} parameter(s) :', Para1=DINT_TO_STRING(ParameterCnt))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ActivateMonitoring
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ActivateMonitoring = {1}', Para1=BOOL_TO_STRING(self._command.ActivateMonitoring))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for UnitLimitAxis
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.UnitLimitAxis = {1}', Para1=USINT_TO_STRING(self._command.UnitLimitAxis))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ThresholdMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ThresholdMode = {1}', Para1=THRESHOLD_MODE_TO_STRING(Value=self._command.ThresholdMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ReactionMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ReactionMode = {1}', Para1=COLLISION_REACTION_MODE_TO_STRING(Value=self._command.ReactionMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Sensitivity
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Sensitivity = {1}', Para1=INT_TO_STRING(self._command.Sensitivity))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SensitivityAxis[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensitivityAxis[1] = {1}', Para1=INT_TO_STRING(self._command.SensitivityAxis[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SensitivityAxis[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensitivityAxis[2] = {1}', Para1=INT_TO_STRING(self._command.SensitivityAxis[2]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SensitivityAxis[3]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensitivityAxis[3] = {1}', Para1=INT_TO_STRING(self._command.SensitivityAxis[3]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SensitivityAxis[4]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensitivityAxis[4] = {1}', Para1=INT_TO_STRING(self._command.SensitivityAxis[4]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SensitivityAxis[5]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensitivityAxis[5] = {1}', Para1=INT_TO_STRING(self._command.SensitivityAxis[5]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SensitivityAxis[6]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensitivityAxis[6] = {1}', Para1=INT_TO_STRING(self._command.SensitivityAxis[6]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitAxis[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitAxis[1] = {1}', Para1=REAL_TO_STRING(self._command.LimitAxis[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitAxis[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitAxis[2] = {1}', Para1=REAL_TO_STRING(self._command.LimitAxis[2]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitAxis[3]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitAxis[3] = {1}', Para1=REAL_TO_STRING(self._command.LimitAxis[3]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitAxis[4]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitAxis[4] = {1}', Para1=REAL_TO_STRING(self._command.LimitAxis[4]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitAxis[5]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitAxis[5] = {1}', Para1=REAL_TO_STRING(self._command.LimitAxis[5]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitAxis[6]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitAxis[6] = {1}', Para1=REAL_TO_STRING(self._command.LimitAxis[6]))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_CollisionDetectionFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        self.ProcessingMode = ProcessingMode.PARALLEL
        self.SequenceFlag = SequenceFlag.NO_SEQUENCE
        return FB_init

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0

        # call base implementation
        super().OnExecRun(AxesGroup=AxesGroup)

        match self._stepCmd:

            case 0:
                if self._execute_R.Q and (not self.Error):
                    # Check function is supported and parameter are valid ?
                    if self.CheckFunctionSupported(AxesGroup=AxesGroup) & self.CheckParameterValid(AxesGroup=AxesGroup):
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(CollisionDetectionOutCmd)), Value=0, DataLen=0)
                        # apply command parameter
                        copy_into(self._parCmd, self.ParCmd)
                        # init parameter sequence
                        self._command.ParSeq = 1
                        # create command data
                        self.CommandData = self.CreateCommandPayload(AxesGroup=AxesGroup)
                        # Add command to active command register
                        self._uniqueID = AxesGroup.Acyclic.ActiveCommandRegister.AddCmd(pCommandFB=self)
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 1:
                if self._responseReceived:
                    # reset response received flag
                    self._responseReceived = False
                    # update state flags
                    self.OnUpdateStateFlags(State=self._response.State)
                    # update state flags
                    self.OnApplyOutCmd(State=self._response.State)

                    # Done, Aborted or Error ?
                    if self._response.State >= CmdMessageState.DONE:
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 2:
                if not self.Execute:
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # Reset FB
        if not self.Execute:
            self.Reset()
        return OnExecRun

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        # Reset State flags
        self.CommandAborted = False
        self.CommandInterrupted = False
        self.Done = False

        match State:

            # No operation or process is active
            case CmdMessageState.EMPTY:
                pass
            # Created but not yet started
            case CmdMessageState.CREATED:
                pass
            # Buffered and awaiting execution
            case CmdMessageState.BUFFERED:
                self.CommandBuffered = True
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                self.CommandBuffered = True
            # Currently active and in progress
            case CmdMessageState.ACTIVE:
                pass
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                self.CommandInterrupted = True
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Done = True
                self.Busy = False
            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.CommandAborted = True
                self.Busy = False
            # Encountered an error during execution
            case CmdMessageState.ERROR:
                self.Error = True
                self.Busy = False

    def ParseResponsePayload(self, *, ResponseData: RobotLibraryResponseDataFB | None = None, Timestamp: SystemTime | None = None) -> int:  # INTERNAL
        if ResponseData is None:
            ResponseData = RobotLibraryResponseDataFB()
        else:
            ResponseData = copy_value(ResponseData)  # VAR_INPUT is a copy in ST
        if Timestamp is None:
            Timestamp = SystemTime()
        ParseResponsePayload: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # call base implementation to parse the header from payload buffer
        ResponseData.PayloadPtr = super().ParseResponsePayload(ResponseData=ResponseData, Timestamp=Timestamp)

        # copy parsed header to response
        self._response.ParSeq = self._rspHeader.ParSeq
        self._response.State = self._rspHeader.State
        self._response.AlarmMessageSeverity = self._rspHeader.AlarmMessageSeverity
        self._response.AlarmMessageCode = self._rspHeader.AlarmMessageCode

        # Create logging
        self.ParseResponsePayloadLog(ResponseData=ResponseData, Timestamp=Timestamp, ParameterCnt=_parameterCnt)
        return ParseResponsePayload

    def ParseResponsePayloadLog(self, *, ResponseData: RobotLibraryResponseDataFB | None = None, Timestamp: SystemTime | None = None, ParameterCnt: int = 0) -> None:  # INTERNAL
        if ResponseData is None:
            ResponseData = RobotLibraryResponseDataFB()
        if Timestamp is None:
            Timestamp = SystemTime()
        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} parameter(s) to parse from the response data:', Para1=DINT_TO_STRING(ParameterCnt))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for no parameter
        self.CreateLogMessage(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='This command has no parameter to parse...')

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        self.CommandAborted = False
        self.CommandInterrupted = False
        return Reset
