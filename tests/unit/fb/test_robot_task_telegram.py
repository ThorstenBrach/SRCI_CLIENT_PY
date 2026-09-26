"""MC_RobotTaskFB telegram coding (CreateSendPayload*, ParseRecvPayload*, Calculate*).

Expected bytes are built from the tables of the SRCI profile V1.5.9 (5-82, 5-83, 5-89, 5-97).
"""

from __future__ import annotations

import struct
from typing import Any

import pytest

from srci.fb.General.MC_RobotTask.MC_RobotTaskFB_Telegram import MC_RobotTaskFB_Telegram
from srci.types import (
    AxesGroup,
    CmdMessageState,
    ComDirection,
    SequenceFlag,
    SystemTime,
    TelegramRobToPlcFragment,
    TelegramState,
)


class FakeACR:
    def __init__(self) -> None:
        self.responses: list[tuple[int, bytes]] = []

    def AddRsp(self, Rsp: TelegramRobToPlcFragment) -> int:
        start = Rsp.Header.PayloadPointer
        self.responses.append(
            (Rsp.Header.CmdID, bytes(Rsp.Command.Payload[start : start + Rsp.Header.PayloadLength]))
        )
        return 0


class Host(MC_RobotTaskFB_Telegram):
    def __init__(self) -> None:
        super().__init__()
        self.SystemTime = SystemTime()
        self.logs: list[dict[str, Any]] = []
        self._parCfg.Com.TelegramLengthPlcToRob = 64
        self._parCfg.Com.TelegramLengthRobToPlc = 128

    def _log(self, **kw: Any) -> None:
        self.logs.append(kw)

    CreateLogMessagePara1 = CreateLogMessagePara2 = CreateLogMessagePara3 = _log
    CreateLogMessagePara4 = CreateLogMessagePara5 = _log


def new_axes_group() -> tuple[AxesGroup, FakeACR]:
    ag = AxesGroup()
    acr = FakeACR()
    ag.Acyclic.ActiveCommandRegister = acr
    return ag, acr


PLC_OPT = ["SubProgramData", "CartesianPosition", "JointPosition", "Force", "CartesianPositionExt",
           "JointPositionExt", "ForceExt"]  # fmt: skip
ROB_OPT = ["SubProgramData", "CartesianPosition", "JointPosition", "Force", "Current", "CartesianPositionExt",
           "JointPositionExt", "ForceExt", "CurrentExt"]  # fmt: skip


# ======================================================================= send


def fill_header(host: Host) -> None:
    h = host.Telegram.PlcToRob.Header
    h.SRCIVersion = 0x25
    h.FastStop_LifeSign = 0x03
    h.TelegramLengthPlcToRob = 64
    h.TelegramLengthRobToPlc = 128
    h.AxesGroupID_Control = 0x01
    h.TelegramNumberPlcToRob = 0x0002
    h.TelegramNumberRobToPlc = 0x0006
    h.ClientDate = 0x2B67
    h.ClientTime = 3_600_000


HEADER = bytes.fromhex("25 03 0040 0080 01 00 0002 0006 2B67 0036EE80")


def test_send_header_table_5_82() -> None:
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    assert len(HEADER) == 18
    assert bytes(out[:18]) == HEADER


def test_send_complete_telegram_with_fragment() -> None:
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    ag.Cyclic.PlcToRob.LifeSign = 0x03
    ag.State.SequenceCountSend = 0
    ag.State.FragmentCountSend[0] = 0
    seq = host.Telegram.PlcToRob.Sequence[0]
    seq.Header.SEQ_ACK = 7
    seq.Header.PayloadLength = 8 + 4
    frag = seq.Fragment[0]
    frag.Header.CmdID = 0x0101
    frag.Header.FragmentAction = 0x01
    frag.Header.PayloadPointer = 0
    frag.Header.PayloadLength = 4
    frag.Command.Payload[0:4] = [0x03, 0xE8, 0x10, 0x00]
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    expected = (
        HEADER
        + bytes.fromhex("0007 000C")
        + bytes.fromhex("0101 00 01 0000 0004")
        + bytes.fromhex("03E81000")
    )
    assert bytes(out[: len(expected)]) == expected
    assert out[63] == 0x03  # footer: LifeSign in the low nibble of the last byte (table 5-84)
    assert not any(out[len(expected) : 63])
    assert ag.State.NewSEQ[0] is False


