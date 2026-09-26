"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramRobToPlcCyclicOptionalData
Author:      Thorsten Brach
Date:        2025-12-21

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
#region imports
from RobotLibrary.IEC_Types import IEC_Struct, REAL, WORD, BYTE, USINT, ARRAY
#endregion

#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalCartesianPosition
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalCartesianPosition(IEC_Struct):
  
    X: REAL
    """TCP position on the X-axis"""

    Y: REAL
    """TCP position on the Y-axis"""

    Z: REAL
    """TCP position on the Z-axis"""

    Rx: REAL
    """Rotation around the X-axis (RX)"""

    Ry: REAL
    """Rotation around the Y-axis (RY)"""

    Rz: REAL
    """Rotation around the Z-axis (RZ)"""

    Config: WORD
    """Configuration"""

    Turns_J2_J1: BYTE
    """Turns of J1 and J2"""

    Turns_J4_J3: BYTE
    """Turns of J3 and J4"""

    Turns_J6_J5: BYTE
    """Turns of J6 and J5"""

    Turns_E1: BYTE
    """Turns of E1"""

    E1: REAL
    """Position of first external axis"""

    ToolNo: USINT
    """Tool number"""

    FrameNo: USINT
    """Frame number"""

    CurrentlyUsedToolNo: USINT
    """Currently used tool number"""

    CurrentlyUsedFrameNo: USINT
    """Currently used frame number"""

    Reserve_1: BYTE
    """Reserve"""

    Reserve_2: BYTE
    """Reserve"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalData
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalCartesianPositionExt(IEC_Struct):
  
    E2: REAL
    """Position of second external axis"""

    E3: REAL
    """Position of third external axis"""

    E4: REAL
    """Position of fourth external axis"""

    E5: REAL
    """Position of fifth external axis"""

    E6: REAL
    """Position of sixth external axis"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalJointPosition
#---------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalCurrent(IEC_Struct):
  
    J1: REAL
    """Current of first joint of the robot"""

    J2: REAL
    """Current of second joint of the robot"""

    J3: REAL
    """Current of third joint of the robot"""

    J4: REAL
    """Current of fourth joint of the robot"""

    J5: REAL
    """Current of fifth joint of the robot"""

    J6: REAL
    """Current of sixth joint of the robot"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalCurrentExt
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalCurrentExt(IEC_Struct):
  
    E1: REAL
    """Current of first external joint of the robot"""

    E2: REAL
    """Current of second external axis"""

    E3: REAL
    """Current of third external axis"""

    E4: REAL
    """Current of fourth external axis"""

    E5: REAL
    """Current of fifth external axis"""

    E6: REAL
    """Current of sixth external axis"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalForce
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalForce(IEC_Struct):
  
    X: REAL
    """Force on the X-axis"""

    Y: REAL
    """Force on the Y-axis"""

    Z: REAL
    """Force on the Z-axis"""

    Rx: REAL
    """Force around the X-axis (RX)"""

    Ry: REAL
    """Force around the Y-axis (RY)"""

    Rz: REAL
    """Force around the Z-axis (RZ)"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalForceExt
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalForceExt(IEC_Struct):
  
    E1: REAL
    """Force on the external axis 1"""

    E2: REAL
    """Force on the external axis 2"""

    E3: REAL
    """Force on the external axis 3"""

    E4: REAL
    """Force on the external axis 4"""

    E5: REAL
    """Force on the external axis 5"""

    E6: REAL
    """Force on the external axis 6"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalJointPosition
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalJointPosition(IEC_Struct):
  
    J1: REAL
    """Position of first joint of the robot"""

    J2: REAL
    """Position of second joint of the robot"""

    J3: REAL
    """Position of third joint of the robot"""

    J4: REAL
    """Position of fourth joint of the robot"""

    J5: REAL
    """Position of fifth joint of the robot"""

    J6: REAL
    """Position of sixth joint of the robot"""

    E1: REAL
    """Position of first external axis"""

    E1_Reserve: WORD
    """Reserve"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalJointPositionExt
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalJointPositionExt(IEC_Struct):
  
    E2: REAL
    """Position of second external axis"""

    E3: REAL
    """Position of third external axis"""

    E4: REAL
    """Position of fourth external axis"""

    E5: REAL
    """Position of fifth external axis"""

    E6: REAL
    """Position of sixth external axis"""


#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalSubProgramData
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalSubProgramData(IEC_Struct):
  
    Data : bytearray = bytearray(25)
    """ Sub program data"""        

#-------------------------------------------------------------------------
# TelegramRobToPlcCyclicOptionalData
#-------------------------------------------------------------------------
class TelegramRobToPlcCyclicOptionalData(IEC_Struct):
  
    SubProgramData: TelegramRobToPlcCyclicOptionalSubProgramData
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC
    called via the function “CallSubprogram”
    """

    CartesianPosition: TelegramRobToPlcCyclicOptionalCartesianPosition
    """
    Cartesian position with TCP position (X, Y, Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1)
    and corresponding coordinate systems (ToolNo, FrameNo)
    """

    JointPosition: TelegramRobToPlcCyclicOptionalJointPosition
    """
    Axes position with joint values (J1, J2, J3, J4, J5, J6)
    and position of first external axis (E1)
    """

    Force: TelegramRobToPlcCyclicOptionalForce
    """
    Force with the divided forces in the individual directions
    (X, Y, Z, RX, RY, RZ)
    """

    Current: TelegramRobToPlcCyclicOptionalCurrent
    """
    Transmit actual axes current of individual axes
    (J1, J2, J3, J4, J5, J6)
    """

    TwoSequences: BYTE
    """
    Set to 1 to define two sequences in one telegram.
    If activated, two sequences also have to be activated
    in the ClientServer direction.
    """

    CartesianPositionExt: TelegramRobToPlcCyclicOptionalCartesianPositionExt
    """
    Transmit the external axis values for an extended cartesian position
    (E2, E3, E4, E5, E6).
    When selected, Tool and Frame will automatically be sent cyclically
    from client to server.
    """

    JointPositionExt: TelegramRobToPlcCyclicOptionalJointPositionExt
    """
    Transmit the external axis values for an extended joint position
    (E2, E3, E4, E5, E6)
    """

    ForceExt: TelegramRobToPlcCyclicOptionalForceExt
    """
    Transmit actual axes force of individual external axes
    (E1, E2, E3, E4, E5, E6)
    """

    CurrentExt: TelegramRobToPlcCyclicOptionalCurrentExt
    """
    Transmit actual axes current of individual external axes
    (E1, E2, E3, E4, E5, E6)
    """