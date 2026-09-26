"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupCyclicPlcToRob
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

from RobotLibrary.IEC_Types import BYTE, UINT, INT, IEC_Struct
from RobotLibrary.Structures.Miscellaneous.VersionStruct import VersionStruct
from RobotLibrary.Structures.DatenAndTime.IEC_DATE import IEC_DATE
from RobotLibrary.Structures.DatenAndTime.IEC_TIME import IEC_TIME
from RobotLibrary.Enumerations.Miscellaneous.ControlHalfByte import ControlHalfByte

class AxesGroupCyclicPlcToRob(IEC_Struct):
    
    SRCIVersion: VersionStruct
    """
    Version of SRCI specification
    Bit 0-4 : Minor version = Features        (0..31)
    Bit 5-7 : Major version = Breaking change (0..07)
    """

    FastStop: BYTE
    """Fast stop trigger"""

    LifeSign: BYTE
    """Connection alive signal"""

    TelegramLengthPlcToRob: UINT
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup.
    Direction client to server
    """

    TelegramLengthRobToPlc: UINT
    """
    Number of Bytes of the frame to be used for the telegram of the given Axisgroup.
    Direction server to client
    """

    AxesGroupID: BYTE
    """Control AxesGroupID telegram state control"""

    Control: ControlHalfByte
    """Telegram state control"""

    Reserved: BYTE
    """Reserved for later versions"""

    TelegramNumberPlcToRob: UINT
    """
    Configuration of the optional cyclic data.
    Direction client to server
    """

    TelegramNumberRobToPlc: UINT
    """
    Configuration of the optional cyclic data.
    Direction server to client
    """

    ClientDate: IEC_DATE
    """Date of the client in the format days since 1990.01.01"""

    ClientTime: IEC_TIME
    """Time in the clients time zone in the format milliseconds since start of day"""

    ToolNo: INT
    """
    Index of tool of returned position
     • -1: Currently used tool on RC
     •  0: Flange (default)
     •  1..254: Tool frames
    """

    FrameNo: INT
    """
    Index of frame of returned position
     • -1: Currently used frame on RC
     •  0: WCS (default)
     •  1..254: User frames
    """