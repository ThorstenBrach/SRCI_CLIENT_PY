"""Write specific parameter of the robot

ST-Source: POUs/Write/MC_WriteSystemVariable/MC_WriteSystemVariableFB.st
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
from srci.functions.Convert.TO_STRING.DATA_TYPE_TO_STRING import DATA_TYPE_TO_STRING
from srci.functions.Convert.TO_STRING.PROCESSING_MODE_TO_STRING import PROCESSING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.SEQUENCE_FLAG_TO_STRING import SEQUENCE_FLAG_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, INT_TO_STRING, SINT_TO_STRING, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, st_for_end, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, DataType, ExecutionMode, MessageType, PriorityLevel, ProcessingMode, ProcessingModeEnum, RobotLibraryConstants, RobotLibraryErrorIdEnum, SequenceFlag, SequenceFlagEnum, Severity, SystemTime, WriteSystemVariableOutCmd, WriteSystemVariableParCmd, WriteSystemVariableRecvData, WriteSystemVariableSendData

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_WriteSystemVariableFB']


class MC_WriteSystemVariableFB(RobotLibraryBaseExecuteFB):
    """Write specific parameter of the robot"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Processing Mode
        self.ProcessingMode: ProcessingMode = ProcessingMode.BUFFERED
        # Defines the target sequence in which the command will be executed
        self.SequenceFlag: SequenceFlag = SequenceFlag.NO_SEQUENCE
        # command parameter
        self.ParCmd: WriteSystemVariableParCmd = WriteSystemVariableParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The command was aborted by another command.
        self.CommandAborted: bool = False
        # TRUE, while command is interrupted during execution and can be continued
        self.CommandInterrupted: bool = False
        # TRUE, when parameters were overwritten but not activated on RC until a restart of the RC
        self.RestartRequested: bool = False
        # command outputs
        self.OutCmd: WriteSystemVariableOutCmd = WriteSystemVariableOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: WriteSystemVariableParCmd = WriteSystemVariableParCmd()
        # command data to send
        self._command: WriteSystemVariableSendData = WriteSystemVariableSendData()
        # response data received
        self._response: WriteSystemVariableRecvData = WriteSystemVariableRecvData()

    def __call__(self, *, ProcessingMode: ProcessingMode | None = None, SequenceFlag: SequenceFlag | None = None, ParCmd: WriteSystemVariableParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 76)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 76)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 76 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 76, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(WriteSystemVariableSendData)), DataLen=76)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 76 - PayloadPtr, 76)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 76, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 76, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.WriteSystemVariable

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
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(WriteSystemVariableParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(WriteSystemVariableParCmd)), DataLen=66) != RobotLibraryConstants.OK

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
        if self.ProcessingMode < ProcessingMode.BUFFERED and self.ProcessingMode > ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check ProcessingModea valid ?
        if ((((((self.ProcessingMode != ProcessingMode.BUFFERED and self.ProcessingMode != ProcessingMode.ABORTING) and self.ProcessingMode != ProcessingMode.PARALLEL) and self.ProcessingMode != ProcessingMode.CONTINUOUS) and self.ProcessingMode != ProcessingMode.DEACTIVATE) and self.ProcessingMode != ProcessingMode.TRIGGER_ONCE) and self.ProcessingMode != ProcessingMode.TRIGGER_CONTINUOUS) and self.ProcessingMode != ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check SequenceFlag valid ?
        if (self.SequenceFlag != SequenceFlag.NO_SEQUENCE and self.SequenceFlag != SequenceFlag.PRIMARY_SEQUENCE) and self.SequenceFlag != SequenceFlag.SECONDARY_SEQUENCE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter SequenceFlag = {1}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.SequenceFlag))
            return CheckParameterValid

        # Check ParCmd.RCParameter valid ?
        if self.ParCmd.RCParameter != False and self.ParCmd.RCParameter != True:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.RCParameter = {1}', Para1=BOOL_TO_STRING(self.ParCmd.RCParameter))
            return CheckParameterValid

        for _idx in range(0, 8):
            # Check ParCmd.RCParameter[_idx] valid ?
            if self.ParCmd.ParameterID[_idx] < 0 and self.ParCmd.ParameterID[_idx] > 4294967295:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ParameterID[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.ParameterID[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 7)

        for _idx in range(0, 8):
            # Check ParCmd.SubParameterID[_idx] valid ?
            if self.ParCmd.SubParameterID[_idx] < 0 and self.ParCmd.SubParameterID[_idx] > 4294967295:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SubParameterID[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.SubParameterID[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 7)

        for _idx in range(0, 8):
            # Check ParCmd.DataType[_idx] valid ?
            if (((((((((((self.ParCmd.DataType[_idx] != DataType.TYPE_BOOL and self.ParCmd.DataType[_idx] != DataType.TYPE_BYTE) and self.ParCmd.DataType[_idx] != DataType.TYPE_WORD) and self.ParCmd.DataType[_idx] != DataType.TYPE_DWORD) and self.ParCmd.DataType[_idx] != DataType.TYPE_SINT) and self.ParCmd.DataType[_idx] != DataType.TYPE_USINT) and self.ParCmd.DataType[_idx] != DataType.TYPE_INT) and self.ParCmd.DataType[_idx] != DataType.TYPE_UINT) and self.ParCmd.DataType[_idx] != DataType.TYPE_DINT) and self.ParCmd.DataType[_idx] != DataType.TYPE_UDINT) and self.ParCmd.DataType[_idx] != DataType.TYPE_REAL) and self.ParCmd.DataType[_idx] != DataType.TYPE_CHAR) and self.ParCmd.DataType[_idx] != DataType.TYPE_CHAR_ARRAY:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.DataType[{2}] = {1}', Para1=DATA_TYPE_TO_STRING(Value=self.ParCmd.DataType[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 7)

        for _idx in range(0, 4):
            # Check ParCmd.Data_0[_idx] valid ?
            if self.ParCmd.Data_0[_idx] < 0 and self.ParCmd.Data_0[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_0[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_0[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_1[_idx] valid ?
            if self.ParCmd.Data_1[_idx] < 0 and self.ParCmd.Data_1[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_1[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_1[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_2[_idx] valid ?
            if self.ParCmd.Data_2[_idx] < 0 and self.ParCmd.Data_2[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_2[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_2[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_3[_idx] valid ?
            if self.ParCmd.Data_3[_idx] < 0 and self.ParCmd.Data_3[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_3[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_3[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_4[_idx] valid ?
            if self.ParCmd.Data_4[_idx] < 0 and self.ParCmd.Data_4[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_4[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_4[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_5[_idx] valid ?
            if self.ParCmd.Data_5[_idx] < 0 and self.ParCmd.Data_5[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_5[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_5[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_6[_idx] valid ?
            if self.ParCmd.Data_6[_idx] < 0 and self.ParCmd.Data_6[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_6[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_6[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Data_7[_idx] valid ?
            if self.ParCmd.Data_7[_idx] < 0 and self.ParCmd.Data_7[_idx] > 65535:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Data_7[{2}] = {1}', Para1=UINT_TO_STRING(self.ParCmd.Data_7[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

        # Check ParCmd.ListenerID valid ?
        if self.ParCmd.ListenerID < 0 or self.ParCmd.ListenerID > 127:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ListenerID = {1}', Para1=SINT_TO_STRING(self.ParCmd.ListenerID))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.WriteSystemVariable
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        self._command.EmitterID[0] = 0
        self._command.EmitterID[1] = 0
        self._command.EmitterID[2] = 0
        self._command.EmitterID[3] = 0
        self._command.ListenerID = self._parCmd.ListenerID
        self._command.Reserve = 0
        copy_into(self._command.ParameterID, self._parCmd.ParameterID)
        copy_into(self._command.SubParameterID, self._parCmd.SubParameterID)

        for _idx in range(0, 8):
            self._command.DataType[_idx] = self._parCmd.DataType[_idx]
        else:
            _idx = st_for_end(0, 7)

        copy_into(self._command.Data_0, self._parCmd.Data_0)
        copy_into(self._command.Data_1, self._parCmd.Data_1)
        copy_into(self._command.Data_2, self._parCmd.Data_2)
        copy_into(self._command.Data_3, self._parCmd.Data_3)
        copy_into(self._command.Data_4, self._parCmd.Data_4)
        copy_into(self._command.Data_5, self._parCmd.Data_5)
        copy_into(self._command.Data_6, self._parCmd.Data_6)
        copy_into(self._command.Data_7, self._parCmd.Data_7)

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

        for _idx in range(0, 8):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.ParameterID[_idx]
                CreateCommandPayload.AddUint(Value=self._command.ParameterID[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 7)

        for _idx in range(0, 8):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SubParameterID[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.SubParameterID[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 7)

        for _idx in range(0, 8):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.DataType[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.DataType[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 7)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_0[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_0[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_1[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_1[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_2[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_2[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_3[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_3[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_4[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_4[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_5[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_5[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_6[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_6[_idx])
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1
        else:
            _idx = st_for_end(0, 3)

        for _idx in range(0, 4):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.Data_7[_idx]
                CreateCommandPayload.AddUsint(Value=self._command.Data_7[_idx])
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
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EmitterID[{2}] = {1}', Para1=SINT_TO_STRING(self._command.EmitterID[_idx]), Para2=DINT_TO_STRING(_idx))
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

        # Create log entry for ParameterID[_idx]
        for _idx in range(0, 8):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.ParameterID
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ParameterID[{2}] = {1}', Para1=UINT_TO_STRING(self._command.ParameterID[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 7)

        # Create log entry for SubParameterID[_idx]
        for _idx in range(0, 8):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.SubParameterID
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SubParameterID[{2}] = {1}', Para1=USINT_TO_STRING(self._command.SubParameterID[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 7)

        # Create log entry for DataType[_idx]
        for _idx in range(0, 8):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.DataType
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DataType[{2}] = {1}', Para1=DATA_TYPE_TO_STRING(Value=DataType(self._command.DataType[_idx])), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 7)

        # Create log entry for Data_0[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_0
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_0[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_0[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_1[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_1
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_1[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_1[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_2[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_2
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_2[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_2[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_3[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_3
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_3[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_3[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_4[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_4
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_4[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_4[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_5[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_5
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_5[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_5[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_6[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_6
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_6[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_6[_idx]), Para2=DINT_TO_STRING(_idx))
        else:
            _idx = st_for_end(0, 3)

        # Create log entry for Data_7[_idx]
        for _idx in range(0, 4):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Command.Data_7
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Data_7[{2}] = {1}', Para1=BYTE_TO_STRING(self._command.Data_7[_idx]), Para2=DINT_TO_STRING(_idx))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_WriteSystemVariableFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        self.ProcessingMode = ProcessingMode.PARALLEL
        self.SequenceFlag = SequenceFlag.NO_SEQUENCE
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(WriteSystemVariableOutCmd)), Value=0, DataLen=4)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.InvocationCounter = self._response.InvocationCounter
            self.OutCmd.OriginID = self._response.OriginID
            self.OutCmd.RestartRequested = self._response.RestartRequested

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(WriteSystemVariableOutCmd)), Value=0, DataLen=4)
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

        # Update RestartRequested flag
        self.RestartRequested = self._response.RestartRequested

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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.InvocationCounter
            self._response.InvocationCounter = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetSint()
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
            # Get Response.RestartRequested
            self._response.RestartRequested = ResponseData.GetBool()
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
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve = {1}', Para1=SINT_TO_STRING(self._response.Reserve))

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
        # Create log entry for RestartRequested
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RestartRequested = {1}', Para1=BOOL_TO_STRING(self._response.RestartRequested))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.RestartRequested = False
        self.CommandBuffered = False
        self.CommandAborted = False
        self.CommandInterrupted = False
        return Reset
