# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_st2py_f28
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    F28: payload order vs. layout of the command structure (``CheckAddParameter``).
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

"""F28: payload order vs. layout of the command structure (``CheckAddParameter``).

``CheckAddParameter`` of the PLC library decides whether a parameter is added by comparing the
bytes of ``_command`` behind the current payload position with zero. That is only correct when
the parameters are added in the order of the structure layout. The function blocks where they
are not get ``CheckAddParameter := TRUE`` (``F28_POUS`` in tools/st2py/config.py). This test
recomputes the list from the generated code, so that a fix in the PLC library (or a new
function block with the problem) is noticed.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path
from typing import Any

from srci.iec import rt
from srci.types import iec
from tools.st2py.config import F28_POUS

FB_ROOT = Path(__file__).resolve().parents[3] / "src" / "srci" / "fb"


def _offset(t: Any, path: list[str | int]) -> int:
    off = 0
    for part in path:
        if isinstance(part, int):
            off += (part - t.lower) * rt.type_size(t.element)
            t = t.element
            continue
        for f in t.struct._IEC_FIELDS_:
            if f.name == part:
                t = f.type
                break
            off += rt.type_size(f.type)
        else:
            raise KeyError(part)
    return off


def _command_path(node: ast.AST) -> list[str | int] | None:
    """``self._command.A.B[2]`` -> ``["A", "B", 2]`` (also inside a conversion call)."""
    for sub in ast.walk(node):
        parts: list[str | int] = []
        e = sub
        while True:
            if isinstance(e, ast.Attribute):
                parts.append(e.attr)
                e = e.value
            elif (
                isinstance(e, ast.Subscript)
                and isinstance(e.slice, ast.Constant)
                and isinstance(e.slice.value, int)
            ):
                parts.append(e.slice.value)
                e = e.value
            else:
                break
        if isinstance(e, ast.Name) and e.id == "self" and parts and parts[-1] == "_command":
            return parts[::-1][1:]
    return None


def _payload_out_of_order(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    if "def CheckAddParameter" not in source:
        return False
    module = importlib.import_module(".".join(path.relative_to(FB_ROOT.parent.parent).with_suffix("").parts))
    fb = getattr(module, path.stem)()
    command = iec.StructType(type(fb._command))
    for fn in ast.walk(ast.parse(source)):
        if not (isinstance(fn, ast.FunctionDef) and fn.name == "CreateCommandPayload"):
            continue
        adds = sorted(
            (c.lineno, p)
            for c in ast.walk(fn)
            if isinstance(c, ast.Call)
            and isinstance(c.func, ast.Attribute)
            and c.func.attr.startswith("Add")
            and c.keywords
            and (p := _command_path(c.keywords[0].value)) is not None
        )
        highest = -1
        for _, p in adds:
            if not p:
                continue
            off = _offset(command, p)
            if off < highest and not str(p[-1]).startswith("Reserve"):
                return True
            highest = max(highest, off)
    return False


def test_f28_list_matches_the_generated_code() -> None:
    found = {p.stem for p in sorted(FB_ROOT.rglob("MC_*FB.py")) if _payload_out_of_order(p)}
    assert found == set(F28_POUS)


def test_write_tool_data_sends_tool_no() -> None:
    """ToolNo is the last payload parameter but the first element of _command."""
    from srci.fb.Write.MC_WriteToolData.MC_WriteToolDataFB import MC_WriteToolDataFB

    fb = MC_WriteToolDataFB()
    fb._command.ToolNo = 3
    assert fb.CheckAddParameter(PayloadPtr=40)
