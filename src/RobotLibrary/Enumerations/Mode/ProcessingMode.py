"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ProcessingMode
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

class ProcessingMode(USINTEnum):
    BUFFERED = 0
    """
    Command is buffered in sequence buffer and executed once
    """

    ABORTING = 1
    """
    Command is buffered in sequence buffer,\n
    aborts and empties previous commands in sequence buffer,\n
    and is executed once
    """

    PARALLEL = 2
    """
    Command is buffered in parallel buffer and executed once
    """

    CONTINUOUS = 3
    """
    Command is buffered in parallel buffer and executed repeatedly\n
    until deliberate deactivation by user
    """

    DEACTIVATE = 9
    """
    CMD execution is stopped and/or CMD is removed from the buffer
    """

    TRIGGER_BUFFERED = 10
    """
    Command is buffered in sequence buffer and executed once (Trigger based)
    """

    TRIGGER_ABORTING = 11
    """
    Command is buffered in sequence buffer,\n
    aborts and empties previous commands in sequence buffer,\n
    and is executed once (Trigger based)
    """

    TRIGGER_ONCE = 12
    """
    Command is buffered in parallel buffer and executed once (Trigger based)
    """

    TRIGGER_CONTINUOUS = 13
    """
    Command is buffered in parallel buffer and executed repeatedly\n
    until deliberate deactivation by user (Trigger based)
    """

    TRIGGER_MULTIPLE = 14
    """
    Command is buffered and executed multiple times when triggered.\n
    The CMD remains in the buffer until removed by the user
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    
    
ProcessingModeEnum = ProcessingMode