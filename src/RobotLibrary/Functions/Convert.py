"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      Convert
Author:      Thorsten Brach
Date:        2026-01-05

Description:
  Converts various data types to their string representations

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
from datetime import datetime, timedelta
from RobotLibrary.IEC_Types import ARRAY, BYTE, DWORD, INT, SINT, WORD, USINT, UINT, DATE, TIME, REAL, TOD
from RobotLibrary import Constants as RobotLibraryConstants
from RobotLibrary.Parameter import SWAP_BYTE_ORDER


from RobotLibrary.Enumerations.Mode.SyncMode import SyncMode
from RobotLibrary.Enumerations.Mode.OperationMode import OperationMode
from RobotLibrary.Enumerations.State.RaSequenceState import RaSequenceState
from RobotLibrary.Enumerations.ArmConfig.ArmConfigShoulder import ArmConfigShoulder
from RobotLibrary.Enumerations.ArmConfig.ArmConfigElbow import ArmConfigElbow
from RobotLibrary.Enumerations.ArmConfig.ArmConfigWrist import ArmConfigWrist
from RobotLibrary.Enumerations.Miscellaneous.AxisUnit import AxisUnit
from RobotLibrary.Enumerations.Miscellaneous.SyncTime import SyncTime

from RobotLibrary.Structures.Miscellaneous.ArmConfigParameter import ArmConfigParameter
from RobotLibrary.Structures.Miscellaneous.FragmentAction import FragmentAction
from RobotLibrary.Structures.Axis.AxisExternalUnit import AxisExternalUnit
from RobotLibrary.Structures.Axis.AxisExternalUsed import AxisExternalUsed
from RobotLibrary.Structures.Axis.AxisJointUnit import AxisJointUnit
from RobotLibrary.Structures.Axis.AxisJointUsed import AxisJointUsed
from RobotLibrary.Structures.Miscellaneous.RCSupportedFunctions import RCSupportedFunctions
from RobotLibrary.Structures.Miscellaneous.RaStatusWord import RaStatusWord
from RobotLibrary.Structures.Miscellaneous.SynchronizationModes import SynchronizationModes
from RobotLibrary.Structures.Miscellaneous.DataEnableSync import DataEnableSync
from RobotLibrary.Structures.Miscellaneous.VersionStruct import VersionStruct
from RobotLibrary.Structures.AxesGroup.Parameter.Plc.AxesGroupParameterPlc import AxesGroupParameterPlcOptionalCyclic
from RobotLibrary.Structures.AxesGroup.Parameter.Rob.AxesGroupParameterRob import AxesGroupParameterRobOptionalCyclic
from RobotLibrary.Structures.DatenAndTime.IEC_DATE import IEC_DATE
from RobotLibrary.Structures.DatenAndTime.IEC_TIME import IEC_TIME
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime


#-------------------------------------------------------------------------
# ByteToFragmentAction - convert BYTE to FragmentAction structure
#-------------------------------------------------------------------------
def ByteToFragmentAction (value : BYTE) -> FragmentAction:

    # return value of function    
    ByteToFragmentAction : FragmentAction = FragmentAction()

    ByteToFragmentAction.Complete.value = value.Bit[0]
    ByteToFragmentAction.Reset.value    = value.Bit[1]
    ByteToFragmentAction.Clear.value    = value.Bit[2]
    ByteToFragmentAction.BIT03.value    = value.Bit[3]
    ByteToFragmentAction.BIT04.value    = value.Bit[4]
    ByteToFragmentAction.BIT05.value    = value.Bit[5]
    ByteToFragmentAction.BIT06.value    = value.Bit[6]
    ByteToFragmentAction.BIT07.value    = value.Bit[7]

    return ByteToFragmentAction

#-------------------------------------------------------------------------
# ByteToAxisJointUsed - convert BYTE to AxisJointUsed structure
#-------------------------------------------------------------------------
def ByteToAxisJointUsed (value : BYTE) -> AxisJointUsed:
    """Convert BYTE to a representing structure of AxisJointUsed."""
    ByteToAxisJointUsed : AxisJointUsed = AxisJointUsed()
    
    ByteToAxisJointUsed.J1.value = value.Bit[1]
    ByteToAxisJointUsed.J2.value = value.Bit[2]
    ByteToAxisJointUsed.J3.value = value.Bit[3]
    ByteToAxisJointUsed.J4.value = value.Bit[4]
    ByteToAxisJointUsed.J5.value = value.Bit[5]
    ByteToAxisJointUsed.J6.value = value.Bit[6]
    
    return ByteToAxisJointUsed


#-------------------------------------------------------------------------
# ByteToAxisExternalUsed - convert BYTE to AxisExternalUsed structure
#-------------------------------------------------------------------------
def ByteToAxisExternalUsed (value : BYTE) -> AxisExternalUsed:
    """Convert BYTE to a representing structure of AxisExternalUsed."""
    ByteToAxisExternalUsed : AxisExternalUsed = AxisExternalUsed()
    
    ByteToAxisExternalUsed.E1.value = value.Bit[1]
    ByteToAxisExternalUsed.E2.value = value.Bit[2]
    ByteToAxisExternalUsed.E3.value = value.Bit[3]
    ByteToAxisExternalUsed.E4.value = value.Bit[4]
    ByteToAxisExternalUsed.E5.value = value.Bit[5]
    ByteToAxisExternalUsed.E6.value = value.Bit[6]
    
    return ByteToAxisExternalUsed


#-------------------------------------------------------------------------
# ByteToAxisJointUnit - convert BYTE to AxisJointUnit structure
#-------------------------------------------------------------------------
def ByteToAxisJointUnit( value : BYTE) -> AxisJointUnit:
    """Convert BYTE to a representing structure of AxisJointUnit."""
    ByteToAxisJointUnit : AxisJointUnit = AxisJointUnit()
    
    ByteToAxisJointUnit.J1 = AxisUnit(int(value.Bit[1]))
    ByteToAxisJointUnit.J2 = AxisUnit(int(value.Bit[2]))
    ByteToAxisJointUnit.J3 = AxisUnit(int(value.Bit[3]))
    ByteToAxisJointUnit.J4 = AxisUnit(int(value.Bit[4]))
    ByteToAxisJointUnit.J5 = AxisUnit(int(value.Bit[5]))
    ByteToAxisJointUnit.J6 = AxisUnit(int(value.Bit[6]))
    
    return ByteToAxisJointUnit


