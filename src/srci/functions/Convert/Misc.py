# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.functions.Convert.Misc
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Conversion functions - ``Functions/Convert/Misc`` and ``Functions/Swap`` of the PLC
#    library.
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

"""Conversion functions - ``Functions/Convert/Misc`` and ``Functions/Swap`` of the PLC library.

One function per ST file; every function carries its ``ST-Source`` marker. Deviations
from the ST code are marked with ``ST-FIX <id>`` and listed in ``docs/ST_FINDINGS.md``.
"""

from __future__ import annotations

import math

from srci.iec.types import bit, set_bit
from srci.types import (
    ArmConfigElbow,
    ArmConfigParameter,
    ArmConfigShoulder,
    ArmConfigWrist,
    AxesGroupParameterPlcOptionalCyclic,
    AxesGroupParameterRobOptionalCyclic,
    AxisExternalUnit,
    AxisExternalUsed,
    AxisJointUnit,
    AxisJointUsed,
    AxisUnit,
    DataEnableSync,
    FragmentAction,
    OperationMode,
    RaSequenceState,
    RaStatusWord,
    RCSupportedFunctions,
    RobotLibraryConstants,
    RobotLibraryParameter,
    SynchronizationModes,
    SyncMode,
    SyncTime,
    VersionStruct,
)

__all__ = [
    "PERCENT_INT_TO_REAL",
    "PERCENT_UINT_TO_REAL",
    "REAL_TO_PERCENT_INT",
    "REAL_TO_PERCENT_UINT",
    "ArmConfigParameterToBytes",
    "ByteToAxisExternalUnit",
    "ByteToAxisExternalUsed",
    "ByteToAxisJointUnit",
    "ByteToAxisJointUsed",
    "ByteToFragmentAction",
    "ByteToVersion",
    "BytesToRCSupportedFunctions",
    "CombineBytesToUint",
    "CombineHalfBytes",
    "CombineHalfSints",
    "DwordToRaStatusWord",
    "FragmentActionToByte",
    "GetHalfeByteHi",
    "GetHalfeByteLo",
    "PlcOptionalCyclicToUint",
    "RobOptionalCyclicToUint",
    "SwapWord",
    "SyncModesToDataEnableSync",
    "VersionToByte",
    "WordToArmConfigElbow",
    "WordToArmConfigShoulder",
    "WordToArmConfigWrist",
]


def _bits_to_int(flags: list[bool]) -> int:
    value = 0
    for i, flag in enumerate(flags):
        value = set_bit(value, i, flag)
    return value


def _round_iec(value: float) -> int:
    """REAL_TO_INT/REAL_TO_UINT: round to nearest, halves away from zero."""
    return int(math.floor(abs(value) + 0.5) * (1 if value >= 0 else -1))


# ------------------------------------------------------------------ half bytes


# ST-Source: Functions/Swap/GetHalfeByteHi.st  sha256: 5a9a1d4444d4b293
def GetHalfeByteHi(Value: int) -> int:
    """Bits 4..7 of ``Value`` as a value 0..15."""
    return (Value >> 4) & 0x0F


# ST-Source: Functions/Swap/GetHalfeByteLo.st  sha256: 447382774c8ae99b
def GetHalfeByteLo(Value: int) -> int:
    """Bits 0..3 of ``Value`` as a value 0..15."""
    return Value & 0x0F


# ST-Source: Functions/Swap/SwapWord.st  sha256: bbfd4ad3fa4f16c8
def SwapWord(Value: int) -> int:
    """Swap the two bytes of a WORD (``RobotLibraryParameter.SWAP_BYTE_ORDER`` is TRUE on x86 PLCs)."""
    if not RobotLibraryParameter.SWAP_BYTE_ORDER:
        return Value & 0xFFFF
    return ((Value & 0xFF) << 8) | ((Value >> 8) & 0xFF)


# ST-Source: Functions/Convert/Misc/CombineHalfBytes.st  sha256: fe7ce44c68e79546
def CombineHalfBytes(HalfByteHi: int, HalfByteLo: int) -> int:
    """Low nibble of ``HalfByteHi`` -> bits 4..7, low nibble of ``HalfByteLo`` -> bits 0..3."""
    return ((HalfByteHi & 0x0F) << 4) | (HalfByteLo & 0x0F)


