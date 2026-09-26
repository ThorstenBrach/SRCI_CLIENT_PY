"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TransformMode
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

class TransformMode(SINTEnum):
    MIRROR_AT_POINT = 0
    """
    0 (default): Mirror at Point with mirroring of the target position's orientation\n
    Requires for the mirror Point the "TransformationParameter_1" and the "TransformationParameter_2" set to "Not used"
    """

    MIRROR_AT_STRAIGHT_LINE = 1
    """
    1: Mirror at Straight Line with mirroring of the target position's orientation\n
    Requires for the Straight Line the "TransformationParameter_1" and the "TransformationParameter_2" set to "X-Axis", "Y-Axis" or "Z-Axis"
    """

    MIRROR_AT_PLANE = 2
    """
    2: Mirror at Plane with mirroring of the target position's orientation\n
    Requires for the Plane the "TransformationParameter_1" and the "TransformationParameter_2" set to "XY-Axis", "XZ-Axis" or "YZ-Axis"
    """

    ROTATE_AROUND_STRAIGHT_LINE = 3
    """
    3: Rotate around Straight Line with rotation of the target position's orientation\n
    Requires for the Straight Line the "TransformationParameter_1" and the "TransformationParameter_2" set to "X-Axis", "Y-Axis" or "Z-Axis"\n
    Requires for the parameter "RotationAngle"
    """

    SHIFT_BY_VECTOR = 4
    """
    4: Shift by Vector\n
    Requires for the shifting Vector defined by the Point the "TransformationParameter_1" and the "TransformationParameter_2" set to "Not used"\n
    Requires for the shifting shortest Vector to the Straight Line the "TransformationParameter_1" and the "TransformationParameter_2" set to "X-Axis", "Y-Axis" or "Z-Axis\"\nRequires for the shifting shortest Vector to the Plane the \"TransformationParameter_1\" and the \"TransformationParameter_2\" set to \"XY-Axis", "XZ-Axis" or "YZ-Axis"
    """
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    