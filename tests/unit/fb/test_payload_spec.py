"""Payload of every function block against the payload tables of the specification V1.5.9.

``tools.payload_check`` records the ``Add*`` / ``Get*`` calls of ``CreateCommandPayload`` and
``ParseResponsePayload`` and compares offsets, sizes and kinds of values with the tables in
``tools/spec_tables/spec_payload_tables.json``. All payloads match except the known
deviations below (docs/ST_FINDINGS.md). When the PLC library is fixed, the entry has to be
removed here - the test fails for fixed entries as well.
"""

from __future__ import annotations

import pytest

from tools.payload_check import Call, compare, fb_classes, function_name, report, send_calls
from tools.spec_tables import Entry, PayloadTable, load_command_types

NO_TABLE = "no payload table in the specification (cyclic data / not specified)"

KNOWN: dict[str, str] = {
    # errors or inconsistencies in the specification (the library follows the other tables)
    "MC_SyncToConveyorFB send": "spec: EmitterID as USINT in table 6-474 (SINT in all other tables)",
    "MC_MoveSuperImposedDynamicFB send": "spec: table 6-492 lacks Offset.RZ (byte numbers inconsistent)",
    "MC_WaitForTriggerFB send": "spec: ConditionalWait is BOOL in the interface, SINT in the table - same values",
    # no table
    "MC_ReadActualPositionCyclicFB send": NO_TABLE,
    "MC_ReadActualPositionCyclicFB recv": NO_TABLE,
    "MC_ReadCallSubprogramCyclicFB send": NO_TABLE,
    "MC_ReadCallSubprogramCyclicFB recv": NO_TABLE,
    "MC_WriteCallSubprogramCyclicFB send": NO_TABLE,
    "MC_WriteCallSubprogramCyclicFB recv": NO_TABLE,
    "MC_SoftSwitchTcpFB send": NO_TABLE,
    "MC_SoftSwitchTcpFB recv": NO_TABLE,
}  # F32/F33/F34 fixed (ST-FIX in tools/st2py/config.py)

CORE = (
    "MC_GroupResetFB",
    "MC_EnableRobotFB",
    "MC_ReadRobotDataFB",
    "MC_ChangeSpeedOverrideFB",
    "MC_GroupInterruptFB",
    "MC_GroupContinueFB",
    "MC_ReadActualPositionFB",
    "MC_MoveAxesAbsoluteFB",
    "MC_MoveDirectAbsoluteFB",
    "MC_MoveLinearAbsoluteFB",
    "MC_GroupJogFB",
    "MC_ReturnToPrimaryFB",
    "MC_SetSequenceFB",
    "MC_ReadToolDataFB",
    "MC_WriteToolDataFB",
    "MC_ReadFrameDataFB",
    "MC_WriteFrameDataFB",
    "MC_ReadLoadDataFB",
    "MC_WriteLoadDataFB",
    "MC_WriteRobotSWLimitsFB",
    "MC_ReadRobotDefaultDynamicsFB",
    "MC_WriteRobotDefaultDynamicsFB",
    "MC_ReadRobotReferenceDynamicsFB",
    "MC_WriteRobotReferenceDynamicsFB",
)


@pytest.fixture(scope="module")
def result() -> dict[str, list[str]]:
    return report()


def test_all_function_blocks_are_checked(result: dict[str, list[str]]) -> None:
    assert len(result) >= 220


def test_payloads_match_the_specification(result: dict[str, list[str]]) -> None:
    deviations = {key for key, problems in result.items() if problems}
    assert sorted(deviations - KNOWN.keys()) == [], "new deviations (see tools.payload_check)"
    assert sorted(KNOWN.keys() - deviations) == [], "fixed - remove from KNOWN and docs/ST_FINDINGS.md"


@pytest.mark.parametrize("fb", CORE)
def test_core_function_blocks_match(result: dict[str, list[str]], fb: str) -> None:
    for direction in ("send", "recv"):
        assert result[f"{fb} {direction}"] == []


