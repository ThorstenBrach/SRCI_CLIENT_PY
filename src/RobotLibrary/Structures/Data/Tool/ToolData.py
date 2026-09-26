"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ToolData
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

from RobotLibrary.IEC_Types import USINT, REAL, BOOL, IEC_Struct
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP
    
class ToolData(IEC_Struct):
  
    Timestamp : IEC_TIMESTAMP
    """ Timestamp"""

    ID : USINT
    """
    Identification of physical tool Default: 0 
    """    

    ExternalTCP : BOOL
    """
    True: Tool fixed False: Tool on flange 
    """

    X : REAL
    """
    Origin of the tool coordinate system relative to the flange coordinate system. 
    X value [mm]  
    """

    Y : REAL
    """
    Origin of the tool coordinate system relative to the flange coordinate system. 
    Y value [mm]  
    """

    Z : REAL
    """
    Origin of the tool coordinate system relative to the flange coordinate system. 
    Z value [mm]  
    """

    Rx : REAL
    """
    Orientation of the tool coordinate system relative to the flange coordinate system 
    RX value[°]
    """

    Ry : REAL
    """
    Orientation of the tool coordinate system relative to the flange coordinate system 
    RX value[°]
    """

    Rz : REAL
    """ 
    Orientation of the tool coordinate system relative to the flange coordinate system 
    RX value[°]
    """

    LoadNo : USINT
    """
    Index of the payload Information of tool and workpiece weight, center of gravity and inertia 
    """