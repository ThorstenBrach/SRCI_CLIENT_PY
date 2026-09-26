"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramRobToPlcSequence
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
from RobotLibrary.IEC_Types import IEC_Struct, ARRAY, UINT  
from RobotLibrary.Parameter import FRAGMENT_MAX
from RobotLibrary.Structures.Telegram.RobToPlc.Fragment.TelegramRobToPlcFragment import TelegramRobToPlcFragment
#endregion

#-------------------------------------------------------------------------
# TelegramRobToPlcSequenceHeader
#-------------------------------------------------------------------------
class TelegramRobToPlcSequenceHeader(IEC_Struct):
  
    SEQ_ACK: UINT
    """Telegram sequence and acknowledgement number"""

    PayloadLength: UINT
    """Length of the telegram sequence excluding this telegram sequence header"""


#-------------------------------------------------------------------------
# TelegramRobToPlcSequence
#-------------------------------------------------------------------------
class TelegramRobToPlcSequence(IEC_Struct):
  
    Header : TelegramRobToPlcSequenceHeader
    """Header"""

    Fragment : ARRAY[TelegramRobToPlcFragment] = ARRAY(0, FRAGMENT_MAX, TelegramRobToPlcFragment)
    """
    Fragment list
    Size: 0..RobotLibraryParameter.FRAGMENT_MAX
    """