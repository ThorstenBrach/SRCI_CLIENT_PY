"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupCyclic
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
from RobotLibrary.Structures.AxesGroup.Cyclic.AxesGroupCyclicPlcToRob import AxesGroupCyclicPlcToRob
from RobotLibrary.Structures.AxesGroup.Cyclic.AxesGroupCyclicRobToPlc import AxesGroupCyclicRobToPlc


class AxesGroupCyclic(IEC_Struct):
    PlcToRob: AxesGroupCyclicPlcToRob
    """Cyclic data from PLC to Robot"""

    RobToPlc: AxesGroupCyclicRobToPlc
    """Cyclic data from Robot to PLC"""