#-------------------------------------------------------------------------
# ByteToAxisExternalUnit - convert BYTE to AxisExternalUnit structure
#-------------------------------------------------------------------------
def ByteToAxisExternalUnit( value : BYTE) -> AxisExternalUnit:
    """Convert BYTE to a representing structure of AxisExternalUnit."""
    ByteToAxisExternalUnit : AxisExternalUnit = AxisExternalUnit()
    
    ByteToAxisExternalUnit.E1 = AxisUnit(int(value.Bit[1]))
    ByteToAxisExternalUnit.E2 = AxisUnit(int(value.Bit[2]))
    ByteToAxisExternalUnit.E3 = AxisUnit(int(value.Bit[3]))
    ByteToAxisExternalUnit.E4 = AxisUnit(int(value.Bit[4]))
    ByteToAxisExternalUnit.E5 = AxisUnit(int(value.Bit[5]))
    ByteToAxisExternalUnit.E6 = AxisUnit(int(value.Bit[6]))
    
    return ByteToAxisExternalUnit


#-------------------------------------------------------------------------
# BytesToRCSupportedFunctions - convert ARRAY[BYTE] to RCSupportedFunctions structure
#-------------------------------------------------------------------------
def BytesToRCSupportedFunctions(value: bytearray) -> RCSupportedFunctions:
    """Convert bytes to a list of booleans representing RCSupportedFunctions."""
    BytesToRCSupportedFunctions : RCSupportedFunctions = RCSupportedFunctions()
    
    # Byte 00 - Bit 0  
    BytesToRCSupportedFunctions.Byte00Bit0.value                 = BYTE(value[00]).Bit[0]
    # Byte 00 - Bit 1 
    BytesToRCSupportedFunctions.ReadRobotData.value              = BYTE(value[00]).Bit[1]
    # Byte 00 - Bit 2  
    BytesToRCSupportedFunctions.EnableRobot.value                = BYTE(value[00]).Bit[2]
    # Byte 00 - Bit 3  
    BytesToRCSupportedFunctions.GroupReset.value                 = BYTE(value[00]).Bit[3]
    # Byte 00 - Bit 4  
    BytesToRCSupportedFunctions.ReadActualPosition.value         = BYTE(value[00]).Bit[4]
    # Byte 00 - Bit 5 
    BytesToRCSupportedFunctions.ReadActualPositionCyclic.value   = BYTE(value[00]).Bit[5]
    # Byte 00 - Bit 6  
    BytesToRCSupportedFunctions.ExchangeConfiguration.value      = BYTE(value[00]).Bit[6]
    # Byte 00 - Bit 7  
    BytesToRCSupportedFunctions.SetSequence.value                = BYTE(value[00]).Bit[7]
    # Byte 01 - Bit 0  
    BytesToRCSupportedFunctions.ChangeSpeedOverride.value        = BYTE(value[1]).Bit[0]
    # Byte 01 - Bit 1  
    BytesToRCSupportedFunctions.ReadMessages.value               = BYTE(value[1]).Bit[1]
    # Byte 01 - Bit 2  
    BytesToRCSupportedFunctions.ReadRobotReferenceDynamics.value = BYTE(value[1]).Bit[2]
    # Byte 01 - Bit 3  
    BytesToRCSupportedFunctions.WriteFrameData.value             = BYTE(value[1]).Bit[3]
    # Byte 01 - Bit 4  
    BytesToRCSupportedFunctions.WriteToolData.value              = BYTE(value[1]).Bit[4]
    # Byte 01 - Bit 5  
    BytesToRCSupportedFunctions.WriteLoadData.value              = BYTE(value[1]).Bit[5]
    # Byte 01 - Bit 6  
    BytesToRCSupportedFunctions.WriteRobotReferenceDynamics.value= BYTE(value[1]).Bit[6]
    # Byte 01 - Bit 7  
    BytesToRCSupportedFunctions.WriteRobotDefaultDynamics.value  = BYTE(value[1]).Bit[7]

    # Byte 02 - Bit 0  
    BytesToRCSupportedFunctions.ReadRobotDefaultDynamics.value   = BYTE(value[2]).Bit[0]
    # Byte 02 - Bit 1  
    BytesToRCSupportedFunctions.ReadFrameData.value              = BYTE(value[2]).Bit[1]
    # Byte 02 - Bit 2  
    BytesToRCSupportedFunctions.ReadToolData.value               = BYTE(value[2]).Bit[2]
    # Byte 02 - Bit 3  
    BytesToRCSupportedFunctions.ReadLoadData.value               = BYTE(value[2]).Bit[3]
    # Byte 02 - Bit 4  
    BytesToRCSupportedFunctions.ReadRobotSWLimits.value          = BYTE(value[2]).Bit[4]
    # Byte 02 - Bit 5  
    BytesToRCSupportedFunctions.GroupJog.value                   = BYTE(value[2]).Bit[5]
    # Byte 02 - Bit 6  
    BytesToRCSupportedFunctions.MoveLinearAbsolute.value         = BYTE(value[2]).Bit[6]
    # Byte 02 - Bit 7  
    BytesToRCSupportedFunctions.MoveDirectAbsolute.value         = BYTE(value[2]).Bit[7]

    # Byte 03 - Bit 0  
    BytesToRCSupportedFunctions.MoveAxesAbsolute.value           = BYTE(value[3]).Bit[0]
    # Byte 03 - Bit 1  
    BytesToRCSupportedFunctions.GroupStop.value                  = BYTE(value[3]).Bit[1]
    # Byte 03 - Bit 2
    BytesToRCSupportedFunctions.GroupContinue.value              = BYTE(value[3]).Bit[2]
    # Byte 03 - Bit 3
    BytesToRCSupportedFunctions.GroupInterrupt.value             = BYTE(value[3]).Bit[3]
    # Byte 03 - Bit 4
    BytesToRCSupportedFunctions.ReturnToPrimary.value            = BYTE(value[3]).Bit[4]
    # Byte 03 - Bit 5
    BytesToRCSupportedFunctions.MoveLinearAbsoluteJ.value        = BYTE(value[3]).Bit[5]
    # Byte 03 - Bit 6
    BytesToRCSupportedFunctions.MoveDirectRelative.value         = BYTE(value[3]).Bit[6]
    # Byte 03 - Bit 7
    BytesToRCSupportedFunctions.MoveAxesRelative.value           = BYTE(value[3]).Bit[7]
    # Byte 04 - Bit 0
    BytesToRCSupportedFunctions.MoveCircularAbsolute.value       = BYTE(value[4]).Bit[0]
    # Byte 04 - Bit 1
    BytesToRCSupportedFunctions.MoveCircularRelative.value       = BYTE(value[4]).Bit[1]
    # Byte 04 - Bit 2
    BytesToRCSupportedFunctions.MoveLinearOffset.value           = BYTE(value[4]).Bit[2]
    # Byte 04 - Bit 3
    BytesToRCSupportedFunctions.MoveDirectOffset.value           = BYTE(value[4]).Bit[3]
    # Byte 04 - Bit 4
    BytesToRCSupportedFunctions.WaitTime.value                   = BYTE(value[4]).Bit[4]
    # Byte 04 - Bit 5
    BytesToRCSupportedFunctions.ReadDigitalInputs.value          = BYTE(value[4]).Bit[5]
    # Byte 04 - Bit 6
    BytesToRCSupportedFunctions.ReadDigitalOutputs.value         = BYTE(value[4]).Bit[6]
    # Byte 04 - Bit 7
    BytesToRCSupportedFunctions.WriteDigitalOutputs.value        = BYTE(value[4]).Bit[7]
    # Byte 05 - Bit 0
    BytesToRCSupportedFunctions.ReadIntegers.value               = BYTE(value[5]).Bit[0]
    # Byte 05 - Bit 1
    BytesToRCSupportedFunctions.ReadReals.value                  = BYTE(value[5]).Bit[1]
    # Byte 05 - Bit 2
    BytesToRCSupportedFunctions.WriteIntegers.value              = BYTE(value[5]).Bit[2]
    # Byte 05 - Bit 3
    BytesToRCSupportedFunctions.WriteReals.value                 = BYTE(value[5]).Bit[3]
    # Byte 05 - Bit 4
    BytesToRCSupportedFunctions.MoveLinearCam.value              = BYTE(value[5]).Bit[4]
    # Byte 05 - Bit 5
    BytesToRCSupportedFunctions.MoveDirectCam.value              = BYTE(value[5]).Bit[5]
    # Byte 05 - Bit 6
    BytesToRCSupportedFunctions.MoveCircularCam.value            = BYTE(value[5]).Bit[6]
    # Byte 05 - Bit 7
    BytesToRCSupportedFunctions.SetTriggerRegister.value         = BYTE(value[5]).Bit[7]
    # Byte 06 - Bit 0
    BytesToRCSupportedFunctions.SetTriggerLimit.value            = BYTE(value[6]).Bit[0]
    # Byte 06 - Bit 1
    BytesToRCSupportedFunctions.SetTriggerUser.value             = BYTE(value[6]).Bit[1]
    # Byte 06 - Bit 2
    BytesToRCSupportedFunctions.SetTriggerError.value            = BYTE(value[6]).Bit[2]
    # Byte 06 - Bit 3
    BytesToRCSupportedFunctions.ReactAtTrigger.value             = BYTE(value[6]).Bit[3]
    # Byte 06 - Bit 4
    BytesToRCSupportedFunctions.WaitForTrigger.value             = BYTE(value[6]).Bit[4]
    # Byte 06 - Bit 5
    BytesToRCSupportedFunctions.ReadSystemVariable.value         = BYTE(value[6]).Bit[5]
    # Byte 06 - Bit 6
    BytesToRCSupportedFunctions.WriteSystemVariable.value        = BYTE(value[6]).Bit[6]
    # Byte 06 - Bit 7
    BytesToRCSupportedFunctions.CalculateForwardKinematic.value  = BYTE(value[6]).Bit[7]
    # Byte 07 - Bit 0
    BytesToRCSupportedFunctions.CalculateInverseKinematic.value  = BYTE(value[7]).Bit[0]
    # Byte 07 - Bit 1
    BytesToRCSupportedFunctions.CalculateCartesianPosition.value = BYTE(value[7]).Bit[1]
    # Byte 07 - Bit 2
    BytesToRCSupportedFunctions.CalculateTool.value              = BYTE(value[7]).Bit[2]
    # Byte 07 - Bit 3
    BytesToRCSupportedFunctions.CalculateFrame.value             = BYTE(value[7]).Bit[3]
    # Byte 07 - Bit 4
    BytesToRCSupportedFunctions.ActivateNextCommand.value        = BYTE(value[7]).Bit[4]
    # Byte 07 - Bit 5
    BytesToRCSupportedFunctions.ShiftPosition.value              = BYTE(value[7]).Bit[5]
    # Byte 07 - Bit 6
    BytesToRCSupportedFunctions.CallSubprogram.value             = BYTE(value[7]).Bit[6]
    # Byte 07 - Bit 7
    BytesToRCSupportedFunctions.MoveLinearRelative.value         = BYTE(value[7]).Bit[7]

    # Byte 08 - Bit 0
    BytesToRCSupportedFunctions.WriteCallSubprogramCyclic.value  = BYTE(value[8]).Bit[0]
    # Byte 08 - Bit 1
    BytesToRCSupportedFunctions.ReadCallSubprogramCyclic.value   = BYTE(value[8]).Bit[1]
    # Byte 08 - Bit 2
    BytesToRCSupportedFunctions.StopSubprogram.value             = BYTE(value[8]).Bit[2]
    # Byte 08 - Bit 3
    BytesToRCSupportedFunctions.ReadDHParameter.value            = BYTE(value[8]).Bit[3]
    # Byte 08 - Bit 4
    BytesToRCSupportedFunctions.RestartController.value          = BYTE(value[8]).Bit[4]
    # Byte 08 - Bit 5
    BytesToRCSupportedFunctions.ReadActualTCPVelocity.value      = BYTE(value[8]).Bit[5]
    # Byte 08 - Bit 6
    BytesToRCSupportedFunctions.UserLogin.value                  = BYTE(value[8]).Bit[6]
    # Byte 08 - Bit 7
    BytesToRCSupportedFunctions.SwitchLanguage.value             = BYTE(value[8]).Bit[7]

    # Byte 09 - Bit 0
    BytesToRCSupportedFunctions.WriteRobotSWLimits.value         = BYTE(value[9]).Bit[0]
    # Byte 09 - Bit 1
    BytesToRCSupportedFunctions.SetOperationMode.value           = BYTE(value[9]).Bit[1]
    # Byte 09 - Bit 2
    BytesToRCSupportedFunctions.ReadWorkArea.value               = BYTE(value[9]).Bit[2]
    # Byte 09 - Bit 3
    BytesToRCSupportedFunctions.WriteWorkArea.value              = BYTE(value[9]).Bit[3]
    # Byte 09 - Bit 4
    BytesToRCSupportedFunctions.ActivateWorkArea.value           = BYTE(value[9]).Bit[4]
    # Byte 09 - Bit 5
    BytesToRCSupportedFunctions.MonitorWorkArea.value            = BYTE(value[9]).Bit[5]
    # Byte 09 - Bit 6
    BytesToRCSupportedFunctions.MoveApproachLinear.value         = BYTE(value[9]).Bit[6]
    # Byte 09 - Bit 7
    BytesToRCSupportedFunctions.MoveDepartLinear.value           = BYTE(value[9]).Bit[7]

    # Byte 10 - Bit 0
    BytesToRCSupportedFunctions.MoveApproachDirect.value         = BYTE(value[10]).Bit[0]
    # Byte 10 - Bit 1
    BytesToRCSupportedFunctions.MoveDepartDirect.value           = BYTE(value[10]).Bit[1]
    # Byte 10 - Bit 2
    BytesToRCSupportedFunctions.SearchHardstop.value             = BYTE(value[10]).Bit[2]
    # Byte 10 - Bit 3
    BytesToRCSupportedFunctions.SearchHardstopJ.value            = BYTE(value[10]).Bit[3]
    # Byte 10 - Bit 4
    BytesToRCSupportedFunctions.MovePickPlaceLinear.value        = BYTE(value[10]).Bit[4]
    # Byte 10 - Bit 5
    BytesToRCSupportedFunctions.MovePickPlaceDirect.value        = BYTE(value[10]).Bit[5]
    # Byte 10 - Bit 6
    BytesToRCSupportedFunctions.ActivateConveyorTracking.value   = BYTE(value[10]).Bit[6]
    # Byte 10 - Bit 7
    BytesToRCSupportedFunctions.RedefineTrackingPosition.value   = BYTE(value[10]).Bit[7]

    # Byte 11 - Bit 0
    BytesToRCSupportedFunctions.SyncToConveyor.value             = BYTE(value[11]).Bit[0]
    # Byte 11 - Bit 1
    BytesToRCSupportedFunctions.ConfigureConveyor.value          = BYTE(value[11]).Bit[1]
    # Byte 11 - Bit 2
    BytesToRCSupportedFunctions.MoveSuperImposed.value           = BYTE(value[11]).Bit[2]
    # Byte 11 - Bit 3
    BytesToRCSupportedFunctions.MoveSuperImposedDynamic.value    = BYTE(value[11]).Bit[3]
    # Byte 11 - Bit 4
    BytesToRCSupportedFunctions.ReadAnalogInput.value            = BYTE(value[11]).Bit[4]
    # Byte 11 - Bit 5
    BytesToRCSupportedFunctions.ReadAnalogOutput.value           = BYTE(value[11]).Bit[5]
    # Byte 11 - Bit 6
    BytesToRCSupportedFunctions.WriteAnalogOutput.value          = BYTE(value[11]).Bit[6]
    # Byte 11 - Bit 7
    BytesToRCSupportedFunctions.MeasuringInput.value             = BYTE(value[11]).Bit[7]

    # Byte 12 - Bit 0
    BytesToRCSupportedFunctions.AbortMeasuringInput.value        = BYTE(value[12]).Bit[0]
    # Byte 12 - Bit 1
    BytesToRCSupportedFunctions.SetTriggerMotion.value           = BYTE(value[12]).Bit[1]
    # Byte 12 - Bit 2
    BytesToRCSupportedFunctions.OpenBrake.value                  = BYTE(value[12]).Bit[2]
    # Byte 12 - Bit 3
    BytesToRCSupportedFunctions.PathAccuracyMode.value           = BYTE(value[12]).Bit[3]
    # Byte 12 - Bit 4
    BytesToRCSupportedFunctions.AvoidSingularity.value           = BYTE(value[12]).Bit[4]
    # Byte 12 - Bit 5
    BytesToRCSupportedFunctions.ForceControl.value               = BYTE(value[12]).Bit[5]
    # Byte 12 - Bit 6
    BytesToRCSupportedFunctions.ForceLimit.value                 = BYTE(value[12]).Bit[6]
    # Byte 12 - Bit 7
    BytesToRCSupportedFunctions.ReadActualForce.value            = BYTE(value[12]).Bit[7]

    # Byte 13 - Bit 0
    BytesToRCSupportedFunctions.BrakeTest.value                  = BYTE(value[13]).Bit[0]
    # Byte 13 - Bit 1
    BytesToRCSupportedFunctions.SoftSwitchTCP.value              = BYTE(value[13]).Bit[1]
    # Byte 13 - Bit 2
    BytesToRCSupportedFunctions.CreateSpline.value               = BYTE(value[13]).Bit[2]
    # Byte 13 - Bit 3
    BytesToRCSupportedFunctions.DeleteSpline.value               = BYTE(value[13]).Bit[3]
    # Byte 13 - Bit 4
    BytesToRCSupportedFunctions.MoveSpline.value                 = BYTE(value[13]).Bit[4]
    # Byte 13 - Bit 5
    BytesToRCSupportedFunctions.DynamicSpline.value              = BYTE(value[13]).Bit[5]
    # Byte 13 - Bit 6
    BytesToRCSupportedFunctions.LoadMeasurementAutomatic.value   = BYTE(value[13]).Bit[6]
    # Byte 13 - Bit 7
    BytesToRCSupportedFunctions.LoadMeasurementSequential.value  = BYTE(value[13]).Bit[7]

    # Byte 14 - Bit 0
    BytesToRCSupportedFunctions.CollisionDetection.value         = BYTE(value[14]).Bit[0]
    # Byte 14 - Bit 1
    BytesToRCSupportedFunctions.FreeDrive.value                  = BYTE(value[14]).Bit[1]
    # Byte 14 - Bit 2
    BytesToRCSupportedFunctions.UnitMeasurement.value            = BYTE(value[14]).Bit[2]
    # Byte 14 - Bit 3
    BytesToRCSupportedFunctions.Byte14Bit03.value                = BYTE(value[14]).Bit[3]
    # Byte 14 - Bit 4
    BytesToRCSupportedFunctions.Byte14Bit04.value                = BYTE(value[14]).Bit[4]
    # Byte 14 - Bit 5
    BytesToRCSupportedFunctions.Byte14Bit05.value                = BYTE(value[14]).Bit[5]
    # Byte 14 - Bit 6
    BytesToRCSupportedFunctions.Byte14Bit06.value                = BYTE(value[14]).Bit[6]
    # Byte 14 - Bit 7
    BytesToRCSupportedFunctions.Byte14Bit07.value                = BYTE(value[14]).Bit[7]

    # Byte 15 - Bit 0
    BytesToRCSupportedFunctions.Byte15Bit00.value                = BYTE(value[15]).Bit[0]
    # Byte 15 - Bit 1
    BytesToRCSupportedFunctions.Byte15Bit01.value                = BYTE(value[15]).Bit[1]
    # Byte 15 - Bit 2
    BytesToRCSupportedFunctions.Byte15Bit02.value                = BYTE(value[15]).Bit[2]
    # Byte 15 - Bit 3
    BytesToRCSupportedFunctions.Byte15Bit03.value                = BYTE(value[15]).Bit[3]
    # Byte 15 - Bit 4
    BytesToRCSupportedFunctions.Byte15Bit04.value                = BYTE(value[15]).Bit[4]
    # Byte 15 - Bit 5
    BytesToRCSupportedFunctions.Byte15Bit05.value                = BYTE(value[15]).Bit[5]
    # Byte 15 - Bit 6
    BytesToRCSupportedFunctions.Byte15Bit06.value                = BYTE(value[15]).Bit[6]
    # Byte 15 - Bit 7
    BytesToRCSupportedFunctions.Byte15Bit07.value                = BYTE(value[15]).Bit[7]

    # Byte 16 - Bit 0
    BytesToRCSupportedFunctions.Byte16Bit00.value                = BYTE(value[16]).Bit[0]
    # Byte 15 - Bit 1
    BytesToRCSupportedFunctions.Byte16Bit01.value                = BYTE(value[16]).Bit[1]
    # Byte 15 - Bit 2
    BytesToRCSupportedFunctions.Byte16Bit02.value                = BYTE(value[16]).Bit[2]
    # Byte 15 - Bit 3
    BytesToRCSupportedFunctions.Byte16Bit03.value                = BYTE(value[16]).Bit[3]
    # Byte 15 - Bit 4
    BytesToRCSupportedFunctions.Byte16Bit04.value                = BYTE(value[16]).Bit[4]
    # Byte 15 - Bit 5
    BytesToRCSupportedFunctions.Byte16Bit05.value                = BYTE(value[16]).Bit[5]
    # Byte 15 - Bit 6
    BytesToRCSupportedFunctions.Byte16Bit06.value                = BYTE(value[16]).Bit[6]
    # Byte 15 - Bit 7
    BytesToRCSupportedFunctions.Byte16Bit07.value                = BYTE(value[16]).Bit[7]

    # Byte 17 - Bit 0
    BytesToRCSupportedFunctions.Byte17Bit00.value                = BYTE(value[17]).Bit[0]
    # Byte 17 - Bit 1
    BytesToRCSupportedFunctions.Byte17Bit01.value                = BYTE(value[17]).Bit[1]
    # Byte 17 - Bit 2
    BytesToRCSupportedFunctions.Byte17Bit02.value                = BYTE(value[17]).Bit[2]
    # Byte 17 - Bit 3
    BytesToRCSupportedFunctions.Byte17Bit03.value                = BYTE(value[17]).Bit[3]
    # Byte 17 - Bit 4
    BytesToRCSupportedFunctions.Byte17Bit04.value                = BYTE(value[17]).Bit[4]
    # Byte 17 - Bit 5
    BytesToRCSupportedFunctions.Byte17Bit05.value                = BYTE(value[17]).Bit[5]
    # Byte 17 - Bit 6
    BytesToRCSupportedFunctions.Byte17Bit06.value                = BYTE(value[17]).Bit[6]
    # Byte 17 - Bit 7
    BytesToRCSupportedFunctions.Byte17Bit07.value                = BYTE(value[17]).Bit[7]

    # Byte 18 - Bit 0
    BytesToRCSupportedFunctions.Byte18Bit00.value                = BYTE(value[18]).Bit[0]
    # Byte 18 - Bit 1
    BytesToRCSupportedFunctions.Byte18Bit01.value                = BYTE(value[18]).Bit[1]
    # Byte 18 - Bit 2
    BytesToRCSupportedFunctions.Byte18Bit02.value                = BYTE(value[18]).Bit[2]
    # Byte 18 - Bit 3
    BytesToRCSupportedFunctions.Byte18Bit03.value                = BYTE(value[18]).Bit[3]
    # Byte 18 - Bit 4
    BytesToRCSupportedFunctions.Byte18Bit04.value                = BYTE(value[18]).Bit[4]
    # Byte 18 - Bit 5
    BytesToRCSupportedFunctions.Byte18Bit05.value                = BYTE(value[18]).Bit[5]
    # Byte 18 - Bit 6
    BytesToRCSupportedFunctions.Byte18Bit06.value                = BYTE(value[18]).Bit[6]
    # Byte 18 - Bit 7
    BytesToRCSupportedFunctions.Byte18Bit07.value                = BYTE(value[18]).Bit[7]
    
    return BytesToRCSupportedFunctions

