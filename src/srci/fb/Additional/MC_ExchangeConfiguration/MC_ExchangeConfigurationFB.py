# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_ExchangeConfigurationFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Reads and writes specific configuration parameters on RC that are required for the RI to
#    work
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

"""Reads and writes specific configuration parameters on RC that are required for the RI to work

ST-Source: POUs/Additional/MC_ExchangeConfiguration/MC_ExchangeConfigurationFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.fb._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from srci.fb._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from srci.functions.Common import CheckTimeout, SetTimeout
from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.functions.Convert.TO_STRING.DATA_ENABLE_SYNC_TO_STRING import DATA_ENABLE_SYNC_TO_STRING
from srci.functions.Convert.TO_STRING.DATA_IN_SYNC_TO_STRING import DATA_IN_SYNC_TO_STRING
from srci.functions.Convert.TO_STRING.LOG_LEVEL_TO_STRING import LOG_LEVEL_TO_STRING
from srci.functions.Convert.TO_STRING.SYNC_REACTION_TO_STRING import SYNC_REACTION_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, SINT_TO_USINT, UDINT_TO_STRING, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExchangeConfigurationOutCmd, ExchangeConfigurationParCmd, ExchangeConfigurationRecvData, ExchangeConfigurationSendData, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SyncReaction, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ExchangeConfigurationFB']


class MC_ExchangeConfigurationFB(RobotLibraryBaseEnableFB):
    """Reads and writes specific configuration parameters on RC that are required for the RI to work"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: ExchangeConfigurationParCmd = ExchangeConfigurationParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # command results
        self.OutCmd: ExchangeConfigurationOutCmd = ExchangeConfigurationOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ExchangeConfigurationParCmd = ExchangeConfigurationParCmd()
        # command data to send
        self._command: ExchangeConfigurationSendData = ExchangeConfigurationSendData()
        # response data received
        self._response: ExchangeConfigurationRecvData = ExchangeConfigurationRecvData()

    def __call__(self, *, ParCmd: ExchangeConfigurationParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ParCmd is not None:
            copy_into(self.ParCmd, ParCmd)
        if Enable is not None:
            self.Enable = Enable
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 33)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 33)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 33 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 33, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ExchangeConfigurationSendData)), DataLen=33)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 33 - PayloadPtr, 33)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 33, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 33, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = True  # Function is mandatory
        return CheckFunctionSupported

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ExchangeConfiguration

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 27 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ExchangeConfigurationParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ExchangeConfigurationParCmd)), DataLen=27) != RobotLibraryConstants.OK

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
            # Reset parameter accepted flag
            self.ParameterAccepted = False
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        CheckParameterValid = True

        # Check ParCmd.LogLevel valid ?
        if ((((self.ParCmd.LogLevel != Severity.DEACTIVATE and self.ParCmd.LogLevel != Severity.DEBUG) and self.ParCmd.LogLevel != Severity.INFO) and self.ParCmd.LogLevel != Severity.WARNING) and self.ParCmd.LogLevel != Severity.ERROR) and self.ParCmd.LogLevel != Severity.FATAL_ERROR:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LogLevel = {1}', Para1=LOG_LEVEL_TO_STRING(Value=self.ParCmd.LogLevel))
            return CheckParameterValid

        # Check ParCmd.WaitAtBlendingZone
        # -> no plausibility check for boolean
        # Check ParCmd.AllowSecSeqWhileSubprogram
        # -> no plausibility check for boolean
        # Check ParCmd.DelayTime valid ?
        if self.ParCmd.DelayTime < 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.DelayTime = {1} ms', Para1=UINT_TO_STRING(self.ParCmd.DelayTime))
            return CheckParameterValid

        # Check ParCmd.WaitForNrOfCmd valid ?
        if self.ParCmd.WaitForNrOfCmd < 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WaitForNrOfCmd = {1}', Para1=UINT_TO_STRING(self.ParCmd.WaitForNrOfCmd))
            return CheckParameterValid

        # Check ParCmd.LifeSignTimeOut valid ?
        if self.ParCmd.LifeSignTimeOut < 10:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LifeSignTimeOut = {1} ms', Para1=UINT_TO_STRING(self.ParCmd.LifeSignTimeOut))
            return CheckParameterValid

        # Check ParCmd.SyncDelay valid ?
        if self.ParCmd.SyncDelay < 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SyncDelay = {1}', Para1=UINT_TO_STRING(self.ParCmd.SyncDelay))
            return CheckParameterValid

        # Check ParCmd.SyncReaction valid ?
        if ((self.ParCmd.SyncReaction != SyncReaction.NO_REACTION and self.ParCmd.SyncReaction != SyncReaction.NO_AUTOMATIC_DISABLE) and self.ParCmd.SyncReaction != SyncReaction.INTERRUPT_WHEN_SEQUENCE_IS_EMPTY) and self.ParCmd.SyncReaction != SyncReaction.IMMEDIATE_INTERRUPT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SyncReaction = {1}', Para1=SYNC_REACTION_TO_STRING(Value=self.ParCmd.SyncReaction))
            return CheckParameterValid
        # Check ParCmd.DataInSync.ToolsInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataInSync.FramesInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataInSync.LoadsInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataInSync.WorkAreasInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataInSync.SoftwareLimitsInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataInSync.DefaultDynamicsInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataInSync.ReferenceDynamicsInSync
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncTool
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncFrame
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncLoad
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncWorkArea
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncSWLimits
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncDefaultDynamics
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.EnableSyncReferenceDynamics
        # -> no plausibility check for boolean
        # Check ParCmd.DataEnableSync.AllowDynamicBlending
        # -> no plausibility check for boolean
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ExchangeConfiguration
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.LogLevel = self._parCmd.LogLevel
        self._command.CtrlByte = set_bit(self._command.CtrlByte, 0, self._parCmd.WaitAtBlendingZone)
        self._command.CtrlByte = set_bit(self._command.CtrlByte, 1, self.Enable)
        self._command.CtrlByte = set_bit(self._command.CtrlByte, 2, self._parCmd.AllowSecSeqWhileSubprogram)
        self._command.CtrlByte = set_bit(self._command.CtrlByte, 3, self._parCmd.AllowDynamicBlending)
        self._command.DelayTime = self._parCmd.DelayTime
        self._command.WaitForNrOfCmd = self._parCmd.WaitForNrOfCmd
        self._command.LifeSignTimeOut = self._parCmd.LifeSignTimeOut
        self._command.SyncDelay = self._parCmd.SyncDelay
        self._command.SyncReaction = self._parCmd.SyncReaction
        self._command.Reserve1 = 0
        copy_into(self._command.DataInSync, self._parCmd.DataInSync)
        self._command.Reserve2 = 0
        copy_into(self._command.DataEnableSync, self._parCmd.DataEnableSync)
        self._command.Reserve3 = 0

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LogLeve
            CreateCommandPayload.AddUsint(Value=SINT_TO_USINT(self._command.LogLevel))
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.CtrlByte
            CreateCommandPayload.AddByte(Value=self._command.CtrlByte)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DelayTime
            CreateCommandPayload.AddUint(Value=self._command.DelayTime)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WaitForNrOfCmd
            CreateCommandPayload.AddUint(Value=self._command.WaitForNrOfCmd)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LifeSignTimeOut
            CreateCommandPayload.AddUint(Value=self._command.LifeSignTimeOut)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.SyncDelay
            CreateCommandPayload.AddUint(Value=self._command.SyncDelay)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.SyncReaction
            CreateCommandPayload.AddUsint(Value=self._command.SyncReaction)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.SyncReaction
            CreateCommandPayload.AddUsint(Value=self._command.Reserve1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DataInSync
            CreateCommandPayload.AddDataInSync(Value=self._command.DataInSync)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve1
            CreateCommandPayload.AddByte(Value=self._command.Reserve2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DataEnableSync
            CreateCommandPayload.AddDataEnableSync(Value=self._command.DataEnableSync)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve2
            CreateCommandPayload.AddByte(Value=self._command.Reserve3)
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
        # Create log entry for LogLevel
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LogLevel = {1}', Para1=LOG_LEVEL_TO_STRING(Value=self._command.LogLevel))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for CtrlByte
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.CtrlByte = {1}', Para1=BYTE_TO_STRING(self._command.CtrlByte))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DelayTime
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DelayTime = {1}', Para1=UINT_TO_STRING(self._command.DelayTime))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WaitForNrOfCmd
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WaitForNrOfCmd = {1}', Para1=UINT_TO_STRING(self._command.WaitForNrOfCmd))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LifeSignTimeOut
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LifeSignTimeOut = {1}', Para1=UINT_TO_STRING(self._command.LifeSignTimeOut))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SyncDelay
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SyncDelay = {1}', Para1=UINT_TO_STRING(self._command.SyncDelay))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SyncReaction
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SyncReaction = {1}', Para1=SYNC_REACTION_TO_STRING(Value=self._command.SyncReaction))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve1 = {1}', Para1=BYTE_TO_STRING(self._command.Reserve1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DataInSync = {1}', Para1=DATA_IN_SYNC_TO_STRING(Value=self._command.DataInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve2 = {1}', Para1=BYTE_TO_STRING(self._command.Reserve2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataEnableSync
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DataEnableSync = {1}', Para1=DATA_ENABLE_SYNC_TO_STRING(Value=self._command.DataEnableSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve3 = {1}', Para1=BYTE_TO_STRING(self._command.Reserve3))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ExchangeConfigurationFB'
        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ExchangeConfigurationOutCmd)), Value=0, DataLen=36)

        if State == CmdMessageState.ACTIVE or True:
            # Update command outputs
            self.OutCmd.LengthACR = self._response.LengthACR
            self.OutCmd.HighestToolIndex = self._response.HighestToolIndex
            self.OutCmd.HighestFrameIndex = self._response.HighestFrameIndex
            self.OutCmd.HighestLoadIndex = self._response.HighestLoadIndex
            self.OutCmd.HighestWorkAreaIndex = self._response.HighestWorkAreaIndex
            copy_into(self.OutCmd.DataInSync, self._response.DataInSync)
            self.OutCmd.ChangeIndexTool = self._response.ChangeIndexTool
            self.OutCmd.ChangeIndexFrame = self._response.ChangeIndexFrame
            self.OutCmd.ChangeIndexLoad = self._response.ChangeIndexLoad
            self.OutCmd.ChangeIndexWorkArea = self._response.ChangeIndexWorkArea
            self.OutCmd.RAWorkingHours = self._response.RAWorkingHours
            self.OutCmd.BrakeTestRequired = bit(self._response.StatusByte, 0)
            self.OutCmd.StepModeExactStopActive = bit(self._response.StatusByte, 1)
            self.OutCmd.StepModeBlendingActive = bit(self._response.StatusByte, 2)
            self.OutCmd.PathAccuracyMode = bit(self._response.StatusByte, 3)
            self.OutCmd.AvoidSingularity = bit(self._response.StatusByte, 4)
            self.OutCmd.CollisionDetectionEnabled = bit(self._response.StatusByte, 5)
            self.OutCmd.AcceleratingSupported = bit(self._response.StatusByte, 6)
            self.OutCmd.DecceleratingSupported = bit(self._response.StatusByte, 7)
            self.OutCmd.ConstantVelocitySupported = self._response.ConstantVelocitySupported
            self.OutCmd.RCWorkingHours = self._response.RCWorkingHours

        # ST-FIX F32
        self.OutCmd.NumberOfServerLogs = self._response.NumberOfServerLogs

    def OnExecCancel(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecCancel: int = 0
        # internal return value
        _retVal: int = 0

        OnExecCancel = RobotLibraryConstants.RUNNING

        match self._stepCancel:

            case 0:
                self.Busy = True

                # Create log entry
                self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Execution of {1} cancelled', Para1=self.MyType)

                # try to remove cmd
                _retVal = AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(UniqueID=self._uniqueID)

                # check result of removement
                if _retVal == RobotLibraryConstants.OK:
                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = RobotLibraryConstants.OK

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} successfully removed from ACR', Para1=self.MyType)
                else:
                    # set timeout
                    SetTimeout(PT=self._timeoutCancel, rTimer=self._timerCancel)
                    # inc step counter
                    self._stepCancel = self._stepCancel + 1

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='{1} was not removed from ACR because execution was already in progress', Para1=self.MyType)

            case 1:
                OnExecCancel = self.OnExecErrorClear(AxesGroup=AxesGroup)

                if OnExecCancel == RobotLibraryConstants.OK:
                    # Reset busy flag
                    self.Busy = False
                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = RobotLibraryConstants.OK
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # reset step counter
        if OnExecCancel != RobotLibraryConstants.RUNNING:
            # Reset FB variables
            self.Reset()
            # Reset step counter
            self._stepCancel = 0
        return OnExecCancel

    def OnExecErrorClear(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecErrorClear: int = 0

        OnExecErrorClear = RobotLibraryConstants.RUNNING

        match self._stepClearError:

            case 0:
                self.Busy = True
                # trigger parameter update to disable FB
                self._parameterUpdateInternal = True
                # call Check Parameter changed method to trigger the parameter update to disable the function
                self.CheckParameterChanged(AxesGroup=AxesGroup)
                # set timeout
                SetTimeout(PT=self._timeoutClearError, rTimer=self._timerClearError)
                # inc step counter
                self._stepClearError = self._stepClearError + 1

            case 1:
                if self._responseReceived:
                    # reset response received flag
                    self._responseReceived = False
                    # reset step counter
                    self._stepClearError = 0
                    # finished
                    OnExecErrorClear = RobotLibraryConstants.OK
                else:
                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerClearError) == RobotLibraryConstants.OK:
                        OnExecErrorClear = RobotLibraryConstants.HAS_ERROR
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # reset step counter
        if OnExecErrorClear != RobotLibraryConstants.RUNNING:
            # Reset
            self.Reset()
            # reset step counter
            self._stepClearError = 0
        return OnExecErrorClear

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:  # PROTECTED
        OnExecRun: int = 0

        # call base implementation
        super().OnExecRun(AxesGroup=AxesGroup)

        match self._stepCmd:

            case 0:
                if self._enable_R.Q and (not self.Error):
                    # reset the rising edge
                    self._enable_R()

                    # Check function is supported and parameter are valid ?
                    if self.CheckFunctionSupported(AxesGroup=AxesGroup) & self.CheckParameterValid(AxesGroup=AxesGroup):
                        # Reset all internal flags
                        self.Reset()
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ExchangeConfigurationOutCmd)), Value=0, DataLen=36)
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

                # do not abort directly, so that the ParSeq update can be send
                if self._enable_F.Q:
                    # Reset Enabled Flag
                    self.Enabled = False
                    # Set Busy flag
                    self.Busy = True
                    # trigger parameter update to disable FB
                    self._parameterUpdateInternal = True
                    # reset the falling edge
                    self._enable_F()
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1

            case 2:
                if self._responseReceived | (CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK) or (not AxesGroup.State.Initialized and (not AxesGroup.State.Synchronized)):
                    self.Reset()
            case _:
                # invalid step
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite=True)

        # Reset FB
        if self._enable_R.Q or self._enable_F.Q:
            self.Reset()
        return OnExecRun

    def OnUpdateStateFlags(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        # Reset State flags

        # Update Enabled flag
        self.Enabled = self._response.Enabled or State == CmdMessageState.ACTIVE  # {warning 'ToDo: Stäubli send Enabled = FALSE instead of true'}

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
                self.ParameterAccepted = True
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                self.CommandBuffered = True
                self.ParameterAccepted = True
            # Currently active and in progress
            case CmdMessageState.ACTIVE:
                pass
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                pass
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Busy = False
            # Aborted before completion
            case CmdMessageState.ABORTED:
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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Enabled
            self._response.Enabled = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Reserve1
            self._response.Reserve1 = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LengthACR
            self._response.LengthACR = ResponseData.GetUint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.HighestToolIndex
            self._response.HighestToolIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.HighestFrameIndex
            self._response.HighestFrameIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.HighestLoadIndex
            self._response.HighestLoadIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.HighestWorkAreaIndex
            self._response.HighestWorkAreaIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.DataInSync
            copy_into(self._response.DataInSync, ResponseData.GetDataInSync())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Reserve2
            self._response.Reserve2 = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ChangeIndexTool
            self._response.ChangeIndexTool = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ChangeIndexFrame
            self._response.ChangeIndexFrame = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ChangeIndexLoad
            self._response.ChangeIndexLoad = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ChangeIndexWorkArea
            self._response.ChangeIndexWorkArea = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.RAWorkingHours
            self._response.RAWorkingHours = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.StatusByte
            self._response.StatusByte = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ConstantVelocitySupported
            self._response.ConstantVelocitySupported = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.RCWorkingHours
            self._response.RCWorkingHours = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # ST-FIX F32
        if ResponseData.IsPayloadRemaining:
            self._response.NumberOfServerLogs = ResponseData.GetUint()
            _parameterCnt = _parameterCnt + 1

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
        # Create log entry for Enabled
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Enabled = {1}', Para1=BOOL_TO_STRING(self._response.Enabled))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve1
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve1 = {1}', Para1=BYTE_TO_STRING(self._response.Reserve1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LengthACR
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LengthACR = {1}', Para1=UINT_TO_STRING(self._response.LengthACR))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for HighestToolIndex
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.HighestToolIndex = {1}', Para1=USINT_TO_STRING(self._response.HighestToolIndex))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for HighestFrameIndex
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.HighestFrameIndex = {1}', Para1=USINT_TO_STRING(self._response.HighestFrameIndex))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for HighestLoadIndex
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.HighestLoadIndex = {1}', Para1=USINT_TO_STRING(self._response.HighestLoadIndex))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for HighestWorkAreaIndex
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.HighestWorkAreaIndex = {1}', Para1=USINT_TO_STRING(self._response.HighestWorkAreaIndex))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.ToolsInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.ToolsInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.ToolsInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.FramesInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.FramesInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.FramesInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.LoadsInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.LoadsInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.LoadsInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.WorkAreasInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.WorkAreasInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.WorkAreasInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.SoftwareLimitsInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.SoftwareLimitsInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.SoftwareLimitsInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.DefaultDynamicsInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.DefaultDynamicsInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.DefaultDynamicsInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataInSync.ReferenceDynamicsInSync
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.DataInSync.ReferenceDynamicsInSync = {1}', Para1=BOOL_TO_STRING(self._response.DataInSync.ReferenceDynamicsInSync))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve2
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve2 = {1}', Para1=BYTE_TO_STRING(self._response.Reserve2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ChangeIndexTool
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ChangeIndexTool = {1}', Para1=USINT_TO_STRING(self._response.ChangeIndexTool))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ChangeIndexFrame
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ChangeIndexFrame = {1}', Para1=USINT_TO_STRING(self._response.ChangeIndexFrame))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ChangeIndexLoad
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ChangeIndexLoad = {1}', Para1=USINT_TO_STRING(self._response.ChangeIndexLoad))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ChangeIndexWorkArea
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ChangeIndexWorkArea = {1}', Para1=USINT_TO_STRING(self._response.ChangeIndexWorkArea))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RAWorkingHours
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RAWorkingHours = {1}', Para1=UDINT_TO_STRING(self._response.RAWorkingHours))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for StatusByte
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.StatusByte = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._response.StatusByte))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ConstantVelocitySupported
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ConstantVelocitySupported = {1}', Para1=BOOL_TO_STRING(self._response.ConstantVelocitySupported))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RCWorkingHours
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RCWorkingHours = {1}', Para1=UDINT_TO_STRING(self._response.RCWorkingHours))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Busy = False
        self.CommandBuffered = False
        self.ParameterAccepted = False
        return Reset
