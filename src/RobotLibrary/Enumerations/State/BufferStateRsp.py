"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      BufferStateRsp
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

class BufferStateRsp(INTEnum):
    EMPTY = 0
    """
    EMPTY
    """

    RECEIVING = 1
    """
    RECEIVING
    """

    RECEIVED = 2
    """
    RECEIVED
    """

    PROCESSED = 3
    """
    PROCESSED
    """

    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)