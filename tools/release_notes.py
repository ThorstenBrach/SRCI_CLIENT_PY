# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.release_notes
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Release notes of a version from CHANGELOG.md (``python -m tools.release_notes v0.1.0``).
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

"""Release notes of a version from CHANGELOG.md (``python -m tools.release_notes v0.1.0``).

Used by the release workflow: checks that the tag matches the package version
(``pyproject.toml`` and ``srci.__version__``) and prints the section ``## [0.1.0]`` of the
change log (the release body). Exit code 1 on a version mismatch or a missing section.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package_version() -> str:
    return str(tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"])


def section(changelog: str, version: str) -> str | None:
    """Text of ``## [version]`` up to the next ``## [`` heading (without the heading)."""
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|\Z)", changelog, flags=re.M | re.S)
    return m.group(1).strip() if m else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.release_notes", description=__doc__)
    ap.add_argument("tag", help="git tag, e.g. v0.1.0")
    args = ap.parse_args(argv)
    version = args.tag.removeprefix("v")
    if version != package_version():
        print(f"tag {args.tag} does not match the package version {package_version()} (pyproject.toml)",
              file=sys.stderr)  # fmt: skip
        return 1
    text = section((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), version)
    if not text:
        print(f"CHANGELOG.md has no section '## [{version}]'", file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
