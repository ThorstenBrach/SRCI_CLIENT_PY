"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SyncInMode
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

class SyncInMode(USINTEnum):
    IN_SYNC_IN_ZONE = 0
    """
    When work piece enters "SyncInZone"\n
    Start synchronization as soon as possible within defined acceleration and velocity limits
    """

    AFTER_DISTANCE = 1
    """
    Start synchronization after specific distance after execution\n
    "SyncInZone" ignored
    """

    AFTER_TIME = 2
    """
    Start synchronization after specific time after execution\n
    "SyncInZone" ignored
    """

    IMMEDIATELY = 3
    """
    As soon as possible within defined acceleration and velocity limits\n
    "SyncInZone" ignored
    """

    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)