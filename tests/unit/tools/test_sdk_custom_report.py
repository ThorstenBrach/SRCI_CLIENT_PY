# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_sdk_custom_report
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#
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

from pathlib import Path

from tools.sdk_custom_report import main, scan


def make_sdk(tmp_path: Path, code: str, documented: str = "") -> Path:
    (tmp_path / "src").mkdir()
    (tmp_path / "srci_py_harness").mkdir()
    (tmp_path / "src" / "a.cpp").write_text(code)
    (tmp_path / "srci_py_harness" / "CUSTOM_CHANGES.md").write_text(documented)
    return tmp_path


OK = """int a;
/* >>> SRCI_PY CUSTOM BEGIN [C-001] time hook */
int b;
/* <<< SRCI_PY CUSTOM END [C-001] */
"""


def test_paired_and_documented(tmp_path: Path) -> None:
    sdk = make_sdk(tmp_path, OK, "| C-001 | a.cpp | time hook |")
    blocks, problems = scan(sdk)
    assert [(b.id, b.begin, b.end, b.reason) for b in blocks] == [("C-001", 2, 4, "time hook")]
    assert problems == [] and main([str(sdk)]) == 0


def test_undocumented_block(tmp_path: Path) -> None:
    assert main([str(make_sdk(tmp_path, OK))]) == 1


def test_unpaired_markers(tmp_path: Path) -> None:
    code = "/* >>> SRCI_PY CUSTOM BEGIN [C-002] x */\n/* <<< SRCI_PY CUSTOM END [C-003] */\n"
    _, problems = scan(make_sdk(tmp_path, code, "C-002 C-003"))
    assert len(problems) == 2
