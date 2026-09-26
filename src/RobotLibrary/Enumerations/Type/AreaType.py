"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AreaType
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

class AreaType(USINTEnum):
    AXES = 0
    """
    0: Axes
    """

    BOX = 1
    """
    1: Box (default)
    """

    CYLINDER = 2
    """
    2: Cylinder
    """

    SPHERE = 3
    """
    3: Sphere (only DefinitionMode 1)
    """

    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)