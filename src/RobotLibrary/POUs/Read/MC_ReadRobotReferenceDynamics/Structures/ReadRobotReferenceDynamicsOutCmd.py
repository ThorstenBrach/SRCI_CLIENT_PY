"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadRobotReferenceDynamicsOutCmd
Author:      Thorsten Brach
Date:        2026-01-12

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Dynamics.ReferenceDynamics import ReferenceDynamics

class ReadRobotReferenceDynamicsOutCmd(IEC_Struct):
    
  DynamicValues : ReferenceDynamics
  """Reference dynamics values according to Table 6-148."""
