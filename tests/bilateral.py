"""Bilateral tests: values sent by a function block as the SDK decodes them, and values set in
the SDK as the function block outputs them.

The SDK harness decodes every received command with the payload tables of the specification
(``SdkSimulator.last_command``) and answers the commands the SDK does not implement with
values set by the test (``SdkSimulator.set_response``). This module fills ``ParCmd`` with
distinct valid values, maps the leaves of ``ParCmd`` / ``OutCmd`` to the field names of the
specification and compares the values with the conversions of the telegram: percent * 100,
optional -1.0 -> 16#FFFF, BOOL -> 0/1, enums -> numbers, ArmConfig -> bits, turn numbers ->
sign + magnitude half bytes (spec 5.5.4.4).
"""

from __future__ import annotations

import dataclasses
import enum
import math
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

# name of a path segment in ParCmd/OutCmd -> name in the specification (both normalised)
ALIASES = {
    "movetime": "time",
    "waittime": "time",
    "toolnoreturn": "toolno",
    "framenoreturn": "frameno",
    "loadnoreturn": "loadno",
    "resettofactorydefaults": "resettofactorydefault",
    "messagecodes": "messagecode",
    "toolsinsync": "tooldatainsyncclient",
    "framesinsync": "framedatainsyncclient",
    "loadsinsync": "loaddatainsyncclient",
    "workareasinsync": "workareadatainsyncclient",
    "softwarelimitsinsync": "swlimitsinsyncclient",
    "defaultdynamicsinsync": "defaultdynamicsinsyncclient",
    "referencedynamicsinsync": "referencedynamicsinsyncclient",
}

# path segments that are not compared: trigger IDs (would make the command wait for a trigger),
# HighPriority (sent as Priority of the header)
NOT_COMPARED = ("emitterid", "listenerid", "highpriority")

# enum values that make the parameter check of the function block fail or change the behaviour
KEEP_DEFAULT = ("sequenceflag", "processingmode", "conveyortype")
ENUM_VALUE = {"operationmode": "T1_EXT"}
# integers that are enum values in the specification (typed USINT in the PLC library)
INT_VALUE = {"unitlimitaxis": 2}

# ArmConfig: the telegram has one bit per element (spec 5.5.4.3): TRUE for BACK / DOWN / FLIP
ARM_CONFIG_BIT = {"ArmConfigShoulder": "BACK", "ArmConfigElbow": "DOWN", "ArmConfigWrist": "FLIP"}

TURNS = ("J1Turns", "J2Turns", "J3Turns", "J4Turns", "J5Turns", "J6Turns", "E1Turns")


def _segment(seg: str) -> str:
    s = seg.lower().replace("_", "")
    s = s.replace("timestampiecdate", "date").replace("timestampiectime", "time")
    base, bracket, index = s.partition("[")
    return ALIASES.get(base, base) + bracket + index


def normalise(path: str) -> str:
    parts = [p for p in re.split(r"\.", path) if p]
    parts = [
        p.replace("Timestamp", "").replace("IEC_DATE", "Date").replace("IEC_TIME", "Time") for p in parts
    ]
    return "".join(_segment(p) for p in parts if p)


