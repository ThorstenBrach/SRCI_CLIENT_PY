"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramRobToPlcCommand
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
from RobotLibrary.Parameter import RESPONSE_PAYLOAD_MAX
from RobotLibrary.IEC_Types import BYTE,SINT, UINT, IEC_Struct
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
#endregion 


#-------------------------------------------------------------------------
# TelegramRobToPlcCommandHeader
#-------------------------------------------------------------------------
class TelegramRobToPlcCommandHeader(IEC_Struct):
  
    ParSeq: BYTE
    """Parameter sequence"""

    State: CmdMessageState
    """Message state"""

    AlarmMessageSeverity: SINT
    """Alarm message severity"""

    AlarmMessageCode: UINT
    """Alarm message code"""

#-------------------------------------------------------------------------
# TelegramRobToPlcCommand
#-------------------------------------------------------------------------
class TelegramRobToPlcCommand(IEC_Struct):
  
    Header : TelegramRobToPlcCommandHeader
    """Header"""

    Payload : bytearray = bytearray(RESPONSE_PAYLOAD_MAX)
    """
    Payload    
    """