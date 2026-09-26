"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadRobotDataOutCmd
Author:      Thorsten Brach
Date:        2025-12-23

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

from RobotLibrary.IEC_Types import IEC_Struct, STRING, USINT
from RobotLibrary.Structures.Axis.AxisExternalUnit import AxisExternalUnit
from RobotLibrary.Structures.Axis.AxisExternalUsed import AxisExternalUsed
from RobotLibrary.Structures.Axis.AxisJointUnit import AxisJointUnit
from RobotLibrary.Structures.Axis.AxisJointUsed import AxisJointUsed
from RobotLibrary.Structures.Miscellaneous.RCSupportedFunctions import RCSupportedFunctions

class ReadRobotDataOutCmd(IEC_Struct):
    """
    Output structure for reading robot data.
    """
    
    RCManufacturer : STRING = STRING(20)
    """RC manufacturer name"""
    
    RCOrderID : STRING = STRING(20)
    """RC part number"""
    
    RCSerialNumber : STRING = STRING(16)
    """RC serial number"""
    
    RASerialNumber : STRING = STRING(16)
    """RA serial number"""
    
    RCFirmwareVersion : STRING = STRING(12)
    """Robot firmware version in manufacturer-specific format"""
    
    RCInterpreterVersion : STRING = STRING(5)
    """RC Interpreter Version"""
    
    AxisJointUsed: AxisJointUsed
    """TRUE = Axis used in Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment"""
    
    AxisExternalUsed: AxisExternalUsed
    """TRUE = Axis used by Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment."""
    
    AxisJointUnit: AxisJointUnit
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment."""
    
    AxisExternalUnit: AxisExternalUnit
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment"""
    
    RCSupportedFunctions: RCSupportedFunctions
    """• TRUE: Function is supported by RC • FALSE: Function is not supported by RC See Table 6-14 for bit assignment."""
    
    RobotID: STRING = STRING(16)
    """Unique and unmodifiable identification of the RA."""
    
    InterpreterCycleTime: USINT
    """Interpreter task cycle time of the RC [ms]"""