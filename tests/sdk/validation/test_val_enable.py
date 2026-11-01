# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_val_enable
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    "Enable" blocks without a reference test set (VAL-ENA): enable, disable,
#    enable again and parameter update while enabled.
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

""" "Enable" blocks without a reference test set (area VAL-ENA).

The reference test sets of EnableRobot and GroupJog check the life cycle of a block with an
``Enable`` input: the function is enabled with the rising edge, stays enabled while Enable is
TRUE, ends with the falling edge without error, can be enabled again, and accepts changed
parameters while enabled (ParameterAccepted). The same is checked here for every other
"Enable" block (force control, free drive, work area monitoring, conveyor tracking, dynamic
spline, superimposed motion, ...). An error of the RC while enabled is MET ERR-03.
"""

from __future__ import annotations

from typing import Any

import pytest

from tests.bilateral import leaves
from tests.sdk.test_methodology import CLASSES, block, cmd_type, commands, outputs, robot

REFERENCE = {"MC_EnableRobotFB", "MC_GroupJogFB", "MC_ReturnToPrimaryFB"}
# needs a motion to superimpose (16#8D21 without one): tested with a motion in VAL-EFF
PRECONDITION = {"MC_MoveSuperImposedDynamicFB"}
NAMES = sorted(n for n, c in CLASSES.items() if hasattr(c(), "Enable") and n not in REFERENCE | PRECONDITION)
UPDATE = [n for n in NAMES if hasattr(CLASSES[n](), "ParameterAccepted")]
_F146 = (
    "LIB-BUG F146: CheckParameterChanged returns at once for an empty ParCmd, so the internal update "
    "with Enable FALSE is never sent: the block stays Enabled / Busy and the RC keeps the function enabled"
)
_F147 = (
    "LIB-BUG F147: ParameterAccepted is set only for the RC states BUFFERED / BUFFERED_IN_PLANNER; an "
    "enable function the RC answers ACTIVE at once, and every acknowledged parameter update, never shows it"
)
_SDK_ENABLE = (
    "SDK-GAP: the Enable FALSE of a parameter update is not evaluated by the SDK, the function stays ACTIVE "
    "(see the SDK notes of ST_FINDINGS, like ReturnToPrimary / F141)"
)
KNOWN: dict[tuple[str, str], str] = {
    **{
        (t, n): _F146 for n in ("MC_FreeDriveFB", "MC_PathAccuracyModeFB") for t in ("cycle", "again", "ends")
    },
    **{("accepted", n): _F147 for n in UPDATE},
    **{
        ("ends", n): _SDK_ENABLE
        for n in (
            "MC_ActivateConveyorTrackingFB",
            "MC_DynamicSplineFB",
            "MC_ForceControlFB",
            "MC_ForceLimitFB",
            "MC_MonitorWorkAreaFB",
            "MC_SyncToConveyorFB",
            "MC_UnitMeasurementFB",
        )
    },
    ("again", "MC_SyncToConveyorFB"): _SDK_ENABLE
    + "; the second SyncToConveyor stays buffered behind the first one",
}
CYCLES = 100


def _params(test: str, names: list[str]) -> list[Any]:
    return [
        pytest.param(n, marks=pytest.mark.xfail(strict=True, reason=KNOWN[(test, n)]))
        if (test, n) in KNOWN
        else pytest.param(n)
        for n in names
    ]


def _on(fb: Any) -> bool:
    """The function is enabled (MonitorWorkArea has only Valid)."""
    return bool(getattr(fb, "Enabled", False) or (not hasattr(fb, "Enabled") and fb.Valid))


def _off(fb: Any) -> bool:
    return not (_on(fb) or fb.Busy or fb.Error)


@pytest.mark.parametrize("name", _params("cycle", NAMES))
def test_enable_and_disable(name: str) -> None:
    """Enable TRUE: Busy and enabled without error, also some cycles later; Enable FALSE: the
    outputs return to FALSE without error."""
    with robot() as (_, h):
        fb = block(name, h)
        fb.Enable = True
        h.run(CYCLES, until=lambda: _on(fb) or bool(fb.Error))
        assert _on(fb) and fb.Busy and not fb.Error, outputs(fb)
        h.run(20)
        assert _on(fb) and not fb.Error, outputs(fb)
        fb.Enable = False
        h.run(CYCLES, until=lambda: _off(fb))
        assert _off(fb), outputs(fb)
        h.run(10)
        assert _off(fb), outputs(fb)


