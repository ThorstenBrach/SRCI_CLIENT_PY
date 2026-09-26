"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TriggerModeMeasurement
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

class TriggerModeMeasurement(USINTEnum):
    NO_TRIGGER = 0
    """
    (default) No trigger related behavior
    """

    POSITIVE_START_NEGATIVE_STOP = 1
    """
    1: Starts the measurement with the positive trigger event and stops it with the negative trigger event\n
    when the trigger function with the identical EmitterID is activated
    """

    POSITIVE_START_STOP = 2
    """
    2: Starts and stops the measurement with the positive trigger event\n
    when the trigger function with the identical EmitterID is activated
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    