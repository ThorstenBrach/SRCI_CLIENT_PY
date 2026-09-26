"""Interface of every function block against the specification (methodology "General FB",
Siemens test case x-02 "Compare the inputs and outputs in the specification with the
in/outputs of the function block").

The inputs/outputs of chapter 6 ("Associated command/response values - Application Layer",
``tools/spec_tables``) must exist in the function block: as input / output of the block or as
field of ``ParCmd`` / ``OutCmd``. Known differences are finding F45 (docs/ST_FINDINGS.md).
"""

from __future__ import annotations

import dataclasses
import inspect

import pytest

from tools.payload_check import fb_classes, function_name
from tools.spec_tables import load_interfaces

# names of the specification -> names of the PLC library
ALIAS = {"AbortingMode": "ExecMode", "Time": "MoveTime"}

# F45: parameters of the specification that the function block does not have
KNOWN_MISSING: dict[str, str] = {
    "MC_CallSubprogramFB": "output Progress",
    "MC_MeasuringInputFB": "outputs CommandAborted, ToolNo_x/FrameNo_x/MeasuredJointPosition_x (OutCmd.Measurings)",
    "MC_GroupStopFB": "output Active",
    "MC_SetSequenceFB": "output Active",
    "MC_ReturnToPrimaryFB": "input Limit (DistanceLimit)",
    "MC_CalculateForwardKinematicFB": "outputs ToolNoReturn, FrameNoReturn (TargetToolNoReturn/...)",
    "MC_CalculateFrameFB": "output FrameData (IEC_Date, ..., Position)",
    "MC_ActivateConveyorTrackingFB": "output TrackingStatusByte (TrackingStatus bits)",
    "MC_RedefineTrackingPosFB": "input StartIndexInit (StartIndexInitPosition)",
    "MC_ForceLimitFB": "input Limit (ForceLimit)",
    "MC_RobotTaskFB": "inputs SoftwareLimits (SWLimits), SystemLogRingBuffer",
    "MC_ReadActualPositionFB": "inputs Enable, ReadCartesianPosition, ReadJointPosition, ReadExtJointPosition; output Position",
    "MC_ReadActualPositionCyclicFB": "outputs ReadingExtJointPosition, ExtCartesianPosition, ExtJointPosition",
    "MC_ReadDHParameterFB": "outputs DHParameterAlpha/A/D/Theta, PositiveJointDirection, JointZeroPosition (DHParameter)",
    "MC_ReadRealsFB": "output ParameterAccepted",
    "MC_DynamicSplineFB": "input Enable (the block has Execute), output RemainingSegment",
    "MC_SetTriggerLimitFB": "output Data",
    "MC_SetTriggerRegisterFB": "inputs IntValue_1/_2, RealValue_1/_2 (arrays IntValue/RealValue)",
    "MC_WaitTimeFB": "input Time (WaitTime)",
    "MC_ReadWorkAreaFB": "outputs WorkAreaNo, Data (WorkAreaNoReturn, WorkAreaData)",
    "MC_WriteWorkAreaFB": "input Data (WorkAreaData)",
    "MC_WriteRobotSWLimitsFB": "input ResetToFactory (ResetToFactoryDefaults)",
}

# function blocks without an interface table in the specification
NO_TABLE = {
    "MC_ExchangeConfigurationFB",
    "MC_ReadMessagesFB",
    "MC_ReadRobotDataFB",
    "MC_SoftSwitchTcpFB",
    "MC_ReadCallSubprogramCyclicFB",
}


def _interface(cls: type) -> tuple[set[str], set[str], set[str]]:
    """(inputs incl. ParCmd fields, outputs incl. OutCmd fields, ParCmd fields) of a block."""
    fb = cls()
    names = {k for k in vars(fb) if k[:1].isupper()}
    inputs = (set(inspect.signature(cls.__call__).parameters) - {"self"}) | names
    par = {f.name for f in dataclasses.fields(fb.ParCmd)} if hasattr(fb, "ParCmd") else set()
    out = {f.name for f in dataclasses.fields(fb.OutCmd)} if hasattr(fb, "OutCmd") else set()
    return inputs | par, names | out, par


def missing(name: str, cls: type) -> list[str]:
    spec = load_interfaces()[function_name(name)]
    inputs, outputs, _ = _interface(cls)
    miss = [f"input {r[0]}" for r in spec["inputs"] if ALIAS.get(r[0], r[0]) not in inputs]
    miss += [f"output {r[0]}" for r in spec["outputs"] if r[0] not in outputs]
    return miss


def extra(name: str, cls: type) -> list[str]:
    """ParCmd fields without an input of the specification (information, finding F39)."""
    spec = load_interfaces()[function_name(name)]
    names = {ALIAS.get(r[0], r[0]) for r in spec["inputs"]}
    return sorted(p for p in _interface(cls)[2] if p not in names)


CLASSES = dict(fb_classes())


@pytest.mark.parametrize("name", sorted(CLASSES))
def test_interface_matches_the_specification(name: str) -> None:
    """GEN-01: every input/output of the specification exists in the function block."""
    if name in NO_TABLE:
        pytest.skip("no interface table in the specification")
    if name in KNOWN_MISSING:
        pytest.xfail(f"F45: {KNOWN_MISSING[name]}")
    assert missing(name, CLASSES[name]) == []


def test_all_function_blocks_have_a_table() -> None:
    spec = load_interfaces()
    without = {n for n in CLASSES if function_name(n) not in spec}
    assert without == NO_TABLE


# F46: fields of ParCmd/OutCmd without a comment in the PLC library
UNDOCUMENTED: set[tuple[str, str]] = set()  # F46 fixed (comments added by override)


def test_parameters_are_documented() -> None:
    """GEN-03 (Siemens x-04 "all parameters have a valid and useful comment"): every field of
    ParCmd/OutCmd has a comment (taken from the PLC library into the generated types)."""
    import ast
    from pathlib import Path

    import srci.types._generated.structs as structs

    tree = ast.parse(Path(structs.__file__).read_text(encoding="utf-8"))
    found = set()
    count = 0
    for node in tree.body:
        if not (isinstance(node, ast.ClassDef) and node.name.endswith(("ParCmd", "OutCmd"))):
            continue
        for i, stmt in enumerate(node.body):
            if (
                isinstance(stmt, ast.AnnAssign)
                and isinstance(stmt.target, ast.Name)
                and stmt.target.id[0] != "_"
            ):
                count += 1
                doc = node.body[i + 1] if i + 1 < len(node.body) else None
                if not (
                    isinstance(doc, ast.Expr)
                    and isinstance(doc.value, ast.Constant)
                    and len(str(doc.value.value).strip()) > 3
                ):
                    found.add((node.name, stmt.target.id))
    assert count > 900
    assert found == UNDOCUMENTED
