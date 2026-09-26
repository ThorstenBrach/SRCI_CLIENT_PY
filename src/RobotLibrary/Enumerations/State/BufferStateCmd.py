"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      BufferStateCmd
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

from RobotLibrary.IEC_Types import INT, INTEnum

class BufferStateCmd(INTEnum):
    EMPTY = 0
    """
    EMPTY
    """

    CREATED = 1
    """
    CREATED
    """

    UPDATE_AVAILABLE = 2
    """
    UPDATE_AVAILABLE
    """

    SENDING = 3
    """
    SENDING
    """

    PROCESSED = 4
    """
    PROCESSED
    """
    
    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)    