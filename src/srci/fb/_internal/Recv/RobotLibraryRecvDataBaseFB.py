"""RobotLibraryRecvDataBaseFB - reads values from a payload buffer."""

# ST-Source: POUs/_internal/Recv/RobotLibraryRecvDataBaseFB.st  sha256: 30280639f7326469

from __future__ import annotations

import struct

from srci.errors import PayloadUnderflowError
from srci.iec.rt import Ptr
from srci.iec.types import bit
from srci.types import (
    ArmConfigElbow,
    ArmConfigParameter,
    ArmConfigShoulder,
    ArmConfigWrist,
    DataInSync,
    FragmentAction,
    TrackingStatus,
    TurnNumber,
)

__all__ = ["RobotLibraryRecvDataBaseFB", "half_byte_to_turn"]


def half_byte_to_turn(value: int, bits: int = 3) -> int:
    """Decode a sign + magnitude turn counter (spec 5.5.4.4). "-0" is returned as 0."""
    magnitude = value & ((1 << bits) - 1)
    return -magnitude if value & (1 << bits) else magnitude


class RobotLibraryRecvDataBaseFB:
    """Base FB for reading the payload.

    Every ``Get*`` method reads at ``PayloadPtr`` and advances it. Multi-byte values
    are big endian, except :meth:`GetDword` (see there).

    Difference to ST: reading past the buffer raises ``PayloadUnderflowError``.
    """

    def __init__(self) -> None:
        # VAR_INPUT
        self.PayloadLen: int = 0
        self.PayloadPtr: int = 0
        # VAR
        self._pPayload: bytearray | bytes | None = None

    # -------------------------------------------------------------- internals

    def UpdatePointer(self) -> None:
        """Set the payload buffer (overridden by the derived FBs)."""

    def _payload_size(self, buf: bytearray | bytes) -> int:
        return len(buf)

    def _peek(self, size: int) -> bytes:
        self.UpdatePointer()
        buf = self._pPayload
        if buf is None:  # NULL_POINTER -> RETURN (value 0)
            return bytes(size)
        end = self.PayloadPtr + size
        limit = self._payload_size(buf)
        if self.PayloadPtr < 0 or end > limit:
            raise PayloadUnderflowError(
                f"reading {size} bytes at {self.PayloadPtr} exceeds payload size {limit}"
            )
        return bytes(buf[self.PayloadPtr : end])

    def _read(self, size: int) -> bytes:
        data = self._peek(size)
        self.PayloadPtr += size
        return data

    def _get(self, fmt: str) -> int | float:
        value: int | float = struct.unpack(fmt, self._read(struct.calcsize(fmt)))[0]
        return value

    # -------------------------------------------------------------- methods

    def GetArmConfig(self) -> ArmConfigParameter:
        tmp = self.GetByte()
        result = ArmConfigParameter(
            Shoulder=ArmConfigShoulder.BACK if bit(tmp, 0) else ArmConfigShoulder.FRONT,
            Elbow=ArmConfigElbow.DOWN if bit(tmp, 1) else ArmConfigElbow.UP,
            Wrist=ArmConfigWrist.FLIP if bit(tmp, 2) else ArmConfigWrist.NON_FLIP,
        )
        self.GetByte()  # second config byte (reserved)
        return result

    def GetBool(self) -> bool:
        return bit(self.GetByte(), 0)

    def GetByte(self) -> int:
        return self._read(1)[0]

    def GetDataBlock(self, pData: Ptr | None = None, Size: int = 0, IsString: bool = False) -> bytes:
        """Read ``Size`` bytes (``Size - 1`` if ``IsString``) and copy them to ``pData``.

        The bytes are also returned (ST: nothing is read if ``pData`` is NULL).
        """
        if IsString:
            Size -= 1
        # ST-FIX F22: ST copies ``Size`` bytes even if the payload buffer ends earlier
        # (MC_ReadMessagesFB reads the 255 byte text at offset 20 of a 256 byte buffer) and
        # so reads the memory behind the buffer. Here the missing bytes are 0.
        self.UpdatePointer()
        buf = self._pPayload
        available = 0 if buf is None else max(0, min(Size, self._payload_size(buf) - self.PayloadPtr))
        data = self._peek(available) + bytes(Size - available)
        self.PayloadPtr += Size
        if pData is not None and Size > 0:
            pData.write(data)
        return data

    def GetDataInSync(self) -> DataInSync:
        tmp = self.GetByte()
        return DataInSync(
            ToolsInSync=bit(tmp, 0),
            FramesInSync=bit(tmp, 1),
            LoadsInSync=bit(tmp, 2),
            WorkAreasInSync=bit(tmp, 3),
            SoftwareLimitsInSync=bit(tmp, 4),
            DefaultDynamicsInSync=bit(tmp, 5),
            ReferenceDynamicsInSync=bit(tmp, 6),
        )

    def GetDword(self) -> int:
        """DWORD **without** byte swap, i.e. little endian - like the ST code.

        Used for the RA status word, which the SDK transmits as a little endian bit
        field (bit 0 in the first byte). See docs/ST_FINDINGS.md F7.
        """
        return int(self._get("<I"))

    def GetFragmentAction(self) -> FragmentAction:
        tmp = self.GetByte()
        return FragmentAction(
            Complete=bit(tmp, 0),
            Reset=bit(tmp, 1),
            Clear=bit(tmp, 2),
            BIT03=bit(tmp, 3),
            BIT04=bit(tmp, 4),
            BIT05=bit(tmp, 5),
            BIT06=bit(tmp, 6),
            BIT07=bit(tmp, 7),
        )

    def GetHalfeByte1(self, IncPayloadPtr: bool) -> int:
        """Bits 0..3 of the current byte."""
        value = self._peek(1)[0] & 0x0F
        if IncPayloadPtr:
            self.PayloadPtr += 1
        return value

    def GetHalfeByte2(self, IncPayloadPtr: bool) -> int:
        """Bits 4..7 of the current byte (as value 0..15)."""
        value = (self._peek(1)[0] >> 4) & 0x0F
        if IncPayloadPtr:
            self.PayloadPtr += 1
        return value

    def GetIecDate(self) -> int:
        return int(self._get(">H"))

    def GetIecTime(self) -> int:
        return int(self._get(">I"))

    def GetInt(self) -> int:
        return int(self._get(">h"))

    def GetReal(self) -> float:
        return float(self._get(">f"))

    def GetSint(self) -> int:
        return int(self._get(">b"))

    def GetString(self, Size: int) -> str:
        """``Size`` bytes as STRING(255) - the string ends at the first NUL byte."""
        data = self._read(Size)
        return data.split(b"\x00", 1)[0].decode("latin-1")

    def GetTrackingStatus(self) -> TrackingStatus:
        tmp = self.GetByte()
        return TrackingStatus(
            ConveyorTrackingEnabled=bit(tmp, 0),
            WaitingForSynchronization=bit(tmp, 1),
            Synchronizing=bit(tmp, 2),
            Synchronous=bit(tmp, 3),
            Desynchronizing=bit(tmp, 4),
            SyncOutZoneEntered=bit(tmp, 5),
            SyncOutZoneLeft=bit(tmp, 6),
            NotUsed=bit(tmp, 7),
        )

    def GetTurnNumbers(self) -> TurnNumber:
        """ST-FIX F3: sign + magnitude decoding according to spec 5.5.4.4.

        The ST code converts the raw nibble with ``BYTE_TO_SINT`` and loses the sign
        (-1 = 2#1001 is read as 9).
        """
        j1 = half_byte_to_turn(self.GetHalfeByte1(False))
        j2 = half_byte_to_turn(self.GetHalfeByte2(True))
        j3 = half_byte_to_turn(self.GetHalfeByte1(False))
        j4 = half_byte_to_turn(self.GetHalfeByte2(True))
        j5 = half_byte_to_turn(self.GetHalfeByte1(False))
        j6 = half_byte_to_turn(self.GetHalfeByte2(True))
        e1 = half_byte_to_turn(self.GetByte(), bits=7)
        return TurnNumber(J1Turns=j1, J2Turns=j2, J3Turns=j3, J4Turns=j4, J5Turns=j5, J6Turns=j6, E1Turns=e1)

    def GetUdint(self) -> int:
        return int(self._get(">I"))

    def GetUint(self) -> int:
        return int(self._get(">H"))

    def GetUsint(self) -> int:
        return int(self._get(">B"))

    def GetWord(self) -> int:
        return int(self._get(">H"))

    def Reset(self) -> None:
        self.PayloadLen = 0
        self.PayloadPtr = 0
