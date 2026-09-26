"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupParameterRob
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
#region Imports
from RobotLibrary.IEC_Types import IEC_Struct, UINT, USINT, UDINT, BOOL,STRING
from RobotLibrary.Structures.Miscellaneous.DataInSync import DataInSync
#endregion


#-------------------------------------------------------------------------
# AxesGroupParameterRobParameter
#-------------------------------------------------------------------------
class AxesGroupParameterRobParameter(IEC_Struct):
    
    RobotName : STRING = STRING(20)
    """User defined robot name"""

    LengthACR: int = 50 #type: ignore #ToDo: Pylance can not follow the dynamic type cast inside the IEC_Struct class
    """
    Returns a metric of how many CMDs it can receive and manage at the same time.
    Must be initialized with a value > 3, because during the interface initialization
    at least 3 commands are executed.
    After ReadRobotData command the value is set to the correct ACR length
    which is supported by the RC.
    """

    HighestToolIndex: int
    """Highest index of available tools on the RC"""

    HighestFrameIndex: int
    """Highest index of available frames on the RC"""

    HighestLoadIndex: int
    """Highest index of available loads on the RC"""

    HighestWorkAreaIndex: int
    """Highest index of available work areas on the RC"""

    DataInSync: DataInSync
    """Data which are synchronized"""

    ChangeIndexTool: int
    """Index of tool changed on RC"""

    ChangeIndexFrame: int
    """Index of frame changed on RC"""

    ChangeIndexLoad: int
    """Index of load changed on RC"""

    ChangeIndexWorkArea: int
    """Index of work area changed on RC"""

    RAWorkingHours: int
    """Working hours of an RA connected to the RC"""

    BrakeTestRequired: int
    """Signals that a brake test is required in the defined monitoring time"""

    StepModeExactStopActive: int
    """StepMode is active and set to ExactStop"""

    StepModeBlendingActive: int
    """StepMode is active and set to Blending"""

    PathAccuracyMode: int
    """PathAccuracyMode is active"""

    AvoidSingularity: int
    """AvoidSingularity is active"""

    CollisionDetectionEnabled: int
    """CollisionDetection is active"""

    AcceleratingSupported: int
    """Cyclic dynamics status bit Accelerating is supported by RC"""

    DecceleratingSupported: int
    """Cyclic dynamics status bit Decelerating is supported by RC"""

    ConstantVelocitySupported: int
    """Cyclic dynamics status bit ConstantVelocity is supported by RC"""

    RCWorkingHours: int
    """
    Total system hours of an RA connected to the RC.
    •  0: Invalid
    • >0: Total system hours
    """


#-------------------------------------------------------------------------
# AxesGroupParameterRobOptionalCyclic
#-------------------------------------------------------------------------
class AxesGroupParameterRobOptionalCyclic(IEC_Struct):
    
    UseCallSubprogram: BOOL
    """
    Bit 00:
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC
    called via the function “CallSubprogram”
    """

    UseCartesianPosition: BOOL
    """
    Bit 01:
    Send a short cartesian position with TCP position (X, Y, Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1)
    and corresponding coordinate systems (ToolNo, FrameNo)
    """

    UseJointPosition: BOOL
    """
    Bit 02:
    Send a short axes position with joint values (J1, J2, J3, J4, J5, J6)
    and position of first external axis (E1)
    """

    UseForce: BOOL
    """
    Bit 03:
    Send the force with the divided forces in the individual directions
    (X, Y, Z, RX, RY, RZ)
    """

    UseCurrent: BOOL
    """
    Bit 04:
    Transmit actual axes current of individual axes
    (J1, J2, J3, J4, J5, J6)
    """

    Bit05: BOOL
    """Bit 05"""

    Bit06: BOOL
    """Bit 06"""

    Bit07: BOOL
    """Bit 07"""

    UseTwoSequences: BOOL
    """
    Bit 08:
    Set to 1 to define two sequences in one telegram.
    If activated, 2 sequences also have to be activated
    in the ServerClient direction
    """

    UseCartesianPositionExt: BOOL
    """
    Bit 09:
    Send the external axis values for an extended cartesian position
    (E2, E3, E4, E5, E6)
    """

    UseJointPositionExt: BOOL
    """
    Bit 10:
    Send the external axis values for an extended joint position
    (E2, E3, E4, E5, E6)
    """

    UseForceExt: BOOL
    """
    Bit 11:
    Transmit the current force for the external axes
    (E1, E2, E3, E4, E5, E6)
    """

    UseCurrentExt: BOOL
    """
    Bit 12:
    Transmit the actual current for the external axes
    (E1, E2, E3, E4, E5, E6)
    """

    Bit13: BOOL
    """Bit 13"""

    Bit14: BOOL
    """Bit 14"""

    Bit15: BOOL
    """Bit 15"""


#-------------------------------------------------------------------------
# AxesGroupParameterRob
#-------------------------------------------------------------------------
class AxesGroupParameterRob(IEC_Struct):
    Parameter : AxesGroupParameterRobParameter
    """Parameter"""

    OptionalCyclic : AxesGroupParameterRobOptionalCyclic
    """Optional cyclic"""