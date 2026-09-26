"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotAxesFlags
Author:      Thorsten Brach
Date:        2025-12-18

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
from RobotLibrary.IEC_Types import BOOL,IEC_Struct

class RobotAxesFlags(IEC_Struct):
    Bit00: BOOL
    """Bit 00 : Not used"""

    AxisJ1: BOOL
    """Bit 01 : Robot axis J1 - property depends of usage"""

    AxisJ2: BOOL
    """Bit 02 : Robot axis J2 - property depends of usage"""

    AxisJ3: BOOL
    """Bit 03 : Robot axis J3 - property depends of usage"""

    AxisJ4: BOOL
    """Bit 04 : Robot axis J4 - property depends of usage"""

    AxisJ5: BOOL
    """Bit 05 : Robot axis J5 - property depends of usage"""

    AxisJ6: BOOL
    """Bit 06 : Robot axis J6 - property depends of usage"""

    Bit07: BOOL
    """Bit 07 : Not used"""