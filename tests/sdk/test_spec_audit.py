# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_spec_audit
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Findings of the specification audit (docs/ST_FINDINGS.md F61 ...) against the SRCI SDK.
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

"""Findings of the specification audit (docs/ST_FINDINGS.md F61 ...) against the SRCI SDK.

Every test names its finding; the fixes are ST-FIX patches (tools/st2py/config.py) or hand
fixes (tools/st2py/fix_guide_manual.md), described in docs/ST_Finding_Solve_Guide.md.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

import pytest

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.sim.sdk import SdkSimulator, sdk_transport
from srci.types import ComDirection, RobotLibraryErrorIdEnum, SequenceFlag
from srci.types.iec import new_instance
from tests.robot_task_harness import SIZE, RobotTaskHarness


@pytest.fixture(autouse=True)
def sdk_parameters(sdk_library: str) -> Iterator[None]:
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@contextmanager
def robot(
    two_sequences: bool = False, enable: bool = True, size: int = SIZE
) -> Iterator[tuple[SdkSimulator, RobotTaskHarness]]:
    from tests.sdk.test_core_fbs import enable as enable_robot

    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        sim.set_move_cycles(5)
        h = RobotTaskHarness(sdk_transport(sim, size, size), size=size, advance=clock.advance)
        if two_sequences:
            h.cfg.Com.TwoSequences = True
            h.cfg.Plc.OptionalCyclic.UseTwoSequences = True
            h.cfg.Rob.OptionalCyclic.UseTwoSequences = True
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, (hex(h.rt.ErrorID), h.history[-5:])
        if enable:
            enable_robot(h, sim)
        yield sim, h


def outputs_consistent(block: Any) -> list[str]:
    """Violations of the output rules of spec table 5-45 (empty list: consistent)."""
    flags = {n: bool(getattr(block, n, False)) for n in ("Busy", "Done", "Error", "CommandAborted", "Active")}
    problems = []
    if sum(flags[n] for n in ("Busy", "Done", "Error", "CommandAborted")) > 1:
        problems.append(f"Busy/Done/Error/CommandAborted not exclusive: {flags}")
    if flags["Active"] and (flags["Error"] or flags["Done"] or flags["CommandAborted"]):
        problems.append(f"Active together with an end state: {flags}")
    if bool(block.ErrorID) != flags["Error"]:
        problems.append(f"Error={flags['Error']} but ErrorID=16#{block.ErrorID:04X}")
    ended = any(flags[n] for n in ("Busy", "Done", "Error", "CommandAborted"))
    if hasattr(block, "Execute") and not hasattr(block, "Enable") and block.Execute and not ended:
        problems.append("Execute TRUE but none of Busy/Done/Error/CommandAborted")
    return problems


def run_checked(h: RobotTaskHarness, blocks: list[Any], cycles: int, until: Any) -> list[str]:
    """Runs ``cycles`` cycles and collects every output violation of ``blocks``."""
    problems: list[str] = []
    for _ in range(cycles):
        h.cycle()
        for b in blocks:
            problems += [f"{type(b).__name__}: {p}" for p in outputs_consistent(b)]
        if until():
            break
    return problems


def move_axes(h: RobotTaskHarness, **par: float) -> Any:
    mv = h.add(new_instance("MC_MoveAxesAbsoluteFB"))
    mv.ParCmd.JointPosition.J1 = 10.0
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = -1.0
    mv.ParCmd.JerkRate = -1.0
    for name, value in par.items():
        setattr(mv.ParCmd, name, value)
    return mv


# ------------------------------------------------------------------ F61 / F62: FB outputs


def test_f61_parameter_error_sets_error_in_the_same_cycle() -> None:
    """F61 (B-01/B-02): a parameter error sets ErrorID and Error in the same cycle."""
    with robot() as (_, h):
        mv = move_axes(h, VelocityRate=500.0)
        mv.Execute = True
        h.cycle()
        assert mv.Error and mv.ErrorID == RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID
        assert outputs_consistent(mv) == []


def test_f61_error_of_the_rc_resets_busy_at_once() -> None:
    """F61 (B-01): an error of the RC (DecelerationRate below the minimum: 16#8D06, previous SDK
    version 16#8E03) -> Error with ErrorID, Busy FALSE, no cycle with ErrorID but without Error."""
    with robot() as (_, h):
        mv = move_axes(h, DecelerationRate=0.5)
        mv.Execute = True
        problems = run_checked(h, [mv], 50, until=lambda: mv.Error)
        assert mv.Error and mv.ErrorID in (0x8D06, 0x8E03) and not mv.Busy
        assert problems == []


def test_f61_register_full_does_not_leave_busy() -> None:
    """F61 (B-03, BUF-01): commands that find no free ACR entry (16#8618) end with Error and
    without Busy; all outputs stay consistent."""
    count = int(str(srci.parameters()["ACTIVE_CMD_REGISTER_ENTRIES_MAX"])) + 3
    with robot() as (_, h):
        fbs = [move_axes(h) for _ in range(count)]
        for fb in fbs:
            fb.Execute = True
        problems = run_checked(h, fbs, count * 10, until=lambda: all(f.Done or f.Error for f in fbs))
        errors = [f for f in fbs if f.Error]
        assert errors and {f.ErrorID for f in errors} == {RobotLibraryErrorIdEnum.ERR_NO_FREE_ACR_ENTRY}
        assert not any(f.Busy for f in errors)
        assert problems == []


def test_f61_group_jog_active_and_error_exclusive() -> None:
    """F61 (B-04): GroupJog with an error of the RC (robot not enabled): Active is never TRUE
    together with Error, Error follows ErrorID."""
    from srci.types import JogMode

    with robot(enable=False) as (_, h):
        jog = h.add(new_instance("MC_GroupJogFB"))
        jog.ParCmd.Mode = JogMode.JOG_AXES
        jog.ParCmd.Override = 100
        jog.ParCmd.Control.Y_J2_Pos = True
        jog.Enable = True
        problems = run_checked(h, [jog], 60, until=lambda: False)
        jog.Enable = False
        problems += run_checked(h, [jog], 10, until=lambda: False)
        assert problems == []


# ------------------------------------------------------------------ F63: two telegram sequences


def test_f63_two_sequences_initialize_and_execute_commands() -> None:
    """F63 (A-01...A-06): with two telegram sequences the RobotTask initializes, and several
    commands at once are exchanged over both sequences in the order of the Seq numbers."""
    with robot(two_sequences=True) as (sim, h):
        fbs = [h.add(new_instance("MC_ReadRobotDataFB")) for _ in range(6)]
        for fb in fbs:
            fb.Execute = True
        h.run(100, until=lambda: all(fb.Done or fb.Error for fb in fbs))
        assert all(fb.Done for fb in fbs), [(fb.Error, hex(fb.ErrorID)) for fb in fbs]
        mv = move_axes(h)
        mv.Execute = True
        h.run(100, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done, hex(mv.ErrorID)
        seq = list(h.ag.State.CurrentSEQ)
        assert abs(seq[0] - seq[1]) == 1  # one common counter, the sequences alternate
        assert not [log.text for log in sim.logs if "decoding sequence" in log.text]
        assert not h.rt.Error


def test_f63_two_sequences_long_commands_are_fragmented_over_both_sequences() -> None:
    """F63 (A-02/A-05): commands longer than one sequence area are fragmented; each sequence
    stays within its half of the acyclic area (the RC decodes every fragment)."""
    with robot(two_sequences=True, size=128) as (sim, h):
        fbs = [move_axes(h) for _ in range(4)]
        for fb in fbs:
            fb.Execute = True
        h.run(300, until=lambda: all(fb.Done or fb.Error for fb in fbs))
        assert all(fb.Done for fb in fbs), [hex(fb.ErrorID) for fb in fbs]
        assert not [log.text for log in sim.logs if "sequence payload" in log.text]


def test_f63_two_sequences_only_in_one_direction_is_an_error() -> None:
    """F63 (A-08): TwoSequences set only in one direction -> 16#80AB, no initialization."""
    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sim, SIZE, SIZE), advance=clock.advance)
        h.cfg.Com.TwoSequences = True
        h.cfg.Plc.OptionalCyclic.UseTwoSequences = True
        h.run(30, until=lambda: bool(h.rt.Error))
        assert h.rt.Error and h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_INVALID_0x80AB
        assert not h.ag.State.CMDsEnabled


