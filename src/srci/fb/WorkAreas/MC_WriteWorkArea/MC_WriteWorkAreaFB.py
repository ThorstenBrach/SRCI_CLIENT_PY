"""Define work area

ST-Source: POUs/WorkAreas/MC_WriteWorkArea/MC_WriteWorkAreaFB.st
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
from srci.functions.Convert.TO_STRING.AREA_TYPE_TO_STRING import AREA_TYPE_TO_STRING
from srci.functions.Convert.TO_STRING.DEFINITION_MODE_TO_STRING import DEFINITION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.functions.Convert.TO_STRING.WORK_AREA_REACTION_MODE_TO_STRING import WORK_AREA_REACTION_MODE_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import AreaType, CmdMessageState, CmdType, DefinitionMode, ExecutionMode, MessageType, PriorityLevel, ProcessingMode, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime, WorkAreaReactionMode, WriteWorkAreaOutCmd, WriteWorkAreaParCmd, WriteWorkAreaRecvData, WriteWorkAreaSendData

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_WriteWorkAreaFB']


class MC_WriteWorkAreaFB(RobotLibraryBaseExecuteFB):
    """Define work area"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Processing Mode
        self.ProcessingMode: ProcessingMode = ProcessingMode.BUFFERED
        # command parameter
        self.ParCmd: WriteWorkAreaParCmd = WriteWorkAreaParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command outputs
        self.OutCmd: WriteWorkAreaOutCmd = WriteWorkAreaOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: WriteWorkAreaParCmd = WriteWorkAreaParCmd()
        # command data to send
        self._command: WriteWorkAreaSendData = WriteWorkAreaSendData()
        # response data received
        self._response: WriteWorkAreaRecvData = WriteWorkAreaRecvData()

    def __call__(self, *, ProcessingMode: ProcessingMode | None = None, ParCmd: WriteWorkAreaParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if ProcessingMode is not None:
            self.ProcessingMode = ProcessingMode(ProcessingMode)
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 156)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 156)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 156 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 156, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(WriteWorkAreaSendData)), DataLen=156)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 156 - PayloadPtr, 156)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 156, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 156, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK

        # ST-FIX F28: payload order differs from the structure layout -> always add the parameter
        CheckAddParameter = True
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.WriteWorkArea

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 149 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(WriteWorkAreaParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(WriteWorkAreaParCmd)), DataLen=149) != RobotLibraryConstants.OK

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

        # Check ParCmd.WorkAreaNo valid ?
        if ((self.ParCmd.WorkAreaNo < 0 or self.ParCmd.WorkAreaNo > 254) or self.ParCmd.WorkAreaNo > AxesGroup.State.ConfigurationData.HighestWorkAreaIndex) or self.ParCmd.WorkAreaNo > AxesGroup.State.UnifiedWorkAreaIndex:
            # Parameter not valid
            CheckParameterValid = False

            # Check LoadNo available on RC ?
            if self.ParCmd.WorkAreaNo > AxesGroup.State.ConfigurationData.HighestWorkAreaIndex:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_WORKAREANO_UNAVAILABLE, Overwrite=True)
            else:
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_WORKAREANO_RANGE, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.WorkAreaNo))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.AreaType valid ?
        if ((self.ParCmd.WorkAreaData.AreaType != AreaType.AXES and self.ParCmd.WorkAreaData.AreaType != AreaType.BOX) and self.ParCmd.WorkAreaData.AreaType != AreaType.CYLINDER) and self.ParCmd.WorkAreaData.AreaType != AreaType.SPHERE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.AreaType = {1}', Para1=AREA_TYPE_TO_STRING(Value=self.ParCmd.WorkAreaData.AreaType))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.AreaMode valid ?
        if self.ParCmd.WorkAreaData.AreaMode != False and self.ParCmd.WorkAreaData.AreaMode != True:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.AreaMode = {1}', Para1=BOOL_TO_STRING(self.ParCmd.WorkAreaData.AreaMode))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.ReactionMode valid ?
        if (self.ParCmd.WorkAreaData.ReactionMode != WorkAreaReactionMode.NO_REACTION and self.ParCmd.WorkAreaData.ReactionMode != WorkAreaReactionMode.ABORT) and self.ParCmd.WorkAreaData.ReactionMode != WorkAreaReactionMode.INTERRUPT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.ReactionMode = {1}', Para1=WORK_AREA_REACTION_MODE_TO_STRING(Value=self.ParCmd.WorkAreaData.ReactionMode))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.ActiveModification valid ?
        if self.ParCmd.WorkAreaData.ActiveModification != False and self.ParCmd.WorkAreaData.ActiveModification != True:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.ActiveModification = {1}', Para1=BOOL_TO_STRING(self.ParCmd.WorkAreaData.ActiveModification))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.DefinitionMode valid ?
        if self.ParCmd.WorkAreaData.DefinitionMode != DefinitionMode.Center and self.ParCmd.WorkAreaData.DefinitionMode != DefinitionMode.Face:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.DefinitionMode = {1}', Para1=DEFINITION_MODE_TO_STRING(Value=self.ParCmd.WorkAreaData.DefinitionMode))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.FrameNo valid ?
        if self.ParCmd.WorkAreaData.FrameNo < 0 or self.ParCmd.WorkAreaData.FrameNo > 254:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.FrameNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.WorkAreaData.FrameNo))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.ZeroPointX valid ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.ZeroPointX) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.ZeroPointX = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.ZeroPointX))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.ZeroPointY valid ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.ZeroPointY) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.ZeroPointY = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.ZeroPointY))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.ZeroPointZ valid ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.ZeroPointZ) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.ZeroPointZ = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.ZeroPointZ))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.X.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.X.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.X.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.X.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.X.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.X.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.X.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.X.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.Y.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.Y.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.Y.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.Y.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.Y.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.Y.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.Y.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.Y.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.Z.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.Z.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.Z.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.Z.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.Z.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.Z.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.WorkAreaData.Z.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.Z.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.Radius ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.Radius) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Radius = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.Radius))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J1Limit.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J1Limit.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J1Limit.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J1Limit.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J1Limit.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J1Limit.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J1Limit.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J1Limit.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J2Limit.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J2Limit.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J2Limit.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J2Limit.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J2Limit.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J2Limit.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J2Limit.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J2Limit.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J3Limit.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J3Limit.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J3Limit.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J3Limit.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J3Limit.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J3Limit.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J3Limit.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J3Limit.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J4Limit.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J4Limit.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J4Limit.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J4Limit.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J4Limit.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J4Limit.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J4Limit.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J4Limit.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J5Limit.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J5Limit.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J5Limit.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J5Limit.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J5Limit.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J5Limit.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J5Limit.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J5Limit.UpperLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J6Limit.LowerLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J6Limit.LowerLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J6Limit.LowerLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J6Limit.LowerLimit))
            return CheckParameterValid

        # Check ParCmd.WorkAreaData.J6Limit.UpperLimit ?
        if SysDepIsValidReal(Value=self.ParCmd.WorkAreaData.J6Limit.UpperLimit) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.J6Limit.UpperLimit = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.WorkAreaData.J6Limit.UpperLimit))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.WriteWorkArea
        # ST-FIX F51: ExecutionMode from ProcessingMode (and SequenceFlag), spec table 5-77
        match self.ProcessingMode:
            case ProcessingMode.BUFFERED | ProcessingMode.TRIGGER_BUFFERED:
                if False:
                    self._command.ExecMode = ExecutionMode.SEQUENCE_SECONDARY
                else:
                    self._command.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
            case ProcessingMode.ABORTING | ProcessingMode.TRIGGER_ABORTING:
                if False:
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
                self.OnUpdateStateFlags(State=CmdMessageState.ERROR)
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority

        copy_into(self._command.WorkAreaData, self._parCmd.WorkAreaData)
        self._command.WorkAreaNo = self._parCmd.WorkAreaNo

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaNo
            CreateCommandPayload.AddUint(Value=self._command.WorkAreaNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ToolData.Timestamp.IEC_DATE
            CreateCommandPayload.AddUint(Value=self._command.WorkAreaData.Timestamp.IEC_DATE)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ToolData.Timestamp.IEC_TIME
            CreateCommandPayload.AddTime(Value=self._command.WorkAreaData.Timestamp.IEC_TIME)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.AreaType
            CreateCommandPayload.AddUsint(Value=self._command.WorkAreaData.AreaType)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.AreaMode
            CreateCommandPayload.AddBool(Value=self._command.WorkAreaData.AreaMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.ReactionMode
            CreateCommandPayload.AddUsint(Value=self._command.WorkAreaData.ReactionMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.ActiveModification
            CreateCommandPayload.AddBool(Value=self._command.WorkAreaData.ActiveModification)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # ST-FIX F33: WorkAreaData.DefinitionMode removed
        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.FrameNo
            CreateCommandPayload.AddUsint(Value=self._command.WorkAreaData.FrameNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.ZeroPointX
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.ZeroPointX)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.ZeroPointY
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.ZeroPointY)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.ZeroPointZ
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.ZeroPointZ)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.X.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.X.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.X.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.X.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.Y.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.Y.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.Y.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.Y.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.Z.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.Z.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.Z.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.Z.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.Radius
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.Radius)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J1Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J1Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J2Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J2Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J3Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J3Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J4Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J4Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J5Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J5Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J6Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J6Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E1Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E1Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J1Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J1Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J2Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J2Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J3Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J3Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J4Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J4Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J5Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J5Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.J6Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.J6Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E1Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E1Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E2Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E2Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E3Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E3Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E4Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E4Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E5Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E5Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E6Limit.LowerLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E6Limit.LowerLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E2Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E2Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E3Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E3Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E4Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E4Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E5Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E5Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.WorkAreaData.E6Limit.UpperLimit
            CreateCommandPayload.AddReal(Value=self._command.WorkAreaData.E6Limit.UpperLimit)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DataChanged
            CreateCommandPayload.AddBool(Value=self._command.DataChanged)
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
        # Create log entry for WorkAreaNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaNo = {1}', Para1=UINT_TO_STRING(self._command.WorkAreaNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._command.WorkAreaData.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._command.WorkAreaData.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.AreaType
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.AreaType = {1}', Para1=AREA_TYPE_TO_STRING(Value=self._command.WorkAreaData.AreaType))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.AreaMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.AreaMode = {1}', Para1=BOOL_TO_STRING(self._command.WorkAreaData.AreaMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ReactionMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.ReactionMode = {1}', Para1=WORK_AREA_REACTION_MODE_TO_STRING(Value=self._command.WorkAreaData.ReactionMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ActiveModification
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.ActiveModification = {1}', Para1=BOOL_TO_STRING(self._command.WorkAreaData.ActiveModification))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.DefinitionMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.DefinitionMode = {1}', Para1=DEFINITION_MODE_TO_STRING(Value=self._command.WorkAreaData.DefinitionMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.FrameNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.FrameNo = {1}', Para1=USINT_TO_STRING(self._command.WorkAreaData.FrameNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ZeroPointX
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.ZeroPointX = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.ZeroPointX))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ZeroPointY
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.ZeroPointY = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.ZeroPointY))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.ZeroPointZ
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.ZeroPointZ = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.ZeroPointZ))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.X.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.X.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.X.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.X.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.X.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.X.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Y.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Y.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.Y.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Y.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Y.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.Y.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Z.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Z.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.Z.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Z.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Z.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.Z.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.Radius
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.Radius = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.Radius))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J1Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J1Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J1Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J2Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J2Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J2Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J3Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J3Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J3Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J4Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J4Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J4Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J5Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J5Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J5Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J6Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J6Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J6Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E1Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E1Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E1Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J1Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J1Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J1Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J2Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J2Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J2Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J3Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J3Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J3Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J4Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J4Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J4Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J5Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J5Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J5Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.J6Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.J6Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.J6Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E1Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E1Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E1Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E2Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E2Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E2Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E3Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E3Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E3Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E4Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E4Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E4Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E5Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E5Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E5Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E6Limit.LowerLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E6Limit.LowerLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E6Limit.LowerLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E2Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E2Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E2Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E3Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E3Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E3Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E4Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E4Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E4Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E5Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E5Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E5Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for WorkAreaData.E6Limit.UpperLimit
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.WorkAreaData.E6Limit.UpperLimit = {1}', Para1=REAL_TO_STRING(self._command.WorkAreaData.E6Limit.UpperLimit))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataChanged
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DataChanged = {1}', Para1=BOOL_TO_STRING(self._command.DataChanged))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_WriteWorkAreaFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(WriteWorkAreaOutCmd)), Value=0, DataLen=0)
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
                        # Update the WorAreas in user defined system datas
                        AxesGroup.SystemData.UpdateWorAreas(Caller=self, SystemTime=AxesGroup.State.SystemTime, WorkAreaNo=self._parCmd.WorkAreaNo, WorkAreaData=self._parCmd.WorkAreaData)
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
        return Reset
