"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxisExternalUsed
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

    
class AxisExternalUsed(IEC_Struct):
  
  E1 : BOOL
  """ 
  External Axis 1 used
  """

  E2 : BOOL
  """
  External Axis 2 used
  """

  E3 : BOOL
  """
  External Axis 3 used
  """

  E4 : BOOL
  """
  External axis 4 used
  """

  E5 : BOOL
  """
  External Axis 5 used
  """

  E6 : BOOL
  """
  External Axis 6 used
  """