# ------------------------------------------------------------------ F64: Done of MoveSpline/MoveSuperImposed


def test_f64_move_superimposed_signals_done() -> None:
    """F64: MC_MoveSuperImposedFB reset Done on state DONE -> Execute TRUE without any status."""
    with robot() as (_, h):
        fb = h.add(new_instance("MC_MoveSuperImposedFB"))
        fb.ParCmd.Offset.X = 1.0
        fb.Execute = True
        problems = run_checked(h, [fb], 100, until=lambda: bool(fb.Done or fb.Error))
        assert fb.Done, (fb.Error, hex(fb.ErrorID))
        assert problems == []


# ------------------------------------------------------------------ F65 ... F68: RI errors of the RobotTask


class Interceptor:
    """Transport between RobotTask and SDK that can freeze or modify the telegram of the RC."""

    def __init__(self, inner: Any) -> None:
        self.inner = inner
        self.frozen: bytes | None = None
        self.modify: Callable[[bytes], bytes] | None = None

    def exchange(self, out: bytes) -> bytes:
        rsp = bytes(self.inner.exchange(out))
        if self.frozen is not None:
            return self.frozen
        return self.modify(rsp) if self.modify else rsp


@contextmanager
def intercepted() -> Iterator[tuple[SdkSimulator, RobotTaskHarness, Interceptor]]:
    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        tr = Interceptor(sdk_transport(sim, SIZE, SIZE))
        h = RobotTaskHarness(tr, advance=clock.advance)  # type: ignore[arg-type]
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        assert h.ag.State.CMDsEnabled
        yield sim, h, tr


