# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_val_parameters
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Parameter tests of the function blocks without a reference test set
#    (VAL-PAR): REAL values, listed values and ranges of the specification.
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

"""Parameter tests of the function blocks without a reference test set (area VAL-PAR).

The reference test sets check every parameter of a command: valid values are executed, invalid
values end with an error. The same method is applied here to the function blocks the reference
does not cover, generically per parameter:

* every REAL parameter: NaN is rejected by the client, nothing is sent (the check of a valid
  REAL also covers infinity)
* every value the specification lists for a parameter is sent to the RC
* a value the specification does not list ends with Error (client or RC)
* the bounds of a range of the specification are sent, a value outside ends with Error

The values and ranges are taken from the command value tables of the specification
(tools/spec_tables/spec_parameter_values.json). Known deviations are strict ``xfail`` with the
finding of docs/ST_FINDINGS.md.
"""

from __future__ import annotations

import math
import re
from typing import Any

import pytest

from tests.bilateral import leaves
from tests.sdk.test_methodology import CLASSES, block, cmd_type, commands, finished, outputs, robot, start
from tools.spec_tables.values import load

# function blocks with a reference test set (their parameters are tested in the RC-* / PLC-* areas)
REFERENCE = {
    "BrakeTest", "CallSubprogram", "ChangeSpeedOverride", "CreateServerLog", "EnableRobot", "GroupContinue",
    "GroupInterrupt", "GroupJog", "GroupReset", "GroupStop", "MoveAxesAbsolute", "MoveDirectAbsolute",
    "MoveLinearAbsolute", "ReadActualPosition", "ReadFrameData", "ReadLoadData", "ReadRobotDefaultDynamics",
    "ReadRobotReferenceDynamics", "ReadRobotSWLimits", "ReadSafeReferencePosition", "ReadServerLog",
    "ReadToolData", "ReturnToPrimary", "SafeReferencing", "SetOperationMode", "SetSequence", "StopSubprogram",
    "WriteFrameData", "WriteLoadData", "WriteRobotDefaultDynamics", "WriteRobotReferenceDynamics",
    "WriteRobotSWLimits", "WriteToolData",
}  # fmt: skip
NAMES = sorted(n for n in CLASSES if n[3:-2] not in REFERENCE)
SPEC = {k.lower(): v for k, v in load().items()}
# inputs of the function block itself (MET GEN-09 / PM-03); ListenerID depends on the ProcessingMode
# (VAL-PM); numbers of tool, frame, load, work area, conveyor are limited by the RC configuration (SDK-RANGE)
NOT_PARCMD = {
    "Execute",
    "Enable",
    "Name",
    "AxesGroup",
    "ProcessingMode",
    "SequenceFlag",
    "AbortingMode",
    "ListenerID",
}
NUMBERS = re.compile(r"(Tool|Frame|Load|WorkArea|Conveyor|Reference)No$")
INTEGER_TYPES = {"USINT": (0, 255), "SINT": (-128, 127), "UINT": (0, 65535), "INT": (-32768, 32767)}
_F142 = "LIB-BUG F142: the check of PositionsArray[x].E2 tests E1, an invalid E2 is sent"
_F143 = "LIB-BUG F143: BlendingParameter is not checked, an invalid value is sent"
_F144 = "LIB-BUG F144: RotationAngle is not checked, an invalid value is sent"
_F145 = "LIB-BUG F145: the limits of the external axes are not checked, an invalid value is sent"
_UNCHECKED = (
    [("MC_CalculateToolFB", f"PositionsArray[{i}].E2", _F142) for i in range(6)]
    + [
        (f"MC_MovePickPlace{k}FB", f"BlendingParameter[{i}]", _F143)
        for k in ("Direct", "Linear")
        for i in (0, 1)
    ]
    + [("MC_ShiftPositionFB", "RotationAngle", _F144)]
    + [
        ("MC_WriteWorkAreaFB", f"WorkAreaData.E{i}Limit.{b}Limit", _F145)
        for i in range(1, 7)
        for b in ("Lower", "Upper")
    ]
)
KNOWN: dict[tuple[str, str, str], str] = {
    (test, name, path): reason for name, path, reason in _UNCHECKED for test in ("nan",)
}


def _spec(name: str) -> list[dict[str, Any]]:
    return SPEC.get(name[3:-2].lower(), [])


def _set(fb: Any, path: str, value: Any) -> None:
    for p, _, owner, key in leaves(fb.ParCmd):
        if p == path:
            if isinstance(key, int):
                list.__setitem__(owner, key, value) if isinstance(owner, list) else owner.__setitem__(
                    key, value
                )
            else:
                setattr(owner, key, value)
            return
    raise KeyError(path)


