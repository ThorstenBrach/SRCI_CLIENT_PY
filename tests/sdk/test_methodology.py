# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_methodology
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Methodology tests of every function block against the SRCI SDK.
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

"""Methodology tests of every function block against the SRCI SDK.

The test series of the Siemens test cases ("General FB", "ErrorID") applied to all function
blocks of the library (docs/TestCases.md):

* GEN-04 valid command not executed: all outputs FALSE / 0, nothing sent
* GEN-05 valid command with the default values, positive edge: Done / Enabled / Valid
* GEN-06 continuous Execute signal: executed once, Done stays TRUE until Execute is reset
* GEN-07 axes group not initialized (RobotTask not running): Error
* GEN-08 Execute for one cycle only: the command is executed, Done for at least one cycle
* GEN-09 undefined ExecMode ("AbortingMode = 18"): Error
* ERR-01 undefined value of an enum parameter: Error, command not executed
* ERR-02 error reported by the RC: Error with the ErrorID of the RC
* PM-01..03 buffered / aborting commands, SEQ-01 secondary sequence
* REP-01 the same instance executed repeatedly
* BUF-01 more commands in one cycle than the active command register holds, BUF-02 16 commands
  in one cycle

Known deviations are ``xfail`` with the finding of docs/ST_FINDINGS.md.
"""

from __future__ import annotations

import enum
import re
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.sim.sdk import SdkSimulator, find_sdk_library, sdk_transport
from srci.types import SequenceFlag
from tests.bilateral import distinct_values, leaves
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tools.payload_check import fb_classes, send_calls

SKIP = {
    "MC_RobotTaskFB": "the RobotTask itself (tests/sdk/test_robot_task.py)",
    "MC_ReadActualPositionCyclicFB": "cyclic data, no command",
    "MC_ReadCallSubprogramCyclicFB": "cyclic data, no command",
    "MC_WriteCallSubprogramCyclicFB": "cyclic data, no command",
}
SDK_NATIVE = {
    1000,
    1001,
    1004,
    2000,
    2001,
    2002,
    2003,
    2100,
    2101,
    2102,
    2103,
    2104,
    5100,
    5102,
    5103,
    5104,
    5105,
    5106,
    5107,
    5200,
    5201,
    5202,
    5203,
    5204,
    5205,
    9000,
    9001,
    9002,
}
FB_INPUTS: dict[str, dict[str, Any]] = {}  # ST-FIX F69: the defaults are valid (e.g. CollisionDetection)
# ParCmd values needed for a valid command: "Action" functions that can only be started by a
# trigger (ListenerID 0 = invalid, spec tables 6-622/6-628, ST-FIX F69)
PARCMD_INPUTS: dict[str, dict[str, Any]] = {
    name: {"ListenerID": 1}
    for name in ("MC_ReactAtTriggerFB", "MC_WaitForTriggerFB", "MC_RedefineTrackingPosFB")
}
CLASSES = {n: c for n, c in fb_classes() if hasattr(c, "CreateCommandPayload") and n not in SKIP}
NAMES = sorted(CLASSES)
EXECUTE = sorted(n for n in NAMES if hasattr(CLASSES[n](), "Execute"))


@pytest.fixture(autouse=True, scope="module")
def sdk_parameters() -> Iterator[None]:
    try:
        find_sdk_library()
    except Exception as exc:
        pytest.skip(str(exc))
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@contextmanager
def robot(initialized: bool = True) -> Iterator[tuple[SdkSimulator, RobotTaskHarness]]:
    """SDK + RobotTask; ``initialized``: commands enabled and the robot enabled."""
    from tests.sdk.test_core_fbs import enable

    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sim, SIZE, SIZE), advance=clock.advance)
        if initialized:
            h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
            enable(h, sim)
        else:
            h.enable = False
        yield sim, h


def block(name: str, h: RobotTaskHarness, values: bool = True) -> Any:
    fb = CLASSES[name]()
    for key, value in FB_INPUTS.get(name, {}).items():
        setattr(fb, key, value)
    if values:
        distinct_values(fb.ParCmd)
    for key, value in PARCMD_INPUTS.get(name, {}).items():
        setattr(fb.ParCmd, key, value)
    h.add(fb)
    return fb


