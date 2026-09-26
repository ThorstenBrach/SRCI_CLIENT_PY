"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RaSequenceState
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

class RaSequenceState(USINTEnum):
    IDLE = 0
    """
    Robot can be moved by incoming command
    """

    EXECUTING = 1
    """
    RC is processing command in active sequence
    """

    INTERRUPTED = 2
    """
    Interrupt is active\nRobot is waiting for Continue
    """

    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)