#-------------------------------------------------------------------------
# SINT_TO_BYTE - converts a SINT to BYTE
#-------------------------------------------------------------------------
def SINT_TO_BYTE(value: SINT | int) -> BYTE:
    return BYTE(int(value))

#-------------------------------------------------------------------------
# BYTE_TO_SINT - converts a BYTE to SINT
#-------------------------------------------------------------------------
def BYTE_TO_SINT(value: BYTE | int) -> SINT:

    return SINT(int(value))

#-------------------------------------------------------------------------
# DwordToRaStatusWord - convert DWORD to RaStatusWord structure
#-------------------------------------------------------------------------
def DwordToRaStatusWord(value: DWORD ) -> RaStatusWord:

    # return value of function
    DwordToRaStatusWord : RaStatusWord = RaStatusWord()

    # temporary byte value
    tmpByte : BYTE = BYTE(0)

    DwordToRaStatusWord.IsMoving.value           = value.Bit[0]
    DwordToRaStatusWord.PrimarySequencePaused.value    = value.Bit[1]
    DwordToRaStatusWord.InPrimaryPos.value             = value.Bit[2]
    DwordToRaStatusWord.SecondarySequenceActive.value  = value.Bit[3]
    DwordToRaStatusWord.IsBlending.value               = value.Bit[4]
    DwordToRaStatusWord.ErrorPending.value             = value.Bit[5]
    DwordToRaStatusWord.RestartInProgress.value        = value.Bit[6]
    DwordToRaStatusWord.Enabled.value                  = value.Bit[7]

    # convert bit for RaSequenceState    
    tmpByte.value = 0
    tmpByte.Bit[0] = value.Bit[8]
    tmpByte.Bit[1] = value.Bit[9]
    
    DwordToRaStatusWord.RaSequenceState                = RaSequenceState(tmpByte.value)
    
    # convert bit for OperationMode
    tmpByte.value = 0
    tmpByte.Bit[0] = value.Bit[10]
    tmpByte.Bit[1] = value.Bit[11]
    tmpByte.Bit[2] = value.Bit[12]
    
    try:
        DwordToRaStatusWord.OperationMode              = OperationMode(tmpByte.value)
    except Exception:
        # Fallback to a safe default when value is invalid (e.g., 0 during startup)
        DwordToRaStatusWord.OperationMode              = OperationMode.T1_LOCAL
    DwordToRaStatusWord.CollisionDetectedEnabled.value = value.Bit[13]
    DwordToRaStatusWord.CollisionDetected.value        = value.Bit[14]
    DwordToRaStatusWord.RestartRequested.value         = value.Bit[15]
    DwordToRaStatusWord.Accelerating.value             = value.Bit[16]
    DwordToRaStatusWord.Decelerating.value             = value.Bit[17]
    DwordToRaStatusWord.ConstantVelocity.value         = value.Bit[18]
    DwordToRaStatusWord.Bit19.value                    = value.Bit[19]
    DwordToRaStatusWord.Bit20.value                    = value.Bit[20]
    DwordToRaStatusWord.Bit21.value                    = value.Bit[21]
    DwordToRaStatusWord.Bit22.value                    = value.Bit[22]
    DwordToRaStatusWord.Bit23.value                    = value.Bit[23]
    DwordToRaStatusWord.Bit24.value                    = value.Bit[24]
    DwordToRaStatusWord.Bit25.value                    = value.Bit[25]
    DwordToRaStatusWord.Bit26.value                    = value.Bit[26]
    DwordToRaStatusWord.Bit27.value                    = value.Bit[27]
    DwordToRaStatusWord.Bit28.value                    = value.Bit[28]
    DwordToRaStatusWord.Bit29.value                    = value.Bit[29]
    DwordToRaStatusWord.Bit30.value                    = value.Bit[30]
    DwordToRaStatusWord.Bit31.value                    = value.Bit[31]

    return DwordToRaStatusWord

