# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_val_processing_mode
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    ProcessingMode / SequenceFlag of the blocks without a reference test
#    set (VAL-PM): allowed values, sequence, parallel buffer, continuous and
#    trigger execution.
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

"""ProcessingMode / SequenceFlag of the blocks without a reference test set (area VAL-PM).

The reference test sets of ReadActualPosition, CallSubprogram, the Write...Data blocks etc. check
how a block with a ``ProcessingMode`` input behaves in every mode it allows: buffered in the
sequence (waits for the motion, interrupted without power), aborting, parallel (next to a motion,
without power), continuous and triggered (Trigger Once / Multiple, Deactivate), and that a
mode or SequenceFlag that does not fit is rejected by the client without sending the command.
The same is checked here for every other block with ``ProcessingMode`` (I/O, registers, system
variables, force / velocity reads, collision detection, load measurement, trigger functions).

The allowed modes of each block come from the command value tables of the specification
(``tools/spec_tables/spec_parameter_values.json``, see VAL-PAR). The telegram coding
(ExecutionMode) of every mode is MET PM-03.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import (
    ProcessingMode,
    RobotLibraryErrorIdEnum,
    RobotLibraryInfoIdEnum,
    SequenceFlag,
    TriggerCondition,
)
from tests.bilateral import distinct_values
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import move_axes
from tests.sdk.test_methodology import (
    CLASSES,
    CLASSES_ALL,
    FB_INPUTS,
    PARCMD_INPUTS,
    cmd_type,
    commands,
    outputs,
    robot,
)
from tests.sdk.trigger_pump import NOT_USER_TRIGGERED, attach_listener_trigger
from tests.sdk.validation.test_val_parameters import REFERENCE
from tools.spec_tables.values import load

# needs a motion to superimpose: tested with a motion in VAL-EFF
PRECONDITION = {"MC_MoveSuperImposedFB"}
_SPEC = load()


def _spec_values(name: str, parameter: str) -> list[int]:
    rows = [r for r in _SPEC.get(name[3:-2], []) if r["name"] == parameter]
    return [int(v) for v in rows[0]["values"]] if rows else []


def _allowed(name: str) -> list[int]:
    return _spec_values(name, "ProcessingMode")


NAMES = sorted(
    n
    for n, c in CLASSES.items()
    if hasattr(c(), "ProcessingMode")
    and not hasattr(c(), "AbortingMode")
    and n[3:-2] not in REFERENCE
    and n not in PRECONDITION
    and _allowed(n)
)
SEQUENCE = {
    ProcessingMode.BUFFERED,
    ProcessingMode.ABORTING,
    ProcessingMode.TRIGGER_BUFFERED,
    ProcessingMode.TRIGGER_ABORTING,
}
# modes of an "Action": executed when the trigger function with EmitterID = ListenerID fires
TRIGGERED = {
    ProcessingMode.TRIGGER_BUFFERED,
    ProcessingMode.TRIGGER_ABORTING,
    ProcessingMode.TRIGGER_ONCE,
    ProcessingMode.TRIGGER_CONTINUOUS,
    ProcessingMode.TRIGGER_MULTIPLE,
}
# ActivateNextCommand ends the active motion of the sequence: that is its function (VAL-EFF)
ENDS_THE_MOTION = {"MC_ActivateNextCommandFB"}
_TCP_VELOCITY = (
    "SPEC: the command values of ReadActualTCPVelocity (table 6-59) list the trigger modes and ListenerID, "
    "the CMD payload (table 6-63) has no EmitterID / ListenerID: the library follows the payload, the RC "
    "executes the command at once (see the notes on the specification of ST_FINDINGS)"
)
KNOWN: dict[tuple[str, str], str] = {
    ("once", "MC_ReadActualTCPVelocityFB"): _TCP_VELOCITY,
    ("multiple", "MC_ReadActualTCPVelocityFB"): _TCP_VELOCITY,
}
CYCLES = 60
MOVE_CYCLES = 100


def _params(test: str, names: list[str]) -> list[Any]:
    return [
        pytest.param(n, marks=pytest.mark.xfail(strict=True, reason=KNOWN[(test, n)]))
        if (test, n) in KNOWN
        else pytest.param(n)
        for n in names
    ]


def _with(mode: ProcessingMode) -> list[str]:
    return [n for n in NAMES if int(mode) in _allowed(n)]


def _fitting_flag(mode: ProcessingMode) -> SequenceFlag:
    return SequenceFlag.PRIMARY_SEQUENCE if mode in SEQUENCE else SequenceFlag.NO_SEQUENCE


def _block(
    name: str,
    h: RobotTaskHarness,
    mode: ProcessingMode,
    flag: SequenceFlag | None = None,
    pump: bool = True,
) -> Any:
    """Block ``name`` with distinct parameter values, ``mode`` and the SequenceFlag that fits it;
    ListenerID 1 for the triggered modes (``pump``: a user trigger is emitted while it waits)."""
    fb = CLASSES[name]()
    for key, value in FB_INPUTS.get(name, {}).items():
        setattr(fb, key, list(value) if isinstance(value, list) else value)
    distinct_values(fb.ParCmd)
    for key, value in PARCMD_INPUTS.get(name, {}).items():
        setattr(fb.ParCmd, key, value)
    if hasattr(fb.ParCmd, "ListenerID"):
        fb.ParCmd.ListenerID = 1 if mode in TRIGGERED else 0
    if isinstance(getattr(fb.ParCmd, "EmitterID", None), list):
        fb.ParCmd.EmitterID[0] = 2  # trigger functions: EmitterID must not be 0 (2: no listener here)
    elif hasattr(fb.ParCmd, "EmitterID"):
        fb.ParCmd.EmitterID = 2
    _consistent(name, fb.ParCmd)
    fb.ProcessingMode = mode
    if hasattr(fb, "SequenceFlag"):
        fb.SequenceFlag = _fitting_flag(mode) if flag is None else flag
    h.add(fb)
    if pump:
        attach_listener_trigger(h, fb, name)
    return fb


def _consistent(name: str, par: Any) -> None:
    """Parameters the RC checks against each other (the distinct values do not fit)."""
    if name == "MC_SetTriggerLimitFB":  # Data_1 >= Data_2
        par.Data_1, par.Data_2 = par.Data_2, par.Data_1
    elif name == "MC_SetTriggerMotionFB":  # distance from the start point (the SDK has no TCP velocity)
        par.TriggerMode_1 = par.TriggerMode_2 = TriggerCondition.START_POSITION_DISTANCE_PERCENT


def _ended(fb: Any) -> bool:
    return bool(fb.Done or fb.Error or getattr(fb, "CommandInterrupted", False))


def _motion(h: RobotTaskHarness) -> Any:
    """MoveAxesAbsolute that is Active (the robot moves for MOVE_CYCLES cycles)."""
    mv = move_axes(h, 50.0)
    mv.Execute = True
    h.run(100, until=lambda: bool(mv.Active or mv.Error))
    assert mv.Active, outputs(mv)
    return mv


def _sent(sim: SdkSimulator, name: str, start_log: int) -> int:
    return commands(sim, cmd_type(name), start_log)


# ------------------------------------------------------------------ allowed values


def _not_allowed() -> list[Any]:
    cases = [(n, m) for n in NAMES for m in ProcessingMode if int(m) not in _allowed(n)]
    return [
        pytest.param(n, m, marks=pytest.mark.xfail(strict=True, reason=KNOWN[("not-allowed", n)]))
        if ("not-allowed", n) in KNOWN
        else pytest.param(n, m)
        for n, m in cases
    ]


@pytest.mark.parametrize(("name", "mode"), _not_allowed())
def test_processing_mode_not_allowed_is_rejected(name: str, mode: ProcessingMode) -> None:
    """A ProcessingMode the specification does not list for the block: Error
    ERR_PROCESSINGMODE_NOT_ALLOWED, the command is not sent."""
    with robot() as (sim, h):
        start_log = len(sim.logs)
        fb = _block(name, h, mode, pump=False)
        fb.Execute = True
        h.run(20, until=lambda: bool(fb.Error))
        assert fb.Error and fb.ErrorID == RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED, outputs(fb)
        assert _sent(sim, name, start_log) == 0


def _allowed_cases() -> list[Any]:
    cases = [
        (n, m)
        for n in NAMES
        for m in ProcessingMode
        if int(m) in _allowed(n) and m != ProcessingMode.DEACTIVATE
    ]
    return [
        pytest.param(n, m, marks=pytest.mark.xfail(strict=True, reason=KNOWN[("allowed", f"{n}:{m.name}")]))
        if ("allowed", f"{n}:{m.name}") in KNOWN
        else pytest.param(n, m)
        for n, m in cases
    ]


@pytest.mark.parametrize(("name", "mode"), _allowed_cases())
def test_processing_mode_allowed_is_executed(name: str, mode: ProcessingMode) -> None:
    """Every ProcessingMode the specification lists (except Deactivate) with the SequenceFlag that
    fits it: the command is sent and the RC accepts it, no error."""
    with robot() as (sim, h):
        start_log = len(sim.logs)
        fb = _block(name, h, mode)
        fb.Execute = True
        h.run(CYCLES, until=lambda: bool(fb.Error or fb.Done))
        assert not fb.Error, outputs(fb)
        assert _sent(sim, name, start_log) == 1


def _sequence_cases() -> list[Any]:
    cases = []
    for n in NAMES:
        if not hasattr(CLASSES[n](), "SequenceFlag"):
            continue
        for m in ProcessingMode:
            if int(m) in _allowed(n) and m != ProcessingMode.DEACTIVATE:
                cases.append((n, m))
    return [
        pytest.param(n, m, marks=pytest.mark.xfail(strict=True, reason=KNOWN[("flag", n)]))
        if ("flag", n) in KNOWN
        else pytest.param(n, m)
        for n, m in cases
    ]


@pytest.mark.parametrize(("name", "mode"), _sequence_cases())
def test_sequence_flag_that_does_not_fit_is_rejected(name: str, mode: ProcessingMode) -> None:
    """Spec 5.5.3.4: a mode in the sequence with "No sequence", or a mode outside the sequence with
    primary sequence, is detected by the client: Error ERR_SEQFLAG_INVALID_IN_PROC_MODE (or
    ERR_SEQFLAG_NOT_ALLOWED when the block does not allow the flag at all), not sent."""
    wrong = SequenceFlag.NO_SEQUENCE if mode in SEQUENCE else SequenceFlag.PRIMARY_SEQUENCE
    # "No sequence" belongs to the modes outside the sequence even where a table omits it
    # (CollisionDetection lists only 1, 2 but allows Parallel)
    flags = _spec_values(name, "SequenceFlag")
    if any(
        m not in SEQUENCE | {ProcessingMode.DEACTIVATE} and int(m) in _allowed(name) for m in ProcessingMode
    ):
        flags.append(int(SequenceFlag.NO_SEQUENCE))
    expected = (
        RobotLibraryErrorIdEnum.ERR_SEQFLAG_INVALID_IN_PROC_MODE
        if int(wrong) in flags
        else RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED
    )
    with robot() as (sim, h):
        start_log = len(sim.logs)
        fb = _block(name, h, mode, wrong, pump=False)
        fb.Execute = True
        h.run(20, until=lambda: bool(fb.Error))
        assert fb.Error and fb.ErrorID == expected, outputs(fb)
        assert _sent(sim, name, start_log) == 0


# ------------------------------------------------------------------ sequence / parallel buffer


@pytest.mark.parametrize("name", _params("parallel-off", _with(ProcessingMode.PARALLEL)))
def test_parallel_without_power(name: str) -> None:
    """Parallel: executed while the robot is not enabled (parallel buffer): Done without error."""
    with robot(enable_robot=False) as (_, h):
        fb = _block(name, h, ProcessingMode.PARALLEL)
        fb.Execute = True
        h.run(CYCLES, until=lambda: _ended(fb))
        assert fb.Done and not fb.Error, outputs(fb)


def _sequence_blocks() -> list[str]:
    return [n for n in _with(ProcessingMode.BUFFERED) if hasattr(CLASSES[n](), "SequenceFlag")]


@pytest.mark.parametrize("name", _params("buffered-off", _sequence_blocks()))
def test_buffered_without_power_is_interrupted(name: str) -> None:
    """Buffered in the primary sequence while the robot is not enabled: CommandInterrupted with
    INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, Busy, no Done, no error."""
    with robot(enable_robot=False) as (_, h):
        fb = _block(name, h, ProcessingMode.BUFFERED)
        fb.Execute = True
        h.run(CYCLES, until=lambda: _ended(fb))
        assert fb.CommandInterrupted and fb.Busy and not (fb.Done or fb.Error), outputs(fb)
        assert fb.InfoID == RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, hex(fb.InfoID)


@pytest.mark.parametrize("name", _params("buffered", _with(ProcessingMode.BUFFERED)))
def test_buffered_waits_for_the_motion(name: str) -> None:
    """Buffered behind an active motion: CommandBuffered and Busy while the robot moves, Done only
    after the motion is Done."""
    with robot() as (sim, h):
        sim.set_move_cycles(MOVE_CYCLES)
        mv = _motion(h)
        fb = _block(name, h, ProcessingMode.BUFFERED)
        fb.Execute = True
        h.run(20)
        assert fb.Busy and fb.CommandBuffered and not (fb.Done or fb.Error), outputs(fb)
        h.run(4 * MOVE_CYCLES, until=lambda: bool(fb.Done or fb.Error))
        assert fb.Done and not fb.Error and mv.Done, (outputs(fb), outputs(mv))


@pytest.mark.parametrize("name", _params("aborting", _with(ProcessingMode.ABORTING)))
def test_aborting_aborts_the_motion(name: str) -> None:
    """Aborting during an active motion: the motion is CommandAborted, the block is Done."""
    with robot() as (sim, h):
        sim.set_move_cycles(MOVE_CYCLES)
        mv = _motion(h)
        fb = _block(name, h, ProcessingMode.ABORTING)
        fb.Execute = True
        h.run(MOVE_CYCLES, until=lambda: bool(fb.Done or fb.Error))
        assert fb.Done and not fb.Error, outputs(fb)
        assert mv.CommandAborted and not mv.Done, outputs(mv)


@pytest.mark.parametrize(
    "name", _params("parallel", [n for n in _with(ProcessingMode.PARALLEL) if n not in ENDS_THE_MOTION])
)
def test_parallel_runs_next_to_the_motion(name: str) -> None:
    """Parallel during an active motion: Done while the motion is still Active; the motion goes on."""
    with robot() as (sim, h):
        sim.set_move_cycles(MOVE_CYCLES)
        mv = _motion(h)
        fb = _block(name, h, ProcessingMode.PARALLEL)
        fb.Execute = True
        h.run(MOVE_CYCLES, until=lambda: bool(fb.Done or fb.Error or mv.Done))
        assert fb.Done and not fb.Error, outputs(fb)
        assert mv.Active and not mv.Done, outputs(mv)
        h.run(4 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done, outputs(mv)


# ------------------------------------------------------------------ continuous / triggered


def _deactivate(h: RobotTaskHarness, fb: Any) -> None:
    """New rising edge with ProcessingMode Deactivate on the same instance: Done, Busy FALSE."""
    fb.Execute = False
    h.run(2)
    fb.ProcessingMode = ProcessingMode.DEACTIVATE
    fb.Execute = True
    h.run(CYCLES, until=lambda: bool(fb.Done or fb.Error))
    assert fb.Done and not fb.Busy and not fb.Error, outputs(fb)


@pytest.mark.parametrize("name", _params("continuous", _with(ProcessingMode.CONTINUOUS)))
def test_continuous_runs_until_deactivated(name: str) -> None:
    """Continuous: Busy (a read block also Valid), no Done, also after Execute FALSE; Deactivate ends it."""
    with robot() as (_, h):
        fb = _block(name, h, ProcessingMode.CONTINUOUS)
        fb.Execute = True
        h.run(CYCLES, until=lambda: bool(fb.Error or getattr(fb, "Valid", False)))
        h.run(10)
        assert fb.Busy and not (fb.Done or fb.Error), outputs(fb)
        assert getattr(fb, "Valid", True), outputs(fb)
        fb.Execute = False
        h.run(10)
        assert fb.Busy and not (fb.Done or fb.Error), outputs(fb)
        _deactivate(h, fb)


def _trigger(h: RobotTaskHarness) -> Any:
    user = CLASSES_ALL["MC_SetTriggerUserFB"]()
    user.ParCmd.EmitterID = 1
    user.ProcessingMode = ProcessingMode.TRIGGER_ONCE
    return h.add(user)


def _emit(h: RobotTaskHarness, user: Any) -> None:
    user.Execute = True
    h.run(CYCLES, until=lambda: bool(user.Done or user.Error))
    assert user.Done and not user.Error, outputs(user)
    user.Execute = False
    h.run(2)


def _listeners(mode: ProcessingMode) -> list[str]:
    return [
        n for n in _with(mode) if hasattr(CLASSES[n]().ParCmd, "ListenerID") and n not in NOT_USER_TRIGGERED
    ]


def _trigger_function(name: str) -> bool:
    """A trigger function is activated by the trigger and then monitors its own condition (no Done)."""
    return name.startswith("MC_SetTrigger")


@pytest.mark.parametrize("name", _params("once", _listeners(ProcessingMode.TRIGGER_ONCE)))
def test_trigger_once_waits_for_the_trigger(name: str) -> None:
    """Trigger Once with ListenerID 1: Busy and CommandBuffered without Done until the user trigger
    with EmitterID 1; then InvocationCounter 1 and Done (a trigger function stays Busy and monitors
    its condition)."""
    with robot() as (_, h):
        fb = _block(name, h, ProcessingMode.TRIGGER_ONCE, pump=False)
        fb.Execute = True
        h.run(20)
        assert fb.Busy and fb.CommandBuffered and not (fb.Done or fb.Error), outputs(fb)
        _emit(h, _trigger(h))
        if _trigger_function(name):
            h.run(10)
            assert fb.Busy and not (fb.Done or fb.Error), outputs(fb)
        else:
            h.run(CYCLES, until=lambda: bool(fb.Done or fb.Error))
            assert fb.Done and not fb.Error, outputs(fb)
        if hasattr(fb.OutCmd, "InvocationCounter"):
            assert fb.OutCmd.InvocationCounter == 1


@pytest.mark.parametrize("name", _params("multiple", _listeners(ProcessingMode.TRIGGER_MULTIPLE)))
def test_trigger_multiple_until_deactivated(name: str) -> None:
    """Trigger Multiple with ListenerID 1: executed at every user trigger (InvocationCounter 1, 2; a
    trigger function is activated by the first one), Busy, no Done; Deactivate ends it."""
    with robot() as (_, h):
        fb = _block(name, h, ProcessingMode.TRIGGER_MULTIPLE, pump=False)
        fb.Execute = True
        h.run(20)
        assert fb.Busy and fb.CommandBuffered and not (fb.Done or fb.Error), outputs(fb)
        user = _trigger(h)
        for count in (1, 2):
            _emit(h, user)
            h.run(10)
            assert fb.Busy and not (fb.Done or fb.Error), outputs(fb)
            if hasattr(fb.OutCmd, "InvocationCounter"):
                # a trigger function is activated once and then monitors its condition
                expected = 1 if _trigger_function(name) else count
                assert fb.OutCmd.InvocationCounter == expected, outputs(fb)
        _deactivate(h, fb)