def test_fragment_payload_pointer_offset() -> None:
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    frag = host.Telegram.PlcToRob.Sequence[0].Fragment[0]
    frag.Header.PayloadPointer = 2
    frag.Header.PayloadLength = 2
    frag.Command.Payload[0:4] = [1, 2, 3, 4]
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    assert bytes(out[22 + 8 : 22 + 10]) == b"\x03\x04"


def test_tool_frame_only_with_cartesian_position_rc_to_plc() -> None:
    """ST-FIX F2: ToolNo/FrameNo (table 5-90) only if 'Cartesian Position' RC -> PLC is configured."""
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    host.Telegram.PlcToRob.Cyclic.ToolNo = 3
    host.Telegram.PlcToRob.Cyclic.FrameNo = 4
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    assert out[18:22] == bytes(4)  # sequence header directly after the header
    ag.CyclicOptional.RobToPlc.CartesianPosition.Active = True
    host.CreateSendPayload(ag, out)
    assert out[18:20] == b"\x03\x04"


def test_send_cartesian_position_table_5_97() -> None:
    """ST-FIX F1: Config has two bytes, the position has 34 bytes."""
    host, (ag, _) = Host(), new_axes_group()
    ag.CyclicOptional.PlcToRob.CartesianPosition.Active = True
    pos = host.Telegram.PlcToRob.CyclicOptional.CartesianPosition
    pos.X, pos.Y, pos.Z, pos.Rx, pos.Ry, pos.Rz = 1.0, 2.0, 3.0, 4.0, 5.0, 6.0
    pos.Config = 0b101
    pos.Turns_J2_J1, pos.Turns_J4_J3, pos.Turns_J6_J5, pos.Turns_E1 = 0x10, 0x20, 0x30, 0x40
    pos.E1 = 7.0
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    block = bytes(out[18 : 18 + 34])
    assert block == struct.pack(">6f", 1, 2, 3, 4, 5, 6) + b"\x05\x00\x10\x20\x30\x40" + struct.pack(">f", 7)


@pytest.mark.parametrize("mask", range(0, 1 << len(PLC_OPT), 7))
def test_calculated_length_matches_written_bytes_plc_to_rob(mask: int) -> None:
    host, (ag, _) = Host(), new_axes_group()
    host._parCfg.Com.TelegramLengthPlcToRob = 256
    for i, name in enumerate(PLC_OPT):
        getattr(ag.CyclicOptional.PlcToRob, name).Active = bool(mask & (1 << i))
    ag.CyclicOptional.RobToPlc.CartesianPosition.Active = bool(mask & 1)
    host.SendData(Payload=bytearray(256))
    host.CreateSendPayloadHeader(ag)
    host.CreateSendPayloadCyclic(ag)
    host.CreateSendPayloadCyclicOptional(ag)
    assert host.SendData.PayloadPtr == host.CalculateCyclicDataLength(ag, ComDirection.PLC_TO_ROB)


def test_second_sequence_starts_at_calculated_address() -> None:
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    host._parCfg.Com.TwoSequences = True
    ag.State.SequenceCountSend = 1
    host.Telegram.PlcToRob.Sequence[1].Header.SEQ_ACK = 0xABCD
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    start = host.CalculateSequencePayloadStartAdr(
        ag, ComDirection.PLC_TO_ROB, SequenceFlag.SECONDARY_SEQUENCE
    )
    assert start == 18 + (64 - 18) // 2
    assert out[start : start + 2] == b"\xab\xcd"


def test_sequence_stops_at_telegram_limit() -> None:
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    host.Telegram.PlcToRob.Header.TelegramLengthPlcToRob = 22  # header + sequence header
    frag = host.Telegram.PlcToRob.Sequence[0].Fragment[0]
    frag.Header.PayloadLength = 4
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    assert host.SendData.PayloadLen == 22  # no fragment written


def test_send_logging() -> None:
    host, (ag, _) = Host(), new_axes_group()
    host.Telegram.PlcToRob.Sequence[0].Header.PayloadLength = 1
    ag.State.NewSEQ[0] = True
    host.CreateSendPayload(ag, bytearray(64))
    assert host.logs and "Bytes send in total" in host.logs[0]["MessageText"]


