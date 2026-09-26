"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotTaskParCfg
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

from RobotLibrary.IEC_Types import IEC_Struct
from.Com.RobotTaskParCfgCom import RobotTaskParCfgCom
from.Plc.RobotTaskParCfgPlc import RobotTaskParCfgPlc
from.Rob.RobotTaskParCfgRob import RobotTaskParCfgRob

class RobotTaskParCfg(IEC_Struct):

    Com    : RobotTaskParCfgCom
    """Common parameter"""
    Plc    : RobotTaskParCfgPlc
    """PLC parameter"""
    Rob    : RobotTaskParCfgRob     
    """Robot parameter"""
