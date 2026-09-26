# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_CalculateFrameFB
#  Author:      Thorsten Brach
#  Date:        2024-06-09
#
#  Description:
#    Calculate frame with three-point method
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

"""Calculate frame with three-point method

ST-Source: POUs/Calculation/MC_CalculateFrame/MC_CalculateFrameFB.st
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
from srci.functions.Convert.TO_STRING.FRAME_CALCULATION_MODE_TO_STRING import FRAME_CALCULATION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_DATE_TO_STRING import IEC_DATE_TO_STRING
from srci.functions.Convert.TO_STRING.IEC_TIME_TO_STRING import IEC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BYTE_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, set_bit, trunc_str, wrap
from srci.types import ArmConfigElbow, ArmConfigShoulder, ArmConfigWrist, CalculateFrameOutCmd, CalculateFrameParCmd, CalculateFrameRecvData, CalculateFrameSendData, CmdMessageState, CmdType, ExecutionMode, FrameCalculationMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_CalculateFrameFB']


class MC_CalculateFrameFB(RobotLibraryBaseExecuteFB):
    """Calculate frame with three-point method"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: CalculateFrameParCmd = CalculateFrameParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # Command output
        self.OutCmd: CalculateFrameOutCmd = CalculateFrameOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: CalculateFrameParCmd = CalculateFrameParCmd()
        # command data to send
        self._command: CalculateFrameSendData = CalculateFrameSendData()
        # response data received
        self._response: CalculateFrameRecvData = CalculateFrameRecvData()
        # Incremented with each position of the input parameter "PositionsArray" sent from the PLC to the RC.
        # Default: 0
        self._dataIndex: int = 0
        # Set TRUE by the client, when according to the user selected "Mode" the final position of the input parameter "PositionsArray" is sent to the RC.
        # Default: FALSE
        self._dataComplete: bool = False

    def __call__(self, *, ParCmd: CalculateFrameParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 72, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(CalculateFrameSendData)), DataLen=72)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 72 - PayloadPtr, 72)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 72, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 72, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.CalculateFrame

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 247 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(CalculateFrameParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(CalculateFrameParCmd)), DataLen=247) != RobotLibraryConstants.OK

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
        if (self.ParCmd.Mode != FrameCalculationMode.THREE_POINT_METHOD and self.ParCmd.Mode != FrameCalculationMode.FOUR_POINT_METHOD) and self.ParCmd.Mode != FrameCalculationMode.ONE_POINT_METHOD:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_FRAMECALCULATIONMODE_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mode = {1}', Para1=FRAME_CALCULATION_MODE_TO_STRING(Value=self.ParCmd.Mode))
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

        # Check ParCmd.Position_X.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.X))
            return CheckParameterValid

        # Check ParCmd.Position_X.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.Y))
            return CheckParameterValid

        # Check ParCmd.Position_X.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.Z))
            return CheckParameterValid

        # Check ParCmd.Position_X.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.Rx))
            return CheckParameterValid

        # Check ParCmd.Position_X.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.Ry))
            return CheckParameterValid

        # Check ParCmd.Position_X.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.Rz))
            return CheckParameterValid

        # Check ParCmd.Position_X.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.E1))
            return CheckParameterValid

        # Check ParCmd.Position_X.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.E2))
            return CheckParameterValid

        # Check ParCmd.Position_X.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.E3))
            return CheckParameterValid

        # Check ParCmd.Position_X.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.E4))
            return CheckParameterValid

        # Check ParCmd.Position_X.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.E5))
            return CheckParameterValid

        # Check ParCmd.Position_X.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_X.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_X.E6))
            return CheckParameterValid

        # Check ParCmd.Position_X.Config.Shoulder valid ?
        if (((self.ParCmd.Position_X.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.Position_X.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.Position_X.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.Position_X.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.Position_X.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.Position_X.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.Position_X.Config.Elbow valid ?
        if (((self.ParCmd.Position_X.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.Position_X.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.Position_X.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.Position_X.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.Position_X.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.Position_X.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.Position_X.Config.Wrist valid ?
        if (((self.ParCmd.Position_X.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.Position_X.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.Position_X.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.Position_X.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.Position_X.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_X.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.Position_X.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.Position_XY.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.X))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.Y))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.Z))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.Rx))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.Ry))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.Rz))
            return CheckParameterValid

        # Check ParCmd.Position_XY.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.E1))
            return CheckParameterValid

        # Check ParCmd.Position_XY.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.E2))
            return CheckParameterValid

        # Check ParCmd.Position_XY.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.E3))
            return CheckParameterValid

        # Check ParCmd.Position_XY.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.E4))
            return CheckParameterValid

        # Check ParCmd.Position_XY.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.E5))
            return CheckParameterValid

        # Check ParCmd.Position_XY.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position_XY.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position_XY.E6))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Config.Shoulder valid ?
        if (((self.ParCmd.Position_XY.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.Position_XY.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.Position_XY.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.Position_XY.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.Position_XY.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.Position_XY.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Config.Elbow valid ?
        if (((self.ParCmd.Position_XY.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.Position_XY.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.Position_XY.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.Position_XY.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.Position_XY.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.Position_XY.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.Position_XY.Config.Wrist valid ?
        if (((self.ParCmd.Position_XY.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.Position_XY.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.Position_XY.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.Position_XY.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.Position_XY.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position_XY.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.Position_XY.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.Origin.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.X))
            return CheckParameterValid

        # Check ParCmd.Origin.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.Y))
            return CheckParameterValid

        # Check ParCmd.Origin.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.Z))
            return CheckParameterValid

        # Check ParCmd.Origin.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.Rx))
            return CheckParameterValid

        # Check ParCmd.Origin.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.Ry))
            return CheckParameterValid

        # Check ParCmd.Origin.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.Rz))
            return CheckParameterValid

        # Check ParCmd.Origin.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.E1))
            return CheckParameterValid

        # Check ParCmd.Origin.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.E2))
            return CheckParameterValid

        # Check ParCmd.Origin.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.E3))
            return CheckParameterValid

        # Check ParCmd.Origin.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.E4))
            return CheckParameterValid

        # Check ParCmd.Origin.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.E5))
            return CheckParameterValid

        # Check ParCmd.Origin.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Origin.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Origin.E6))
            return CheckParameterValid

        # Check ParCmd.Origin.Config.Shoulder valid ?
        if (((self.ParCmd.Origin.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.Origin.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.Origin.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.Origin.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.Origin.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.Origin.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.Origin.Config.Elbow valid ?
        if (((self.ParCmd.Origin.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.Origin.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.Origin.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.Origin.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.Origin.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.Origin.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.Origin.Config.Wrist valid ?
        if (((self.ParCmd.Origin.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.Origin.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.Origin.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.Origin.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.Origin.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Origin.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.Origin.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.OriginShift.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.X))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.Y))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.Z))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.Rx))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.Ry))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.Rz))
            return CheckParameterValid

        # Check ParCmd.OriginShift.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.E1))
            return CheckParameterValid

        # Check ParCmd.OriginShift.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.E2))
            return CheckParameterValid

        # Check ParCmd.OriginShift.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.E3))
            return CheckParameterValid

        # Check ParCmd.OriginShift.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.E4))
            return CheckParameterValid

        # Check ParCmd.OriginShift.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.E5))
            return CheckParameterValid

        # Check ParCmd.OriginShift.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.OriginShift.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.OriginShift.E6))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Config.Shoulder valid ?
        if (((self.ParCmd.OriginShift.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.OriginShift.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.OriginShift.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.OriginShift.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.OriginShift.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.OriginShift.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Config.Elbow valid ?
        if (((self.ParCmd.OriginShift.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.OriginShift.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.OriginShift.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.OriginShift.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.OriginShift.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.OriginShift.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.OriginShift.Config.Wrist valid ?
        if (((self.ParCmd.OriginShift.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.OriginShift.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.OriginShift.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.OriginShift.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.OriginShift.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriginShift.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.OriginShift.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.ReferenceFrame valid ?
        if self.ParCmd.ReferenceFrame < 0 or self.ParCmd.ReferenceFrame > 254:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReferenceFrame = {1}', Para1=USINT_TO_STRING(self.ParCmd.ReferenceFrame))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.CalculateFrame
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.DataIndex = self._dataIndex
        self._command.DataComplete = set_bit(self._command.DataComplete, 0, self._dataComplete)
        self._command.Reserve = 0
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.ReferenceFrame = self._parCmd.ReferenceFrame
        self._command.Mode = self._parCmd.Mode

        match self._parCmd.Mode:

            case FrameCalculationMode.THREE_POINT_METHOD:
                match self._dataIndex:

                    case 1:
                        copy_into(self._command.Position, self._parCmd.Origin)
                    case 2:
                        copy_into(self._command.Position, self._parCmd.Position_X)
                    case 3:
                        copy_into(self._command.Position, self._parCmd.Position_XY)

            case FrameCalculationMode.FOUR_POINT_METHOD:
                match self._dataIndex:

                    case 1:
                        copy_into(self._command.Position, self._parCmd.Origin)
                    case 2:
                        copy_into(self._command.Position, self._parCmd.Position_X)
                    case 3:
                        copy_into(self._command.Position, self._parCmd.Position_XY)
                    case 4:
                        copy_into(self._command.Position, self._parCmd.OriginShift)

            case FrameCalculationMode.ONE_POINT_METHOD:
                copy_into(self._command.Position, self._parCmd.Origin)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DataIndex
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
            # add command.Reserve
            CreateCommandPayload.AddByte(Value=self._command.Reserve)
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
            # add command.ReferenceFrame
            CreateCommandPayload.AddUsint(Value=self._command.ReferenceFrame)
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
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=BYTE_TO_STRING(self._command.Reserve))

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
        # Create log entry for ReferenceFrame
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ReferenceFrame = {1}', Para1=USINT_TO_STRING(self._command.ReferenceFrame))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Mode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mode = {1}', Para1=FRAME_CALCULATION_MODE_TO_STRING(Value=FrameCalculationMode(self._command.Mode)))

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

        self.MyType = 'MC_CalculateFrameFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(CalculateFrameOutCmd)), Value=0, DataLen=31)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.IEC_Date = self._response.IEC_Date
            self.OutCmd.IEC_TIME = self._response.IEC_TIME
            self.OutCmd.ReferenceFrame = self._response.ReferenceFrame
            copy_into(self.OutCmd.Position, self._response.Position)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(CalculateFrameOutCmd)), Value=0, DataLen=31)
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
                    case FrameCalculationMode.ONE_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 1
                    case FrameCalculationMode.THREE_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 3
                    case FrameCalculationMode.FOUR_POINT_METHOD:
                        self._dataComplete = self._dataIndex >= 4

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

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.IEC_Date
            self._response.IEC_Date = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.IEC_TIME
            self._response.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.ReferenceFrame
            self._response.ReferenceFrame = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Reserve
            self._response.Reserve = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Position.X
            self._response.Position.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Position.Y
            self._response.Position.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Position.Z
            self._response.Position.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Position.Rx
            self._response.Position.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Position.Ry
            self._response.Position.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get response.Position.Rz
            self._response.Position.Rz = ResponseData.GetReal()
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
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.IEC_Date = {1}', Para1=IEC_DATE_TO_STRING(Value=self._response.IEC_Date))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for IEC_TIME
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._response.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ReferenceFrame
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.ReferenceFrame = {1}', Para1=USINT_TO_STRING(self._response.ReferenceFrame))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Reserve = {1}', Para1=BYTE_TO_STRING(self._response.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.X
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Position.X = {1}', Para1=REAL_TO_STRING(self._response.Position.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Y
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Position.Y = {1}', Para1=REAL_TO_STRING(self._response.Position.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Z
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Position.Z = {1}', Para1=REAL_TO_STRING(self._response.Position.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Rx
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Position.Rx = {1}', Para1=REAL_TO_STRING(self._response.Position.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Ry
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Position.Ry = {1}', Para1=REAL_TO_STRING(self._response.Position.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Position.Rz
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Position.Rz = {1}', Para1=REAL_TO_STRING(self._response.Position.Rz))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        return Reset
