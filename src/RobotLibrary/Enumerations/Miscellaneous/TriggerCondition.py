"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TriggerCondition
Author:      Thorsten Brach
Date:        2025-12-13

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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class TriggerCondition(SINTEnum):

    TARGET_POSITION_TIME_MS = -5
    """
    5: Time in ms\n
    point reference is target position\n
    """

    TARGET_POSITION_TCP_VELOCITY_ABSOLUTE = -4
    """
    4: TCP velocity in mm/s\n
    point reference is target position\n
    """

    TARGET_POSITION_TCP_VELOCITY_PERCENT = -3
    """
    3: TCP velocity in % of reference velocity\n
    point reference is target position\n
    """

    TARGET_POSITION_DISTANCE_ABSOLUTE = -2
    """
    2: Distance in mm of trajectory\n
    point reference is target position\n
    """

    TARGET_POSITION_DISTANCE_PERCENT = -1
    """
    1: Distance in % of trajectory\n
    point reference is target position\n
    """

    UNDEFINED = 0
    """
    0: Undefined\n
    """

    START_POSITION_DISTANCE_PERCENT = 1
    """
    1: Distance in % of trajectory\n
    point reference is start position\n
    """

    START_POSITION_DISTANCE_ABSOLUTE = 2
    """
    2: Distance in mm of trajectory\n
    point reference is start position\n
    """

    START_POSITION_TCP_VELOCITY_PERCENT = 3
    """
    3: TCP velocity in % of reference velocity\n
    point reference is start position\n
    """

    START_POSITION_TCP_VELOCIT_ABSOLUTE = 4
    """
    4: TCP velocity in mm/s\n
    point reference is start position\n
    """

    START_POSITION_TIME_MS = 5
    """
    5: Time in ms\n
    point reference is start position\n
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)        