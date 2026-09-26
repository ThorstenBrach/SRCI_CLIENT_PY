"""Commands specified reaction from RA when defined force/torque detected

ST-Source: POUs/ForceControl/MC_ForceLimit/MC_ForceLimitFB.st
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
from srci.functions.Convert.TO_STRING.CONNECTION_MODE_TO_STRING import CONNECTION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.REFERENCE_TYPE_TO_STRING import REFERENCE_TYPE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BYTE_TO_STRING, DINT_TO_STRING, INT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, SINT_TO_USINT, USINT_TO_SINT, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, st_for_end, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ConnectionMode, ExecutionMode, ForceLimitOutCmd, ForceLimitParCmd, ForceLimitRecvData, ForceLimitSendData, MessageType, PriorityLevel, ReferenceType, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ForceLimitFB']


class MC_ForceLimitFB(RobotLibraryBaseEnableFB):
    """Commands specified reaction from RA when defined force/torque detected"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: ForceLimitParCmd = ForceLimitParCmd()
        # VAR_OUTPUT
        # TRUE, while the following outputs return valid values
        self.Valid: bool = False
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # Command output
        self.OutCmd: ForceLimitOutCmd = ForceLimitOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ForceLimitParCmd = ForceLimitParCmd()
        # command data to send
        self._command: ForceLimitSendData = ForceLimitSendData()
        # response data received
        self._response: ForceLimitRecvData = ForceLimitRecvData()

    def __call__(self, *, ParCmd: ForceLimitParCmd | None = None, Enable: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 89)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 89)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 89 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 89, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ForceLimitSendData)), DataLen=89)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 89 - PayloadPtr, 89)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 89, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 89, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ForceLimit

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 79 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ForceLimitParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ForceLimitParCmd)), DataLen=79) != RobotLibraryConstants.OK

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
            # Reset Valid output of the FB
            self.Valid = False
            # Reset parameter accepted flag
            self.ParameterAccepted = False
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False
        # internal index for loops
        _idx: int = 0

        CheckParameterValid = True

        # Check ParCmd.ReferenceType valid ?
        if self.ParCmd.ReferenceType != ReferenceType.TOOL and self.ParCmd.ReferenceType != ReferenceType.FRAME:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReferenceType = {1}', Para1=REFERENCE_TYPE_TO_STRING(Value=self.ParCmd.ReferenceType))
            return CheckParameterValid

        for _idx in range(0, 6):
            # Check ParCmd.SensorValue[_idx] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SensorValue[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SensorValue[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SensorValue[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 5)

        # Check ParCmd.ToolNo valid ?
        if ((self.ParCmd.ToolNo < 0 or self.ParCmd.ToolNo > 254) or self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex) or self.ParCmd.ToolNo > AxesGroup.State.UnifiedToolIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check ToolNo available on RC ?
            if self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ToolNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.ToolNo))
            return CheckParameterValid

        # Check ParCmd.FrameNo valid ?
        if ((self.ParCmd.FrameNo < 0 or self.ParCmd.FrameNo > 254) or self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex) or self.ParCmd.FrameNo > AxesGroup.State.UnifiedFrameIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check FrameNo available on RC ?
            if self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMENO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.FrameNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.FrameNo))
            return CheckParameterValid

        for _idx in range(0, 6):
            # Check ParCmd.ForceLimit[_idx] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.ForceLimit[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ForceLimit[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.ForceLimit[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 5)

        # Check ParCmd.ConnectionMode valid ?
        if self.ParCmd.ConnectionMode != ConnectionMode.RC_CONNECTED and self.ParCmd.ConnectionMode != ConnectionMode.PLC_CONNECTED:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ConnectionMode = {1}', Para1=CONNECTION_MODE_TO_STRING(Value=self.ParCmd.ConnectionMode))
            return CheckParameterValid

        for _idx in range(0, 6):
            # Check ParCmd.SensorFrame[_idx] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SensorFrame[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SensorFrame[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SensorFrame[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

        # Check ParCmd.CalibrationData valid ?
        if self.ParCmd.CalibrationData < 0 or self.ParCmd.CalibrationData > 255:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.CalibrationData = {1}', Para1=USINT_TO_STRING(self.ParCmd.CalibrationData))
            return CheckParameterValid

        # Check ParCmd.FixedSensor
        # -> no plausibility check for boolean
        # Check ParCmd.EmitterID valid ?
        if self.ParCmd.EmitterID < -127 or self.ParCmd.EmitterID > 127:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EmitterID = {1}', Para1=SINT_TO_STRING(self.ParCmd.EmitterID))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ForceLimit
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.EmitterID[0] = self._parCmd.EmitterID
        self._command.ListenerID = 0
        self._command.Reserve = 0
        self._command.ToolNo = self._parCmd.ToolNo
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.ConnectionMode = SINT_TO_USINT(self._parCmd.ConnectionMode)
        self._command.FixedSensor = set_bit(self._command.FixedSensor, 0, self._parCmd.FixedSensor)
        copy_into(self._command.SensorFrame, self._parCmd.SensorFrame)
        self._command.CalibrationData = self._parCmd.CalibrationData
        self._command.ReferenceType = self._parCmd.ReferenceType
        copy_into(self._command.SensorValue, self._parCmd.SensorValue)
        copy_into(self._command.ForceLimit, self._parCmd.ForceLimit)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.EmitterID[x]
                CreateCommandPayload.AddSint(Value=self._command.EmitterID[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ListenerID
            CreateCommandPayload.AddSint(Value=self._command.ListenerID)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve
            CreateCommandPayload.AddByte(Value=self._command.Reserve)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ToolNo
            CreateCommandPayload.AddUsint(Value=self._command.ToolNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.FrameNo
            CreateCommandPayload.AddUsint(Value=self._command.FrameNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ConnectionMode
            CreateCommandPayload.AddUsint(Value=self._command.ConnectionMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.FixedSensor
            CreateCommandPayload.AddByte(Value=self._command.FixedSensor)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        for _idx in range(0, 6):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SensorFrame[x]
                CreateCommandPayload.AddReal(Value=self._command.SensorFrame[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 5)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.CalibrationData
            CreateCommandPayload.AddUsint(Value=self._command.CalibrationData)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ReferenceType
            CreateCommandPayload.AddUsint(Value=self._command.ReferenceType)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        for _idx in range(0, 6):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SensorValue[x]
                CreateCommandPayload.AddReal(Value=self._command.SensorValue[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 5)

        for _idx in range(0, 6):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.ForceLimit[x]
                CreateCommandPayload.AddReal(Value=self._command.ForceLimit[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

        # Create logging
        self.CreateCommandPayloadLog(AxesGroup=AxesGroup, ParameterCnt=_parameterCnt)
        return CreateCommandPayload

    def CreateCommandPayloadLog(self, *, AxesGroup: _T.AxesGroup, ParameterCnt: int = 0) -> None:  # INTERNAL
        # internal index for loops
        _idx: int = 0

        # Create log entry for Parameter start
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Create command payload with {1} parameter(s) :', Para1=DINT_TO_STRING(ParameterCnt))

        # Create log entry for EmitterID[x]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.EmitterID
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EmitterID[{1}] = {2}', Para1=DINT_TO_STRING(_idx), Para2=SINT_TO_STRING(self._command.EmitterID[_idx]))
        else:
            _idx = st_for_end(0, 3)

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ListenerID
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ListenerID = {1}', Para1=SINT_TO_STRING(self._command.ListenerID))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=BYTE_TO_STRING(self._command.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ToolNo = {1}', Para1=USINT_TO_STRING(self._command.ToolNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for FrameNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.FrameNo = {1}', Para1=USINT_TO_STRING(self._command.FrameNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ConnectionMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ConnectionMode = {1}', Para1=CONNECTION_MODE_TO_STRING(Value=ConnectionMode(USINT_TO_SINT(self._command.ConnectionMode))))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for FixedSensor
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.FixedSensor = {1}', Para1=BYTE_TO_STRING(self._command.FixedSensor))

        for _idx in range(0, 6):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for ForceLimit[0]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensorFrame[{1}] = {2}', Para1=DINT_TO_STRING(_idx), Para2=REAL_TO_STRING(self._command.SensorFrame[_idx]))
        else:
            _idx = st_for_end(0, 5)

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for CalibrationData
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.CalibrationData = {1}', Para1=USINT_TO_STRING(self._command.CalibrationData))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ReferenceType
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ReferenceType = {1}', Para1=REFERENCE_TYPE_TO_STRING(Value=self._command.ReferenceType))

        for _idx in range(0, 6):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for ForceLimit[0]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SensorValue[{1}] = {2}', Para1=DINT_TO_STRING(_idx), Para2=REAL_TO_STRING(self._command.SensorValue[_idx]))
        else:
            _idx = st_for_end(0, 5)

        for _idx in range(0, 6):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for ForceLimit[0]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ForceLimit[{1}] = {2}', Para1=DINT_TO_STRING(_idx), Para2=REAL_TO_STRING(self._command.ForceLimit[_idx]))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_ForceLimitFB'

        self.ExecMode = ExecutionMode.CONTINUOUS
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ForceLimitOutCmd)), Value=0, DataLen=12)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.ForceStatus.ForceControlEnabled = bit(self._response.ForceStatus, 0)
            self.OutCmd.ForceStatus.ForceLimitEnabled = bit(self._response.ForceStatus, 1)
            self.OutCmd.ForceStatus.ApplyingForce = bit(self._response.ForceStatus, 2)
            self.OutCmd.ForceStatus.MaxDeviationReached = bit(self._response.ForceStatus, 3)
            self.OutCmd.ForceStatus.SpecifiedForceTorqueReached = bit(self._response.ForceStatus, 4)
            self.OutCmd.ForceStatus.SpecifiedForceLimitReached = bit(self._response.ForceStatus, 5)
            self.OutCmd.ForceStatus.Bit06 = bit(self._response.ForceStatus, 6)
            self.OutCmd.ForceStatus.Bit07 = bit(self._response.ForceStatus, 7)
            self.OutCmd.FollowID = self._response.OriginID  # {warning 'ToDo'}

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
                    # reset the falling edge
                    self._enable_F()

                    # Check function is supported and parameter are valid ?
                    if self.CheckFunctionSupported(AxesGroup=AxesGroup) & self.CheckParameterValid(AxesGroup=AxesGroup):
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ForceLimitOutCmd)), Value=0, DataLen=12)
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

            # Wait for response received or timeout or not Initialized
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
        self.Valid = False

        # Update enable flag
        self.Enabled = bit(self._response.ForceStatus, 1)

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
                self.Valid = True
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

        # ST-FIX F33: ForceStatus is the last value (byte 8, spec table 6-750), it was read twice
        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.InvocationCounter
            self._response.InvocationCounter = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Reserved
            self._response.Reserved = ResponseData.GetSint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.OriginID
            self._response.OriginID = ResponseData.GetInt()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ForceStatus
            self._response.ForceStatus = ResponseData.GetByte()
            # inc parameter counter
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
        # Create log entry for InvocationCounter
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.InvocationCounter = {1}', Para1=USINT_TO_STRING(self._response.InvocationCounter))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve = {1}', Para1=SINT_TO_STRING(self._response.Reserved))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for OriginID
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.OriginID = {1}', Para1=INT_TO_STRING(self._response.OriginID))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ForceStatus
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ForceStatus = {1}', Para1=BYTE_TO_STRING(self._response.ForceStatus))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Valid = False
        self.Busy = False
        self.CommandBuffered = False
        self.ParameterAccepted = False
        return Reset
