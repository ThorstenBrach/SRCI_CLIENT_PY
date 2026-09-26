"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupParameterCmdEntries
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

class AxesGroupParameterCmdEntries(UINTEnum):
    RobotTask = 0
    """
    Handles multiple mechanisms required for operation of the interface
    """

    ReadRobotData = 9002
    """
    Read robot-specific data from the RC
    """

    EnableRobot = 1
    """
    Enable/Disable robot into RA power state "Enabled"
    """

    GroupReset = 2
    """
    Acknowledgement all pending errors
    """

    ReadActualPosition = 3
    """
    Read the actual position - TCP: X…RZ + config/Turn, Joint: (J1…E6)
    """

    ReadActualPositionCyclic = 4
    """
    Read the actual position cyclically
    """

    ReadDHParameter = 5
    """
    Read D-H-parameters of robot
    """

    RestartController = 6
    """
    Restart/reboot of the RC
    """

    ReadActualTCPVelocity = 7
    """
    Read actual TCP velocity
    """

    UserLogin = 8
    """
    Login on RC from PLC
    """

    SwitchLanguage = 9
    """
    Switch language of robot teach pendant from PLC
    """

    ExchangeConfiguration = 10
    """
    Reads and writes specific configuration parameters on RC that are required for the RI to work
    """

    SetSequence = 11
    """
    Set active sequence
    """

    ChangeSpeedOverride = 12
    """
    Change actual speed override
    """

    ReadMessages = 13
    """
    Read error codes of pending errors and move them into user data block "RobotData"
    """

    ReadRobotReferenceDynamics = 14
    """
    Read reference values of robot dynamics for path movement
    """

    WriteFrameData = 15
    """
    Change configuration of selected user frame number
    """

    WriteToolData = 16
    """
    Change configuration of selected tool number
    """

    WriteLoadData = 17
    """
    Change configuration of selected payload number
    """

    WriteRobotReferenceDynamics = 18
    """
    Write reference values of robot dynamics for path movement
    """

    WriteRobotDefaultDynamics = 19
    """
    Write default values of dynamic parameters used by move commands
    """

    ReadRobotDefaultDynamics = 20
    """
    Read default values of dynamic parameters used by move commands
    """

    ReadFrameData = 21
    """
    Read content of selected user frame number
    """

    ReadToolData = 22
    """
    Read content of selected tool number
    """

    ReadLoadData = 23
    """
    Read content of selected payload number
    """

    ReadRobotSWLimits = 24
    """
    Read actual software limits of the axes\n
    Positive and negative limit of Joint J1…J6, E1…E6
    """

    WriteRobotSWLimits = 25
    """
    Change robot limits of robot axes (degree)
    """

    SetOperationMode = 26
    """
    Switch operation mode of RC\n
    (Automatic External, T1 External, T2 External)
    """

    ReadWorkArea = 27
    """
    Read configuration of defined work areas
    """

    WriteWorkArea = 28
    """
    Define work area
    """

    ActivateWorkArea = 29
    """
    Enable/Disable work areas of RC and check if TCP is inside/outside of active work area
    """

    MonitorWorkArea = 30
    """
    Monitor enabled work areas
    """

    GroupJog = 31
    """
    Jog robot manually
    """

    MoveLinearAbsolute = 32
    """
    Move the TCP to an absolute cartesian position\n
    (linear interpolation)
    """

    MoveDirectAbsolute = 33
    """
    Move joints to an absolute cartesian position\n
    Absolute cartesian PTP (joint interpolated movement)
    """

    MoveAxesAbsolute = 34
    """
    Move all joints to an absolute joint position\n
    Absolute Joint PTP
    """

    GroupStop = 35
    """
    Abort actual movement and delete buffer
    """

    GroupInterrupt = 36
    """
    Interrupt active movement, possible to continue movement
    """

    GroupContinue = 37
    """
    Continue interrupted path
    """

    MoveLinearRelative = 38
    """
    Move the TCP relative to the actual cartesian position\n
    (linear interpolation)
    """

    MoveDirectRelative = 39
    """
    Relative cartesian PTP (joint interpolated movement)
    """

    MoveAxesRelative = 40
    """
    Move all joints relative to actual joint position\n
    Relative Joint PTP
    """

    ReturnToPrimary = 41
    """
    Return to path left during active interrupt
    """

    MoveCircularAbsolute = 42
    """
    Move the TCP to an absolute joint position\n
    (circular interpolation)
    """

    MoveCircularRelative = 43
    """
    Move the TCP relative to the actual cartesian position\n
    (circular interpolation)
    """

    MoveLinearOffset = 44
    """
    Move the TCP relative to a reference cartesian position\n
    (linear interpolation)
    """

    MoveDirectOffset = 45
    """
    Move the TCP relative to a reference cartesian position\n
    (PTP interpolation)
    """

    WaitTime = 46
    """
    Set wait command between motion commands
    """

    MoveApproachLinear = 47
    """
    Linear move to target position through auxiliary position defined by offset in all dimensions
    """

    MoveDepartLinear = 48
    """
    Linear move from actual position to destination through auxiliary position defined by offset in all dimensions
    """

    MoveApproachDirect = 49
    """
    Direct move to target position through auxiliary position defined by offset in all dimensions
    """

    MoveDepartDirect = 50
    """
    Direct move from actual position to destination through auxiliary position defined by offset in all dimensions
    """

    SearchHardstop = 51
    """
    Move robot into contact with obstruction (mechanical limit) and hold it in this position
    """

    SearchHardstopJ = 52
    """
    Move robot into contact with obstruction (mechanical limit) and hold it in this position
    """

    MovePickPlaceLinear = 53
    """
    Command several interpolated movements of robot arm on linear paths from actual position
    """

    MovePickPlaceDirect = 54
    """
    Commands interpolated movement of robot arm on a partly undefined path from actual position
    """

    ActivateConveyorTracking = 55
    """
    Activate conveyor tracking mode
    """

    RedefineTrackingPos = 56
    """
    Redefine tracking position for conveyor tracking
    """

    SyncToConveyor = 57
    """
    Synchronize robot with conveyor
    """

    ConfigureConveyor = 58
    """
    Configure conveyor parameters
    """

    MoveSuperImposed = 59
    """
    Activate superimposed motion of TCP to defined motion
    """

    MoveSuperImposedDynamic = 60
    """
    Activate superimposed motion of TCP to defined motion (dynamic)
    """

    ReadDigitalInputs = 61
    """
    Read digital input group of RC
    """

    ReadDigitalOutputs = 62
    """
    Read digital output group of RC
    """

    WriteDigitalOutputs = 63
    """
    Write digital output group of RC
    """

    ReadIntegers = 64
    """
    Read integer values on RC
    """

    ReadReals = 65
    """
    Read real values on RC
    """

    WriteIntegers = 66
    """
    Write integer values on RC
    """

    WriteReals = 67
    """
    Write real values on RC
    """

    MoveLinearCam = 68
    """
    Set trigger in defined position of linear path (cartesian)
    """

    MoveDirectCam = 69
    """
    Set trigger in defined position of a PTP path
    """

    MoveCircularCam = 70
    """
    Set trigger in defined position of a circular path
    """

    ReadAnalogInput = 71
    """
    Read analog input of RC
    """

    ReadAnalogOutput = 72
    """
    Read analog output of RC
    """

    WriteAnalogOutput = 73
    """
    Write analog output of RC
    """

    MeasuringInput = 74
    """
    Capture trigger position, measuring input
    """

    AbortMeasuringInput = 75
    """
    Abort triggering of position, measuring input
    """

    SetTriggerRegister = 76
    """
    Trigger actions based on I/O related events
    """

    SetTriggerLimit = 77
    """
    Trigger actions based on physical events (e.g. force limit reached)
    """

    SetTriggerUser = 78
    """
    Trigger actions based on user-defined events
    """

    SetTriggerError = 79
    """
    Trigger actions based on incoming error event
    """

    ReactAtTrigger = 80
    """
    Action that initiates specified events when triggered
    """

    WaitForTrigger = 81
    """
    Wait to process next command in sequence until trigger signal is received
    """

    ReadSystemVariable = 82
    """
    Read specific parameter of the robot
    """

    WriteSystemVariable = 83
    """
    Change value of specific vendor parameter
    """

    CalculateForwardKinematic = 84
    """
    Calculate forward kinematic
    """

    CalculateInverseKinematic = 85
    """
    Calculate inverse kinematic
    """

    CalculateCartesianPosition = 86
    """
    Calculate cartesian position from existing cartesian position
    """

    CalculateTool = 87
    """
    Calculate tool (TCP) with four-point method
    """

    CalculateFrame = 88
    """
    Calculate frame with three-point method
    """

    ActivateNextCommand = 89
    """
    Cancel currently active move command and continue with the next buffered command
    """

    ShiftPosition = 90
    """
    Transform a defined position in space
    """

    SetTriggerMotion = 91
    """
    Trigger an action based on a motion-related parameter
    """

    OpenBrake = 92
    """
    Release robot arm’s brakes
    """

    CallSubprogram = 93
    """
    Call subprogram stored in RC from PLC
    """

    WriteCallSubprogramCyclic = 94
    """
    Writes cyclic data of called subprogram
    """

    ReadCallSubprogramCyclic = 95
    """
    Reads cyclic data of called subprogram
    """

    StopSubprogram = 96
    """
    Stops an active subprogram
    """

    PathAccuracyMode = 97
    """
    Switch path mode between high and low accuracy
    """

    AvoidSingularity = 98
    """
    Activate/Deactivate functionality to avoid singularities
    """

    ForceControl = 99
    """
    Enables the RC to apply user-defined force/torque through RA's TCP movement
    """

    ForceLimit = 100
    """
    Commands specified reaction from RA when defined force/torque detected
    """

    ReadActualForce = 101
    """
    Read actual force/torque at TCP
    """

    BrakeTest = 102
    """
    Activate robot cycle brake test and give feedback to PLC
    """

    SoftSwitchTCP = 103
    """
    Push robot: robot calculates opposite vector and moves slowly in that direction
    """

    CreateSpline = 104
    """
    Create spline on RC from positions stored in PLC
    """

    DeleteSpline = 105
    """
    Delete spline previously created on RC
    """

    MoveSpline = 106
    """
    Move spline previously created on RC
    """

    DynamicSpline = 107
    """
    Create and move spline on RC simultaneously
    """

    LoadMeasurementAutomatic = 108
    """
    Automatic detection of load data
    """

    LoadMeasurementSequential = 109
    """
    Sequential detection of load data
    """

    CollisionDetection = 110
    """
    Turn on/off the collision detection
    """

    FreeDrive = 111
    """
    Move the robot axes by hand
    """

    UnitMeasurement = 112
    """
    Measure length, execution time or signal output time
    """

    MAX_ENTRY = 113
    """
    Maximum entry
    """
    
    # Set enum size for ctypes evaluation
    setattr(UINTEnum, 'ctypes_type', UINT)    