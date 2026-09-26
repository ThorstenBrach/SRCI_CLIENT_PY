# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.fix_guide
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Generate ``docs/ST_Finding_Solve_Guide.md``: how to fix the findings in the PLC library
#    (ST).
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

"""Generate ``docs/ST_Finding_Solve_Guide.md``: how to fix the findings in the PLC library (ST).

``python -m tools.st2py.fix_guide`` (``--check``: fail if the guide is out of date).

The guide is built from the same corrections the transpiler applies (``tools/st2py/config.py``,
``tools/plcopen_gen/overrides.py``), so every ST diff in it is exactly the change that makes the
Python code correct. The corrections are applied one by one to the ST text of RobotLibrary.xml;
every step is shown as a unified diff of the ST text before and after the step. Fixes that exist
only in hand written Python (telegram coding, conversion functions) are described in
``tools/st2py/fix_guide_manual.md``, which is copied into the guide.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from tools.plcopen_gen import overrides as ov
from tools.plcopen_gen.model import ArrayRef
from tools.plcopen_gen.parser import parse_library

from .__main__ import DEFAULT_XML, ROOT, PatchError, clone_pou
from .config import CONFIG, Config, SourcePatch
from .decl import parse_interface
from .library import Pou, load_pous

GUIDE = ROOT / "docs" / "ST_Finding_Solve_Guide.md"
MANUAL = Path(__file__).with_name("fix_guide_manual.md")
FINDINGS = ROOT / "docs" / "ST_FINDINGS.md"
FINDING = re.compile(r"\bF(\d+)\b")
MAX_FULL = 3  # identical changes in more POUs are listed by name only


def finding_of(reason: str) -> int:
    match = FINDING.search(reason)
    if match is None:
        raise ValueError(f"correction without finding id: {reason!r}")
    return int(match.group(1))


@dataclass
class Step:
    finding: int
    kind: str  # patch, append, variables, clone
    pou: str
    where: str  # method name, "body", "declaration"
    reason: str
    diff: list[str]

    @property
    def key(self) -> tuple[str, ...]:
        """The changed lines only (without context): equal keys = the same change."""
        return (
            self.kind,
            self.where,
            *(line for line in self.diff if line[:1] in "+-" and line[:3] not in ("+++", "---")),
        )


@dataclass
class Guide:
    steps: list[Step] = field(default_factory=list)

    def by_finding(self) -> dict[int, list[Step]]:
        out: dict[int, list[Step]] = {}
        for step in self.steps:
            out.setdefault(step.finding, []).append(step)
        return dict(sorted(out.items()))


def _diff(before: str, after: str, name: str) -> list[str]:
    return list(
        difflib.unified_diff(
            before.splitlines(), after.splitlines(), f"a/{name}", f"b/{name}", n=3, lineterm=""
        )
    )


def _parts(pou: Pou) -> dict[str, str]:
    parts = {"declaration": pou.decl.strip("\n"), "body": pou.body.src.strip("\n")}
    for method in pou.methods.values():
        parts[method.name] = (method.decl.strip("\n") + "\n\n" + method.body.src.strip("\n")).strip("\n")
    return parts


def collect(xml: Path = DEFAULT_XML, cfg: Config = CONFIG) -> Guide:
    """Apply the corrections step by step (order of ``apply_patches``) and record the diffs."""
    pous = load_pous(xml)
    guide = Guide()
    for clone in cfg.clones:
        before = _parts(pous[clone.target.upper()])
        clone_pou(pous, clone)
        after = _parts(pous[clone.target.upper()])
        for name in sorted(set(before) | set(after), key=lambda n: (n not in ("declaration", "body"), n)):
            diff = _diff(before.get(name, ""), after.get(name, ""), f"{clone.target}.{name}")
            if diff:
                guide.steps.append(
                    Step(finding_of(clone.reason), "clone", clone.target, name, clone.reason, diff)
                )
    for var in cfg.variables:
        pou = pous[var.pou.upper()]
        pou.vars.extend(parse_interface(f"FUNCTION_BLOCK {var.pou}\n{var.decl}").vars)
        diff = [f"+{line}" for line in var.decl.splitlines()]
        guide.steps.append(
            Step(finding_of(var.reason), "variables", var.pou, "declaration", var.reason, diff)
        )
    for patch in cfg.patches:
        _apply_patch(pous, patch, guide)
    for append in cfg.appends:
        body = pous[append.pou.upper()].methods[append.method.upper()].body
        old_src = body.src
        body.src = body.src.rstrip() + "\n\n" + append.text
        guide.steps.append(
            Step(
                finding_of(append.reason),
                "append",
                append.pou,
                append.method,
                append.reason,
                _diff(old_src.strip("\n"), body.src.strip("\n"), f"{append.pou}.{append.method}"),
            )
        )
    return guide


def _apply_patch(pous: dict[str, Pou], patch: SourcePatch, guide: Guide) -> None:
    pou = pous[patch.pou.upper()]
    body = pou.body if patch.method is None else pou.methods[patch.method.upper()].body
    before = body.src
    if patch.regex:
        new = patch.new if patch.template else patch.new.replace("\\", "\\\\")
        body.src = re.sub(patch.old, new, body.src)
    else:
        body.src = body.src.replace(patch.old, patch.new)
    if body.src == before:
        raise PatchError(f"patch for {patch.pou}.{patch.method} changes nothing")
    where = patch.method or "body"
    guide.steps.append(
        Step(
            finding_of(patch.reason),
            "patch",
            patch.pou,
            where,
            patch.reason,
            _diff(before.strip("\n"), body.src.strip("\n"), f"{patch.pou}.{where}"),
        )
    )


# ----------------------------------------------------------------------------- rendering


def _titles() -> dict[int, str]:
    """Short problem text of every finding from docs/ST_FINDINGS.md (column "Problem")."""
    out: dict[int, str] = {}
    for line in FINDINGS.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\| F(\d+) \| (.*?) \| (.*?) \|", line)
        if match:
            out[int(match.group(1))] = f"{match.group(2)} - {match.group(3)}"
    return out


def _type_changes() -> list[tuple[int, str]]:
    lib = parse_library(DEFAULT_XML)
    rows: list[tuple[int, str]] = []
    for c in ov.OVERRIDES:
        rows.append((_fid(c.reason), f"Constant `{c.group}.{c.name}` := `{_init(c.init)}` - {c.reason}"))
    for e in ov.ENUM_OVERRIDES:
        rows.append(
            (
                _fid(e.reason),
                f"Enum `{e.enum}.{e.name}` := {e.value} (add the element if missing) - {e.reason}",
            )
        )
    for f in ov.FIELD_OVERRIDES:
        what = []
        if f.init is not None:
            what.append(f"initial value `{_init(f.init)}`")
        if f.doc:
            what.append(f"comment `/// {f.doc}`")
        structs = sorted(
            n
            for n, st in lib.structs.items()
            if ov._matches(f.struct, n) and any(x.name == f.field for x in st.fields)
        )
        names = ", ".join(f"`{n}`" for n in structs)
        rows.append((_fid(f.reason), f"Field `{f.field}` ({', '.join(what)}) in {names} - {f.reason}"))
    for a in ov.FIELD_ADDS:
        pos = f"after `{a.after}`" if a.after else "at the end"
        rows.append(
            (
                _fid(a.reason),
                f"New field in `{a.struct}` ({pos}): `{a.name} : {_type(a.type)};  /// {a.doc}` - {a.reason}",
            )
        )
    return sorted(rows, key=lambda r: r[0])


def _fid(reason: str) -> int:
    match = FINDING.search(reason)
    return int(match.group(1)) if match else 0


def _init(value: object) -> str:
    members = getattr(value, "members", None)
    if members is not None:
        return "(" + ", ".join(f"{name} := {_init(v)}" for name, v in members) + ")"
    text = getattr(value, "text", None) or getattr(value, "value", None)
    return str(text if text is not None else value)


def _type(ref: object) -> str:
    if isinstance(ref, ArrayRef):
        return f"ARRAY[{ref.lower_expr}..{ref.upper_expr}] OF {_type(ref.element)}"
    return str(getattr(ref, "name", ref))


HEADER = """# ST Finding Solve Guide

