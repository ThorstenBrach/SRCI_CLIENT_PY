"""RobotLibrarySendData*/RecvData* - byte level behaviour (wire format big endian)."""

from __future__ import annotations

import math
import random
import struct

import pytest

from srci.errors import PayloadOverflowError, PayloadUnderflowError, ValueRangeError
from srci.fb._internal.Recv.RobotLibraryRecvDataBaseFB import half_byte_to_turn
from srci.fb._internal.Recv.RobotLibraryRecvDataFB import RobotLibraryRecvDataFB
from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from srci.fb._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from srci.fb._internal.Send.RobotLibrarySendDataBaseFB import turn_to_half_byte
from srci.fb._internal.Send.RobotLibrarySendDataFB import RobotLibrarySendDataFB
from srci.types import (
    ArmConfigElbow,
    ArmConfigParameter,
    ArmConfigShoulder,
    ArmConfigWrist,
    DataEnableSync,
    DataInSync,
    TurnNumber,
)


def sender(size: int = 64) -> tuple[RobotLibrarySendDataFB, bytearray]:
    buf = bytearray(size)
    s = RobotLibrarySendDataFB()
    s(Payload=buf, PayLoadSize=size)
    s.Reset()
    return s, buf


def receiver(data: bytes) -> RobotLibraryRecvDataFB:
    r = RobotLibraryRecvDataFB()
    r.Reset()
    r(Payload=data, PayloadSize=len(data))
    return r


# ---------------------------------------------------------------- golden bytes


@pytest.mark.parametrize(
    ("method", "value", "expected"),
    [
        ("AddByte", 0xAB, b"\xab"),
        ("AddUsint", 200, b"\xc8"),
        ("AddSint", -2, b"\xfe"),
        ("AddUint", 0x1234, b"\x12\x34"),
        ("AddInt", -2, b"\xff\xfe"),
        ("AddUdint", 0x01020304, b"\x01\x02\x03\x04"),
        ("AddDword", 0x01020304, b"\x01\x02\x03\x04"),
        ("AddReal", 1.0, b"\x3f\x80\x00\x00"),
        ("AddReal", -2.5, b"\xc0\x20\x00\x00"),
        ("AddTime", 86_399_999, struct.pack(">I", 86_399_999)),
        ("AddIecTime", 1000, b"\x00\x00\x03\xe8"),
        ("AddIecDate", 0x2B67, b"\x2b\x67"),
        ("AddBool", True, b"\x01"),
        ("AddBool", False, b"\x00"),
        ("AddString", "Abc", b"Abc"),
    ],
)
def test_add_golden(method: str, value: object, expected: bytes) -> None:
    s, buf = sender()
    n = getattr(s, method)(value)
    assert bytes(buf[: len(expected)]) == expected
    assert n == s.PayloadLen == s.PayloadPtr == len(expected)


@pytest.mark.parametrize(
    ("method", "data", "expected"),
    [
        ("GetByte", b"\xab", 0xAB),
        ("GetUsint", b"\xc8", 200),
        ("GetSint", b"\xfe", -2),
        ("GetUint", b"\x12\x34", 0x1234),
        ("GetWord", b"\x12\x34", 0x1234),
        ("GetInt", b"\xff\xfe", -2),
        ("GetUdint", b"\x01\x02\x03\x04", 0x01020304),
        ("GetIecTime", b"\x00\x00\x03\xe8", 1000),
        ("GetIecDate", b"\x2b\x67", 0x2B67),
        ("GetReal", b"\x3f\x80\x00\x00", 1.0),
        ("GetBool", b"\x03", True),  # only bit 0 counts
        ("GetBool", b"\x02", False),
        # GetDword has no byte swap in ST (little endian, see ST_FINDINGS F7)
        ("GetDword", b"\x01\x02\x03\x04", 0x04030201),
    ],
)
def test_get_golden(method: str, data: bytes, expected: object) -> None:
    r = receiver(data)
    assert getattr(r, method)() == expected
    assert r.PayloadPtr == len(data)


def test_roundtrip_random_values() -> None:
    rnd = random.Random(4711)
    for _ in range(300):
        s, buf = sender(32)
        u, i, d, f = (
            rnd.randrange(0, 65536),
            rnd.randrange(-32768, 32768),
            rnd.randrange(0, 2**32),
            rnd.uniform(-1e6, 1e6),
        )
        s.AddUint(u)
        s.AddInt(i)
        s.AddUdint(d)
        s.AddReal(f)
        r = receiver(bytes(buf))
        assert (r.GetUint(), r.GetInt(), r.GetUdint()) == (u, i, d)
        assert math.isclose(r.GetReal(), struct.unpack(">f", struct.pack(">f", f))[0])


# ---------------------------------------------------------------- ranges / buffers


@pytest.mark.parametrize(
    ("method", "value"),
    [
        ("AddByte", 256),
        ("AddByte", -1),
        ("AddUint", 65536),
        ("AddInt", 40000),
        ("AddSint", 128),
        ("AddUsint", 1.5),
    ],
)
def test_values_out_of_range_raise(method: str, value: object) -> None:
    s, _ = sender()
    with pytest.raises(ValueRangeError):
        getattr(s, method)(value)


def test_real_overflow_raises() -> None:
    s, _ = sender()
    with pytest.raises(ValueRangeError):
        s.AddReal(1e40)


def test_write_past_payload_size_raises() -> None:
    s, _ = sender(3)
    s.AddUint(1)
    with pytest.raises(PayloadOverflowError):
        s.AddUint(2)
    assert s.PayloadPtr == 2  # nothing written


