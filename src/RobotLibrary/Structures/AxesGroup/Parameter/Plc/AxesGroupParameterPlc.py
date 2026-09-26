"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupParameterPlc
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

from RobotLibrary.IEC_Types import IEC_Struct, UINT, STRING, BOOL
from RobotLibrary.Structures.Miscellaneous.SynchronizationModes import SynchronizationModes
from RobotLibrary.Structures.Miscellaneous.SyncUserInteraction import SyncUserInteraction

#-------------------------------------------------------------------------
# AxesGroupParameterPlcParameter
#-------------------------------------------------------------------------
class AxesGroupParameterPlcParameter(IEC_Struct):
    ManufacturedID: UINT
    """Manufactured ID"""

    OrderID : STRING = STRING(20)
    """Order ID"""

    SerialNumber : STRING = STRING(16)
    """Serial Number"""

    FirmwareVersion : STRING = STRING(8)
    """Firmware Version"""

    InterfaceVersion : STRING = STRING(8)
    """Client Interface Version"""

    SynchronizationModes: SynchronizationModes
    """Synchronization modes"""

    SyncUserInteraction: SyncUserInteraction
    """Synchronization needs user interaction"""


#-------------------------------------------------------------------------
# AxesGroupParameterPlcOptionalCyclic
#-------------------------------------------------------------------------
class AxesGroupParameterPlcOptionalCyclic(IEC_Struct):
    
    UseCallSubprogram: BOOL
    """
    Bit 00:
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC
    called via the function “CallSubprogram”
    """

    UseCartesianPosition: BOOL
    """
    Bit 01:
    Send a short cartesian position with TCP position (X, Y, Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1)
    and corresponding coordinate systems (ToolNo, FrameNo)
    """

    UseJointPosition: BOOL
    """
    Bit 02:
    Send a short axes position with joint values (J1, J2, J3, J4, J5, J6)
    and position of first external axis (E1)
    """

    UseForce: BOOL
    """
    Bit 03:
    Send the force with the divided forces in the individual directions
    (X, Y, Z, RX, RY, RZ)
    """

    Bit04: BOOL
    """Bit 04"""

    Bit05: BOOL
    """Bit 05"""

    Bit06: BOOL
    """Bit 06"""

    Bit07: BOOL
    """Bit 07"""

    UseTwoSequences: BOOL
    """
    Bit 08:
    Set to 1 to define two sequences in one telegram.
    If activated, 2 sequences also have to be activated
    in the ServerClient direction
    """

    UseCartesianPositionExt: BOOL
    """
    Bit 09:
    Send the external axis values for an extended cartesian position
    (E2, E3, E4, E5, E6)
    """

    UseJointPositionExt: BOOL
    """
    Bit 10:
    Send the external axis values for an extended joint position
    (E2, E3, E4, E5, E6)
    """

    Bit11: BOOL
    """Bit 11"""

    Bit12: BOOL
    """Bit 12"""

    Bit13: BOOL
    """Bit 13"""

    Bit14: BOOL
    """Bit 14"""

    Bit15: BOOL
    """Bit 15"""
    

#-------------------------------------------------------------------------
# AxesGroupParameterPlc
#-------------------------------------------------------------------------
class AxesGroupParameterPlc(IEC_Struct):
    
    Parameter: AxesGroupParameterPlcParameter
    """Parameter"""

    OptionalCyclic: AxesGroupParameterPlcOptionalCyclic
    """Optional cyclic"""