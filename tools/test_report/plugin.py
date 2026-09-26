# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.test_report.plugin
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    pytest plugin: result of every test case for the test report (``--tc-report DIR``).
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

"""pytest plugin: result of every test case for the test report (``--tc-report DIR``).

Loaded with ``-p tools.test_report.plugin`` (pyproject ``addopts``). Without ``--tc-report``
the plugin does nothing. With it, ``DIR/results.json``, ``DIR/TestReport.md`` and
``DIR/TestReport.html`` are written at the end of the session.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.getgroup("srci").addoption(
        "--tc-report",
        metavar="DIR",
        default=None,
        help="write the test report (results.json, TestReport.md, TestReport.html) to DIR",
    )


class Recorder:
    def __init__(self, target: Path) -> None:
        self.target = target
        self.results: dict[str, dict[str, Any]] = {}

    def set(self, nodeid: str, outcome: str, reason: str, duration: float) -> None:
        entry = self.results.setdefault(
            nodeid, {"nodeid": nodeid, "outcome": outcome, "reason": reason, "duration": 0.0}
        )
        entry["duration"] += duration
        if outcome in ("failed", "error") or entry["outcome"] == "passed":
            entry["outcome"], entry["reason"] = outcome, reason

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        wasxfail = getattr(report, "wasxfail", None)
        if report.when == "call":
            if wasxfail is not None:
                outcome = "xfailed" if report.skipped else "xpassed"
                self.set(report.nodeid, outcome, str(wasxfail), report.duration)
            elif report.skipped:
                self.set(report.nodeid, "skipped", _skip_reason(report), report.duration)
            else:
                reason = "" if report.passed else _failure(report)
                self.set(report.nodeid, report.outcome, reason, report.duration)
        elif report.when == "setup":
            if report.skipped:
                if wasxfail is not None:
                    self.set(report.nodeid, "xfailed", str(wasxfail), 0.0)
                else:
                    self.set(report.nodeid, "skipped", _skip_reason(report), 0.0)
            elif report.failed:
                self.set(report.nodeid, "error", _failure(report), report.duration)
        elif report.failed:
            self.set(report.nodeid, "error", _failure(report), report.duration)

    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session: pytest.Session) -> None:
        from tools.test_report import report

        self.target.mkdir(parents=True, exist_ok=True)
        results = sorted(self.results.values(), key=lambda r: r["nodeid"])
        meta = report.metadata()
        (self.target / "results.json").write_text(
            json.dumps({"meta": meta, "results": results}, indent=1), encoding="utf-8"
        )
        report.write(self.target, meta, results)


def _skip_reason(report: pytest.TestReport) -> str:
    longrepr = report.longrepr
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        return str(longrepr[2]).removeprefix("Skipped: ")
    return str(longrepr)


def _failure(report: pytest.TestReport) -> str:
    text = report.longreprtext.strip().splitlines()
    errors = [line for line in text if line.startswith("E ")]
    return (errors[-1][2:].strip() if errors else (text[-1] if text else ""))[:300]


def pytest_configure(config: pytest.Config) -> None:
    target = config.getoption("--tc-report")
    if target and not hasattr(config, "workerinput"):
        config.pluginmanager.register(Recorder(Path(target)), "srci_tc_report")
