"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRobCyclicOptionalData
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
#region Imports
from RobotLibrary.IEC_Types import IEC_Struct, BYTE, WORD, REAL, ARRAY
#endregion


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalCartesianPosition - Optional Cartesian Position
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalCartesianPosition(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalCartesianPositionExt - Optional Cartesian Position Extended
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalCartesianPositionExt(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalCurrent - Optional Current
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalCurrent(IEC_Struct):
    
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalCurrentExt - Optional Current Extended
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalCurrentExt(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalForce - Optional Force
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalForce(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalForceExt - Optional Force Extended
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalForceExt(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalJointPosition - Optional Joint Position
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalJointPosition(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalJointPositionExt - Optional Joint Position Extended
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalJointPositionExt(IEC_Struct):
  
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


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalSubProgramData - Optional Sub Program Data
#------------------------------------------------------------
class TelegramPlcToRobCyclicOptionalSubProgramData(IEC_Struct):

    Data : bytearray = bytearray(25)
    """Sub program data"""    


#------------------------------------------------------------
# TelegramPlcToRobCyclicOptionalData - Optional Data
#------------------------------------------------------------   
class TelegramPlcToRobCyclicOptionalData(IEC_Struct):
    
    SubProgramData        :  TelegramPlcToRobCyclicOptionalSubProgramData
    """Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC called via the function “CallSubprogram”"""

    CartesianPosition     :  TelegramPlcToRobCyclicOptionalCartesianPosition
    """short cartesian position with TCP position (X, Y,Z), rotation (RX, RY, RZ), configuration bytes (Config, TurnNumber), position of first external axis (E1) and corresponding coordinate systems (ToolNo, FrameNo)"""

    CartesianPositionExt  :  TelegramPlcToRobCyclicOptionalCartesianPositionExt
    """ 
    The external axis values for an extended cartesian position (E2, E3, E4, E5, E6) \n
    When selected, Tool and Frame will automatically cyclically be sent from client to server.
    """

    JointPosition         :  TelegramPlcToRobCyclicOptionalJointPosition
    """ short axes position with joint values (J1, J2, J3,J4, J5, J6) and position of first external axis (E1)"""

    JointPositionExt      :  TelegramPlcToRobCyclicOptionalJointPositionExt
    """ the external axis values for an extended joint position (E2, E3, E4, E5, E6)"""

    Force                 :  TelegramPlcToRobCyclicOptionalForce
    """ force with the divided forces in the individual directions (X, Y, Z, RX, RY, RZ)"""

    ForceExt              :  TelegramPlcToRobCyclicOptionalForceExt
    """ current force for the external axis (E1, E2, E3, E4, E5, E6)"""

    Current               :  TelegramPlcToRobCyclicOptionalCurrent
    """ actual axes current of individual axes (J1, J2, J3, J4, J5, J6)"""

    CurrentExt            :  TelegramPlcToRobCyclicOptionalCurrentExt
    """ actual current for the external axis (E1, E2,E3, E4, E5, E6)"""    
  
    Data : ARRAY[BYTE] = ARRAY(0, 25, BYTE) 
    """Sub program data"""