"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramRobToPlc
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

from RobotLibrary.IEC_Types import IEC_Struct,ARRAY
from RobotLibrary.Structures.Telegram.RobToPlc.Header.TelegramRobToPlcHeader import TelegramRobToPlcHeader
from RobotLibrary.Structures.Telegram.RobToPlc.CyclicOptional.TelegramRobToPlcCyclicOptionalData import TelegramRobToPlcCyclicOptionalData
from RobotLibrary.Structures.Telegram.RobToPlc.Sequence.TelegramRobToPlcSequence import TelegramRobToPlcSequence
from RobotLibrary.Structures.Telegram.RobToPlc.Footer.TelegramRobToPlcFooter import TelegramRobToPlcFooter

    
class TelegramRobToPlc(IEC_Struct):
  
    Header         : TelegramRobToPlcHeader
    """Telegram header"""

    CyclicOptional : TelegramRobToPlcCyclicOptionalData
    """Cyclic optional data"""

    Sequence       : ARRAY[TelegramRobToPlcSequence] =  ARRAY(0, 1, TelegramRobToPlcSequence)
    """
    Sequence data
    Size: 0..1 (2 elements)
    """

    Footer         : TelegramRobToPlcFooter
    """Footer"""