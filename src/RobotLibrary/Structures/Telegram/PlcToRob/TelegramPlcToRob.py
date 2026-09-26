"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRob
Author:      Thorsten Brach
Date:        2025-12-21

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

#region imports
from RobotLibrary.IEC_Types import ARRAY, IEC_Struct
from RobotLibrary.Structures.Telegram.PlcToRob.Footer.TelegramPlcToRobFooter import TelegramPlcToRobFooter
from RobotLibrary.Structures.Telegram.PlcToRob.Header.TelegramPlcToRobHeader import TelegramPlcToRobHeader
from RobotLibrary.Structures.Telegram.PlcToRob.Cyclic.TelegramPlcToRobCyclicData import TelegramPlcToRobCyclicData
from RobotLibrary.Structures.Telegram.PlcToRob.CyclicOptional.TelegramPlcToRobCyclicOptionalData import TelegramPlcToRobCyclicOptionalData
from RobotLibrary.Structures.Telegram.PlcToRob.Sequence.TelegramPlcToRobSequence import TelegramPlcToRobSequence
#end imports


#-------------------------------------------------------------------------
# TelegramPlcToRob
#-------------------------------------------------------------------------
class TelegramPlcToRob(IEC_Struct):
  
    Header         : TelegramPlcToRobHeader
    """Header"""

    Cyclic         : TelegramPlcToRobCyclicData
    """Cyclic data"""

    CyclicOptional : TelegramPlcToRobCyclicOptionalData
    """Cyclic optional data"""

    Sequence       : ARRAY[TelegramPlcToRobSequence] = ARRAY(0, 1, TelegramPlcToRobSequence)
    """
    Sequence data
    Size: 0..1 (2 elements)
    """  
    Footer         : TelegramPlcToRobFooter
    """Footer"""
