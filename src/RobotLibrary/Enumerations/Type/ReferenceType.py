"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReferenceType
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

class ReferenceType(USINTEnum):
    TOOL = 0
    """
    Distance is applied in the Tool coordinate system.
    The setting of the parameter FrameNo will be ignored.
    """

    FRAME = 1
    """
    Distance is applied in the Frame coordinate system.
    The settings of the ToolNo are also effective and must be considered.
    """
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    