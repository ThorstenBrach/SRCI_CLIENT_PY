# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.test_report.report
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Test report (Markdown + HTML) from the results of a pytest run.
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

"""Test report (Markdown + HTML) from the results of a pytest run.

The report is the quality evidence of a release: test environment (versions, git commit,
SDK simulator), summary, status of every test case (ID from ``tests/testcases.json``), the
known deviations (findings ``Fnn`` of docs/ST_FINDINGS.md, tests marked xfail) and every
instance that did not pass.
"""

from __future__ import annotations

import hashlib
import html
import json
import platform
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tools.test_report import registry

ROOT = registry.ROOT
FINDINGS = ROOT / "docs" / "ST_FINDINGS.md"
OUTCOMES = ("passed", "failed", "error", "xfailed", "xpassed", "skipped")
FINDING = re.compile(r"\bF\d{2}\b")


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def metadata() -> dict[str, Any]:
    """Test environment of this run."""
    meta: dict[str, Any] = {
        "date": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain", "--untracked-files=no")),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    try:
        from importlib.metadata import version

        meta["srci_version"] = version("srci")
    except Exception:
        meta["srci_version"] = _pyproject_version()
    spec = ROOT / "tools" / "spec_tables" / "spec_payload_tables.json"
    meta["specification"] = json.loads(spec.read_text(encoding="utf-8")).get("source", "")
    try:
        from srci.sim.sdk import API_VERSION, find_sdk_library

        library = find_sdk_library()
        meta["sdk_library"] = library.name
        meta["sdk_library_sha256"] = hashlib.sha256(library.read_bytes()).hexdigest()
        meta["sdk_api_version"] = API_VERSION
    except Exception:
        meta["sdk_library"] = "not available (SDK tests skipped)"
    return meta


def _pyproject_version() -> str:
    match = re.search(r'^version = "(.+)"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"), re.M)
    return match.group(1) if match else "?"


def findings() -> dict[str, str]:
    """Finding ID -> short text (column "Problem" of docs/ST_FINDINGS.md)."""
    found = {}
    for line in FINDINGS.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 4 and re.fullmatch(r"F\d{2}", cells[1]):
            text = re.sub(r"`", "", cells[3])
            found[cells[1]] = text if len(text) <= 160 else text[:157].rsplit(" ", 1)[0] + " ..."
    return found


@dataclass
class Case:
    entry: dict[str, Any]
    results: list[dict[str, Any]] = field(default_factory=list)

    @property
    def counts(self) -> Counter[str]:
        return Counter(r["outcome"] for r in self.results)

    @property
    def status(self) -> str:
        counts = self.counts
        if not self.results:
            return "not run"
        if counts["failed"] or counts["error"]:
            return "FAILED"
        if counts["xpassed"]:
            return "check (xpassed)"
        if counts["passed"] == 0 and counts["xfailed"] == 0:
            return "skipped"
        if counts["xfailed"]:
            return "passed, known deviations"
        return "passed"

    @property
    def findings(self) -> list[str]:
        return sorted(
            {f for r in self.results if r["outcome"] == "xfailed" for f in FINDING.findall(r["reason"])}
        )


def group(
    results: list[dict[str, Any]], entries: list[dict[str, Any]]
) -> tuple[list[Case], list[dict[str, Any]]]:
    """Results per test case (registry order) and the results without registry entry."""
    cases = {str(e["test"]): Case(e) for e in entries if e.get("status") == "active"}
    unknown = []
    for result in results:
        key = result["nodeid"].split("[", 1)[0]
        if key in cases:
            cases[key].results.append(result)
        else:
            unknown.append(result)
    return list(cases.values()), unknown


def instance_id(case: Case, result: dict[str, Any]) -> str:
    nodeid = result["nodeid"]
    return f"{case.entry['id']}[{nodeid.split('[', 1)[1]}" if "[" in nodeid else str(case.entry["id"])


def build(meta: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    entries = registry.load()
    cases, unknown = group(results, entries)
    totals = Counter(r["outcome"] for r in results)
    per_area: dict[str, Counter[str]] = defaultdict(Counter)
    for case in cases:
        code, _ = registry.area_of(str(case.entry["test"]))
        per_area[code]["cases"] += 1
        per_area[code].update(case.counts)
    finding_texts = findings()
    finding_counts: Counter[str] = Counter()
    for result in results:
        if result["outcome"] == "xfailed":
            finding_counts.update(
                set(FINDING.findall(result["reason"])) or {"(no finding: precondition or RC)"}
            )
    return {
        "meta": meta,
        "cases": cases,
        "unknown": unknown,
        "totals": totals,
        "per_area": per_area,
        "findings": [(f, n, finding_texts.get(f, "")) for f, n in sorted(finding_counts.items())],
        "verdict": "FAILED" if totals["failed"] or totals["error"] else "PASSED",
    }


# --------------------------------------------------------------------------- Markdown


def _md(text: object) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_markdown(data: dict[str, Any]) -> str:
    meta, totals = data["meta"], data["totals"]
    names = registry.area_names()
    out = [
        "# SRCI_PY - Test report",
        "",
        f"**Result: {data['verdict']}** - {sum(totals.values())} test instances in {len(data['cases'])} test cases.",
        "",
        "## Test environment",
        "",
        "| | |",
        "|---|---|",
    ]
    rows = [
        ("Date", meta.get("date")),
        ("srci version", meta.get("srci_version")),
        (
            "Git commit",
            f"{meta.get('git_commit', '')[:12]} ({meta.get('git_branch', '')})"
            + (" + local changes" if meta.get("git_dirty") else ""),
        ),
        ("Python", meta.get("python")),
        ("Platform", meta.get("platform")),
        ("Specification", meta.get("specification")),
        ("SDK simulator", meta.get("sdk_library")),
        ("SDK simulator SHA-256", meta.get("sdk_library_sha256", "-")),
        ("SDK simulator C API", meta.get("sdk_api_version", "-")),
    ]
    out += [f"| {k} | {_md(v)} |" for k, v in rows]
    out += ["", "## Summary", "", "| Outcome | Instances |", "|---|---:|"]
    out += [f"| {o} | {totals[o]} |" for o in OUTCOMES]
    out += [
        "",
        "`xfailed`: known deviation (finding of docs/ST_FINDINGS.md, the behavior of the PLC library is",
        "kept 1:1); `skipped`: not applicable (e.g. no parameter of the kind, SDK not available).",
        "",
        "## Areas",
        "",
        "| Area | Description | Test cases | passed | failed | xfailed | skipped |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for code, counts in data["per_area"].items():
        out.append(
            f"| {code} | {names[code]} | {counts['cases']} | {counts['passed']} | "
            f"{counts['failed'] + counts['error']} | {counts['xfailed']} | {counts['skipped']} |"
        )
    out += ["", "## Known deviations (xfail)", "", "| Finding | Instances | Description |", "|---|---:|---|"]
    out += [f"| {f} | {n} | {_md(t)} |" for f, n, t in data["findings"]]
    out += [
        "",
        "## Test cases",
        "",
        "| ID | Title | Instances | Status | Findings |",
        "|---|---|---:|---|---|",
    ]
    for case in data["cases"]:
        out.append(
            f"| {case.entry['id']} | {_md(case.entry['title'])} | {len(case.results)} | {case.status} | "
            f"{', '.join(case.findings)} |"
        )
    out += ["", "## Instances not passed", "", "| Instance | Outcome | Reason |", "|---|---|---|"]
    for case in data["cases"]:
        for result in case.results:
            if result["outcome"] != "passed":
                out.append(
                    f"| {_md(instance_id(case, result))} | {result['outcome']} | {_md(result['reason'])} |"
                )
    if data["unknown"]:
        out += ["", "## Tests without registry entry", ""]
        out += [f"- {r['nodeid']}: {r['outcome']}" for r in data["unknown"]]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- HTML

CSS = """
:root{--bg:#fff;--fg:#1d2330;--muted:#5d6675;--line:#dfe3ea;--head:#f3f5f8;
--ok:#1a7f37;--bad:#c62828;--warn:#9a6700;--skip:#6e7781}
@media (prefers-color-scheme:dark){:root{--bg:#14171c;--fg:#e6e9ee;--muted:#9aa3b0;--line:#2c323b;
--head:#1d2128;--ok:#4ac26b;--bad:#ff6b6b;--warn:#d29922;--skip:#8b949e}}
body{background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,Segoe UI,sans-serif;margin:0 auto;
max-width:1200px;padding:24px 16px}
h1{margin:0 0 4px}h2{margin-top:32px;border-bottom:1px solid var(--line);padding-bottom:4px}
table{border-collapse:collapse;width:100%;margin:8px 0}th,td{border:1px solid var(--line);
padding:4px 8px;text-align:left;vertical-align:top}th{background:var(--head)}td.n{text-align:right}
.passed{color:var(--ok)}.FAILED,.failed,.error{color:var(--bad);font-weight:600}
.xfailed,.known{color:var(--warn)}.skipped{color:var(--skip)}
.verdict{font-size:18px;font-weight:700}tr.case td:first-child{white-space:nowrap}details summary{cursor:pointer}code{font-size:12px}
.wrap{overflow-x:auto}input{padding:6px 8px;width:100%;max-width:360px;margin:8px 0;
background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:4px}
"""

SCRIPT = """
document.getElementById('filter').addEventListener('input',e=>{const q=e.target.value.toLowerCase();
document.querySelectorAll('#cases tbody tr.case').forEach(r=>{r.style.display=
r.textContent.toLowerCase().includes(q)?'':'none'})});
"""


def _h(text: object) -> str:
    return html.escape(str(text))


def _css_class(status: str) -> str:
    return {"passed, known deviations": "known", "check (xpassed)": "known"}.get(status, status.split()[0])


def render_html(data: dict[str, Any]) -> str:
    meta, totals = data["meta"], data["totals"]
    names = registry.area_names()
    verdict_class = "passed" if data["verdict"] == "PASSED" else "FAILED"
    parts = [
        "<!doctype html><html lang=en><head><meta charset=utf-8>",
        "<meta name=viewport content='width=device-width,initial-scale=1'>",
        f"<title>SRCI_PY test report</title><style>{CSS}</style></head><body>",
        "<h1>SRCI_PY - Test report</h1>",
        f"<p class='verdict {verdict_class}'>Result: {data['verdict']}</p>",
        f"<p>{sum(totals.values())} test instances in {len(data['cases'])} test cases, {_h(meta.get('date'))}</p>",
        "<h2>Test environment</h2><div class=wrap><table>",
    ]
    env = [
        ("srci version", meta.get("srci_version")),
        (
            "Git commit",
            f"{meta.get('git_commit', '')} ({meta.get('git_branch', '')})"
            + (" + local changes" if meta.get("git_dirty") else ""),
        ),
        ("Python", meta.get("python")),
        ("Platform", meta.get("platform")),
        ("Specification", meta.get("specification")),
        ("SDK simulator", meta.get("sdk_library")),
        ("SDK simulator SHA-256", meta.get("sdk_library_sha256", "-")),
        ("SDK simulator C API", meta.get("sdk_api_version", "-")),
    ]
    parts += [f"<tr><th>{_h(k)}</th><td><code>{_h(v)}</code></td></tr>" for k, v in env]
    parts.append("</table></div><h2>Summary</h2><table><tr>")
    parts += [f"<th>{o}</th>" for o in OUTCOMES]
    parts.append("</tr><tr>")
    parts += [f"<td class='n {o}'>{totals[o]}</td>" for o in OUTCOMES]
    parts.append(
        "</tr></table><h2>Areas</h2><div class=wrap><table><tr><th>Area</th><th>Description</th>"
        "<th>Cases</th><th>passed</th><th>failed</th><th>xfailed</th><th>skipped</th></tr>"
    )
    for code, c in data["per_area"].items():
        parts.append(
            f"<tr><td>{code}</td><td>{_h(names[code])}</td><td class=n>{c['cases']}</td><td class=n>{c['passed']}"
            f"</td><td class=n>{c['failed'] + c['error']}</td><td class=n>{c['xfailed']}</td>"
            f"<td class=n>{c['skipped']}</td></tr>"
        )
    parts.append(
        "</table></div><h2>Known deviations (xfail)</h2><div class=wrap><table>"
        "<tr><th>Finding</th><th>Instances</th><th>Description</th></tr>"
    )
    parts += [f"<tr><td>{f}</td><td class=n>{n}</td><td>{_h(t)}</td></tr>" for f, n, t in data["findings"]]
    parts.append(
        "</table></div><h2>Test cases</h2><input id=filter placeholder='Filter test cases'>"
        "<div class=wrap><table id=cases><thead><tr><th>ID</th><th>Title</th><th>Instances</th>"
        "<th>Status</th><th>Findings</th></tr></thead><tbody>"
    )
    for case in data["cases"]:
        status = case.status
        details = ""
        not_passed = [r for r in case.results if r["outcome"] != "passed"]
        if len(case.results) > 1 or not_passed:
            rows = "".join(
                f"<tr><td><code>{_h(instance_id(case, r))}</code></td><td class={r['outcome']}>{r['outcome']}</td>"
                f"<td>{_h(r['reason'])}</td></tr>"
                for r in case.results
            )
            details = f"<details><summary>instances</summary><table>{rows}</table></details>"
        refs = ", ".join(str(r) for r in case.entry.get("refs", []))
        parts.append(
            f"<tr class=case><td><b>{_h(case.entry['id'])}</b></td><td>{_h(case.entry['title'])}"
            f"<br><code>{_h(case.entry['test'])}</code>{'<br>' + _h(refs) if refs else ''}{details}</td>"
            f"<td class=n>{len(case.results)}</td><td class='{_css_class(status)}'>{_h(status)}</td>"
            f"<td>{', '.join(case.findings)}</td></tr>"
        )
    parts.append("</tbody></table></div>")
    if data["unknown"]:
        parts.append("<h2>Tests without registry entry</h2><ul>")
        parts += [f"<li><code>{_h(r['nodeid'])}</code>: {r['outcome']}</li>" for r in data["unknown"]]
        parts.append("</ul>")
    parts.append(f"<script>{SCRIPT}</script></body></html>")
    return "\n".join(parts)


def write(target: Path, meta: dict[str, Any], results: list[dict[str, Any]]) -> None:
    data = build(meta, results)
    (target / "TestReport.md").write_text(render_markdown(data), encoding="utf-8", newline="\n")
    (target / "TestReport.html").write_text(render_html(data), encoding="utf-8", newline="\n")
