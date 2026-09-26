"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RCSupportedFunctions
Author:      Thorsten Brach
Date:        2025-12-20

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

from RobotLibrary.IEC_Types import BOOL, IEC_Struct


class RCSupportedFunctions(IEC_Struct):
    
    Byte00Bit0: BOOL
    """Byte 00 - Bit 0"""

    ReadRobotData: BOOL = True #type: ignore
    """Byte 00 - Bit 1 -> must be initialized with true, because this command is part of the interface initialization"""

    EnableRobot: BOOL
    """Byte 00 - Bit 2"""

    GroupReset: BOOL
    """Byte 00 - Bit 3"""

    ReadActualPosition: BOOL
    """Byte 00 - Bit 4"""

    ReadActualPositionCyclic: BOOL
    """Byte 00 - Bit 5"""

    ExchangeConfiguration: BOOL = True #type: ignore
    """Byte 00 - Bit 6 -> must be initialized with true, because this command is part of the interface initialization"""

    SetSequence: BOOL
    """Byte 00 - Bit 7"""

    ChangeSpeedOverride: BOOL
    """Byte 01 - Bit 0"""

    ReadMessages: BOOL = True #type: ignore
    """Byte 01 - Bit 1 -> must be initialized with true, because this command is part of the interface initialization"""

    ReadRobotReferenceDynamics: BOOL
    """Byte 01 - Bit 2"""

    WriteFrameData: BOOL
    """Byte 01 - Bit 3"""

    WriteToolData: BOOL
    """Byte 01 - Bit 4"""

    WriteLoadData: BOOL
    """Byte 01 - Bit 5"""

    WriteRobotReferenceDynamics: BOOL
    """Byte 01 - Bit 6"""

    WriteRobotDefaultDynamics: BOOL
    """Byte 01 - Bit 7"""

    ReadRobotDefaultDynamics: BOOL
    """Byte 02 - Bit 0"""

    ReadFrameData: BOOL
    """Byte 02 - Bit 1"""

    ReadToolData: BOOL
    """Byte 02 - Bit 2"""

    ReadLoadData: BOOL
    """Byte 02 - Bit 3"""

    ReadRobotSWLimits: BOOL
    """Byte 02 - Bit 4"""

    GroupJog: BOOL
    """Byte 02 - Bit 5"""

    MoveLinearAbsolute: BOOL
    """Byte 02 - Bit 6"""

    MoveDirectAbsolute: BOOL
    """Byte 02 - Bit 7"""

    MoveAxesAbsolute: BOOL
    """Byte 03 - Bit 0"""

    GroupStop: BOOL
    """Byte 03 - Bit 1"""

    GroupContinue: BOOL
    """Byte 03 - Bit 2"""

    GroupInterrupt: BOOL
    """Byte 03 - Bit 3"""

    ReturnToPrimary: BOOL
    """Byte 03 - Bit 4"""

    MoveLinearAbsoluteJ: BOOL
    """Byte 03 - Bit 5"""

    MoveDirectRelative: BOOL
    """Byte 03 - Bit 6"""

    MoveAxesRelative: BOOL
    """Byte 03 - Bit 7"""

    MoveCircularAbsolute: BOOL
    """Byte 04 - Bit 0"""

    MoveCircularRelative: BOOL
    """Byte 04 - Bit 1"""

    MoveLinearOffset: BOOL
    """Byte 04 - Bit 2"""

    MoveDirectOffset: BOOL
    """Byte 04 - Bit 3"""

    WaitTime: BOOL
    """Byte 04 - Bit 4"""

    ReadDigitalInputs: BOOL
    """Byte 04 - Bit 5"""

    ReadDigitalOutputs: BOOL
    """Byte 04 - Bit 6"""

    WriteDigitalOutputs: BOOL
    """Byte 04 - Bit 7"""

    ReadIntegers: BOOL
    """Byte 05 - Bit 0"""

    ReadReals: BOOL
    """Byte 05 - Bit 1"""

    WriteIntegers: BOOL
    """Byte 05 - Bit 2"""

    WriteReals: BOOL
    """Byte 05 - Bit 3"""

    MoveLinearCam: BOOL
    """Byte 05 - Bit 4"""

    MoveDirectCam: BOOL
    """Byte 05 - Bit 5"""

    MoveCircularCam: BOOL
    """Byte 05 - Bit 6"""

    SetTriggerRegister: BOOL
    """Byte 05 - Bit 7"""

    SetTriggerLimit: BOOL
    """Byte 06 - Bit 0"""

    SetTriggerUser: BOOL
    """Byte 06 - Bit 1"""

    SetTriggerError: BOOL
    """Byte 06 - Bit 2"""

    ReactAtTrigger: BOOL
    """Byte 06 - Bit 3"""

    WaitForTrigger: BOOL
    """Byte 06 - Bit 4"""

    ReadSystemVariable: BOOL
    """Byte 06 - Bit 5"""

    WriteSystemVariable: BOOL
    """Byte 06 - Bit 6"""

    CalculateForwardKinematic: BOOL
    """Byte 06 - Bit 7"""

    CalculateInverseKinematic: BOOL
    """Byte 07 - Bit 0"""

    CalculateCartesianPosition: BOOL
    """Byte 07 - Bit 1"""

    CalculateTool: BOOL
    """Byte 07 - Bit 2"""

    CalculateFrame: BOOL
    """Byte 07 - Bit 3"""

    ActivateNextCommand: BOOL
    """Byte 07 - Bit 4"""

    ShiftPosition: BOOL
    """Byte 07 - Bit 5"""

    CallSubprogram: BOOL
    """Byte 07 - Bit 6"""

    MoveLinearRelative: BOOL
    """Byte 07 - Bit 7"""

    WriteCallSubprogramCyclic: BOOL
    """Byte 08 - Bit 0"""

    ReadCallSubprogramCyclic: BOOL
    """Byte 08 - Bit 1"""

    StopSubprogram: BOOL
    """Byte 08 - Bit 2"""

    ReadDHParameter: BOOL
    """Byte 08 - Bit 3"""

    RestartController: BOOL
    """Byte 08 - Bit 4"""

    ReadActualTCPVelocity: BOOL
    """Byte 08 - Bit 5"""

    UserLogin: BOOL
    """Byte 08 - Bit 6"""

    SwitchLanguage: BOOL
    """Byte 08 - Bit 7"""

    WriteRobotSWLimits: BOOL
    """Byte 09 - Bit 0"""

    SetOperationMode: BOOL
    """Byte 09 - Bit 1"""

    ReadWorkArea: BOOL
    """Byte 09 - Bit 2"""

    WriteWorkArea: BOOL
    """Byte 09 - Bit 3"""

    ActivateWorkArea: BOOL
    """Byte 09 - Bit 4"""

    MonitorWorkArea: BOOL
    """Byte 09 - Bit 5"""

    MoveApproachLinear: BOOL
    """Byte 09 - Bit 6"""

    MoveDepartLinear: BOOL
    """Byte 09 - Bit 7"""

    MoveApproachDirect: BOOL
    """Byte 10 - Bit 0"""

    MoveDepartDirect: BOOL
    """Byte 10 - Bit 1"""

    SearchHardstop: BOOL
    """Byte 10 - Bit 2"""

    SearchHardstopJ: BOOL
    """Byte 10 - Bit 3"""

    MovePickPlaceLinear: BOOL
    """Byte 10 - Bit 4"""

    MovePickPlaceDirect: BOOL
    """Byte 10 - Bit 5"""

    ActivateConveyorTracking: BOOL
    """Byte 10 - Bit 6"""

    RedefineTrackingPosition: BOOL
    """Byte 10 - Bit 7"""

    SyncToConveyor: BOOL
    """Byte 11 - Bit 0"""

    ConfigureConveyor: BOOL
    """Byte 11 - Bit 1"""

    MoveSuperImposed: BOOL
    """Byte 11 - Bit 2"""

    MoveSuperImposedDynamic: BOOL
    """Byte 11 - Bit 3"""

    ReadAnalogInput: BOOL
    """Byte 11 - Bit 4"""

    ReadAnalogOutput: BOOL
    """Byte 11 - Bit 5"""

    WriteAnalogOutput: BOOL
    """Byte 11 - Bit 6"""

    MeasuringInput: BOOL
    """Byte 11 - Bit 7"""

    AbortMeasuringInput: BOOL
    """Byte 12 - Bit 0"""

    SetTriggerMotion: BOOL
    """Byte 12 - Bit 1"""

    OpenBrake: BOOL
    """Byte 12 - Bit 2"""

    PathAccuracyMode: BOOL
    """Byte 12 - Bit 3"""

    AvoidSingularity: BOOL
    """Byte 12 - Bit 4"""

    ForceControl: BOOL
    """Byte 12 - Bit 5"""

    ForceLimit: BOOL
    """Byte 12 - Bit 6"""

    ReadActualForce: BOOL
    """Byte 12 - Bit 7"""

    BrakeTest: BOOL
    """Byte 13 - Bit 0"""

    SoftSwitchTCP: BOOL
    """Byte 13 - Bit 1"""

    CreateSpline: BOOL
    """Byte 13 - Bit 2"""

    DeleteSpline: BOOL
    """Byte 13 - Bit 3"""

    MoveSpline: BOOL
    """Byte 13 - Bit 4"""

    DynamicSpline: BOOL
    """Byte 13 - Bit 5"""

    LoadMeasurementAutomatic: BOOL
    """Byte 13 - Bit 6"""

    LoadMeasurementSequential: BOOL
    """Byte 13 - Bit 7"""

    CollisionDetection: BOOL
    """Byte 14 - Bit 0"""

    FreeDrive: BOOL
    """Byte 14 - Bit 1"""

    UnitMeasurement: BOOL
    """Byte 14 - Bit 2"""

    Byte14Bit03: BOOL
    """Byte 14 - Bit 3"""

    Byte14Bit04: BOOL
    """Byte 14 - Bit 4"""

    Byte14Bit05: BOOL
    """Byte 14 - Bit 5"""

    Byte14Bit06: BOOL
    """Byte 14 - Bit 6"""

    Byte14Bit07: BOOL
    """Byte 14 - Bit 7"""

    Byte15Bit00: BOOL
    """Byte 15 - Bit 0"""

    Byte15Bit01: BOOL
    """Byte 15 - Bit 1"""

    Byte15Bit02: BOOL
    """Byte 15 - Bit 2"""

    Byte15Bit03: BOOL
    """Byte 15 - Bit 3"""

    Byte15Bit04: BOOL
    """Byte 15 - Bit 4"""

    Byte15Bit05: BOOL
    """Byte 15 - Bit 5"""

    Byte15Bit06: BOOL
    """Byte 15 - Bit 6"""

    Byte15Bit07: BOOL
    """Byte 15 - Bit 7"""

    Byte16Bit00: BOOL
    """Byte 16 - Bit 0"""

    Byte16Bit01: BOOL
    """Byte 16 - Bit 1"""

    Byte16Bit02: BOOL
    """Byte 16 - Bit 2"""

    Byte16Bit03: BOOL
    """Byte 16 - Bit 3"""

    Byte16Bit04: BOOL
    """Byte 16 - Bit 4"""

    Byte16Bit05: BOOL
    """Byte 16 - Bit 5"""

    Byte16Bit06: BOOL
    """Byte 16 - Bit 6"""

    Byte16Bit07: BOOL
    """Byte 16 - Bit 7"""

    Byte17Bit00: BOOL
    """Byte 17 - Bit 0"""

    Byte17Bit01: BOOL
    """Byte 17 - Bit 1"""

    Byte17Bit02: BOOL
    """Byte 17 - Bit 2"""

    Byte17Bit03: BOOL
    """Byte 17 - Bit 3"""

    Byte17Bit04: BOOL
    """Byte 17 - Bit 4"""

    Byte17Bit05: BOOL
    """Byte 17 - Bit 5"""

    Byte17Bit06: BOOL
    """Byte 17 - Bit 6"""

    Byte17Bit07: BOOL
    """Byte 17 - Bit 7"""

    Byte18Bit00: BOOL
    """Byte 18 - Bit 0"""

    Byte18Bit01: BOOL
    """Byte 18 - Bit 1"""

    Byte18Bit02: BOOL
    """Byte 18 - Bit 2"""

    Byte18Bit03: BOOL
    """Byte 18 - Bit 3"""

    Byte18Bit04: BOOL
    """Byte 18 - Bit 4"""

    Byte18Bit05: BOOL
    """Byte 18 - Bit 5"""

    Byte18Bit06: BOOL
    """Byte 18 - Bit 6"""

    Byte18Bit07: BOOL
    """Byte 18 - Bit 7"""