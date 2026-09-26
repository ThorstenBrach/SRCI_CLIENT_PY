"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      rmConfigParameter
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

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Enumerations.ArmConfig.ArmConfigShoulder import  ArmConfigShoulder
from RobotLibrary.Enumerations.ArmConfig.ArmConfigElbow import  ArmConfigElbow
from RobotLibrary.Enumerations.ArmConfig.ArmConfigWrist import  ArmConfigWrist

class ArmConfigParameter(IEC_Struct):

    Shoulder : ArmConfigShoulder
    """
    Configuration of shoulder
    """
      
    Elbow    : ArmConfigElbow
    """
    Configuration of elbow
    """

    Wrist    : ArmConfigWrist
    """ 
    Configuration of wrist
    """