def leaves(value: Any, prefix: str = "") -> Iterator[tuple[str, Any, Any, str | int]]:
    """(path, value, owner, key) of all scalar leaves of a structure."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        for f in dataclasses.fields(value):
            yield from _leaf(getattr(value, f.name), f"{prefix}{f.name}", value, f.name)
    elif isinstance(value, list | bytearray):
        for i, item in enumerate(value):
            yield from _leaf(item, f"{prefix}[{i}]", value, i)


def _leaf(v: Any, path: str, owner: Any, key: str | int) -> Iterator[tuple[str, Any, Any, str | int]]:
    if (dataclasses.is_dataclass(v) and not isinstance(v, type)) or isinstance(v, list | bytearray):
        sep = "" if isinstance(v, list | bytearray) else "."
        yield from leaves(v, path + sep)
    else:
        yield path, v, owner, key


def _set(owner: Any, key: str | int, value: Any) -> None:
    if isinstance(key, int):  # position in the list (IecArray: independent of the lower bound)
        if isinstance(owner, list):
            list.__setitem__(owner, key, value)
        else:
            owner[key] = value
    else:
        setattr(owner, key, value)


def distinct_values(parcmd: Any) -> dict[str, Any]:
    """Fills ``parcmd`` with distinct, valid values; returns path -> value set."""
    chosen: dict[str, Any] = {}
    k = 0
    for path, value, owner, key in leaves(parcmd):
        name = path.lower()
        norm = normalise(path)
        if any(x in norm for x in NOT_COMPARED):
            continue
        k += 1
        new: Any = value
        if isinstance(value, bool):
            # only axes the simulated robot has (J1..J6, E1); GroupJog: one direction only
            if re.search(r"axise[2-6]|bit0\d|\.e[2-6]$", name) or (".control." in f".{name}" and k % 4):
                new = False
            else:
                new = True
        elif isinstance(value, enum.IntEnum):
            members = list(type(value))
            last = norm.rsplit("]", 1)[-1]
            bit = ARM_CONFIG_BIT.get(type(value).__name__)
            if any(last.endswith(x) for x in KEEP_DEFAULT):
                new = value
            elif any(last.endswith(x) for x in ENUM_VALUE):
                new = type(value)[next(v for x, v in ENUM_VALUE.items() if last.endswith(x))]
            elif bit is not None:
                new = type(value)[bit]
            else:
                new = members[1] if len(members) > 1 else value  # the second value of the enum
        elif isinstance(value, int):
            if any(norm.endswith(x) for x in INT_VALUE):
                new = next(v for x, v in INT_VALUE.items() if norm.endswith(x))
            elif name.endswith("turns"):  # sign + magnitude, -7..7
                new = -(1 + k % 6) if k % 2 else 1 + k % 6
            elif name.endswith(("toolno", "frameno", "loadno", "conveyorno")):
                new = 1 + k % 15
            elif name.endswith("workareano"):
                new = 1
            elif "index" in name or name.endswith("no") or "id" in name:
                new = 1 + k % 7
            elif "time" in name:
                new = 100 + 10 * k
            else:
                new = 1 + k % 100
        elif isinstance(value, float):
            new = float(10 + k % 80) + 0.5 if "rate" in name or "override" in name else 1.25 + k
        elif isinstance(value, str):
            new = f"T{k}"
        else:
            continue
        _set(owner, key, new)
        chosen[path] = new
    return chosen


def _turn_byte(turns: int, bits: int = 3) -> int:
    return (abs(turns) & ((1 << bits) - 1)) | ((1 << bits) if turns < 0 else 0)


def turn_number_bytes(t: dict[str, int]) -> list[int]:
    """TurnNumber (J1Turns..E1Turns) as the 4 bytes of the telegram (spec 5.5.4.4)."""
    j = [_turn_byte(t.get(n, 0)) for n in TURNS[:6]]
    # bit 0..3: J1, bit 4..7: J2, ... (table 5-24)
    return [(j[1] << 4) | j[0], (j[3] << 4) | j[2], (j[5] << 4) | j[4], _turn_byte(t.get("E1Turns", 0), 7)]


def expected_text(value: Any, sdk_text: str, path: str = "") -> bool:
    """``value`` (ParCmd/OutCmd) equals the SDK value ``sdk_text`` (with telegram conversions)."""
    if path.lower().endswith("override") and isinstance(value, int) and sdk_text == str(value * 100):
        return True  # INT percent -> factor 100
    if isinstance(value, enum.IntEnum) and type(value).__name__ in ARM_CONFIG_BIT:
        return sdk_text == ("1" if value.name == ARM_CONFIG_BIT[type(value).__name__] else "0")
    if isinstance(value, bool):
        return sdk_text in ("1", "true") if value else sdk_text in ("0", "false")
    if isinstance(value, str):
        return sdk_text == value
    try:
        sdk = float(sdk_text)
    except ValueError:
        return False
    v = float(value)
    if math.isclose(sdk, v, rel_tol=1e-6, abs_tol=1e-6):
        return True
    # percent values: REAL -> UINT/INT *100, -1.0 -> 16#FFFF
    return isinstance(value, float) and (sdk == round(v * 100) or (v == -1.0 and sdk == 65535))


@dataclass
class Comparison:
    matched: list[str] = field(default_factory=list)
    mismatched: list[str] = field(default_factory=list)  # "path: sent x, SDK y"
    missing: list[str] = field(default_factory=list)  # leaves without a field in the SDK decoding

    @property
    def ok(self) -> bool:
        return not self.mismatched and not self.missing


def _find(key: str, by_name: dict[str, tuple[str, str]]) -> tuple[str, str] | None:
    hit = by_name.get(key)
    if hit is not None:
        return hit
    # arrays of the ParCmd ("IntValue[0]") are single fields in the spec ("IntValue_1")
    m = re.fullmatch(r"(.*)\[(\d+)\]", key)
    if m and (hit := by_name.get(f"{m.group(1)}{int(m.group(2)) + 1}")) is not None:
        return hit
    # structure names that the spec leaves out ("DataEnableSync.EnableSyncTool" -> "EnableSyncTool")
    candidates = [n for n in by_name if key.endswith(n) and len(n) >= 4]
    return by_name[max(candidates, key=len)] if candidates else None


def compare_fields(values: dict[str, Any], sdk: dict[str, str]) -> Comparison:
    by_name = {normalise(n): (n, v) for n, v in sdk.items()}
    result = Comparison()
    turns: dict[str, dict[str, int]] = {}
    # structures of BOOLs sent as one byte ("RobotAxesActive": Bit00, AxisJ1, ...)
    packed: dict[str, list[tuple[str, bool]]] = {}
    for path, value in values.items():
        prefix = path.rpartition(".")[0]
        if isinstance(value, bool) and prefix and normalise(prefix) in by_name:
            packed.setdefault(prefix, []).append((path, value))
    for prefix, bits in packed.items():
        byte = sum(1 << i for i, (_, v) in enumerate(bits) if v)
        name, text = by_name[normalise(prefix)]
        (result.matched if int(float(text)) == byte else result.mismatched).append(
            prefix if int(float(text)) == byte else f"{prefix}: {byte}, SDK {name}={text}"
        )
        for path, _ in bits:
            values = {k: v for k, v in values.items() if k != path}
    for path, value in values.items():
        prefix, _, last = path.rpartition(".")
        if last in TURNS and prefix.endswith("TurnNumber"):
            turns.setdefault(prefix, {})[last] = value
            continue
        hit = _find(normalise(path), by_name)
        if hit is None:
            result.missing.append(path)
        elif expected_text(value, hit[1], path):
            result.matched.append(path)
        else:
            result.mismatched.append(f"{path}: {value!r}, SDK {hit[0]}={hit[1]}")
    for prefix, t in turns.items():
        for i, byte in enumerate(turn_number_bytes(t)):
            hit = _find(normalise(f"{prefix}[{i}]"), by_name)
            if hit is None:
                result.missing.append(f"{prefix}[{i}]")
            elif int(float(hit[1])) == byte:
                result.matched.append(f"{prefix}[{i}]")
            else:
                result.mismatched.append(f"{prefix}[{i}]: {byte}, SDK {hit[0]}={hit[1]} ({t})")
    return result


# data types of the specification tables -> test values for the responses of the SDK
_INT_RANGE = {
    "SINT": (-100, 100),
    "USINT": (1, 200),
    "INT": (-3000, 3000),
    "UINT": (1, 60000),
    "DINT": (-100000, 100000),
    "UDINT": (1, 1000000),
    "BYTE": (1, 200),
    "WORD": (1, 60000),
    "DWORD": (1, 1000000),
    "DATE": (1, 20000),
    "TIME": (1, 100000),
    "TIME_OF_DAY": (1, 86399999),
}


def response_values(entries: list[Any]) -> dict[str, object]:
    """Distinct values for the fields of a response table (header bytes 0..3 excluded)."""
    values: dict[str, object] = {}
    k = 0
    text: dict[str, int] = {}
    for e in entries:
        if e.offset < 4 or not e.names:
            continue
        names = [n for n in e.names if not n.startswith("Reserved")]
        if not names:
            continue
        k += 1
        if e.type == "CHAR":
            base = e.names[0].split("[")[0]
            text[base] = text.get(base, 0) + 1
            continue
        if e.type in ("BYTE", "BOOL") and len(e.names) > 1:
            if {"Shoulder", "Elbow", "Wrist"} & set(e.names):
                continue  # ArmConfig: bit names repeat for every position of a response
            for i, n in enumerate(e.names):
                if not n.startswith("Reserved"):
                    values[n] = (k + i) % 2  # alternating bits
            continue
        if e.type == "USINT" and len(e.names) == 2:
            continue  # half bytes (header-like), not used in responses of commands
        if "TurnNumber[" in names[0]:
            # sign + magnitude without "-0" (not representable in the PLC library, F11)
            low_nibble, high_nibble = 1 + k % 7, 9 + (k + 3) % 7
            values[names[0]] = (1 + k % 60) if names[0].endswith("[3]") else (high_nibble << 4) | low_nibble
        elif e.type in ("REAL", "LREAL"):
            values[names[0]] = 0.25 + k
        else:
            low, high = _INT_RANGE.get(e.type, (1, 200))
            values[names[0]] = low + (k * 7) % (high - low)
    for base, size in text.items():
        values[base] = ("R" + "abcdefghij" * 30)[: min(size, 12)]
    return values
