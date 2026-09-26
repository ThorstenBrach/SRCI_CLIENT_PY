"""Bilateral tests of every function block against the SRCI SDK.

One run per function block: ``ParCmd`` is filled with distinct valid values
(``tests.bilateral.distinct_values``), the SDK answers with distinct values for every field of
the response table of the specification (commands the SDK does not implement itself), the
function block is executed until Done / Valid / Error.

* send: every ``ParCmd`` value must arrive in the SDK (decoded with the payload tables of the
  specification) - ``SdkSimulator.last_command``.
* recv: every value the SDK sent must appear in ``OutCmd``.

Leaves of ``ParCmd`` / ``OutCmd`` without a field in the telegram are listed in
``NOT_IN_TELEGRAM`` (reviewed: finding F39). Known deviations are ``xfail`` with the finding.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import pytest

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.sim.sdk import SdkSimulator, find_sdk_library, sdk_transport
from srci.types import SequenceFlag
from tests.bilateral import Comparison, compare_fields, distinct_values, leaves, response_values
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tools.payload_check import fb_classes, function_name, send_calls
from tools.spec_tables import load

# command types the SDK implements itself (its own response values)
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

# not testable this way: cyclic functions (no command), payload > 255 bytes (F33)
SKIP = {
    "MC_ReadActualPositionCyclicFB": "cyclic data, no command",
    "MC_ReadCallSubprogramCyclicFB": "cyclic data, no command",
    "MC_WriteCallSubprogramCyclicFB": "cyclic data, no command",
    "MC_CreateSplineFB": "F33: payload > 255 bytes",
    "MC_DynamicSplineFB": "F33: payload > 255 bytes",
}

# inputs of the function block itself (not ParCmd) needed for a valid command
FB_INPUTS: dict[str, dict[str, Any]] = {
    "MC_CollisionDetectionFB": {"SequenceFlag": SequenceFlag.PRIMARY_SEQUENCE}
}


@dataclass
class Result:
    cmd_type: int
    send: Comparison | None
    recv: Comparison | None
    error_id: int = 0
    notes: list[str] = field(default_factory=list)


@pytest.fixture(autouse=True, scope="module")
def sdk_parameters() -> Iterator[None]:
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@cache
def run(name: str) -> Result:
    """Executes the function block ``name`` against the SDK (once per test session)."""
    from tests.sdk.test_core_fbs import enable

    cls = dict(fb_classes())[name]
    cmd_type = int(send_calls(cls)[0].value)
    table = load().get((function_name(name), "recv"))
    rsp = response_values(table.entries) if table and cmd_type not in SDK_NATIVE else {}
    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sim, SIZE, SIZE), advance=clock.advance)
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        enable(h, sim)
        sim.set_response(cmd_type, rsp)
        fb = cls()
        for key, value in FB_INPUTS.get(name, {}).items():
            setattr(fb, key, value)
        sent = distinct_values(fb.ParCmd) if hasattr(fb, "ParCmd") else {}
        h.add(fb)
        if hasattr(fb, "Execute"):
            fb.Execute = True
        else:
            fb.Enable = True
        h.run(200, until=lambda: bool(getattr(fb, "Done", False) or getattr(fb, "Valid", False) or fb.Error))
        received = sim.last_command(cmd_type)
        send = compare_fields(_rename(name, sent), received) if received is not None else None
        recv = None
        if rsp and hasattr(fb, "OutCmd"):
            out = {path: value for path, value, _, _ in leaves(fb.OutCmd)}
            recv = compare_fields(_rename(name, out), {k: str(v) for k, v in rsp.items()})
        return Result(cmd_type, send, recv, int(fb.ErrorID))


def _rename(name: str, values: dict[str, Any]) -> dict[str, Any]:
    """Leaves of ParCmd/OutCmd renamed to the names of the specification (RENAME)."""
    out = {}
    for path, value in values.items():
        for old, new in RENAME.get(name, ()):
            if path == old or path.startswith((old + ".", old + "[")):
                path = new + path[len(old) :]
                break
        out[path] = value
    return out


def _names() -> list[str]:
    return [n for n, c in fb_classes() if hasattr(c, "CreateCommandPayload")]


def _covered(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path == a or path.startswith((a + ".", a + "[")) or f".{a}." in f".{path}." for a in prefixes)


def _problems(c: Comparison | None, allowed: tuple[str, ...]) -> list[str]:
    if c is None:
        return ["command not received by the SDK"]
    mismatched = [m for m in c.mismatched if not _covered(m.split(":")[0], allowed)]
    missing = [m for m in c.missing if not _covered(m, allowed)]
    return mismatched + [f"{m}: no field in the telegram" for m in missing]


@pytest.fixture(scope="module")
def sdk_available() -> None:
    try:
        find_sdk_library()
    except Exception as exc:
        pytest.skip(str(exc))


@pytest.mark.parametrize("name", _names())
def test_send(sdk_available: None, name: str) -> None:
    """Every ParCmd value arrives in the SDK with the value and at the place of the specification."""
    if name in SKIP:
        pytest.skip(SKIP[name])
    if name in KNOWN_SEND:
        pytest.xfail(KNOWN_SEND[name])
    result = run(name)
    assert _problems(result.send, NOT_IN_TELEGRAM.get(name, ())) == []


@pytest.mark.parametrize("name", _names())
def test_recv(sdk_available: None, name: str) -> None:
    """Every value of the response of the SDK appears in OutCmd."""
    if name in SKIP:
        pytest.skip(SKIP[name])
    result = run(name)
    if result.cmd_type in SDK_NATIVE:
        pytest.skip("response values of the SDK itself (tests/sdk/test_core_fbs.py)")
    if result.recv is None:
        pytest.skip("no response values (no OutCmd or empty response table)")
    if name in KNOWN_RECV:
        pytest.xfail(KNOWN_RECV[name])
    assert _problems(result.recv, RECV_NOT_COMPARED + NOT_IN_TELEGRAM.get(name, ())) == []


# ------------------------------------------------------------------ known deviations
# see docs/ST_FINDINGS.md; an xfail entry fails (strict) when the deviation is fixed

KNOWN_SEND: dict[str, str] = {
    "MC_OpenBrakeFB": "F33: RobotAxes/ExternalAxesBrakeRelease not sent as in the spec",
    "MC_MoveApproachDirectFB": "F33: additional Reserve byte after the ArmConfig -> E1..E6 shifted",
    "MC_MoveCircularAbsoluteFB": "F33: PathChoice/Manipulation as 2 bytes, ConfigMode/TurnMode/Time missing",
    "MC_MoveCircularCamFB": "F33: Time missing -> AuxPoint/EndPoint E2..E6 shifted",
    "MC_MoveLinearCamFB": "F33: additional BOOL before BlendingParameter -> positions shifted",
    "MC_MoveLinearRelativeFB": "F33: Reserved byte before Time missing -> Time, E2..E6 shifted",
    "MC_LoadMeasurementAutomaticFB": "F33: Position_1 complete before Position_2 (spec: J1..E1 of both, then E2..E6)",
    "MC_ForceControlFB": "F33: ReferenceType sent as UINT -> following values shifted",
    "MC_UserLoginFB": "F34: Password/Username not padded to 50 characters",
    "MC_SetTriggerLimitFB": "F33: Reserved byte after ListenerID missing -> all values shifted",
    "MC_SetTriggerMotionFB": "F33: Reserved byte after ListenerID missing -> all values shifted",
    "MC_WriteWorkAreaFB": "F33: additional byte before ZeroPointX, limits not as in the spec",
    "MC_WriteDigitalOutputsFB": "F33: Index[5..6]/Reserved missing, Values as REAL",
    "MC_WriteIntegersFB": "F33: FOR 1 TO 6 -> Values/Index shifted by one",
    "MC_WriteSystemVariableFB": "F33: last byte (RCParameter) not sent",
    "MC_ReturnToPrimaryFB": "spec: TrajectoryMode is USINT 0/1/2 (6.3.11.3) but one bit in table 6-332",
    "MC_MoveSuperImposedDynamicFB": "spec: table 6-492 lacks Offset.RZ, byte numbers inconsistent",
}

KNOWN_RECV: dict[str, str] = {
    "MC_CallSubprogramFB": "F33: ReturnData one byte short -> shifted; InstanceID not in the response",
    "MC_OpenBrakeFB": "F33: ExternalAxesBrakeReleased not read, bytes shifted",
    "MC_UnitMeasurementFB": "F40: OutCmd only updated in state ACTIVE - values of a DONE response are lost",
    "MC_SyncToConveyorFB": "F40: OutCmd only updated in state ACTIVE - values of a DONE response are lost",
    "MC_CalculateToolFB": "F33: ToolData parsed before TCPMaxError/TCPMeanError",
    "MC_ForceLimitFB": "F33: additional byte before OriginID",
    "MC_ReadDHParameterFB": "F33: PositiveJointDirection bits read as 7 bytes",
    "MC_ReadWorkAreaFB": "F33: additional byte before ZeroPointX, limits not as in the spec",
    "MC_MonitorWorkAreaFB": "F33: 2 WORDs read, spec has 1 (MonitoringState)",
}

# leaves of ParCmd/OutCmd that have no field in the telegram of the specification (F39, to be
# reviewed: parameters of an older/newer draft, values used only in the PLC, ...)
NOT_IN_TELEGRAM: dict[str, tuple[str, ...]] = {
    "MC_CollisionDetectionFB": ("ProcessingMode", "SequenceFlag"),
    "MC_StopSubprogramFB": ("SequenceFlag",),
    "MC_UnitMeasurementFB": ("NewMeasurement",),
    "MC_MovePickPlaceDirectFB": ("ReductionRate",),
    "MC_MoveAxesAbsoluteFB": ("ConfigMode",),
    "MC_ActivateConveyorTrackingFB": ("PLCEncoderValue", "RCEncoderValue"),
    "MC_RedefineTrackingPosFB": ("InitObjectPosition",),
    "MC_MoveSuperImposedFB": (
        "VelocityDiffRate",
        "AccelerationDiffRate",
        "DecelerationDiffRate",
        "JerkDiffRate",
    ),
    "MC_SetTriggerRegisterFB": ("EvaluateStartCondition",),
    # the position selected by DataIndex is sent (one per command), the arrays are not compared
    "MC_CalculateToolFB": ("PositionsArray",),
    "MC_CalculateFrameFB": ("Origin", "OriginShift", "Position_X", "Position_XY"),
    "MC_LoadMeasurementAutomaticFB": ("MeasuringID",),
    "MC_LoadMeasurementSequentialFB": ("MeasuringID",),
    "MC_ReadActualTCPVelocityFB": ("OriginID", "InvocationCounter"),
    "MC_MoveSplineFB": ("ActualIndex",),
    "MC_CalculateForwardKinematicFB": ("TargetToolNoReturn", "TargetFrameNoReturn"),
    "MC_MeasuringInputFB": ("Measurings[2]", "Measurings[3]"),
}

# response direction: FollowID is set by the PLC library (trigger chain), ArmConfig bits are
# covered by the layout tests (the bit names repeat in responses with several positions)
RECV_NOT_COMPARED: tuple[str, ...] = ("FollowID", "Config")

# ParCmd/OutCmd names -> names of the specification
RENAME: dict[str, tuple[tuple[str, str], ...]] = {
    "MC_CalculateFrameFB": (
        ("IEC_Date", "FrameData.Date"),
        ("IEC_TIME", "FrameData.Time"),
        ("ReferenceFrame", "FrameData.ReferenceFrame"),
        ("Position", "FrameData"),
    ),
    "MC_ActivateConveyorTrackingFB": (("TrackingStatus", "TrackingStatusByte"),),
    "MC_MeasuringInputFB": tuple(
        (f"Measurings[{i}].{field}", f"{spec}_{i + 1}")
        for i in (0, 1)
        for field, spec in (
            ("MeasuredCartesianPosition", "MeasuredCartesianPosition"),
            ("MeasuredJointPosition", "MeasuredJointPosition"),
            ("ToolNo", "ToolNo"),
            ("FrameNo", "FrameNo"),
        )
    ),
}
