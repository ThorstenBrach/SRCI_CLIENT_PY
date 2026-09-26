"""Functions/Convert/Misc - checked against the SRCI profile V1.5.9 where it defines the bits."""

from __future__ import annotations

import pytest

from srci.fb._internal.Recv.RobotLibraryRecvDataFB import RobotLibraryRecvDataFB
from srci.functions.Convert import Misc as M
from srci.types import (
    ArmConfigElbow,
    ArmConfigParameter,
    ArmConfigShoulder,
    ArmConfigWrist,
    AxesGroupParameterPlcOptionalCyclic,
    AxesGroupParameterRobOptionalCyclic,
    AxisUnit,
    FragmentAction,
    OperationMode,
    RaSequenceState,
    RCSupportedFunctions,
    SynchronizationModes,
    SyncMode,
    SyncTime,
    VersionStruct,
)


def test_version_encoding_table_5_86() -> None:
    assert M.VersionToByte(VersionStruct(MajorVersion=1, MinorVersion=5)) == 0b001_00101
    assert M.VersionToByte(VersionStruct(MajorVersion=1, MinorVersion=3)) == 0x23
    v = M.ByteToVersion(0x25)
    assert (v.MajorVersion, v.MinorVersion, v.PatchVersion) == (1, 5, 0)
    for byte in range(256):
        assert M.VersionToByte(M.ByteToVersion(byte)) == byte


def test_half_bytes_and_uint() -> None:
    assert M.CombineHalfBytes(0x0A, 0x05) == 0xA5
    assert M.CombineHalfBytes(0xFA, 0xF5) == 0xA5  # only the low nibbles count
    assert M.CombineHalfSints(-1, 1) == 0xF1
    assert (M.GetHalfeByteHi(0xA5), M.GetHalfeByteLo(0xA5)) == (0xA, 0x5)
    assert M.CombineBytesToUint(HiByte=0x12, LoByte=0x34) == 0x1234
    assert M.SwapWord(0x1234) == 0x3412


def test_status_word_table_5_105() -> None:
    """ST-FIX F6: bit 13 CollisionDetected, 14 RestartRequested, 15..17 acceleration states."""
    s = M.DwordToRaStatusWord(1 << 0 | 1 << 7 | 1 << 8 | 3 << 10 | 1 << 13 | 1 << 17)
    assert s.IsMoving and s.Enabled
    assert s.RaSequenceState == RaSequenceState.EXECUTING
    assert s.OperationMode == OperationMode.AUTO
    assert s.CollisionDetected and s.ConstantVelocity
    assert not (s.RestartRequested or s.Accelerating or s.Decelerating or s.CollisionDetectedEnabled)
    for bit_no, name in [(1, "PrimarySequencePaused"), (2, "InPrimaryPos"), (3, "SecondarySequenceActive"),
                         (4, "IsBlending"), (5, "ErrorPending"), (6, "RestartInProgress"), (14, "RestartRequested"),
                         (15, "Accelerating"), (16, "Decelerating"), (31, "Bit31")]:  # fmt: skip
        assert getattr(M.DwordToRaStatusWord(1 << bit_no), name), name


def test_status_word_undefined_enum_values() -> None:
    s = M.DwordToRaStatusWord(3 << 8)  # RaSequenceState 3 / OperationMode 0 are not defined
    assert int(s.RaSequenceState) == 3 and int(s.OperationMode) == 0
    assert isinstance(s.OperationMode, OperationMode)


def test_status_word_little_endian_on_the_wire() -> None:
    """The RC sends the status as little endian bit field (SDK) - GetDword + DwordToRaStatusWord."""
    r = RobotLibraryRecvDataFB()
    r(Payload=bytes([0b1000_0001, 0x00, 0x00, 0x00]))
    s = M.DwordToRaStatusWord(r.GetDword())
    assert s.IsMoving and s.Enabled


def test_rc_supported_functions_mapping() -> None:
    data = bytearray(19)
    data[0] = 0b0000_0010  # ReadRobotData
    data[2] = 0b0100_0000  # MoveLinearAbsolute
    data[3] = 0b0000_0010  # GroupStop
    data[18] = 0b1000_0000  # Byte18Bit07
    f = M.BytesToRCSupportedFunctions(data)
    assert f.ReadRobotData and f.MoveLinearAbsolute and f.GroupStop and f.Byte18Bit07
    assert not f.Reserved and not f.EnableRobot
    assert sum(getattr(f, x.name) for x in RCSupportedFunctions._IEC_FIELDS_) == 4
    assert len(RCSupportedFunctions._IEC_FIELDS_) == 19 * 8
    with pytest.raises(ValueError):
        M.BytesToRCSupportedFunctions(b"\x00")


