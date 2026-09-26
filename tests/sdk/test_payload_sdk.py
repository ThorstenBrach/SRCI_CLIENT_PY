"""Payload of the function blocks against the structures of the SRCI SDK.

The SDK copies a command payload into a packed C++ structure (``deserializeCommand<CMD::X>``)
and a response structure into the payload (``serializeResponse``). ``srci_sim_layout`` fills
these structures with a byte pattern and converts them like the SDK; multi-byte fields
appear reversed, which gives the exact field layout of the SDK (``tools.payload_check``).
Every ``Add*`` / ``Get*`` call of a function block must match it.
"""

from __future__ import annotations

import pytest

from srci.sim.sdk import SdkSimulator, layout_pattern, sdk_layout
from tools.payload_check import compare_sdk, fb_classes, recv_calls, sdk_fields, send_calls

# known differences (docs/ST_FINDINGS.md)
KNOWN = {  # F32 fixed
    "MC_ExchangeConfigurationFB recv": "SDK: NumberOfServerLogs (spec bytes 28..29) not in the SDK structure",
    "MC_ReadActualPositionFB recv": "SDK: 2 reserved bytes before the extended axes (not in the spec)",
}

SKIP: set[str] = set()  # F33 fixed: one spline point per command


def _cases() -> list[tuple[str, type]]:
    return [(n, c) for n, c in fb_classes() if hasattr(c, "CreateCommandPayload") and n not in SKIP]


def _result(name: str, cls: type) -> dict[str, list[str]]:
    sent = send_calls(cls)
    cmd_type = int(sent[0].value)
    result: dict[str, list[str]] = {}
    for direction, calls in (("send", sent), ("recv", recv_calls(cls))):
        wire = sdk_layout(cmd_type, direction == "recv")
        if wire is not None:  # the SDK has a structure for this command
            result[f"{name} {direction}"] = compare_sdk(calls, sdk_fields(wire, layout_pattern))
    return result


@pytest.fixture(scope="module")
def results(sdk_library: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for name, cls in _cases():
        out.update(_result(name, cls))
    return out


def test_sdk_structures_are_checked(results: dict[str, list[str]]) -> None:
    # 20 command and 20 response structures, some commands have several function blocks
    assert len(results) >= 38


def test_payloads_match_the_sdk(results: dict[str, list[str]]) -> None:
    deviations = {key: problems for key, problems in results.items() if problems}
    new = {k: v for k, v in deviations.items() if k not in KNOWN}
    assert new == {}, "new deviations from the SDK structures"
    assert sorted(KNOWN.keys() - deviations.keys()) == [], "fixed - remove from KNOWN"


def test_layout_of_a_known_structure(sdk: SdkSimulator) -> None:
    """MoveAxesAbsolute: header (type UINT, 2 half bytes), emitter/listener, 4 UINT rates, ..."""
    wire = sdk_layout(2101, response=False)
    assert wire is not None and len(wire) == 80
    fields = sdk_fields(wire, layout_pattern)
    assert fields[:4] == [(0, 2), (2, 1), (3, 1), (4, 1)]
    assert (10, 2) in fields and (28, 4) in fields  # VelocityRate, JointPosition.J1
