"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      CmdType
Author:      Thorsten Brach
Date:        2025-12-14

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

from RobotLibrary.IEC_Types import UINT, UINTEnum

class CmdType(UINTEnum):
    RobotTask = 0
    """
    Handles multiple mechanisms required for operation of the interface
    """

    ReadRobotData = 9002
    """
    Read robot-specific data from the RC
    """

    EnableRobot = 1000
    """
    Enable/Disable robot into RA power state "Enabled"
    """

    GroupReset = 1001
    """
    Acknowledgement all pending errors
    """

    ReadActualPosition = 5100
    """
    Read the actual position - TCP: X…RZ + config/Turn, Joint: (J1…E6)
    """

    ReadActualPositionCyclic = 1
    """
    Read the actual position cyclically
    """

    ReadDHParameter = 5101
    """
    Read D-H-parameters of robot
    """

    RestartController = 1101
    """
    Restart/reboot of the RC
    """

    ReadActualTCPVelocity = 5111
    """
    Read actual TCP velocity
    """

    UserLogin = 1006
    """
    Login on RC from PLC
    """

    SwitchLanguage = 1005
    """
    Switch language of robot teach pendant from PLC
    """

    ExchangeConfiguration = 9000
    """
    Reads and writes specific configuration parameters on RC that are required for the RI to work
    """

    SetSequence = 1004
    """
    Set active sequence
    """

    ChangeSpeedOverride = 2000
    """
    Change actual speed override
    """

    ReadMessages = 9001
    """
    Read error codes of pending errors and move them into user data block "RobotData"
    """

    ReadRobotReferenceDynamics = 5105
    """
    Read reference values of robot dynamics for path movement
    """

    WriteFrameData = 5200
    """
    Change configuration of selected user frame number
    """

    WriteToolData = 5205
    """
    Change configuration of selected tool number
    """

    WriteLoadData = 5201
    """
    Change configuration of selected payload number
    """

    WriteRobotReferenceDynamics = 5203
    """
    Write reference values of robot dynamics for path movement
    """

    WriteRobotDefaultDynamics = 5202
    """
    Write default values of dynamic parameters used by move commands
    """

    ReadRobotDefaultDynamics = 5104
    """
    Read default values of dynamic parameters used by move commands
    """

    ReadFrameData = 5102
    """
    Read content of selected user frame number
    """

    ReadToolData = 5107
    """
    Read content of selected tool number
    """

    ReadLoadData = 5103
    """
    Read content of selected payload number
    """

    ReadRobotSWLimits = 5106
    """
    Read actual software limits of the axes\n
    Positive and negative limit of Joint J1…J6, E1…E6
    """

    WriteRobotSWLimits = 5204
    """
    Change robot limits of robot axes (degree)
    """

    SetOperationMode = 1003
    """
    Switch operation mode of RC (Automatic External, T1 External, T2 External)
    """

    ReadWorkArea = 7502
    """
    Read configuration of defined work areas
    """

    WriteWorkArea = 7503
    """
    Define work area
    """

    ActivateWorkArea = 7500
    """
    Enable/Disable work areas of RC and check if TCP is inside/outside of active work area
    """

    MonitorWorkArea = 7501
    """
    Monitor enabled work areas
    """

    GroupJog = 2100
    """
    Jog robot manually
    """

    MoveLinearAbsolute = 2103
    """
    Move the TCP to an absolute cartesian position (linear interpolation)
    """

    MoveDirectAbsolute = 2102
    """
    Move joints to an absolute cartesian position (Absolute cartesian PTP)\n
    Joint interpolated movement
    """

    MoveAxesAbsolute = 2101
    """
    Move all joints to an absolute joint position (Absolute Joint PTP)
    """

    GroupStop = 2003
    """
    Abort actual movement and delete buffer
    """

    GroupInterrupt = 2002
    """
    Interrupt active movement, possible to continue movement
    """

    GroupContinue = 2001
    """
    Continue interrupted path
    """

    MoveLinearRelative = 2110
    """
    Move the TCP relative to the actual cartesian position (linear interpolation)
    """

    MoveDirectRelative = 2108
    """
    Move joints relative to relative cartesian position (Relative cartesian PTP)\n
    Joint interpolated movement
    """

    MoveAxesRelative = 2105
    """
    Move all joints relative to actual joint position (Relative Joint PTP)
    """

    ReturnToPrimary = 2104
    """
    Return to path left during active interrupt
    """

    MoveCircularAbsolute = 2109
    """
    Move the TCP to an absolute joint position (linear interpolation)
    """

    MoveCircularRelative = 2106
    """
    Move the TCP relative to the actual cartesian position (circular interpolation)
    """

    MoveLinearOffset = 2112
    """
    Move the TCP relative to a reference cartesian position (linear interpolation)
    """

    MoveDirectOffset = 2111
    """
    Move the TCP relative to a reference cartesian position (PTPT interpolation)
    """

    WaitTime = 7005
    """
    Set wait command between motion commands
    """

    MoveApproachLinear = 2201
    """
    Linear Move to target position through auxiliary position defined by offset in all dimensions (movement to target position linear)
    """

    MoveDepartLinear = 2203
    """
    Linear Move from actual position to destination through auxiliary position defined by offset in all dimensions (movement to target position linear)
    """

    MoveApproachDirect = 2200
    """
    Direct Move to target position through auxiliary position defined by offset in all dimensions (movement to target position PTP)
    """

    MoveDepartDirect = 2202
    """
    Direct Move from actual position to destination through auxiliary position defined by offset in all dimensions (movement to the target position PTP)
    """

    SearchHardstop = 2500
    """
    Move robot into contact with obstruction (mechanical Limit) and hold it in this position
    """

    SearchHardstopJ = 2501
    """
    Move robot into contact with obstruction (mechanical Limit) and hold it in this position
    """

    MovePickPlaceLinear = 2205
    """
    Command several interpolated movement of robot arm on linear paths from actual position
    """

    MovePickPlaceDirect = 2204
    """
    Commands interpolated movement of robot arm on a partly undefined path from actual position
    """

    ActivateConveyorTracking = 2300
    """
    Activate conveyor tracking mode
    """

    RedefineTrackingPos = 2302
    """
    Redefine tracking position for conveyor tracking
    """

    SyncToConveyor = 2303
    """
    Synchronize robot with conveyor
    """

    ConfigureConveyor = 2301
    """
    Configure conveyor parameters
    """

    MoveSuperImposed = 2502
    """
    Activate superimposed motion of TCP to defined motion
    """

    MoveSuperImposedDynamic = 2503
    """
    Activate superimposed motion of TCP to defined motion
    """

    ReadDigitalInputs = 6100
    """
    Read digital input and output group of RC
    """

    ReadDigitalOutputs = 6101
    """
    Read digital output group of RC
    """

    WriteDigitalOutputs = 6104
    """
    Write digital output group of RC
    """

    ReadIntegers = 6102
    """
    Read integer values on RC
    """

    ReadReals = 6103
    """
    Read real values on RC
    """

    WriteIntegers = 6105
    """
    Write integer values on RC
    """

    WriteReals = 6106
    """
    Write real values on RC
    """

    MoveLinearCam = 2402
    """
    Set trigger in defined position of path (L = Linear Path) (cartesian) switch periphery.
    """

    MoveDirectCam = 2401
    """
    Set a trigger in a defined position of a path. (PTP)
    """

    MoveCircularCam = 2400
    """
    Set a trigger in a defined position of a circular path
    """

    ReadAnalogInput = 6107
    """
    Read analog input of RC
    """

    ReadAnalogOutput = 6108
    """
    Read analog output of RC
    """

    WriteAnalogOutput = 6109
    """
    Write analog output of RC
    """

    MeasuringInput = 6001
    """
    Capture trigger Position, measuring input
    """

    AbortMeasuringInput = 6000
    """
    Abort triggering of Position, measuring input
    """

    SetTriggerRegister = 3004
    """
    Trigger "Actions" based on I/O related events (e.g. change of DI's state)
    """

    SetTriggerLimit = 3002
    """
    Trigger "Actions" based on physical events (e.g. force limit reached)
    """

    SetTriggerUser = 3005
    """
    Trigger "Actions" based on physical events (e.g. force limit reached)
    """

    SetTriggerError = 3001
    """
    Trigger "Actions" based on incoming error event
    """

    ReactAtTrigger = 3000
    """
    "Action" that initiates specified events when triggered
    """

    WaitForTrigger = 3006
    """
    Wait to process next command in sequence until trigger signal is received
    """

    ReadSystemVariable = 5109
    """
    Read specific parameter of the robot
    """

    WriteSystemVariable = 5206
    """
    Change value of specific vendor parameter
    """

    CalculateForwardKinematic = 7203
    """
    Calculate Forward Kinematic
    """

    CalculateInverseKinematic = 7204
    """
    Calculate Inverse Kinematic
    """

    CalculateCartesianPosition = 7200
    """
    Calculate cartesian position from existing cartesian position
    """

    CalculateTool = 7202
    """
    Calculate tool (TCP) with four-point method
    """

    CalculateFrame = 7201
    """
    Calculate frame with three-point method
    """

    ActivateNextCommand = 7000
    """
    Cancel currently active move command and continue with the next buffered command
    """

    ShiftPosition = 7205
    """
    Transform a defined position in space
    """

    SetTriggerMotion = 3003
    """
    Trigger an action based on a motion-related parameter (e.g. progress of trajectory)
    """

    OpenBrake = 7100
    """
    Release robot arm's brakes
    """

    CallSubprogram = 7001
    """
    Call subprogram stored in RC from PLC
    """

    WriteCallSubprogramCyclic = 2
    """
    Writes cyclic data of called subprogram
    """

    ReadCallSubprogramCyclic = 3
    """
    Reads cyclic data of called subprogram
    """

    StopSubprogram = 7008
    """
    Stops an active subprogram
    """

    PathAccuracyMode = 7401
    """
    Switch path mode between high and low accuracy
    """

    AvoidSingularity = 7400
    """
    Activate/Deactivate functionality to avoid singularities
    """

    ForceControl = 7301
    """
    Enables the RC to apply user-defined force/torque through RA's TCP movement
    """

    ForceLimit = 7302
    """
    Commands specified reaction from RA when defined force/torque detected
    """

    ReadActualForce = 5110
    """
    Read actual force/torque at TCP
    """

    BrakeTest = 7101
    """
    Activate robot cycle brake test and give feedback to PLC
    """

    SoftSwitchTCP = 7300
    """
    Push robot: Robot calculates opposite vector and moves slowly in that direction
    """

    CreateSpline = 2600
    """
    Create spline on RC from positions stored in PLC
    """

    DeleteSpline = 2601
    """
    Delete spline previously created on RC
    """

    MoveSpline = 2603
    """
    Move spline previously created on RC
    """

    DynamicSpline = 2602
    """
    Create and move spline on RC simultaneously
    """

    LoadMeasurementAutomatic = 7006
    """
    Automatic detection of load data
    """

    LoadMeasurementSequential = 7007
    """
    Sequential detection of load data
    """

    CollisionDetection = 7003
    """
    Turn on/off the collision detection
    """

    FreeDrive = 7002
    """
    Move the robot axes by hand
    """

    UnitMeasurement = 7004
    """
    Measure the length of objects in the cartesian space, execution time for specified section of a job or signal output time of a specified signal
    """
    
    