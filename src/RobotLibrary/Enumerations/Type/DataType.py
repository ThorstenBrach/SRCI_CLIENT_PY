"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      DataType
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

class DataType(USINT):
    TYPE_BOOL = 1
    """
    BOOL
    """

    TYPE_BYTE = 2
    """
    BYTE
    """

    TYPE_WORD = 3
    """
    WORD
    """

    TYPE_DWORD = 4
    """
    DWORD
    """

    TYPE_SINT = 5
    """
    SINT
    """

    TYPE_USINT = 6
    """
    USINT
    """

    TYPE_INT = 7
    """
    INT
    """

    TYPE_UINT = 8
    """
    UINT
    """

    TYPE_DINT = 9
    """
    DINT
    """

    TYPE_UDINT = 10
    """
    UDINT
    """

    TYPE_REAL = 11
    """
    REAL
    """

    TYPE_CHAR = 12
    """
    CHAR
    """

    TYPE_CHAR_ARRAY = 13
    """
    CHAR_ARRAY
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)