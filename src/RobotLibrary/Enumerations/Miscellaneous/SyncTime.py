"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SyncTime
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

from RobotLibrary.IEC_Types import DINT, DINTEnum

class SyncTime(DINTEnum):

    DURING_START_UP = 0
    """
    Synchronization during startup
    """

    AFTER_START_UP = 1
    """
    Synchronization after startup
    """
    # Set enum size for ctypes evaluation
    setattr(DINTEnum, 'ctypes_type', DINT)        