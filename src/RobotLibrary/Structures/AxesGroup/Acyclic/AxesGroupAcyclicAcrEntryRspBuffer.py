"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupAcyclicAcrEntryRspBuffer
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

from RobotLibrary.IEC_Types import BYTE, UDINT, SINT, UINT, DWORD, IEC_Struct, USINT
from RobotLibrary.Functions.Convert import GetHalfeByteHi, GetHalfeByteLo
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Enumerations.State.BufferStateRsp import BufferStateRsp
from RobotLibrary.Parameter import RESPONSE_PAYLOAD_MAX

from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Enumerations.Miscellaneous.Severity  import Severity



class AxesGroupAcyclicAcrEntryRspBuffer(IEC_Struct):
    Timestamp: SystemTime
    """Timestamp"""

    State: BufferStateRsp
    """Buffer state"""

    Payload : bytearray = bytearray(RESPONSE_PAYLOAD_MAX)
    """
    Payload defined by type per CMD definition.
    Processed by Application Layer Task.
    Size: 0..RobotLibraryParameter.RESPONSE_PAYLOAD_MAX
    """

    PayloadLen: UDINT
    """Payload length"""

    PayLoadPtr: DWORD
    """Payload pointer"""      
   
    
    # --------------------------------------------------------
    # GetRspHeaderFromPayload - get response header from payload
    # --------------------------------------------------------
    def GetRspHeaderFromPayload(self) -> RspHeader:
        """Get the header part of the response data."""
        
        # temporaty response header
        _rspHeader : RspHeader = RspHeader()
        # temporary byte value
        _tmpByte   : BYTE = BYTE(0)
        # temporary sint value
        _tmpSint   : SINT = SINT(0)
        # temporary uint value
        _tmpUint   : UINT = UINT(0)


        # Get State, ParSeq from payload
        _tmpByte = BYTE.from_buffer(self.Payload[0:1])
        # Set State in header
        _rspHeader.State                = CmdMessageState(GetHalfeByteLo(_tmpByte).value)
        # Set ParSeq in header
        _rspHeader.ParSeq.value         =                 GetHalfeByteHi(_tmpByte).value
       
         # Get AlarmMessageSeverity from payload
        _tmpSint = SINT.from_buffer(self.Payload[1:2])
        # Set AlarmMessageSeverity in header
        _rspHeader.AlarmMessageSeverity = Severity       (_tmpSint.value)
        
        # Get AlarmMessageCode from payload
        _tmpUint = UINT.from_buffer(self.Payload[2:4])
        # Set AlarmMessageCode in header
        _rspHeader.AlarmMessageCode = _tmpUint

        return _rspHeader
        