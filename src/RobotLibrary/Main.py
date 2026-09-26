"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibrary Main POU
Author:      Thorsten Brach
Date:        2026-01-22

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

#region 
import socket

from RobotLibrary.Interfaces.IMessageLogger import IMessageLogger  #noqa: F401
from RobotLibrary.Parameter import SYSTEM_LOG_MAX, MESSAGE_LOG_MAX, MESSAGE_TEXT_LEN
from RobotLibrary.IEC_Types import IEC_String, BOOL,INT, DWORD ,DINT, REAL, IEC_POU, BYTE, STRING, WORD, UINT, UDINT, IEC_Struct, ARRAY  #noqa: F401
from RobotLibrary.IEC_Scheduler import Scheduler, Task, TaskPriority, WatchdogAction  #noqa: F401
from RobotLibrary.POUs.General.MC_RobotTask.MC_RobotTaskFB import MC_RobotTaskFB  #noqa: F401
from RobotLibrary.POUs.General.MC_EnableRobot.MC_EnableRobotFB import MC_EnableRobotFB
from RobotLibrary.POUs.General.MC_GroupReset.MC_GroupResetFB import MC_GroupResetFB
from RobotLibrary.POUs.BasicMove.MC_GroupJog.MC_GroupJogFB import MC_GroupJogFB  #noqa: F401
from RobotLibrary.POUs.BasicMove.MC_GroupStop.MC_GroupStopFB import MC_GroupStopFB  #noqa: F401
from RobotLibrary.POUs.BasicMove.MC_GroupInterrupt.MC_GroupInterruptFB import MC_GroupInterruptFB  #noqa: F401
from RobotLibrary.POUs.BasicMove.MC_GroupContinue.MC_GroupContinueFB import MC_GroupContinueFB  #noqa: F401
from RobotLibrary.POUs.BasicMove.MC_ChangeSpeedOverride.MC_ChangeSpeedOverrideFB import MC_ChangeSpeedOverrideFB  #noqa: F401
from RobotLibrary.POUs.BasicMove.MC_MoveAxesAbsolute.MC_MoveAxesAbsoluteFB import MC_MoveAxesAbsoluteFB
from RobotLibrary.POUs.BasicMove.MC_MoveDirectAbsolute.MC_MoveDirectAbsoluteFB import MC_MoveDirectAbsoluteFB
from RobotLibrary.POUs.Read.MC_ReadActualPosition.MC_ReadActualPositionFB import MC_ReadActualPositionFB  #noqa: F401

from RobotLibrary.Enumerations.Miscellaneous.SyncTime import SyncTime
from RobotLibrary.Enumerations.Mode.SyncMode import SyncMode
from RobotLibrary.Enumerations.Type.MessageType import MessageType  #noqa: F401
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity  #noqa: F401
from RobotLibrary.Enumerations.Miscellaneous.SyncReaction import SyncReaction
from RobotLibrary.Enumerations.Level.MessageLevel import MessageLevelEnum
from RobotLibrary.Enumerations.Mode.StepMode import StepMode
from RobotLibrary.Enumerations.Mode.TurnMode import TurnMode
from RobotLibrary.Enumerations.Mode.BlendingMode import BlendingMode
from RobotLibrary.Enumerations.ArmConfig.ArmConfigShoulder import ArmConfigShoulder
from RobotLibrary.Enumerations.ArmConfig.ArmConfigElbow import ArmConfigElbow
from RobotLibrary.Enumerations.ArmConfig.ArmConfigWrist import ArmConfigWrist

from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime  #noqa: F401
from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage  #noqa: F401
from RobotLibrary.Structures.Data.Tool.Tool import Tool
from RobotLibrary.Structures.Data.Load.Load import Load
from RobotLibrary.Structures.Data.Frame.Frame import Frame
from RobotLibrary.Structures.Data.WorkArea.RobotWorkArea import RobotWorkArea
from RobotLibrary.Structures.Data.User.UserData import UserData as UserDataStruct
from RobotLibrary.Structures.Miscellaneous.SWLimits import  SWLimits as SWLimitsStruct
from RobotLibrary.Structures.Dynamics.DefaultDynamics import  DefaultDynamics as DefaultDynamicsStruct
from RobotLibrary.Structures.Dynamics.ReferenceDynamics import  ReferenceDynamics as ReferenceDynamicsStruct
#endregion

