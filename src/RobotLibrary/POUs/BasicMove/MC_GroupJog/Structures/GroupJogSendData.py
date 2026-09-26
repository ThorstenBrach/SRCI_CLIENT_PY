"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      GroupJogSendData
Author:      Thorsten Brach
Date:        2026-01-24

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
from RobotLibrary.IEC_Types import BOOL, BYTE, USINT, REAL, UINT, ARRAY
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Enumerations.Mode.JogMode import JogMode

class GroupJogSendData(CmdHeader):
  
    Enable                 : BOOL
    """Enables jogging of the robot when set to TRUE"""

    Reserve                : BYTE
    """Reserve"""

    ToolNo                 : USINT
    """
    Relates to Mode 0 (JogFrame) and 1 (JogTool) Index of tool
     •      0: Flange (default):
     • 1..254: Tool frames
     """

    FrameNo                : USINT
    """
    Relates to Mode 0 (JogFrame) Index of frame
     •      0: WCS (default)
     • 1..254: User frames
    """

    Mode                   : USINT
    """
    Specifies in which mode the robot is jogged
    """

    Reserve2               : BYTE
    """Reserve"""

    IncrementalTranslation : REAL
    """
    Increments for jogging translational axes for defined distance
    •  0: Incremental mode OFF (default) - Movement is active until "Control" is reset, or error occurs.
    • >0: Incremental mode ON            - Movement is active until distance defined by input value is reached without changes to "Control", "Control" is reset, or error occurs
    """

    IncrementalRotation    : REAL
    """
    Increments for jogging rotational axes for defined distance
    • 0: Incremental mode OFF (default) - Movement is active until "Control" is reset, or error occurs.
    • >0 Incremental mode ON:           - Movement is active until distance defined by input value is reached without changes to "Control", "Control" is reset, or error occurs
    """
    
    Override               : UINT
    """
    Velocity in % of monitoring speed or ReferenceVelocity, depending on the currently active operation mode 
    (T1 External/T2 External: Monitoring speed; Automatic External: ReferenceVelocity )
    •    0%: No movement of the robot
    •   10%: default
    • ≤100%: use input parameter value
    """
    
    JogControl             : ARRAY[BYTE] = ARRAY(0, 2, BYTE)
    """ Change to jog and define direction according to Mode. See Table 6-223 """
    
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
        self.Enable = BOOL(False)
        self.Reserve = BYTE(0)
        self.ToolNo = USINT(0)
        self.FrameNo = USINT(0)
        self.Mode = JogMode.JOG_AXES
        self.Reserve2 = BYTE(0)
        self.IncrementalTranslation = REAL(0.0)
        self.IncrementalRotation = REAL(0.0)
        self.Override = UINT(10)
        self.JogControl = ARRAY(0, 2, BYTE)
        
    
    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:

        bytes = bytearray()

        # header
        bytes.extend(super().GetBytes(order))

        # command data
        bytes.extend(self.Enable.GetBytes(order))
        bytes.extend(self.Reserve.GetBytes(order))
        bytes.extend(self.ToolNo.GetBytes(order))
        bytes.extend(self.FrameNo.GetBytes(order))
        bytes.extend(self.Mode.GetBytes(order))
        bytes.extend(self.Reserve2.GetBytes(order))
        bytes.extend(self.IncrementalTranslation.GetBytes(order))
        bytes.extend(self.IncrementalRotation.GetBytes(order))
        bytes.extend(self.Override.GetBytes(order))
        bytes.extend(self.JogControl[0].GetBytes(order))
        bytes.extend(self.JogControl[1].GetBytes(order))
        bytes.extend(self.JogControl[2].GetBytes(order))
        return bytes
