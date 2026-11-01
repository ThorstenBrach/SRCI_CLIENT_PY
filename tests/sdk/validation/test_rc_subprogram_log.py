# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_subprogram_log
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of CallSubprogram / StopSubprogram: behaviour of the robot controller.
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

"""Validation tests of CallSubprogram / StopSubprogram: behaviour of the robot controller.

The SDK harness simulates a subprogram (``SdkSimulator.set_subprogram_cycles``): it runs a number
of cycles with Progress / InProgress, stands still while its sequence is interrupted, ends with
ABORTED on an abort request or a matching StopSubprogram and starts again after every run in
ProcessingMode CONTINUOUS. StopSubprogram is answered by the (modified) SDK itself, including the
info codes for "nothing to stop" and the checks of StopMode / TargetID.

The simulated subprogram has no content: it moves no axis, raises no error of its own and has no
cyclic data. Where the specified behaviour needs that, the test is a strict ``xfail`` (SDK-GAP);
where the client library deviates from the specification, a strict ``xfail`` (LIB-BUG).
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import (
    ProcessingMode,
    RobotLibraryErrorIdEnum,
    RobotLibraryInfoIdEnum,
    SequenceFlag,
    StopMode,
)
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, order, state, watch

CALL_SUBPROGRAM = 7001
STOP_SUBPROGRAM = 7008
SUB_CYCLES = 30  # cycles of one run of the simulated subprogram
E = RobotLibraryErrorIdEnum
I = RobotLibraryInfoIdEnum  # noqa: E741
PM = ProcessingMode
SF = SequenceFlag

PRIMARY = (PM.BUFFERED, SF.PRIMARY_SEQUENCE)
PRIMARY_ABORTING = (PM.ABORTING, SF.PRIMARY_SEQUENCE)
PARALLEL = (PM.PARALLEL, SF.NO_SEQUENCE)
CONTINUOUS = (PM.CONTINUOUS, SF.NO_SEQUENCE)

_GAP_BUFFERED = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated CallSubprogram answers the first telegram with ACTIVE and never reports "
    "BUFFERED, so CommandBuffered is not set; an RC confirms the command with BUFFERED before it starts it "
    "(spec 5.6 command states, CallSubprogram interface: CommandBuffered mandatory)",
)
_BUG_PARAMETER_ACCEPTED = pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F120: MC_CallSubprogramFB never sets ParameterAccepted (OnUpdateStateFlags sets it for no "
    "state, only Reset / CheckParameterChanged clear it); spec interface CallSubprogram: ParameterAccepted "
    "is a mandatory output (parameters acknowledged by the RC)",
)
_BUG_INSTANCE_ID = pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F121: MC_CallSubprogramFB.OnApplyOutCmd writes OutCmd.InstanceID := 0 (marked ToDo); spec "
    "interface CallSubprogram: InstanceID is a mandatory unique ID, the TargetID of StopSubprogram with "
    "StopMode 1 (6.5.21). The response telegram (table 6-710) has no InstanceID, its source must be defined",
)
_GAP_RC_ERROR = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: no stimulus for an error inside a running subprogram of the sequence; the simulated "
    "subprogram ignores motion errors (set_motion_error) and set_command_error ends it with ERROR. Expected "
    "RC reaction: the sequence is interrupted, the call reports CommandInterrupted",
)
_GAP_JOB_CHANGE = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the harness restarts the continuous subprogram with the new JobID; spec table 7-1: "
    "16#8C42 (changing the JobID in ProcessingMode 3 during runtime is not supported)",
)
_GAP_CYCLIC = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK ignores bit 0 (CallSubprogram data) of the telegram numbers "
    "(04_Network.cpp splitTelegramNoSC/CS: receive/sendCallSubprogram = false, optional cyclic data "
    "'not finished yet'); with the optional cyclic subprogram data the RI drops to NOT_INITIALIZED "
    "('Invalid sequence payload length'). Spec 5.5.4 optional cyclic data, 6.5.19 / 6.5.20",
)


@pytest.fixture(autouse=True)
def _subprogram(sdk: SdkSimulator) -> None:
    sdk.set_subprogram_cycles(SUB_CYCLES)


def _call(h: RobotTaskHarness, job: int = 1, mode: tuple[int, int] = PARALLEL, **inputs: Any) -> Any:
    """CallSubprogram with JobID ``job`` and (ProcessingMode, SequenceFlag) ``mode``."""
    cs = fb(h, "MC_CallSubprogramFB", ProcessingMode=mode[0], SequenceFlag=mode[1], **inputs)
    cs.ParCmd.JobID = job
    return cs


def _stop(
    h: RobotTaskHarness, target: int, stop_mode: int = StopMode.STOP_JOB_ID, mode: tuple[int, int] = PARALLEL
) -> Any:
    st = fb(h, "MC_StopSubprogramFB", ProcessingMode=mode[0], SequenceFlag=mode[1])
    st.ParCmd.TargetID = target
    st.ParCmd.StopMode = stop_mode
    return st


def _flags(block: Any) -> dict[str, Any]:
    out = {**state(block), "InfoID": hex(block.InfoID)}
    if hasattr(block, "InProgress"):
        out.update(InProgress=block.InProgress, Progress=block.OutCmd.Progress)
    return out


def _running(h: RobotTaskHarness, cs: Any) -> None:
    """Run until the call reports InProgress (asserted)."""
    h.run(20, until=lambda: bool(cs.InProgress or cs.Error))
    assert cs.InProgress and cs.Busy and not cs.Error, _flags(cs)


def _ended(cs: Any) -> bool:
    return bool(cs.Done or cs.Error or cs.CommandAborted)


def _all_outputs_reset(cs: Any) -> bool:
    flags = (
        "Busy",
        "Done",
        "Error",
        "Valid",
        "InProgress",
        "CommandBuffered",
        "CommandAborted",
        "CommandInterrupted",
        "ParameterAccepted",
    )
    return not any(getattr(cs, f) for f in flags) and cs.ErrorID == 0


# ---------------------------------------------------------------- run to Done


@pytest.mark.parametrize(
    ("mode", "powered"),
    [(PRIMARY, True), (PARALLEL, True), (PARALLEL, False)],
    ids=["primary-sequence", "parallel", "parallel-without-power"],
)
def test_call_runs_to_done(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: tuple[int, int], powered: bool
) -> None:
    """A valid CallSubprogram runs with Valid / InProgress and ends with Done; Execute FALSE resets all outputs.

    Primary sequence and parallel buffer with the robot enabled; parallel buffer also without power
    (a parallel subprogram needs no power). The sequence case without power is a separate test.
    """
    if powered:
        enable(robot)
    cs = _call(robot, mode=mode, Execute=True)
    in_progress = []
    seen = watch(robot, [cs], SUB_CYCLES + 50, lambda: in_progress.append(cs.InProgress) or _ended(cs))[0]
    assert cs.Done and not cs.Error and not cs.CommandAborted, _flags(cs)
    assert order(seen, "Busy", "Valid", "Done"), seen.flags
    assert any(in_progress) and not cs.InProgress and cs.OutCmd.Progress == 100, _flags(cs)
    assert sdk.last_command(CALL_SUBPROGRAM)["JobID"] == "1"
    cs.Execute = False
    robot.run(2)
    assert _all_outputs_reset(cs), _flags(cs)


def test_call_execute_pulse_still_reports_done(robot: RobotTaskHarness) -> None:
    """Execute TRUE for a single cycle starts the subprogram anyway, Done is shown for one cycle at the end."""
    enable(robot)
    cs = _call(robot, mode=PRIMARY, Execute=True)
    robot.run(1)
    cs.Execute = False
    done_cycles = 0
    for _ in range(SUB_CYCLES + 50):
        robot.run(1)
        done_cycles += bool(cs.Done)
        if done_cycles and not cs.Done:
            break
    assert done_cycles == 1 and not cs.Error, _flags(cs)
    assert _all_outputs_reset(cs), _flags(cs)


@_GAP_BUFFERED
def test_call_reports_command_buffered(robot: RobotTaskHarness) -> None:
    """CallSubprogram reports CommandBuffered (RC confirmed the command) before the subprogram is in progress."""
    cs = _call(robot)
    seen = execute(robot, cs, cycles=SUB_CYCLES + 50)
    assert order(seen, "Busy", "CommandBuffered", "Valid", "Done"), seen.flags


@_BUG_PARAMETER_ACCEPTED
def test_call_reports_parameter_accepted(robot: RobotTaskHarness) -> None:
    """CallSubprogram sets ParameterAccepted once the RC acknowledged the parameters of the running call."""
    cs = _call(robot, mode=CONTINUOUS, Execute=True)
    _running(robot, cs)
    robot.run(5)
    assert cs.ParameterAccepted, _flags(cs)


@_BUG_INSTANCE_ID
def test_call_instance_ids_are_unique(robot: RobotTaskHarness) -> None:
    """Two calls running at the same time report two different, non-zero InstanceIDs."""
    first = _call(robot, job=1, mode=CONTINUOUS, Execute=True)
    second = _call(robot, job=2, mode=CONTINUOUS, Execute=True)
    _running(robot, first)
    _running(robot, second)
    ids = (first.OutCmd.InstanceID, second.OutCmd.InstanceID)
    assert 0 not in ids and ids[0] != ids[1], ids


def test_call_job_id_unknown_to_rc_is_an_error(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A JobID without program on the RC ends with Error ERR_JOBID_NOT_EXIST, Done / InProgress stay FALSE.

    Stimulus: the simulator answers CallSubprogram with 16#8C37 (it has no list of programs).
    """
    sdk.set_command_error(CALL_SUBPROGRAM, E.ERR_JOBID_NOT_EXIST)
    cs = _call(robot, job=999)
    seen = execute(robot, cs, cycles=50)
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_JOBID_NOT_EXIST, seen.final
    assert "Done" not in seen.flags and "Valid" not in seen.flags, seen.flags
    assert _all_outputs_reset(cs), _flags(cs)


