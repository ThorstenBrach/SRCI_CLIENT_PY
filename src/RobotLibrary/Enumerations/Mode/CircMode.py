"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      CircMode
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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class CircMode(SINTEnum):
    BORDER = 0
    """
    "AuxPoint" defines a point on the circle crossed on the path from the starting to the end point.
    """

    CENTER = 1
    """
    "AuxPoint" defines the center point of the circle.
    """

    CENTER_WITH_ANGLE = 2
    """
    "AuxPoint" defines the center point of the circle,\n
    "Angle" defines the end position of the circular motion,\n
    and "CircPlane" defines the circle’s plane.
    """

    RADIUS = 3
    """
    "AuxPoint" defines a vector which length is the radius of the circle.\n
    The plane of the circle is defined by the rule of right thumb while the \"AuxPoint\"\n
    defines the spearhead point of the perpendicular.
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)