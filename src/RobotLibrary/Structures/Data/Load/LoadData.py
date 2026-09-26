"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      LoadData
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
from RobotLibrary.IEC_Types import USINT, REAL, IEC_Struct
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP
    
class LoadData(IEC_Struct):
  
    Timestamp : IEC_TIMESTAMP
    """
    Timestamp
    """

    X : REAL
    """
    Origin of the coordinate system relative to the BCS/WCS/UCS 
    X value [mm]
    """

    Y : REAL
    """
    Origin of the coordinate system relative to the BCS/WCS/UCS 
    Y value [mm]
    """

    Z : REAL
    """
    Origin of the coordinate system relative to the BCS/WCS/UCS 
    Z value [mm]
    """

    Rx : REAL
    """
    Orientation of the coordinate system relative to the BCS/WCS/UCS
    Rx value [°]
    """

    Ry : REAL
    """
    Rx value [°]
    """

    Rz : REAL
    """
    Rx value [°]
    """

    Mass : REAL
    """
    The mass of the tool and workpiece being gripped. [kg]
    """
    
    Ix : REAL
    """
    The moment of inertia of the load around the resulting inertia X-Axis [kg/m²]
    """
    
    Iy : REAL
    """
    The moment of inertia of the load around the resulting inertia y-axis [kg/m²]
    """

    Iz : REAL
    """ 
    The moment of inertia of the load around the resulting inertia z-axis [kg/m²]
    """