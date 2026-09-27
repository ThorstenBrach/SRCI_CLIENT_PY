# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_MoveSuperImposedFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Activate superimposed motion of TCP to defined motion
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

"""Activate superimposed motion of TCP to defined motion

ST-Source: POUs/SuperImposing/MC_MoveSuperImposed/MC_MoveSuperImposedFB.st
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
from srci.functions.Convert.Misc import CombineHalfSints, PERCENT_UINT_TO_REAL, REAL_TO_PERCENT_UINT
from srci.functions.Convert.TO_STRING.ARM_CONFIG_ELBOW_TO_STRING import ARM_CONFIG_ELBOW_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_SHOULDER_TO_STRING import ARM_CONFIG_SHOULDER_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_TO_STRING import ARM_CONFIG_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_WRIST_TO_STRING import ARM_CONFIG_WRIST_TO_STRING
from srci.functions.Convert.TO_STRING.PROCESSING_MODE_TO_STRING import PROCESSING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.REFERENCE_TYPE_TO_STRING import REFERENCE_TYPE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BYTE_TO_STRING, DINT_TO_STRING, INT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, copy_into, copy_value, trunc_str, wrap
from srci.types import ArmConfigElbow, ArmConfigShoulder, ArmConfigWrist, CmdMessageState, CmdType, ExecutionMode, MessageType, MoveSuperImposedOutCmd, MoveSuperImposedParCmd, MoveSuperImposedRecvData, MoveSuperImposedSendData, PriorityLevel, ProcessingMode, ProcessingModeEnum, ReferenceType, RobotLibraryConstants, RobotLibraryErrorIdEnum, Severity, SystemTime

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_MoveSuperImposedFB']


class MC_MoveSuperImposedFB(RobotLibraryBaseExecuteFB):
    """Activate superimposed motion of TCP to defined motion"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Processing Mode
        self.ProcessingMode: ProcessingMode = ProcessingMode.BUFFERED
        # command parameter
        self.ParCmd: MoveSuperImposedParCmd = MoveSuperImposedParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The command takes control of the motion of the according axis group
        self.Active: bool = False
        # Receiving of input parameter values has been acknowledged by RC
        self.ParameterAccepted: bool = False
        # command outputs
        self.OutCmd: MoveSuperImposedOutCmd = MoveSuperImposedOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: MoveSuperImposedParCmd = MoveSuperImposedParCmd()
        # command data to send
        self._command: MoveSuperImposedSendData = MoveSuperImposedSendData()
        # response data received
        self._response: MoveSuperImposedRecvData = MoveSuperImposedRecvData()

    def __call__(self, *, ProcessingMode: ProcessingMode | None = None, ParCmd: MoveSuperImposedParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 84)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 84)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 84 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 84, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(MoveSuperImposedSendData)), DataLen=84)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 84 - PayloadPtr, 84)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 84, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 84, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK

        # ST-FIX F28: payload order differs from the structure layout -> always add the parameter
        CheckAddParameter = True
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.MoveSuperImposed

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 85 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(MoveSuperImposedParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(MoveSuperImposedParCmd)), DataLen=85) != RobotLibraryConstants.OK

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
        # internal index for loops
        _idx: int = 0

        CheckParameterValid = True

        # Check ParCmd.ProcessingMode defined ?
        # ST-FIX F26
        if self.ProcessingMode < ProcessingMode.BUFFERED or self.ProcessingMode > ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check ProcessingMode valid ?
        if (((self.ProcessingMode != ProcessingMode.PARALLEL and self.ProcessingMode != ProcessingMode.CONTINUOUS) and self.ProcessingMode != ProcessingMode.DEACTIVATE) and self.ProcessingMode != ProcessingMode.TRIGGER_ONCE) and self.ProcessingMode != ProcessingMode.TRIGGER_MULTIPLE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid

        # Check ParCmd.Offset.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.X))
            return CheckParameterValid

        # Check ParCmd.Offset.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.Y))
            return CheckParameterValid

        # Check ParCmd.Offset.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.Z))
            return CheckParameterValid

        # Check ParCmd.Offset.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.Rx))
            return CheckParameterValid

        # Check ParCmd.Offset.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.Ry))
            return CheckParameterValid

        # Check ParCmd.Offset.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.Rz))
            return CheckParameterValid

        # Check ParCmd.Offset.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.E1))
            return CheckParameterValid

        # Check ParCmd.Offset.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.E2))
            return CheckParameterValid

        # Check ParCmd.Offset.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.E3))
            return CheckParameterValid

        # Check ParCmd.Offset.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.E4))
            return CheckParameterValid

        # Check ParCmd.Offset.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.E5))
            return CheckParameterValid

        # Check ParCmd.Offset.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Offset.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Offset.E6))
            return CheckParameterValid

        # Check ParCmd.Offset.Config.Shoulder valid ?
        if (((self.ParCmd.Offset.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.Offset.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.Offset.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.Offset.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.Offset.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.Offset.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.Offset.Config.Elbow valid ?
        if (((self.ParCmd.Offset.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.Offset.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.Offset.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.Offset.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.Offset.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.Offset.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.Offset.Config.Wrist valid ?
        if (((self.ParCmd.Offset.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.Offset.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.Offset.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.Offset.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.Offset.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Offset.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.Offset.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.ReferenceType valid ?
        if self.ParCmd.ReferenceType != ReferenceType.TOOL and self.ParCmd.ReferenceType != ReferenceType.FRAME:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ReferenceType = {1}', Para1=REFERENCE_TYPE_TO_STRING(Value=self.ParCmd.ReferenceType))
            return CheckParameterValid

        # Check ParCmd.VelocityDiffRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.VelocityDiffRate) == False or (self.ParCmd.VelocityDiffRate < 0 and self.ParCmd.VelocityDiffRate != -1)) or self.ParCmd.VelocityDiffRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.VelocityDiffRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.VelocityDiffRate))
            return CheckParameterValid

        # Check ParCmd.AccelerationDiffRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.AccelerationDiffRate) == False or (self.ParCmd.AccelerationDiffRate < 0 and self.ParCmd.AccelerationDiffRate != -1)) or self.ParCmd.AccelerationDiffRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_ACCELERATION_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AccelerationDiffRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AccelerationDiffRate))
            return CheckParameterValid

        # Check ParCmd.DecelerationDiffRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.DecelerationDiffRate) == False or (self.ParCmd.DecelerationDiffRate < 0 and self.ParCmd.DecelerationDiffRate != -1)) or self.ParCmd.DecelerationDiffRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_DECELERATION_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.DecelerationDiffRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.DecelerationDiffRate))
            return CheckParameterValid

        # Check ParCmd.JerkDiffRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.JerkDiffRate) == False or (self.ParCmd.JerkDiffRate < 0 and self.ParCmd.JerkDiffRate != -1)) or self.ParCmd.JerkDiffRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_JERK_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.JerkDiffRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.JerkDiffRate))
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

        # Check ParCmd.ListenerID valid ?
        if self.ParCmd.ListenerID < 0 or self.ParCmd.ListenerID > 127:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            # ST-FIX F69
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_LISTENERID_MUST_BE_POSITIVE, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ListenerID = {1}', Para1=SINT_TO_STRING(self.ParCmd.ListenerID))
            return CheckParameterValid

        # ST-FIX F69: trigger IDs and SequenceFlag (table 7-1, 5.5.12.4, e.g. table 6-496)
        if CheckParameterValid and (((self.ParCmd.EmitterID[0] < -127 or self.ParCmd.EmitterID[1] < -127) or self.ParCmd.EmitterID[2] < -127) or self.ParCmd.EmitterID[3] < -127):
            CheckParameterValid = False
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_EMITTERID_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessage(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EmitterID (< -127)')
            return CheckParameterValid
        if (CheckParameterValid and self.ProcessingMode >= ProcessingMode.TRIGGER_BUFFERED) and self.ParCmd.ListenerID == 0:
            CheckParameterValid = False
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ListenerID = 0 with ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid
        if ((CheckParameterValid and self.ProcessingMode != ProcessingMode.DEACTIVATE) and (not self.ProcessingMode >= ProcessingMode.TRIGGER_BUFFERED)) and self.ParCmd.ListenerID > 0:
            CheckParameterValid = False
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_LISTENERID_NOT_ALLOWED, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ListenerID <> 0 with ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
            return CheckParameterValid
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.MoveSuperImposed
        # ST-FIX F51: ExecutionMode from ProcessingMode (and SequenceFlag), spec table 5-77
        match self.ProcessingMode:
            case ProcessingMode.BUFFERED | ProcessingMode.TRIGGER_BUFFERED:
                self._command.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
            case ProcessingMode.ABORTING | ProcessingMode.TRIGGER_ABORTING:
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
                # Create log entry
                self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ProcessingMode = {1}', Para1=PROCESSING_MODE_TO_STRING(Value=self.ProcessingMode))
                self.OnUpdateStateFlags(State=CmdMessageState.ERROR)
        self._command.ParSeq = self._command.ParSeq
        self._command.Priority = self.Priority
        copy_into(self._command.EmitterID, self._parCmd.EmitterID)
        self._command.ListenerID = self._parCmd.ListenerID
        self._command.Reserve = 0
        self._command.VelocityDiffRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.VelocityDiffRate, IsOptional=False)
        self._command.AccelerationDiffRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.AccelerationDiffRate, IsOptional=False)
        self._command.DecelerationDiffRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.DecelerationDiffRate, IsOptional=True)
        self._command.JerkDiffRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.JerkDiffRate, IsOptional=True)
        self._command.ToolNo = self._parCmd.ToolNo
        self._command.FrameNo = self._parCmd.FrameNo
        copy_into(self._command.Offset, self._parCmd.Offset)
        self._command.ReferenceType = self._parCmd.ReferenceType
        self._command.Reserve2 = 0

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
            # add command.VelocityDiffRate
            CreateCommandPayload.AddUint(Value=self._command.VelocityDiffRate)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AccelerationDiffRate
            CreateCommandPayload.AddUint(Value=self._command.AccelerationDiffRate)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DecelerationDiffRate
            CreateCommandPayload.AddUint(Value=self._command.DecelerationDiffRate)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.JerkDiffRate
            CreateCommandPayload.AddUint(Value=self._command.JerkDiffRate)
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
            # add command.Offset.X
            CreateCommandPayload.AddReal(Value=self._command.Offset.X)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.Y
            CreateCommandPayload.AddReal(Value=self._command.Offset.Y)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.Z
            CreateCommandPayload.AddReal(Value=self._command.Offset.Z)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.Rx
            CreateCommandPayload.AddReal(Value=self._command.Offset.Rx)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.Ry
            CreateCommandPayload.AddReal(Value=self._command.Offset.Ry)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.Rz
            CreateCommandPayload.AddReal(Value=self._command.Offset.Rz)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.Config
            CreateCommandPayload.AddArmConfig(Value=self._command.Offset.Config)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.TurnNumber
            CreateCommandPayload.AddTurnNumber(Value=self._command.Offset.TurnNumber)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.E1
            CreateCommandPayload.AddReal(Value=self._command.Offset.E1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.ReferenceType
            CreateCommandPayload.AddUsint(Value=self._command.ReferenceType)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Reserve2
            CreateCommandPayload.AddByte(Value=self._command.Reserve2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.E2
            CreateCommandPayload.AddReal(Value=self._command.Offset.E2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.E3
            CreateCommandPayload.AddReal(Value=self._command.Offset.E3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.E4
            CreateCommandPayload.AddReal(Value=self._command.Offset.E4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.E5
            CreateCommandPayload.AddReal(Value=self._command.Offset.E5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Offset.E6
            CreateCommandPayload.AddReal(Value=self._command.Offset.E6)
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
            # Create log entry for Command,EmitterID
            self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EmitterID[{2}] = {1}', Para1=SINT_TO_STRING(self._command.EmitterID[_idx]), Para2=DINT_TO_STRING(_idx))

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
        # Create log entry for VelocityDiffRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.VelocityDiffRate = {1}', Para1=UINT_TO_STRING(self._command.VelocityDiffRate))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AccelerationDiffRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AccelerationDiffRate = {1}', Para1=UINT_TO_STRING(self._command.AccelerationDiffRate))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DecelerationDiffRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DecelerationDiffRate = {1}', Para1=UINT_TO_STRING(self._command.DecelerationDiffRate))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for JerkDiffRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.JerkDiffRate = {1}', Para1=UINT_TO_STRING(self._command.JerkDiffRate))

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
        # Create log entry for Offset.X
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.X = {1}', Para1=REAL_TO_STRING(self._command.Offset.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.Y
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.Y = {1}', Para1=REAL_TO_STRING(self._command.Offset.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.Z
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.Z = {1}', Para1=REAL_TO_STRING(self._command.Offset.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.Rx
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.Rx = {1}', Para1=REAL_TO_STRING(self._command.Offset.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.Ry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.Ry = {1}', Para1=REAL_TO_STRING(self._command.Offset.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.Rz
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.Rz = {1}', Para1=REAL_TO_STRING(self._command.Offset.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.Config
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._command.Offset.Config))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.TurnNumber[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.TurnNumber[0] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.Offset.TurnNumber.J2Turns, HalfSintLo=self._command.Offset.TurnNumber.J1Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.TurnNumber[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.TurnNumber[1] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.Offset.TurnNumber.J4Turns, HalfSintLo=self._command.Offset.TurnNumber.J3Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.TurnNumber[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.TurnNumber[2] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.Offset.TurnNumber.J6Turns, HalfSintLo=self._command.Offset.TurnNumber.J5Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.TurnNumber[3]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Position.TurnNumber[3] = {1}', Para1=SINT_TO_STRING(self._command.Offset.TurnNumber.E1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.E1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.E1 = {1}', Para1=REAL_TO_STRING(self._command.Offset.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ReferenceType
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ReferenceType = {1}', Para1=REFERENCE_TYPE_TO_STRING(Value=ReferenceType(self._command.ReferenceType)))

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
        # Create log entry for Offset.E2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.E2 = {1}', Para1=REAL_TO_STRING(self._command.Offset.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.E3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.E3 = {1}', Para1=REAL_TO_STRING(self._command.Offset.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.E4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.E4 = {1}', Para1=REAL_TO_STRING(self._command.Offset.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.E5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.E5 = {1}', Para1=REAL_TO_STRING(self._command.Offset.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Offset.E6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Offset.E6 = {1}', Para1=REAL_TO_STRING(self._command.Offset.E6))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_MoveSuperImposedFB'

        self.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
        self.Priority = PriorityLevel.NORMAL
        self.ProcessingMode = ProcessingMode.PARALLEL
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(MoveSuperImposedOutCmd)), Value=0, DataLen=13)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.InvocationCounter = self._response.InvocationCounter
            self.OutCmd.OriginID = self._response.OriginID
            self.OutCmd.Progress = PERCENT_UINT_TO_REAL(Value=self._response.Progress, IsOptional=True)
            self.OutCmd.RemainingDistance = self._response.RemainingDistance

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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(MoveSuperImposedOutCmd)), Value=0, DataLen=13)
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
                self.ParameterAccepted = True
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                self.CommandBuffered = True
                self.ParameterAccepted = True
            # Currently active and in progress
            case CmdMessageState.ACTIVE:
                self.Active = True
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                pass
            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass
            # Successfully completed
            case CmdMessageState.DONE:
                self.Done = True  # ST-FIX F64
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
            # Get Response.Progress
            self._response.Progress = ResponseData.GetUint()
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check payload remaining ?
        if ResponseData.IsPayloadRemaining:
            # Get Response.RemainingDistance
            self._response.RemainingDistance = ResponseData.GetReal()
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
        # Create log entry for Progress
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.Progress = {1}', Para1=UINT_TO_STRING(self._response.Progress))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for RemainingDistance
        self.CreateLogMessagePara1(Timestamp=Timestamp, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Response.RemainingDistance = {1}', Para1=REAL_TO_STRING(self._response.RemainingDistance))

    def Reset(self) -> int:  # PROTECTED
        Reset: int = 0

        Reset = super().Reset()

        self.Done = False
        self.Busy = False
        self.Active = False
        self.CommandBuffered = False
        self.ParameterAccepted = False
        return Reset
