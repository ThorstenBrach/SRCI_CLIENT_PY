# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_ci_sdk_summary
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    tools.ci_sdk_summary: public CI summary of the SDK tests without messages.
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

"""tools.ci_sdk_summary: public CI summary of the SDK tests without messages."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.ci_sdk_summary import main, summarize

JUNIT = """<?xml version="1.0" encoding="utf-8"?>
<testsuites><testsuite name="pytest" tests="4">
<testcase classname="tests.sdk.test_a" name="test_ok"/>
<testcase classname="tests.sdk.test_a" name="test_bad"><failure message="SECRET SDK LOG">SECRET SOURCE</failure></testcase>
<testcase classname="tests.sdk.test_b" name="test_err"><error message="SECRET">x</error></testcase>
<testcase classname="tests.sdk.test_b" name="test_skip"><skipped message="s"/></testcase>
</testsuite></testsuites>
"""


def test_summary_lists_failed_ids_without_messages(tmp_path: Path) -> None:
    f = tmp_path / "junit.xml"
    f.write_text(JUNIT, encoding="utf-8")
    text, code = summarize(f)
    assert code == 1
    assert "4 run, 1 passed, 2 failed, 1 skipped" in text
    assert "FAILED tests.sdk.test_a::test_bad" in text and "FAILED tests.sdk.test_b::test_err" in text
    assert "SECRET" not in text


def test_all_passed(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    f = tmp_path / "junit.xml"
    f.write_text('<testsuite name="p"><testcase classname="c" name="t"/></testsuite>', encoding="utf-8")
    assert main([str(f)]) == 0
    assert "1 run, 1 passed, 0 failed" in capsys.readouterr().out


def test_missing_file_fails(tmp_path: Path) -> None:
    assert main([str(tmp_path / "none.xml")]) == 1


def test_require_sdk_fails_without_library(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """SRCI_REQUIRE_SDK=1: a missing SDK library stops the session (no silent skip in CI)."""
    from tests.conftest import pytest_sessionstart

    monkeypatch.setenv("SRCI_REQUIRE_SDK", "1")
    monkeypatch.setenv("SRCI_SDK_SIM_LIB", str(tmp_path / "missing.so"))
    monkeypatch.setenv("SRCI_SDK_DIR", str(tmp_path))
    monkeypatch.setattr("srci.sim.sdk.REPO_ROOT", tmp_path / "repo")
    with pytest.raises(pytest.UsageError, match="SRCI_REQUIRE_SDK"):
        pytest_sessionstart(None)  # type: ignore[arg-type]
