"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ControlHalfByte
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

from RobotLibrary.IEC_Types import BYTE, BYTEEnum

class ControlHalfByte(BYTEEnum):

    NONE = 0
    """
    Default value, no control active
    """

    INITIALIZE = 1
    """
    Initialization is requested by the client
    """
    
    RESUME = 2
    """
    Resume of operation is requested by the client
    """
    
    RESET = 3
    """
    Resetting of the RC is requested by the client. The RC must stop the motion, and clear all state.
    """
    
    ACK_ERROR = 4
    """
    Acknowledgement of a telegram state error
    """
    
    CLIENT_ERROR = 5
    """
    Signaling that a client error occurred. The Server must respond by setting its RI state to NOT_INITIALIZED
    """
    
    # Set enum size for ctypes evaluation
    setattr(BYTEEnum, 'ctypes_type', BYTE)        