"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      InitializationState
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

class InitializationState(INTEnum):
    DEFAULT = 0
    """
    Default
    """

    ERROR_TELEGRAM_CONTROL = 161
    """
    Error: Telegram control does not match the telegram state
    """

    ERROR_INIT_LOST = 162
    """
    Error: Initialization lost for unknown reason\nSee message log after reinitializing
    """

    ERROR_TELEGRAM_LENGTH = 163
    """
    Error: Telegram length does not match the length provided in the communication interface
    """

    ERROR_INCOMPATIBLE_SRCI = 164
    """
    Error: Incompatible major SRCI version
    """

    ERROR_LIFESIGN_TIMEOUT = 165
    """
    Error: Lifesign timeout
    """

    ERROR_CYCLIC_DATA_MISMATCH = 166
    """
    Error: The selected optional cyclic data does not fit in the given telegram size
    """

    ERROR_INTERFACE_RESET = 167
    """
    Error: The robot interface was reset after being initialized
    """

    ERROR_SEQUENCE_TIMEOUT = 168
    """
    Error: Telegram sequence timeout
    """

    ERROR_TELEGRAM_NUMBER_CHANGED = 169
    """
    Error: The telegram number changed after initialization
    """

    ERROR_INVALID_AXES_GROUP = 170
    """
    Error: Invalid AxesGroupID
    """

    ERROR_INVALID_TELEGRAM_NUMBER = 171
    """
    Error: Telegram number is invalid\n
    E.g. TwoSequences is only activated in one direction
    """

    ERROR_TELEGRAM_NUMBER_NOT_SUPPORTED = 172
    """
    Error: Telegram Number is not supported
    """

    READY_TO_RESUME = 253
    """
    Ready to resume\n
    The RC is currently not initialized but has state in the ACR
    """

    READY_FOR_INITIALIZATION = 254
    """
    Ready for initialization\n
    The RC is currently not initialized and has no state in the ACR"""

    INITIALIZED = 255
    """
    Initialized\n
    The RC state is Initialized
    """
    
    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)    