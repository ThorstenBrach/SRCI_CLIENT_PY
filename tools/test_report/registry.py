"""Registry of the test cases: a stable, unique ID for every test function.

``tests/testcases.json`` holds one entry per test function::

    {"id": "SDK-CORE-007", "test": "tests/sdk/test_core_fbs.py::test_group_stop",
     "title": "...", "refs": ["spec 6.x"], "status": "active"}

- IDs are assigned once and never reused: a removed test keeps its entry with
  ``"status": "retired"``.
- The methodology tests carry their pattern ID in the docstring (``GEN-05 (...): text``);
  that ID is used instead of a numbered one.
- A parametrized test is one test case; every parameter set is an instance
  ``<ID>[<parameter id>]`` in the test report.
- ``title``: first sentence of the docstring; tests without docstring get a title from
  their name that can be improved in the registry (the registry wins over the name, a
  docstring wins over the registry).
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "tests" / "testcases.json"

# test file (prefix, relative to tests/) -> (area code, area name); the first match wins
AREAS: list[tuple[str, str, str]] = [
    ("sdk/test_methodology.py", "MET", "Methodology tests of all function blocks against the SDK"),
    ("sdk/test_bilateral.py", "SDK-BIL", "Bilateral tests: client payload decoded by the SDK and back"),
    ("sdk/test_payload_sdk.py", "SDK-PAY", "Payload layout against the command structures of the SDK"),
    ("sdk/test_core_fbs.py", "SDK-CORE", "Core function blocks against the SDK"),
    ("sdk/test_robot_task.py", "SDK-RT", "RobotTask (communication, synchronization) against the SDK"),
    ("sdk/", "SDK-LOOP", "SDK in the loop (simulator binding)"),
    ("tcp/", "TCP", "TCP transport"),
    (
        "unit/fb/test_interface_spec.py",
        "SPEC-IF",
        "Interfaces of the function blocks against the specification",
    ),
    ("unit/fb/test_payload_spec.py", "SPEC-PAY", "Payload layout against the tables of the specification"),
    ("unit/fb/", "UT-FB", "Function blocks (unit tests without SDK)"),
    ("unit/functions/", "UT-FN", "Functions of the library"),
    ("unit/iec/", "UT-IEC", "IEC 61131-3 runtime (data types, timers, conversions)"),
    ("unit/runtime/", "UT-RUN", "Cyclic runner"),
    ("unit/transport/", "UT-TR", "Transports"),
    ("unit/types/", "UT-TYP", "Generated data types"),
    ("unit/tools/", "UT-TOOL", "Code generators and tools"),
    ("unit/", "UT-PKG", "Package, logging"),
]

PATTERN_ID = re.compile(r"^([A-Z]{2,4}-\d{2})\b")


@dataclass(frozen=True)
class TestFunction:
    test: str  # tests/<path>::<function> (or ::Class::function)
    docstring: str

    @property
    def path(self) -> str:
        return self.test.split("::", 1)[0]


def area_of(test: str) -> tuple[str, str]:
    rel = test.split("::", 1)[0].removeprefix("tests/")
    for prefix, code, name in AREAS:
        if rel.startswith(prefix):
            return code, name
    raise ValueError(f"no area for {test}")


def area_names() -> dict[str, str]:
    names: dict[str, str] = {}
    for _, code, name in AREAS:
        names.setdefault(code, name)
    return names


def scan(root: Path = ROOT) -> list[TestFunction]:
    """All test functions below tests/ (AST, without importing the modules)."""
    found = []
    for path in sorted((root / "tests").rglob("test_*.py")):
        rel = path.relative_to(root).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_"):
                found.append(TestFunction(f"{rel}::{node.name}", ast.get_docstring(node) or ""))
            elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef) and sub.name.startswith("test_"):
                        found.append(
                            TestFunction(f"{rel}::{node.name}::{sub.name}", ast.get_docstring(sub) or "")
                        )
    return found


def split_doc(doc: str) -> tuple[str, str]:
    """(text, reference) of a docstring ``"GEN-05 (Siemens x-06): text"``."""
    text = PATTERN_ID.sub("", " ".join(doc.split())).strip()
    ref = ""
    if text.startswith("("):
        depth = 0
        for i, char in enumerate(text):
            depth += {"(": 1, ")": -1}.get(char, 0)
            if depth == 0:
                ref, text = text[1:i], text[i + 1 :]
                break
    return text.lstrip(" :"), ref


def first_sentence(doc: str) -> str:
    text, _ = split_doc(doc)
    match = re.match(r"(.+?[.!?])(\s|$)", text)
    sentence = (match.group(1) if match else text).strip()
    return sentence[:1].upper() + sentence[1:]


def title_from_name(test: str) -> str:
    name = test.rsplit("::", 1)[1].removeprefix("test_").replace("_", " ")
    return name[:1].upper() + name[1:]


def load(path: Path = REGISTRY) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return list(json.loads(path.read_text(encoding="utf-8")))


def save(entries: list[dict[str, object]], path: Path = REGISTRY) -> None:
    path.write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def update(entries: list[dict[str, object]], functions: list[TestFunction]) -> list[dict[str, object]]:
    """Registry for ``functions``: new tests get the next free ID of their area, removed
    tests are retired, titles follow the docstrings."""
    by_test = {str(e["test"]): dict(e) for e in entries}
    used = {str(e["id"]) for e in entries}
    current = {f.test for f in functions}
    for entry in by_test.values():
        if entry["test"] not in current:
            entry["status"] = "retired"
    for function in functions:
        found = by_test.get(function.test)
        match = PATTERN_ID.match(function.docstring)
        renamed = None
        if found is None and match:
            # pattern ID of a renamed test function: the retired entry moves to the new name
            renamed = next(
                (e for e in by_test.values() if e["id"] == match.group(1) and e["test"] not in current),
                None,
            )
        if found is not None:
            entry = found
        elif renamed is not None:
            del by_test[str(renamed["test"])]
            renamed["test"] = function.test
            by_test[function.test] = renamed
            entry = renamed
        else:
            if match:
                new_id = match.group(1)
            else:
                code, _ = area_of(function.test)
                n = 1 + max(
                    (int(i.rsplit("-", 1)[1]) for i in used if i.rsplit("-", 1)[0] == code), default=0
                )
                new_id = f"{code}-{n:03d}"
            if new_id in used:
                raise ValueError(f"test ID {new_id} of {function.test} is already used")
            used.add(new_id)
            entry = {"id": new_id, "test": function.test, "title": "", "refs": [], "status": "active"}
            by_test[function.test] = entry
        entry["status"] = "active"
        if function.docstring:
            entry["title"] = first_sentence(function.docstring)
            _, ref = split_doc(function.docstring)
            if ref and PATTERN_ID.match(function.docstring):
                entry["refs"] = [ref]
        elif not entry.get("title"):
            entry["title"] = title_from_name(function.test)
    return sorted(by_test.values(), key=lambda e: (area_order(str(e["id"]), str(e["test"])), str(e["id"])))


def area_order(test_id: str, test: str) -> int:
    code, _ = area_of(test)
    codes = list(dict.fromkeys(c for _, c, _ in AREAS))
    return codes.index(code)


def problems(entries: list[dict[str, object]], functions: list[TestFunction]) -> list[str]:
    """Differences between the registry and the test functions (empty: up to date)."""
    found: list[str] = []
    ids = [str(e["id"]) for e in entries]
    found += [f"duplicate test ID {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    expected = update(entries, functions)
    if expected != entries:
        old = {str(e["test"]): e for e in entries}
        for entry in expected:
            if old.get(str(entry["test"])) != entry:
                found.append(
                    f"registry entry out of date: {entry['test']} -> {entry['id']} {entry['title']!r}"
                )
    return found


def lookup(entries: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """``test`` (without parameters) -> registry entry of the active tests."""
    return {str(e["test"]): e for e in entries if e.get("status") == "active"}
