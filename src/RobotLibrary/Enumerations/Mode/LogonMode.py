"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      LogonMode
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

class LogonMode(SINTEnum):
    PASSWORD_ONLY = 0
    """
    Password only (default)
    """

    USERNAME_AND_PASSWORD = 1
    """
    Username and Password
    """

    LEVEL_ID_AND_PASSWORD = 2
    """
    Level ID and Password
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)