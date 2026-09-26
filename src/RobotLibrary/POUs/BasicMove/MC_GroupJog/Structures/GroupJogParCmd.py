"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      GroupJogParCmd
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
from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Enumerations.Mode.JogMode import JogMode
from RobotLibrary.Structures.Miscellaneous.JogControl import JogControl 

class GroupJogParCmd(IEC_Struct):
  
    Mode                   : JogMode
    """Specifies in which mode the robot is jogged"""

    """
    Velocity in % of monitoring speed or ReferenceVelocity, depending on the currently active operation mode
    (T1 External/T2 External: Monitoring speed; Automatic External: ReferenceVelocity )
     •    0%: No movement of the robot
     •   10%: default
     • ≤100%: use input parameter value
    """
    Override               : int

    """Change to jog and define direction according to Mode. See Table 6-223"""
    Control                : JogControl

    """
    Relates to Mode 0 (JogFrame) and 1 (JogTool) Index of tool
     •      0: Flange (default):
     • 1..254: Tool frames
    """
    ToolNo                 : int

    """
    Relates to Mode 0 (JogFrame) Index of frame
     •      0: WCS (default)
     • 1..254: User frames
    """
    FrameNo                : int

    """Increments for jogging translational axes for defined distance
     •  0: Incremental mode OFF (default) - Movement is active until "Control" is reset, or error occurs.
     • >0: Incremental mode ON            - Movement is active until distance defined by input value is reached without changes to "Control", "Control" is reset, or error occurs
    """
    IncrementalTranslation : float

    """ Increments for jogging rotational axes for defined distance
     • 0: Incremental mode OFF (default) - Movement is active until "Control" is reset, or error occurs.
     • >0 Incremental mode ON:           - Movement is active until distance defined by input value is reached without changes to "Control", "Control" is reset, or error occurs
    """
    IncrementalRotation    : float
    
    #-------------------------------------------
    # Constructor
    # #-----------------------------------------
    def __init__(self, **kwargs: Any) -> None:
        
        super().__init__(**kwargs)
        
        self.Mode                   = JogMode.JOG_AXES
        self.Override               = int(5)
        self.Control                = JogControl()
        self.ToolNo                 = int(0)
        self.FrameNo                = int(0)
        self.IncrementalTranslation = float(0.0)
        self.IncrementalRotation    = float(0.0)
