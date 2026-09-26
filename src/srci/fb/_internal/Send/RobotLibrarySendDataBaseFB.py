# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.fb._internal.Send.RobotLibrarySendDataBaseFB
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    RobotLibrarySendDataBaseFB - writes values into a payload buffer (wire format big
#    endian).
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""RobotLibrarySendDataBaseFB - writes values into a payload buffer (wire format big endian)."""

# ST-Source: POUs/_internal/Send/RobotLibrarySendDataBaseFB.st  sha256: c7da786b5fb145a9

from __future__ import annotations

import struct

from srci.errors import PayloadOverflowError, ValueRangeError
from srci.functions.Convert.Misc import CombineHalfBytes
from srci.iec.rt import Ptr
from srci.iec.types import check_range, set_bit
from srci.types import (
    ArmConfigElbow,
    ArmConfigParameter,
    ArmConfigShoulder,
    ArmConfigWrist,
    DataEnableSync,
    DataInSync,
    TurnNumber,
)
from srci.types.iec import BYTE, DWORD, INT, REAL, SINT, TOD, UDINT, UINT, USINT, Elementary

__all__ = ["RobotLibrarySendDataBaseFB", "turn_to_half_byte"]


def turn_to_half_byte(turns: int, bits: int = 3) -> int:
    """Encode a turn counter as sign + magnitude (spec 5.5.4.4, table 5-25).

    ``bits`` magnitude bits (3 for J1..J6, 7 for E1), the next bit is the sign
    (TRUE = negative direction).
    """
    limit = (1 << bits) - 1
    if not -limit <= turns <= limit:
        raise ValueRangeError(f"turn number {turns} out of range [-{limit}..{limit}]")
    return (abs(turns) & limit) | ((1 << bits) if turns < 0 else 0)


class RobotLibrarySendDataBaseFB:
    """Base FB for writing the payload.

    Every ``Add*`` method appends a value at ``PayloadPtr`` and returns the new
    ``PayloadLen``. Multi-byte values are written big endian (the PLC library swaps
    the bytes with ``RobotLibraryParameter.SWAP_BYTE_ORDER`` on little endian PLCs).

    Differences to ST: values out of the IEC range raise ``ValueRangeError`` and
    writing past the buffer raises ``PayloadOverflowError`` (ST overwrites memory).
    """

    def __init__(self) -> None:
        # VAR_INPUT
        self.PayloadLen: int = 0
        self.PayloadPtr: int = 0
        # VAR
        self._pPayload: bytearray | None = None

    # -------------------------------------------------------------- internals

    def UpdatePointer(self) -> None:
        """Set the payload buffer (overridden by the derived FBs)."""

    def _payload_size(self, buf: bytearray) -> int:
        return len(buf)

    def _write(self, data: bytes) -> int:
        self.UpdatePointer()
        buf = self._pPayload
        if buf is None:  # NULL_POINTER -> RETURN
            return 0
        end = self.PayloadPtr + len(data)
        size = self._payload_size(buf)
        if self.PayloadPtr < 0 or end > size:
            raise PayloadOverflowError(
                f"writing {len(data)} bytes at {self.PayloadPtr} exceeds payload size {size}"
            )
        buf[self.PayloadPtr : end] = data
        self.PayloadPtr = end
        self.PayloadLen = self.PayloadPtr
        return self.PayloadLen

    def _add(self, value: int | float, t: Elementary, fmt: str) -> int:
        check_range(value, t)
        return self._write(struct.pack(fmt, value))

    # -------------------------------------------------------------- methods

    def AddArmConfig(self, Value: ArmConfigParameter) -> int:
        tmp = 0
        tmp = set_bit(tmp, 0, Value.Shoulder == ArmConfigShoulder.BACK)
        tmp = set_bit(tmp, 1, Value.Elbow == ArmConfigElbow.DOWN)
        tmp = set_bit(tmp, 2, Value.Wrist == ArmConfigWrist.FLIP)
        self.AddByte(tmp)
        self.AddByte(0)
        return self.PayloadLen

    def AddBool(self, Value: bool) -> int:
        return self._write(bytes([1 if Value else 0]))

    def AddByte(self, Value: int) -> int:
        return self._add(Value, BYTE, ">B")

    def AddDataBlock(self, pValue: Ptr | bytes | bytearray | list[int], Size: int | None = None) -> int:
        """Copy a block of bytes (``pValue``: pointer or the bytes). ``Size`` defaults to ``len``."""
        if isinstance(pValue, Ptr):
            size = pValue.size - pValue.offset if Size is None else Size
            Value: bytes | bytearray | list[int] = pValue.read(size) if size > 0 else b""
        else:
            Value = pValue
        size = len(Value) if Size is None else Size
        if size == 0 or len(Value) == 0:
            return self.PayloadLen  # ST: RETURN without changing anything
        if size > len(Value):
            raise ValueError(f"Size {size} exceeds data block length {len(Value)}")
        return self._write(bytes(Value[:size]))

    def AddDataEnableSync(self, Value: DataEnableSync) -> int:
        v = Value
        flags = [
            v.EnableSyncTool,
            v.EnableSyncFrame,
            v.EnableSyncLoad,
            v.EnableSyncWorkArea,
            v.EnableSyncSWLimits,
            v.EnableSyncDefaultDynamics,
            v.EnableSyncReferenceDynamics,
        ]
        tmp = 0
        for i, flag in enumerate(flags):
            tmp = set_bit(tmp, i, flag)
        self.AddByte(tmp)
        return self.PayloadLen

    def AddDataInSync(self, Value: DataInSync) -> int:
        v = Value
        flags = [
            v.ToolsInSync,
            v.FramesInSync,
            v.LoadsInSync,
            v.WorkAreasInSync,
            v.SoftwareLimitsInSync,
            v.DefaultDynamicsInSync,
            v.ReferenceDynamicsInSync,
        ]
        tmp = 0
        for i, flag in enumerate(flags):
            tmp = set_bit(tmp, i, flag)
        self.AddByte(tmp)
        return self.PayloadLen

    def AddDword(self, Value: int) -> int:
        return self._add(Value, DWORD, ">I")

    def AddHalfBytes(self, HalfByteHi: int, HalfByteLo: int) -> int:
        return self._write(bytes([CombineHalfBytes(HalfByteHi=HalfByteHi, HalfByteLo=HalfByteLo)]))

    def AddIecDate(self, Value: int) -> int:
        """IEC_DATE (UINT, days since 1990-01-01)."""
        return self._add(Value, UINT, ">H")

    def AddIecTime(self, Value: int) -> int:
        """IEC_TIME (TOD, milliseconds since midnight)."""
        return self._add(Value, TOD, ">I")

    def AddInt(self, Value: int) -> int:
        return self._add(Value, INT, ">h")

    def AddReal(self, Value: float) -> int:
        check_range(float(Value), REAL)
        return self._write(struct.pack(">f", Value))

    def AddSint(self, Value: int) -> int:
        return self._add(Value, SINT, ">b")

    def AddString(self, Value: str) -> int:
        """Characters without terminating NUL (STRING(255), single byte characters)."""
        if len(Value) == 0:
            return self.PayloadLen  # ST: RETURN
        data = Value.encode("latin-1")
        if len(data) > 255:
            raise ValueError("STRING(255) exceeded")
        return self._write(data)

    def AddTime(self, Value: int) -> int:
        """TOD in milliseconds since midnight."""
        return self._add(Value, TOD, ">I")

    def AddTurnNumber(self, Value: TurnNumber) -> int:
        """ST-FIX F3: sign + magnitude encoding according to spec 5.5.4.4.

        The ST code writes the two's complement low nibble (``SINT_TO_BYTE``), so -1 is
        sent as 2#1111 which the RC reads as -7.
        """
        self.AddHalfBytes(
            HalfByteHi=turn_to_half_byte(Value.J2Turns), HalfByteLo=turn_to_half_byte(Value.J1Turns)
        )
        self.AddHalfBytes(
            HalfByteHi=turn_to_half_byte(Value.J4Turns), HalfByteLo=turn_to_half_byte(Value.J3Turns)
        )
        self.AddHalfBytes(
            HalfByteHi=turn_to_half_byte(Value.J6Turns), HalfByteLo=turn_to_half_byte(Value.J5Turns)
        )
        self.AddByte(turn_to_half_byte(Value.E1Turns, bits=7))
        return self.PayloadLen

    def AddUdint(self, Value: int) -> int:
        return self._add(Value, UDINT, ">I")

    def AddUint(self, Value: int) -> int:
        return self._add(Value, UINT, ">H")

    def AddUsint(self, Value: int) -> int:
        return self._add(Value, USINT, ">B")

    def Reset(self) -> None:
        self.PayloadLen = 0
        self.PayloadPtr = 0
