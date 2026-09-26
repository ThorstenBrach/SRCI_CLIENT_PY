"""CLI: ``python -m tools.plcopen_gen [--check] [--xml PATH] [--out DIR]``."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from .emitter import Generator
from .overrides import apply_overrides
from .parser import parse_library

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_XML = ROOT / "third_party" / "robotlibrary" / "RobotLibrary.xml"
DEFAULT_OUT = ROOT / "src" / "srci" / "types" / "_generated"


def generate(xml: Path) -> dict[str, str]:
    """Return ``{file name: source}`` for all generated modules."""
    digest = hashlib.sha256(xml.read_bytes()).hexdigest()
    note = f"Source: third_party/robotlibrary/{xml.name} (sha256 {digest[:16]})"
    lib = parse_library(xml)
    apply_overrides(lib)
    gen = Generator(lib, note)
    return {
        "__init__.py": gen.emit_init(),
        "enums.py": gen.emit_enums(),
        "structs.py": gen.emit_structs(),
        "constants.py": gen.emit_constants(),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.plcopen_gen", description=__doc__)
    ap.add_argument("--xml", type=Path, default=DEFAULT_XML)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="fail if the generated files are out of date")
    args = ap.parse_args(argv)

    files = generate(args.xml)
    if args.check:
        stale = [
            n
            for n, src in files.items()
            if not (args.out / n).exists() or (args.out / n).read_text("utf-8") != src
        ]
        if stale:
            print("generated files are out of date: " + ", ".join(stale), file=sys.stderr)
            print("run: python -m tools.plcopen_gen", file=sys.stderr)
            return 1
        print("generated files are up to date")
        return 0
    args.out.mkdir(parents=True, exist_ok=True)
    for name, src in files.items():
        (args.out / name).write_text(src, encoding="utf-8", newline="\n")
    print(f"wrote {len(files)} files to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
