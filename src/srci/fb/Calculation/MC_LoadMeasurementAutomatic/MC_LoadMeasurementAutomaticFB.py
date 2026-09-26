"""Automatic detection of load data

ST-Source: POUs/Calculation/MC_LoadMeasurementAutomatic/MC_LoadMeasurementAutomaticFB.st
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
from srci.functions.Convert.TO_STRING.ABORTING_MODE_TO_STRING import ABORTING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.LOAD_MEASUREMENT_MODE_TO_STRING import LOAD_MEASUREMENT_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.SEQUENCE_FLAG_TO_STRING import SEQUENCE_FLAG_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING, REAL_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import AbortingMode, AbortingModeEnum, CmdMessageState, CmdType, ExecutionMode, LoadMeasurementAutomaticOutCmd, LoadMeasurementAutomaticParCmd, LoadMeasurementAutomaticRecvData, LoadMeasurementAutomaticSendData, LoadMeasurementMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, SequenceFlag, SequenceFlagEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_LoadMeasurementAutomaticFB']


class MC_LoadMeasurementAutomaticFB(RobotLibraryBaseExecuteFB):
    """Automatic detection of load data"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Parameter which determines the behavior towards the previously sent and still active or buffered commands.
        self.AbortingMode: AbortingMode = AbortingMode.BUFFER
        # Defines the target sequence in which the command will be executed
        self.SequenceFlag: SequenceFlag = SequenceFlag.NO_SEQUENCE
        # Command parameter
        self.ParCmd: LoadMeasurementAutomaticParCmd = LoadMeasurementAutomaticParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The command takes control of the motion of the according axis group.
        self.Active: bool = False
        # The command was aborted by another command.
        self.CommandAborted: bool = False
        # TRUE, while command is interrupted during execution and can be continued.
        self.CommandInterrupted: bool = False
        # Command output
        self.OutCmd: LoadMeasurementAutomaticOutCmd = LoadMeasurementAutomaticOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: LoadMeasurementAutomaticParCmd = LoadMeasurementAutomaticParCmd()
        # command data to send
        self._command: LoadMeasurementAutomaticSendData = LoadMeasurementAutomaticSendData()
        # response data received
        self._response: LoadMeasurementAutomaticRecvData = LoadMeasurementAutomaticRecvData()

    def __call__(self, *, AbortingMode: AbortingMode | None = None, SequenceFlag: SequenceFlag | None = None, ParCmd: LoadMeasurementAutomaticParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if AbortingMode is not None:
            self.AbortingMode = AbortingMode(AbortingMode)
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 143)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 143)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 143 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 143, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(LoadMeasurementAutomaticSendData)), DataLen=143)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 143 - PayloadPtr, 143)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 143, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 143, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.LoadMeasurementAutomatic

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 137 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(LoadMeasurementAutomaticParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(LoadMeasurementAutomaticParCmd)), DataLen=137) != RobotLibraryConstants.OK

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

        # Check AbortingMode valid ?
        if self.AbortingMode != AbortingMode.BUFFER and self.AbortingMode != AbortingMode.ABORT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_ABORTINGMODE_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter AbortingMode = {1}', Para1=ABORTING_MODE_TO_STRING(Value=self.AbortingMode))
            return CheckParameterValid

        # Check SequenceFlag valid ?
        if self.SequenceFlag != SequenceFlag.PRIMARY_SEQUENCE and self.SequenceFlag != SequenceFlag.SECONDARY_SEQUENCE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter SequenceFlag = {1}', Para1=SEQUENCE_FLAG_TO_STRING(Value=self.SequenceFlag))
            return CheckParameterValid

        # Check ParCmd.Mode valid ?
        if ((self.ParCmd.Mode != LoadMeasurementMode.ONE_POSITION and self.ParCmd.Mode != LoadMeasurementMode.CONFIGURATION_ANGLE) and self.ParCmd.Mode != LoadMeasurementMode.AREA) and self.ParCmd.Mode != LoadMeasurementMode.TWO_POSITIONS:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mode = {1}', Para1=LOAD_MEASUREMENT_MODE_TO_STRING(Value=self.ParCmd.Mode))
            return CheckParameterValid

        # Check ParCmd.Mass valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Mass) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mass = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Mass))
            return CheckParameterValid

        for _idx in range(0, 2):
            # Check ParCmd.Area_J3[x] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.Area_J3[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Area_J3[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Area_J3[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Area_J4[x] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.Area_J4[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Area_J4[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Area_J4[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Area_J5[x] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.Area_J5[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Area_J5[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Area_J5[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.Area_J6[x] valid ?
            if SysDepIsValidReal(Value=self.ParCmd.Area_J6[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Area_J6[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Area_J6[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

        # Check ParCmd.Position_1.J1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.J1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.J1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.J1))
            return CheckParameterValid

        # Check ParCmd.Position_1.J2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.J2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.J2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.J2))
            return CheckParameterValid

        # Check ParCmd.Position_1.J3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.J3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.J3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.J3))
            return CheckParameterValid

        # Check ParCmd.Position_1.J4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.J4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.J4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.J4))
            return CheckParameterValid

        # Check ParCmd.Position_1.J5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.J5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.J5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.J5))
            return CheckParameterValid

        # Check ParCmd.Position_1.J6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.J6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.J6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.J6))
            return CheckParameterValid

        # Check ParCmd.Position_1.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.E1))
            return CheckParameterValid

        # Check ParCmd.Position_1.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.E2))
            return CheckParameterValid

        # Check ParCmd.Position_1.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.E3))
            return CheckParameterValid

        # Check ParCmd.Position_1.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.E4))
            return CheckParameterValid

        # Check ParCmd.Position_1.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.E5))
            return CheckParameterValid

        # Check ParCmd.Position_1.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_1.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_1.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_1.E6))
            return CheckParameterValid

        # Check ParCmd.Position_2.J1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.J1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.J1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.J1))
            return CheckParameterValid

        # Check ParCmd.Position_2.J2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.J2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.J2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.J2))
            return CheckParameterValid

        # Check ParCmd.Position_2.J3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.J3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.J3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.J3))
            return CheckParameterValid

        # Check ParCmd.Position_2.J4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.J4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.J4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.J4))
            return CheckParameterValid

        # Check ParCmd.Position_2.J5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.J5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.J5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.J5))
            return CheckParameterValid

        # Check ParCmd.Position_2.J6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.J6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.J6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.J6))
            return CheckParameterValid

        # Check ParCmd.Position_2.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.E1))
            return CheckParameterValid

        # Check ParCmd.Position_2.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.E2))
            return CheckParameterValid

        # Check ParCmd.Position_2.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.E3))
            return CheckParameterValid

        # Check ParCmd.Position_2.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.E4))
            return CheckParameterValid

        # Check ParCmd.Position_2.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.E5))
            return CheckParameterValid

        # Check ParCmd.Position_2.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_2.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_2.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_2.E6))
            return CheckParameterValid

        # Check ParCmd.ConfigurationAngle valid ?
        if SysDepIsValidReal(Value=self.ParCmd.ConfigurationAngle) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ConfigurationAngle = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.ConfigurationAngle))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.LoadMeasurementAutomatic
        # ST-FIX F51: ExecutionMode from AbortingMode and SequenceFlag (spec table 5-77)
        if self.SequenceFlag == SequenceFlag.SECONDARY_SEQUENCE:
            if self.AbortingMode == AbortingMode.ABORT:
                self._command.ExecMode = ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY
            else:
                self._command.ExecMode = ExecutionMode.SEQUENCE_SECONDARY
        else:
            if self.AbortingMode == AbortingMode.ABORT:
                self._command.ExecMode = ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY
            else:
                self._command.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        self._command.Mass = self.ParCmd.Mass
        self._command.Mode = self.ParCmd.Mode
        self._command.Reserved = 0
        copy_into(self._command.Area_J3, self.ParCmd.Area_J3)
        copy_into(self._command.Area_J4, self.ParCmd.Area_J4)
        copy_into(self._command.Area_J5, self.ParCmd.Area_J5)
        copy_into(self._command.Area_J6, self.ParCmd.Area_J6)
        self._command.ConfigurationAngle = self.ParCmd.ConfigurationAngle
        copy_into(self._command.Position_1, self.ParCmd.Position_1)
        copy_into(self._command.Position_2, self.ParCmd.Position_2)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Mass
            CreateCommandPayload.AddReal(Value=self._command.Mass)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Mode
            CreateCommandPayload.AddUsint(Value=self._command.Mode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserved
            CreateCommandPayload.AddByte(Value=self._command.Reserved)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J3[0]
            CreateCommandPayload.AddReal(Value=self._command.Area_J3[0])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J3[1]
            CreateCommandPayload.AddReal(Value=self._command.Area_J3[1])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J4[0]
            CreateCommandPayload.AddReal(Value=self._command.Area_J4[0])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J4[1]
            CreateCommandPayload.AddReal(Value=self._command.Area_J4[1])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J5[0]
            CreateCommandPayload.AddReal(Value=self._command.Area_J5[0])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J5[1]
            CreateCommandPayload.AddReal(Value=self._command.Area_J5[1])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J6[0]
            CreateCommandPayload.AddReal(Value=self._command.Area_J6[0])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Area_J6[1]
            CreateCommandPayload.AddReal(Value=self._command.Area_J6[1])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ConfigurationAngle
            CreateCommandPayload.AddReal(Value=self._command.ConfigurationAngle)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.J1
            CreateCommandPayload.AddReal(Value=self._command.Position_1.J1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.J2
            CreateCommandPayload.AddReal(Value=self._command.Position_1.J2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.J3
            CreateCommandPayload.AddReal(Value=self._command.Position_1.J3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.J4
            CreateCommandPayload.AddReal(Value=self._command.Position_1.J4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.J5
            CreateCommandPayload.AddReal(Value=self._command.Position_1.J5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.J6
            CreateCommandPayload.AddReal(Value=self._command.Position_1.J6)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.E1
            CreateCommandPayload.AddReal(Value=self._command.Position_1.E1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.E2
            CreateCommandPayload.AddReal(Value=self._command.Position_1.E2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.E3
            CreateCommandPayload.AddReal(Value=self._command.Position_1.E3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.E4
            CreateCommandPayload.AddReal(Value=self._command.Position_1.E4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.E5
            CreateCommandPayload.AddReal(Value=self._command.Position_1.E5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_1.E6
            CreateCommandPayload.AddReal(Value=self._command.Position_1.E6)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.J1
            CreateCommandPayload.AddReal(Value=self._command.Position_2.J1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.J2
            CreateCommandPayload.AddReal(Value=self._command.Position_2.J2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.J3
            CreateCommandPayload.AddReal(Value=self._command.Position_2.J3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.J4
            CreateCommandPayload.AddReal(Value=self._command.Position_2.J4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.J5
            CreateCommandPayload.AddReal(Value=self._command.Position_2.J5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.J6
            CreateCommandPayload.AddReal(Value=self._command.Position_2.J6)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.E1
            CreateCommandPayload.AddReal(Value=self._command.Position_2.E1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.E2
            CreateCommandPayload.AddReal(Value=self._command.Position_2.E2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.E3
            CreateCommandPayload.AddReal(Value=self._command.Position_2.E3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.E4
            CreateCommandPayload.AddReal(Value=self._command.Position_2.E4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.E5
            CreateCommandPayload.AddReal(Value=self._command.Position_2.E5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position_2.E6
            CreateCommandPayload.AddReal(Value=self._command.Position_2.E6)
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
        # Create log entry for Mass
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mass = {1}', Para1=REAL_TO_STRING(self._command.Mass))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Mode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mode = {1}', Para1=LOAD_MEASUREMENT_MODE_TO_STRING(Value=self._command.Mode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserved
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserved = {1}', Para1=REAL_TO_STRING(self._command.Reserved))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J3[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J3[0] = {1}', Para1=REAL_TO_STRING(self._command.Area_J3[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J3[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J3[1] = {1}', Para1=REAL_TO_STRING(self._command.Area_J3[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J4[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J4[0] = {1}', Para1=REAL_TO_STRING(self._command.Area_J4[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J4[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J4[1] = {1}', Para1=REAL_TO_STRING(self._command.Area_J4[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J5[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J5[0] = {1}', Para1=REAL_TO_STRING(self._command.Area_J5[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J5[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J5[1] = {1}', Para1=REAL_TO_STRING(self._command.Area_J5[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J6[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J6[0] = {1}', Para1=REAL_TO_STRING(self._command.Area_J6[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Area_J6[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Area_J6[1] = {1}', Para1=REAL_TO_STRING(self._command.Area_J6[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ConfigurationAngle
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ConfigurationAngle = {1}', Para1=REAL_TO_STRING(self._command.ConfigurationAngle))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.J1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.J1 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.J1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.J2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.J2 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.J2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.J3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.J3 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.J3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.J4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.J4 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.J4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.J5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.J5 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.J5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.J6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.J6 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.J6))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.E1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.E1 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.J1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.J1 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.J1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.J2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.J2 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.J2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.J3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.J3 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.J3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.J4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.J4 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.J4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.J5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.J5 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.J5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.J6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.J6 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.J6))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.E1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.E1 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.E2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.E2 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.E3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.E3 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.E4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.E4 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.E5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.E5 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_1.E6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_1.E6 = {1}', Para1=REAL_TO_STRING(self._command.Position_1.E6))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.E2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.E2 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.E3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.E3 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.E4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.E4 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.E5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.E5 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position_2.E6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position_2.E6 = {1}', Para1=REAL_TO_STRING(self._command.Position_2.E6))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_LoadMeasurementAutomaticFB'

        self.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
        self.Priority = PriorityLevel.NORMAL
        self.AbortingMode = AbortingMode.BUFFER
        self.SequenceFlag = SequenceFlag.PRIMARY_SEQUENCE
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(LoadMeasurementAutomaticOutCmd)), Value=0, DataLen=49)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.MeasuringID = self._response.MeasuringID
            copy_into(self.OutCmd.LoadData, self._response.LoadData)
            self.OutCmd.LoadDataAvailable = self._response.LoadDataAvailable

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(LoadMeasurementAutomaticOutCmd)), Value=0, DataLen=49)
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
        self.Active = False
        self.CommandBuffered = False
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
                self.Active = True
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
            # Get Response.LoadData.Timestamp.TsData
            self._response.LoadData.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Timestamp.TsTime
            self._response.LoadData.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.X
            self._response.LoadData.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Y
            self._response.LoadData.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Z
            self._response.LoadData.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Rx
            self._response.LoadData.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Ry
            self._response.LoadData.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Rz
            self._response.LoadData.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Mass
            self._response.LoadData.Mass = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Ix
            self._response.LoadData.Ix = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Iy
            self._response.LoadData.Iy = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadData.Iz
            self._response.LoadData.Iz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.LoadDataAvailable
            self._response.LoadDataAvailable = ResponseData.GetBool()
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
        # Create log entry for LoadData.Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._response.LoadData.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Timestamp.IEC_TIME
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._response.LoadData.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.X
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.X = {1}', Para1=REAL_TO_STRING(self._response.LoadData.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Y
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Y = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Z
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Z = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Rx
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Rx = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Ry
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Ry = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Rz
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Rz = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Mass
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Mass = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Mass))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Ix
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Ix = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Ix))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Iy
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Iy = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Iy))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadData.Iz
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadData.Iz = {1}', Para1=REAL_TO_STRING(self._response.LoadData.Iz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LoadDataAvailable
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.LoadDataAvailable = {1}', Para1=BOOL_TO_STRING(self._response.LoadDataAvailable))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.Active = False
        self.CommandBuffered = False
        self.CommandAborted = False
        self.CommandInterrupted = False
        return Reset