RobotInData       = bytearray(256)
RobotOutData      = bytearray(256)
HOST = "192.168.2.10"
PORT = 54600


class Main(IEC_POU):
    """ Main Class of the Robot Application"""
    
    #region variables
    RobotInData       = bytearray(256)
    RobotOutData      = bytearray(256)
    SystemLog         : ARRAY[STRING] = ARRAY(0, SYSTEM_LOG_MAX, STRING(MESSAGE_TEXT_LEN))
    MessageLog        : ARRAY[AlarmMessage] = ARRAY (0, MESSAGE_LOG_MAX,  AlarmMessage) 
    #endregion


    #------------------------------------------------------------
    # Constructor
    #------------------------------------------------------------
    def __init__(self, ) -> None:

        # call base implementation
        super().__init__()

        # init data structures
        self.AxesGroup         = AxesGroup()
        self.UserData          = UserDataStruct()
        self.ToolData          = [Tool ()         for _ in range(0, 15)]
        self.FrameData         = [Frame()         for _ in range(0, 15)]
        self.LoadData          = [Load ()         for _ in range(0, 15)]
        self.WorkAreas         = [RobotWorkArea() for _ in range(0, 15)]
        self.SWLimits          = SWLimitsStruct()
        self.DefaultDynamics   = DefaultDynamicsStruct()
        self.ReferenceDynamics = ReferenceDynamicsStruct()

        # init function blocks
        self.RobotTask           = MC_RobotTaskFB()
        self.GroupReset          = MC_GroupResetFB()
        self.EnableRobot         = MC_EnableRobotFB()
        self.GroupReset          = MC_GroupResetFB()
        self.GroupJog            = MC_GroupJogFB()
        self.GroupStop           = MC_GroupStopFB()
        self.GroupInterrupt      = MC_GroupInterruptFB()
        self.GroupContinue       = MC_GroupContinueFB()
        self.ChangeSpeedOverride = MC_ChangeSpeedOverrideFB()
        self.MoveAxesAbsolute    = MC_MoveAxesAbsoluteFB()
        self.MoveDirectAbsolute  = MC_MoveDirectAbsoluteFB()
        self.ReadActualPosition  = MC_ReadActualPositionFB()
        
        # internal variables
        self.stepCmd = 0

        # apply configuration parameters
        self.ApplyConfigurationParameters()


    #------------------------------------------------------------
    # Apply configuration parameters
    #------------------------------------------------------------
    def ApplyConfigurationParameters(self) -> None :
        """ Apply configuration parameters to RobotTask FB """

        #region Apply configuration parameters to RobotTask FB
        
        # Communication Parameters
        self.RobotTask.ParCfg.Com.LifeSignTimeOut                               = 100 #ms
        self.RobotTask.ParCfg.Com.TelegramLengthPlcToRob                        = 256
        self.RobotTask.ParCfg.Com.TelegramLengthRobToPlc                        = 256
        
        # PLC Parameters        
        self.RobotTask.ParCfg.Plc.CycleTime                                     = 10 #ms
        self.RobotTask.ParCfg.Plc.Parameter.ManufacturedID                      = UINT(99)
        self.RobotTask.ParCfg.Plc.Parameter.OrderID                             = '12345678901234567890'
        self.RobotTask.ParCfg.Plc.Parameter.SerialNumber                        = '1234567890123456'
        self.RobotTask.ParCfg.Plc.Parameter.FirmwareVersion                     = '12345678'
        self.RobotTask.ParCfg.Plc.Parameter.InterfaceVersion                    = '1.5'

        # PLC Synchronization Modes
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.Tool              [SyncTime.DURING_START_UP] = SyncMode.SERVER_TO_CLIENT
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.Tool              [SyncTime. AFTER_START_UP] = SyncMode.AUTOMATIC
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.Frame             [SyncTime.DURING_START_UP] = SyncMode.SERVER_TO_CLIENT
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.Frame             [SyncTime. AFTER_START_UP] = SyncMode.AUTOMATIC
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.Load              [SyncTime.DURING_START_UP] = SyncMode.SERVER_TO_CLIENT
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.Load              [SyncTime. AFTER_START_UP] = SyncMode.AUTOMATIC
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas         [SyncTime.DURING_START_UP] = SyncMode.NO_SYNCHRONIZATION # not yet supported by stäubli 
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas         [SyncTime. AFTER_START_UP] = SyncMode.NO_SYNCHRONIZATION # not yet supported by stäubli
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits          [SyncTime.DURING_START_UP] = SyncMode.SERVER_TO_CLIENT
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits          [SyncTime. AFTER_START_UP] = SyncMode.AUTOMATIC
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics   [SyncTime.DURING_START_UP] = SyncMode.SERVER_TO_CLIENT
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics   [SyncTime. AFTER_START_UP] = SyncMode.AUTOMATIC
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics [SyncTime.DURING_START_UP] = SyncMode.SERVER_TO_CLIENT
        self.RobotTask.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics [SyncTime. AFTER_START_UP] = SyncMode.AUTOMATIC

        # PLC Optional Cyclic Data
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseCallSubprogram.value        = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseCartesianPosition.value     = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseJointPosition.value         = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseForce.value                 = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit04.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit05.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit06.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit07.value                    = False  
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseTwoSequences.value          = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseCartesianPositionExt.value  = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.UseJointPositionExt.value      = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit11.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit12.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit13.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit14.value                    = False
        self.RobotTask.ParCfg.Plc.OptionalCyclic.Bit15.value                    = False  

        # Robot Parameters
        self.RobotTask.ParCfg.Rob.Parameter.WaitAtBlendingZone                  = True # must be True for Stäubli
        self.RobotTask.ParCfg.Rob.Parameter.AllowSecSeqWhileSubprogram          = False
        self.RobotTask.ParCfg.Rob.Parameter.AllowDynamicBlending                = False
        self.RobotTask.ParCfg.Rob.Parameter.DelayTime                           = 0
        self.RobotTask.ParCfg.Rob.Parameter.WaitForNrOfCmd                      = 1
        self.RobotTask.ParCfg.Rob.Parameter.SyncDelay                           = 0
        self.RobotTask.ParCfg.Rob.Parameter.SyncReaction                        = SyncReaction.NO_REACTION
        self.RobotTask.ParCfg.Rob.Parameter.MessageLevel                        = MessageLevelEnum.WARNING

        # Robot Optional Cyclic Data
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseCallSubprogram.value        = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseCartesianPosition.value     = True
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseJointPosition.value         = True
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseForce.value                 = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseCurrent.value               = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.Bit05.value                    = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.Bit06.value                    = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.Bit07.value                    = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseTwoSequences.value          = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseCartesianPositionExt.value  = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseJointPositionExt.value      = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseForceExt.value              = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.UseCurrentExt.value            = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.Bit13.value                    = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.Bit14.value                    = False
        self.RobotTask.ParCfg.Rob.OptionalCyclic.Bit15.value                    = False

        # endregion



    #--------------------------------------------------------
    # Cyclic call ( called from the scheduler )
    #--------------------------------------------------------
    def on_call(self):

        # call robot task
        self.RobotTask( 
            RobotName         = 'Stäubli CS9',
            AxesGroupID       = 0,
            OnlineChange      = False,
            RobotInData       = self.RobotInData,
            RobotOutData      = self.RobotOutData,
            UserData          = self.UserData,
            AxesGroup         = self.AxesGroup,
            ToolData          = self.ToolData,
            FrameData         = self.FrameData,
            LoadData          = self.LoadData,
            WorkAreas         = self.WorkAreas,
            SWLimits          = self.SWLimits,
            DefaultDynamics   = self.DefaultDynamics,
            ReferenceDynamics = self.ReferenceDynamics,
            SystemLog         = self.SystemLog,
            MessageLog        = self.MessageLog
        )

        # call GroupReset FB
        self.GroupReset( 
            Name              = 'GroupReset',
            ExecMode          = self.GroupReset.ExecMode,
            Priority          = self.GroupReset.Priority,
            AxesGroup         = self.AxesGroup)

        # call GroupStop FB
        self.GroupStop( 
            Name              = 'GroupStop',
            ExecMode          = self.GroupStop.ExecMode,
            Priority          = self.GroupStop.Priority,
            AxesGroup         = self.AxesGroup)

        # call GroupInterrupt FB
        self.GroupInterrupt( 
            Name              = 'GroupInterrupt',
            ExecMode          = self.GroupInterrupt.ExecMode,
            Priority          = self.GroupInterrupt.Priority,
            AxesGroup         = self.AxesGroup)

        # call GroupContinue FB
        self.GroupContinue( 
            Name              = 'GroupContinue',
            ExecMode          = self.GroupContinue.ExecMode,
            Priority          = self.GroupContinue.Priority,
            AxesGroup         = self.AxesGroup)

        # call EnableRobot FB
        self.EnableRobot(  
            Name             = 'EnableRobot',
            ExecMode         = self.EnableRobot.ExecMode,
            Priority         = self.EnableRobot.Priority,
            AxesGroup        = self.AxesGroup
        )
        
        # call ChangeSpeedOverrideFB
        self.ChangeSpeedOverride(
            Name             = 'ChangeSpeedOverride',
            ExecMode         = self.ChangeSpeedOverride.ExecMode,
            Priority         = self.ChangeSpeedOverride.Priority,
            AxesGroup        = self.AxesGroup
        )
        
        # call MoveAxesAbsoluteFB
        self.MoveAxesAbsolute(
            Name             ='MoveAxesAbsolute',
            ExecMode         = self.MoveAxesAbsolute.ExecMode,
            Priority         = self.MoveAxesAbsolute.Priority,
            AxesGroup        = self.AxesGroup
        )

        # call MoveDirectAbsoluteFB
        self.MoveDirectAbsolute(
            Name             ='MoveDirectAbsolute',
            ExecMode         = self.MoveDirectAbsolute.ExecMode,
            Priority         = self.MoveDirectAbsolute.Priority,
            AxesGroup        = self.AxesGroup
        )

        # call ReadActualPositionFB
        self.ReadActualPosition(
            Name             = 'ReadActualPosition',
            ExecMode         = self.ReadActualPosition.ExecMode,
            Priority         = self.ReadActualPosition.Priority,
            AxesGroup        = self.AxesGroup
        )


    #--------------------------------------------------------
    # Execute Robot example sequence
    #--------------------------------------------------------
    def ExecuteExample (self) -> None :
        
        match self.stepCmd:
            
            case 0:

                # Check RobotTaskFB ready ?
                if (( not self.RobotTask.Busy  ) and
                    ( not self.RobotTask.Error )) :

                    # enable robot task
                    self.RobotTask.Enable = True
                    # increase step counter
                    self.stepCmd += 1

            case 1:

                # Wait RobotTask done ? 
                if ((( not self.RobotTask.Busy         )  and
                     ( not self.RobotTask.Error        )) and
                    ((     self.RobotTask.Initialized  )  or
                     (     self.RobotTask.Synchronized ))) :

                    # increase step counter
                    self.stepCmd += 1

            case 2:

                # Check GroupReset ready ?
                if (( not self.GroupReset.Busy  ) and
                    ( not self.GroupReset.Error )) :

                    # Reset pending errors 
                    self.GroupReset.Execute = True
                    # increase step counter
                    self.stepCmd += 1

            case 3:

                # Wait GroupReset done ?
                if (( not self.GroupReset.Busy    ) and
                    ( not self.GroupReset.Error   ) and
                    (     self.GroupReset.Done )) :

                    # Reset group reset command
                    self.GroupReset.Execute = False
                    # increase step counter
                    self.stepCmd += 1

            case 4:

                # Check EnableRobotFB ready ?
                if (( not self.EnableRobot.Busy  ) and
                    ( not self.EnableRobot.Error )) :

                    # set command parameters
                    self.EnableRobot.ParCmd.HoldToRun  = False 
                    self.EnableRobot.ParCmd.ManualStep = False
                    self.EnableRobot.ParCmd.StepMode   = StepMode.EXACT_STOP

                    # enable robot
                    self.EnableRobot.Enable = True
                    # increase step counter
                    self.stepCmd += 1

            case 5:

                # Wait EnableRobot done ?
                if (( not self.EnableRobot.Busy    ) and
                    ( not self.EnableRobot.Error   ) and
                    (     self.EnableRobot.Enabled )) :

                    # increase step counter
                    self.stepCmd += 1
                    
            case 6:

                # Check ChangeSpeedOverrideFB ready ?
                if (( not self.ChangeSpeedOverride.Busy  ) and
                    ( not self.ChangeSpeedOverride.Error )) :

                    # set command parameters
                    self.ChangeSpeedOverride.ParCmd.Override = 50

                    # enable robot
                    self.ChangeSpeedOverride.Execute = True
                    # increase step counter
                    self.stepCmd += 1

            case 7:

                # Wait ChangeSpeedOverride done ?
                if (( not self.ChangeSpeedOverride.Busy  ) and
                    ( not self.ChangeSpeedOverride.Error ) and
                    (     self.ChangeSpeedOverride.Done  )) :

                    # Reset change speed override command
                    self.ChangeSpeedOverride.Execute = False
                    # increase step counter
                    self.stepCmd += 1

            case 8:
                
                # Check MoveAxesAbsoluteFB ready ?
                if (( not self.MoveAxesAbsolute.Busy  ) and
                    ( not self.MoveAxesAbsolute.Error )) :

                    # set command parameters
                    self.MoveAxesAbsolute.ParCmd.JointPosition.J1     = 90.0
                    self.MoveAxesAbsolute.ParCmd.JointPosition.J2     = 45.0
                    self.MoveAxesAbsolute.ParCmd.JointPosition.J3     = 30.0
                    self.MoveAxesAbsolute.ParCmd.JointPosition.J4     = 0.0
                    self.MoveAxesAbsolute.ParCmd.JointPosition.J5     = 90.0
                    self.MoveAxesAbsolute.ParCmd.JointPosition.J6     = 0.0
                    self.MoveAxesAbsolute.ParCmd.VelocityRate         = 100.0
                    self.MoveAxesAbsolute.ParCmd.AccelerationRate     = 100.0 
                    self.MoveAxesAbsolute.ParCmd.DecelerationRate     = 100.0
                    self.MoveAxesAbsolute.ParCmd.JerkRate             = 100.0
                    self.MoveAxesAbsolute.ParCmd.ToolNo               = 0
                    self.MoveAxesAbsolute.ParCmd.BlendingMode         = BlendingMode.EXACT_STOP
                    self.MoveAxesAbsolute.ParCmd.BlendingParameter[0] = 10
                    self.MoveAxesAbsolute.ParCmd.BlendingParameter[1] = 10
                    self.MoveAxesAbsolute.ParCmd.MoveTime             = 0 # ms
                    self.MoveAxesAbsolute.ParCmd.ConfigMode.Shoulder  = ArmConfigShoulder.SAME
                    self.MoveAxesAbsolute.ParCmd.ConfigMode.Elbow     = ArmConfigElbow.SAME
                    self.MoveAxesAbsolute.ParCmd.ConfigMode.Wrist     = ArmConfigWrist.SAME
                    self.MoveAxesAbsolute.ParCmd.Manipulation         = True
                    self.MoveAxesAbsolute.ParCmd.EmitterID[0]         = 0
                    self.MoveAxesAbsolute.ParCmd.EmitterID[1]         = 0
                    self.MoveAxesAbsolute.ParCmd.EmitterID[2]         = 0
                    self.MoveAxesAbsolute.ParCmd.EmitterID[3]         = 0

                    # execute move axes absolute command
                    self.MoveAxesAbsolute.Execute = True
                    # increase step counter
                    self.stepCmd += 1

            case 9:

                # Wait MoveAxesAbsoluteFB buffered ?
                if (( not self.MoveAxesAbsolute.Busy            ) and
                    ( not self.MoveAxesAbsolute.Error           ) and
                    (     self.MoveAxesAbsolute.CommandBuffered )) :

                    # Reset move axes absolute command
                    self.MoveAxesAbsolute.Execute = False
                    # increase step counter
                    self.stepCmd += 1



            case 10:

                # Check MoveDirectAbsoluteFB ready ?
                if (( not self.MoveDirectAbsolute.Busy  ) and
                    ( not self.MoveDirectAbsolute.Error )) :

                    # set command parameters
                    self.MoveDirectAbsolute.ParCmd.Position.X                = 200.0
                    self.MoveDirectAbsolute.ParCmd.Position.Y                = 300.0
                    self.MoveDirectAbsolute.ParCmd.Position.Z                = 150.0
                    self.MoveDirectAbsolute.ParCmd.Position.Rx               = 0.0
                    self.MoveDirectAbsolute.ParCmd.Position.Ry               = 0.0
                    self.MoveDirectAbsolute.ParCmd.Position.Rz               = 0.0
                    self.MoveDirectAbsolute.ParCmd.Position.Config.Shoulder  = ArmConfigShoulder.FRONT
                    self.MoveDirectAbsolute.ParCmd.Position.Config.Elbow     = ArmConfigElbow.UP
                    self.MoveDirectAbsolute.ParCmd.Position.Config.Wrist     = ArmConfigWrist.NON_FLIP
                    self.MoveDirectAbsolute.ParCmd.VelocityRate              = 100.0
                    self.MoveDirectAbsolute.ParCmd.AccelerationRate          = 100.0 
                    self.MoveDirectAbsolute.ParCmd.DecelerationRate          = 100.0
                    self.MoveDirectAbsolute.ParCmd.JerkRate                  = 100.0
                    self.MoveDirectAbsolute.ParCmd.ToolNo                    = 0
                    self.MoveDirectAbsolute.ParCmd.FrameNo                   = 0
                    self.MoveDirectAbsolute.ParCmd.BlendingMode              = BlendingMode.EXACT_STOP
                    self.MoveDirectAbsolute.ParCmd.BlendingParameter[0]      = 10
                    self.MoveDirectAbsolute.ParCmd.BlendingParameter[1]      = 10
                    self.MoveDirectAbsolute.ParCmd.MoveTime                  = 0 # ms
                    self.MoveDirectAbsolute.ParCmd.ConfigMode.Shoulder       = ArmConfigShoulder.SAME
                    self.MoveDirectAbsolute.ParCmd.ConfigMode.Elbow          = ArmConfigElbow.SAME
                    self.MoveDirectAbsolute.ParCmd.ConfigMode.Wrist          = ArmConfigWrist.SAME
                    self.MoveDirectAbsolute.ParCmd.TurnMode                  = TurnMode.SAME
                    self.MoveDirectAbsolute.ParCmd.Manipulation              = True
                    self.MoveDirectAbsolute.ParCmd.EmitterID[0]              = 0
                    self.MoveDirectAbsolute.ParCmd.EmitterID[1]              = 0
                    self.MoveDirectAbsolute.ParCmd.EmitterID[2]              = 0
                    self.MoveDirectAbsolute.ParCmd.EmitterID[3]              = 0

                    # execute move axes absolute command
                    self.MoveDirectAbsolute.Execute = True
                    # increase step counter
                    self.stepCmd += 1

            case 11:

                # Wait MoveDirectAbsoluteFB buffered ?
                if (( not self.MoveDirectAbsolute.Busy            ) and
                    ( not self.MoveDirectAbsolute.Error           ) and
                    (     self.MoveDirectAbsolute.CommandBuffered )) :

                    # Reset move direct absolute command
                    self.MoveDirectAbsolute.Execute = False
                    # increase step counter
                    self.stepCmd += 1


