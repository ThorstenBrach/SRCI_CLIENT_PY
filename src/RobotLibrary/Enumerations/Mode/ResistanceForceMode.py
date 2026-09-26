"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ResistanceForceMode
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

class ResistanceForceMode(USINTEnum):
    RESISTANCE_FORCE_TCP = 0
    """
    0 (default): ResistanceForceTCP.\n
    Set \"0\" to set the resistance of the RA against the external force at the TCP.
    """

    RESISTANCE_FORCE_AXIS = 1
    """
    1: ResistanceForceAxis.\n
    Set \"1\" to set the resistance of the RA against the external force for each axis independently.
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    