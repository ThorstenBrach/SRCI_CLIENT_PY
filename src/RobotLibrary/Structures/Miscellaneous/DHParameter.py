"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      DHParameter
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

from RobotLibrary.IEC_Types import BOOL, REAL, ARRAY, IEC_Struct

class DHParameter(IEC_Struct):

    Alpha                  : ARRAY[REAL] = ARRAY(0, 6, REAL)
    """DH parameter α for each joint - 0 if not supported"""

    A                      : ARRAY[REAL] = ARRAY(0, 6, REAL)
    """DH parameter A for each joint - 0 if not supported"""

    D                      : ARRAY[REAL] = ARRAY(0, 6, REAL)
    """DH parameter D for each joint - 0 if not supported"""

    Theta                  : ARRAY[REAL] = ARRAY(0, 6, REAL)
    """DH parameter Theta for each joint - 0 if not supported"""

    PositiveJointDirection : ARRAY[BOOL] = ARRAY(0, 6, BOOL)
    """
    Positive joint direction of each joint.
    TRUE when positive joint direction points to the right.
    See also Figure 6-16.
    """

    JointZeroPosition      : ARRAY[REAL] = ARRAY(0, 6, REAL)
    """
    Offset of zero position of joint to zero position suggested by Figure 6-17.
    """