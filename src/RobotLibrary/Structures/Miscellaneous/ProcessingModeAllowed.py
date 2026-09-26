"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ProcessingModeAllowed
Author:      Thorsten Brach
Date:        2025-12-20

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

from RobotLibrary.IEC_Types import BOOL, IEC_Struct

class ProcessingModeAllowed(IEC_Struct):
    
    BUFFERED: BOOL
    """Command is buffered in sequence buffer and executed once"""

    ABORTING: BOOL
    """
    Command is buffered in sequence buffer, aborts and empties previous commands
    in sequence buffer, and is executed once
    """

    PARALLEL: BOOL
    """Command is buffered in parallel buffer and executed once"""

    CONTINUOUS: BOOL
    """
    Command is buffered in parallel buffer and executed repeatedly
    until deliberate deactivation by user
    """

    DEACTIVATE: BOOL
    """CMD execution is stopped and/or CMD is removed from the buffer"""

    TRIGGER_BUFFERED: BOOL
    """Command is buffered in sequence buffer and executed once (Trigger based)"""

    TRIGGER_ABORTING: BOOL
    """
    Command is buffered in sequence buffer, aborts and empties previous commands
    in sequence buffer, and is executed once (Trigger based)
    """

    TRIGGER_ONCE: BOOL
    """Command is buffered in parallel buffer and executed once (Trigger based)"""

    TRIGGER_CONTINUOUS: BOOL
    """
    Command is buffered in parallel buffer and executed repeatedly
    until deliberate deactivation by user (Trigger based)
    """

    TRIGGER_MULTIPLE: BOOL
    """
    Command is buffered and executed multiple times when triggered.
    The CMD remains in the buffer until removed by the user.
    """