#-------------------------------------------------------------------------
# PlcOptionalCyclicToUint - convert AxesGroupParameterPlcOptionalCyclic to UINT
#-------------------------------------------------------------------------
def PlcOptionalCyclicToUint(value : AxesGroupParameterPlcOptionalCyclic) -> UINT :

    #return value of the function
    PlcOptionalCyclicToUint : UINT = UINT(0)

    PlcOptionalCyclicToUint.Bit[0]  = value.UseCallSubprogram.value
    PlcOptionalCyclicToUint.Bit[1]  = value.UseCartesianPosition.value
    PlcOptionalCyclicToUint.Bit[2]  = value.UseJointPosition.value
    PlcOptionalCyclicToUint.Bit[3]  = value.UseForce.value
    PlcOptionalCyclicToUint.Bit[4]  = value.Bit04.value
    PlcOptionalCyclicToUint.Bit[5]  = value.Bit05.value
    PlcOptionalCyclicToUint.Bit[6]  = value.Bit06.value
    PlcOptionalCyclicToUint.Bit[7]  = value.Bit07.value 
    PlcOptionalCyclicToUint.Bit[8]  = value.UseTwoSequences.value
    PlcOptionalCyclicToUint.Bit[9]  = value.UseCartesianPositionExt.value
    PlcOptionalCyclicToUint.Bit[10] = value.UseJointPositionExt.value
    PlcOptionalCyclicToUint.Bit[11] = value.Bit11.value
    PlcOptionalCyclicToUint.Bit[12] = value.Bit12.value
    PlcOptionalCyclicToUint.Bit[13] = value.Bit13.value
    PlcOptionalCyclicToUint.Bit[14] = value.Bit14.value
    PlcOptionalCyclicToUint.Bit[15] = value.Bit15.value  

    return PlcOptionalCyclicToUint


