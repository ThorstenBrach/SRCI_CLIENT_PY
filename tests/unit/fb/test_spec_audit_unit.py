# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.fb.test_spec_audit_unit
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Findings of the specification audit (docs/ST_FINDINGS.md F61 ...) without the SDK.
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

"""Findings of the specification audit (docs/ST_FINDINGS.md F61 ...) without the SDK."""

from __future__ import annotations

from srci.fb import MC_MoveAxesAbsoluteFB
from srci.types import (
    AxesGroupAcyclicAcrEntryRspBuffer,
    CmdMessageState,
    ComDirection,
    RobotLibraryErrorIdEnum,
    SequenceFlag,
    Severity,
    SystemTime,
)
from tests.helpers import Host, new_axes_group


def response(state: CmdMessageState, severity: int = 0, code: int = 0) -> AxesGroupAcyclicAcrEntryRspBuffer:
    rsp = AxesGroupAcyclicAcrEntryRspBuffer()
    rsp.Payload[0] = 0x10 | int(state)  # ParSeq 1, State (table 5-120)
    rsp.Payload[1] = severity & 0xFF
    rsp.Payload[2], rsp.Payload[3] = code >> 8, code & 0xFF
    rsp.PayloadLen = 4
    return rsp


def test_f61_state_error_without_code_is_8613() -> None:
    """F61 (B-05): response state ERROR without error code -> 16#8613, Error TRUE."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.CallBack(RspData=response(CmdMessageState.ERROR), Timestamp=SystemTime())
    assert fb.ErrorID == RobotLibraryErrorIdEnum.ERR_ROBOT_ERROR_NO_ID
    assert fb.Error and not fb.Busy


def test_f61_state_error_with_warning_only_is_8613() -> None:
    """F61 (B-05): state ERROR with severity WARNING -> warning kept and 16#8613."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.CallBack(RspData=response(CmdMessageState.ERROR, Severity.WARNING, 0x7001), Timestamp=SystemTime())
    assert fb.WarningID == 0x7001
    assert fb.ErrorID == RobotLibraryErrorIdEnum.ERR_ROBOT_ERROR_NO_ID and fb.Error


def test_f61_error_of_the_rc_sets_error_at_once() -> None:
    """F61 (B-01): the response with an error sets Error together with ErrorID (not one cycle
    later) and resets Busy."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.Busy = True
    fb.CallBack(RspData=response(CmdMessageState.ERROR, Severity.ERROR, 0x8E03), Timestamp=SystemTime())
    assert fb.ErrorID == 0x8E03 and fb.Error and not fb.Busy


def test_f62_warning_and_info_are_held_until_reset() -> None:
    """F62 (B-06): a later response without message does not clear WarningID/InfoID."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.CallBack(RspData=response(CmdMessageState.ACTIVE, Severity.WARNING, 0x7001), Timestamp=SystemTime())
    assert fb.WarningID == 0x7001
    fb.CallBack(RspData=response(CmdMessageState.ACTIVE, Severity.INFO, 0x6001), Timestamp=SystemTime())
    fb.CallBack(RspData=response(CmdMessageState.DONE), Timestamp=SystemTime())
    assert (fb.WarningID, fb.InfoID, fb.ErrorID) == (0x7001, 0x6001, 0)
    fb.Reset()
    assert (fb.WarningID, fb.InfoID) == (0, 0)


# ------------------------------------------------------------------ F63 telegram sequence areas


def areas(host: Host, direction: ComDirection) -> list[tuple[int, int]]:
    ag, _ = new_axes_group()
    return [
        (
            host.CalculateSequencePayloadStartAdr(AxesGroup=ag, Direction=direction, Sequence=s),
            host.CalculateSequencePayloadMax(AxesGroup=ag, Direction=direction, Sequence=s),
        )
        for s in (SequenceFlag.PRIMARY_SEQUENCE, SequenceFlag.SECONDARY_SEQUENCE)
    ]


