"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ActiveCommandRegisterState
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

class ActiveCommandRegisterState(INTEnum):
    IS_FREE = 0
    """
    IS_FREE\n
    Denotes not used but available resources\n(empty slots in the ACR)
    """

    IS_PROCESSING = 1
    """
    IS_PROCESSING\n
    CMDs are actively being processed by client or server\nIncludes commands waiting in the sequence buffer\n
    (not currently ACTIVE)
    """

    IS_FINAL = 2
    """
    IS_FINAL\n
    State reached on CMD termination\n
    Execution of this task has finished and results can be examined
    """

    # Set enum size for ctypes evaluation
    setattr(INTEnum, 'ctypes_type', INT)