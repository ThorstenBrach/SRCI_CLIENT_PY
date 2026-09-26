"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRobCommand
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
#region Imports
from RobotLibrary.IEC_Types import BYTE, IEC_Struct, ARRAY
from RobotLibrary.Parameter import PARAMETER_PAYLOAD_MAX
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Enumerations.Type.CmdType import CmdType
#endregion

#------------------------------------------------------------
# TelegramPlcToRobCommandHeader - Command Header
#------------------------------------------------------------
class TelegramPlcToRobCommandHeader(IEC_Struct):
  
    CmdType : CmdType
    """ Command type"""
    
    Prio : PriorityLevel
    """CMD priority level"""
    
    ExecMode : ExecutionMode
    """Execution Mode"""
    
    ParSequence : BYTE    
    """Parameter Sequence"""

#------------------------------------------------------------
# TelegramPlcToRobCommand - Command
#------------------------------------------------------------
class TelegramPlcToRobCommand(IEC_Struct):
    
    Header  : TelegramPlcToRobCommandHeader
    """ Header"""

    Payload : bytearray = bytearray(PARAMETER_PAYLOAD_MAX) 
    """ Payload"""