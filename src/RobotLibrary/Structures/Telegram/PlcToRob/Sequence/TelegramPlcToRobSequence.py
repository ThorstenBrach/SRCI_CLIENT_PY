"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRobSequence
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
# region Imports
from RobotLibrary.IEC_Types import ARRAY, IEC_Struct,UINT
from RobotLibrary.Parameter import FRAGMENT_MAX
from RobotLibrary.Structures.Telegram.PlcToRob.Fragment.TelegramPlcToRobFragment import TelegramPlcToRobFragment
# endregion


#------------------------------------------------------------
# TelegramPlcToRobSequenceHeader - Sequence Header
#------------------------------------------------------------
class TelegramPlcToRobSequenceHeader(IEC_Struct):
  
    SEQ_ACK: UINT
    """Telegram sequence and acknowledgement number"""

    PayloadLength: UINT
    """Length of the telegram sequence excluding this telegram sequence header"""


#------------------------------------------------------------
# TelegramPlcToRobSequence - Sequence
#------------------------------------------------------------
class TelegramPlcToRobSequence(IEC_Struct):
  
    Header: TelegramPlcToRobSequenceHeader
    """Header"""

    Fragment : ARRAY[TelegramPlcToRobFragment] = ARRAY(0, FRAGMENT_MAX, TelegramPlcToRobFragment)
    """
    Fragment list
    Size: 0..RobotLibraryParameter.FRAGMENT_MAX
    """