def test_f63_one_sequence_area_is_the_acyclic_area() -> None:
    """F63 (A-03): one sequence: area = telegram length - cyclic data - footer."""
    host = Host()
    (start, size), (_, size2) = areas(host, ComDirection.ROB_TO_PLC)
    assert (start, size, size2) == (10, 128 - 10 - 1, 0)


def test_f63_two_sequences_halve_the_acyclic_area() -> None:
    """F63 (A-02/A-03): two sequences: the acyclic area is halved like in spec Fig. 5-205 and in
    the SDK (1st = area / 2 behind the cyclic data, 2nd = rest behind the 1st); no overlap."""
    host = Host()
    host._parCfg.Com.TwoSequences = True
    for direction, length, cyclic in ((ComDirection.ROB_TO_PLC, 128, 10), (ComDirection.PLC_TO_ROB, 64, 18)):
        (s1, n1), (s2, n2) = areas(host, direction)
        area = length - cyclic - 1
        assert (s1, n1) == (cyclic, area // 2)
        assert (s2, n2) == (cyclic + area // 2, area - area // 2)
        assert s2 + n2 == length - 1  # the footer follows


def test_f63_second_sequence_is_sent_at_its_address() -> None:
    """F63 (A-04): both sequence headers are written, the 2nd one at its own address, and both
    NewSEQ flags are reset after sending."""
    host, (ag, _) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    ag.State.SequenceCountSend = 1
    ag.State.NewSEQ[0] = ag.State.NewSEQ[1] = True
    host.Telegram.PlcToRob.Header.TelegramLengthPlcToRob = 64
    host.Telegram.PlcToRob.Sequence[0].Header.SEQ_ACK = 5
    host.Telegram.PlcToRob.Sequence[1].Header.SEQ_ACK = 6
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    (s1, _), (s2, _) = areas(host, ComDirection.PLC_TO_ROB)
    assert out[s1 : s1 + 4] == bytes.fromhex("0005 0000")
    assert out[s2 : s2 + 4] == bytes.fromhex("0006 0000")
    assert ag.State.NewSEQ == [False, False]


def recv_telegram(host: Host, acks: tuple[int, int], cmd_ids: tuple[int, int]) -> bytearray:
    data = bytearray(128)
    for idx, (ack, cmd) in enumerate(zip(acks, cmd_ids, strict=True)):
        start = areas(host, ComDirection.ROB_TO_PLC)[idx][0]
        frag = cmd.to_bytes(2, "big") + bytes([0, 1]) + (0).to_bytes(2, "big") + (4).to_bytes(2, "big")
        payload = frag + bytes([0x1A, 0, 0, 0])  # State DONE
        data[start : start + 4] = ack.to_bytes(2, "big") + len(payload).to_bytes(2, "big")
        data[start + 4 : start + 4 + len(payload)] = payload
    return data


def test_f63_responses_are_processed_in_the_order_of_the_ack() -> None:
    """F63 (A-06): both sequences acknowledged in one telegram -> the one with the lower Ack
    first (spec Fig. 5-207/5-208), independent of its position in the telegram."""
    host, (ag, acr) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    ag.State.CurrentSEQ[0], ag.State.CurrentSEQ[1] = 8, 7
    host.ParseRecvPayload(ag, recv_telegram(host, (8, 7), (0x0101, 0x0202)))
    assert [cmd for cmd, _ in acr.responses] == [0x0202, 0x0101]


def test_f63_ack_of_an_other_seq_is_ignored() -> None:
    """F63: a sequence whose Ack is not the Seq that was sent (the SDK sends Ack 0 in the
    sequence it does not process) carries no response."""
    host, (ag, acr) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    ag.State.CurrentSEQ[0], ag.State.CurrentSEQ[1] = 8, 9
    host.ParseRecvPayload(ag, recv_telegram(host, (8, 0), (0x0101, 0x0202)))
    assert [cmd for cmd, _ in acr.responses] == [0x0101]