# ST-Source: Functions/Convert/Misc/CombineHalfSints.st  sha256: 6c96b6bd218f0b92
def CombineHalfSints(HalfSintHi: int, HalfSintLo: int) -> int:
    """Two SINT values as sign + magnitude nibbles (turn numbers, spec 5.5.4.4): bits 0..2 value,
    bit 3 sign, ``HalfSintHi`` in bits 4..7.

    ST-FIX F60: the ST code combines the two's complement nibbles (-1 -> 2#1111 = -7 for the RC).
    """

    def nibble(value: int) -> int:
        return (min(abs(value), 7)) | (0x08 if value < 0 else 0)

    return (nibble(HalfSintHi) << 4) | nibble(HalfSintLo)


# ST-Source: Functions/Convert/Misc/CombineBytesToUint.st  sha256: 3a15b45d66be6f3c
def CombineBytesToUint(HiByte: int, LoByte: int) -> int:
    return ((HiByte & 0xFF) << 8) | (LoByte & 0xFF)


# ------------------------------------------------------------------ version


# ST-Source: Functions/Convert/Misc/VersionToByte.st  sha256: 88b861629daf852b
def VersionToByte(Value: VersionStruct) -> int:
    """Bits 0..4 minor version, bits 5..7 major version (spec table 5-86)."""
    return ((Value.MajorVersion & 0x07) << 5) | (Value.MinorVersion & 0x1F)


# ST-Source: Functions/Convert/Misc/ByteToVersion.st  sha256: 90fa65ab9ac47b5f
def ByteToVersion(Value: int) -> VersionStruct:
    return VersionStruct(MajorVersion=(Value >> 5) & 0x07, MinorVersion=Value & 0x1F, PatchVersion=0)


# ------------------------------------------------------------------ bit structures


# ST-Source: Functions/Convert/Misc/ArmConfigParameterToBytes.st  sha256: b5b90ab71497ccbf
def ArmConfigParameterToBytes(Value: ArmConfigParameter) -> list[int]:
    """``ARRAY[0..1] OF BYTE``: Shoulder bits 0..3, Elbow bits 4..7 of byte 0, Wrist bits 0..3 of byte 1."""
    return [CombineHalfBytes(int(Value.Elbow), int(Value.Shoulder)), int(Value.Wrist) & 0x0F]


# ST-Source: Functions/Convert/Misc/FragmentActionToByte.st  sha256: 2a699df99ca1df04
def FragmentActionToByte(FragmentAction: FragmentAction) -> int:
    fa = FragmentAction
    return _bits_to_int([fa.Complete, fa.Reset, fa.Clear, fa.BIT03, fa.BIT04, fa.BIT05, fa.BIT06, fa.BIT07])


# ST-Source: Functions/Convert/Misc/ByteToFragmentAction.st  sha256: ba2b74453faf6c16
def ByteToFragmentAction(FragmentAction_: int) -> FragmentAction:
    b = FragmentAction_
    return FragmentAction(
        Complete=bit(b, 0),
        Reset=bit(b, 1),
        Clear=bit(b, 2),
        BIT03=bit(b, 3),
        BIT04=bit(b, 4),
        BIT05=bit(b, 5),
        BIT06=bit(b, 6),
        BIT07=bit(b, 7),
    )


# ST-Source: Functions/Convert/Misc/PlcOptionalCyclicToUint.st  sha256: f4d48ca8fb480e41
def PlcOptionalCyclicToUint(OptionalCyclic: AxesGroupParameterPlcOptionalCyclic) -> int:
    """TelegramNumber ClientServer (spec table 5-87)."""
    o = OptionalCyclic
    return _bits_to_int(
        [
            o.UseCallSubprogram,
            o.UseCartesianPosition,
            o.UseJointPosition,
            o.UseForce,
            o.Bit04,
            o.Bit05,
            o.Bit06,
            o.Bit07,
            o.UseTwoSequences,
            o.UseCartesianPositionExt,
            o.UseJointPositionExt,
            o.Bit11,
            o.Bit12,
            o.Bit13,
            o.Bit14,
            o.Bit15,
        ]
    )


# ST-Source: Functions/Convert/Misc/RobOptionalCyclicToUint.st  sha256: 3d5d1b392b75c3c8
def RobOptionalCyclicToUint(OptionalCyclic: AxesGroupParameterRobOptionalCyclic) -> int:
    """TelegramNumber ServerClient (spec table 5-88)."""
    o = OptionalCyclic
    return _bits_to_int(
        [
            o.UseCallSubprogram,
            o.UseCartesianPosition,
            o.UseJointPosition,
            o.UseForce,
            o.UseCurrent,
            o.Bit05,
            o.Bit06,
            o.Bit07,
            o.UseTwoSequences,
            o.UseCartesianPositionExt,
            o.UseJointPositionExt,
            o.UseForceExt,
            o.UseCurrentExt,
            o.Bit13,
            o.Bit14,
            o.Bit15,
        ]
    )


