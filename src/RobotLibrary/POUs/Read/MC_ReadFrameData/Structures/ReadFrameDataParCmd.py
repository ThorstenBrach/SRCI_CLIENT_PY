"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadFrameDataParCmd
Author:      Thorsten Brach
Date:        2026-01-05

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

class ReadFrameDataParCmd(IEC_Struct):

    FrameNo   : int
    """
    Frame index\n
     • -1: Currently used frame on RC\n
     • 0: WCS\n
     • 1 (default)..254: UCS (User frames)\n
    """