#-------------------------------------------------------------------------
# RobOptionalCyclicToUint - convert AxesGroupParameterRobOptionalCyclic to UINT
#-------------------------------------------------------------------------
def RobOptionalCyclicToUint(value : AxesGroupParameterRobOptionalCyclic) -> UINT :
    
    RobOptionalCyclicToUint : UINT = UINT(0)
    
    RobOptionalCyclicToUint.Bit[0]  = value.UseCallSubprogram.value
    RobOptionalCyclicToUint.Bit[1]  = value.UseCartesianPosition.value
    RobOptionalCyclicToUint.Bit[2]  = value.UseJointPosition.value
    RobOptionalCyclicToUint.Bit[3]  = value.UseForce.value
    RobOptionalCyclicToUint.Bit[4]  = value.UseCurrent.value
    RobOptionalCyclicToUint.Bit[5]  = value.Bit05.value
    RobOptionalCyclicToUint.Bit[6]  = value.Bit06.value
    RobOptionalCyclicToUint.Bit[7]  = value.Bit07.value
    RobOptionalCyclicToUint.Bit[8]  = value.UseTwoSequences.value
    RobOptionalCyclicToUint.Bit[9]  = value.UseCartesianPositionExt.value
    RobOptionalCyclicToUint.Bit[10] = value.UseJointPositionExt.value
    RobOptionalCyclicToUint.Bit[11] = value.UseForceExt.value
    RobOptionalCyclicToUint.Bit[12] = value.UseCurrentExt.value
    RobOptionalCyclicToUint.Bit[13] = value.Bit13.value
    RobOptionalCyclicToUint.Bit[14] = value.Bit14.value
    RobOptionalCyclicToUint.Bit[15] = value.Bit15.value

    return RobOptionalCyclicToUint