@pytest.mark.parametrize("name", _params("again", NAMES))
def test_enable_again(name: str) -> None:
    """After Enable FALSE the same instance can be enabled again: the command is sent a second time."""
    with robot() as (sim, h):
        fb = block(name, h)
        start_log = len(sim.logs)
        for _ in range(2):
            fb.Enable = True
            h.run(CYCLES, until=lambda: _on(fb) or bool(fb.Error))
            assert _on(fb) and not fb.Error, outputs(fb)
            fb.Enable = False
            h.run(CYCLES, until=lambda: _off(fb))
            assert _off(fb), outputs(fb)
        assert commands(sim, cmd_type(name), start_log) == 2


@pytest.mark.parametrize("name", _params("ends", NAMES))
def test_disable_ends_the_function_on_the_rc(name: str) -> None:
    """Enable FALSE also ends the function on the RC: the command is DONE or ABORTED there."""
    with robot() as (sim, h):
        fb = block(name, h)
        fb.Enable = True
        h.run(CYCLES, until=lambda: _on(fb) or bool(fb.Error))
        assert _on(fb), outputs(fb)
        start_log = len(sim.logs)
        fb.Enable = False
        h.run(CYCLES)
        tag = f"({cmd_type(name)}), cmdID"
        assert any(
            tag in log.text and ("-> DONE" in log.text or "-> ABORTED" in log.text)
            for log in sim.logs[start_log:]
        ), outputs(fb)


def _changeable(fb: Any) -> tuple[str, Any, Any]:
    """The first REAL (else BOOL) parameter (path, owner, key)."""
    for kind in (float, bool):
        for path, value, owner, key in leaves(fb.ParCmd):
            if type(value) is kind and not str(key).startswith("Bit"):  # BitNN: reserved bits
                return path, owner, key
    pytest.skip("no REAL or BOOL parameter to change")


def _change(fb: Any) -> str:
    path, owner, key = _changeable(fb)
    old = owner[key] if isinstance(key, int) else getattr(owner, key)
    new = (not old) if isinstance(old, bool) else old + 1.0
    if isinstance(key, int):
        owner[key] = new
    else:
        setattr(owner, key, new)
    return path


@pytest.mark.parametrize("name", _params("update", UPDATE))
def test_parameter_update_is_acknowledged(name: str) -> None:
    """A parameter changed while enabled is sent as parameter update (new ParSeq) and acknowledged by
    the RC; the function stays enabled without error."""
    with robot() as (_, h):
        fb = block(name, h)
        fb.Enable = True
        h.run(CYCLES, until=lambda: _on(fb) or bool(fb.Error))
        h.run(10)
        assert _on(fb), outputs(fb)
        par_seq = fb._command.ParSeq
        path = _change(fb)
        h.run(
            CYCLES, until=lambda: fb._command.ParSeq != par_seq and fb._response.ParSeq == fb._command.ParSeq
        )
        assert fb._command.ParSeq != par_seq, path
        assert fb._response.ParSeq == fb._command.ParSeq, (path, fb._response.ParSeq, fb._command.ParSeq)
        assert _on(fb) and not fb.Error, (path, outputs(fb))


@pytest.mark.parametrize("name", _params("accepted", UPDATE))
def test_parameter_accepted_while_enabled(name: str) -> None:
    """ParameterAccepted is TRUE once the RC acknowledged the parameters: after the enable and again
    after a parameter update (spec: can differ from CommandBuffered for "Enable" blocks)."""
    with robot() as (_, h):
        fb = block(name, h)
        fb.Enable = True
        h.run(CYCLES, until=lambda: (_on(fb) and bool(fb.ParameterAccepted)) or bool(fb.Error))
        assert _on(fb) and fb.ParameterAccepted, outputs(fb)
        _change(fb)
        h.run(CYCLES, until=lambda: fb._response.ParSeq == fb._command.ParSeq and bool(fb.ParameterAccepted))
        assert fb.ParameterAccepted and _on(fb), outputs(fb)
