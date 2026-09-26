"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxisJointUnit
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

from RobotLibrary.Enumerations.Miscellaneous.AxisUnit import AxisUnit
from RobotLibrary.IEC_Types import IEC_Struct 
    
class AxisJointUnit(IEC_Struct):
  
  J1 : AxisUnit  
  """ 
  Joint Axis 1 unit
  """

  J2 : AxisUnit  
  """
  Joint Axis 2 unit
  """

  J3 : AxisUnit  
  """
  Joint Axis 3 unit
  """

  J4 : AxisUnit  
  """
  Joint axis 4 unit
  """

  J5 : AxisUnit 
  """
  Joint Axis 5 unit
  """

  J6 : AxisUnit
  """
  Joint Axis 6 unit
  """