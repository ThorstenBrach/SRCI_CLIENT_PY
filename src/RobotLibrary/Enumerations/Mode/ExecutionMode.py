"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ExecutionMode
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

class ExecutionMode(USINTEnum):
    SEQUENCE_PRIMARY = 0
    """
    Command is buffered in sequence buffer and executed once
    """

    SEQUENCE_ABORT_OTHERS_PRIMARY = 1
    """
    Command is buffered in sequence buffer,\n
    aborts and empties previous commands in sequence buffer,\n
    and is executed once
    """

    PARALLEL = 2
    """
    Command is buffered in parallel buffer and executed once.\n
    The execution may also be Trigger based
    """

    CONTINUOUS = 3
    """
    Command is buffered in parallel buffer and executed repeatedly\n
    until deliberate deactivation by user.\n
    The de- and activation may also be Trigger based
    """

    TRIGGER_MULTIPLE = 5
    """
    Command is buffered and executed once when triggered.\n
    The CMD remains in the buffer until removed by the user
    """

    SEQUENCE_SECONDARY = 7
    """
    Command is buffered in sequence buffer and executed once (Secondary)
    """

    SEQUENCE_ABORT_OTHERS_SECONDARY = 8
    """
    Command is buffered in sequence buffer,\n
    aborts and empties previous commands in sequence buffer\n
    and is executed once (Secondary)
    """

    STOP_PARALLEL_CONTINUOUS_TRIGGER = 9
    """
    CMD execution is stopped and/or CMD is removed from the buffer
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)