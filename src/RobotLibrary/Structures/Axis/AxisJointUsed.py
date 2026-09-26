"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxisJointUsed
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

from RobotLibrary.IEC_Types import BOOL, IEC_Struct
    
class AxisJointUsed(IEC_Struct):
  
  J1 : BOOL
  """ 
  Joint Axis 1 used
  """

  J2 : BOOL
  """
  Joint Axis 2 used
  """

  J3 : BOOL
  """
  Joint Axis 3 used
  """

  J4 : BOOL
  """
  Joint axis 4 used
  """

  J5 : BOOL
  """
  Joint Axis 5 used
  """

  J6 : BOOL
  """
  Joint Axis 6 used
  """