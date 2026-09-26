"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryLogFB
Author:      Thorsten Brach
Date:        2025-12-26

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


from RobotLibrary.IEC_Types import IEC_POU, BOOL, BYTE, UDINT, USINT, UINT, INT, SINT, DWORD, REAL, IEC_String, STRING, TIME
from RobotLibrary.Structures.DatenAndTime import IEC_DATE, IEC_TIME
from RobotLibrary.Structures.Miscellaneous.DataInSync import DataInSync
from RobotLibrary.Structures.Miscellaneous.DataEnableSync import DataEnableSync
from RobotLibrary.Structures.Miscellaneous.ArmConfigParameter import ArmConfigParameter
from RobotLibrary.Structures.Miscellaneous.TurnNumber import TurnNumber

from RobotLibrary.Enumerations.ArmConfig.ArmConfigShoulder import ArmConfigShoulder
from RobotLibrary.Enumerations.ArmConfig.ArmConfigElbow import ArmConfigElbow
from RobotLibrary.Enumerations.ArmConfig.ArmConfigWrist import ArmConfigWrist

class RobotLibrarySendDataBaseFB(IEC_POU):
    # VAR_INPUT
    PayloadLen: UDINT = UDINT(0)
    """Payload length"""
    PayloadPtr: UDINT = UDINT(0)
    """Payload pointer (offset)"""

    # VAR (internal)
    _payload : bytearray = bytearray()
    
    """Internal payload buffer owned by the base class unless overridden"""


    # --------------------------------------------------------
    # UpdatePointer - override in derived classes to set a custom buffer
    # --------------------------------------------------------
    def UpdatePointer(self) -> None:
        """No-op in base. Derived classes must set `_payload` explicitly.

        Example:
            def UpdatePointer(self):
                self._payload = self.PayLoad
        """
        return

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    def _ensure_capacity(self, nbytes: int) -> None:
        """Grow internal buffer to hold write at current pointer + nbytes."""
        needed = int(self.PayloadPtr.value) + nbytes
        if needed > len(self._payload):
            self._payload.extend(b"\x00" * (needed - len(self._payload)))

    def _addToPayload(self, data: bytes) -> None:
        """Write bytes at current pointer and advance pointer/length."""
        off = int(self.PayloadPtr.value)
        self._ensure_capacity(len(data))
        self._payload[off:off + len(data)] = data
        self.PayloadPtr = UDINT(off + len(data))
        self.PayloadLen = UDINT(self.PayloadPtr.value)

    def _to_iec(self, Value, typ):
        """Coerce plain ints or proxy objects into IEC types."""
        if isinstance(Value, typ):
            return Value
        # Already an IEC type or proxy that can serialize itself
        if hasattr(Value, 'GetBytes'):
            return Value

        # Special handling for REAL: coerce via float to avoid truncation
        # and OverflowError for non-finite values when using int().
        if typ is REAL:
            try:
                v = float(Value.value) if hasattr(Value, 'value') else float(Value)
            except (TypeError, ValueError):
                # Fallback: attempt direct float conversion
                v = float(Value)
            return REAL(v)

        # Default path for integer-like IEC types
        if hasattr(Value, 'value'):
            v = int(Value.value)
        else:
            v = int(Value)
        return typ(v)

    # --------------------------------------------------------
    # Add methods (mirror PLC FB behavior)
    # --------------------------------------------------------
    def AddBool(self, Value: BOOL) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, BOOL)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddByte(self, Value: BYTE) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, BYTE)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddUsint(self, Value: USINT) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, USINT)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddSint(self, Value: SINT) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, SINT)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddUint(self, Value: UINT) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, UINT)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddUdint(self, Value: UDINT) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, UDINT)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddDword(self, Value: DWORD) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, DWORD)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddInt(self, Value: INT) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, INT)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddReal(self, Value: REAL | float) -> UDINT:
        self.UpdatePointer()
        
        if isinstance(Value, float):
            Value = REAL(Value)
        
        v = self._to_iec(Value, REAL)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddHalfBytes(self, HalfByteHi: BYTE | USINT, HalfByteLo: BYTE | USINT) -> UDINT:
        self.UpdatePointer()
        v = ((int(HalfByteHi.value) & 0x0F) << 4) | (int(HalfByteLo.value) & 0x0F)
        self._addToPayload(bytes([v]))
        return UDINT(self.PayloadLen.value)

    def AddDataBlock(self, pValue: bytes | bytearray | memoryview, Size: UDINT | int) -> UDINT:
        self.UpdatePointer()
        
        Size = int(Size)
        
        if pValue is None or Size == 0:
            return UDINT(self.PayloadLen.value)
        mv = memoryview(pValue)
        self._addToPayload(mv[:Size].tobytes())
        return UDINT(self.PayloadLen.value)

    def AddString(self, Value: IEC_String | STRING | str) -> UDINT:
        self.UpdatePointer()
        s = str(Value)
        if len(s) == 0:
            return UDINT(self.PayloadLen.value)
        # copy only content length (like PLC LEN(Value))
        self._addToPayload(s.encode("ascii", errors="replace"))
        return UDINT(self.PayloadLen.value)
    
    def AddTime(self, Value : TIME) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, TIME)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddIecDate(self, Value) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, IEC_DATE)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)

    def AddIecTime(self, Value) -> UDINT:
        self.UpdatePointer()
        v = self._to_iec(Value, IEC_TIME)
        self._addToPayload(v.GetBytes('big'))
        return UDINT(self.PayloadLen.value)


    # --------------------------------------------------------
    # AddDataInSync
    # --------------------------------------------------------
    def AddDataInSync(self, Value : DataInSync) -> UDINT:

        tmpByte : BYTE = BYTE(0)
        tmpByte.Bit[0] = Value.ToolsInSync
        tmpByte.Bit[1] = Value.FramesInSync
        tmpByte.Bit[2] = Value.LoadsInSync
        tmpByte.Bit[3] = Value.WorkAreasInSync
        tmpByte.Bit[4] = Value.SoftwareLimitsInSync
        tmpByte.Bit[5] = Value.DefaultDynamicsInSync
        tmpByte.Bit[6] = Value.ReferenceDynamicsInSync

        return self.AddByte(tmpByte)

    # --------------------------------------------------------
    # AddDataEnableSync
    # --------------------------------------------------------
    def AddDataEnableSync(self, Value : DataEnableSync) -> UDINT:
        
        tmpByte : BYTE = BYTE(0)
        
        tmpByte.Bit[0] = Value.EnableSyncTool
        tmpByte.Bit[1] = Value.EnableSyncFrame
        tmpByte.Bit[2] = Value.EnableSyncLoad
        tmpByte.Bit[3] = Value.EnableSyncWorkArea
        tmpByte.Bit[4] = Value.EnableSyncSWLimits
        tmpByte.Bit[5] = Value.EnableSyncDefaultDynamics
        tmpByte.Bit[6] = Value.EnableSyncReferenceDynamics
        
        return self.AddByte(tmpByte)

    # --------------------------------------------------------
    # AddArmConfig
    # --------------------------------------------------------
    def AddArmConfig(self, Value: ArmConfigParameter) -> UDINT:
        
        _tmpByte : BYTE = BYTE(0)
        
        _tmpByte.Bit[0] = Value.Shoulder == ArmConfigShoulder.BACK
        _tmpByte.Bit[1] = Value.Elbow    == ArmConfigElbow.DOWN
        _tmpByte.Bit[2] = Value.Wrist    == ArmConfigWrist.FLIP

        self.AddByte(_tmpByte)
        self.AddByte(BYTE(0))

        return UDINT(self.PayloadLen.value)

    # --------------------------------------------------------
    # AddTurnNumber
    # --------------------------------------------------------
    def AddTurnNumber(self, Value: TurnNumber) -> UDINT:

        self.AddHalfBytes( HalfByteHi = BYTE(Value.J2Turns.value) , HalfByteLo = BYTE(Value.J1Turns.value))
        self.AddHalfBytes( HalfByteHi = BYTE(Value.J4Turns.value) , HalfByteLo = BYTE(Value.J3Turns.value))
        self.AddHalfBytes( HalfByteHi = BYTE(Value.J6Turns.value) , HalfByteLo = BYTE(Value.J5Turns.value))

        self.AddByte(BYTE(Value.E1Turns.value))

        return UDINT(self.PayloadLen.value)


    # --------------------------------------------------------
    # ReseSetLifeSignFootert
    # --------------------------------------------------------
    def SetLifeSignFooter(self, LifeSign : BYTE) -> None:
        # check payload pointer is valid? 
        if self._payload is not None:
            # calculate pointer to last byte
            LifeSignPtr = len(self._payload) - 1
            # set LifeSign byte
            self._payload[LifeSignPtr] = LifeSign.value
        else:
            raise Exception("Payload pointer is not valid in SetLifeSignFooter")

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------
    def Reset(self) -> None:
        # Zero-fill existing buffer without changing length
        if self._payload is not None:
            for i in range(len(self._payload)):
                self._payload[i] = 0

        self.PayloadPtr = UDINT(0)
        self.PayloadLen = UDINT(0)

    # --------------------------------------------------------
    # Pointer exposure helpers
    # --------------------------------------------------------
    def GetPayloadBytes(self):
        """Return (bytes, length) snapshot of the current payload."""
        self.UpdatePointer()
        return bytes(self._payload), len(self._payload)

    # --------------------------------------------------------
    # GetPayloadBytesAsDebugString :  Bytes per line with DEC | HEX | ASCII columns
    # --------------------------------------------------------
    def GetPayloadBytesAsDebugString(
        self,
        only_written: bool = True,
        addr_prefix: str = "ADR ",
        addr_start: int = 0,
        addr_width: int = 3,
        hex_prefix: str = "0x",
        ascii_nonprintable: str = ".",
    ) -> str:
        """Return payload one byte per line with DEC | HEX | ASCII columns.

        Example: "ADR 000: 048 | 0x30 | 0"
        - only_written: True formats first PayloadLen bytes, False formats full buffer.
        - addr_prefix: prefix before the address label.
        - addr_start: starting address index.
        - addr_width: zero-padded width for address.
        - hex_prefix: prefix for hex values (default '0x').
        - ascii_nonprintable: placeholder for non-printable bytes (default '.')
        """
        self.UpdatePointer()
        data = self._payload[:int(self.PayloadLen.value)] if only_written else self._payload
        lines = []
        for i, b in enumerate(data):
            addr = f"{addr_prefix}{addr_start + i:0{addr_width}d}: "
            dec_part = f"{b:03d}"
            hex_part = f"{hex_prefix}{b:02X}"
            ascii_part = chr(b) if 32 <= b <= 126 else ascii_nonprintable
            lines.append(f"{addr}{dec_part} | {hex_part} | {ascii_part}")
        return "\n".join(lines)
    
