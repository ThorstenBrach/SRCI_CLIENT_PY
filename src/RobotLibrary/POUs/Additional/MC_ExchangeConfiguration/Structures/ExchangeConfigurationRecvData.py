"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ExchangeConfigurationRecvData
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

from RobotLibrary.IEC_Types import BOOL, BYTE, UINT, USINT, UDINT
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.Miscellaneous.DataInSync import DataInSync

class ExchangeConfigurationRecvData(RspHeader):
    """
    Response data structure for exchange configuration.
    """
    
    Enabled: BOOL
    """TRUE when function is exchanging data"""
    
    Reserve1: BYTE
    """Reserve"""
    
    LengthACR: UINT
    """Returns a metric of how many CMDs it can receive and manage at the same time"""
    
    HighestToolIndex: USINT
    """Highest index of available tools on the RC."""
    
    HighestFrameIndex: USINT
    """Highest index of available frames on the RC."""
    
    HighestLoadIndex: USINT
    """Highest index of available loads on the RC."""
    
    HighestWorkAreaIndex: USINT
    """Highest index of available work areas on the RC."""
    
    DataInSync: DataInSync
    """Datas which are synchronized"""
    
    Reserve2: BYTE
    """Reserve"""
    
    ChangeIndexTool: USINT
    """Index of tool changed on RC"""
    
    ChangeIndexFrame: USINT
    """Index of frame changed on RC"""
    
    ChangeIndexLoad: USINT
    """Index of load changed on RC"""
    
    ChangeIndexWorkArea: USINT
    """Index of work area changed on RC"""
    
    RAWorkingHours: UDINT
    """Working hours of an RA connected to the RC"""
    
    StatusByte: BYTE
    """Status byte"""
    
    ConstantVelocitySupported: BOOL
    """Cyclic dynamics status bit ConstantVelocity is supported by RC (see chapter 5.5.3.2)"""
    
    RCWorkingHours: UDINT
    """
    Total system hours of an RA connected to the RC. Must not be modifiable by the user.
    • 0: Invalid
    • >1: Total system hours
    """