def start(fb: Any, on: bool = True) -> None:
    if hasattr(fb, "Execute"):
        fb.Execute = on
    else:
        fb.Enable = on


def finished(fb: Any) -> bool:
    return bool(
        getattr(fb, "Done", False)
        or getattr(fb, "Valid", False)
        or getattr(fb, "Enabled", False)
        or getattr(fb, "Active", False)
        or fb.Error
    )


def outputs(fb: Any) -> dict[str, Any]:
    names = (
        "Busy",
        "Done",
        "Enabled",
        "Valid",
        "Active",
        "Error",
        "CommandBuffered",
        "CommandAborted",
        "CommandInterrupted",
        "ParameterAccepted",
        "ErrorID",
        "WarningID",
        "InfoID",
    )
    return {n: getattr(fb, n) for n in names if hasattr(fb, n)}


def commands(sim: SdkSimulator, cmd_type: int, start_log: int = 0) -> int:
    """Commands of ``cmd_type`` the SDK accepted since log entry ``start_log``."""
    return sum(
        1
        for log in sim.logs[start_log:]
        if f"({cmd_type}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def cmd_type(name: str) -> int:
    return int(send_calls(CLASSES[name])[0].value)


# ------------------------------------------------------------------ GEN-04


@pytest.mark.parametrize("name", NAMES)
def test_gen04_not_executed(name: str) -> None:
    """GEN-04 (Siemens x-05): valid command, not executed -> all outputs FALSE / 0, nothing sent."""
    with robot() as (sim, h):
        start_log = len(sim.logs)
        fb = block(name, h)
        h.run(20)
        assert not any(outputs(fb).values()), outputs(fb)
        assert commands(sim, cmd_type(name), start_log) == 0


# ------------------------------------------------------------------ GEN-05

# mandatory parameters without a valid default (spec: M, no default) -> the block or the RC
# rejects the command with the default values; that is the correct reaction
GEN05_MANDATORY = {
    "MC_SetOperationModeFB": "OperationMode",
    "MC_SetSequenceFB": "TargetSequence",
    "MC_SwitchLanguageFB": "LanguageCode",
    "MC_UserLoginFB": "Username/Password",
    "MC_ReadAnalogInputFB": "Index",
    "MC_SetTriggerRegisterFB": "TriggerMode",
    "MC_ReadLoadDataFB": "LoadNo (load 0 cannot be read)",
    "MC_WriteLoadDataFB": "LoadNo",
    "MC_WriteFrameDataFB": "FrameNo (frame 0 = world cannot be written)",
    "MC_WriteToolDataFB": "ToolNo (tool 0 = flange cannot be written)",
    "MC_WriteRobotSWLimitsFB": "limits (0/0 for all axes)",
    "MC_CreateSplineFB": "SplineData (at least one point)",
}
GEN05_KNOWN = {
    "MC_ActivateConveyorTrackingFB": "precondition: the RC reports ConveyorTrackingEnabled",
    "MC_MoveSuperImposedFB": "precondition: needs a motion to superimpose",
    "MC_MoveSplineFB": "precondition: needs a spline created with CreateSpline",
}


@pytest.mark.parametrize("name", NAMES)
def test_gen05_default_values(name: str) -> None:
    """GEN-05 (Siemens x-06): valid command with the default values, positive edge -> Done /
    Enabled / Valid without error (ST-FIX F41, F43, F44); blocks with mandatory parameters
    without default reject the command."""
    if name in GEN05_KNOWN:
        pytest.xfail(GEN05_KNOWN[name])
    with robot() as (_, h):
        fb = block(name, h, values=False)
        start(fb)
        h.run(200, until=lambda: finished(fb))
        if name in GEN05_MANDATORY:
            assert fb.Error and fb.ErrorID, outputs(fb)
        else:
            assert finished(fb) and not fb.Error, outputs(fb)


# ------------------------------------------------------------------ GEN-06

# one command per position (DataIndex) / per spline point (ST-FIX F33)
GEN06_REPEAT = {"MC_CalculateFrameFB", "MC_CalculateToolFB", "MC_CreateSplineFB"}
GEN06_KNOWN = {
    "MC_MoveSuperImposedFB": "precondition: needs a motion to superimpose",
    "MC_MoveSplineFB": "precondition: needs a spline created with CreateSpline",
}


@pytest.mark.parametrize("name", EXECUTE)
def test_gen06_continuous_execute(name: str) -> None:
    """GEN-06 (Siemens x-07): Execute stays TRUE -> the command is executed once, Done stays
    TRUE as long as Execute is TRUE and is reset with its falling edge."""
    if name in GEN06_KNOWN:
        pytest.xfail(GEN06_KNOWN[name])
    with robot() as (sim, h):
        fb = block(name, h)
        start_log = len(sim.logs)
        start(fb)
        h.run(200, until=lambda: finished(fb))
        h.run(50)
        if fb.Error:
            pytest.skip(f"command rejected by the RC ({fb.ErrorID:#x}), see test_bilateral")
        assert fb.Done, outputs(fb)
        count = commands(sim, cmd_type(name), start_log)
        assert count >= 1 if name in GEN06_REPEAT else count == 1
        start(fb, False)
        h.run(2)
        assert not fb.Done


# ------------------------------------------------------------------ GEN-07

# blocks of the start-up sequence may run before the commands are enabled; without RobotTask
# they end with ERR_TIMEOUT_CMD after the command timeout (5 s, ST-FIX F47/F53)
GEN07_STARTUP = {"MC_ExchangeConfigurationFB", "MC_ReadMessagesFB", "MC_ReadRobotDataFB"}


@pytest.mark.parametrize("name", NAMES)
def test_gen07_axes_group_not_initialized(name: str) -> None:
    """GEN-07 (Siemens x-08 "Axes group is not defined"): RobotTask not running -> Error (blocks
    of the start-up: after the command timeout)."""
    with robot(initialized=False) as (sim, h):
        fb = block(name, h)
        start(fb)
        h.run(700 if name in GEN07_STARTUP else 100, until=lambda: bool(fb.Error))
        assert fb.Error and fb.ErrorID != 0, outputs(fb)
        assert commands(sim, cmd_type(name)) == 0


# ------------------------------------------------------------------ GEN-08


@pytest.mark.parametrize("name", EXECUTE)
def test_gen08_execute_for_one_cycle(name: str) -> None:
    """GEN-08 (Siemens 1-13, spec 5.5.x "Output status"): Execute TRUE for one cycle -> the command
    is executed anyway and Done / Error / CommandAborted is set for at least one cycle."""
    if name in GEN06_KNOWN:
        pytest.xfail(GEN06_KNOWN[name])
    with robot() as (sim, h):
        fb = block(name, h)
        start(fb)
        h.run(1)
        start(fb, False)
        seen = set()
        for _ in range(200):
            h.cycle()
            seen |= {k for k in ("Done", "Error", "CommandAborted") if getattr(fb, k, False)}
            if seen and not fb.Busy:
                break
        assert seen, outputs(fb)
        assert commands(sim, cmd_type(name)) >= 1


# ------------------------------------------------------------------ GEN-09


@pytest.mark.parametrize("name", NAMES)
def test_gen09_undefined_exec_mode(name: str) -> None:
    """GEN-09 (Siemens x-09 "AbortingMode is not defined", ST-FIX F48): undefined AbortingMode
    (18), ProcessingMode (18) or ExecMode (18) for blocks without these inputs -> Error, nothing
    sent."""
    with robot() as (sim, h):
        start_log = len(sim.logs)
        fb = block(name, h)
        for key in ("AbortingMode", "ProcessingMode", "ExecMode"):
            if hasattr(fb, key):
                setattr(fb, key, 18)
                break
        start(fb)
        h.run(100, until=lambda: finished(fb))
        assert fb.Error and not fb.Busy, outputs(fb)
        assert commands(sim, cmd_type(name), start_log) == 0


# ------------------------------------------------------------------ ERR-01


def _enum_parameters() -> list[tuple[str, str]]:
    cases = []
    for name in NAMES:
        for path, value, _, _ in leaves(CLASSES[name]().ParCmd):
            if isinstance(value, enum.IntEnum) and not re.match(r"SplineData\[[1-9]", path):
                cases.append((name, path))  # spline: the enums of the first point are enough
    return cases


ERR01_KNOWN: dict[tuple[str, str], str] = {}  # F49 fixed


@pytest.mark.parametrize(("name", "path"), _enum_parameters())
def test_err01_undefined_enum_value(name: str, path: str) -> None:
    """ERR-01 (Siemens "ErrorID": "Use ... that isn't defined"): undefined value of an enum
    parameter -> Error."""
    if (name, path) in ERR01_KNOWN:
        pytest.xfail(ERR01_KNOWN[(name, path)])
    with robot() as (_, h):
        fb = block(name, h)
        for p, value, owner, key in leaves(fb.ParCmd):
            if p == path:
                bad = max(m.value for m in type(value)) + 10
                if isinstance(key, int):
                    list.__setitem__(owner, key, bad) if isinstance(owner, list) else owner.__setitem__(
                        key, bad
                    )
                else:
                    setattr(owner, key, bad)
        start(fb)
        h.run(100, until=lambda: finished(fb))
        assert fb.Error and fb.ErrorID != 0, outputs(fb)


# ------------------------------------------------------------------ ERR-02

RC_ERROR = 0x8123


@pytest.mark.parametrize("name", NAMES)
def test_err02_error_of_the_rc(name: str) -> None:
    """ERR-02 (Siemens "ErrorID": "Error occurred during execution"): the RC answers with an
    error -> Error, ErrorID of the RC."""
    t = cmd_type(name)
    if t in SDK_NATIVE:
        pytest.skip("command implemented by the SDK itself (errors: tests/sdk/test_core_fbs.py)")
    with robot() as (sim, h):
        sim.set_command_error(t, RC_ERROR)
        fb = block(name, h)
        start(fb)
        h.run(100, until=lambda: finished(fb))
        assert fb.Error and fb.ErrorID == RC_ERROR, outputs(fb)


# ------------------------------------------------------------------ PM / SEQ (motion)

MOTION = sorted(n for n in NAMES if hasattr(CLASSES[n](), "AbortingMode") and n.startswith("MC_Move"))
# blocks whose valid command is rejected by the RC or needs a precondition (see GEN-05, bilateral)
MOTION_KNOWN = {
    "MC_MoveSplineFB": "precondition: needs a spline created with CreateSpline",
    "MC_MoveSuperImposedFB": "precondition: needs a motion to superimpose",
}


def _motion(name: str, h: RobotTaskHarness) -> Any:
    fb = block(name, h)
    for rate in ("DecelerationRate", "JerkRate"):  # the SDK supports only "not set"
        if hasattr(fb.ParCmd, rate):
            setattr(fb.ParCmd, rate, -1.0)
    for field in ("MoveTime", "BlendingMode", "Manipulation"):  # not supported by the simulation
        if hasattr(fb.ParCmd, field):
            setattr(fb.ParCmd, field, type(getattr(fb.ParCmd, field))(0))
    return fb


@pytest.mark.parametrize("name", MOTION)
def test_pm01_buffered(name: str) -> None:
    """PM-01 (Siemens "ProcessingMode"/"AbortingMode = Buffer"): two commands of the same kind
    -> the second one is buffered until the first one is done, both are Done in this order."""
    if name in MOTION_KNOWN:
        pytest.xfail(MOTION_KNOWN[name])
    with robot() as (sim, h):
        sim.set_move_cycles(30)
        first, second = _motion(name, h), _motion(name, h)
        start(first)
        h.run(3)
        start(second)
        done_order: list[str] = []
        for _ in range(300):
            h.cycle()
            for label, fb in (("first", first), ("second", second)):
                if fb.Done and label not in done_order:
                    done_order.append(label)
                if fb.Error:
                    pytest.fail(f"{label}: error {fb.ErrorID:#x}")
            if first.Active:
                assert not second.Active, "second command active while the first one is active"
            if len(done_order) == 2:
                break
        assert done_order == ["first", "second"], (outputs(first), outputs(second))


@pytest.mark.parametrize("name", MOTION)
def test_pm02_aborting(name: str) -> None:
    """PM-02 (Siemens "AbortingMode = Abort"): a second command with AbortingMode ABORT aborts
    the active one -> first CommandAborted, second Done."""
    if name in MOTION_KNOWN:
        pytest.xfail(MOTION_KNOWN[name])
    if not 2100 < cmd_type(name) < 2299:
        pytest.skip("SDK: only types 2101..2298 are motion commands of the planner (cam 240x)")
    with robot() as (sim, h):
        sim.set_move_cycles(100)
        first, second = _motion(name, h), _motion(name, h)
        start(first)
        h.run(100, until=lambda: bool(first.Active or first.Error))
        assert first.Active, outputs(first)
        second.AbortingMode = type(second.AbortingMode).ABORT
        start(second)
        h.run(400, until=lambda: bool(second.Done or second.Error))
        assert second.Done, outputs(second)
        assert first.CommandAborted and not first.Done, outputs(first)


EXEC_MODE_FBS = sorted(
    n for n in NAMES if hasattr(CLASSES[n](), "AbortingMode") or hasattr(CLASSES[n](), "ProcessingMode")
)


def _exec_mode_combinations(fb: Any) -> list[tuple[dict[str, Any], int]]:
    """(inputs, expected ExecutionMode) of spec table 5-77 for the inputs the block has."""
    from srci.types import AbortingMode, ExecutionMode, ProcessingMode

    seq = (
        [SequenceFlag.PRIMARY_SEQUENCE, SequenceFlag.SECONDARY_SEQUENCE]
        if hasattr(fb, "SequenceFlag")
        else [None]
    )
    out: list[tuple[dict[str, Any], int]] = []
    for flag in seq:
        secondary = flag == SequenceFlag.SECONDARY_SEQUENCE
        base = {} if flag is None else {"SequenceFlag": flag}
        if hasattr(fb, "AbortingMode"):
            out.append(({**base, "AbortingMode": AbortingMode.BUFFER}, 7 if secondary else 0))
            out.append(({**base, "AbortingMode": AbortingMode.ABORT}, 8 if secondary else 1))
        else:
            out.append(({**base, "ProcessingMode": ProcessingMode.BUFFERED}, 7 if secondary else 0))
            out.append(({**base, "ProcessingMode": ProcessingMode.ABORTING}, 8 if secondary else 1))
            out.append(({**base, "ProcessingMode": ProcessingMode.TRIGGER_BUFFERED}, 7 if secondary else 0))
            out.append(({**base, "ProcessingMode": ProcessingMode.TRIGGER_ABORTING}, 8 if secondary else 1))
    if hasattr(fb, "ProcessingMode") and not hasattr(fb, "AbortingMode"):
        nos = {} if not hasattr(fb, "SequenceFlag") else {"SequenceFlag": SequenceFlag.NO_SEQUENCE}
        out += [
            ({**nos, "ProcessingMode": ProcessingMode.PARALLEL}, int(ExecutionMode.PARALLEL)),
            ({**nos, "ProcessingMode": ProcessingMode.CONTINUOUS}, int(ExecutionMode.CONTINUOUS)),
            ({**nos, "ProcessingMode": ProcessingMode.TRIGGER_ONCE}, int(ExecutionMode.PARALLEL)),
            ({**nos, "ProcessingMode": ProcessingMode.TRIGGER_MULTIPLE}, int(ExecutionMode.TRIGGER_MULTIPLE)),
        ]
    return out


@pytest.mark.parametrize("name", EXEC_MODE_FBS)
def test_pm03_execution_mode(name: str) -> None:
    """PM-03 (ST-FIX F51, spec table 5-77): the ExecutionMode in the telegram follows the inputs
    AbortingMode / ProcessingMode and SequenceFlag (Buffered/Aborting x primary/secondary,
    Parallel, Continuous, Trigger Once / Multiple)."""
    if name in MOTION_KNOWN:
        pytest.xfail(MOTION_KNOWN[name])
    checked = 0
    for inputs, expected in _exec_mode_combinations(CLASSES[name]()):
        with robot() as (sim, h):
            fb = _motion(name, h) if name in MOTION else block(name, h)
            for key, value in inputs.items():
                setattr(fb, key, value)
            start(fb)
            h.run(20)
            sent = sim.last_command(cmd_type(name))
            if sent is None:
                assert fb.Error, (inputs, outputs(fb))  # combination rejected by the block itself
                continue
            assert int(sent["@ExecutionMode"]) == expected, inputs
            checked += 1
    assert checked, "no combination was sent"


@pytest.mark.parametrize("name", MOTION)
def test_seq01_secondary_sequence(name: str) -> None:
    """SEQ-01 (Siemens "SequenceFlag", spec 5.6.4.5): the primary sequence is interrupted,
    SetSequence(secondary), a command with SequenceFlag SECONDARY + GroupContinue is
    executed while the primary command stays interrupted, SetSequence(primary) is accepted."""
    if name in MOTION_KNOWN:
        pytest.xfail(MOTION_KNOWN[name])
    if not 2100 < cmd_type(name) < 2299:
        pytest.skip("SDK: only types 2101..2298 are motion commands of the planner (cam 240x)")
    with robot() as (sim, h):
        sim.set_move_cycles(100)
        primary = _motion(name, h)
        start(primary)
        h.run(100, until=lambda: bool(primary.Active or primary.Error))
        interrupt = h.add(CLASSES_ALL["MC_GroupInterruptFB"](), Execute=True)
        h.run(100, until=lambda: bool(interrupt.Done or interrupt.Error))
        assert interrupt.Done and primary.CommandInterrupted, outputs(primary)
        to_secondary = h.add(CLASSES_ALL["MC_SetSequenceFB"](), Execute=True)
        to_secondary.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
        h.run(100, until=lambda: bool(to_secondary.Done or to_secondary.Error))
        assert to_secondary.Done, outputs(to_secondary)
        secondary = _motion(name, h)
        secondary.SequenceFlag = SequenceFlag.SECONDARY_SEQUENCE
        start(secondary)
        h.run(5)
        h.add(CLASSES_ALL["MC_GroupContinueFB"](), Execute=True)  # continue in the secondary sequence
        h.run(400, until=lambda: bool(secondary.Done or secondary.Error))
        assert secondary.Done, outputs(secondary)
        assert not primary.Done and primary.Busy, outputs(primary)
        # back to the primary sequence: SetSequence(primary) is accepted; the SDK then rejects
        # GroupContinue (0x8C02) and does not continue the primary command (SDK, not the client)
        to_primary = h.add(CLASSES_ALL["MC_SetSequenceFB"](), Execute=True)
        to_primary.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
        h.run(100, until=lambda: bool(to_primary.Done or to_primary.Error))
        assert to_primary.Done, outputs(to_primary)


CLASSES_ALL = dict(fb_classes())


# ------------------------------------------------------------------ REP-01 / BUF-01 / BUF-02


@pytest.mark.parametrize("name", EXECUTE)
def test_rep01_repeated_execution(name: str) -> None:
    """REP-01: the same instance is executed 5 times in a row (new rising edge after Done) ->
    every execution sends one command and ends with Done."""
    if name in GEN06_KNOWN:
        pytest.xfail(GEN06_KNOWN[name])
    with robot() as (sim, h):
        sim.set_move_cycles(5)
        fb = _motion(name, h) if name in MOTION else block(name, h)
        start_log = len(sim.logs)
        for run in range(5):
            start(fb)
            h.run(1000, until=lambda: bool(fb.Done or fb.Error))
            if fb.Error:
                pytest.skip(f"command rejected by the RC ({fb.ErrorID:#x}), see test_bilateral")
            assert fb.Done, (run, outputs(fb))
            start(fb, False)
            h.run(2)
            assert not fb.Done and not fb.Busy, (run, outputs(fb))
        count = commands(sim, cmd_type(name), start_log)
        assert count >= 5 if name in GEN06_REPEAT else count == 5


PLANNER = [n for n in MOTION if n not in MOTION_KNOWN and 2100 < cmd_type(n) < 2299]


@pytest.mark.parametrize("name", PLANNER)
def test_buf01_more_commands_than_register_entries(name: str) -> None:
    """BUF-01 (Siemens "1 CMD called 50 times in one cycle"): more motion commands started in
    one cycle than the active command register has entries -> the commands that fit are
    buffered and executed, the others end with Error ERR_NO_FREE_ACR_ENTRY; no command stays
    Busy."""
    from srci.types import RobotLibraryErrorIdEnum

    count = int(str(srci.parameters()["ACTIVE_CMD_REGISTER_ENTRIES_MAX"])) + 5
    with robot() as (sim, h):
        sim.set_move_cycles(3)
        fbs = [_motion(name, h) for _ in range(count)]
        for fb in fbs:
            start(fb)
        h.run(count * 10, until=lambda: all(fb.Done or fb.Error for fb in fbs))
        assert all(fb.Done or fb.Error for fb in fbs), [
            outputs(fb) for fb in fbs if not (fb.Done or fb.Error)
        ]
        errors = [fb for fb in fbs if fb.Error]
        assert errors, "register overflow not reported"
        assert {fb.ErrorID for fb in errors} == {RobotLibraryErrorIdEnum.ERR_NO_FREE_ACR_ENTRY}
        assert sum(fb.Done for fb in fbs) >= count - 10


@pytest.mark.parametrize("name", ["MC_GroupStopFB", "MC_GroupInterruptFB", "MC_WriteIntegersFB"])
def test_buf02_more_than_15_commands_in_one_cycle(name: str) -> None:
    """BUF-02 (Siemens "Call more than 15 CMDs in 1 Cycle"): 16 instances started in the same
    cycle -> all commands are sent and every instance ends with Done or with the error of the
    RC (a limit of the RC is not a limit of the client)."""
    with robot() as (sim, h):
        start_log = len(sim.logs)
        fbs = [h.add(CLASSES_ALL[name]()) for _ in range(16)]
        for fb in fbs:
            start(fb)
        h.run(500, until=lambda: all(fb.Done or fb.Error for fb in fbs))
        assert all(fb.Done or (fb.Error and fb.ErrorID) for fb in fbs), [outputs(fb) for fb in fbs]
        assert commands(sim, _type_of(name), start_log) == 16


def _type_of(name: str) -> int:
    return int(send_calls(CLASSES_ALL[name])[0].value)


@pytest.mark.parametrize(
    "name", ["MC_GroupStopFB", "MC_MoveAxesAbsoluteFB", "MC_ReadToolDataFB", "MC_EnableRobotFB"]
)
def test_tmo01_no_response(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """TMO-01 (ST-FIX F53): the RC never answers the command -> Error ERR_TIMEOUT_CMD after the
    command timeout (5 s), Busy FALSE; before the fix the block stayed Busy forever."""
    from srci.fb._internal.ActiveCommandRegisterFB import ActiveCommandRegisterFB
    from srci.types import RobotLibraryErrorIdEnum

    with robot() as (_, h):
        fb = _motion(name, h) if name in MOTION else h.add(CLASSES_ALL[name]())
        monkeypatch.setattr(ActiveCommandRegisterFB, "AddRsp", lambda self, **_: 0)
        start(fb)
        h.run(400)  # 4 s
        assert fb.Busy and not fb.Error, outputs(fb)
        h.run(200, until=lambda: bool(fb.Error))
        assert fb.Error and fb.ErrorID == RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, outputs(fb)
        assert not fb.Busy
