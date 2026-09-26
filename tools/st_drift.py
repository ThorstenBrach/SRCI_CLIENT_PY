# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st_drift
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Detect Python code whose ST source changed since it was ported.
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

"""Detect Python code whose ST source changed since it was ported.

Every ported unit carries a marker comment::

    # ST-Source: POUs/BasicMove/MC_GroupStop/MC_GroupStopFB.st  sha256: 0123456789abcdef

(the path is relative to ``RobotLibrary/Library`` of the PLC library, the hash is the
first 16 hex digits of the sha256 of the ST file with normalised line endings).
``File.st#Name`` refers to one ``METHOD``/``PROPERTY`` of a large POU only.

Usage::

    python -m tools.st_drift <path to RobotLibrary/Library>            # report
    python -m tools.st_drift <path to RobotLibrary/Library> --update   # re-stamp hashes

Exit code 1 if a referenced ST file changed or is missing.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile(r"#\s*ST-Source:\s*(?P<path>\S+)\s+sha256:\s*(?P<hash>[0-9a-f]{16})")


_UNIT = re.compile(
    r"^(?:METHOD|PROPERTY)(?:\s+(?:PRIVATE|PUBLIC|PROTECTED|INTERNAL|FINAL|ABSTRACT))*\s+(\w+)\b.*?"
    r"^END_(?:METHOD|PROPERTY)\b",
    re.MULTILINE | re.DOTALL,
)


def st_units(text: str) -> dict[str, str]:
    """``METHOD``/``PROPERTY`` blocks of an ST file by name."""
    return {m.group(1): m.group(0) for m in _UNIT.finditer(text)}


def st_hash(path: Path, unit: str | None = None) -> str:
    """Hash of an ST file (or of one method of it), independent of CRLF/LF line endings."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    if unit is not None:
        units = st_units(data.decode("utf-8", errors="replace"))
        if unit not in units:
            raise KeyError(unit)
        data = units[unit].encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16]


@dataclass(frozen=True)
class Marker:
    file: Path
    line: int
    st_path: str
    hash: str


def find_markers(src: Path) -> list[Marker]:
    markers: list[Marker] = []
    for py in sorted(src.rglob("*.py")):
        if "_generated" in py.parts:
            continue
        for no, text in enumerate(py.read_text("utf-8").splitlines(), 1):
            m = MARKER.search(text)
            if m:
                markers.append(Marker(py, no, m["path"], m["hash"]))
    return markers


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.st_drift", description=__doc__)
    ap.add_argument("library", type=Path, help="path to RobotLibrary/Library of the PLC library")
    ap.add_argument("--src", type=Path, default=ROOT / "src" / "srci")
    ap.add_argument("--update", action="store_true", help="write the current hashes into the markers")
    args = ap.parse_args(argv)

    changed: list[str] = []
    for mk in find_markers(args.src):
        file_part, _, unit = mk.st_path.partition("#")
        st_file = args.library / file_part
        rel = mk.file.relative_to(args.src.parent)
        try:
            current = st_hash(st_file, unit or None)
        except (FileNotFoundError, KeyError):
            changed.append(f"{rel}:{mk.line}: ST source missing: {mk.st_path}")
            continue
        if current == mk.hash:
            continue
        if args.update:
            lines = mk.file.read_text("utf-8").split("\n")
            lines[mk.line - 1] = lines[mk.line - 1].replace(f"sha256: {mk.hash}", f"sha256: {current}")
            mk.file.write_text("\n".join(lines), "utf-8", newline="\n")
            print(f"updated {rel}:{mk.line} {mk.st_path}")
        else:
            changed.append(f"{rel}:{mk.line}: ST source changed since porting: {mk.st_path}")
    for line in changed:
        print(line, file=sys.stderr)
    if not changed:
        print("all ported units are up to date with their ST sources")
    return 1 if changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
