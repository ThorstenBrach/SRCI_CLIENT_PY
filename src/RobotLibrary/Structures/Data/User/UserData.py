"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      UserData
Author:      Thorsten Brach
Date:        2025-12-18

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import BOOL, UINT, USINT, TIME, REAL, STRING, IEC_Struct
from RobotLibrary.Enumerations.Level.LogLevel import LogLevel
from RobotLibrary.Enumerations.Level.MessageLevel import MessageLevel
from RobotLibrary.Enumerations.Mode.OperationMode import OperationMode
from RobotLibrary.Structures.Axis.AxisJointUsed import AxisJointUsed
from RobotLibrary.Structures.Axis.AxisExternalUsed import AxisExternalUsed
from RobotLibrary.Structures.Axis.AxisJointUnit import AxisJointUnit
from RobotLibrary.Structures.Axis.AxisExternalUnit import AxisExternalUnit
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPositionShort, RobotJointPositionExt
from RobotLibrary.Structures.Miscellaneous.DataEnableSync import DataEnableSync
from RobotLibrary.Structures.Miscellaneous.VersionStruct import VersionStruct
from RobotLibrary.Structures.Miscellaneous.RCSupportedFunctions import RCSupportedFunctions
from RobotLibrary.Structures.Miscellaneous.SynchronizationModes import SynchronizationModes
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPositionShort, RobotCartesianPositionExt
    
