"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ErrorTriggerMode
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

class ErrorTriggerMode(SINTEnum):
    ANY_COMMAND = 0
    """
    Any command (default)
    """

    GENERAL_COMMANDS = 1
    """
    General commands
    """

    ADMINISTRATIVE_COMMANDS = 2
    """
    Administrative commands
    """

    MOVE_COMMANDS = 3
    """
    Move commands
    """

    PERIPHERY_COMMANDS = 4
    """
    Periphery commands
    """

    EXTENDED_COMMANDS = 5
    """
    Extended commands
    """

    SPECIFIC_COMMAND_OR_RI_MESSAGE = 6
    """
    Specific command or RI message
    """

    SPECIFIC_RC_OR_RA_MESSAGE_CODE = 7
    """
    Specific RC or RA message code
    """

    ANY_RI_MESSAGE_CODE = 8
    """
    Any RI message code
    """

    ANY_RC_OR_RA_MESSAGE_CODE = 9
    """
    Any RC or RA message code
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    