def test_f65_lifesign_timeout_is_80a5() -> None:
    """F65 (C-02): the lifesign of the RC does not change -> 16#80A5 (table 7-2), not initialized."""
    with intercepted() as (_, h, tr):
        tr.frozen = bytes(h.rin)
        h.run(50, until=lambda: bool(h.rt.Error))
        assert h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_LIFESIGN_TIMEOUT_0x80A5
        assert not h.rt.Initialized


def test_f65_sequence_timeout_is_80a8() -> None:
    """F65 (C-03): the RC keeps the lifesign alive but acknowledges no sequence for
    4 x LifeSignTimeOut -> 16#80A8, not initialized."""
    with intercepted() as (_, h, tr):
        start = h.rt.CalculateSequencePayloadStartAdr(
            AxesGroup=h.ag, Direction=ComDirection.ROB_TO_PLC, Sequence=SequenceFlag.PRIMARY_SEQUENCE
        )
        old_ack = bytes(h.rin[start : start + 2])

        def keep_ack(rsp: bytes) -> bytes:  # lifesign alive, but no new Ack
            data = bytearray(rsp)
            data[start : start + 4] = old_ack + b"\x00\x00"
            return bytes(data)

        tr.modify = keep_ack
        cycles = h.run(100, until=lambda: bool(h.rt.Error))
        assert h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8_0x80A8, hex(
            h.rt.ErrorID
        )
        assert not h.rt.Initialized
        assert cycles * h.cycle_time * 1000 >= 4 * h.cfg.Com.LifeSignTimeOut


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (0xA5, 0xA5),  # RI error of the RC in the telegram state
        (0xAD, 0xAD),
        (254, RobotLibraryErrorIdEnum.ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7),
        (0, RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0x80A2),
    ],
)
def test_f65_reason_of_the_loss_of_initialization(state: int, expected: int) -> None:
    """F65 (C-01): the reason of the loss of the initialization is reported (table 7-2)."""
    with intercepted() as (_, h, tr):

        def set_state(rsp: bytes) -> bytes:
            data = bytearray(rsp)
            data[3] = state  # telegram state (table 5-83)
            return bytes(data)

        tr.modify = set_state
        h.run(5, until=lambda: bool(h.rt.Error))
        assert h.rt.Error and h.rt.ErrorID == expected, hex(h.rt.ErrorID)


def test_f66_invalid_frame_is_not_processed() -> None:
    """F66 (C-04): lifesign in header and footer differ -> frame counted and not processed."""
    with intercepted() as (_, h, tr):
        rd = h.add(new_instance("MC_ReadRobotDataFB"))
        rd.Execute = True

        def break_footer(rsp: bytes) -> bytes:
            data = bytearray(rsp)
            data[SIZE - 1] ^= 0x30  # lifesign of the footer (high nibble)
            return bytes(data)

        tr.modify = break_footer
        before = h.ag.State.InvalidFrames
        h.run(10)
        assert h.ag.State.InvalidFrames >= before + 9  # the frame of the cycle before was valid
        assert not rd.Done  # the responses of the invalid frames are not processed
        tr.modify = None
        h.run(50, until=lambda: bool(rd.Done or rd.Error))
        assert rd.Done


