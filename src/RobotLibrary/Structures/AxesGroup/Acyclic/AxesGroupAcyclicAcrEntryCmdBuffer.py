"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupAcyclicAcrEntryCmdBuffer
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

from RobotLibrary.IEC_Types import IEC_Struct, BYTE, UDINT, UINT
from RobotLibrary.Functions.Convert import GetHalfeByteHi, GetHalfeByteLo
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Enumerations.State.BufferStateCmd import BufferStateCmd
from RobotLibrary.Parameter import PARAMETER_PAYLOAD_MAX
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel


class AxesGroupAcyclicAcrEntryCmdBuffer(IEC_Struct):
    
    Timestamp  : SystemTime
    """Timestamp"""

    State      : BufferStateCmd
    """Buffer state"""

    Payload    : bytearray = bytearray(PARAMETER_PAYLOAD_MAX)
    """
    Payload defined by type per CMD definition.
    Processed by Application Layer Task.
    Size: 0..RobotLibraryParameter.PARAMETER_PAYLOAD_MAX
    """

    PayloadLen : UDINT
    """Payload length"""

    PayLoadPtr : UINT
    """Payload pointer position"""

    # --------------------------------------------------------
    # GetCmdHeaderFromPayload - get command header from payload
    # --------------------------------------------------------
    def GetCmdHeaderFromPayload(self) -> CmdHeader:
        """Get the header part of the command data."""

        # temporaty command header        
        _cmdHeader : CmdHeader= CmdHeader()
        # temporary byte value
        _tmpByte   : BYTE = BYTE(0)
        # temporary uint value
        _tmpUint   : UINT = UINT(0)
        
        
        # Get CmdType from payload
        _tmpUint = UINT.from_buffer(self.Payload[0:2])
        # Set CmdType in header
        _cmdHeader.CmdTyp = CmdType( _tmpUint.value)
        
        # Get ExecMode from payload
        _tmpByte  = BYTE.from_buffer(self.Payload[2:3]) 
        # Set ExecMode in header
        _cmdHeader.ExecMode = ExecutionMode(GetHalfeByteLo(_tmpByte).value)
        
        # Get ParSeq and Priority from payload
        _tmpByte  = BYTE.from_buffer(self.Payload[3:4])
        # Set ParSeq Header
        _cmdHeader.ParSeq   =               GetHalfeByteHi(_tmpByte)        
        # Set Priority Header
        _cmdHeader.Priority = PriorityLevel(GetHalfeByteLo(_tmpByte).value)

        return _cmdHeader