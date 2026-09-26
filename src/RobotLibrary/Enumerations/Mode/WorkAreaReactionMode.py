"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WorkAreaReactionMode
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

class WorkAreaReactionMode(USINTEnum):
    NO_REACTION = 0
    """
    0: No reaction (default)\n
    • RC reports violation\n
    • Robot is not stopped
    """

    ABORT = 1
    """
    1: Abort\n
    • RC reports violation\n
    • RC returns error\n
    • Robot is stopped\n
    • Sequence buffer emptied
    """

    INTERRUPT = 2
    """
    2: Interrupt\n
    • RC reports violation\n
    • Robot movement is paused\n
    • Movement can be continued by function GroupContinue
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    