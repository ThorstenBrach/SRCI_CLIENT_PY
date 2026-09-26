"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      StopMode
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

class StopMode(USINTEnum):
    STOP_JOB_ID = 0
    """
    0: Stop via JobID (default)\n
    TargetID is interpreted as JobID\n
    All instances of the defined JobID are stopped
    """

    STOP_INSTANCE_ID = 1
    """
    1: Stop via InstanceID\n
    TargetID is interpreted as InstanceID\n
    The instance of the defined InstanceID is stopped
    """

    STOP_ALL_SUBPROGRAMS = 2
    """
    2: Stop all subprograms\n
    All subprograms independent of the input parameter value of TargetID are stopped
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    