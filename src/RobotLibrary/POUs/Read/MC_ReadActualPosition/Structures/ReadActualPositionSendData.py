"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadActualPositionSendData
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

from RobotLibrary.IEC_Types import USINT , SINT, ARRAY
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader

class ReadActualPositionSendData(CmdHeader):
    """Structure for received data from MoveAxesAbsolute command."""
    
    EmitterID          : ARRAY[SINT] = ARRAY(0, 4, SINT) 
    """
    ID of Action that will be executed when this command is active
     • >0: Start Action - Start executing the Action function with the identical ListenerID.
     • <0: Stop Action  -  Stop executing the Action function with the identical ListenerID.
     • 0: No trigger (default)-  If no EmitterID is defined, the function will not trigger any Action during its execution
    For more information see section Triggers of this chapter or chapter 5.5.12.4.
    """

    ListenerID         : SINT
    """
    ID of the trigger function that may be triggered:
     • 0: Immediately (default). - Start executing THIS function immediately.
     • >0: Triggero Start executing when the trigger function with the identical EmitterID is called.
    For more information see chapter 5.5.12.4.
    """

    Reserve            : SINT
    """Reserve"""

    ToolNo             : USINT
    """
    Index of tool of returned position
     •     -1: Currently used tool on RC
     •      0: Flange (default)
     • 1..254: Tool frames
     """

    FrameNo            : USINT
    """
    Index of frame of returned position
     •     -1: Currently used frame on RC
     •      0: WCS (default)
     • 1..254: User frames
     """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        
        super().__init__()
        self.EmitterID = ARRAY(0, 3, SINT)
        self.ListenerID = SINT(0)
        self.Reserve = SINT(0)
        self.ToolNo = USINT(0)
        self.FrameNo = USINT(0)