class Com(IEC_POU):
    
    #--------------------------------------------------------
    # Cyclic call ( called from the scheduler )
    #--------------------------------------------------------
    def on_call(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Client:
            Client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            Client.connect((HOST, PORT))
            print(f"Client connected to {HOST}:{PORT}")
            try:
                while True:
                    
                    Client.sendall(RobotOutData)

                    RobotInData.clear()
                    
                    while len(RobotInData) < 256:
                        chunk = Client.recv(256 - len(RobotInData))
                        if not chunk:
                            raise ConnectionError("socket closed during recv")
                        
                        RobotInData.extend(chunk)
                        
            except KeyboardInterrupt:
                    print("Interrupt acknowledged by server.")


#------------------------------------------------------------
# Task Scheduling
#------------------------------------------------------------

# create Task
TaskMain = Main()
TaskCom = Com()

# create scheduler
scheduler = Scheduler()

# add task
scheduler.add_task(Task(name                 = "Main",
                        function             = TaskMain.on_call,
                        interval_ms          = 10, 
                        priority             = TaskPriority.HIGH,
                        cpu_affinity         = None, # None = All CPUs, Usage: [1,2,3,...] for specific CPUs
                        watchdog_ms          = 30,
                        watchdog_action      = WatchdogAction.NONE,
                        watchdog_sensitivity = 3,
                        autostart            = False)
)


# add task
scheduler.add_task(Task(name                 = "Com",
                        function             = TaskCom.on_call,
                        interval_ms          = 8, 
                        priority             = TaskPriority.HIGH,
                        cpu_affinity         = None, # None = All CPUs, Usage: [1,2,3,...] for specific CPUs
                        watchdog_ms          = 30,
                        watchdog_action      = WatchdogAction.NONE,
                        watchdog_sensitivity = 3,
                        autostart            = False)
)


# start tasks
scheduler.start_all()


























while True:
   pass
#  time.sleep(1.0)

# stop tasks
scheduler.stop_all()