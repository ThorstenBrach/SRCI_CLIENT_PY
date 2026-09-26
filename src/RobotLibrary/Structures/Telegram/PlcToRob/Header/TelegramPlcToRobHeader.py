"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRobHeader
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

# region Imports
from RobotLibrary.IEC_Types import BYTE, UINT, IEC_Struct
from RobotLibrary.Structures.DatenAndTime.IEC_DATE import IEC_DATE
from RobotLibrary.Structures.DatenAndTime.IEC_TIME import IEC_TIME
# endregion

#------------------------------------------------------------
# TelegramPlcToRobHeader - Header
#------------------------------------------------------------
class TelegramPlcToRobHeader(IEC_Struct):
  
    SRCIVersion: BYTE
    """
    Version of SRCI specification
    Bit 0-4 : Minor version = Features        (0..31)
    Bit 5-7 : Major version = Breaking change (0..07)
    """

    FastStop_LifeSign: BYTE
    """Fast stop trigger | LifeSign"""

    TelegramLengthPlcToRob: UINT
    """
    Number of bytes of the frame to be used for the telegram
    of the given AxisGroup. Direction client to server
    """

    TelegramLengthRobToPlc: UINT
    """
    Number of bytes of the frame to be used for the telegram
    of the given AxisGroup. Direction server to client
    """

    AxesGroupID_Control: BYTE
    """Control AxesGroupID | Telegram state control"""

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