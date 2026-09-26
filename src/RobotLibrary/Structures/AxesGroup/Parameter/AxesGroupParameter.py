"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupParameter
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

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.AxesGroup.Parameter.Plc.AxesGroupParameterPlc import AxesGroupParameterPlc
from RobotLibrary.Structures.AxesGroup.Parameter.Rob.AxesGroupParameterRob import AxesGroupParameterRob

class AxesGroupParameter(IEC_Struct):
  
    Plc: AxesGroupParameterPlc
    """PLC specific data"""

    Rob: AxesGroupParameterRob
    """
    RC data read by the function "ReadRobotData"   
    """