def test_f68_changed_telegram_number_is_a_warning() -> None:
    """F68 (C-06): optional cyclic data changed during operation -> warning 16#7003 (spec 6.1.1)."""
    from srci.types import RobotLibraryWarningIdEnum

    with intercepted() as (_, h, _tr):
        h.cfg.Rob.OptionalCyclic.UseJointPosition = not h.cfg.Rob.OptionalCyclic.UseJointPosition
        h.run(3)
        assert h.rt.WarningID == RobotLibraryWarningIdEnum.WARN_TELEGRAM_NO_CHANGED_DURING_OPERATION
        assert not h.rt.Error and h.ag.State.CMDsEnabled


# ------------------------------------------------------------------ F69 ... F73: parameter checks


def first_error(block: Any, **inputs: Any) -> int:
    """Starts ``block`` with ``inputs`` (``ParCmd.X`` as ``ParCmd__X``) and returns ErrorID after
    one cycle (client-side checks: the command is not sent)."""
    with robot(enable=False) as (_sim, h):
        h.add(block)
        for name, value in inputs.items():
            target = block
            *path, last = name.split("__")
            for part in path:
                target = getattr(target, part)
            if "[" in last:
                attr, idx = last.rstrip("]").split("[")
                getattr(target, attr)[int(idx)] = value
            else:
                setattr(target, last, value)
        if hasattr(block, "Execute"):
            block.Execute = True
        else:
            block.Enable = True
        h.cycle()
        assert outputs_consistent(block) == []
        return int(block.ErrorID)


P = RobotLibraryErrorIdEnum
PM = "ProcessingMode"
SF = "SequenceFlag"


