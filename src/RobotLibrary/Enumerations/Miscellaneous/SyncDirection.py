"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SyncDirection
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

class SyncDirection(INTEnum):

    NO_SYNC = 0
    """
    No synchronization will be executed
    """

    PLC_TO_ROB = 1
    """
    Server data will be overwritten immediately by client data
    """

    ROB_TO_PLC = 2
    """
    Client data will be overwritten immediately by server data
    """

    AUTOMATIC = 3
    """
    Server or client data will be overwritten immediately by changed data
    """
    
    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)        