# ST-Source: Functions/Convert/Misc/DwordToRaStatusWord.st  sha256: e0122e086d0bd0d9
def DwordToRaStatusWord(Value: int) -> RaStatusWord:
    """Status word of the robot arm (spec table 5-105).

    ST-FIX F6: the ST code inserts ``CollisionDetectedEnabled`` at bit 13 and therefore
    shifts all following bits by one. Spec 1.5.9 (table 5-105) and the SDK define
    bit 13 CollisionDetected, 14 RestartRequested, 15 Accelerating, 16 Decelerating,
    17 ConstantVelocity, 18..31 reserved. ``CollisionDetectedEnabled`` is not part of the
    status word and stays FALSE.
    """
    v = Value
    return RaStatusWord(
        IsMoving=bit(v, 0),
        PrimarySequencePaused=bit(v, 1),
        InPrimaryPos=bit(v, 2),
        SecondarySequenceActive=bit(v, 3),
        IsBlending=bit(v, 4),
        ErrorPending=bit(v, 5),
        RestartInProgress=bit(v, 6),
        Enabled=bit(v, 7),
        RaSequenceState=RaSequenceState((v >> 8) & 0x03),
        OperationMode=OperationMode((v >> 10) & 0x07),
        CollisionDetectedEnabled=False,
        CollisionDetected=bit(v, 13),
        RestartRequested=bit(v, 14),
        Accelerating=bit(v, 15),
        Decelerating=bit(v, 16),
        ConstantVelocity=bit(v, 17),
        **{f"Bit{i}": bit(v, i) for i in range(19, 32)},
    )


