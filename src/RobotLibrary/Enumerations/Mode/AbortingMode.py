
"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AbortingMode
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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class AbortingMode(SINTEnum):

    BUFFER = 0
    """
    The current movement command as well as all stored movements are executed as programmed.\n
    The new motion command is queued in the motion buffer.\n
    """

    ABORT = 1
    """
    The current movement command is aborted. All buffered motion movements are discarded.\n
    The new target position is approached, depending on the motion command.\n
    """

    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    
    
# Alias
AbortingModeEnum = AbortingMode 