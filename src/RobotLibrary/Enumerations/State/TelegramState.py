"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramState
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

class TelegramState(USINTEnum):
    UNDEFINED = 0
    """
    Default
    """

    ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE = 161
    """
    Telegram control does not match the telegram state
    """

    ERROR_162_INIT_LOST_UNKNOWN = 162
    """
    Initialization lost for unknown reason\n
    See message log after reinitializing
    """

    ERROR_163_TELEGRAM_LENGTH_MISMATCH = 163
    """
    Telegram length does not match the length provided in the communication interface
    """

    ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE = 164
    """
    Incompatible major SRCI version
    """

    ERROR_165_LIFESIGN_TIMEOUT = 165
    """
    Lifesign timeout
    """

    ERROR_166_CYCLIC_DATA_TOO_LARGE = 166
    """
    The selected optional cyclic data does not fit in the given telegram size
    """

    ERROR_167_INTERFACE_WAS_RESET_AFTER_INIT = 167
    """
    The robot interface was reset after being initialized
    """

    ERROR_168_TELEGRAM_SEQ_TIMEOUT = 168
    """
    Telegram sequence timeout
    """

    ERROR_169_TELEGRAM_NO_CHANGED_AFTER_INIT = 169
    """
    The telegram number changed after initialization
    """

    ERROR_170_AXESGROUP_ID_INVALID = 170
    """
    Invalid AxesGroupID
    """

    ERROR_171_TELEGRAM_NUMBER_INVALID = 171
    """
    Telegram number is invalid\n
    E.g. TwoSequences is only activated in one direction
    """

    ERROR_172_TELEGRAM_NUMBER_NOT_SUPPORTED = 172
    """
    Telegram Number is not supported
    """

    ERROR_173_SERVER_CONNECTION_LOST = 173
    """
    Server connection lost
    """

    READY_TO_RESUME = 253
    """
    The RC is currently not initialized but has state in the ACR
    """

    READY_FOR_INITIALIZATION = 254
    """
    The RC is currently not initialized and has no state in the ACR
    """

    INITIALIZED = 255
    """
    The RC state is Initialized
    """

    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)