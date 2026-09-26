"""Payload tables of the SRCI specification ("Sent/Received CMD payload ... of <function>").

Reads the text export of the specification PDF (``pdftotext -layout``) and returns every
payload table as a list of entries (byte offset, data type, parameter names). The tables
are the reference for the payload tests of the function blocks (tests/unit/fb/test_payload_spec.py).

The text export of the specification is *not* part of the repository (copyright PNO); the
result of this parser is stored in ``spec_payload_tables.json`` (only offsets, data types
and parameter names).

    python -m tools.spec_tables <spec.txt>       # writes tools/spec_tables/spec_payload_tables.json
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

JSON_PATH = Path(__file__).with_name("spec_payload_tables.json")

TYPE_SIZES = {
    "BOOL": 1,
    "BYTE": 1,
    "CHAR": 1,
    "SINT": 1,
    "USINT": 1,
    "INT": 2,
    "UINT": 2,
    "WORD": 2,
    "DATE": 2,
    "DINT": 4,
    "UDINT": 4,
    "DWORD": 4,
    "REAL": 4,
    "TIME": 4,
    "TIME_OF_DAY": 4,
    "LREAL": 8,
}

_CAPTION = re.compile(
    r'Table (\d+-\d+): (Sent|Received) CMD payload \((PLC to RC|RC to PLC)\) of\s+"([^"]+)"'
)
_ENTRY = re.compile(
    r"^\s+(\d{1,3})?\s+(" + "|".join(sorted(TYPE_SIZES, key=len, reverse=True)) + r")\b\s*(.*)$"
)
_BYTE_NO = re.compile(r"^\s+(\d{1,3})\s*$")
_NAME_ONLY = re.compile(r"^\s{12,}([A-Za-z][\w.\[\]]*(?:\s{2,}[A-Za-z][\w.\[\]]*)?)\s*$")
_END = re.compile(r"^\s*\d*\s*(Table \d+-\d+:|\d+\.\d+\.\d+(\.\d+)*\s+\S|NOTE\b)")
# captions with a wrong function name in the specification
CAPTION_FIXES = {"6-203": "ReadRobotSWLimits"}  # 6.2.19.5, caption says "WriteRobotSWLimits"
_NOISE = re.compile(r"Copyright PNO|^\s*Draft\s*$|Profile Standard Robot Command Interface|END of page")


@dataclass
class Entry:
    offset: int
    type: str
    names: list[str] = field(default_factory=list)

    @property
    def size(self) -> int:
        return TYPE_SIZES[self.type]


@dataclass
class PayloadTable:
    table: str
    direction: str  # "send" (PLC to RC) / "recv" (RC to PLC)
    function: str
    entries: list[Entry]


def _names(text: str) -> list[str]:
    return [n for n in re.split(r"\s{2,}", text.strip()) if n]


def parse_table(lines: list[str]) -> list[Entry]:
    entries: list[Entry] = []
    start: int | None = None  # first byte number since the last entry
    pending_names: list[str] = []  # bit names above a BYTE row
    bit_row = False  # the last entry is a BYTE with bit names printed above and below its row
    for line in lines:
        if _NOISE.search(line) or not line.strip() or "ByteNo" in line:
            continue
        if m := _ENTRY.match(line):
            no, typ, rest = m.groups()
            expected = entries[-1].offset + entries[-1].size if entries else 0
            # multi-byte rows: the type is printed next to one of its byte numbers, the first one
            # was seen above
            if start is not None:
                offset = start
            elif no is not None and int(no) >= expected:
                offset = int(no)
            else:
                offset = expected
            bit_row = typ == "BYTE" and bool(pending_names)
            entries.append(Entry(offset, typ, pending_names + _names(rest)))
            pending_names, start = [], None
            continue
        if m := _BYTE_NO.match(line):
            no = int(m.group(1))
            expected = entries[-1].offset + entries[-1].size if entries else 0
            if start is None and no >= expected:  # numbers below a multi-byte entry belong to it
                start = no
            continue
        if m := _NAME_ONLY.match(line):
            names = _names(m.group(1))
            # bit names below a BYTE row belong to it when its first names were printed above it
            # (centered bit layout); otherwise they are the names above the next BYTE row
            if bit_row and start is None and len(entries[-1].names) < 8:
                entries[-1].names.extend(names)
            else:
                pending_names.extend(names)
    return entries


def parse_spec(text: str) -> list[PayloadTable]:
    lines = text.splitlines()
    tables: list[PayloadTable] = []
    for i, line in enumerate(lines):
        m = _CAPTION.search(line)
        if m is None or "...." in line:  # table of contents
            continue
        body: list[str] = []
        for nxt in lines[i + 1 :]:
            if _END.match(nxt):
                break
            body.append(nxt)
        table, kind, _, function = m.groups()
        function = CAPTION_FIXES.get(table, function).strip()
        direction = "send" if kind == "Sent" else "recv"
        # a second "ByteNo" header without caption: table of the other direction (6-620)
        headers = [j for j, x in enumerate(body) if "ByteNo" in x]
        if len(headers) > 1:
            second = body[headers[1] :]
            body = body[: headers[1]]
            other = "recv" if direction == "send" else "send"
            tables.append(PayloadTable(f"{table} (no caption)", other, function, parse_table(second)))
        tables.append(PayloadTable(table, direction, function, parse_table(body)))
    return tables


_SECTION = re.compile(r"^\d+\s+6\.\d+\.\d+\s+([A-Za-z]+)\s*$")
_TYPE = re.compile(r"^\d+\s+Type: (\d+)")


def parse_command_types(text: str) -> dict[str, int]:
    """Command type of every function ("6.x.y <Function>" followed by "Type: <n>")."""
    lines = text.splitlines()
    types: dict[str, int] = {}
    for i, line in enumerate(lines):
        if m := _TYPE.match(line):
            for j in range(i - 1, max(i - 8, 0), -1):
                if h := _SECTION.match(lines[j]):
                    types[h.group(1)] = int(m.group(1))
                    break
    return types


def load_command_types() -> dict[str, int]:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    return dict(data["command_types"])


def load() -> dict[tuple[str, str], PayloadTable]:
    """Tables from ``spec_payload_tables.json``, key (function, "send"/"recv")."""
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    return {
        (t["function"], t["direction"]): PayloadTable(
            t["table"], t["direction"], t["function"], [Entry(o, ty, n) for o, ty, n in t["entries"]]
        )
        for t in data["tables"]
    }


def main(argv: list[str] | None = None) -> int:
    import sys

    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    text = Path(args[0]).read_text(encoding="utf-8")
    tables = parse_spec(text)
    types = parse_command_types(text)
    lines = [
        json.dumps(
            {
                "table": t.table,
                "direction": t.direction,
                "function": t.function,
                "entries": [[e.offset, e.type, e.names] for e in t.entries],
            },
            separators=(",", ":"),
        )
        for t in tables
    ]
    source = "Profile Robot Command Interface V1.5.9 (2024-12-04), payload tables of chapter 6"
    out = (
        '{"source":'
        + json.dumps(source)
        + ',\n"command_types":'
        + json.dumps(types, sort_keys=True)
        + ',\n"tables":[\n'
        + ",\n".join(lines)
        + "\n]}\n"
    )
    JSON_PATH.write_text(out, encoding="utf-8")
    print(f"{len(tables)} tables, {len(types)} command types -> {JSON_PATH}")
    return 0