@pytest.mark.parametrize(
    ("name", "inputs", "expected"),
    [
        # F69 (D-01): EmitterID range -127..127 (table 5-62)
        ("MC_MoveLinearAbsoluteFB", {"ParCmd__EmitterID[2]": -128}, P.ERR_EMITTERID_NOT_ALLOWED),
        ("MC_SetTriggerUserFB", {"ParCmd__EmitterID": -128}, P.ERR_EMITTERID_NOT_ALLOWED),
        # F69 (D-02): ListenerID negative / 0 in a trigger mode / > 0 in a mode without trigger
        ("MC_ReadIntegersFB", {"ParCmd__ListenerID": -1}, P.ERR_LISTENERID_MUST_BE_POSITIVE),
        ("MC_ReactAtTriggerFB", {"ParCmd__ListenerID": 0}, P.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
        ("MC_ReadIntegersFB", {PM: 12, "ParCmd__ListenerID": 0}, P.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
        ("MC_ReadIntegersFB", {PM: 2, "ParCmd__ListenerID": 3}, P.ERR_LISTENERID_NOT_ALLOWED),
        # F69 (D-03): SequenceFlag against the ProcessingMode (e.g. table 6-496)
        ("MC_ReadIntegersFB", {PM: 2, SF: 1}, P.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        ("MC_ReadIntegersFB", {PM: 0, SF: 0}, P.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        ("MC_WriteIntegersFB", {PM: 3, SF: 2}, P.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        # F70 (D-04/D-05/D-06): the error IDs of the specification
        ("MC_ReadIntegersFB", {PM: 10, "ParCmd__ListenerID": 1}, P.ERR_PROCESSINGMODE_NOT_ALLOWED),
        ("MC_ReadIntegersFB", {SF: 7}, P.ERR_SEQFLAG_NOT_ALLOWED),
        ("MC_MoveSuperImposedFB", {"ParCmd__EmitterID[1]": -128}, P.ERR_EMITTERID_NOT_ALLOWED),
        ("MC_GroupJogFB", {"ParCmd__Override": 101.0}, P.ERR_OVERRIDE_INVALID),
        # F71 (D-08): Priority 1..4
        ("MC_ReadRobotDataFB", {"Priority": 0}, P.ERR_PRIORITY_TOO_HIGH),
        ("MC_ReadRobotDataFB", {"Priority": 5}, P.ERR_PRIORITY_TOO_LOW),
    ],
)
def test_f69_f71_parameter_checks(name: str, inputs: dict[str, Any], expected: int) -> None:
    """F69...F71: invalid parameters are rejected by the client with the ID of table 7-1."""
    assert first_error(new_instance(name), **inputs) == expected


@pytest.mark.parametrize("name", ["MC_ReadIntegersFB", "MC_WriteIntegersFB", "MC_CallSubprogramFB"])
def test_f69_defaults_are_valid(name: str) -> None:
    """F69: the default values of the function blocks pass the new checks."""
    assert first_error(new_instance(name)) not in {
        P.ERR_SEQFLAG_INVALID_IN_PROC_MODE,
        P.ERR_LISTENERID_NOT_ALLOWED,
        P.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO,
        P.ERR_ACYCLICDATA_TOO_LARGE,
    }


def test_f73_read_actual_position_cyclic_with_current_tool() -> None:
    """F73 (D-10): ToolNo/FrameNo -1 (currently used) -> the outputs are updated."""
    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        sim.set_move_cycles(5)
        h = RobotTaskHarness(sdk_transport(sim, SIZE, SIZE), advance=clock.advance)
        h.cfg.Rob.OptionalCyclic.UseJointPosition = True
        h.cfg.Rob.OptionalCyclic.UseCartesianPosition = True
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        cyc = h.add(new_instance("MC_ReadActualPositionCyclicFB"))
        cyc.ParCmd.ReadJointPosition = cyc.ParCmd.ReadCartesianPosition = True
        cyc.ParCmd.ToolNo = cyc.ParCmd.FrameNo = -1
        cyc.Enable = True
        h.run(20, until=lambda: bool(cyc.Enabled or cyc.Error))
        assert cyc.Enabled and not cyc.Error, hex(cyc.ErrorID)


# ------------------------------------------------------------------ F74/F75: message buffer, IDs


def test_f74_client_error_is_in_the_message_buffer_with_acr_entry_and_type() -> None:
    """F74 (E-01/E-03): a parameter error of the client and an error of the RC are written into
    the message buffer; messages of a sent command carry its ACR entry and command type."""
    from srci.types import CmdType, MessageType, Severity

    with robot() as (_, h):
        h.rt.LogLevel = Severity.DEBUG
        bad = move_axes(h, VelocityRate=500.0)
        bad.Execute = True
        rc = move_axes(h, DecelerationRate=0.5)
        rc.Execute = True
        h.run(50, until=lambda: bool(bad.Error and rc.Error))
        h.run(2)
        msgs = [m for m in h.ag.MessageLog.Messages if m.MessageType == MessageType.CMD and m.MessageCode]
        by_code = {m.MessageCode: m for m in msgs}
        assert RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID in by_code, [hex(m.MessageCode) for m in msgs]
        client = by_code[RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID]
        assert client.Severity == Severity.ERROR  # not sent: no ACR entry / command type
        assert "MC_MoveAxesAbsoluteFB" in client.MessageText
        server = by_code.get(0x8D06) or by_code[0x8E03]  # SDK 1.0.0-RC2 / previous version
        assert server.AcrID > 0 and server.CmdType == CmdType.MoveAxesAbsolute


def test_e02_group_reset_clears_the_message_buffer() -> None:
    """E-02 (already fulfilled, no fix): GroupReset deletes the messages of the PLC buffer (5.5.11.5)."""
    from srci.types import Severity

    with robot() as (_, h):
        h.rt.LogLevel = Severity.DEBUG
        bad = move_axes(h, VelocityRate=500.0)
        bad.Execute = True
        h.run(3)
        assert h.ag.MessageLog.MessagesEntries > 0
        reset = h.add(new_instance("MC_GroupResetFB"))
        reset.Execute = True
        h.run(2)
        assert h.ag.MessageLog.MessagesEntries == 0


def test_f75_missing_ids_of_the_specification() -> None:
    """F75 (E-05/C-08): IDs of tables 7-1/7-4 and names with the correct value."""
    from srci.types import RobotLibraryInfoIdEnum

    assert RobotLibraryErrorIdEnum(0x8D52).name == "ERR_INVALID_PARAM_EMITTERID_EQUALS_LISTENERID"
    assert RobotLibraryErrorIdEnum(0x8E22).name == "ERR_OPTIONAL_PARAM_EXTERNAL_TCP_NOT_SUPPORTED"
    assert RobotLibraryInfoIdEnum(0x6D54).name == "INFO_TRIGGER_PARAMETERS_NOT_USED"
    assert RobotLibraryErrorIdEnum.ERR_LIFESIGN_TIMEOUT_0x8004 == 0x8004
    assert RobotLibraryErrorIdEnum.ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8 == 0x80A8
