"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SyncReaction
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

class SyncReaction(USINTEnum):

    NO_REACTION = 0
    """
    System behavior unaffected
    """

    NO_AUTOMATIC_DISABLE = 1
    """
    No automatic disable\n
    Reaction will only apply when RA is disabled\n
    RA can only be enabled if client and server are synchronized
    """

    INTERRUPT_WHEN_SEQUENCE_IS_EMPTY = 2
    """
    No automatic disable\n
    RA can only be enabled if client and server are synchronized\n
    RA sequence state will change to interrupted when no command is buffered in the active sequence\n
    Continuation is only possible if client and server are synchronized
    """

    IMMEDIATE_INTERRUPT = 3
    """
    No automatic disable\n
    RA can only be enabled if client and server are synchronized\n
    RA sequence state will change to interrupted\n
    Continuation is only possible if client and server are synchronized
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)