# FBs whose command type is not a function of chapter 6 (cyclic data) or whose payload cannot
# be built (F33: spline FBs write past the payload buffer)
NO_COMMAND_TYPE = {
    "MC_ReadActualPositionCyclicFB",
    "MC_ReadCallSubprogramCyclicFB",
    "MC_WriteCallSubprogramCyclicFB",
    "MC_CreateSplineFB",
    "MC_DynamicSplineFB",
}


def test_command_types_match_the_specification() -> None:
    """ST-FIX F35: MoveLinearAbsoluteJ was sent as MoveLinearAbsolute, SoftSwitchTcp as
    ShiftPosition, MoveCircularAbsolute/Relative with the numbers of an older draft."""
    spec = {name.lower(): value for name, value in load_command_types().items()}
    wrong = {}
    for name, cls in fb_classes():
        if not hasattr(cls, "CreateCommandPayload") or name in NO_COMMAND_TYPE:
            continue
        sent = int(send_calls(cls)[0].value)
        expected = spec.get(function_name(name).lower())
        if sent != expected:
            wrong[name] = (sent, expected)
    assert wrong == {}


# ---------------------------------------------------------------- the checker itself


TABLE = PayloadTable(
    "x",
    "send",
    "Test",
    [
        Entry(0, "UINT", ["Type"]),
        Entry(2, "USINT", ["A"]),
        Entry(3, "REAL", ["B"]),
        Entry(7, "CHAR", ["S[0]"]),
        Entry(8, "CHAR", ["S[1]"]),
    ],
)


def test_compare_equal() -> None:
    calls = [Call(0, "AddUint", 2), Call(2, "AddUsint", 1), Call(3, "AddReal", 4), Call(7, "AddString", 2)]
    assert compare(calls, TABLE) == []


def test_compare_detects_shift_kind_length_and_strings() -> None:
    shifted = [Call(0, "AddUint", 2), Call(2, "AddUint", 2), Call(4, "AddReal", 4)]
    assert any("size 2" in p for p in compare(shifted, TABLE))
    wrong_kind = [
        Call(0, "AddUint", 2),
        Call(2, "AddSint", 1),
        Call(3, "AddReal", 4),
        Call(7, "AddString", 2),
    ]
    assert compare(wrong_kind, TABLE) == ["AddSint@2: Sint but table USINT A"]
    short_string = [
        Call(0, "AddUint", 2),
        Call(2, "AddUsint", 1),
        Call(3, "AddReal", 4),
        Call(7, "AddString", 1),
    ]
    assert compare(short_string, TABLE)[0] == "AddString@7: 1 bytes, table S has 2"


def test_sdk_fields_from_the_pattern() -> None:
    from srci.sim.sdk import layout_pattern
    from tools.payload_check import compare_sdk, sdk_fields

    host = [layout_pattern(i) for i in range(9)]
    # structure: UINT (0..1), USINT (2), REAL (3..6), 2 BYTE (7, 8) -> wire order reversed per field
    wire = bytes(host[1::-1] + host[2:3] + host[6:2:-1] + host[7:9])
    fields = sdk_fields(wire, layout_pattern)
    assert fields == [(0, 2), (2, 1), (3, 4), (7, 1), (8, 1)]
    ok = [
        Call(0, "AddUint", 2),
        Call(2, "AddUsint", 1),
        Call(3, "AddReal", 4),
        Call(7, "AddByte", 1),
        Call(8, "AddByte", 1),
    ]
    assert compare_sdk(ok, fields) == []
    shifted = [Call(0, "AddUint", 2), Call(2, "AddUint", 2), Call(4, "AddReal", 4)]
    problems = compare_sdk(shifted, fields)
    assert "AddUint@2 (2 bytes): SDK field 1 bytes at 2" in problems
    assert "payload length 8, SDK structure 9" in problems