def test_call_reexecuted_with_same_job_while_running(robot: RobotTaskHarness) -> None:
    """Execute FALSE and TRUE again with the same JobID while the call runs: the block keeps showing that call.

    No error; the call runs on and ends with Done.
    """
    cs = _call(robot, Execute=True)
    _running(robot, cs)
    cs.Execute = False
    robot.run(1)
    cs.Execute = True
    robot.run(2)
    assert cs.Busy and cs.InProgress and not cs.Error, _flags(cs)
    robot.run(SUB_CYCLES + 20, until=lambda: _ended(cs))
    assert cs.Done and not cs.Error, _flags(cs)


# ---------------------------------------------------------------- power, interrupt, sequences


@pytest.mark.parametrize("block", ["call", "stop"])
def test_sequence_command_without_power_is_interrupted(robot: RobotTaskHarness, block: str) -> None:
    """A sequence command (CallSubprogram / StopSubprogram) without power stays Busy with CommandInterrupted.

    InfoID INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, no Done, no Error.
    """
    cmd = _call(robot, mode=PRIMARY) if block == "call" else _stop(robot, 3, mode=PRIMARY)
    seen = execute(robot, cmd, cycles=60, reset=False)
    assert order(seen, "Busy", "CommandInterrupted"), seen.flags
    assert cmd.Busy and not cmd.Done and not cmd.Error, _flags(cmd)
    assert cmd.InfoID == I.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, _flags(cmd)


