"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      OperationMode
Author:      Thorsten Brach
Date:        2025-12-14

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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class OperationMode(USINTEnum):
    T1_LOCAL = 1
    """
    Test mode 1 (local)\n
    Maximum velocity of TCP is restricted to <250 mm/s\n
    Robot can only be moved while enable switch is active\n
    Designed for jogging, teaching program, verification\n
    Safety door can be opened
    """

    T2_LOCAL = 2
    """
    Test mode 2 (local)\n
    Maximum velocity of TCP not restricted (100%)\n
    Robot can only be moved while enable switch is active\n
    Designed for program verification (step mode)\n
    Safety door can be opened
    """

    AUTO = 3
    """
    Automatic mode\n
    Maximum velocity of TCP not restricted (100%)\n
    Robot is executing user program automatically\n
    Robot will stop if safety devices report error\n
    (e.g. safety door must be closed)
    """

    AUTO_EXT = 4
    """
    External Automatic mode (PLC mode)\n
    Robot is operated remotely only\n
    Maximum velocity of TCP not restricted (100%)\n
    Robot is executing user program automatically\n
    Jogging possible\n
    Robot will stop if safety devices report error\n
    (e.g. safety door must be closed)
    """

    T1_EXT = 5
    """
    External Test mode 1 (PLC mode with T1 functionality)\n
    Robot is operated remotely only\n
    Maximum velocity of TCP is restricted to <250 mm/s\n
    Robot can only be moved while enable switch is active\n
    Designed for jogging, teaching, program verification\n
    Safety door can be opened
    """

    T2_EXT = 6
    """
    External Test mode 2\n
    Robot is operated remotely only\n
    Maximum velocity of TCP not restricted (100%)\n
    Robot can only be moved while enable switch is active\n
    Designed for jogging, program verification (step mode)\n
    Safety door can be opened
    """
    
        # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)