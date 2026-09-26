"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ExecutionModeAllowed
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

class ExecutionModeAllowed(IEC_Struct):
    PRIMARY_SEQ: BOOL
    """Primary Sequence"""

    PRIMARY_SEQ_ABORT: BOOL
    """Primary Sequence abort"""

    SECONDARY_SEQ: BOOL
    """Secondary Sequence"""

    SECONDARY_SEQ_ABORT: BOOL
    """Secondary Sequence abort"""

    PAR: BOOL = True #type: ignore
    """ Parallel"""

    PAR_TASK: BOOL
    """ Parallel tasl"""

    PAR_TRIGGER: BOOL
    """ Prallel trigger"""

    PAR_TRIGGER_TASK : BOOL
    """ Parallel trigger task"""