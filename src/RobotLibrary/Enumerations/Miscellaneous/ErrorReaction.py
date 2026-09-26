"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ErrorReaction
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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class ErrorReaction(USINTEnum):

    ABORT_AND_MOVE = 0
    """
    Abort and move Abort active move command and delete commands buffered in sequence Move robot by specified ErrorVector
    """

    ABORT = 1
    """
    1: Abort\n
    Abort active move command and delete commands buffered in sequence\n
    No additional movements\n
    """
    
    NO_REACTION = 2
    """
    2: No reaction\n
    Error event is ignored by active move command\n
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)