Generated by `python -m tools.st2py.fix_guide` from the corrections of the transpiler - do not edit;
the hand written part comes from `tools/st2py/fix_guide_manual.md`.
Source: `third_party/robotlibrary/RobotLibrary.xml` (sha256 `{digest}`).
Findings: [ST_FINDINGS.md](ST_FINDINGS.md).

## Instructions for the agent that fixes the PLC library

You fix the findings of the SRCI PLC library (Structured Text, Codesys/TwinCAT) that are already
fixed in the Python port. Every ST change below is **exactly** the change the Python port applies
to the ST text before it transpiles it, so the result is proven by the Python test suite
(unit tests, bilateral tests and the Siemens methodology against the SRCI SDK).

1. **Scope.** Change only what this guide shows. Do not reformat, rename or "improve" other code.
   Keep the comments `// ST-FIX Fnn` of the new code - they mark the fix in the library.
2. **Order.** Work finding by finding in the order of this guide and, inside a finding, step by
   step. The steps are cumulative: the context lines of a step already contain the earlier
   steps (also of earlier findings in the same method).
3. **Diffs.** Each step is a unified diff of one part of a POU (`declaration`, `body` or a
   method). The ST text comes from the XML export; indentation and blank lines in the `.st`
   files may differ - match the lines by content. `-` lines are removed, `+` lines added.
   Where a finding changes the same lines in many POUs, the diff is shown once and the other
   POUs are listed; apply the same change there (the context lines can differ slightly).
4. **Declarations.** "variables" steps add the shown `VAR…END_VAR` / `VAR_INPUT…END_VAR` block to
   the declaration of the POU (merge into an existing section of the same kind if you prefer).
