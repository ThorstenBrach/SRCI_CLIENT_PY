"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryRecvDataBaseFB
Author:      Thorsten Brach
Date:        2026-01-01

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
import struct
from typing import cast

from RobotLibrary.Enumerations.ArmConfig.ArmConfigShoulder import ArmConfigShoulder
from RobotLibrary.Enumerations.ArmConfig.ArmConfigElbow import ArmConfigElbow 
from RobotLibrary.Enumerations.ArmConfig.ArmConfigWrist import ArmConfigWrist

from RobotLibrary.Structures.DatenAndTime.IEC_DATE import IEC_DATE
from RobotLibrary.Structures.DatenAndTime.IEC_TIME import IEC_TIME


from RobotLibrary.IEC_Types import (
    IEC_POU,
    BOOL,
    BYTE,
    USINT,
    SINT,
    UINT,
    UDINT,
    WORD,
    DWORD,
    INT,
    REAL,
    DATE,
    TOD,
    DT,
    IEC_String,
)
from RobotLibrary.Structures.Miscellaneous.TurnNumber import TurnNumber
from RobotLibrary.Structures.Miscellaneous.ArmConfigParameter import ArmConfigParameter
from RobotLibrary.Structures.Miscellaneous.DataInSync import DataInSync


class RobotLibraryRecvDataBaseFB(IEC_POU):
    """
    Base receiver FB: reads IEC datatypes from an attached payload buffer and
    advances an internal payload pointer.

    Buffer ownership:
    - Derived classes must set `_payload` to the external buffer in `UpdatePointer()`.
    - This base does not allocate or copy; it only reads and advances `PayloadPtr`.
    """

    # VAR_INPUT
    PayloadLen: UDINT = UDINT(0)
    PayloadPtr: UDINT = UDINT(0)

    # VAR (internal)
    _payload : bytearray = bytearray()

    # --------------------------------------------------------
    # Derived classes should link external buffers here
    # --------------------------------------------------------
    def UpdatePointer(self) -> None:
        """
        No-op in base. Derived classes must set `_payload` explicitly, e.g.:

            def UpdatePointer(self):
                self._payload = self.PayLoad
                self.PayloadLen = UDINT(len(self.PayLoad))
        """
        return

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    def _ensure_buffer(self) -> None:
        if self._payload is None:
            self._payload = bytearray()
            self.PayloadLen = UDINT(0)
            self.PayloadPtr = UDINT(0)

    def _read(self, nbytes: int) -> bytes:
        self.UpdatePointer()
        self._ensure_buffer()
        off = int(self.PayloadPtr.value)
        end = min(off + nbytes, len(self._payload))
        data = bytes(self._payload[off:end])
        # advance by requested size (PLC semantics); caller should ensure bounds
        self.PayloadPtr = UDINT(off + nbytes)
        return data

    # --------------------------------------------------------
    # Get methods (mirror PLC FB behavior; big-endian for multi-byte)
    # --------------------------------------------------------
    def GetBool(self) -> BOOL:
        b = self._read(1)
        v = (b[0] & 0x01) != 0 if b else False
        return BOOL(v)

    def GetByte(self) -> BYTE:
        b = self._read(1)
        return BYTE(b[0] if b else 0)

    def GetUsint(self) -> USINT:
        b = self._read(1)
        return USINT(b[0] if b else 0)

    def GetSint(self) -> SINT:
        b = self._read(1)
        val = b[0] if b else 0
        if val > 127:
            val -= 256
        return SINT(val)

    def GetUint(self) -> UINT:
        b = self._read(2)
        val = int.from_bytes(b if len(b) == 2 else b.ljust(2, b"\x00"), "big", signed=False)
        return UINT(val)

    def GetWord(self) -> WORD:
        b = self._read(2)
        val = int.from_bytes(b if len(b) == 2 else b.ljust(2, b"\x00"), "big", signed=False)
        return WORD(val)

    def GetInt(self) -> INT:
        b = self._read(2)
        val = int.from_bytes(b if len(b) == 2 else b.ljust(2, b"\x00"), "big", signed=True)
        return INT(val)

    def GetUdint(self) -> UDINT:
        b = self._read(4)
        val = int.from_bytes(b if len(b) == 4 else b.ljust(4, b"\x00"), "big", signed=False)
        return UDINT(val)

    def GetDword(self) -> DWORD:
        b = self._read(4)
        val = int.from_bytes(b if len(b) == 4 else b.ljust(4, b"\x00"), "big", signed=False)
        return DWORD(val)

    def GetReal(self) -> REAL:
        b = self._read(4)
        if len(b) != 4:
            b = b.ljust(4, b"\x00")
        val = struct.unpack(">f", b)[0]
        return REAL(val)

    def GetIecTime(self) -> IEC_TIME:
        """
        Reads IEC TIME (milliseconds) as big-endian UDINT and
        returns an `IEC_TIME` instance which provides `to_timedelta()` and `to_string()` helpers.
        """
        return cast(IEC_TIME, self.GetUdint())

    def GetTime(self) -> UDINT:
        """
        Reads IEC TIME (milliseconds) as big-endian UDINT.
        Returns an `UDINT` instance to stay consistent with IEC types.
        """
        b = self._read(4)
        val = int.from_bytes(b if len(b) == 4 else b.ljust(4, b"\x00"), "big", signed=False)
        return UDINT(val)

    def GetIecDate(self) -> IEC_DATE:
        """
        Reads IEC DATE (days since 1970-01-01) as big-endian UDINT and
        returns an `IEC_DATE` instance which provides `to_date()` and `to_string()` helpers.
        """        
        return cast(IEC_DATE, self.GetUint())

    def GetDate(self) -> DATE:
        """
        Reads IEC DATE (days since 1970-01-01) as big-endian UDINT and
        returns a `DATE` instance which provides `to_date()` and `to_string()` helpers.
        """
        b = self._read(2)
        val = int.from_bytes(b if len(b) == 2 else b.ljust(2, b"\x00"), "big", signed=False)
        return cast(DATE, DATE(val))

    def GetTimeOfDay(self) -> TOD:
        """
        Reads IEC TIME_OF_DAY (milliseconds since midnight) as big-endian UDINT and
        returns a `TOD` instance which provides `to_time()` and `to_string()` helpers.
        """
        b = self._read(4)
        val = int.from_bytes(b if len(b) == 4 else b.ljust(4, b"\x00"), "big", signed=False)
        return cast(TOD, TOD(val))

    def GetDateAndTime(self) -> DT:
        """
        Reads IEC DATE_AND_TIME/DT as big-endian UDINT and returns a `DT` (alias of UDINT).
        Interpretation (e.g., as POSIX seconds) can vary by PLC; convert externally as needed.
        """
        b = self._read(4)
        val = int.from_bytes(b if len(b) == 4 else b.ljust(4, b"\x00"), "big", signed=False)
        return cast(DT, DT(val))

    def GetDataBlock(self, Size: int, IsString: bool) -> bytes:
        
        if IsString:
            # PLC subtracts the terminator; sending side writes LEN only
            Size = max(0, Size - 1)
        return self._read(Size)

    def GetString(self, Size: INT) -> IEC_String:
        size = max(0, int(Size.value))
        b = self._read(size)
        s = b.decode("ascii", errors="replace")
        return IEC_String(size, s)

    def GetHalfeByte1(self, IncPayloadPtr: bool) -> BYTE:
        # first nibble (low 4 bits) of current byte
        off = int(self.PayloadPtr.value)
        self.UpdatePointer()
        self._ensure_buffer()
        val = self._payload[off] if off < len(self._payload) else 0
        nibble = val & 0x0F
        if bool(IncPayloadPtr):
            self.PayloadPtr = UDINT(off + 1)
        return BYTE(nibble)

    def GetHalfeByte2(self, IncPayloadPtr: bool) -> BYTE:
        # second nibble (high 4 bits) of current byte
        off = int(self.PayloadPtr.value)
        self.UpdatePointer()
        self._ensure_buffer()
        val = self._payload[off] if off < len(self._payload) else 0
        nibble = (val >> 4) & 0x0F
        if bool(IncPayloadPtr):
            self.PayloadPtr = UDINT(off + 1)
        return BYTE(nibble)

    # --------------------------------------------------------
    # Get DataInSync structure
    # --------------------------------------------------------
    def GetDataInSync(self) -> DataInSync :
        
        GetDataInSync = DataInSync()

        GetDataInSync.ToolsInSync = self.GetBool().value
        GetDataInSync.FramesInSync = self.GetBool().value
        GetDataInSync.LoadsInSync = self.GetBool().value
        GetDataInSync.WorkAreasInSync = self.GetBool().value
        GetDataInSync.SoftwareLimitsInSync = self.GetBool().value
        GetDataInSync.DefaultDynamicsInSync = self.GetBool().value
        GetDataInSync.ReferenceDynamicsInSync = self.GetBool().value
        
        return GetDataInSync


    # --------------------------------------------------------
    # Get ArmConfigParameter structure
    # --------------------------------------------------------
    def GetArmConfig(self) -> ArmConfigParameter :
        
        GetArmConfig : ArmConfigParameter = ArmConfigParameter()
        
        # get 1st Byte
        _tmpByte = self.GetByte()

        if ( _tmpByte.Bit[0] ) :
        
            GetArmConfig.Shoulder = ArmConfigShoulder.BACK
        else:
            GetArmConfig.Shoulder = ArmConfigShoulder.FRONT
        

        if ( _tmpByte.Bit[1] ) :
        
            GetArmConfig.Elbow = ArmConfigElbow.DOWN
        else:
            GetArmConfig.Elbow = ArmConfigElbow.UP
        

        if ( _tmpByte.Bit[2] ) :
        
            GetArmConfig.Wrist = ArmConfigWrist.FLIP
        else:
            GetArmConfig.Wrist = ArmConfigWrist.NON_FLIP

        # get 2nd byte to inc the PayloadPointer
        _tmpByte = self.GetByte()

        return GetArmConfig


    def GetTurnNumbers(self) -> TurnNumber :

        GetTurnNumbers : TurnNumber = TurnNumber()
        
        # update internal pointer
        self.UpdatePointer()

        # check pointer is valid ? 
        if (self._payload is not None):

            GetTurnNumbers.J1Turns = SINT(self.GetHalfeByte1(False).value)
            GetTurnNumbers.J2Turns = SINT(self.GetHalfeByte2(True ).value)
            GetTurnNumbers.J3Turns = SINT(self.GetHalfeByte1(False).value)
            GetTurnNumbers.J4Turns = SINT(self.GetHalfeByte2(True ).value)
            GetTurnNumbers.J5Turns = SINT(self.GetHalfeByte1(False).value)
            GetTurnNumbers.J6Turns = SINT(self.GetHalfeByte2(True ).value)
            GetTurnNumbers.E1Turns = SINT(self.GetByte().value)

        return GetTurnNumbers


    # --------------------------------------------------------
    # Reset pointer
    # --------------------------------------------------------
    def Reset(self) -> None:
        # Mirror PLC: reset pointer and length; do not alter buffer content
        self.PayloadPtr = UDINT(0)
        self.PayloadLen = UDINT(0)
        
        if self._payload is not None:
            # reset buffer content
            for i in range(len(self._payload)):
                self._payload[i] = 0
        

    # --------------------------------------------------------
    # Optional: attach external payload
    # --------------------------------------------------------
    def SetPayload(self, payload: bytes | bytearray) -> None:
        self._payload = bytearray(payload)
        self.PayloadLen = UDINT(len(self._payload))
        self.PayloadPtr = UDINT(0)

    # --------------------------------------------------------
    # Debug formatting
    # --------------------------------------------------------
    def GetPayloadBytesAsDebugString(self, only_written: bool = True) -> str:
        """
        Returns a multi-line string with DEC | HEX | ASCII per byte, addressed:

            ADR 000: 048 | 0x30 | 0

        - only_written=True: show bytes from 0..PayloadLen-1
        - only_written=False: show full buffer length
        """
        self.UpdatePointer()
        self._ensure_buffer()

        total_len = len(self._payload)
        written_len = int(self.PayloadLen.value)
        length = min(written_len if only_written else total_len, total_len)

        lines: list[str] = []
        for i in range(length):
            val = self._payload[i]
            ascii_char = chr(val) if 32 <= val <= 126 else "."
            lines.append(f"ADR {i:03d}: {val:03d} | 0x{val:02X} | {ascii_char}")

        return "\n".join(lines)