def test_axis_bytes() -> None:
    used = M.ByteToAxisJointUsed(0b0100_0010)
    assert used.J1 and used.J6 and not used.J2
    unit = M.ByteToAxisJointUnit(0b0000_0010)  # ST-FIX F9: bit 1 -> J1
    assert unit.J1 == AxisUnit(1) and unit.J2 == AxisUnit(0)
    ext = M.ByteToAxisExternalUsed(0b0000_0010)
    assert ext.E1 and not ext.E2
    assert M.ByteToAxisExternalUnit(0b0100_0000).E6 == AxisUnit(1)


def test_fragment_action_roundtrip() -> None:
    for value in range(256):
        assert M.FragmentActionToByte(M.ByteToFragmentAction(value)) == value
    assert M.FragmentActionToByte(FragmentAction(Complete=True, Clear=True)) == 0b101


def test_optional_cyclic_telegram_numbers() -> None:
    plc = AxesGroupParameterPlcOptionalCyclic(UseCartesianPosition=True, UseTwoSequences=True)
    assert M.PlcOptionalCyclicToUint(plc) == (1 << 1) | (1 << 8)
    rob = AxesGroupParameterRobOptionalCyclic(UseCurrent=True, UseCurrentExt=True)
    assert M.RobOptionalCyclicToUint(rob) == (1 << 4) | (1 << 12)


def test_arm_config_conversions() -> None:
    cfg = ArmConfigParameter(
        Shoulder=ArmConfigShoulder.BACK, Elbow=ArmConfigElbow.UP, Wrist=ArmConfigWrist.SAME
    )
    assert M.ArmConfigParameterToBytes(cfg) == [0x43, 0x01]
    # Config WORD of the cyclic position: bits are in the first byte on the wire (spec table 5-89)
    r = RobotLibraryRecvDataFB()
    r(Payload=b"\x05\x00")
    word = r.GetWord()
    assert M.WordToArmConfigShoulder(word) == ArmConfigShoulder.BACK
    assert M.WordToArmConfigElbow(word) == ArmConfigElbow.UP
    assert M.WordToArmConfigWrist(word) == ArmConfigWrist.FLIP


def test_sync_modes() -> None:
    modes = SynchronizationModes()
    for name in ("Tool", "Frame", "Load", "WorkAreas", "SWLimits", "DefaultDynamics", "ReferenceDynamics"):
        getattr(modes, name)[:] = [SyncMode.NO_SYNCHRONIZATION] * 2
    modes.Frame[SyncTime.AFTER_START_UP] = SyncMode.AUTOMATIC
    sync = M.SyncModesToDataEnableSync(modes)
    assert sync.EnableSyncFrame and not sync.EnableSyncTool and not sync.EnableSyncReferenceDynamics


@pytest.mark.parametrize(
    ("value", "optional", "expected"),
    [
        (50.0, False, 5000),
        (0.005, False, 1),
        (-0.005, False, -1),
        (-1.0, True, -1),
        (-1.0, False, -1),
    ],  # ST-FIX F41: -1.0 = default also if not optional,
)
def test_real_to_percent_int(value: float, optional: bool, expected: int) -> None:
    assert M.REAL_TO_PERCENT_INT(value, optional) == expected


def test_percent_conversions() -> None:
    assert M.REAL_TO_PERCENT_UINT(100.0) == 10000
    assert M.REAL_TO_PERCENT_UINT(-1.0, True) == 0xFFFF
    assert M.PERCENT_UINT_TO_REAL(0xFFFF, True) == -1.0
    assert M.PERCENT_UINT_TO_REAL(0xFFFF, False) == 655.35
    assert M.PERCENT_INT_TO_REAL(-1, True) == -1.0
    assert M.PERCENT_INT_TO_REAL(-150) == -1.5
    assert M.PERCENT_INT_TO_REAL(M.REAL_TO_PERCENT_INT(12.34)) == 12.34
