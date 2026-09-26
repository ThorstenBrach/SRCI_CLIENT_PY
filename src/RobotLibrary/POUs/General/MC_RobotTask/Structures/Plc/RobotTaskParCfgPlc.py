"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotTaskParCfgCom
Author:      Thorsten Brach
Date:        2026-01-06

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

from RobotLibrary.Structures.AxesGroup.Parameter.Plc.AxesGroupParameterPlc import AxesGroupParameterPlcOptionalCyclic, AxesGroupParameterPlcParameter
from RobotLibrary.IEC_Types import IEC_Struct


class RobotTaskParCfgPlcParameter(AxesGroupParameterPlcParameter):
    pass


class RobotTaskParCfgPlc(IEC_Struct):
    
    CycleTime      : int = 10
    """PLC cycle time"""
    Parameter      : RobotTaskParCfgPlcParameter
    """parameter"""
    OptionalCyclic : AxesGroupParameterPlcOptionalCyclic
    """Configuration of optional cyclic data send to the Robot"""
