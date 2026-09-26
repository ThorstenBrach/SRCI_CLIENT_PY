"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteFrameDataParCmd
Author:      Thorsten Brach
Date:        2026-01-11

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
from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Structures.Data.Frame.FrameData import FrameData

class WriteFrameDataParCmd(IEC_Struct):



    FrameNo            : int
    """
    Frame index M
     • 0: WCS (default) O
     • 1..254: UCS (User frames)
    """

    FrameData          : FrameData
    """Frame data (see chapter 5.5.6.2)"""