# ======================================================================= receive


def rc_header(lifesign: int = 3, state: int = 255, status: int = 0x81, override: int = 5000) -> bytes:
    """Table 5-83."""
    return bytes([0x25, lifesign << 4, 0, state]) + struct.pack("<I", status) + struct.pack(">H", override)


def rc_telegram(body: bytes, size: int = 128, lifesign: int = 3) -> bytes:
    data = bytearray(size)
    data[: len(body)] = body
    data[-1] = lifesign << 4  # table 5-85: LifeSign in the high nibble
    return bytes(data)


def fragment(cmd_id: int, payload: bytes, pointer: int = 0, action: int = 1) -> bytes:
    return struct.pack(">HBBHH", cmd_id, 0, action, pointer, len(payload)) + payload


def test_receive_header_and_footer() -> None:
    host, (ag, _) = Host(), new_axes_group()
    data = rc_telegram(rc_header() + struct.pack(">HH", 0, 0))
    host.ParseRecvPayload(ag, data)
    h = host.Telegram.RobToPlc.Header
    assert (h.SRCIVersion.MajorVersion, h.SRCIVersion.MinorVersion) == (1, 5)
    assert h.LifeSign == 3 and h.TelegramState == TelegramState.INITIALIZED
    assert h.StatusRobotArm == 0x81 and h.Override == 5000
    assert host.Telegram.RobToPlc.Footer.LifeSign == 3


def test_receive_sequence_with_response() -> None:
    host, (ag, acr) = Host(), new_axes_group()
    rsp = bytes([0x21, 0xFE, 0x12, 0x34, 0xAA])  # State 1, ParSeq 2, severity -2, code 0x1234, data
    body = rc_header() + struct.pack(">HH", 5, 8 + len(rsp)) + fragment(0x0101, rsp)
    host.ParseRecvPayload(ag, rc_telegram(body))
    frag = host.Telegram.RobToPlc.Sequence[0].Fragment[0]
    assert acr.responses == [(0x0101, rsp)]
    assert frag.Command.Header.State == CmdMessageState(1)
    assert frag.Command.Header.ParSeq == 2
    assert frag.Command.Header.AlarmMessageSeverity == -2
    assert frag.Command.Header.AlarmMessageCode == 0x1234
    assert ag.State.LastACK[0] == 5


def test_same_ack_is_not_processed_twice() -> None:
    host, (ag, acr) = Host(), new_axes_group()
    body = rc_header() + struct.pack(">HH", 5, 9) + fragment(0x0101, b"\x01")
    host.ParseRecvPayload(ag, rc_telegram(body))
    host.ParseRecvPayload(ag, rc_telegram(body))
    assert len(acr.responses) == 1


def test_two_fragments_in_one_sequence() -> None:
    host, (ag, acr) = Host(), new_axes_group()
    payload = fragment(1, b"\x01\x02") + fragment(2, b"\x03", pointer=0)
    body = rc_header() + struct.pack(">HH", 1, len(payload)) + payload
    host.ParseRecvPayload(ag, rc_telegram(body))
    assert acr.responses == [(1, b"\x01\x02"), (2, b"\x03")]


def test_second_sequence_is_parsed_from_its_start_address() -> None:
    """ST-FIX F5: fragment index and payload pointer restart for the second sequence."""
    host, (ag, acr) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    start = host.CalculateSequencePayloadStartAdr(
        ag, ComDirection.ROB_TO_PLC, SequenceFlag.SECONDARY_SEQUENCE
    )
    assert start == 10 + (128 - 10) // 2
    first = rc_header() + struct.pack(">HH", 1, 9) + fragment(1, b"\x11")
    second = struct.pack(">HH", 1, 9) + fragment(2, b"\x22")
    data = bytearray(rc_telegram(first))
    data[start : start + len(second)] = second
    host.ParseRecvPayload(ag, bytes(data))
    assert acr.responses == [(1, b"\x11"), (2, b"\x22")]
    assert host.Telegram.RobToPlc.Sequence[1].Fragment[0].Header.CmdID == 2


def test_invalid_fragment_pointer_is_logged() -> None:
    host, (ag, acr) = Host(), new_axes_group()
    body = rc_header() + struct.pack(">HH", 1, 10) + fragment(1, b"\x01\x02", pointer=255)
    host.ParseRecvPayload(ag, rc_telegram(body))
    assert acr.responses == []
    assert any("Invalid fragment payload pointer" in log["MessageText"] for log in host.logs)


