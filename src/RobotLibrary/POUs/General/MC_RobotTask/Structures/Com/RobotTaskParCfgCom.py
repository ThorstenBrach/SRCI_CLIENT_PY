"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotTaskParCfgCom
Author:      Thorsten Brach
Date:        2026-01-06

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

class RobotTaskParCfgCom(IEC_Struct):

    LifeSignTimeOut        : int = 5000
    """
    Maximum allowed time between incrementation of LifeSign before communication error.\n
     • <10 ms: Invalid\n
     • 50 ms: default
    """
    TelegramLengthPlcToRob : int = 256
    """Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction client to server"""
    TelegramLengthRobToPlc : int = 256
    """Number of Bytes of the frame to be used for the telegram of the given Axisgroup. Direction server to client"""
    TwoSequences           : bool = False 
    """Use two sequences in telegram ?"""