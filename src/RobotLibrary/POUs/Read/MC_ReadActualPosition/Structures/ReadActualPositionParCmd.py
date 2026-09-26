"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadActualPositionParCmd
Author:      Thorsten Brach
Date:        2026-01-25

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from typing import Any
from RobotLibrary.IEC_Types import IEC_Struct

class ReadActualPositionParCmd(IEC_Struct):

    ToolNo             : int
    """
    Index of tool of returned position
    •     -1: Currently used tool on RC
    •      0: Flange (default)
    • 1..254: Tool frames
    """
  
    FrameNo            : int
    """
    Index of frame of returned position
    •     -1: Currently used frame on RC
    •      0: WCS (default)
    • 1..254: User frames
    """

    ListenerID         : int
    """
    ID of associated trigger function
    •  0: No Trigger (default) -> No trigger related behavior
    • >0: Trigger              -> Start executing when the trigger function with the identical EmitterID is triggered.
    Always positive. For more information, see chapter 5.5.12 Triggers
    """
    
    def __init__(self, **kwargs: Any) -> None:
        
        super().__init__(**kwargs)
        
        self.ToolNo = 0
        self.FrameNo = 0
        self.ListenerID = 0