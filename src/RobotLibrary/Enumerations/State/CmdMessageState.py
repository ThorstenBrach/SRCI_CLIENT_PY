"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      CmdMessageState
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

class CmdMessageState(USINTEnum):
    EMPTY = 0
    """
    No operation or process is active
    """

    CREATED = 1
    """
    Created but not yet started
    """

    BUFFERED = 2
    """
    Buffered and awaiting execution
    """

    BUFFERED_IN_PLANNER = 3
    """
    Buffered in planner for future execution
    """

    ACTIVE = 4
    """
    Currently active and in progress
    """

    INTERRUPTED = 5
    """
    Interrupted and awaiting continuation
    """

    ABORT_REQUEST = 6
    """
    Requested for abort
    """

    DONE = 10
    """
    Successfully completed
    """

    ABORTED = 14
    """
    Aborted before completion
    """

    ERROR = 15
    """
    Encountered an error during execution
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    