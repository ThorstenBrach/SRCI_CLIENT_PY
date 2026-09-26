# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_CalculateToolFB
#  Author:      Thorsten Brach
#  Date:        2024-06-09
#
#  Description:
#    Calculate tool (TCP) with four-point method
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

"""Calculate tool (TCP) with four-point method

ST-Source: POUs/Calculation/MC_CalculateTool/MC_CalculateToolFB.st
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
from srci.functions.Convert.Misc import CombineHalfSints
from srci.functions.Convert.TO_STRING.ARM_CONFIG_ELBOW_TO_STRING import ARM_CONFIG_ELBOW_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_SHOULDER_TO_STRING import ARM_CONFIG_SHOULDER_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_TO_STRING import ARM_CONFIG_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_WRIST_TO_STRING import ARM_CONFIG_WRIST_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.TOOL_CALCULATION_MODE_TO_STRING import TOOL_CALCULATION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, trunc_str, wrap
from srci.types import ArmConfigElbow, ArmConfigShoulder, ArmConfigWrist, CalculateToolOutCmd, CalculateToolParCmd, CalculateToolRecvData, CalculateToolSendData, CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime, ToolCalculationMode

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_CalculateToolFB']


class MC_CalculateToolFB(RobotLibraryBaseExecuteFB):
    """Calculate tool (TCP) with four-point method"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: CalculateToolParCmd = CalculateToolParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Command output
        self.OutCmd: CalculateToolOutCmd = CalculateToolOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: CalculateToolParCmd = CalculateToolParCmd()
        # command data to send
        self._command: CalculateToolSendData = CalculateToolSendData()
        # response data received
        self._response: CalculateToolRecvData = CalculateToolRecvData()
        # Incremented with each position of the input parameter "PositionsArray" sent from the PLC to the RC.
        # • Default: 0
        self._dataIndex: int = 0
        # Set TRUE by the client, when according to the user selected "Mode" the final position of the input parameter "PositionsArray" is sent to the RC.
        # • Default: FALSE
        self._dataComplete: bool = False

    def __call__(self, *, ParCmd: CalculateToolParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 72)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 72)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 72 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 72, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(CalculateToolSendData)), DataLen=72)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 72 - PayloadPtr, 72)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 72, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 72, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.CalculateTool

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 370 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(CalculateToolParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(CalculateToolParCmd)), DataLen=370) != RobotLibraryConstants.OK

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

        # Check ParCmd.Mode valid ?
        if (((((self.ParCmd.Mode != ToolCalculationMode.TWO_POINT_Z_METHOD and self.ParCmd.Mode != ToolCalculationMode.THREE_POINT_METHOD) and self.ParCmd.Mode != ToolCalculationMode.FOUR_POINT_METHOD) and self.ParCmd.Mode != ToolCalculationMode.FIVE_POINT_METHOD) and self.ParCmd.Mode != ToolCalculationMode.SIX_POINT_METHOD) and self.ParCmd.Mode != ToolCalculationMode.ABC_WORLD_METHOD) and self.ParCmd.Mode != ToolCalculationMode.ABC_TWO_POINT_METHOD:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mode = {1}', Para1=TOOL_CALCULATION_MODE_TO_STRING(Value=self.ParCmd.Mode))
            return CheckParameterValid

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

        # Check ParCmd.ExternalTCP valid ?
        if self.ParCmd.ExternalTCP != False and self.ParCmd.ExternalTCP != True:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ExternalTCP = {1}', Para1=BOOL_TO_STRING(self.ParCmd.ExternalTCP))
            return CheckParameterValid

        for _idx in range(0, 6):
            # Check ParCmd.PositionsArray[x].X valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].X) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].X), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Y valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].Y) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Y), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Z valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].Z) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Z), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Rx valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].Rx) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Rx), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Ry valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].Ry) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Ry), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Rz valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].Rz) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Rz), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].E1 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].E1) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].E1), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].E2 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].E1) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].E2), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].E3 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].E3) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].E3), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].E4 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].E4) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].E4), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].E5 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].E5) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].E5), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].E6 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.PositionsArray[_idx].E6) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].E6), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Config.Shoulder valid ?
            if (((self.ParCmd.PositionsArray[_idx].Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.PositionsArray[_idx].Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.PositionsArray[_idx].Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.PositionsArray[_idx].Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.PositionsArray[_idx].Config.Shoulder != ArmConfigShoulder.FRONT:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Config.Shoulder), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Config.Elbow valid ?
            if (((self.ParCmd.PositionsArray[_idx].Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.PositionsArray[_idx].Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.PositionsArray[_idx].Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.PositionsArray[_idx].Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.PositionsArray[_idx].Config.Elbow != ArmConfigElbow.UP:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2]].Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Config.Elbow), Para2=DINT_TO_STRING(_idx))

                break
                return CheckParameterValid

            # Check ParCmd.PositionsArray[x].Config.Wrist valid ?
            if (((self.ParCmd.PositionsArray[_idx].Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.PositionsArray[_idx].Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.PositionsArray[_idx].Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.PositionsArray[_idx].Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.PositionsArray[_idx].Config.Wrist != ArmConfigWrist.NON_FLIP:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PositionsArray[{2}].Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.PositionsArray[_idx].Config.Wrist), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.CalculateTool
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.DataIndex = self._dataIndex
        self._command.DataComplete = set_bit(self._command.DataComplete, 0, self._dataComplete)
        self._command.ToolNo = self._parCmd.ToolNo
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.Mode = self._parCmd.Mode
        self._command.ExternalTCP = set_bit(self._command.ExternalTCP, 0, self._parCmd.ExternalTCP)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TargetFrameNo
            CreateCommandPayload.AddUsint(Value=self._command.DataIndex)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DataComplete
            CreateCommandPayload.AddByte(Value=self._command.DataComplete)
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
            # add command.Mode
            CreateCommandPayload.AddSint(Value=self._command.Mode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Mode
            CreateCommandPayload.AddUsint(Value=self._command.ExternalTCP)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.X
            CreateCommandPayload.AddReal(Value=self._command.Position.X)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.Y
            CreateCommandPayload.AddReal(Value=self._command.Position.Y)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.Z
            CreateCommandPayload.AddReal(Value=self._command.Position.Z)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.Rx
            CreateCommandPayload.AddReal(Value=self._command.Position.Rx)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.Ry
            CreateCommandPayload.AddReal(Value=self._command.Position.Ry)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.Rz
            CreateCommandPayload.AddReal(Value=self._command.Position.Rz)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.Config
            CreateCommandPayload.AddArmConfig(Value=self._command.Position.Config)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.TurnNumber
            CreateCommandPayload.AddTurnNumber(Value=self._command.Position.TurnNumber)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.E1
            CreateCommandPayload.AddReal(Value=self._command.Position.E1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.E2
            CreateCommandPayload.AddReal(Value=self._command.Position.E2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.E3
            CreateCommandPayload.AddReal(Value=self._command.Position.E3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.E4
            CreateCommandPayload.AddReal(Value=self._command.Position.E4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.E5
            CreateCommandPayload.AddReal(Value=self._command.Position.E5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Position.E6
            CreateCommandPayload.AddReal(Value=self._command.Position.E6)
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
        # Create log entry for DataIndex
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DataIndex = {1}', Para1=USINT_TO_STRING(self._command.DataIndex))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DataComplete
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DataComplete = {1}', Para1=BYTE_TO_STRING(self._command.DataComplete))

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
        # Create log entry for Mode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mode = {1}', Para1=TOOL_CALCULATION_MODE_TO_STRING(Value=self._command.Mode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ExternalTCP
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ExternalTCP = {1}', Para1=BOOL_TO_STRING(bit(self._command.ExternalTCP, 0)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.X
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.X = {1}', Para1=REAL_TO_STRING(self._command.Position.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Y
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.Y = {1}', Para1=REAL_TO_STRING(self._command.Position.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Z
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.Z = {1}', Para1=REAL_TO_STRING(self._command.Position.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Rx
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.Rx = {1}', Para1=REAL_TO_STRING(self._command.Position.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Ry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.Ry = {1}', Para1=REAL_TO_STRING(self._command.Position.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Rz
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.Rz = {1}', Para1=REAL_TO_STRING(self._command.Position.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Config
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._command.Position.Config))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.TurnNumber[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.TurnNumber[0] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.Position.TurnNumber.J2Turns, HalfSintLo=self._command.Position.TurnNumber.J1Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.TurnNumber[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.TurnNumber[1] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.Position.TurnNumber.J4Turns, HalfSintLo=self._command.Position.TurnNumber.J3Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.TurnNumber[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.TurnNumber[2] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.Position.TurnNumber.J6Turns, HalfSintLo=self._command.Position.TurnNumber.J5Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.TurnNumber[3]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.TurnNumber[3] = {1}', Para1=SINT_TO_STRING(self._command.Position.TurnNumber.E1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.E1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.E1 = {1}', Para1=REAL_TO_STRING(self._command.Position.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.E2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.E2 = {1}', Para1=REAL_TO_STRING(self._command.Position.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.E3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.E3 = {1}', Para1=REAL_TO_STRING(self._command.Position.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.E4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.E4 = {1}', Para1=REAL_TO_STRING(self._command.Position.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.E5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.E5 = {1}', Para1=REAL_TO_STRING(self._command.Position.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.E6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.E6 = {1}', Para1=REAL_TO_STRING(self._command.Position.E6))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_CalculateToolFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(CalculateToolOutCmd)), Value=0, DataLen=41)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.TCPMaxError = self._response.TCPMaxError
            self.OutCmd.TCPMeanError = self._response.TCPMeanError
            copy_into(self.OutCmd.ToolData, self._response.ToolData)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(CalculateToolOutCmd)), Value=0, DataLen=41)
                        # apply command parameter
                        copy_into(self._parCmd, self.ParCmd)
                        # init parameter sequence
                        self._command.ParSeq = 1
                        # set timeout
                        SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 1:
                self._dataIndex = wrap(self._dataIndex + 1, 'USINT')

                match self._parCmd.Mode:

                    case ToolCalculationMode.TWO_POINT_Z_METHOD:
                        self._dataComplete = self._dataIndex >= 2

                    case ToolCalculationMode.THREE_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 3

                    case ToolCalculationMode.FOUR_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 4

                    case ToolCalculationMode.FIVE_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 5

                    case ToolCalculationMode.SIX_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 6

                    case ToolCalculationMode.ABC_WORLD_METHOD:
                        self._dataComplete = self._dataIndex >= 1

                    case ToolCalculationMode.ABC_TWO_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 2

                # create command data
                self.CommandData = self.CreateCommandPayload(AxesGroup=AxesGroup)
                # Add command to active command register
                self._uniqueID = AxesGroup.Acyclic.ActiveCommandRegister.AddCmd(pCommandFB=self)
                # set timeout
                SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                # inc step counter
                self._stepCmd = self._stepCmd + 1

            case 2:
                if self._responseReceived:
                    # reset response received flag
                    self._responseReceived = False
                    # update state flags
                    self.OnUpdateStateFlags(State=self._response.State)
                    # update state flags
                    self.OnApplyOutCmd(State=self._response.State)

                    # Done, Aborted or Error ?
                    if self._response.State >= CmdMessageState.DONE:
                        if self._dataComplete or self._response.State == CmdMessageState.ABORTED:
                            # set timeout
                            SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                            # inc step counter
                            self._stepCmd = self._stepCmd + 1
                        else:
                            # set timeout
                            SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                            # dec step counter
                            self._stepCmd = self._stepCmd - 1

            case 3:
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

        # ST-FIX F33: IEC_Date removed
        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TCPMaxError
            self._response.TCPMaxError = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TCPMeanError
            self._response.TCPMeanError = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1
        # ST-FIX F33
        self._response.ToolData.Timestamp.IEC_DATE = ResponseData.GetIecDate()
        _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.Time
            self._response.ToolData.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.X
            self._response.ToolData.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.Y
            self._response.ToolData.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.Z
            self._response.ToolData.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.Rx
            self._response.ToolData.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.Ry
            self._response.ToolData.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.Rz
            self._response.ToolData.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.ID
            self._response.ToolData.ID = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.LoadNo
            self._response.ToolData.LoadNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.ToolData.ExternalTCP
            self._response.ToolData.ExternalTCP = ResponseData.GetBool()
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
        # Create log entry for IEC_Date
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._response.ToolData.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TCPMaxError
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TCPMaxError = {1}', Para1=REAL_TO_STRING(self._response.TCPMaxError))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TCPMeanError
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TCPMeanError = {1}', Para1=REAL_TO_STRING(self._response.TCPMeanError))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for IEC_Time
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._response.ToolData.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.X
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.X = {1}', Para1=REAL_TO_STRING(self._response.ToolData.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.Y
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Y = {1}', Para1=REAL_TO_STRING(self._response.ToolData.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.Z
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Z = {1}', Para1=REAL_TO_STRING(self._response.ToolData.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.Rx
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Rx = {1}', Para1=REAL_TO_STRING(self._response.ToolData.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.Ry
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Ry = {1}', Para1=REAL_TO_STRING(self._response.ToolData.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.Rz
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.Rz = {1}', Para1=REAL_TO_STRING(self._response.ToolData.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.ID
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.ID = {1}', Para1=USINT_TO_STRING(self._response.ToolData.ID))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.LoadNo
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.LoadNo = {1}', Para1=USINT_TO_STRING(self._response.ToolData.LoadNo))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ToolData.ExternalTCP
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ToolData.ExternalTCP = {1}', Para1=BOOL_TO_STRING(self._response.ToolData.ExternalTCP))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        return Reset