# ST-Source: Functions/Convert/Misc/BytesToRCSupportedFunctions.st  sha256: 4fce1def1c4a954d
def BytesToRCSupportedFunctions(Bytes: bytes | bytearray | list[int]) -> RCSupportedFunctions:
    """``ARRAY[0..18] OF BYTE`` -> RCSupportedFunctions.

    The ST code maps member n of the structure (in declaration order) to
    ``Bytes[n / 8].(n MOD 8)`` - verified for all 152 members.
    """
    if len(Bytes) < 19:
        raise ValueError(f"19 bytes expected, got {len(Bytes)}")
    result = RCSupportedFunctions()
    for n, f in enumerate(RCSupportedFunctions._IEC_FIELDS_):
        setattr(result, f.name, bit(Bytes[n // 8], n % 8))
    return result


# ST-Source: Functions/Convert/Misc/ByteToAxisExternalUnit.st  sha256: b0f7ef84849797c4
def ByteToAxisExternalUnit(AxisExternalUnit_: int) -> AxisExternalUnit:
    b = AxisExternalUnit_
    return AxisExternalUnit(**{f"E{i}": AxisUnit(int(bit(b, i))) for i in range(1, 7)})


# ST-Source: Functions/Convert/Misc/ByteToAxisExternalUsed.st  sha256: ec8191bb9d911433
def ByteToAxisExternalUsed(AxisExternalUsed_: int) -> AxisExternalUsed:
    b = AxisExternalUsed_
    return AxisExternalUsed(**{f"E{i}": bit(b, i) for i in range(1, 7)})


# ST-Source: Functions/Convert/Misc/ByteToAxisJointUnit.st  sha256: 9d5dc750cc858518
def ByteToAxisJointUnit(AxisJointUnit_: int) -> AxisJointUnit:
    """ST-FIX F9: the ST code assigns bit 1 to J2 (and then bit 2 to J2 again), J1 is never set.

    Mapped like :func:`ByteToAxisJointUsed`: J1 = bit 1 ... J6 = bit 6.
    """
    b = AxisJointUnit_
    return AxisJointUnit(**{f"J{i}": AxisUnit(int(bit(b, i))) for i in range(1, 7)})


# ST-Source: Functions/Convert/Misc/ByteToAxisJointUsed.st  sha256: 5543c813431864ec
def ByteToAxisJointUsed(AxisJointUsed_: int) -> AxisJointUsed:
    b = AxisJointUsed_
    return AxisJointUsed(**{f"J{i}": bit(b, i) for i in range(1, 7)})


# ST-Source: Functions/Convert/Misc/SyncModesToDataEnableSync.st  sha256: 0e76f9536f93fbc7
def SyncModesToDataEnableSync(Value: SynchronizationModes) -> DataEnableSync:
    def enabled(modes: list[SyncMode]) -> bool:
        return (
            modes[SyncTime.DURING_START_UP] > SyncMode.NO_SYNCHRONIZATION
            or modes[SyncTime.AFTER_START_UP] > SyncMode.NO_SYNCHRONIZATION
        )

    return DataEnableSync(
        EnableSyncTool=enabled(Value.Tool),
        EnableSyncFrame=enabled(Value.Frame),
        EnableSyncLoad=enabled(Value.Load),
        EnableSyncWorkArea=enabled(Value.WorkAreas),
        EnableSyncSWLimits=enabled(Value.SWLimits),
        EnableSyncDefaultDynamics=enabled(Value.DefaultDynamics),
        EnableSyncReferenceDynamics=enabled(Value.ReferenceDynamics),
    )


# ST-Source: Functions/Convert/Misc/WordToArmConfigElbow.st  sha256: d608980d7e2b2456
def WordToArmConfigElbow(Value: int) -> ArmConfigElbow:
    return ArmConfigElbow.DOWN if bit(SwapWord(Value), 1) else ArmConfigElbow.UP


# ST-Source: Functions/Convert/Misc/WordToArmConfigShoulder.st  sha256: 3fde64921e003625
def WordToArmConfigShoulder(Value: int) -> ArmConfigShoulder:
    return ArmConfigShoulder.BACK if bit(SwapWord(Value), 0) else ArmConfigShoulder.FRONT


# ST-Source: Functions/Convert/Misc/WordToArmConfigWrist.st  sha256: b45de53c7cb88971
def WordToArmConfigWrist(Value: int) -> ArmConfigWrist:
    return ArmConfigWrist.FLIP if bit(SwapWord(Value), 2) else ArmConfigWrist.NON_FLIP


# ------------------------------------------------------------------ percent encoding

_FACTOR = RobotLibraryConstants.REAL_CONVERSION_FACTOR


# ST-Source: Functions/Convert/Misc/REAL_TO_PERCENT_INT.st  sha256: c9441164de3bfd46
def REAL_TO_PERCENT_INT(Value: float, IsOptional: bool = False) -> int:
    """Percent value -> INT with factor 100 (-1.0 -> 16#FFFF).

    ST-FIX F41: -1.0 ("<0 %: use the default", spec 5.x robot dynamics) is sent as 16#FFFF also
    for parameters that are not optional (ST: only with IsOptional -> -100 was sent).
    """
    if Value == -1.0:
        return -1  # UINT_TO_INT(16#FFFF)
    return _round_iec(Value * _FACTOR)


# ST-Source: Functions/Convert/Misc/REAL_TO_PERCENT_UINT.st  sha256: 7e323e4b10da806a
def REAL_TO_PERCENT_UINT(Value: float, IsOptional: bool = False) -> int:
    """Percent value -> UINT with factor 100; -1.0 -> 16#FFFF (ST-FIX F41, see REAL_TO_PERCENT_INT)."""
    if Value == -1.0:
        return 0xFFFF
    return _round_iec(Value * _FACTOR) & 0xFFFF  # REAL_TO_UINT: out-of-range values wrap like on the PLC


# ST-Source: Functions/Convert/Misc/PERCENT_INT_TO_REAL.st  sha256: 53df6f10d702dea5
def PERCENT_INT_TO_REAL(Value: int, IsOptional: bool = False) -> float:
    """INT with factor 100 -> percent. 16#FFFF (INT -1) of an optional value -> -1.0.

    The ST code compares the INT with 16#FFFF_FFFF / 16#0000_FFFF; intended meaning is
    "all bits set" (see docs/ST_FINDINGS.md F10).
    """
    if IsOptional and (Value & 0xFFFF) == 0xFFFF:
        return -1.0
    return float(Value) / _FACTOR


# ST-Source: Functions/Convert/Misc/PERCENT_UINT_TO_REAL.st  sha256: e5e4cef0b6d05c11
def PERCENT_UINT_TO_REAL(Value: int, IsOptional: bool = False) -> float:
    if IsOptional and Value in (0xFFFF, 0xFFFF_FFFF):
        return -1.0
    return float(Value) / _FACTOR
