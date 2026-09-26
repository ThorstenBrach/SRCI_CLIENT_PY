# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.ci_sdk_summary
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Result of the SDK tests for a public CI log (``python -m tools.ci_sdk_summary
#    junit.xml``).
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

"""Result of the SDK tests for a public CI log (``python -m tools.ci_sdk_summary junit.xml``).

The SRCI SDK is private: failure messages of the SDK tests can contain log texts of the SDK,
compiler output can contain SDK source lines. The CI job "sdk" therefore writes the complete
output only to files that are neither printed nor uploaded, and prints this summary: counts and
the IDs of the failed tests - no messages. Run the failed tests locally for details.
Exit code 1 if a test failed or had an error (or no test ran).
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def summarize(junit: Path) -> tuple[str, int]:
    root = ET.parse(junit).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    total = failed = skipped = 0
    names: list[str] = []
    for suite in suites:
        for case in suite.iter("testcase"):
            total += 1
            name = f"{case.get('classname', '')}::{case.get('name', '')}"
            if case.find("failure") is not None or case.find("error") is not None:
                failed += 1
                names.append(name)
            elif case.find("skipped") is not None:
                skipped += 1
    lines = [f"SDK tests: {total} run, {total - failed - skipped} passed, {failed} failed, {skipped} skipped"]
    lines += [f"FAILED {n}" for n in names]
    if failed:
        lines.append(
            "(messages are not shown because they may contain SDK internals - run the tests locally)"
        )
    return "\n".join(lines), 1 if failed or total == 0 else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.ci_sdk_summary", description=__doc__)
    ap.add_argument("junit", type=Path)
    args = ap.parse_args(argv)
    if not args.junit.is_file():
        print("SDK tests: no result file (pytest did not start)")
        return 1
    text, code = summarize(args.junit)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
