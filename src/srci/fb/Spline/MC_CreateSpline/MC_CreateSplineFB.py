"""Create spline on RC from positions stored in PLC

ST-Source: POUs/Spline/MC_CreateSpline/MC_CreateSplineFB.st
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
from srci.functions.Convert.Misc import CombineHalfSints, REAL_TO_PERCENT_UINT
from srci.functions.Convert.TO_STRING.ARM_CONFIG_ELBOW_TO_STRING import ARM_CONFIG_ELBOW_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_SHOULDER_TO_STRING import ARM_CONFIG_SHOULDER_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_TO_STRING import ARM_CONFIG_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_WRIST_TO_STRING import ARM_CONFIG_WRIST_TO_STRING
from srci.functions.Convert.TO_STRING.SPLINE_MODE_TO_STRING import SPLINE_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BYTE_TO_STRING, DINT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, TIME_TO_STRING, TIME_TO_UINT, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, st_for_end, trunc_str, type_size, wrap
from srci.types import ArmConfigElbow, ArmConfigShoulder, ArmConfigWrist, CmdMessageState, CmdType, CreateSplineOutCmd, CreateSplineParCmd, CreateSplineRecvData, CreateSplineSendData, ExecutionMode, MessageType, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, RobotLibraryParameter, Severity, SplineMode, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_CreateSplineFB']


class MC_CreateSplineFB(RobotLibraryBaseExecuteFB):
    """Create spline on RC from positions stored in PLC"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # command parameter
        self.ParCmd: CreateSplineParCmd = CreateSplineParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # command results
        self.OutCmd: CreateSplineOutCmd = CreateSplineOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: CreateSplineParCmd = CreateSplineParCmd()
        # command data to send
        self._command: CreateSplineSendData = CreateSplineSendData()
        # response data received
        self._response: CreateSplineRecvData = CreateSplineRecvData()

    def __call__(self, *, ParCmd: CreateSplineParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * _iec.array_len(1, type_size(_iec.StructType(CreateSplineSendData))))
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * _iec.array_len(1, type_size(_iec.StructType(CreateSplineSendData))))
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, type_size(_iec.ArrayType(1, type_size(_iec.StructType(CreateSplineSendData)), _iec.BYTE)) - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, type_size(_iec.StructType(CreateSplineSendData)), _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(CreateSplineSendData)), DataLen=type_size(_iec.StructType(CreateSplineSendData)))
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, type_size(_iec.ArrayType(1, type_size(_iec.StructType(CreateSplineSendData)), _iec.BYTE)) - PayloadPtr, type_size(_iec.ArrayType(1, type_size(_iec.StructType(CreateSplineSendData)), _iec.BYTE)))
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, type_size(_iec.StructType(CreateSplineSendData)), _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, type_size(_iec.StructType(CreateSplineSendData)), _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.CreateSpline

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if type_size(_iec.StructType(CreateSplineParCmd)) == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(CreateSplineParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(CreateSplineParCmd)), DataLen=type_size(_iec.StructType(CreateSplineParCmd))) != RobotLibraryConstants.OK

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
        if (((self.ParCmd.Mode != SplineMode.DISCRETE_POINTS and self.ParCmd.Mode != SplineMode.BEZIER_SPLINE) and self.ParCmd.Mode != SplineMode.B_SPLINES) and self.ParCmd.Mode != SplineMode.CUBIC_HERMITE_SPLINE) and self.ParCmd.Mode != SplineMode.C_SPLINES:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Mode = {1}', Para1=SPLINE_MODE_TO_STRING(Value=self.ParCmd.Mode))
            return CheckParameterValid

        for _idx in range(0, RobotLibraryParameter.SPLINE_DATA_MAX + 1):
            # Check ParCmd.SplineData[x].Position.X valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.X) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.[{2}].Position.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.X), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Y valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.Y) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Y), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Z valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.Z) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Z))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Rx valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.Rx) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Rx), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Ry valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.Ry) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Ry), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Rz valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.Rz) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Rz), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.E1 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.E1) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.E1), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.E2 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.E2) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.E2), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[_idx].Position.E3 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.E3) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.E3), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.E4 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.E4) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.E4), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.E5 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.E5) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.E5), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.E6 valid ?
            if SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].Position.E6) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.E6), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Config.Shoulder valid ?
            if (((self.ParCmd.SplineData[_idx].Position.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.SplineData[_idx].Position.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.SplineData[_idx].Position.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.SplineData[_idx].Position.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.SplineData[_idx].Position.Config.Shoulder != ArmConfigShoulder.FRONT:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Config.Shoulder), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Config.Elbow valid ?
            if (((self.ParCmd.SplineData[_idx].Position.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.SplineData[_idx].Position.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.SplineData[_idx].Position.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.SplineData[_idx].Position.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.SplineData[_idx].Position.Config.Elbow != ArmConfigElbow.UP:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Config.Elbow), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].Position.Config.Wrist valid ?
            if (((self.ParCmd.SplineData[_idx].Position.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.SplineData[_idx].Position.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.SplineData[_idx].Position.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.SplineData[_idx].Position.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.SplineData[_idx].Position.Config.Wrist != ArmConfigWrist.NON_FLIP:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].Position.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.SplineData[_idx].Position.Config.Wrist), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].VelocityRate valid ?
            if (SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].VelocityRate) == False or (self.ParCmd.SplineData[_idx].VelocityRate < 0 and self.ParCmd.SplineData[_idx].VelocityRate != -1)) or self.ParCmd.SplineData[_idx].VelocityRate > 100:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].VelocityRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].VelocityRate), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].AccelerationRate valid ?
            if (SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].AccelerationRate) == False or (self.ParCmd.SplineData[_idx].AccelerationRate < 0 and self.ParCmd.SplineData[_idx].AccelerationRate != -1)) or self.ParCmd.SplineData[_idx].AccelerationRate > 100:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_ACCELERATION_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].AccelerationRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].AccelerationRate), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].DecelerationRate valid ?
            if (SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].DecelerationRate) == False or (self.ParCmd.SplineData[_idx].DecelerationRate < 0 and self.ParCmd.SplineData[_idx].DecelerationRate != -1)) or self.ParCmd.SplineData[_idx].DecelerationRate > 100:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_DECELERATION_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].DecelerationRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].DecelerationRate), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].JerkRate valid ?
            if (SysDepIsValidReal(Value=self.ParCmd.SplineData[_idx].JerkRate) == False or (self.ParCmd.SplineData[_idx].JerkRate < 0 and self.ParCmd.SplineData[_idx].JerkRate != -1)) or self.ParCmd.SplineData[_idx].JerkRate > 100:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_JERK_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].JerkRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.SplineData[_idx].JerkRate), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].ToolNo valid ?
            if self.ParCmd.SplineData[_idx].ToolNo < 0 or self.ParCmd.SplineData[_idx].ToolNo > 254:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].ToolNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.SplineData[_idx].ToolNo), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].FrameNo valid ?
            if self.ParCmd.SplineData[_idx].FrameNo < 0 or self.ParCmd.SplineData[_idx].FrameNo > 254:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].FrameNo = {1}', Para1=USINT_TO_STRING(self.ParCmd.SplineData[_idx].FrameNo), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid

            # Check ParCmd.SplineData[x].MoveTime valid ?
            if self.ParCmd.SplineData[_idx].MoveTime < 0:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.SplineData[{2}].MoveTime = {1}', Para1=TIME_TO_STRING(self.ParCmd.SplineData[_idx].MoveTime), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # Parameter count
        _parameterCnt: int = 0
        # internal index for loops
        _idx: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.CreateSpline
        self._command.ExecMode = self.ExecMode
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        self._command.Mode = self._parCmd.Mode
        self._command.SplineID = self._parCmd.SplineID

        for _idx in range(1, RobotLibraryParameter.SPLINE_DATA_MAX + 1):
            self._command.SplineData[_idx].VelocityRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.SplineData[_idx].VelocityRate, IsOptional=False)
            self._command.SplineData[_idx].AccelerationRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.SplineData[_idx].AccelerationRate, IsOptional=False)
            self._command.SplineData[_idx].DecelerationRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.SplineData[_idx].DecelerationRate, IsOptional=True)
            self._command.SplineData[_idx].JerkRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.SplineData[_idx].JerkRate, IsOptional=True)
            self._command.SplineData[_idx].ToolNo = self._parCmd.SplineData[_idx].ToolNo
            self._command.SplineData[_idx].FrameNo = self._parCmd.SplineData[_idx].FrameNo
            self._command.SplineData[_idx].MoveTime = TIME_TO_UINT(self._parCmd.SplineData[_idx].MoveTime)
        else:
            _idx = st_for_end(1, RobotLibraryParameter.SPLINE_DATA_MAX)

        # copy command data to header
        copy_into(self._cmdHeader, self._command)
        # call base implementation to copy header to payload buffer
        CreateCommandPayload = super().CreateCommandPayload(AxesGroup=AxesGroup)

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Mode
            CreateCommandPayload.AddUint(Value=self._command.Mode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.SplineID
            CreateCommandPayload.AddSint(Value=self._command.SplineID)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        for _idx in range(1, RobotLibraryParameter.SPLINE_DATA_MAX + 1):
            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.VelocityRate
                CreateCommandPayload.AddUint(Value=self._command.SplineData[_idx].VelocityRate)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.AccelerationRate
                CreateCommandPayload.AddUint(Value=self._command.SplineData[_idx].AccelerationRate)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.DecelerationRate
                CreateCommandPayload.AddUint(Value=self._command.SplineData[_idx].DecelerationRate)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.JerkRate
                CreateCommandPayload.AddUint(Value=self._command.SplineData[_idx].JerkRate)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.ToolNo
                CreateCommandPayload.AddUsint(Value=self._command.SplineData[_idx].ToolNo)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.FrameNo
                CreateCommandPayload.AddUsint(Value=self._command.SplineData[_idx].FrameNo)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.X
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.X)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.Y
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.Y)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.Z
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.Z)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.Rx
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.Rx)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.Ry
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.Ry)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.Rz
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.Rz)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.Config
                CreateCommandPayload.AddArmConfig(Value=self._command.SplineData[_idx].Position.Config)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.TurnNumber
                CreateCommandPayload.AddTurnNumber(Value=self._command.SplineData[_idx].Position.TurnNumber)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.E1
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.E1)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].MoveTime
                CreateCommandPayload.AddUint(Value=self._command.SplineData[_idx].MoveTime)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.E2
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.E2)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.E3
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.E3)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.E4
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.E4)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.E5
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.E5)
                # inc parameter counter
                _parameterCnt = _parameterCnt + 1

            # Check parameter must be added ?
            if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
                # add command.SplineData[_idx].Position.E6
                CreateCommandPayload.AddReal(Value=self._command.SplineData[_idx].Position.E6)
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

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Mode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Mode = {1}', Para1=SPLINE_MODE_TO_STRING(Value=SplineMode(self._command.Mode)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for SplineID
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineID = {1}', Para1=SINT_TO_STRING(self._command.SplineID))

        # Create log entry for SplineData[x]
        for _idx in range(1, RobotLibraryParameter.SPLINE_DATA_MAX + 1):
            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for VelocityRate
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].VelocityRate = {1}', Para1=UINT_TO_STRING(self._command.SplineData[_idx].VelocityRate), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for AccelerationRate
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].AccelerationRate = {1}', Para1=UINT_TO_STRING(self._command.SplineData[_idx].AccelerationRate), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for DecelerationRate
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].DecelerationRate = {1}', Para1=UINT_TO_STRING(self._command.SplineData[_idx].DecelerationRate), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for JerkRate
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].JerkRate = {1}', Para1=UINT_TO_STRING(self._command.SplineData[_idx].JerkRate), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for ToolNo
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].ToolNo = {1}', Para1=USINT_TO_STRING(self._command.SplineData[_idx].ToolNo), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for FrameNo
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].FrameNo = {1}', Para1=USINT_TO_STRING(self._command.SplineData[_idx].FrameNo), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.X
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.X = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.X), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.Y
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.Y = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.Y), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.Z
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.Z = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.Z), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.Rx
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.Rx = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.Rx), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.Ry
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.Ry = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.Ry), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.Rz
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.Rz = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.Rz), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.Config
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._command.SplineData[_idx].Position.Config), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.TurnNumber[0]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.TurnNumber[0] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.SplineData[_idx].Position.TurnNumber.J2Turns, HalfSintLo=self._command.SplineData[_idx].Position.TurnNumber.J1Turns)), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.TurnNumber[1]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.TurnNumber[1] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.SplineData[_idx].Position.TurnNumber.J4Turns, HalfSintLo=self._command.SplineData[_idx].Position.TurnNumber.J3Turns)), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.TurnNumber[2]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.TurnNumber[2] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.SplineData[_idx].Position.TurnNumber.J6Turns, HalfSintLo=self._command.SplineData[_idx].Position.TurnNumber.J5Turns)), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.TurnNumber[3]
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.TurnNumber[3] = {1}', Para1=SINT_TO_STRING(self._command.SplineData[_idx].Position.TurnNumber.E1Turns), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.E1
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.E1 = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.E1), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for MoveTime
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].MoveTime = {1}', Para1=UINT_TO_STRING(self._command.SplineData[_idx].MoveTime), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.E2
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.E2 = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.E2), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.E3
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.E3 = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.E3), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.E4
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.E4 = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.E4), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.E5
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.E5 = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.E5), Para2=DINT_TO_STRING(_idx))

            # Return if no parameter is remaining...
            if ParameterCnt == 0:
                return
            # dec remaining parameter(s)
            ParameterCnt = ParameterCnt - 1
            # Create log entry for Position.E6
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.SplineData[{2}].Position.E6 = {1}', Para1=REAL_TO_STRING(self._command.SplineData[_idx].Position.E6), Para2=DINT_TO_STRING(_idx))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_CreateSplineFB'

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(CreateSplineOutCmd)), Value=0, DataLen=0)
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
