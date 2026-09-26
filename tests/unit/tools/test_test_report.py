# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_test_report
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Test case registry and test report (tools/test_report).
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

"""Test case registry and test report (tools/test_report)."""

from __future__ import annotations

from tools.test_report import registry, report


def test_every_test_has_an_id() -> None:
    """The registry tests/testcases.json is up to date (python -m tools.test_report update)."""
    assert registry.problems(registry.load(), registry.scan()) == []


def test_ids_are_unique_and_stable() -> None:
    entries = registry.load()
    functions = registry.scan()
    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids))
    added = [*functions, registry.TestFunction("tests/sdk/test_core_fbs.py::test_new_one", "")]
    updated = registry.update(entries, added)
    new = next(e for e in updated if e["test"] == "tests/sdk/test_core_fbs.py::test_new_one")
    assert new["id"] not in ids and str(new["id"]).startswith("SDK-CORE-")
    removed = registry.update(entries, functions[1:])
    retired = next(e for e in removed if e["test"] == functions[0].test)
    assert retired["status"] == "retired" and retired["id"] == next(
        e["id"] for e in entries if e["test"] == functions[0].test
    )


def test_pattern_id_and_reference_from_the_docstring() -> None:
    doc = 'GEN-07 (Siemens x-08 "Axes group is not defined"): robotTask not running -> Error.'
    assert registry.split_doc(doc) == (
        "robotTask not running -> Error.",
        'Siemens x-08 "Axes group is not defined"',
    )
    assert registry.first_sentence(doc) == "RobotTask not running -> Error."


def test_report_from_results() -> None:
    results = [
        {
            "nodeid": "tests/sdk/test_methodology.py::test_gen05_default_values[A]",
            "outcome": "passed",
            "reason": "",
        },
        {
            "nodeid": "tests/sdk/test_methodology.py::test_gen05_default_values[B]",
            "outcome": "xfailed",
            "reason": "F41: DecelerationRate default",
        },
        {"nodeid": "tests/sdk/test_core_fbs.py::test_group_stop", "outcome": "failed", "reason": "assert x"},
    ]
    meta = {"date": "2026-01-01", "git_commit": "abc", "specification": "V1.5.9"}
    data = report.build(meta, results)
    assert data["verdict"] == "FAILED"
    cases = {c.entry["id"]: c for c in data["cases"] if c.results}
    assert cases["GEN-05"].status == "passed, known deviations" and cases["GEN-05"].findings == ["F41"]
    markdown = report.render_markdown(data)
    assert "| GEN-05[B] | xfailed | F41: DecelerationRate default |" in markdown
    assert "**Result: FAILED**" in markdown
    html = report.render_html(data)
    assert "<b>GEN-05</b>" in html and "F41" in html


def test_findings_are_read_from_st_findings() -> None:
    found = report.findings()
    assert {"F41", "F50", "F52"} <= set(found)