# -------------------------------------------------------------------------
# WordToArmConfigShoulder - convert WORD to ArmConfigShoulder enumeration
# -------------------------------------------------------------------------
def WordToArmConfigShoulder(value: WORD) -> ArmConfigShoulder:
    """Convert WORD to ArmConfigShoulder enumeration."""

    # return value of function
    WordToArmConfigShoulder : ArmConfigShoulder


    if ( SWAP_BYTE_ORDER):
        pass
        #value = SwapWord(value) # ToDo: Implement SwapWord function


    if ( value.Bit[0] ):
    
        WordToArmConfigShoulder = ArmConfigShoulder.BACK
    else:
        WordToArmConfigShoulder = ArmConfigShoulder.FRONT

    return WordToArmConfigShoulder


#-------------------------------------------------------------------------
# WordToArmConfigElbow - convert WORD to ArmConfigElbow enumeration
#-------------------------------------------------------------------------
def WordToArmConfigElbow(value: WORD) -> ArmConfigElbow:
    """Convert WORD to ArmConfigElbow enumeration."""
    
    # return value of function
    WordToArmConfigElbow : ArmConfigElbow


    if ( SWAP_BYTE_ORDER):
        pass
        #value = SwapWord(value) # ToDo: Implement SwapWord function
    

    if ( value.Bit[0] ):
    
        WordToArmConfigElbow = ArmConfigElbow.DOWN
    else:
        WordToArmConfigElbow = ArmConfigElbow.UP

    return WordToArmConfigElbow


#-------------------------------------------------------------------------
# WordToWordToArmConfigWrist - convert WORD to ArmConfigElbow enumeration
#-------------------------------------------------------------------------
def WordToArmConfigWrist(value: WORD) -> ArmConfigWrist:
    """Convert WORD to ArmConfigWrist enumeration."""
    
    # return value of function
    WordToArmConfigWrist : ArmConfigWrist


    if ( SWAP_BYTE_ORDER):
        pass
        #value = SwapWord(value) # ToDo: Implement SwapWord function
    

    if ( value.Bit[0] ):
    
        WordToArmConfigWrist = ArmConfigWrist.FLIP
    else:
        WordToArmConfigWrist = ArmConfigWrist.NON_FLIP

    return WordToArmConfigWrist


#-------------------------------------------------------------------------
# VersionToByte - convert VersionStruct to BYTE
#-------------------------------------------------------------------------
def VersionToByte(Value : VersionStruct) -> BYTE:

    VersionToByte : BYTE = BYTE(0)

    # Minor version  • Features
    #                • 0..31 minor versions
    VersionToByte.Bit[0] = Value.MinorVersion.Bit[0]
    VersionToByte.Bit[1] = Value.MinorVersion.Bit[1]
    VersionToByte.Bit[2] = Value.MinorVersion.Bit[2]
    VersionToByte.Bit[3] = Value.MinorVersion.Bit[3]
    VersionToByte.Bit[4] = Value.MinorVersion.Bit[4]
    # Major version  • Breaking change
    #                • 0..7 major versions
    VersionToByte.Bit[5] = Value.MajorVersion.Bit[0]
    VersionToByte.Bit[6] = Value.MajorVersion.Bit[1]
    VersionToByte.Bit[7] = Value.MajorVersion.Bit[2]

    return VersionToByte

