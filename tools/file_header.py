# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.file_header
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    File header of all Python files - the same header as in the ST sources of the PLC
#    library.
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

"""File header of all Python files - the same header as in the ST sources of the PLC library.

``python -m tools.file_header``          add the header to every hand-written file that has none
``python -m tools.file_header --check``  fail if a file has no header (CI)

The generated files get the header from their generator (``tools.st2py``: author and date of the
ST source, ``tools.plcopen_gen``). Hand-written files: object = module name, date = date of the
first commit of the file, description = first line of the module docstring.
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "Thorsten Brach"
PROJECT = "SRCI Robot Library - Python client"
LINE = "# " + "-" * 73
MARKER = f"#  {PROJECT}"
GENERATED_DATE = "2026-09-26"  # date of the files generated from the PLC library (Python port)
DIRS = ("src", "tools", "tests", "examples")


def render(obj: str, date: str, description: str = "", author: str = AUTHOR) -> str:
    """The header as comment block (ends with a newline)."""
    desc = textwrap.wrap(" ".join(description.split()), 88) or [""]
    lines = [
        LINE,
        MARKER,
        LINE,
        "#",
        f"#  Object:      {obj}",
        f"#  Author:      {author}",
        f"#  Date:        {date}",
        "#",
        "#  Description:",
        *(f"#    {d}".rstrip() for d in desc),
        "#",
        "#  Copyright:",
        f"#    (C) {date[:4]} {author}. All rights reserved",
        "#             Licensed under the MIT License.",
        "#",
        "#  Disclaimer:",
        "#    This project is provided without any guarantee and can be used for",
        "#    private and commercial purposes. Any use is at the user's",
        "#    own risk and responsibility.",
        "#",
        LINE,
    ]
    return "\n".join(lines) + "\n"


def st_fields(decl: str) -> tuple[str, str]:
    """Author and date from the header comment of an ST declaration (defaults if missing)."""
    author = re.search(r"//\s*Author:\s*(.+?)\s*$", decl, flags=re.M)
    date = re.search(r"//\s*Date:\s*(\d{4}-\d{2}-\d{2})", decl)
    return (author.group(1) if author else AUTHOR), (date.group(1) if date else GENERATED_DATE)


def has_header(text: str) -> bool:
    return MARKER in text[:600]


def _first_commit_date(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%ad", "--date=short", "--", str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    return out[-1] if out else GENERATED_DATE


def _doc_line(text: str) -> str:
    try:
        doc = ast.get_docstring(ast.parse(text)) or ""
    except SyntaxError:
        doc = ""
    return doc.strip().splitlines()[0] if doc.strip() else ""


def files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", *(f"{d}/*.py" for d in DIRS)]
        + [f"{d}/*.pyi" for d in DIRS],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    return sorted(ROOT / f for f in out if (ROOT / f).is_file())


def module_name(path: Path) -> str:
    """Dotted module name (``srci.api.client``, ``tools.st2py``, ``tests.sdk.test_core_fbs``)."""
    rel = path.relative_to(ROOT).with_suffix("")
    parts = list(rel.parts[1:] if rel.parts[0] == "src" else rel.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def add_header(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if has_header(text):
        return False
    obj = module_name(path)
    head = render(obj, _first_commit_date(path), _doc_line(text))
    path.write_text(head + ("\n" if text.strip() else "") + text, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.file_header", description=__doc__)
    ap.add_argument("--check", action="store_true", help="only check, fail if a header is missing")
    args = ap.parse_args(argv)
    missing = [p for p in files() if not has_header(p.read_text(encoding="utf-8"))]
    if args.check:
        for p in missing:
            print("no file header:", p.relative_to(ROOT), file=sys.stderr)
        if missing:
            print("run: python -m tools.file_header", file=sys.stderr)
        return 1 if missing else 0
    for p in missing:
        add_header(p)
    print(f"file header added to {len(missing)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
