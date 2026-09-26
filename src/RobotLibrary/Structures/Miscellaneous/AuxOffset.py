"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AuxOffset
Author:      Thorsten Brach
Date:        2025-12-20

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

from RobotLibrary.IEC_Types import REAL, IEC_Struct

class AuxOffset(IEC_Struct):
    X: REAL
    """Offset in X-direction"""

    Y: REAL
    """Offset in Y-direction"""

    Z: REAL
    """Offset in Z-direction"""

    Rx: REAL
    """Offset in Rx-direction"""

    Ry: REAL
    """Offset in Ry-direction"""

    Rz: REAL
    """Offset in Rz-direction"""