#-------------------------------------------------------------------------
# FragmentActionToByte - convert FragmentAction to BYTE
#-------------------------------------------------------------------------
def FragmentActionToByte(Value : FragmentAction) -> BYTE:

    # return value of function
    FragmentActionToByte : BYTE = BYTE(0)

    FragmentActionToByte.Bit[0] = Value.Complete.value
    FragmentActionToByte.Bit[1] = Value.Reset.value
    FragmentActionToByte.Bit[2] = Value.Clear.value
    FragmentActionToByte.Bit[3] = Value.BIT03.value
    FragmentActionToByte.Bit[4] = Value.BIT04.value
    FragmentActionToByte.Bit[5] = Value.BIT05.value
    FragmentActionToByte.Bit[6] = Value.BIT06.value
    FragmentActionToByte.Bit[7] = Value.BIT07.value

    return FragmentActionToByte


#-------------------------------------------------------------------------
# GetHalfeByteLo - get low nibble (bits 0..3) from
#-------------------------------------------------------------------------
def GetHalfeByteLo(value: BYTE | int) -> BYTE:
    """Return low nibble (bits 0..3) of the given byte-like value as BYTE."""
    nibble = int(value) & 0x0F

    return BYTE(nibble)


#-------------------------------------------------------------------------
# GetHalfeByteHi - get high nibble (bits 4..7) from
#-------------------------------------------------------------------------
def GetHalfeByteHi(value: BYTE | int) -> BYTE:
    """Return high nibble (bits 4..7) of the given byte-like value as BYTE."""
    nibble = (int(value) >> 4) & 0x0F

    return BYTE(nibble)


#------------------------------------------------------------------------
# CombineHalfBytes - combine high nibble (bits 4..7) from
#-------------------------------------------------------------------------
def CombineHalfBytes(HalfByteHi : BYTE | USINT | SINT, HalfByteLo : BYTE| USINT | SINT) -> USINT:
    
    CombineHalfBytes : USINT = USINT(0)
    
    # merage ParSeq and Priority to combined variable
    CombineHalfBytes.Bit[0] = HalfByteLo.Bit[0]
    CombineHalfBytes.Bit[1] = HalfByteLo.Bit[1]
    CombineHalfBytes.Bit[2] = HalfByteLo.Bit[2]
    CombineHalfBytes.Bit[3] = HalfByteLo.Bit[3]

    CombineHalfBytes.Bit[4] = HalfByteHi.Bit[0]
    CombineHalfBytes.Bit[5] = HalfByteHi.Bit[1]
    CombineHalfBytes.Bit[6] = HalfByteHi.Bit[2]
    CombineHalfBytes.Bit[7] = HalfByteHi.Bit[3]

    return CombineHalfBytes


#------------------------------------------------------------------------
# CombineBytesToUint - combine two BYTES to UINT
#-------------------------------------------------------------------------
def CombineBytesToUint(ByteHi : BYTE | USINT | SINT | int, ByteLo : BYTE| USINT | SINT | int) -> UINT:
    
    # return value of the function
    CombineBytesToUint : UINT = UINT(0)
    
    if (isinstance(ByteHi, int)):
        ByteHi = BYTE(ByteHi)
    
    if (isinstance(ByteLo, int)):
        ByteLo = BYTE(ByteLo)
    
    # merage ParSeq and Priority to combined variable
    CombineBytesToUint.Bit[0]  = ByteLo.Bit[0]
    CombineBytesToUint.Bit[1]  = ByteLo.Bit[1]
    CombineBytesToUint.Bit[2]  = ByteLo.Bit[2]
    CombineBytesToUint.Bit[3]  = ByteLo.Bit[3]
    CombineBytesToUint.Bit[4]  = ByteLo.Bit[4]
    CombineBytesToUint.Bit[5]  = ByteLo.Bit[5]
    CombineBytesToUint.Bit[6]  = ByteLo.Bit[6]
    CombineBytesToUint.Bit[7]  = ByteLo.Bit[7]

    CombineBytesToUint.Bit[8]  = ByteHi.Bit[0]
    CombineBytesToUint.Bit[9]  = ByteHi.Bit[1]
    CombineBytesToUint.Bit[10] = ByteHi.Bit[2]
    CombineBytesToUint.Bit[11] = ByteHi.Bit[3]
    CombineBytesToUint.Bit[12] = ByteHi.Bit[4]
    CombineBytesToUint.Bit[13] = ByteHi.Bit[5]
    CombineBytesToUint.Bit[14] = ByteHi.Bit[6]
    CombineBytesToUint.Bit[15] = ByteHi.Bit[7]

    return CombineBytesToUint


#-------------------------------------------------------------------------
# DATE_TO_IEC_DATE - converts DATE to IEC_DATE
#-------------------------------------------------------------------------
def DATE_TO_IEC_DATE(value: DATE) -> IEC_DATE:
    """Convert DATE to IEC_DATE_TIME."""
    return value #Todo check if this is correct


#-------------------------------------------------------------------------
# TIME_TO_IEC_TIME - converts TIME to IEC_TIME
#-------------------------------------------------------------------------
def TIME_TO_IEC_TIME(value: TIME) -> IEC_TIME:
    """Convert TIME to IEC_TIME."""
    return value #Todo check if this is correct


#-------------------------------------------------------------------------
# PERCENT_UINT_TO_REAL - converts a percentage in UINT format to REAL
#-------------------------------------------------------------------------
def PERCENT_UINT_TO_REAL(Value: UINT | int, IsOptional: bool = False) -> REAL:
    """Convert a percentage in UINT format to REAL.

    IEC behavior:
    - If optional and Value equals 0xFFFF or 0xFFFFFFFF (not supported), return -1.0.
    - Otherwise divide by REAL_CONVERSION_FACTOR to get REAL.
    """

    v = int(Value)

    if (( IsOptional and v == 0xFFFFFFFF )or 
        ( IsOptional and v == 0x0000FFFF )):

        return REAL(-1.0)

    return REAL(float(v) / RobotLibraryConstants.REAL_CONVERSION_FACTOR)


#-------------------------------------------------------------------------
# REAL_TO_PERCENT_UINT - converts a percentage in REAL format to UINT
#-------------------------------------------------------------------------
def REAL_TO_PERCENT_UINT(Value: REAL | float, IsOptional: bool = False) -> UINT:
    """Convert a percentage in REAL format to UINT.

    IEC behavior:
    - If optional and Value equals -1.0, return 0xFFFF.
    - Otherwise multiply by REAL_CONVERSION_FACTOR and convert to UINT.
    """
    
    v = float(Value)

    if ( IsOptional and v == -1.0 ):
        return UINT(0x0000FFFF)

    return UINT(int(v * RobotLibraryConstants.REAL_CONVERSION_FACTOR))

