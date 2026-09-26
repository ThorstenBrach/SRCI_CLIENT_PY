"""CMD_TYPE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/CMD_TYPE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import UINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import CmdType

__all__ = ['CMD_TYPE_TO_STRING']


def CMD_TYPE_TO_STRING(*, Value: CmdType = CmdType.RobotTask) -> str:
    CMD_TYPE_TO_STRING: str = ''

    match Value:
        case CmdType.RobotTask:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='RobotTask ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.RobotTask)), 80)

        case CmdType.ReadRobotData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadRobotData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadRobotData)), 80)

        case CmdType.EnableRobot:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='EnableRobot ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.EnableRobot)), 80)

        case CmdType.GroupReset:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='GroupReset ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.GroupReset)), 80)

        case CmdType.ReadActualPosition:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadActualPosition ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadActualPosition)), 80)

        case CmdType.ReadActualPositionCyclic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadActualPositionCyclic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadActualPositionCyclic)), 80)

        case CmdType.ReadDHParameter:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadDHParameter ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadDHParameter)), 80)

        case CmdType.RestartController:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='RestartController ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.RestartController)), 80)

        case CmdType.ReadActualTCPVelocity:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadActualTCPVelocity ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadActualTCPVelocity)), 80)

        case CmdType.UserLogin:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='UserLogin ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.UserLogin)), 80)

        case CmdType.SwitchLanguage:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SwitchLanguage ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SwitchLanguage)), 80)

        case CmdType.ExchangeConfiguration:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ExchangeConfiguration ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ExchangeConfiguration)), 80)

        case CmdType.SetSequence:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetSequence ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetSequence)), 80)

        case CmdType.ChangeSpeedOverride:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ChangeSpeedOverride ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ChangeSpeedOverride)), 80)

        case CmdType.ReadMessages:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadMessages ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadMessages)), 80)

        case CmdType.ReadRobotReferenceDynamics:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadRobotReferenceDynamics ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadRobotReferenceDynamics)), 80)

        case CmdType.WriteFrameData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteFrameData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteFrameData)), 80)

        case CmdType.WriteToolData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteToolData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteToolData)), 80)

        case CmdType.WriteLoadData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteLoadData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteLoadData)), 80)

        case CmdType.WriteRobotReferenceDynamics:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteRobotReferenceDynamics ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteRobotReferenceDynamics)), 80)

        case CmdType.WriteRobotDefaultDynamics:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteRobotDefaultDynamics ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteRobotDefaultDynamics)), 80)

        case CmdType.ReadRobotDefaultDynamics:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadRobotDefaultDynamics ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadRobotDefaultDynamics)), 80)

        case CmdType.ReadFrameData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadFrameData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadFrameData)), 80)

        case CmdType.ReadToolData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadToolData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadToolData)), 80)

        case CmdType.ReadLoadData:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadLoadData ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadLoadData)), 80)

        case CmdType.ReadRobotSWLimits:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadRobotSWLimits ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadRobotSWLimits)), 80)

        case CmdType.WriteRobotSWLimits:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteRobotSWLimits ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteRobotSWLimits)), 80)

        case CmdType.SetOperationMode:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetOperationMode ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetOperationMode)), 80)

        case CmdType.ReadWorkArea:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadWorkArea ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadWorkArea)), 80)

        case CmdType.WriteWorkArea:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteWorkArea ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteWorkArea)), 80)

        case CmdType.ActivateWorkArea:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ActivateWorkArea ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ActivateWorkArea)), 80)

        case CmdType.MonitorWorkArea:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MonitorWorkArea ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MonitorWorkArea)), 80)

        case CmdType.GroupJog:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='GroupJog ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.GroupJog)), 80)

        case CmdType.MoveLinearAbsolute:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveLinearAbsolute ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveLinearAbsolute)), 80)

        case CmdType.MoveDirectAbsolute:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveDirectAbsolute ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveDirectAbsolute)), 80)

        case CmdType.MoveAxesAbsolute:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveAxesAbsolute ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveAxesAbsolute)), 80)

        case CmdType.GroupStop:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='GroupStop ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.GroupStop)), 80)

        case CmdType.GroupInterrupt:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='GroupInterrupt ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.GroupInterrupt)), 80)

        case CmdType.GroupContinue:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='GroupContinue ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.GroupContinue)), 80)

        case CmdType.MoveLinearRelative:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveLinearRelative ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveLinearRelative)), 80)

        case CmdType.MoveDirectRelative:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveDirectRelative ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveDirectRelative)), 80)

        case CmdType.MoveAxesRelative:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveAxesRelative ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveAxesRelative)), 80)

        case CmdType.ReturnToPrimary:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReturnToPrimary ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReturnToPrimary)), 80)

        case CmdType.MoveCircularAbsolute:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveCircularAbsolute ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveCircularAbsolute)), 80)

        case CmdType.MoveCircularRelative:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveCircularRelative ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveCircularRelative)), 80)

        case CmdType.MoveLinearOffset:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveLinearOffset ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveLinearOffset)), 80)

        case CmdType.MoveDirectOffset:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveDirectOffset ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveDirectOffset)), 80)

        case CmdType.WaitTime:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WaitTime ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WaitTime)), 80)

        case CmdType.MoveApproachLinear:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveApproachLinear ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveApproachLinear)), 80)

        case CmdType.MoveDepartLinear:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveDepartLinear ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveDepartLinear)), 80)

        case CmdType.MoveApproachDirect:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveApproachDirect ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveApproachDirect)), 80)

        case CmdType.MoveDepartDirect:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveDepartDirect ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveDepartDirect)), 80)

        case CmdType.SearchHardstop:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SearchHardstop ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SearchHardstop)), 80)

        case CmdType.SearchHardstopJ:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SearchHardstopJ ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SearchHardstopJ)), 80)

        case CmdType.MovePickPlaceLinear:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MovePickPlaceLinear ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MovePickPlaceLinear)), 80)

        case CmdType.MovePickPlaceDirect:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MovePickPlaceDirect ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MovePickPlaceDirect)), 80)

        case CmdType.ActivateConveyorTracking:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ActivateConveyorTracking ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ActivateConveyorTracking)), 80)

        case CmdType.RedefineTrackingPos:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='RedefineTrackingPos ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.RedefineTrackingPos)), 80)

        case CmdType.SyncToConveyor:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SyncToConveyor ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SyncToConveyor)), 80)

        case CmdType.ConfigureConveyor:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ConfigureConveyor ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ConfigureConveyor)), 80)

        case CmdType.MoveSuperImposed:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveSuperImposed ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveSuperImposed)), 80)

        case CmdType.MoveSuperImposedDynamic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveSuperImposedDynamic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveSuperImposedDynamic)), 80)

        case CmdType.ReadDigitalInputs:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadDigitalInputs ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadDigitalInputs)), 80)

        case CmdType.ReadDigitalOutputs:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadDigitalOutputs ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadDigitalOutputs)), 80)

        case CmdType.WriteDigitalOutputs:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteDigitalOutputs ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteDigitalOutputs)), 80)

        case CmdType.ReadIntegers:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadIntegers ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadIntegers)), 80)

        case CmdType.ReadReals:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadReals ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadReals)), 80)

        case CmdType.WriteIntegers:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteIntegers ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteIntegers)), 80)

        case CmdType.WriteReals:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteReals ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteReals)), 80)

        case CmdType.MoveLinearCam:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveLinearCam ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveLinearCam)), 80)

        case CmdType.MoveDirectCam:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveDirectCam ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveDirectCam)), 80)

        case CmdType.MoveCircularCam:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveCircularCam ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveCircularCam)), 80)

        case CmdType.ReadAnalogInput:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadAnalogInput ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadAnalogInput)), 80)

        case CmdType.ReadAnalogOutput:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadAnalogOutput ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadAnalogOutput)), 80)

        case CmdType.WriteAnalogOutput:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteAnalogOutput ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteAnalogOutput)), 80)

        case CmdType.MeasuringInput:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MeasuringInput ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MeasuringInput)), 80)

        case CmdType.AbortMeasuringInput:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='AbortMeasuringInput ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.AbortMeasuringInput)), 80)

        case CmdType.SetTriggerRegister:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetTriggerRegister ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetTriggerRegister)), 80)

        case CmdType.SetTriggerLimit:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetTriggerLimit ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetTriggerLimit)), 80)

        case CmdType.SetTriggerUser:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetTriggerUser ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetTriggerUser)), 80)

        case CmdType.SetTriggerError:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetTriggerError ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetTriggerError)), 80)

        case CmdType.ReactAtTrigger:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReactAtTrigger ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReactAtTrigger)), 80)

        case CmdType.WaitForTrigger:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WaitForTrigger ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WaitForTrigger)), 80)

        case CmdType.ReadSystemVariable:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadSystemVariable ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadSystemVariable)), 80)

        case CmdType.WriteSystemVariable:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteSystemVariable ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteSystemVariable)), 80)

        case CmdType.CalculateForwardKinematic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CalculateForwardKinematic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CalculateForwardKinematic)), 80)

        case CmdType.CalculateInverseKinematic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CalculateInverseKinematic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CalculateInverseKinematic)), 80)

        case CmdType.CalculateCartesianPosition:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CalculateCartesianPosition ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CalculateCartesianPosition)), 80)

        case CmdType.CalculateTool:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CalculateTool ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CalculateTool)), 80)

        case CmdType.CalculateFrame:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CalculateFrame ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CalculateFrame)), 80)

        case CmdType.ActivateNextCommand:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ActivateNextCommand ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ActivateNextCommand)), 80)

        case CmdType.ShiftPosition:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ShiftPosition ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ShiftPosition)), 80)

        case CmdType.SetTriggerMotion:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SetTriggerMotion ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SetTriggerMotion)), 80)

        case CmdType.OpenBrake:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='OpenBrake ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.OpenBrake)), 80)

        case CmdType.CallSubprogram:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CallSubprogram ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CallSubprogram)), 80)

        case CmdType.WriteCallSubprogramCyclic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='WriteCallSubprogramCyclic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.WriteCallSubprogramCyclic)), 80)

        case CmdType.ReadCallSubprogramCyclic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadCallSubprogramCyclic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadCallSubprogramCyclic)), 80)

        case CmdType.StopSubprogram:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='StopSubprogram ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.StopSubprogram)), 80)

        case CmdType.PathAccuracyMode:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='PathAccuracyMode ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.PathAccuracyMode)), 80)

        case CmdType.AvoidSingularity:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='AvoidSingularity ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.AvoidSingularity)), 80)

        case CmdType.ForceControl:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ForceControl ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ForceControl)), 80)

        case CmdType.ForceLimit:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ForceLimit ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ForceLimit)), 80)

        case CmdType.ReadActualForce:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='ReadActualForce ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.ReadActualForce)), 80)

        case CmdType.BrakeTest:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='BrakeTest ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.BrakeTest)), 80)

        case CmdType.SoftSwitchTCP:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='SoftSwitchTCP ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.SoftSwitchTCP)), 80)

        case CmdType.CreateSpline:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CreateSpline ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CreateSpline)), 80)

        case CmdType.DeleteSpline:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='DeleteSpline ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.DeleteSpline)), 80)

        case CmdType.MoveSpline:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='MoveSpline ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.MoveSpline)), 80)

        case CmdType.DynamicSpline:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='DynamicSpline ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.DynamicSpline)), 80)

        case CmdType.LoadMeasurementAutomatic:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='LoadMeasurementAutomatic ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.LoadMeasurementAutomatic)), 80)

        case CmdType.LoadMeasurementSequential:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='LoadMeasurementSequential ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.LoadMeasurementSequential)), 80)

        case CmdType.CollisionDetection:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='CollisionDetection ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.CollisionDetection)), 80)

        case CmdType.FreeDrive:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='FreeDrive ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.FreeDrive)), 80)

        case CmdType.UnitMeasurement:
            CMD_TYPE_TO_STRING = trunc_str(StrReplace(Str='UnitMeasurement ({0})', SubStr1='{0}', SubStr2=UINT_TO_STRING(CmdType.UnitMeasurement)), 80)
        case _:
            CMD_TYPE_TO_STRING = trunc_str(CONCAT('CMD_TYPE_TO_STRING Function: Error -> no parsing for value', UINT_TO_STRING(Value)), 80)
    return CMD_TYPE_TO_STRING