def test_invalid_sequence_length_is_logged() -> None:
    host, (ag, acr) = Host(), new_axes_group()
    body = rc_header() + struct.pack(">HH", 1, 500)
    host.ParseRecvPayload(ag, rc_telegram(body))
    assert acr.responses == []
    assert any("Invalid sequence payload length" in log["MessageText"] for log in host.logs)


def test_receive_cartesian_position_table_5_89() -> None:
    host, (ag, _) = Host(), new_axes_group()
    ag.CyclicOptional.RobToPlc.CartesianPosition.Active = True
    pos = (
        struct.pack(">6f", 1, 2, 3, 4, 5, 6)
        + b"\x05\x00\x10\x20\x30\x40"
        + struct.pack(">f", 7)
        + bytes([1, 2, 3, 4, 0, 0])
    )
    assert len(pos) == 40
    host.ParseRecvPayload(ag, rc_telegram(rc_header() + pos + struct.pack(">HH", 0, 0)))
    p = host.Telegram.RobToPlc.CyclicOptional.CartesianPosition
    assert (p.X, p.Rz, p.E1) == (1.0, 6.0, 7.0)
    assert p.Config == 0x0500 and p.Turns_J2_J1 == 0x10 and p.Turns_E1 == 0x40
    assert (p.ToolNo, p.FrameNo, p.CurrentlyUsedToolNo, p.CurrentlyUsedFrameNo) == (1, 2, 3, 4)


@pytest.mark.parametrize("mask", range(0, 1 << len(ROB_OPT), 23))
def test_calculated_length_matches_read_bytes_rob_to_plc(mask: int) -> None:
    host, (ag, _) = Host(), new_axes_group()
    for i, name in enumerate(ROB_OPT):
        getattr(ag.CyclicOptional.RobToPlc, name).Active = bool(mask & (1 << i))
    host.RecvData(Payload=bytes(512))
    host.ParseRecvPayloadHeader(ag)
    host.ParseRecvPayloadCyclic(ag)
    host.ParseRecvPayloadCyclicOptional(ag)
    assert host.RecvData.PayloadPtr == host.CalculateCyclicDataLength(ag, ComDirection.ROB_TO_PLC)


# ======================================================================= lengths


def test_payload_max_and_telegram_length() -> None:
    host, (ag, _) = Host(), new_axes_group()
    assert (
        host.CalculateSequencePayloadMax(ag, ComDirection.PLC_TO_ROB, SequenceFlag.PRIMARY_SEQUENCE)
        == 64 - 18
    )
    assert (
        host.CalculateSequencePayloadMax(ag, ComDirection.ROB_TO_PLC, SequenceFlag.SECONDARY_SEQUENCE) == 59
    )
    assert host.CalculateSequencePayloadMax(ag, ComDirection.PLC_TO_ROB, SequenceFlag.NO_SEQUENCE) == 0
    host.Telegram.PlcToRob.Sequence[0].Header.PayloadLength = 10
    assert host.CalculateTelegramLengthPlcToRob(ag) == 18 + 4 + 10 + 2
    host._parCfg.Com.TwoSequences = True
    host.Telegram.PlcToRob.Sequence[1].Header.PayloadLength = 3
    assert host.CalculateTelegramLengthPlcToRob(ag) == 18 + 4 + 10 + 4 + 3 + 2


def test_all_optional_combinations_fit_the_sizeof_table() -> None:
    """Spec tables 5-87/5-88: bytes required per optional cyclic block (RC -> PLC)."""
    host, (ag, _) = Host(), new_axes_group()
    expected = {"SubProgramData": 26, "CartesianPosition": 40, "JointPosition": 30, "Force": 24, "Current": 24,
                "CartesianPositionExt": 20, "JointPositionExt": 20, "ForceExt": 24, "CurrentExt": 24}  # fmt: skip
    for name, size in expected.items():
        for other in ROB_OPT:
            getattr(ag.CyclicOptional.RobToPlc, other).Active = other == name
        assert host.CalculateCyclicDataLength(ag, ComDirection.ROB_TO_PLC) == 10 + size, name