#-------------------------------------------------------------------------
# SyncModesToDataEnableSync - converts SynchronizationModes to DataEnableSync
#-------------------------------------------------------------------------
def SyncModesToDataEnableSync(Value : SynchronizationModes) -> DataEnableSync :
    
    SyncModesToDataEnableSync : DataEnableSync = DataEnableSync()
    
    
    SyncModesToDataEnableSync.EnableSyncTool              = (( Value.Tool             [SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.Tool             [SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    SyncModesToDataEnableSync.EnableSyncFrame             = (( Value.Frame            [SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.Frame            [SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    SyncModesToDataEnableSync.EnableSyncLoad              = (( Value.Load             [SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.Load             [SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    SyncModesToDataEnableSync.EnableSyncWorkArea          = (( Value.WorkAreas        [SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.WorkAreas        [SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    SyncModesToDataEnableSync.EnableSyncSWLimits          = (( Value.SwLimits         [SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.SwLimits         [SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    SyncModesToDataEnableSync.EnableSyncDefaultDynamics   = (( Value.DefaultDynamics  [SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.DefaultDynamics  [SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    SyncModesToDataEnableSync.EnableSyncReferenceDynamics = (( Value.ReferenceDynamics[SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION ) or
                                                             ( Value.ReferenceDynamics[SyncTime. AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION ))
    
    return SyncModesToDataEnableSync


#-------------------------------------------------------------------------
# ByteToVersion - convert BYTE to VersionStruct
#-------------------------------------------------------------------------
def ByteToVersion(value: BYTE | int ) -> VersionStruct :

    # return value of function
    ByteToVersion : VersionStruct = VersionStruct()

    if (isinstance(value, int)):

        value = BYTE(value)

    # Minor version  • Features
    #                • 0..31 minor versions
    ByteToVersion.MinorVersion.Bit[0] = value.Bit[0]
    ByteToVersion.MinorVersion.Bit[1] = value.Bit[1]
    ByteToVersion.MinorVersion.Bit[2] = value.Bit[2]
    ByteToVersion.MinorVersion.Bit[3] = value.Bit[3]
    ByteToVersion.MinorVersion.Bit[4] = value.Bit[4]
    
    # Major version  • Breaking change
    #                • 0..7 major versions
    ByteToVersion.MajorVersion.Bit[0] = value.Bit[5]
    ByteToVersion.MajorVersion.Bit[1] = value.Bit[6]
    ByteToVersion.MajorVersion.Bit[2] = value.Bit[7]

    return ByteToVersion

#-------------------------------------------------------------------------
# IEC_TIME_TO_STRING - converts IEC_TIME to STRING
#-------------------------------------------------------------------------
def IEC_TIME_TO_STRING(value: IEC_TIME) -> str:
    """Convert IEC_TIME to STRING in format "hh:mm:ss.sss"."""
    total_milliseconds = int(value)  # Assuming IEC_TIME is in milliseconds

    hours = total_milliseconds // 3600000
    minutes = (total_milliseconds % 3600000) // 60000
    seconds = (total_milliseconds % 60000) // 1000
    milliseconds = total_milliseconds % 1000

    return str(f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}")

#-------------------------------------------------------------------------
# IEC_DATE_TO_STRING - converts IEC_DATE to STRING
#-------------------------------------------------------------------------
def IEC_DATE_TO_STRING(value: IEC_DATE) -> str:
    """Convert IEC_DATE to STRING in format "YYYY-MM-DD"."""
    # Assuming IEC_DATE is represented as the number of days since a reference date
    # For this example, let's assume the reference date is January 1, 1970
    reference_date = datetime(1970, 1, 1)
    target_date = reference_date + timedelta(days=int(value))

    return target_date.strftime("%Y-%m-%d")

#-------------------------------------------------------------------------
# IEC_TIMESTAMP_TO_SYSTEMTIME - converts IEC_TIMESTAMP to SYSTEMTIME
#-------------------------------------------------------------------------
def IEC_TIMESTAMP_TO_SYSTEMTIME(value: IEC_TIMESTAMP) -> SystemTime:
    """Convert IEC_TIMESTAMP (IEC_DATE + IEC_TIME) to SYSTEMTIME.

    IEC_TIMESTAMP holds two fields:
    - IEC_DATE: days since 1970-01-01 (alias of DATE/UINT, 2 bytes)
    - IEC_TIME: milliseconds since midnight (alias of TIME/UDINT, 4 bytes)

    SYSTEMTIME expects:
    - SystemDate: DATE (days since epoch)
    - SystemTime: TOD (milliseconds since midnight)
    """

    days_since_epoch = int(value.IEC_DATE)
    ms_since_midnight = int(value.IEC_TIME)

    return SystemTime(SystemDate=DATE(days_since_epoch), SystemTime=TOD(ms_since_midnight))


#-------------------------------------------------------------------------
# ArmConfigParameterToBytes - convert ArmConfigParameter to ARRAY[BYTE]
# -------------------------------------------------------------------------
def ArmConfigParameterToBytes(Value : ArmConfigParameter) -> ARRAY[BYTE] :
    
    ArmConfigParameterToBytes : ARRAY[BYTE] = ARRAY(0,1, BYTE)

    tmpValue : INT = INT(0)

    tmpValue = Value.Shoulder.TypeValue

    ArmConfigParameterToBytes[0].Bit[0] = tmpValue.Bit[0]
    ArmConfigParameterToBytes[0].Bit[1] = tmpValue.Bit[1]
    ArmConfigParameterToBytes[0].Bit[2] = tmpValue.Bit[2]
    ArmConfigParameterToBytes[0].Bit[3] = tmpValue.Bit[3]

    tmpValue = Value.Elbow.TypeValue

    ArmConfigParameterToBytes[0].Bit[4] = tmpValue.Bit[0]
    ArmConfigParameterToBytes[0].Bit[5] = tmpValue.Bit[1]
    ArmConfigParameterToBytes[0].Bit[6] = tmpValue.Bit[2]
    ArmConfigParameterToBytes[0].Bit[7] = tmpValue.Bit[3]

    tmpValue = Value.Wrist.TypeValue

    ArmConfigParameterToBytes[1].Bit[0] = tmpValue.Bit[0]
    ArmConfigParameterToBytes[1].Bit[1] = tmpValue.Bit[1]
    ArmConfigParameterToBytes[1].Bit[2] = tmpValue.Bit[2]
    ArmConfigParameterToBytes[1].Bit[3] = tmpValue.Bit[3]
    
    ArmConfigParameterToBytes[1].Bit[4] = False
    ArmConfigParameterToBytes[1].Bit[5] = False
    ArmConfigParameterToBytes[1].Bit[6] = False
    ArmConfigParameterToBytes[1].Bit[7] = False

    return ArmConfigParameterToBytes