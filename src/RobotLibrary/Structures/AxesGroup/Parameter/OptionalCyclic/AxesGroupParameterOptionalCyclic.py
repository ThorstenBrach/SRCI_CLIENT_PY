"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupParameterOptionalCyclic
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

#region Imports
from RobotLibrary.IEC_Types import IEC_Struct, BOOL
#endregion


#-------------------------------------------------------------------------
# AxesGroupParameterOptionalCyclicPlcToRob
#-------------------------------------------------------------------------
class AxesGroupParameterOptionalCyclicPlcToRob(IEC_Struct):
  
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
# AxesGroupParameterOptionalCyclicRobToPlc
#-------------------------------------------------------------------------
class AxesGroupParameterOptionalCyclicRobToPlc(IEC_Struct):
  
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

    UseCurrent: BOOL
    """
    Bit 04:
    Transmit actual axes current of individual axes
    (J1, J2, J3, J4, J5, J6)
    """

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

    UseForceExt: BOOL
    """
    Bit 11:
    Transmit the current force for the external axes
    (E1, E2, E3, E4, E5, E6)
    """

    UseCurrentExt: BOOL
    """
    Bit 12:
    Transmit the actual current for the external axes
    (E1, E2, E3, E4, E5, E6)
    """

    Bit13: BOOL
    """Bit 13"""

    Bit14: BOOL
    """Bit 14"""

    Bit15: BOOL
    """Bit 15"""


#-------------------------------------------------------------------------
# AxesGroupParameterOptionalCyclic
#-------------------------------------------------------------------------
class AxesGroupParameterOptionalCyclic(IEC_Struct):
  
    PlcToRob : AxesGroupParameterOptionalCyclicPlcToRob
    """ Configuration of optional cyclic data send to the Robot"""

    RobToPlc : AxesGroupParameterOptionalCyclicRobToPlc
    """ Configuration of optional cyclic data received from the Robot"""