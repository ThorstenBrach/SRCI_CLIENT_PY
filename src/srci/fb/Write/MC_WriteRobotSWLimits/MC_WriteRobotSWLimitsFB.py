# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_WriteRobotSWLimitsFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Change robot limits of robot axes (degree)
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

"""Change robot limits of robot axes (degree)

ST-Source: POUs/Write/MC_WriteRobotSWLimits/MC_WriteRobotSWLimitsFB.st
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
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING, REAL_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime, WriteRobotSWLimitsOutCmd, WriteRobotSWLimitsParCmd, WriteRobotSWLimitsRecvData, WriteRobotSWLimitsSendData

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_WriteRobotSWLimitsFB']


class MC_WriteRobotSWLimitsFB(RobotLibraryBaseExecuteFB):
    """Change robot limits of robot axes (degree)"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: WriteRobotSWLimitsParCmd = WriteRobotSWLimitsParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command outputs
        self.OutCmd: WriteRobotSWLimitsOutCmd = WriteRobotSWLimitsOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: WriteRobotSWLimitsParCmd = WriteRobotSWLimitsParCmd()
        # command data to send
        self._command: WriteRobotSWLimitsSendData = WriteRobotSWLimitsSendData()
        # response data received
        self._response: WriteRobotSWLimitsRecvData = WriteRobotSWLimitsRecvData()

    def __call__(self, *, ParCmd: WriteRobotSWLimitsParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 108)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 108)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 108 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 108, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(WriteRobotSWLimitsSendData)), DataLen=108)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 108 - PayloadPtr, 108)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 108, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 108, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK

        # ST-FIX F28: payload order differs from the structure layout -> always add the parameter
        CheckAddParameter = True
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotSWLimits

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 103 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(WriteRobotSWLimitsParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(WriteRobotSWLimitsParCmd)), DataLen=103) != RobotLibraryConstants.OK

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

        # Check ParCmd.LimitValues.J1LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J1LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J1LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J1LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J1UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J1UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J1UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J1UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J2LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J2LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J2LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J2LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J2UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J2UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J2UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J2UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J3LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J3LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J3LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J3LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J3UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J3UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J3UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J3UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J4LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J4LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J4LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J4LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J4UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J4UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J4UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J4UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J5LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J5LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J5LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J5LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J5UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J5UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J5UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J5UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J6LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J6LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J6LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J6LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.J6UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.J6UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.J6UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.J6UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E1LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E1LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E1LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E1LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E1UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E1UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E1UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E1UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E2LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E2LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E2LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E2LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E2UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E2UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E2UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E2UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E3LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E3LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E3LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E3LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E3UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E3UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E3UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E3UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E4LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E4LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E4LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E4LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E4UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E4UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E4UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E4UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E5LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E5LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E5LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E5LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E5UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E5UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E5UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E5UpperLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E6LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E6LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E6LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E6LowerLimit))

            return CheckParameterValid

        # Check ParCmd.LimitValues.E6UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.LimitValues.E6UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.LimitValues.E6UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.LimitValues.E6UpperLimit))

            return CheckParameterValid

        # Check ParCmd.ResetToFactoryDefaults ?
        if self.ParCmd.ResetToFactoryDefaults != False and self.ParCmd.ResetToFactoryDefaults != True:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ResetToFactoryDefaults = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ResetToFactoryDefaults))

            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.WriteRobotSWLimits
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        copy_into(self._command.LimitValues, self._parCmd.LimitValues)
        self._command.ResetToFactoryDefaults = self._parCmd.ResetToFactoryDefaults

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.Timestamp.IEC_DATE
            CreateCommandPayload.AddUint(Value=self._command.LimitValues.Timestamp.IEC_DATE)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.Timestamp.IEC_TIME
            CreateCommandPayload.AddTime(Value=self._command.LimitValues.Timestamp.IEC_TIME)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J1LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J1LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J2LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J2LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J3LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J3LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J41LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J4LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J5LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J5LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J6LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J6LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E1LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E1LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J1UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J1UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J2UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J2UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J3UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J3UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J4UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J4UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J5UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J5UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.J6UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.J6UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E1UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E1UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E2LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E2LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E3LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E3LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E4LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E4LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E5LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E5LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E6LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E6LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E2UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E2UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E3UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E3UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E4UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E4UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E5UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E5UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.LimitValues.E6UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.LimitValues.E6UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # ST-FIX F31: ResetToFactoryDefaults (byte 106, spec table 6-209) was not sent
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            CreateCommandPayload.AddBool(Value=self._command.ResetToFactoryDefaults)
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
        # Create log entry for LimitValues.Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._command.LimitValues.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.Timestamp.IEC_TIME
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._command.LimitValues.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J1LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J1LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J1LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J2LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J2LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J2LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J3LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J3LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J3LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J4LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J4LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J4LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J5LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J5LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J5LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J6LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J6LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J6LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E1LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E1LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E1LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J1UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J1UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J1UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J2UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J2UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J2UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J3UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J3UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J3UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J4UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J4UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J4UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J5UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J5UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J5UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.J6UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.J6UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.J6UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E1UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E1UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E1UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E2LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E2LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E2LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E3LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E3LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E3LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E4LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E4LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E4LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E5LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E5LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E5LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E6LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E6LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E6LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E2UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E2UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E2UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E3UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E3UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E3UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E4UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E4UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E4UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E5UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E5UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E5UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for LimitValues.E6UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.LimitValues.E6UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.LimitValues.E6UpperLimit))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_WriteRobotSWLimitsFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(WriteRobotSWLimitsOutCmd)), Value=0, DataLen=1)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(WriteRobotSWLimitsOutCmd)), Value=0, DataLen=1)
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
                        # Update the SWLimits in user defined system datas
                        AxesGroup.SystemData.UpdateSWLimits(LimitValues=self._parCmd.LimitValues)
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
                pass
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Done = True
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
        # Create log entry for RestartRequested
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RestartRequested = {1}', Para1=BOOL_TO_STRING(self._response.RestartRequested))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        return Reset
