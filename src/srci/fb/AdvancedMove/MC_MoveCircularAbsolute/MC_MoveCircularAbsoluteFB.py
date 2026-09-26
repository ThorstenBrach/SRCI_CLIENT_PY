# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MC_MoveCircularAbsoluteFB
#  Author:      Thorsten Brach
#  Date:        2024-06-01
#
#  Description:
#    Move the TCP to an absolute cartesian position (circular interpolation)
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

"""Move the TCP to an absolute cartesian position (circular interpolation)

ST-Source: POUs/AdvancedMove/MC_MoveCircularAbsolute/MC_MoveCircularAbsoluteFB.st
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
from srci.functions.Convert.Misc import ArmConfigParameterToBytes, CombineHalfSints, PERCENT_UINT_TO_REAL, REAL_TO_PERCENT_UINT
from srci.functions.Convert.TO_STRING.ABORTING_MODE_TO_STRING import ABORTING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_ELBOW_TO_STRING import ARM_CONFIG_ELBOW_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_SHOULDER_TO_STRING import ARM_CONFIG_SHOULDER_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_TO_STRING import ARM_CONFIG_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_WRIST_TO_STRING import ARM_CONFIG_WRIST_TO_STRING
from srci.functions.Convert.TO_STRING.BLENDING_MODE_TO_STRING import BLENDING_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.functions.Convert.TO_STRING.CIRC_MODE_TO_STRING import CIRC_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.CIRC_PLANE_TO_STRING import CIRC_PLANE_TO_STRING
from srci.functions.Convert.TO_STRING.ORI_MODE_TO_STRING import ORI_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.PATH_CHOICE_TO_STRING import PATH_CHOICE_TO_STRING
from srci.functions.Convert.TO_STRING.SEQUENCE_FLAG_TO_STRING import SEQUENCE_FLAG_TO_STRING
from srci.functions.Convert.TO_STRING.TURN_MODE_TO_STRING import TURN_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.VALID_REAL_TO_STRING import VALID_REAL_TO_STRING
from srci.iec.conv import BOOL_TO_BYTE, BOOL_TO_STRING, BYTE_TO_STRING, DINT_TO_STRING, INT_TO_STRING, REAL_TO_STRING, SINT_TO_STRING, TIME_TO_STRING, TIME_TO_UINT, UINT_TO_STRING, USINT_TO_STRING
from srci.iec.rt import ADR, LIMIT, SysDepIsValidReal, SysDepMemCmp, SysDepMemCpy, SysDepMemSet, bit, copy_into, copy_value, st_for_end, trunc_str, wrap
from srci.types import AbortingMode, AbortingModeEnum, ArmConfigElbow, ArmConfigShoulder, ArmConfigWrist, BlendingMode, CircMode, CircPlane, CmdMessageState, CmdType, ExecutionMode, MessageType, MoveCircularAbsoluteOutCmd, MoveCircularAbsoluteParCmd, MoveCircularAbsoluteRecvData, MoveCircularAbsoluteSendData, OriMode, PathChoice, PriorityLevel, RobotLibraryConstants, RobotLibraryErrorIdEnum, SequenceFlag, SequenceFlagEnum, Severity, SystemTime, TurnMode

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AxesGroup

__all__ = ['MC_MoveCircularAbsoluteFB']


class MC_MoveCircularAbsoluteFB(RobotLibraryBaseExecuteFB):
    """Move the TCP to an absolute cartesian position (circular interpolation)"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Parameter which determines the behavior towards the previously sent and still active or buffered commands
        self.AbortingMode: AbortingMode = AbortingMode.BUFFER
        # Defines the target sequence in which the command will be executed
        self.SequenceFlag: SequenceFlag = SequenceFlag.NO_SEQUENCE
        # command results
        self.ParCmd: MoveCircularAbsoluteParCmd = MoveCircularAbsoluteParCmd()
        # VAR_OUTPUT
        # Command is transferred and confirmed by the RC
        self.CommandBuffered: bool = False
        # The command takes control of the motion of the according axis group
        self.Active: bool = False
        # The command was aborted by another command.
        self.CommandAborted: bool = False
        # TRUE, while command is interrupted during execution and can be continued
        self.CommandInterrupted: bool = False
        # command results
        self.OutCmd: MoveCircularAbsoluteOutCmd = MoveCircularAbsoluteOutCmd()
        # VAR
        # internal copy of command parameter
        self._parCmd: MoveCircularAbsoluteParCmd = MoveCircularAbsoluteParCmd()
        # command data to send
        self._command: MoveCircularAbsoluteSendData = MoveCircularAbsoluteSendData()
        # response data received
        self._response: MoveCircularAbsoluteRecvData = MoveCircularAbsoluteRecvData()

    def __call__(self, *, AbortingMode: AbortingMode | None = None, SequenceFlag: SequenceFlag | None = None, ParCmd: MoveCircularAbsoluteParCmd | None = None, Execute: bool | None = None, Name: str | None = None, ExecMode: ExecutionMode | None = None, Priority: PriorityLevel | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
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
        Payload: _iec.IecArray[int] = _iec.IecArray(1, [0] * 171)
        # Null Byte array
        Null: _iec.IecArray[int] = _iec.IecArray(1, [0] * 171)
        # Data length to compare
        DataLen: int = 0

        # Payload pointer must be decreased by one byte, because ADR(Payload) is already one byte !
        PayloadPtr = LIMIT(0, PayloadPtr - 1, 171 - 1)
        # Convert command struct to payload array
        SysDepMemCpy(pDest=ADR(Payload, None, _iec.ArrayType(1, 171, _iec.BYTE)), pSrc=ADR(self, '_command', _iec.StructType(MoveCircularAbsoluteSendData)), DataLen=171)
        # Calculate the data length to compare - at least one byte must be compared !
        DataLen = LIMIT(1, 171 - PayloadPtr, 171)
        # Compare Payload-Array with Null-Byte-Array
        CheckAddParameter = SysDepMemCmp(pData1=ADR(Payload, None, _iec.ArrayType(1, 171, _iec.BYTE)) + PayloadPtr, pData2=ADR(Null, None, _iec.ArrayType(1, 171, _iec.BYTE)), DataLen=DataLen) != RobotLibraryConstants.OK

        # ST-FIX F28: payload order differs from the structure layout -> always add the parameter
        CheckAddParameter = True
        return CheckAddParameter

    def CheckFunctionSupported(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckFunctionSupported: bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.MoveCircularAbsolute

        if not CheckFunctionSupported:
            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup=AxesGroup)
        return CheckFunctionSupported

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if 177 == 0 or self._stepCmd == 0:
            return CheckParameterChanged

        # compare memory
        self._parameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCmd', _iec.StructType(MoveCircularAbsoluteParCmd)), pData2=ADR(self, '_parCmd', _iec.StructType(MoveCircularAbsoluteParCmd)), DataLen=177) != RobotLibraryConstants.OK

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

        # Check ParCmd.CircMode valid ?
        if ((self.ParCmd.CircMode != CircMode.BORDER and self.ParCmd.CircMode != CircMode.CENTER) and self.ParCmd.CircMode != CircMode.CENTER_WITH_ANGLE) and self.ParCmd.CircMode != CircMode.RADIUS:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.CircMode = {1}', Para1=CIRC_MODE_TO_STRING(Value=self.ParCmd.CircMode))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.X))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.Y))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.Z))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.Rx))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.Ry))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.Rz))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.E1))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.E2))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.E3))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.E4))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.E5))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.AuxPoint.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AuxPoint.E6))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Config.Shoulder valid ?
        if (((self.ParCmd.AuxPoint.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.AuxPoint.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.AuxPoint.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.AuxPoint.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.AuxPoint.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.AuxPoint.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Config.Elbow valid ?
        if (((self.ParCmd.AuxPoint.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.AuxPoint.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.AuxPoint.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.AuxPoint.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.AuxPoint.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.AuxPoint.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.AuxPoint.Config.Wrist valid ?
        if (((self.ParCmd.AuxPoint.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.AuxPoint.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.AuxPoint.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.AuxPoint.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.AuxPoint.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AuxPoint.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.AuxPoint.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.CircPlane valid ?
        if (self.ParCmd.CircPlane != CircPlane.XZ_PLANE and self.ParCmd.CircPlane != CircPlane.YZ_PLANE) and self.ParCmd.CircPlane != CircPlane.XY_PLANE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.CircPlane = {1}', Para1=CIRC_PLANE_TO_STRING(Value=self.ParCmd.CircPlane))
            return CheckParameterValid

        # Check ParCmd.Tolerance valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Tolerance) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Tolerance = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Tolerance))
            return CheckParameterValid

        # Check ParCmd.EndPoint.X valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.X) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.X = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.X))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Y valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.Y) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Y = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.Y))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Z valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.Z) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Z = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.Z))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Rx valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.Rx) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Rx = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.Rx))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Ry valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.Ry) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Ry = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.Ry))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Rz valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.Rz) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Rz = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.Rz))
            return CheckParameterValid

        # Check ParCmd.EndPoint.E1 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.E1) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.E1 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.E1))
            return CheckParameterValid

        # Check ParCmd.EndPoint.E2 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.E2) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.E2 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.E2))
            return CheckParameterValid

        # Check ParCmd.EndPoint.E3 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.E3) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.E3 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.E3))
            return CheckParameterValid

        # Check ParCmd.EndPoint.E4 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.E4) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.E4 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.E4))
            return CheckParameterValid

        # Check ParCmd.EndPoint.E5 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.E5) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.E5 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.E5))
            return CheckParameterValid

        # Check ParCmd.EndPoint.E6 valid ?
        if SysDepIsValidReal(Value=self.ParCmd.EndPoint.E6) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.E6 = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.EndPoint.E6))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Config.Shoulder valid ?
        if (((self.ParCmd.EndPoint.Config.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.EndPoint.Config.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.EndPoint.Config.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.EndPoint.Config.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.EndPoint.Config.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Config.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.EndPoint.Config.Shoulder))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Config.Elbow valid ?
        if (((self.ParCmd.EndPoint.Config.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.EndPoint.Config.Elbow != ArmConfigElbow.SAME) and self.ParCmd.EndPoint.Config.Elbow != ArmConfigElbow.FREE) and self.ParCmd.EndPoint.Config.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.EndPoint.Config.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Config.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.EndPoint.Config.Elbow))
            return CheckParameterValid

        # Check ParCmd.EndPoint.Config.Wrist valid ?
        if (((self.ParCmd.EndPoint.Config.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.EndPoint.Config.Wrist != ArmConfigWrist.SAME) and self.ParCmd.EndPoint.Config.Wrist != ArmConfigWrist.FREE) and self.ParCmd.EndPoint.Config.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.EndPoint.Config.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EndPoint.Config.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.EndPoint.Config.Wrist))
            return CheckParameterValid

        # Check ParCmd.Angle valid ?
        if SysDepIsValidReal(Value=self.ParCmd.Angle) == False:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.Angle = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.Angle))
            return CheckParameterValid

        # Check ParCmd.PathChoice valid ?
        if self.ParCmd.PathChoice != PathChoice.CLOCKWISE and self.ParCmd.PathChoice != PathChoice.COUNTERCLOCKWISE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.PathChoice = {1}', Para1=PATH_CHOICE_TO_STRING(Value=self.ParCmd.PathChoice))
            return CheckParameterValid

        # Check ParCmd.VelocityRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.VelocityRate) == False or (self.ParCmd.VelocityRate < 0 and self.ParCmd.VelocityRate != -1)) or self.ParCmd.VelocityRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.VelocityRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.VelocityRate))
            return CheckParameterValid

        # Check ParCmd.AccelerationRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.AccelerationRate) == False or (self.ParCmd.AccelerationRate < 0 and self.ParCmd.AccelerationRate != -1)) or self.ParCmd.AccelerationRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_ACCELERATION_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.AccelerationRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.AccelerationRate))
            return CheckParameterValid

        # Check ParCmd.DecelerationRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.DecelerationRate) == False or (self.ParCmd.DecelerationRate < 0 and self.ParCmd.DecelerationRate != -1)) or self.ParCmd.DecelerationRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_DECELERATION_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.DecelerationRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.DecelerationRate))
            return CheckParameterValid

        # Check ParCmd.JerkRate valid ?
        if (SysDepIsValidReal(Value=self.ParCmd.JerkRate) == False or (self.ParCmd.JerkRate < 0 and self.ParCmd.JerkRate != -1)) or self.ParCmd.JerkRate > 100:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_JERK_INVALID, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.JerkRate = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.JerkRate))
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

        # Check ParCmd.BlendingMode valid ?
        if (((((self.ParCmd.BlendingMode != BlendingMode.EXACT_STOP and self.ParCmd.BlendingMode != BlendingMode.DEFINED_VELOCITY) and self.ParCmd.BlendingMode != BlendingMode.CORNER_DISTANCE) and self.ParCmd.BlendingMode != BlendingMode.MAX_CORNER_DEVIATION) and self.ParCmd.BlendingMode != BlendingMode.CORNER_DISTANCE_2R) and self.ParCmd.BlendingMode != BlendingMode.RAMP_OVERLAP) and self.ParCmd.BlendingMode != BlendingMode.CORNER_DISTANCE_1R:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.BlendingMode = {1}', Para1=BLENDING_MODE_TO_STRING(Value=self.ParCmd.BlendingMode))
            return CheckParameterValid

        for _idx in range(0, 2):
            # Check ParCmd.BlendingParameter valid ?
            if SysDepIsValidReal(Value=self.ParCmd.BlendingParameter[_idx]) == False:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_JERK_INVALID, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.BlendingParameter[{2}] = {1}', Para1=VALID_REAL_TO_STRING(Value=self.ParCmd.JerkRate), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        else:
            _idx = st_for_end(0, 1)

        # Check ParCmd.MoveTime valid ?
        if self.ParCmd.MoveTime < 0:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.MoveTime = {1}', Para1=TIME_TO_STRING(self.ParCmd.MoveTime))
            return CheckParameterValid

        # Check ParCmd.BlendingMode valid ?
        if ((self.ParCmd.OriMode != OriMode.LINEAR_INTERPOLATED and self.ParCmd.OriMode != OriMode.JOINT_INTERPOLATED) and self.ParCmd.OriMode != OriMode.FIX) and self.ParCmd.OriMode != OriMode.PATH:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.OriMode = {1}', Para1=ORI_MODE_TO_STRING(Value=self.ParCmd.OriMode))
            return CheckParameterValid

        # Check ParCmd.ConfigMode.Shoulder valid ?
        if (((self.ParCmd.ConfigMode.Shoulder != ArmConfigShoulder.USE_CONFIG and self.ParCmd.ConfigMode.Shoulder != ArmConfigShoulder.SAME) and self.ParCmd.ConfigMode.Shoulder != ArmConfigShoulder.FREE) and self.ParCmd.ConfigMode.Shoulder != ArmConfigShoulder.BACK) and self.ParCmd.ConfigMode.Shoulder != ArmConfigShoulder.FRONT:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ConfigMode.Shoulder = {1}', Para1=ARM_CONFIG_SHOULDER_TO_STRING(Value=self.ParCmd.ConfigMode.Shoulder))
            return CheckParameterValid

        # Check ParCmd.ConfigMode.Elbow valid ?
        if (((self.ParCmd.ConfigMode.Elbow != ArmConfigElbow.USE_CONFIG and self.ParCmd.ConfigMode.Elbow != ArmConfigElbow.SAME) and self.ParCmd.ConfigMode.Elbow != ArmConfigElbow.FREE) and self.ParCmd.ConfigMode.Elbow != ArmConfigElbow.DOWN) and self.ParCmd.ConfigMode.Elbow != ArmConfigElbow.UP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ConfigMode.Elbow = {1}', Para1=ARM_CONFIG_ELBOW_TO_STRING(Value=self.ParCmd.ConfigMode.Elbow))
            return CheckParameterValid

        # Check ParCmd.ConfigMode.Wrist valid ?
        if (((self.ParCmd.ConfigMode.Wrist != ArmConfigWrist.USE_CONFIG and self.ParCmd.ConfigMode.Wrist != ArmConfigWrist.SAME) and self.ParCmd.ConfigMode.Wrist != ArmConfigWrist.FREE) and self.ParCmd.ConfigMode.Wrist != ArmConfigWrist.FLIP) and self.ParCmd.ConfigMode.Wrist != ArmConfigWrist.NON_FLIP:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.ConfigMode.Wrist = {1}', Para1=ARM_CONFIG_WRIST_TO_STRING(Value=self.ParCmd.ConfigMode.Wrist))
            return CheckParameterValid

        # Check ParCmd.TurnMode valid ?
        if (self.ParCmd.TurnMode != TurnMode.USE_TURN_NUMBER and self.ParCmd.TurnMode != TurnMode.SAME) and self.ParCmd.TurnMode != TurnMode.FREE:
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite=True)
            # Create log entry
            self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.TurnMode = {1}', Para1=TURN_MODE_TO_STRING(Value=self.ParCmd.TurnMode))
            return CheckParameterValid

        # Check ParCmd.Manipulation
        # -> no plausibility check for boolean
        for _idx in range(0, 4):
            # Check ParCmd.EmitterID valid ?
            if self.ParCmd.EmitterID[_idx] < -127 or self.ParCmd.EmitterID[_idx] > 127:
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                # ST-FIX F69
                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_EMITTERID_NOT_ALLOWED, Overwrite=True)
                # Create log entry
                self.CreateLogMessagePara2(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=self.ErrorID, MessageText='Invalid Parameter ParCmd.EmitterID[{2}] = {1}', Para1=SINT_TO_STRING(self.ParCmd.EmitterID[_idx]), Para2=DINT_TO_STRING(_idx))
                break
                return CheckParameterValid
        # ST-FIX F69: trigger IDs and SequenceFlag (table 7-1, 5.5.12.4, e.g. table 6-496)
        return CheckParameterValid

    def CreateCommandPayload(self, *, AxesGroup: _T.AxesGroup) -> RobotLibraryCommandDataFB:  # INTERNAL
        CreateCommandPayload: RobotLibraryCommandDataFB = RobotLibraryCommandDataFB()
        # internal index for loops
        _idx: int = 0
        # Parameter count
        _parameterCnt: int = 0

        # set command parameter
        self._command.CmdTyp = CmdType.MoveCircularAbsolute
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
        self._command.EmitterID[0] = self._parCmd.EmitterID[0]
        self._command.EmitterID[1] = self._parCmd.EmitterID[1]
        self._command.EmitterID[2] = self._parCmd.EmitterID[2]
        self._command.EmitterID[3] = self._parCmd.EmitterID[3]
        self._command.ListenerID = 0
        self._command.Reserve = 0
        self._command.VelocityRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.VelocityRate, IsOptional=False)
        self._command.AccelerationRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.AccelerationRate, IsOptional=False)
        self._command.DecelerationRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.DecelerationRate, IsOptional=True)
        self._command.JerkRate = REAL_TO_PERCENT_UINT(Value=self._parCmd.JerkRate, IsOptional=True)
        self._command.ToolNo = self._parCmd.ToolNo
        self._command.FrameNo = self._parCmd.FrameNo
        self._command.BlendingMode = self._parCmd.BlendingMode
        self._command.OriMode = self._parCmd.OriMode
        copy_into(self._command.BlendingParameter, self._parCmd.BlendingParameter)
        copy_into(self._command.AuxPoint, self._parCmd.AuxPoint)
        copy_into(self._command.EndPoint, self._parCmd.EndPoint)
        self._command.CircMode = self._parCmd.CircMode
        self._command.CircPlane = self._parCmd.CircPlane
        self._command.Tolerance = self._parCmd.Tolerance
        self._command.Angle = self._parCmd.Angle
        self._command.PathChoice = bit(self._parCmd.PathChoice, 0)
        self._command.Manipulation = self._parCmd.Manipulation
        copy_into(self._command.ConfigMode, ArmConfigParameterToBytes(Value=self._parCmd.ConfigMode))
        self._command.TurnMode = self._parCmd.TurnMode
        self._command.TurnMode = self._parCmd.TurnMode
        self._command.MoveTime = TIME_TO_UINT(self._parCmd.MoveTime)

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
            CreateCommandPayload.AddSint(Value=self._command.Reserve)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.VelocityRate
            CreateCommandPayload.AddUint(Value=self._command.VelocityRate)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AccelerationRate
            CreateCommandPayload.AddUint(Value=self._command.AccelerationRate)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.DecelerationRate
            CreateCommandPayload.AddUint(Value=self._command.DecelerationRate)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.JerkRate
            CreateCommandPayload.AddUint(Value=self._command.JerkRate)
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
            # add command.mFrameNo
            CreateCommandPayload.AddUsint(Value=self._command.FrameNo)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.BlendingMode
            CreateCommandPayload.AddUsint(Value=self._command.BlendingMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.OriMode
            CreateCommandPayload.AddUsint(Value=self._command.OriMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.BlendingParameter[0]
            CreateCommandPayload.AddReal(Value=self._command.BlendingParameter[0])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.BlendingParameter[1]
            CreateCommandPayload.AddReal(Value=self._command.BlendingParameter[1])
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.X
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.X)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.Y
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.Y)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.Z
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.Z)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.Rx
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.Rx)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.Ry
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.Ry)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.Rz
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.Rz)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.Config
            CreateCommandPayload.AddArmConfig(Value=self._command.AuxPoint.Config)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.TurnNumber
            CreateCommandPayload.AddTurnNumber(Value=self._command.AuxPoint.TurnNumber)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.E1
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.E1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.X
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.X)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.Y
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.Y)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.Z
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.Z)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.Rx
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.Rx)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.Ry
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.Ry)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.Rz
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.Rz)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.Config
            CreateCommandPayload.AddArmConfig(Value=self._command.EndPoint.Config)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.TurnNumber
            CreateCommandPayload.AddTurnNumber(Value=self._command.EndPoint.TurnNumber)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.E1
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.E1)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.CircMode
            CreateCommandPayload.AddSint(Value=self._command.CircMode)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.CircPlane
            CreateCommandPayload.AddSint(Value=self._command.CircPlane)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Tolerance
            CreateCommandPayload.AddReal(Value=self._command.Tolerance)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Angle
            CreateCommandPayload.AddReal(Value=self._command.Angle)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.PathChoice
            CreateCommandPayload.AddByte(Value=BOOL_TO_BYTE(self._command.PathChoice) | BOOL_TO_BYTE(self._command.Manipulation) << 1)  # ST-FIX F37
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.Manipulation
            CreateCommandPayload.AddByte(Value=0)  # ST-FIX F37: reserved byte, the value is bit 1 of the byte before
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # ST-FIX F33
        CreateCommandPayload.AddByte(Value=self._command.ConfigMode[0])
        _parameterCnt = _parameterCnt + 1
        CreateCommandPayload.AddByte(Value=self._command.ConfigMode[1])
        _parameterCnt = _parameterCnt + 1
        CreateCommandPayload.AddUsint(Value=self._command.TurnMode)
        _parameterCnt = _parameterCnt + 1
        CreateCommandPayload.AddByte(Value=0)
        _parameterCnt = _parameterCnt + 1
        CreateCommandPayload.AddUint(Value=self._command.MoveTime)
        _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.E2
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.E2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.E3
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.E3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.E4
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.E4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.E5
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.E5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.AuxPoint.E6
            CreateCommandPayload.AddReal(Value=self._command.AuxPoint.E6)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.E2
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.E2)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.E3
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.E3)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.E4
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.E4)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.E5
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.E5)
            # inc parameter counter
            _parameterCnt = _parameterCnt + 1

        # Check parameter must be added ?
        if self.CheckAddParameter(PayloadPtr=CreateCommandPayload.PayloadPtr):
            # add command.EndPoint.E6
            CreateCommandPayload.AddReal(Value=self._command.EndPoint.E6)
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
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=SINT_TO_STRING(self._command.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for VelocityRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.VelocityRate = {1}', Para1=UINT_TO_STRING(self._command.VelocityRate))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AccelerationRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AccelerationRate = {1}', Para1=UINT_TO_STRING(self._command.AccelerationRate))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for DecelerationRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.DecelerationRate = {1}', Para1=UINT_TO_STRING(self._command.DecelerationRate))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for JerkRate
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.JerkRate = {1}', Para1=UINT_TO_STRING(self._command.JerkRate))

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
        # Create log entry for BlendingMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.BlendingMode = {1}', Para1=BLENDING_MODE_TO_STRING(Value=self._command.BlendingMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for OriMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.OriMode = {1}', Para1=ORI_MODE_TO_STRING(Value=self._command.OriMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for BlendingParameter[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.BlendingParameter[0] = {1}', Para1=REAL_TO_STRING(self._command.BlendingParameter[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for BlendingParameter[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.BlendingParameter[1] = {1}', Para1=REAL_TO_STRING(self._command.BlendingParameter[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.X
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.X = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Y
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Y = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Z
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Z = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Rx
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Rx = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Ry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Ry = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Rz
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Rz = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Config
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._command.AuxPoint.Config))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.Config = {1}', Para1=SINT_TO_STRING(self._command.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.TurnNumber[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.TurnNumber[0] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.AuxPoint.TurnNumber.J2Turns, HalfSintLo=self._command.AuxPoint.TurnNumber.J1Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.TurnNumber[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.TurnNumber[1] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.AuxPoint.TurnNumber.J4Turns, HalfSintLo=self._command.AuxPoint.TurnNumber.J3Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.TurnNumber[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.TurnNumber[2] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.AuxPoint.TurnNumber.J6Turns, HalfSintLo=self._command.AuxPoint.TurnNumber.J5Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.TurnNumber[3]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.TurnNumber[3] = {1}', Para1=SINT_TO_STRING(self._command.AuxPoint.TurnNumber.E1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.E1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.E1 = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.X
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.X = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.X))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Y
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Y = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.Y))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Z
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Z = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.Z))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Rx
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Rx = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.Rx))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Ry
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Ry = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.Ry))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Rz
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Rz = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.Rz))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Config
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Config = {1}', Para1=ARM_CONFIG_TO_STRING(Value=self._command.EndPoint.Config))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.Config = {1}', Para1=SINT_TO_STRING(self._command.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.TurnNumber[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.TurnNumber[0] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.EndPoint.TurnNumber.J2Turns, HalfSintLo=self._command.EndPoint.TurnNumber.J1Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.TurnNumber[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.EndPoint[1] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.EndPoint.TurnNumber.J4Turns, HalfSintLo=self._command.EndPoint.TurnNumber.J3Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.TurnNumber[2]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.TurnNumber[2] = {1}', Para1=BYTE_TO_STRING(CombineHalfSints(HalfSintHi=self._command.EndPoint.TurnNumber.J6Turns, HalfSintLo=self._command.EndPoint.TurnNumber.J5Turns)))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.TurnNumber[3]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.TurnNumber[3] = {1}', Para1=SINT_TO_STRING(self._command.EndPoint.TurnNumber.E1Turns))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.E1
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.E1 = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.E1))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for CircMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.CircMode = {1}', Para1=CIRC_MODE_TO_STRING(Value=self._command.CircMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for CircPlane
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.CircPlane = {1}', Para1=CIRC_PLANE_TO_STRING(Value=self._command.CircPlane))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Tolerance
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Tolerance = {1}', Para1=REAL_TO_STRING(self._command.Tolerance))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Angle
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Angle = {1}', Para1=REAL_TO_STRING(self._command.Angle))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for PathChoice
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.PathChoice = {1}', Para1=BOOL_TO_STRING(self._command.PathChoice))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Manipulation
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Manipulation = {1}', Para1=BOOL_TO_STRING(self._command.Manipulation))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ConfigMode[0]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ConfigMode[0] = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.ConfigMode[0]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for ConfigMode[1]
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.ConfigMode[1] = {1}', Para1=BYTE_TO_STRING_BIN(Value=self._command.ConfigMode[1]))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for TurnMode
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.TurnMode = {1}', Para1=TURN_MODE_TO_STRING(Value=self._command.TurnMode))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for Reserve
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.Reserve = {1}', Para1=SINT_TO_STRING(self._command.Reserve))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for MoveTime
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.MoveTime = {1}', Para1=UINT_TO_STRING(self._command.MoveTime))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.E2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.E2 = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.E3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.E3 = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.E4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.E4 = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.E5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.E5 = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for AuxPoint.E6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.AuxPoint.E6 = {1}', Para1=REAL_TO_STRING(self._command.AuxPoint.E6))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.E2
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.E2 = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.E2))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.E3
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.E3 = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.E3))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.E4
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.E4 = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.E4))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.E5
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.E5 = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.E5))

        # Return if no parameter is remaining...
        if ParameterCnt == 0:
            return
        # dec remaining parameter(s)
        ParameterCnt = ParameterCnt - 1
        # Create log entry for EndPoint.E6
        self.CreateLogMessagePara1(Timestamp=AxesGroup.State.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='Command.EndPoint.E6 = {1}', Para1=REAL_TO_STRING(self._command.EndPoint.E6))

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_MoveCircularAbsoluteFB'

        self.ExecMode = ExecutionMode.SEQUENCE_PRIMARY
        self.Priority = PriorityLevel.NORMAL
        self.AbortingMode = AbortingMode.BUFFER
        self.SequenceFlag = SequenceFlag.PRIMARY_SEQUENCE
        return FB_init

    def OnApplyOutCmd(self, *, State: CmdMessageState = CmdMessageState.EMPTY) -> None:  # PROTECTED
        if State == CmdMessageState.EMPTY:
            # Reset command outputs
            SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(MoveCircularAbsoluteOutCmd)), Value=0, DataLen=12)

        if State == CmdMessageState.ACTIVE or State == CmdMessageState.DONE:
            # Update results
            self.OutCmd.FollowID = self._response.OriginID
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
                        SysDepMemSet(pDest=ADR(self, 'OutCmd', _iec.StructType(MoveCircularAbsoluteOutCmd)), Value=0, DataLen=12)
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
        self.CommandAborted = False
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
        self.CommandAborted = False
        self.CommandInterrupted = False
        return Reset