class UserData(IEC_Struct):
  
  """
  state of the synchronizationrelated comparison mechanism 
  """
  EnableSync : DataEnableSync

  """
  TRUE if two sequences in one Telegram are active
  """
  ActivateTwoSequences : bool

  """
  Synchronisation modes  
  """
  SynchronizationModes : SynchronizationModes  

  """
  Defines waiting time [ms] of RC between receiving a first move command when motion queue is empty and starting the first movement. See also chapter 5.6.8.
  """
  DelayTime : int 

  """
  Define number of points required to calculate the blending. See also chapter 5.6.8
  """
  WaitForNrOfCmd : int

  """
  Defines blending behavior for single move commands
   • 0 (default): Move to end position :
       Robot moves exactly the target position independently of the selected "BlendingMode"
   
   • 1: Wait at blending parameter : 
        Robot stops its movement when the specified blending parameter is reached
  """
  WaitAtBlendingZone : bool

  """ 
  Allow a sequence switch from primary to secondary while a subprogram called via CallSubprogram (6.5.18) in the sequence is in progress
  """
  AllowSecSeqWhileSubprogram : bool

  """
  Allows blending when CallSubprogram is called in sequence and removed afterwards.
  For more information see chapter 6.5.21.
   • 0 (default): Dynamic blending is prevented
   • 1: Dynamic blending is allowed
  """
  AllowDynamicBlending : bool

  """
  Maximum allowed time [ms] between incrementation of LifeSign before communication error.
   • <10 ms: Invalid
   • 50 ms: default
  See also chapter 5.6.6.2.
  """
  LifeSignTimeOut : int

  """
  Specifies system reaction in case inconsistency of synchronization data is detected according to Table 6-81. For more information refer to chapter 5.6.7.2
  """
  SyncReaction : int

  """ 
  Defines a delay time [ms] between detecting an inconsistency of configuration data between server and client an executing the defined SyncReaction.
  Always positive.
   • Default: 0 ms
  """
  SyncDelay : int

  """ 
  Defines up to which level of severity messages will be logged in the RC's server log
  """
  LogLevel : LogLevel

  """
  Defines up to which level of severity messages will be transmitted to the PLC's message buffer
  """
  MessageLevel : MessageLevel

  """
  Manufactured ID
  """
  PLCManufacturedID : int

  """
  Order ID
  """
  PLCOrderID : str

  """
  Serial Number
  """
  PLCSerialNumber : str

  """
  Firmware Version
  """
  PLCFirmwareVersion : str

  """
  Client Interface Version
  """
  PLCInterfaceVersion : str

  """
  Version of client implementation in format (X.X.X)
  """
  PLCLibraryVersion : VersionStruct

  """
  RC manufacturer name 
  """
  RCManufacturer : str

  """
  RC part number 
  """
  RCOrderID : str

  """
  RC serial number 
  """
  RCSerialNumber : str

  """
  RA serial number 
  """
  RASerialNumber : str

  """
  Robot firmware version in manufacturer-specific format 
  """
  RCFirmwareVersion : str

  """
  Version of server implementation in format (X.X.X) 
  """
  RCInterpreterVersion : VersionStruct

  """
  Version of SRCI specification on which server implementation is based in format (X.X.X)  
  """
  RCSRCIVersion : VersionStruct

  """
  TRUE  = Axis used in Robot, FALSE = Axis NOT used. See Table 6-13 for bit assignment.
  """
  AxisJointUsed : AxisJointUsed

  """
  TRUE = Axis used by Robot, FALSE = Axis NOT used. See Table 6-13 for bit assignment.
  """
  AxisExternalUsed : AxisExternalUsed

  """
  TRUE = mm, FALSE = °. See Table 6-13 for bit assignment.
  """
  AxisJointUnit : AxisJointUnit

  """
  TRUE = mm, FALSE = °. See Table 6-13 for bit assignment.
  """
  AxisExternalUnit : AxisExternalUnit

  """
  Interface is initialized and ready to process commands.
  """
  Initialized : bool

  """
  All synchronization-related configuration data between client and server is synchronized.
  """
  Synchronized : bool

  """
  ToolData synchronization is activated.
  """
  ToolDataSynchronizing : bool

  """
  FrameData synchronization is activated.
  """
  FrameDataSynchronizing : bool

  """
  LoadData synchronization is activated.
  """
  LoadDataSynchronizing : bool

  """
  WorkAreaData synchronization is activated.
  """
  WorkAreaDataSynchronizing : bool

  """
  SWLimits synchronization is activated.
  """
  SWLimitsSynchronizing : bool

  """
  DefaultDynamics synchronization is activated.
  """
  DefaultDynamicsSynchronizing : bool

  """
  ReferenceDynamics synchronization is activated.
  """
  ReferenceDynamicsSynchronizing : bool
  
  """
  TRUE, when robot's axes values change due to physical movement of axes. Can only be TRUE in sequence state "Executing". Default: FALSE 
  """
  IsMoving : bool

  """
  TRUE, when move commands buffered by the primary sequence are currently not processed. Default: FALSE 
  """
  PrimarySequencePaused : bool

  """
  TRUE, when robot is moving in the primary sequence. FALSE, when robot leaves its position by other means than move commands in the primary sequence. Default: FALSE
  """
  InPrimaryPos : bool

  """
  TRUE, when secondary sequence is active. Default: FALSE
  """
  SecondarySequenceActive : bool

  """
  Shows that an error acknowledgement by the client is necessary. Default: FALSE
  """
  ErrorPending : bool

  """
  TRUE, when RC is restarting. Default: FALSE
  """
  RestartInProgress : bool

  """
  Signals that a brake test is required in the defined monitoring time (see chapter 6.5.27).
  """
  BrakeTestRequired : bool

  """
  RA power state. Default: FALSE
  """
  Enabled : bool

  """
  TRUE, while RA sequence states returns Idle. Default: FALSE
  """
  Idle : bool

  """
  TRUE, while RA sequence states returns Executing. Default: FALSE
  """
  Executing : bool

  """
  TRUE, while RA sequence states returns Interrupted. Default: FALSE
  """
  Interrupted : bool

  """
  TRUE, when robot is currently blending between to move commands. Can only be TRUE in sequence state "Executing". Default: FALSE
  """
  IsBlending : bool  

  """
  Operation Mode (see chapter 5.5.1)
  """
  OperationMode : OperationMode

  """
  PathAccuracyMode is active (see chapter 6.5.22) 
  """
  PathAccuracyMode : bool

  """
  AvoidSingularity is active (see chapter 6.5.23) 
  """
  AvoidSingularity : bool

  """
  TRUE, while CollisionDetection is enabled (see chapter 6.5.35) Default: FALSE 
  """
  CollisionDetectionEnabled : bool

  """
  TRUE, when a collision was detected while CollisionDetection is enabled (see chapter 6.5.35) Default: FALSE 
  """
  CollisionDetected : bool

  """
  TRUE, when the RC requests a restart of the RC induced through the functions "WriteRobotSWLimits" (chapter 6.2.16) or "WriteSystemVariable" (chapter 6.5.8) Default: FALSE 
  """
  RestartRequested : bool

  """
  Actual override
  """
  ActualOverride : float

  """
  StepMode is active and set to ExactStop (see chapter 6.1.3) 
  """
  StepModeExactStopActive : bool

  """
  StepMode is active and set to Blending (see chapter 6.1.3) 
  """
  StepModeBlendingActive : bool

  """
  Cyclic dynamics status bit Accelerating is supported by RC (see chapter 5.5.3.2) 
  """
  AcceleratingSupported : bool

  """
  TRUE, when the robot is currently accelerating Default: FALSE 
  """
  Accelerating : bool

  """
  Cyclic dynamics status bit Decelerating is supported by RC (see chapter 5.5.3.2) 
  """
  DeceleratingSupported : bool

  """
  TRUE, when the robot is currently decelerating Default: FALSE 
  """
  Decelerating : bool

  """
  Cyclic dynamics status bit ConstantVelocity is supported by RC (see chapter 5.5.3.2) 
  """
  ConstantVelocitySupported : bool

  """
  TRUE, while the robot velocity is constant Default: FALSE 
  """
  ConstantVelocity : bool

  """
  TRUE, while the CartesianPosition is returned cyclically 
  """
  ReadingCartesianPosition : bool

  """
  TRUE, while the ExtCartesianPosition is returned cyclically 
  """
  ReadingExtCartesianPosition : bool

  """
  TRUE, while the JointPosition is returned cyclically 
  """
  ReadingJointPosition : bool

  """
  TRUE, while the ExtJointPosition is returned cyclically 
  """
  ReadingExtJointPosition : bool

  """
  Cyclically returned, absolute coordinates of current position in selected coordinate systems (see input parameters ToolNo and FrameNo of function ReadActualPositionCyclic 6.1.6)
  """
  CartesianPosition : RobotCartesianPositionShort

  """
  Cyclically returned, absolute cartesian position of the external axes of the robot in selected coordinate systems (see input parameters ToolNo and FrameNo of function ReadActualPositionCyclic 6.1.6)
  """
  ExtCartesianPosition : RobotCartesianPositionExt  

  """
  Cyclically returned, absolute position of the robot in Joint position
  """
  JointPosition : RobotJointPositionShort

  """
  Cyclically returned, absolute joint position of the external axes of the robot
  """
  ExtJointPosition : RobotJointPositionExt 

  """
  TRUE: Function is supported by RC
  FALSE: Function is not supported by RC
  See Table 6-14 for bit assignment.
  """
  RCSupportedFunctions : RCSupportedFunctions
