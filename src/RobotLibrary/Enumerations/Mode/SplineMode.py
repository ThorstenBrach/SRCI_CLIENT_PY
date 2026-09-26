"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SplineMode
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

from RobotLibrary.IEC_Types import UINT, UINTEnum

class SplineMode(UINTEnum):
    DISCRETE_POINTS = 0
    """
    0: Discrete Points
    """

    BEZIER_SPLINE = 1
    """
    1: Bézier Spline
    """

    B_SPLINES = 2
    """
    2: B-Splines
    """

    CUBIC_HERMITE_SPLINE = 3
    """
    3: Cubic Hermite Spline
    """

    C_SPLINES = 4
    """
    4: C-Splines
    """
    
    # Set enum size for ctypes evaluation
    setattr(UINTEnum, 'ctypes_type', UINT)    