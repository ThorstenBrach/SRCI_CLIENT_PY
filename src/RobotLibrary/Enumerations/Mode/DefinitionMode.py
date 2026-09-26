"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      DefinitionMode
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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class DefinitionMode(USINTEnum):
    Center = 1
    """
    ZeroPoint describes center point of body 
    """

    Face = 2
    """
    ZeroPoint describes point on face of body. Parameter values for X2, Y2, Z2 will be ignored  
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    