def _run(name: str, path: str, value: Any) -> tuple[Any, int]:
    """Executes ``name`` with ``path`` = ``value``; returns the block and the commands the SDK accepted."""
    with robot() as (sim, h):
        fb = block(name, h)
        _set(fb, path, value)
        start_log = len(sim.logs)
        start(fb)
        h.run(100, until=lambda: finished(fb))
        return fb, commands(sim, cmd_type(name), start_log)


def _params(test: str, cases: list[tuple[Any, ...]]) -> list[Any]:
    """Test parameters; the known deviations are strict ``xfail``."""
    return [
        pytest.param(*c, marks=pytest.mark.xfail(strict=True, reason=KNOWN[(test, c[0], c[1])]))
        if (test, c[0], c[1]) in KNOWN
        else pytest.param(*c)
        for c in cases
    ]


# ------------------------------------------------------------------ REAL parameters


def _reals() -> list[tuple[Any, ...]]:
    result: list[tuple[Any, ...]] = []
    for name in NAMES:
        for path, value, _, _ in leaves(CLASSES[name]().ParCmd):
            if isinstance(value, float):
                result.append((name, path))
    return result


REALS = _reals()


@pytest.mark.parametrize(("name", "path"), _params("nan", REALS))
def test_real_not_a_number(name: str, path: str) -> None:
    """A REAL parameter that is not a number (NaN) is rejected by the client: Error, nothing is sent."""
    fb, sent = _run(name, path, math.nan)
    assert fb.Error and fb.ErrorID != 0 and sent == 0, (outputs(fb), sent)


# ------------------------------------------------------------------ listed values and ranges


# typing errors of the specification: (function, parameter) -> values the text means
SPEC_ERRATA: dict[tuple[str, str], list[int]] = {
    ("SoftSwitchTcp", "LimitMode"): [1],  # "• 0: No limit defined", then again "• 0: Limit defined"
}
OPEN_VALUE = {"positive": 1, "non_negative": 0, "negative": -1}


def _scalar_parameters() -> list[tuple[str, str, dict[str, Any]]]:
    """(block, ParCmd path, spec row) of the scalar integer parameters with listed values or ranges."""
    result = []
    for name in NAMES:
        paths = {p: v for p, v, _, _ in leaves(CLASSES[name]().ParCmd)}
        for row in _spec(name):
            if row["name"] in NOT_PARCMD or NUMBERS.search(row["name"]) or row["type"] not in INTEGER_TYPES:
                continue
            value = paths.get(row["name"])
            if value is None or isinstance(value, bool | float):
                continue
            row = dict(row, values=sorted({*row["values"], *SPEC_ERRATA.get((name[3:-2], row["name"]), [])}))
            if row["values"] or row["ranges"] or row["open"] or row["invalid"]:
                result.append((name, row["name"], row))
    return result


SCALARS = _scalar_parameters()


def _accepted_values() -> list[tuple[Any, ...]]:
    """Listed values, the bounds of the ranges and the smallest value of an open range ("• >0: ...")."""
    result = []
    for name, path, row in SCALARS:
        low, high = INTEGER_TYPES[row["type"]]
        values = set(row["values"]) | {OPEN_VALUE[o] for o in row["open"]}
        for a, b in row["ranges"]:
            values |= {a, b}
        result += [(name, path, v) for v in sorted(values - set(row["invalid"])) if low <= v <= high]
    return result


def _rejected_values() -> list[tuple[Any, ...]]:
    """Values the specification marks as invalid ("• 0: Undefined") and the value above every listed
    value and range when no open range ("• >0: ...") continues upwards."""
    result = []
    for name, path, row in SCALARS:
        low, high = INTEGER_TYPES[row["type"]]
        values = set(row["invalid"])
        listed = [*row["values"], *row["invalid"], *(b for _, b in row["ranges"])]
        if listed and not {"positive", "non_negative"} & set(row["open"]) and max(listed) + 1 <= high:
            values.add(max(listed) + 1)
        result += [(name, path, v) for v in sorted(values) if low <= v <= high]
    return result


@pytest.mark.parametrize(("name", "path", "value"), _params("accepted", _accepted_values()))
def test_specified_value_is_sent(name: str, path: str, value: int) -> None:
    """A value the specification lists for the parameter (or a bound of its range) is sent to the RC."""
    fb, sent = _run(name, path, value)
    assert sent >= 1, (outputs(fb), sent)


@pytest.mark.parametrize(("name", "path", "value"), _params("rejected", _rejected_values()))
def test_value_outside_the_specification_is_an_error(name: str, path: str, value: int) -> None:
    """A value the specification marks as invalid, or above its values and ranges, ends with Error (client or RC)."""
    fb, sent = _run(name, path, value)
    assert fb.Error and fb.ErrorID != 0, (outputs(fb), sent)
