"""Compares the payload of every function block with the payload tables of the specification.

The ``Add*`` calls of ``CreateCommandPayload`` and the ``Get*`` calls of
``ParseResponsePayload`` are recorded (offset, method, size) and compared with the table
of the function in ``tools/spec_tables/spec_payload_tables.json``:

* every call must start at the offset of a table entry (or inside a CHAR/BYTE array),
* it must cover whole entries (size),
* the kind of value must match (REAL / signed / unsigned),
* the payload must have the length of the table.

    python -m tools.payload_check            # report of all function blocks
    python -m tools.payload_check MC_MoveAxesAbsoluteFB
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.spec_tables import Entry, PayloadTable, load

FB_ROOT = Path(__file__).resolve().parents[1] / "src" / "srci" / "fb"

SIGNED = {"SINT", "INT", "DINT", "LINT"}
REAL = {"REAL", "LREAL"}

# kind of value written/read by a method (None: any, e.g. bit fields / byte blocks)
METHOD_KIND: dict[str, str | None] = {
    "Real": "real",
    "Sint": "signed",
    "Int": "signed",
    "Dint": "signed",
    "Usint": "unsigned",
    "Uint": "unsigned",
    "Udint": "unsigned",
    "Byte": "unsigned",
    "Word": "unsigned",
    "Dword": "unsigned",
    "Bool": "unsigned",
    "HalfBytes": "unsigned",
    "HalfeByte2": "unsigned",
    "IecDate": "unsigned",
    "IecTime": "unsigned",
    "Time": "unsigned",
}


def kind(spec_type: str) -> str:
    if spec_type in REAL:
        return "real"
    if spec_type in SIGNED:
        return "signed"
    return "unsigned"


@dataclass
class Call:
    offset: int
    method: str
    size: int

    @property
    def kind(self) -> str | None:
        return METHOD_KIND.get(self.method[3:])


@contextmanager
def recording(cls: type, prefix: str) -> Iterator[list[Call]]:
    """Records the outermost ``prefix*`` method calls of ``cls`` instances."""
    calls: list[Call] = []
    depth = 0
    originals: dict[str, Callable[..., Any]] = {}
    for name in dir(cls):
        if not name.startswith(prefix) or not callable(getattr(cls, name)):
            continue
        original = getattr(cls, name)
        originals[name] = original

        def wrapper(self: Any, *args: Any, __name: str = name, __orig: Any = original, **kw: Any) -> Any:
            nonlocal depth
            start = self.PayloadPtr
            depth += 1
            try:
                return __orig(self, *args, **kw)
            finally:
                depth -= 1
                if depth == 0:
                    calls.append(Call(start, __name, self.PayloadPtr - start))

        setattr(cls, name, wrapper)
    try:
        yield calls
    finally:
        for name, original in originals.items():
            setattr(cls, name, original)


def fb_classes() -> Iterator[tuple[str, type]]:
    for path in sorted(FB_ROOT.rglob("MC_*FB.py")):
        module = importlib.import_module(".".join(path.relative_to(FB_ROOT.parents[1]).with_suffix("").parts))
        yield path.stem, getattr(module, path.stem)


def function_name(fb_name: str) -> str:
    return fb_name.removeprefix("MC_").removesuffix("FB")


def _fill_strings(obj: Any) -> None:
    for f in getattr(type(obj), "_IEC_FIELDS_", ()):
        value = getattr(obj, f.name)
        if isinstance(value, str):
            setattr(obj, f.name, "x")
        elif hasattr(type(value), "_IEC_FIELDS_"):
            _fill_strings(value)


def _array_end(table: PayloadTable, e: Entry) -> int:
    """End offset of the CHAR/BYTE array that starts with ``e`` (``X[0]``, ``X[1]``, ...)."""
    base = e.names[0].split("[")[0] if e.names else ""
    end = e.offset + e.size
    for x in table.entries:
        if x.offset == end and x.type == e.type and x.names and x.names[0].split("[")[0] == base:
            end += x.size
    return end


def send_calls(fb_cls: type) -> list[Call]:
    from srci.fb._internal.Send.RobotLibrarySendDataBaseFB import RobotLibrarySendDataBaseFB
    from srci.types import AxesGroup

    fb = fb_cls()
    for name in ("ParCmd", "_parCmd"):  # short strings reveal fields that are not padded
        if hasattr(fb, name):
            _fill_strings(getattr(fb, name))
    if hasattr(fb, "CheckAddParameter"):
        fb.CheckAddParameter = lambda **_: True  # complete payload
    with recording(RobotLibrarySendDataBaseFB, "Add") as calls:
        fb.CreateCommandPayload(AxesGroup=AxesGroup())
    return list(calls)


def recv_calls(fb_cls: type) -> list[Call]:
    from srci.fb._internal.Recv.RobotLibraryRecvDataBaseFB import RobotLibraryRecvDataBaseFB
    from srci.fb._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB

    fb = fb_cls()
    data = RobotLibraryResponseDataFB()
    data.PayloadLen = len(data.Payload)  # everything is "remaining"
    with recording(RobotLibraryRecvDataBaseFB, "Get") as calls:
        fb.ParseResponsePayload(ResponseData=data)
    # GetHalfeByte1(IncPayloadPtr=False) reads the byte of the next call
    return [c for c in calls if c.size > 0]


def compare(calls: list[Call], table: PayloadTable) -> list[str]:
    """Differences between the recorded calls and the table (empty: equal)."""
    problems: list[str] = []
    entries = {x.offset: x for x in table.entries}
    covered: dict[int, Entry] = {}
    for x in table.entries:
        for i in range(x.size):
            covered[x.offset + i] = x
    spec_end = max(x.offset + x.size for x in table.entries)
    for c in calls:
        if c.size == 0:
            continue
        label = f"{c.method}@{c.offset}"
        found = entries.get(c.offset)
        if found is None:
            inside = covered.get(c.offset)
            if inside is not None and inside.type in {"CHAR", "BYTE"}:
                continue  # inside a byte array
            where = (
                f"inside {inside.type} {'/'.join(inside.names)}@{inside.offset}"
                if inside
                else "not in the table"
            )
            problems.append(f"{label}: {where}")
            continue
        e = found
        # entries covered by the call
        end = c.offset + c.size
        span = [x for x in table.entries if c.offset <= x.offset < end]
        span_end = max(x.offset + x.size for x in span)
        if c.method.endswith(("DataBlock", "String")):
            array_end = _array_end(table, e)
            if e.names and e.names[0].endswith("[0]") and end != array_end:
                problems.append(
                    f"{label}: {c.size} bytes, table {'/'.join(e.names)[:-3]} has {array_end - c.offset}"
                )
            continue
        if span_end != end and e.type != "CHAR":
            problems.append(
                f"{label}: size {c.size}, table {e.type} {'/'.join(e.names)} ({span_end - c.offset})"
            )
            continue
        if (
            c.kind is not None
            and len(span) == 1
            and c.kind != kind(e.type)
            and e.type not in {"BYTE", "CHAR"}
        ):
            problems.append(f"{label}: {c.method[3:]} but table {e.type} {'/'.join(e.names)}")
    end = max((c.offset + c.size for c in calls), default=0)
    if end != spec_end:
        problems.append(f"payload length {end}, table {spec_end}")
    return problems


def report(only: set[str] | None = None) -> dict[str, list[str]]:
    tables = load()
    result: dict[str, list[str]] = {}
    for name, cls in fb_classes():
        if only and name not in only:
            continue
        func = function_name(name)
        for direction, get in (("send", send_calls), ("recv", recv_calls)):
            key = f"{name} {direction}"
            table = tables.get((func, direction))
            if not hasattr(cls, "CreateCommandPayload"):
                continue
            if table is None:
                result[key] = ["no table in the specification"]
                continue
            try:
                calls = get(cls)
            except Exception as exc:
                result[key] = [f"{type(exc).__name__}: {exc}"]
                continue
            result[key] = compare(calls, table)
    return result


def main() -> int:
    only = set(sys.argv[1:]) or None
    res = report(only)
    bad = {k: v for k, v in res.items() if v}
    for key, problems in bad.items():
        print(key)
        for p in problems:
            print("   ", p)
    print(f"{len(res) - len(bad)} of {len(res)} payloads match the specification")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())


def side_by_side(fb_name: str, direction: str) -> str:
    """Table entries and recorded calls next to each other (for the analysis of differences)."""
    cls = dict(fb_classes())[fb_name]
    table = load()[(function_name(fb_name), direction)]
    calls = {c.offset: c for c in (send_calls(cls) if direction == "send" else recv_calls(cls)) if c.size}
    rows = []
    offsets = sorted({e.offset for e in table.entries} | set(calls))
    by_offset = {e.offset: e for e in table.entries}
    for off in offsets:
        e = by_offset.get(off)
        c = calls.get(off)
        if (
            c is None
            and e is not None
            and e.type in {"CHAR", "BYTE"}
            and e.names
            and e.names[0].endswith("]")
            and not e.names[0].endswith("[0]")
        ):
            continue  # inside an array
        left = f"{e.type:<11} {'/'.join(e.names)[:40]}" if e else ""
        right = f"{c.method}({c.size})" if c else ""
        rows.append(f"{off:4} {left:<53} {right}")
    return f"{fb_name} {direction} (table {table.table})\n" + "\n".join(rows)
