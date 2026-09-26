"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxisExternalUnit
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
    
class AxisExternalUnit(IEC_Struct):
  
  E1 : AxisUnit 
  """ 
  External Axis 1 unit
  """

  E2 : AxisUnit  
  """
  External Axis 2 unit
  """

  E3 : AxisUnit  
  """
  External Axis 3 unit
  """

  E4 : AxisUnit  
  """
  External axis 4 unit
  """

  E5 : AxisUnit 
  """
  External Axis 5 unit
  """

  E6 : AxisUnit
  """
  External Axis 6 unit
  """