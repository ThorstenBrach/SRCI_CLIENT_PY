"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      Telegram
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

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Telegram.PlcToRob.TelegramPlcToRob import TelegramPlcToRob
from RobotLibrary.Structures.Telegram.RobToPlc.TelegramRobToPlc import TelegramRobToPlc

    
class Telegram(IEC_Struct):
  
    PlcToRob : TelegramPlcToRob
    """PLC to Robot"""
    RobToPlc : TelegramRobToPlc
    """Robot to PLC"""
