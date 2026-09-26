"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      JogControl
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

from RobotLibrary.IEC_Types import IEC_Struct

class JogControl(IEC_Struct):
    X_J1_Pos: bool
    """
    Mode Frame : Movement in positive direction X of selected frame
    Mode Tool  : Movement in positive direction X of selected tool
    Mode Axes  : Movement in positive direction joint 1
    """

    X_J1_Neg: bool
    """
    Mode Frame : Movement in negative direction X of selected frame
    Mode Tool  : Movement in negative direction X of selected tool
    Mode Axes  : Movement in negative direction joint 1
    """

    Y_J2_Pos: bool
    """
    Mode Frame : Movement in positive direction Y of selected frame
    Mode Tool  : Movement in positive direction Y of selected tool
    Mode Axes  : Movement in positive direction joint 2
    """

    Y_J2_Neg: bool
    """
    Mode Frame : Movement in negative direction Y of selected frame
    Mode Tool  : Movement in negative direction Y of selected tool
    Mode Axes  : Movement in negative direction joint 2
    """

    Z_J3_Pos: bool
    """
    Mode Frame : Movement in positive direction Z of selected frame
    Mode Tool  : Movement in positive direction Z of selected tool
    Mode Axes  : Movement in positive direction joint 3
    """

    Z_J3_Neg: bool
    """
    Mode Frame : Movement in negative direction Z of selected frame
    Mode Tool  : Movement in negative direction Z of selected tool
    Mode Axes  : Movement in negative direction joint 3
    """

    Rx_J4_Pos: bool
    """
    Mode Frame : Movement in positive direction Rx of selected frame
    Mode Tool  : Movement in positive direction Rx of selected tool
    Mode Axes  : Movement in positive direction joint 4
    """

    Rx_J4_Neg: bool
    """
    Mode Frame : Movement in negative direction Rx of selected frame
    Mode Tool  : Movement in negative direction Rx of selected tool
    Mode Axes  : Movement in negative direction joint 4
    """

    Ry_J5_Pos: bool
    """
    Mode Frame : Movement in positive direction Ry of selected frame
    Mode Tool  : Movement in positive direction Ry of selected tool
    Mode Axes  : Movement in positive direction joint 5
    """

    Ry_J5_Neg: bool
    """
    Mode Frame : Movement in negative direction Ry of selected frame
    Mode Tool  : Movement in negative direction Ry of selected tool
    Mode Axes  : Movement in negative direction joint 5
    """

    Rz_J6_Pos: bool
    """
    Mode Frame : Movement in positive direction Rz of selected frame
    Mode Tool  : Movement in positive direction Rz of selected tool
    Mode Axes  : Movement in positive direction joint 6
    """

    Rz_J6_Neg: bool
    """
    Mode Frame : Movement in negative direction Rz of selected frame
    Mode Tool  : Movement in negative direction Rz of selected tool
    Mode Axes  : Movement in negative direction joint 6
    """

    E1_Pos: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in positive direction first external axis
    """

    E1_Neg: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in negative direction first external axis
    """

    E2_Pos: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in positive direction second external axis
    """

    E2_Neg: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in negative direction second external axis
    """

    E3_Pos: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in positive direction third external axis
    """

    E3_Neg: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in negative direction third external axis
    """

    E4_Pos: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in positive direction fourth external axis
    """

    E4_Neg: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in negative direction fourth external axis
    """

    E5_Pos: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in positive direction fifth external axis
    """

    E5_Neg: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in negative direction fifth external axis
    """

    E6_Pos: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in positive direction sixth external axis
    """

    E6_Neg: bool
    """
    Mode Frame : not supported
    Mode Tool  : not supported
    Mode Axes  : Movement in negative direction sixth external axis
    """