"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReturnMode
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

from RobotLibrary.IEC_Types import BYTE, BYTEEnum

class ReturnMode(BYTEEnum):
    INTERRUPT_POSITION = 0
    """
    Interrupt position
    """

    END_POSITION = 1
    """
    End position
    """
    
    # Set enum size for ctypes evaluation
    setattr(BYTEEnum, 'ctypes_type', BYTE)    