"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupCyclicRobToPlc
Author:      Thorsten Brach
Date:        2025-12-20

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

from RobotLibrary.IEC_Types import BYTE, UINT, IEC_Struct
from RobotLibrary.Structures.Miscellaneous.VersionStruct import VersionStruct
from RobotLibrary.Structures.Miscellaneous.RaStatusWord import RaStatusWord
from RobotLibrary.Enumerations.State.TelegramState import TelegramState

class AxesGroupCyclicRobToPlc(IEC_Struct):
    
    SRCIVersion: VersionStruct
    """
    Version of SRCI specification
    Bit 0-4 : Minor version = Features        (0..31)
    Bit 5-7 : Major version = Breaking change (0..07)
    """

    LifeSign: BYTE
    """Connection alive signal"""

    Reserved: BYTE
    """Reserved byte"""

    TelegramState: TelegramState
    """Initialization and telegram control state"""

    StatusRobotArm: RaStatusWord
    """Combination of various RA related states"""

    Override: UINT
    """Actual override in percentage encoding"""

    