def test_power_off_interrupts_sequence_call(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Disabling the robot while a sequence call runs: CommandInterrupted, InProgress FALSE, Progress kept."""
    en = enable(robot)
    cs = _call(robot, mode=PRIMARY, Execute=True)
    _running(robot, cs)
    robot.run(5)
    en.Enable = False
    robot.run(30, until=lambda: bool(cs.CommandInterrupted or _ended(cs)))
    assert not sdk.enabled
    assert cs.CommandInterrupted and cs.Busy and not cs.InProgress and not cs.Error, _flags(cs)
    assert 0 < cs.OutCmd.Progress < 100 and cs.InfoID == I.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, _flags(cs)


@_GAP_RC_ERROR
def test_rc_error_interrupts_sequence_call(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """An error of the RC inside a running sequence subprogram interrupts it: CommandInterrupted, no Done."""
    enable(robot)
    cs = _call(robot, job=5, mode=PRIMARY, Execute=True)
    _running(robot, cs)
    sdk.set_motion_error(0x6C02)
    robot.run(SUB_CYCLES + 10, until=lambda: bool(cs.CommandInterrupted or _ended(cs)))
    assert cs.CommandInterrupted and not cs.Done, _flags(cs)


def test_primary_call_waits_while_secondary_sequence_active(robot: RobotTaskHarness) -> None:
    """With the secondary sequence active a primary call waits, a secondary call runs to Done.

    Back in the primary sequence the primary call is interrupted until GroupContinue, then it runs to Done.
    """
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SF.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    primary = _call(robot, job=1, mode=PRIMARY, Execute=True)
    secondary = _call(robot, job=2, mode=(PM.BUFFERED, SF.SECONDARY_SEQUENCE), Execute=True)
    robot.run(SUB_CYCLES + 30, until=lambda: _ended(secondary))
    assert secondary.Done and not secondary.Error, _flags(secondary)
    assert primary.Busy and not primary.InProgress and not _ended(primary), _flags(primary)
    back = fb(robot, "MC_SetSequenceFB")
    back.ParCmd.TargetSequence = SF.PRIMARY_SEQUENCE
    assert execute(robot, back).final["Done"]
    robot.run(10)
    assert primary.Busy and not _ended(primary), _flags(primary)
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    robot.run(SUB_CYCLES + 30, until=lambda: _ended(primary))
    assert primary.Done and not primary.Error, _flags(primary)


# ---------------------------------------------------------------- continuous


def test_continuous_call_takes_new_data(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """New Data while a CONTINUOUS call runs: Valid drops and comes back, the RC gets the new data, it runs on."""
    cs = _call(robot, mode=CONTINUOUS, Execute=True)
    _running(robot, cs)
    robot.run(3)
    assert cs.Valid
    cs.ParCmd.Data[0] = 7
    valid = []
    for _ in range(10):
        robot.run(1)
        valid.append(cs.Valid)
    assert False in valid and valid[-1], valid
    assert sdk.last_command(CALL_SUBPROGRAM)["Data[0]"] == "7"
    assert cs.Busy and cs.InProgress and not cs.Error and not cs.Done, _flags(cs)


@_GAP_JOB_CHANGE
def test_continuous_call_rejects_job_change(robot: RobotTaskHarness) -> None:
    """A new JobID while a CONTINUOUS call runs is rejected by the RC with ERR_JOBID_CHANGE_PM3_NOT_ALLOWED."""
    cs = _call(robot, mode=CONTINUOUS, Execute=True)
    _running(robot, cs)
    cs.ParCmd.JobID = 3
    robot.run(10, until=lambda: _ended(cs))
    assert cs.Error and cs.ErrorID == E.ERR_JOBID_CHANGE_PM3_NOT_ALLOWED, _flags(cs)


def test_continuous_call_with_execute_pulse_and_deactivate(robot: RobotTaskHarness) -> None:
    """A CONTINUOUS call started with a one-cycle Execute pulse runs on; DEACTIVATE + new edge ends it with Done."""
    cs = _call(robot, job=0, mode=CONTINUOUS, Execute=True)
    robot.run(1)
    cs.Execute = False
    robot.run(2 * SUB_CYCLES)
    assert cs.Busy and cs.InProgress and not _ended(cs), _flags(cs)
    cs.ProcessingMode = PM.DEACTIVATE
    cs.Execute = True
    robot.run(20, until=lambda: _ended(cs))
    assert cs.Done and not cs.Error and not cs.InProgress, _flags(cs)


def test_trigger_continuous_call_waits_for_its_trigger(robot: RobotTaskHarness) -> None:
    """TRIGGER_CONTINUOUS with ListenerID > 0 and no trigger: buffered, no error, no Done, InvocationCounter 0."""
    cs = _call(robot, mode=(PM.TRIGGER_CONTINUOUS, SF.NO_SEQUENCE))
    cs.ParCmd.ListenerID = 5
    seen = execute(robot, cs, cycles=60, reset=False)
    assert order(seen, "Busy", "CommandBuffered"), seen.flags
    assert cs.Busy and not cs.Done and not cs.Error, _flags(cs)
    assert cs.OutCmd.InvocationCounter == 0


# ---------------------------------------------------------------- StopSubprogram


@pytest.mark.parametrize(
    ("call_mode", "stop_mode"),
    [
        (PARALLEL, PRIMARY),
        (PRIMARY, PRIMARY_ABORTING),
        (PRIMARY, PARALLEL),
        (PARALLEL, PARALLEL),
        (CONTINUOUS, PARALLEL),
    ],
    ids=[
        "call-parallel-stop-sequence",
        "call-sequence-stop-aborting",
        "call-sequence-stop-parallel",
        "call-parallel-stop-parallel",
        "call-continuous-stop-parallel",
    ],
)
def test_stop_by_job_aborts_running_call(
    robot: RobotTaskHarness, call_mode: tuple[int, int], stop_mode: tuple[int, int]
) -> None:
    """StopSubprogram with the JobID of the running call ends with Done, the call with CommandAborted."""
    enable(robot)
    cs = _call(robot, job=1, mode=call_mode, Execute=True)
    _running(robot, cs)
    st = _stop(robot, 1, mode=stop_mode)
    seen = execute(robot, st, cycles=60)
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    robot.run(20, until=lambda: _ended(cs))
    assert cs.CommandAborted and not cs.Done and not cs.Busy and not cs.InProgress, _flags(cs)
    cs.Execute = False
    robot.run(2)
    assert _all_outputs_reset(cs), _flags(cs)


def test_stop_by_job_aborts_every_instance_of_the_job(robot: RobotTaskHarness) -> None:
    """Two CONTINUOUS calls with the same JobID: StopSubprogram via that JobID aborts both."""
    first = _call(robot, job=1, mode=CONTINUOUS, Execute=True)
    second = _call(robot, job=1, mode=CONTINUOUS, Execute=True)
    _running(robot, first)
    _running(robot, second)
    seen = execute(robot, _stop(robot, 1))
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    robot.run(10, until=lambda: _ended(first) and _ended(second))
    assert first.CommandAborted and second.CommandAborted, (_flags(first), _flags(second))


def test_stop_all_subprograms(robot: RobotTaskHarness) -> None:
    """StopMode STOP_ALL_SUBPROGRAMS with TargetID -1 aborts every running call."""
    first = _call(robot, job=0, mode=CONTINUOUS, Execute=True)
    second = _call(robot, job=1, mode=CONTINUOUS, Execute=True)
    _running(robot, first)
    _running(robot, second)
    seen = execute(robot, _stop(robot, -1, StopMode.STOP_ALL_SUBPROGRAMS))
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    robot.run(10, until=lambda: _ended(first) and _ended(second))
    assert first.CommandAborted and second.CommandAborted, (_flags(first), _flags(second))


@_BUG_INSTANCE_ID
def test_stop_by_instance_id(robot: RobotTaskHarness) -> None:
    """StopMode STOP_INSTANCE_ID with the InstanceID of the first call aborts only that call."""
    first = _call(robot, job=0, mode=CONTINUOUS, Execute=True)
    second = _call(robot, job=1, mode=CONTINUOUS, Execute=True)
    _running(robot, first)
    _running(robot, second)
    st = _stop(robot, first.OutCmd.InstanceID, StopMode.STOP_INSTANCE_ID)
    seen = execute(robot, st, reset=False)
    assert seen.final["Done"] and st.InfoID == 0, _flags(st)
    robot.run(10, until=lambda: _ended(first))
    assert first.CommandAborted and second.InProgress and not _ended(second), (_flags(first), _flags(second))


def test_stop_buffered_call_that_has_not_started(robot: RobotTaskHarness) -> None:
    """Two calls in the primary sequence; stopping the JobID of the second (still buffered) aborts it, the first ends Done."""
    enable(robot)
    first = _call(robot, job=0, mode=PRIMARY, Execute=True)
    second = _call(robot, job=1, mode=PRIMARY, Execute=True)
    _running(robot, first)
    assert second.Busy and not second.InProgress, _flags(second)
    seen = execute(robot, _stop(robot, 1))
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    robot.run(SUB_CYCLES + 30, until=lambda: _ended(first) and _ended(second))
    assert first.Done and not first.CommandAborted, _flags(first)
    assert second.CommandAborted and not second.Done, _flags(second)


@pytest.mark.parametrize(
    ("target", "stop_mode", "info"),
    [
        (99, StopMode.STOP_JOB_ID, I.INFO_JOBID_NOT_RUNNING),
        (-1, StopMode.STOP_ALL_SUBPROGRAMS, I.INFO_NO_ACTIVE_SUBPROGRAM),
    ],
    ids=["job-not-running", "all-none-active"],
)
@pytest.mark.parametrize("mode", [PARALLEL, PRIMARY], ids=["parallel", "sequence"])
def test_stop_without_matching_subprogram_reports_info(
    robot: RobotTaskHarness, target: int, stop_mode: int, info: int, mode: tuple[int, int]
) -> None:
    """StopSubprogram when nothing matches ends with Done, no Error, and the InfoID of table 7-1."""
    enable(robot)
    st = _stop(robot, target, stop_mode, mode=mode)
    seen = execute(robot, st, reset=False)
    assert seen.final["Done"] and not seen.final["Error"], _flags(st)
    assert st.InfoID == info, _flags(st)
    st.Execute = False
    robot.run(2)
    assert not st.Done and not st.Busy and st.InfoID == 0, _flags(st)


def test_stop_all_with_target_id_is_rejected_by_rc(robot: RobotTaskHarness) -> None:
    """StopMode STOP_ALL_SUBPROGRAMS with a TargetID other than -1: Error ERR_STOP_MODE_2_TARGETID_NEG1."""
    seen = execute(robot, _stop(robot, 3, StopMode.STOP_ALL_SUBPROGRAMS))
    assert seen.final["Error"] and seen.final["ErrorID"] == E.ERR_STOP_MODE_2_TARGETID_NEG1, seen.final
    assert "Done" not in seen.flags


def test_buffered_stop_runs_after_continue(robot: RobotTaskHarness) -> None:
    """A sequence StopSubprogram waits while the sequence is interrupted; after GroupContinue it aborts the call.

    The StopSubprogram shows CommandInterrupted meanwhile, a CONTINUOUS call started in parallel runs.
    """
    enable(robot)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    st = _stop(robot, 0, mode=PRIMARY)
    st.Execute = True
    robot.run(10)
    assert st.CommandInterrupted and st.Busy and not st.Done, _flags(st)
    cs = _call(robot, job=0, mode=CONTINUOUS, Execute=True)
    _running(robot, cs)
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    robot.run(20, until=lambda: bool(st.Done and _ended(cs)))
    assert st.Done and not st.Error and not st.CommandInterrupted, _flags(st)
    assert cs.CommandAborted, _flags(cs)


def test_buffered_stop_aborted_by_group_stop(robot: RobotTaskHarness) -> None:
    """A sequence StopSubprogram waiting in the interrupted sequence ends with CommandAborted on GroupStop."""
    enable(robot)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    st = _stop(robot, 3, mode=PRIMARY)
    st.Execute = True
    robot.run(10)
    assert st.CommandInterrupted and st.Busy, _flags(st)
    assert execute(robot, fb(robot, "MC_GroupStopFB")).final["Done"]
    robot.run(10, until=lambda: _ended(st))
    assert st.CommandAborted and not st.Done and not st.Error, _flags(st)


# ---------------------------------------------------------------- cyclic subprogram data


@_GAP_CYCLIC
def test_cyclic_subprogram_data_round_trip(sdk: SdkSimulator) -> None:
    """With the optional cyclic subprogram data both cyclic blocks are enabled and exchange 26 bytes with a running call.

    Setup: RobotTask with UseCallSubprogram in both directions (256-byte telegrams). The RC side is
    expected to receive the written bytes and to send its own bytes back.
    """
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, 256, 256), advance=clock.advance, size=256)
        h.cfg.Plc.OptionalCyclic.UseCallSubprogram = True
        h.cfg.Rob.OptionalCyclic.UseCallSubprogram = True
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, h.history
        wr = fb(h, "MC_WriteCallSubprogramCyclicFB", Enable=True)
        for i in range(26):
            wr.ParCmd.Data[i] = i + 1
        rd = fb(h, "MC_ReadCallSubprogramCyclicFB", Enable=True)
        cs = _call(h, mode=CONTINUOUS, Execute=True)
        h.run(30, until=lambda: bool(wr.Enabled and rd.Enabled and cs.InProgress))
        assert wr.Enabled and rd.Enabled and not wr.Error and not rd.Error, (state(wr), state(rd))
        assert cs.InProgress, _flags(cs)
        assert any(rd.OutCmd.Data), list(rd.OutCmd.Data)