def test_payload_size_limits_buffer() -> None:
    buf = bytearray(10)
    s = RobotLibrarySendDataFB()
    s(Payload=buf, PayLoadSize=4)
    s.AddUdint(1)
    with pytest.raises(PayloadOverflowError):
        s.AddByte(1)


def test_read_past_end_raises() -> None:
    r = receiver(b"\x01")
    with pytest.raises(PayloadUnderflowError):
        r.GetUint()


def test_reset_clears_payload() -> None:
    s, buf = sender(8)
    s.AddUdint(0xFFFFFFFF)
    s.Reset()
    assert buf == bytearray(8) and s.PayloadPtr == s.PayloadLen == 0


def test_empty_string_and_datablock_write_nothing() -> None:
    s, _ = sender()
    s.AddString("")
    s.AddDataBlock(b"")
    assert s.PayloadLen == 0


def test_datablock_and_string() -> None:
    s, buf = sender()
    s.AddDataBlock([1, 2, 3, 4], 3)
    assert bytes(buf[:3]) == b"\x01\x02\x03"
    r = receiver(b"Hello\x00xyz")
    assert r.GetString(9) == "Hello"
    r = receiver(b"abc\x00")
    assert r.GetDataBlock(4, IsString=True) == b"abc"


# ---------------------------------------------------------------- footer / lifesign


def test_lifesign_footer() -> None:
    s, buf = sender(16)
    s.SetLifeSignFooter(LifeSign=0x0A)
    assert buf[15] == 0x0A
    r = receiver(bytes([0] * 15 + [0xA0]))
    assert r.GetLifeSignFooter() == 0x0A  # RC -> PLC: LifeSign in the high nibble


def test_half_bytes() -> None:
    s, buf = sender()
    s.AddHalfBytes(HalfByteHi=0x0C, HalfByteLo=0x03)
    assert buf[0] == 0xC3
    r = receiver(b"\xc3")
    assert r.GetHalfeByte1(False) == 0x3
    assert r.GetHalfeByte2(True) == 0xC
    assert r.PayloadPtr == 1


# ---------------------------------------------------------------- structured values


def test_turn_number_example_of_the_spec() -> None:
    """Spec 1.5.9 table 5-26 (J1 -0, J2 +0, J3 -0, J4 +1, J5 +0, J6 -2, E1 +14)."""
    r = receiver(bytes([0x08, 0x18, 0xA0, 0x0E]))
    t = r.GetTurnNumbers()
    assert (t.J1Turns, t.J2Turns, t.J3Turns, t.J4Turns, t.J5Turns, t.J6Turns, t.E1Turns) == (
        0,
        0,
        0,
        1,
        0,
        -2,
        14,
    )
    s, buf = sender()
    s.AddTurnNumber(t)
    assert bytes(buf[:4]) == bytes([0x00, 0x10, 0xA0, 0x0E])  # "-0" cannot be represented by SINT (F11)


@pytest.mark.parametrize("turns", range(-7, 8))
def test_turn_nibble_roundtrip(turns: int) -> None:
    assert half_byte_to_turn(turn_to_half_byte(turns)) == turns


def test_turn_e1_range() -> None:
    assert half_byte_to_turn(turn_to_half_byte(-127, bits=7), bits=7) == -127
    with pytest.raises(ValueRangeError):
        turn_to_half_byte(8)
    s, _ = sender()
    with pytest.raises(ValueRangeError):
        s.AddTurnNumber(TurnNumber(J1Turns=-8))


def test_arm_config_roundtrip() -> None:
    cfg = ArmConfigParameter(
        Shoulder=ArmConfigShoulder.BACK, Elbow=ArmConfigElbow.UP, Wrist=ArmConfigWrist.FLIP
    )
    s, buf = sender()
    s.AddArmConfig(cfg)
    assert bytes(buf[:2]) == b"\x05\x00"
    assert receiver(bytes(buf[:2])).GetArmConfig() == cfg


def test_sync_flags() -> None:
    s, buf = sender()
    off = {f.name: False for f in DataEnableSync._IEC_FIELDS_}  # PLC library default is TRUE
    s.AddDataEnableSync(
        DataEnableSync(**{**off, "EnableSyncTool": True, "EnableSyncReferenceDynamics": True})
    )
    s.AddDataInSync(DataInSync(FramesInSync=True, SoftwareLimitsInSync=True))
    assert bytes(buf[:2]) == bytes([0b0100_0001, 0b0001_0010])
    r = receiver(bytes(buf[1:2]))
    assert r.GetDataInSync() == DataInSync(FramesInSync=True, SoftwareLimitsInSync=True)


def test_fragment_action_and_tracking_status() -> None:
    r = receiver(b"\x05\x81")
    fa = r.GetFragmentAction()
    assert (fa.Complete, fa.Reset, fa.Clear) == (True, False, True)
    ts = r.GetTrackingStatus()
    assert ts.ConveyorTrackingEnabled and ts.NotUsed and not ts.Synchronous


# ---------------------------------------------------------------- command / response buffers


def test_command_data_buffer() -> None:
    c = RobotLibraryCommandDataFB()
    assert len(c.Payload) == 256
    c.AddUint(0x1001)
    assert bytes(c.Payload[:2]) == b"\x10\x01"
    c.Reset()
    assert c.PayloadLen == 0 and not any(c.Payload)


def test_response_data_buffer() -> None:
    r = RobotLibraryResponseDataFB()
    r.Payload[0:2] = b"\x00\x2a"
    r.PayloadLen = 2
    assert r.IsPayloadRemaining
    assert r.GetUint() == 42
    assert not r.IsPayloadRemaining
