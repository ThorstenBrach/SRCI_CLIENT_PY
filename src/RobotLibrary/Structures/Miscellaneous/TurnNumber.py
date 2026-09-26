"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TurnNumber
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
from RobotLibrary.IEC_Types import SINT, IEC_Struct


class TurnNumber(IEC_Struct):

  J1Turns : SINT
  """ 
  Turn number of J1
  """
  
  J2Turns : SINT
  """   
  Turn number of J2
  """
  
  J3Turns : SINT
  """
  Turn number of J3
  """
  
  J4Turns : SINT
  """
  Turn number of J4
  """
  
  J5Turns : SINT
  """
  Turn number of J5
  """
  
  J6Turns : SINT
  """ 
  Turn number of J6
  """
  
  E1Turns : SINT  
  """ 
  Turn number of E1
  """