5. **Clones.** "clone" steps replace a POU by a copy of another one (e.g. `MC_OpenBrakeFB` becomes
   an Enable block like `MC_FreeDriveFB`); the diffs show every part against the old POU. New
   methods appear as a diff against an empty text - create them.
6. **Types.** The section *Data types* lists changes of DUTs, enums and constants.
7. **Hand written parts.** The section *Fixes without generated diff* describes fixes that the
   Python port implements in hand written code; implement them as described.
8. **If a diff does not match** the current ST (the library changed since the export): do not
   guess. Stop that finding and report the POU, method and the diff.
9. **Verification** (in the SRCI_PY repository after the fixes):
   1. export the library as PLCopen XML to `third_party/robotlibrary/RobotLibrary.xml`;
   2. `python -m tools.plcopen_gen` - every type override that is now in the XML fails as
      "obsolete": remove it from `tools/plcopen_gen/overrides.py` and run again;
   3. `python -m tools.st2py` - every source patch whose fix is now in the ST fails as
      "obsolete (text not found / no match)": remove it from `tools/st2py/config.py`
      (also `VarAppend`/`BodyAppend`/`PouClone` that now fail) and run again until no error;
   4. `git diff src/` must show no functional change (only comments/whitespace);
   5. `pytest` (with the SDK: `SRCI_SDK_SIM_LIB=…`) - everything green;
   6. `python -m tools.st2py.fix_guide` - the guide then only lists what is still open.

## Overview

| Finding | Problem | Steps | POUs |
|---|---|---:|---|
"""


def render(guide: Guide, digest: str) -> str:
    titles = _titles()
    groups = guide.by_finding()
    types = _type_changes()
    type_ids = {fid for fid, _ in types}
    manual = MANUAL.read_text(encoding="utf-8").strip("\n")
    manual_ids = {int(m) for m in re.findall(r"^### F(\d+)", manual, flags=re.M)}
    out = [HEADER.format(digest=digest[:16])]
    for fid in sorted(set(groups) | type_ids | manual_ids):
        steps = groups.get(fid, [])
        pous = sorted({s.pou for s in steps})
        extra = []
        if fid in type_ids:
            extra.append("data types")
        if fid in manual_ids:
            extra.append("hand written")
        where = ", ".join(f"`{p}`" for p in pous[:4]) + (f" (+{len(pous) - 4})" if len(pous) > 4 else "")
        where = ", ".join(x for x in (where, *extra) if x)
        title = _cell(titles.get(fid, ""))
        out.append(f"| [F{fid}](#f{fid}) | {title} | {len(steps)} | {where} |")
    out += ["", "## Generated ST changes", ""]
    for fid, steps in groups.items():
        out += [f"### F{fid}", "", f"_{_cell(titles.get(fid, ''))}_", ""]
        reasons = list(dict.fromkeys(s.reason for s in steps))
        out += [f"- {r}" for r in reasons] + [""]
        seen: dict[tuple[str, ...], list[Step]] = {}
        for step in steps:
            seen.setdefault(step.key, []).append(step)
        for same in seen.values():
            first = same[0]
            out.append(f"**{first.pou}** · `{first.where}` · {first.kind}")
            out += ["", "```diff", *first.diff, "```", ""]
            if len(same) > 1:
                shown = same[1:MAX_FULL]
                for step in shown:
                    out.append(f"**{step.pou}** · `{step.where}` · {step.kind}")
                    out += ["", "```diff", *step.diff, "```", ""]
                rest = same[MAX_FULL:]
                if rest:
                    names = ", ".join(f"`{s.pou}`" for s in rest)
                    out += [f"Same change (same `-`/`+` lines) in: {names}", ""]
    out += ["## Data types", "", "Change the DUTs / enums / constants of the library:", ""]
    out += [f"- **F{fid}** {text}" if fid else f"- {text}" for fid, text in types]
    out += ["", "## Fixes without generated diff", "", manual, ""]
    return "\n".join(out)


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def build(xml: Path = DEFAULT_XML) -> str:
    digest = hashlib.sha256(xml.read_bytes()).hexdigest()
    return render(collect(xml), digest)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.st2py.fix_guide", description=__doc__)
    ap.add_argument("--xml", type=Path, default=DEFAULT_XML)
    ap.add_argument("--check", action="store_true", help="fail if the guide is out of date")
    args = ap.parse_args(argv)
    text = build(args.xml)
    if args.check:
        if not GUIDE.exists() or GUIDE.read_text(encoding="utf-8") != text:
            print(
                f"out of date: {GUIDE.relative_to(ROOT)} - run: python -m tools.st2py.fix_guide",
                file=sys.stderr,
            )
            return 1
        print(f"{GUIDE.relative_to(ROOT)} is up to date")
        return 0
    GUIDE.write_text(text, encoding="utf-8", newline="\n")
    print(f"-> {GUIDE.relative_to(ROOT)} ({text.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
