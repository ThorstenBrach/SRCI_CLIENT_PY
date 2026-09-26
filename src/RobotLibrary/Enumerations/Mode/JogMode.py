"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      JogMode
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

class JogMode(USINTEnum):
    JOG_FRAME = 0
    """
    Jog TCP manually in the given frame (WCS/UCS)\n
    Movement on several coordinate axes simultaneously possible
    """

    JOG_TOOL = 1
    """
    Jog TCP manually in the given tool coordinate system\n
    Movement on several coordinate axes simultaneously possible
    """

    JOG_AXES = 2
    """
    Jog joints manually without referring to a given frame or tool\n
    Movement of several axes simultaneously possible
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    