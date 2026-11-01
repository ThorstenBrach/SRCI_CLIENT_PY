# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.spec_tables.values
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Value ranges of the command parameters of the SRCI specification
#    ("Associated command values of <function>").
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

"""Value ranges of the command parameters ("Associated command values of <function>").

Reads the text export of the specification PDF (``pdftotext -layout``) and returns, per function
and parameter, the data type, the listed values ("• 2: ..."), the ranges ("1..254") and whether
a negative value is the default ("<0%: (default)"). The tables are the reference of the
parameter tests VAL-PAR (tests/sdk/validation/test_val_parameters.py).

Only facts are stored (names, data types, numbers), no text of the specification (copyright PNO).

    python -m tools.spec_tables.values <spec.txt>   # writes tools/spec_tables/spec_parameter_values.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

JSON_PATH = Path(__file__).with_name("spec_parameter_values.json")

_CAPTION = re.compile(
    r'Table 6-\d+: Associated command values of "\s*(\w+)\s*"(?:\s*\u2013\s*"Application( Layer")?)?\s*$'
)
_TYPES = (
    r"(BOOL|STRING|USINT|SINT|UINT|INT|UDINT|DINT|REAL|LREAL|WORD|BYTE|DWORD|ARRAY|Robot\w*|"
    r"AxesGroup|TIME|ULINT|LINT)"
)
_ROW = re.compile(r"^\s{0,8}([A-Z][A-Za-z0-9_\[\]\.]*)(?:\s\d)?\s{2,}" + _TYPES)
_END = re.compile(r"Table 6-\d+:|^\s*6\.\d+\.\d+\.\d+ ")
_NOISE = re.compile(r"Copyright PNO|Draft|^\s*Parameter\s+Data Type")
_BULLET = re.compile(r"•\s*(-?\d+(?![\d.])|[<>≥≤]\s*-?\d+)\s*(?:\(default\))?\s*:?(.*?)(?=•|$)", re.S)
_INVALID = re.compile(r"Undefined|not allowed|returns an error", re.I)
_OPEN = {">0": "positive", "≥0": "non_negative", "<0": "negative"}
_RANGE = re.compile(r"(?<![\[\d-])(-?\d+)\s*(?:\(default\))?\s*\.\.\s*(-?\d+)(?!\])")


def parse_values(text: str) -> dict[str, list[dict[str, Any]]]:
    """Parameters of every "Associated command values" table (the longest table per function)."""
    lines = text.split("\n")
    result: dict[str, list[dict[str, Any]]] = {}
    i = 0
    while i < len(lines) - 1:
        m = _CAPTION.search(lines[i])
        if not m or "...." in lines[i] or "...." in lines[i + 1]:  # table of contents
            i += 1
            continue
        rows: list[dict[str, Any]] = []
        j = i + 1
        while j < len(lines) and not _END.search(lines[j]):
            r = _ROW.match(lines[j])
            if r:
                rows.append(
                    {"name": r.group(1), "type": lines[j][r.start(2) :].split("  ")[0].strip(), "text": ""}
                )
            if rows and not _NOISE.search(lines[j]):
                rows[-1]["text"] += lines[j] + "\n"
            j += 1
        if len(rows) > len(result.get(m.group(1), [])):
            result[m.group(1)] = rows
        i = j
    return {
        function: [
            {
                "name": r["name"],
                "type": r["type"],
                **_bullets(r["text"]),
                "ranges": [[int(a), int(b)] for a, b in _RANGE.findall(r["text"])],
                "negative_default": "<0" in r["text"] and "default" in r["text"],
            }
            for r in rows
        ]
        for function, rows in sorted(result.items())
    }


def _bullets(text: str) -> dict[str, list[Any]]:
    """Listed values ("• 2: ..."), invalid listed values ("• 0: Undefined") and open ranges ("• >0: ...")."""
    values: set[int] = set()
    invalid: set[int] = set()
    open_: set[str] = set()
    for key, body in _BULLET.findall(re.sub(r"\s+", " ", text)):
        key = key.replace(" ", "")
        if key in _OPEN:
            open_.add(_OPEN[key])
        elif key.lstrip("-").isdigit():
            (invalid if _INVALID.search(body) else values).add(int(key))
    return {"values": sorted(values), "invalid": sorted(invalid), "open": sorted(open_)}


def load() -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = json.loads(JSON_PATH.read_text(encoding="utf-8"))["functions"]
    return data


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    functions = parse_values(Path(args[0]).read_text(encoding="utf-8"))
    source = "Profile Robot Command Interface V1.5.9 (2024-12-04), command values of chapter 6"
    lines = [f"  {json.dumps(f)}: {json.dumps(rows, separators=(',', ':'))}" for f, rows in functions.items()]
    out = '{"source": ' + json.dumps(source) + ',\n "functions": {\n' + ",\n".join(lines) + "\n }}\n"
    JSON_PATH.write_text(out, encoding="utf-8", newline="\n")
    print(f"{len(functions)} functions -> {JSON_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
