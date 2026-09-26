"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRobFragment
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
from RobotLibrary.IEC_Types import IEC_Struct, UINT, BYTE
from RobotLibrary.Structures.Telegram.PlcToRob.Command.TelegramPlcToRobCommand import TelegramPlcToRobCommand
#wendregion


#------------------------------------------------------------
# TelegramPlcToRobFragmentHeader - Fragment Header
#------------------------------------------------------------
class TelegramPlcToRobFragmentHeader(IEC_Struct):
  
    CmdID: UINT
    """Command instance identifier used to assign the CMD payload to a specific CMD instance"""

    Reserve: BYTE
    """Empty reserve byte"""

    FragmentAction: BYTE
    """Fragment action byte"""

    PayloadPointer: UINT
    """Append received payload in the receive buffer at this position"""

    PayloadLength: UINT
    """Length of the CMD payload"""




#------------------------------------------------------------
# TelegramPlcToRobFragment - Fragment
#------------------------------------------------------------
class TelegramPlcToRobFragment(IEC_Struct):
    
    Header  : TelegramPlcToRobFragmentHeader
    """Header"""

    Command : TelegramPlcToRobCommand
    """Command"""
