"""Transform a defined position in space

ST-Source: POUs/Additional/MC_ShiftPosition/MC_ShiftPositionFB.st
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
from srci.functions.Convert.TO_STRING.REFERENCE_ELEMENT_TO_STRING import REFERENCE_ELEMENT_TO_STRING
from srci.functions.Convert.TO_STRING.TRANSFORM_MODE_TO_STRING import TRANSFORM_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BYTE_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import ArmConfigElbow, ArmConfigShoulder, ArmConfigWrist, CmdMessageState, CmdType, ExecutionMode, MessageType, PriorityLevel, ReferenceElement, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, ShiftPositionOutCmd, ShiftPositionParCmd, ShiftPositionRecvData, ShiftPositionSendData, SystemTime, TransformMode

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_ShiftPositionFB']


class MC_ShiftPositionFB(RobotLibraryBaseExecuteFB):
    """Transform a defined position in space"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Command parameter
        self.ParCmd: ShiftPositionParCmd = ShiftPositionParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command results
        self.OutCmd: ShiftPositionOutCmd = ShiftPositionOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: ShiftPositionParCmd = ShiftPositionParCmd()
        # command data to send
        self._command: ShiftPositionSendData = ShiftPositionSendData()
        # response data received
        self._response: ShiftPositionRecvData = ShiftPositionRecvData()

    def __call__(self, *, ParCmd: ShiftPositionParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 105)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 105)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 105 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 105, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(ShiftPositionSendData)), DataLen=105)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 105 - PayloadPtr, 105)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 105, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 105, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ShiftPosition

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 100 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(ShiftPositionParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(ShiftPositionParCmd)), DataLen=100) != RobotLibraryConstants.OK

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

        CheckParameterValid = True

        # Check ParCmd.Mode valid ?
        if (((self.ParCmd.Mode != TransformMode.MIRROR_AT_POINT and self.ParCmd.Mode != TransformMode.MIRROR_AT_STRAIGHT_LINE) and self.ParCmd.Mode != TransformMode.MIRROR_AT_PLANE) and self.ParCmd.Mode != TransformMode.ROTATE_AROUND_STRAIGHT_LINE) and self.ParCmd.Mode != TransformMode.SHIFT_BY_VECTOR:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mode = {1}', Para1=TRANSFORM_MODE_TO_STRING(Value=self.ParCmd.Mode))
            return CheckParameterValid

        # Check ParCmd.Position.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.X))
            return CheckParameterValid

        # Check ParCmd.Position.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.Y))
            return CheckParameterValid

        # Check ParCmd.Position.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.Z))
            return CheckParameterValid

        # Check ParCmd.Position.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.Rx))
            return CheckParameterValid

        # Check ParCmd.Position.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.Ry))
            return CheckParameterValid

        # Check ParCmd.Position.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.Rz))
            return CheckParameterValid

        # Check ParCmd.Position.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.E1))
            return CheckParameterValid

        # Check ParCmd.Position.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.E2))
            return CheckParameterValid

        # Check ParCmd.Position.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.E3))
            return CheckParameterValid

        # Check ParCmd.Position.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.E4))
            return CheckParameterValid

        # Check ParCmd.Position.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.E5))
            return CheckParameterValid

        # Check ParCmd.Position.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Position.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Position.E6))
            return CheckParameterValid

        # Check ParCmd.Position.Config.Shoulder valid ?
        if (((self.ParCmd.Position.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.Position.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.Position.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.Position.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.Position.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.Position.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.Position.Config.Elbow valid ?
        if (((self.ParCmd.Position.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.Position.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.Position.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.Position.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.Position.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.Position.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.Position.Config.Wrist valid ?
        if (((self.ParCmd.Position.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.Position.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.Position.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.Position.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.Position.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Position.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.Position.Config.Wrist))
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

        # Check ParCmd.TargetFrameNo valid ?
        if self.ParCmd.TargetFrameNo < 0 or self.ParCmd.TargetFrameNo > 254:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TargetFrameNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.TargetFrameNo))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_1.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TransformationParameter_1.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_1.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TransformationParameter_1.X))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_1.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TransformationParameter_1.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_1.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TransformationParameter_1.Y))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_1.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TransformationParameter_1.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_1.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TransformationParameter_1.Z))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_1.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TransformationParameter_1.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_1.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TransformationParameter_1.Rx))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_1.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TransformationParameter_1.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_1.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TransformationParameter_1.Ry))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_1.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.TransformationParameter_1.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_1.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.TransformationParameter_1.Rz))
            return CheckParameterValid

        # Check ParCmd.TransformationParameter_2 valid ?
        if (((((self.ParCmd.TransformationParameter_2 != ReferenceElement.NOT_USED and self.ParCmd.TransformationParameter_2 != ReferenceElement.X_AXIS) and self.ParCmd.TransformationParameter_2 != ReferenceElement.Y_AXIS) and self.ParCmd.TransformationParameter_2 != ReferenceElement.Z_AXIS) and self.ParCmd.TransformationParameter_2 != ReferenceElement.XY_PLANE) and self.ParCmd.TransformationParameter_2 != ReferenceElement.XZ_PLANE) and self.ParCmd.TransformationParameter_2 != ReferenceElement.YZ_PLANE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TransformationParameter_2 = {1}', Para1=REFERENCE_ELEMENT_TO_STRING(Value=self.ParCmd.TransformationParameter_2))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.ShiftPosition
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        copy_into(self._command.TransformationParameter_1, self._parCmd.TransformationParameter_1)
        self._command.TransformationParameter_2 = self._parCmd.TransformationParameter_2
        self._command.RotationAngle = self._parCmd.RotationAngle
        self._command.Mode = self._parCmd.Mode
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.TargetFrameNo = self._parCmd.TargetFrameNo
        copy_into(self._command.Position, self._parCmd.Position)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Timestamp.IEC_DATE
            CreateCommandPayload.AddIecDate(Value=self._command.TransformationParameter_1.Timestamp.IEC_DATE)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Timestamp.IEC_TIME
            CreateCommandPayload.AddIecTime(Value=self._command.TransformationParameter_1.Timestamp.IEC_TIME)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.ReferenceFrame
            CreateCommandPayload.AddUsint(Value=self._command.TransformationParameter_1.ReferenceFrame)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve
            CreateCommandPayload.AddByte(Value=0)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.X
            CreateCommandPayload.AddReal(Value=self._command.TransformationParameter_1.X)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Y
            CreateCommandPayload.AddReal(Value=self._command.TransformationParameter_1.Y)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Z
            CreateCommandPayload.AddReal(Value=self._command.TransformationParameter_1.Z)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Rx
            CreateCommandPayload.AddReal(Value=self._command.TransformationParameter_1.Rx)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Ry
            CreateCommandPayload.AddReal(Value=self._command.TransformationParameter_1.Ry)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_1.Rz
            CreateCommandPayload.AddReal(Value=self._command.TransformationParameter_1.Rz)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TransformationParameter_2
            CreateCommandPayload.AddUsint(Value=self._command.TransformationParameter_2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.RotationAngle
            CreateCommandPayload.AddReal(Value=self._command.RotationAngle)
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
            # add command.FrameNo
            CreateCommandPayload.AddUsint(Value=self._command.FrameNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.TargetFrameNo
            CreateCommandPayload.AddUsint(Value=self._command.TargetFrameNo)
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
            # add command.Position.Config
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
        # Create log entry for TransformationParameter_1.Timestamp.IEC_DATE
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Timestamp.IEC_DATE = {1}', Para1=IEC_DATE_TO_STRING(Value=self._command.TransformationParameter_1.Timestamp.IEC_DATE))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.Timestamp.IEC_TIME
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Timestamp.IEC_TIME = {1}', Para1=IEC_TIME_TO_STRING(Value=self._command.TransformationParameter_1.Timestamp.IEC_TIME))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.ReferenceFrame
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.ReferenceFrame = {1}', Para1=USINT_TO_STRING(self._command.TransformationParameter_1.ReferenceFrame))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=USINT_TO_STRING(0))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.X
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.X = {1}', Para1=REAL_TO_STRING(self._command.TransformationParameter_1.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.Y
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Y = {1}', Para1=REAL_TO_STRING(self._command.TransformationParameter_1.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.Z
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Z = {1}', Para1=REAL_TO_STRING(self._command.TransformationParameter_1.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.Rx
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Rx = {1}', Para1=REAL_TO_STRING(self._command.TransformationParameter_1.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.Ry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Ry = {1}', Para1=REAL_TO_STRING(self._command.TransformationParameter_1.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_1.Rz
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_1.Rz = {1}', Para1=REAL_TO_STRING(self._command.TransformationParameter_1.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformationParameter_2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TransformationParameter_2 = {1}', Para1=USINT_TO_STRING(self._command.TransformationParameter_2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RotationAngle
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.RotationAngle = {1}', Para1=REAL_TO_STRING(self._command.RotationAngle))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Mode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mode = {1}', Para1=TRANSFORM_MODE_TO_STRING(Value=self._command.Mode))

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
        # Create log entry for TargetFrameNo
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TargetFrameNo = {1}', Para1=USINT_TO_STRING(self._command.TargetFrameNo))

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

        self.MyType = 'MC_ShiftPositionFB'

        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ShiftPositionOutCmd)), Value=0, DataLen=61)

        if State == CmdMessageState.DONE:
            # Update results
            copy_into(self.OutCmd.TransformedPosition, self._response.TransformedPosition)

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(ShiftPositionOutCmd)), Value=0, DataLen=61)
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
            # Get Response.TransformedPosition.X
            self._response.TransformedPosition.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.Y
            self._response.TransformedPosition.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.Z
            self._response.TransformedPosition.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.Rx
            self._response.TransformedPosition.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.Ry
            self._response.TransformedPosition.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.Rz
            self._response.TransformedPosition.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.Config
            copy_into(self._response.TransformedPosition.Config, ResponseData.GetArmConfig())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.TurnNumber
            copy_into(self._response.TransformedPosition.TurnNumber, ResponseData.GetTurnNumbers())
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.E1
            self._response.TransformedPosition.E1 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.E2
            self._response.TransformedPosition.E2 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.E3
            self._response.TransformedPosition.E3 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.E4
            self._response.TransformedPosition.E4 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.E5
            self._response.TransformedPosition.E5 = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.TransformedPosition.E6
            self._response.TransformedPosition.E6 = ResponseData.GetReal()
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
        # Create log entry for TransformedPosition.X
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.X = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.Y
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.Y = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.Z
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.Z = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.Rx
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.Rx = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.Ry
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.Ry = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.Rz
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.Rz = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.Config
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._response.TransformedPosition.Config))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.J1Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.J1Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.J1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.J2Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.J2Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.J2Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.J3Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.J3Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.J3Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.J4Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.J4Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.J4Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.J5Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.J5Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.J5Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.J6Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.J6Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.J6Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.TurnNumber.E1Turns
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.TurnNumber.E1Turns = {1}', Para1=SINT_TO_STRING(self._response.TransformedPosition.TurnNumber.E1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.E1
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.E1 = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.E2
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.E2 = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.E3
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.E3 = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.E4
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.E4 = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.E5
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.E5 = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TransformedPosition.E6
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.TransformedPosition.E6 = {1}', Para1=REAL_TO_STRING(self._response.TransformedPosition.E6))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.CommandBuffered = False
        return Reset
