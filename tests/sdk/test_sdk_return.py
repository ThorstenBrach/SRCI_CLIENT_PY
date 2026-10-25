# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_sdk_return
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Tests of the commands added to the SRCI SDK ("SDK return").
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

"""Tests of the commands added to the SRCI SDK ("SDK return", private SDK branch sdk-return).

The SDK itself answers these commands: it decodes the command with its own CMD structure, calls
the firmware function (simulated robot of the harness) and encodes the response with its own RSP
structure. The firmware probe of the harness records the parameters the firmware received and
answers with the response values of the test (``SdkSimulator.firmware_command`` /
``set_response``, names of the specification). One run per function block:

* send: every parameter the firmware received equals the field of the telegram (decoded with the
  payload tables of the specification) - the CMD structure of the SDK matches the specification;
  every field of the telegram reaches the firmware (``FW_NOT_PASSED``: fields the SDK uses itself).
* recv: every response value of the firmware appears in ``OutCmd`` - the RSP structure of the
  SDK matches the specification.
* the function block completes without error.

Only the function blocks of the command types of the SDK return are tested (test data per group:
``tests/sdk/sdk_return/<group>.py``); commands this SDK does not answer itself are skipped.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, find_sdk_library, sdk_transport

import srci
from srci.iec.clock import FakeClock, use_clock
from tests.bilateral import Comparison, compare_fields, distinct_values, leaves, response_values
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.sdk_return import ADDED_TYPES, ERROR_CASES, FW_NOT_PASSED, KNOWN, PARCMD, RSP_VALUES
from tests.sdk.test_bilateral import NOT_IN_TELEGRAM, RECV_NOT_COMPARED, SKIP, _rename
from tools.payload_check import fb_classes, function_name, send_calls
from tools.spec_tables import load

# fields of the command header / trigger header: used by the SDK, not passed to the firmware
HEADER_FIELDS = ("Type", "ExecutionMode", "ParSeq", "EmitterID", "ListenerID", "SequenceFlag", "Priority")
# fields of the trigger response header: filled by the SDK (trigger engine), not by the firmware
TRIGGER_RSP = ("InvocationCounter", "OriginID", "MissedInvocationCounter")

@dataclass
class Result:
    cmd_type: int
    firmware: dict[str, str] | None
    received: dict[str, str] | None
    recv: Comparison | None
    error_id: int = 0
    done: bool = False
    notes: list[str] = field(default_factory=list)


@pytest.fixture(autouse=True, scope="module")
def sdk_parameters() -> Any:
    try:
        find_sdk_library()
    except Exception as exc:
        pytest.skip(str(exc))
    if not hasattr(SdkSimulator, "firmware_command"):
        pytest.skip("SDK simulator without firmware probe (SDK return)")
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@cache
def run(name: str, overrides: tuple[tuple[str, Any], ...] = ()) -> Result:
    """Executes the function block ``name`` against the SDK (once per test session);
    ``overrides``: ParCmd values (path, value) set after the distinct values."""
    from tests.sdk.test_core_fbs import enable
    from tests.sdk.test_methodology import PARCMD_INPUTS

    from tests.sdk.test_bilateral import FB_INPUTS

    cls = dict(fb_classes())[name]
    cmd_type = int(send_calls(cls)[0].value)
    table = load().get((function_name(name), "recv"))
    rsp = response_values(table.entries) if table else {}
    rsp.update(RSP_VALUES.get(name, {}))
    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sim, SIZE, SIZE), advance=clock.advance)
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        if name != "MC_EnableRobotFB":
            enable(h, sim)
        sim.set_response(cmd_type, rsp)
        fb = cls()
        for key, value in FB_INPUTS.get(name, {}).items():
            setattr(fb, key, list(value) if isinstance(value, list) else value)
        if hasattr(fb, "ParCmd"):
            distinct_values(fb.ParCmd)
        for key, value in PARCMD_INPUTS.get(name, {}).items():
            setattr(fb.ParCmd, key, value)
        for path, value in (*PARCMD.get(name, {}).items(), *overrides):
            _set(fb.ParCmd, path, value)
        h.add(fb)
        if hasattr(fb, "Execute"):
            fb.Execute = True
        else:
            fb.Enable = True

        def done() -> bool:
            # Enable blocks without Valid (OpenBrake, FreeDrive, ...): output Enabled
            return bool(
                getattr(fb, "Done", False) or getattr(fb, "Valid", False) or getattr(fb, "Enabled", False)
            )

        def finished() -> bool:
            return done() or bool(fb.Error)

        h.run(200, until=finished)
        firmware = sim.firmware_command(cmd_type)
        received = sim.last_command(cmd_type)
        recv = None
        if rsp and hasattr(fb, "OutCmd") and firmware is not None:
            out = {path: value for path, value, _, _ in leaves(fb.OutCmd)}
            recv = compare_fields(_rename(name, out), {k: str(v) for k, v in rsp.items()})
        result = Result(cmd_type, firmware, received, recv, int(fb.ErrorID), done())
        result.notes.append(f"InfoID=16#{int(getattr(fb, 'InfoID', 0)):04X}")
        return result


def _set(obj: Any, path: str, value: Any) -> None:
    """Sets ``obj.<path>`` (path with "." and "[i]", e.g. ``Index[1]``)."""
    parts = path.replace("]", "").replace("[", ".").split(".")
    for part in parts[:-1]:
        obj = obj[int(part)] if part.isdigit() else getattr(obj, part)
    last = parts[-1]
    if last.isdigit():
        obj[int(last)] = value
    else:
        setattr(obj, last, value)


def _names() -> list[str]:
    return [
        n
        for n, c in fb_classes()
        if hasattr(c, "CreateCommandPayload") and n not in SKIP and int(send_calls(c)[0].value) in ADDED_TYPES
    ]


def _equal(a: str, b: str) -> bool:
    if a == b:
        return True
    try:
        x, y = float(a), float(b)
    except ValueError:
        return False
    return math.isclose(x, y, rel_tol=1e-6, abs_tol=1e-6)


def _header(name: str) -> bool:
    base = name.split("[")[0].split(".")[-1]
    return base in HEADER_FIELDS or base.startswith("Reserved") or name.startswith("@")


@cache
def _answered_by_sdk(cmd_type: int) -> bool:
    with SdkSimulator(10) as sim:
        return bool(sim.answered_by_sdk(cmd_type))


def _skip_unless_added(name: str) -> None:
    cmd_type = int(send_calls(dict(fb_classes())[name])[0].value)
    if not _answered_by_sdk(cmd_type):
        pytest.skip("command not implemented by this SDK (group of the SDK return not applied)")


def _result(name: str) -> Result:
    _skip_unless_added(name)
    if name in KNOWN:
        pytest.xfail(KNOWN[name])
    return run(name)


@pytest.mark.parametrize("name", _names())
def test_done(name: str) -> None:
    """The SDK executes the command without error."""
    result = _result(name)
    assert result.error_id == 0, f"ErrorID 16#{result.error_id:04X}"
    assert result.done


@pytest.mark.parametrize("name", _names())
def test_send(name: str) -> None:
    """Every parameter the firmware received equals the field of the telegram (CMD structure)."""
    result = _result(name)
    assert result.received is not None, "command not received by the SDK"
    assert result.firmware is not None, f"firmware function not called (ErrorID 16#{result.error_id:04X})"
    wrong = [
        f"{k}: firmware {v}, telegram {result.received.get(k)}"
        for k, v in result.firmware.items()
        if k not in result.received or not _equal(v, result.received[k])
    ]
    allowed = FW_NOT_PASSED.get(name, ())
    lost = [
        k
        for k in result.received
        if not _header(k) and k not in result.firmware and not any(k == a or k.startswith(a) for a in allowed)
    ]
    assert wrong == []
    assert lost == [], "fields of the telegram not passed to the firmware"


@pytest.mark.parametrize("name", _names())
def test_recv(name: str) -> None:
    """Every response value of the firmware appears in OutCmd (RSP structure)."""
    result = _result(name)
    if result.recv is None:
        pytest.skip("no response values")
    allowed = RECV_NOT_COMPARED + TRIGGER_RSP + NOT_IN_TELEGRAM.get(name, ())

    # also nested names (e.g. Data.DefinitionMode after RENAME), like _covered of test_bilateral
    def covered(p: str) -> bool:
        return any(p == a or p.startswith((a + ".", a + "[")) or f".{a}." in f".{p}." for a in allowed)

    problems = [m for m in result.recv.mismatched if not covered(m.split(":")[0])]
    problems += [f"{m}: no field in the telegram" for m in result.recv.missing if not covered(m)]
    assert problems == []


@pytest.mark.parametrize(
    ("name", "overrides", "error_id", "info_id"),
    ERROR_CASES,
    ids=[f"{n}-{e:04X}-{i:04X}" for n, _, e, i in ERROR_CASES],
)
def test_parameter_check(name: str, overrides: tuple[tuple[str, Any], ...], error_id: int, info_id: int) -> None:
    """The SDK checks the parameters of the added commands (error / info codes of the specification)."""
    if name not in _names():
        pytest.skip("function block not in the SRCI library or command not added")
    _skip_unless_added(name)
    result = run(name, overrides)
    assert result.received is not None, "command not received by the SDK"
    assert f"16#{result.error_id:04X}" == f"16#{error_id:04X}"
    if info_id:
        assert f"InfoID=16#{info_id:04X}" in result.notes
