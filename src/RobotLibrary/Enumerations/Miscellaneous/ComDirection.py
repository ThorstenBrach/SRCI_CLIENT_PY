"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ComDirection
Author:      Thorsten Brach
Date:        2025-12-13

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

from RobotLibrary.IEC_Types import INT, INTEnum

class ComDirection(INTEnum):

    PLC_TO_ROB = 0
    """
    Communication direction PLC to Robot
    """

    ROB_TO_PLC = 1
    """
    Communication direction Robot to PLC
    """
    
    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)        