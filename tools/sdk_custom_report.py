# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.sdk_custom_report
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Report (and check) the SRCI_PY changes inside the private SRCI SDK.
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

"""Report (and check) the SRCI_PY changes inside the private SRCI SDK.

Markers::

    /* >>> SRCI_PY CUSTOM BEGIN [C-001] reason */
    ...
    /* <<< SRCI_PY CUSTOM END [C-001] */

Every BEGIN needs a matching END with the same id, ids must be unique and listed in
``srci_py_harness/CUSTOM_CHANGES.md``. Exit code 1 on problems.

Usage: ``python -m tools.sdk_custom_report "<path to SRCI SDK>"``
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

BEGIN = re.compile(r"SRCI_PY CUSTOM BEGIN \[(?P<id>C-\d{3})\]\s*(?P<reason>.*?)\s*(?:\*/)?\s*$")
END = re.compile(r"SRCI_PY CUSTOM END \[(?P<id>C-\d{3})\]")
SOURCE_DIRS = ("src", "include", "lib")
SUFFIXES = {".cpp", ".h", ".hpp", ".c"}


@dataclass(frozen=True)
class Block:
    id: str
    file: Path
    begin: int
    end: int
    reason: str


def scan(sdk: Path) -> tuple[list[Block], list[str]]:
    blocks: list[Block] = []
    problems: list[str] = []
    for folder in SOURCE_DIRS:
        for path in sorted((sdk / folder).rglob("*")):
            if path.suffix not in SUFFIXES:
                continue
            open_blocks: dict[str, tuple[int, str]] = {}
            for no, line in enumerate(path.read_text("utf-8", errors="replace").splitlines(), 1):
                if m := BEGIN.search(line):
                    if m["id"] in open_blocks:
                        problems.append(f"{path}:{no}: nested BEGIN for {m['id']}")
                    open_blocks[m["id"]] = (no, m["reason"])
                elif m := END.search(line):
                    if m["id"] not in open_blocks:
                        problems.append(f"{path}:{no}: END without BEGIN for {m['id']}")
                        continue
                    begin, reason = open_blocks.pop(m["id"])
                    blocks.append(Block(m["id"], path.relative_to(sdk), begin, no, reason))
            for block_id, (no, _) in open_blocks.items():
                problems.append(f"{path}:{no}: BEGIN without END for {block_id}")
    return blocks, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.sdk_custom_report", description=__doc__)
    ap.add_argument("sdk", type=Path, help="path of the SRCI SDK folder")
    args = ap.parse_args(argv)
    blocks, problems = scan(args.sdk)
    doc_file = args.sdk / "srci_py_harness" / "CUSTOM_CHANGES.md"
    documented = set(re.findall(r"C-\d{3}", doc_file.read_text("utf-8"))) if doc_file.exists() else set()
    for block in blocks:
        if block.id not in documented:
            problems.append(f"{block.file}:{block.begin}: {block.id} is not listed in CUSTOM_CHANGES.md")
        print(f"{block.id}  {block.file}:{block.begin}-{block.end}  {block.reason}")
    print(f"{len(blocks)} custom block(s)")
    for p in problems:
        print(p, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
