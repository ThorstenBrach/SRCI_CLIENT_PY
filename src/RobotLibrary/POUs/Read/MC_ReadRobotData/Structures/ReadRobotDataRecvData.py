"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadRobotDataRecvData
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

from RobotLibrary.IEC_Types import STRING, BYTE, USINT
from RobotLibrary.Structures.Common.RspHeader import RspHeader


class ReadRobotDataRecvData(RspHeader):
    """
    Response data structure for reading robot data.
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
    
    Reserve : BYTE
    """Reserve"""
    
    AxisJointUsed : BYTE
    """TRUE = Axis used in Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment"""
    
    AxisExternalUsed : BYTE
    """TRUE = Axis used by Robot FALSE = Axis NOT used. See Table 6-13 for bit assignment."""
    
    AxisJointUnit : BYTE
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment."""
    
    AxisExternalUnit : BYTE
    """TRUE = mm FALSE = ° See Table 6-13 for bit assignment"""
    
    RCSupportedFunctions: bytearray = bytearray(19)
    """• TRUE: Function is supported by RC • FALSE: Function is not supported by RC See Table 6-14 for bit assignment."""
    
    Reserve2 : BYTE
    """Reserve 2"""
    
    RobotID: STRING = STRING(16)
    """Unique and unmodifiable identification of the RA."""
    
    InterpreterCycleTime : USINT
    """Interpreter task cycle time of the RC [ms]"""
    
    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:
        
        bytes = bytearray()
        
        # header
        bytes.extend(super().GetBytes(order))
        # response data
        bytes.extend(self.RCManufacturer.to_bytes())
        bytes.extend(self.RCOrderID.to_bytes())
        bytes.extend(self.RCSerialNumber.to_bytes())
        bytes.extend(self.RASerialNumber.to_bytes())
        bytes.extend(self.RCFirmwareVersion.to_bytes())
        bytes.extend(self.RCInterpreterVersion.to_bytes())
        bytes.extend(self.Reserve.to_bytes())
        bytes.extend(self.AxisJointUsed.to_bytes())
        bytes.extend(self.AxisExternalUsed.to_bytes())
        bytes.extend(self.AxisJointUnit.to_bytes())
        bytes.extend(self.AxisExternalUnit.to_bytes())
        bytes.extend(self.RCSupportedFunctions)
        bytes.extend(self.Reserve2.to_bytes())
        bytes.extend(self.RobotID.to_bytes())
        bytes.extend(self.InterpreterCycleTime.to_bytes())
        
        return bytes    