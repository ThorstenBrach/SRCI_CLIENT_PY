"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SingularityAvoidanceMode
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

class SingularityAvoidanceMode(USINTEnum):
    NO_CHANGE = 0
    """
    0: NoChange (default)\n
    Allow movement of one or more joints to avoid singularities without a change of the orientation
    """

    LOCK_J4 = 1
    """
    1: Lock J4\n
    Lock the 4th joint to avoid singularities
    """

    TOOL_ORIENTATION = 2
    """
    2: ToolOrientation\n
    Allow a small movement of the tool orientation to avoid singularities
    """

    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)