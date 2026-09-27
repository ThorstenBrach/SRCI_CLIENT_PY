# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.export_xml
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Write the corrections of the Python port back into the PLCopen XML of the PLC library.
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

"""Write the corrections of the Python port back into the PLCopen XML of the PLC library.

``python -m tools.st2py.export_xml -o RobotLibrary_fixed.xml`` (``--verify``: check the result).

The Python port applies its corrections of the ST code (``tools/st2py/config.py``) and of the
data types (``tools/plcopen_gen/overrides.py``) while it reads ``RobotLibrary.xml``. This tool
applies exactly the same corrections to the XML file itself, so the fixed library can be
imported into TwinCAT / Codesys ("Import PLCopenXML", replace the existing objects):

* only the changed objects are rewritten, everything else stays byte-identical;
* object IDs (GUIDs), folders, attributes and access modifiers are kept; methods that a clone
  (``PouClone``) adds get new, stable object IDs;
* declarations are written twice, as the plain text declaration (``InterfaceAsPlainText``, used
  by the IDE) and as structured PLCopen interface (variables added/removed by name).

``--verify`` proves that the XML contains all corrections: the generators read the fixed XML
**without** any correction (only the hand written Python parts stay) and must produce the same
types and function blocks as from the original XML with the corrections.

Not in the XML: the fixes that exist only in hand written Python (``Mixin``, see the section
"Fixes without generated diff" of ``docs/ST_Finding_Solve_Guide.md``).
"""

from __future__ import annotations

import argparse
import ast
import html
import re
import sys
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from tools.plcopen_gen.model import (
    ArrayRef,
    DerivedRef,
    ElemRef,
    InitValue,
    SimpleValue,
    StringRef,
    StructValue,
    TypeRef,
)
from tools.plcopen_gen.overrides import (
    ENUM_OVERRIDES,
    FIELD_ADDS,
    FIELD_OVERRIDES,
    OVERRIDES,
    EnumOverride,
    FieldAdd,
    FieldOverride,
    _matches,
)

from .config import CONFIG, Config, PouClone
from .decl import ELEMENTARY, TArray, TElem, TNamed, TString, parse_interface
from .library import Pou, load_pous

__all__ = ["ExportError", "ExportResult", "export", "verify"]

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_XML = ROOT / "third_party" / "robotlibrary" / "RobotLibrary.xml"
XHTML = '<xhtml xmlns="http://www.w3.org/1999/xhtml">'
_UUID_NS = uuid.UUID("6f1c2d7e-5a43-4c1b-9e0e-5c2b8f3a7d10")  # stable IDs of added methods

_SECTION_TAG = {"input": "inputVars", "output": "outputVars", "inout": "inOutVars", "local": "localVars",
                "temp": "tempVars"}  # fmt: skip
_TAG_SECTION = {v: k for k, v in _SECTION_TAG.items()}


class ExportError(Exception):
    pass


@dataclass
class ExportResult:
    xml: str
    changed: list[str] = field(default_factory=list)  # "POU", "POU.Method", "type X"
    delete: list[str] = field(default_factory=list)  # objects to delete by hand after the import


# ---------------------------------------------------------------------- text helpers


def _x(text: str) -> str:
    return escape(text)  # the export escapes only & < >


def _block(text: str, start: int, open_tag: str, close_tag: str) -> tuple[int, int]:
    """Start and end (behind the close tag) of the element starting at ``start``."""
    end = text.find(close_tag, start)
    if end < 0:
        raise ExportError(f"{open_tag}: no {close_tag}")
    return start, end + len(close_tag)


def _find_element(
    text: str, open_prefix: str, close_tag: str, lo: int = 0, hi: int | None = None
) -> tuple[int, int]:
    hi = len(text) if hi is None else hi
    i = text.find(open_prefix, lo, hi)
    if i < 0:
        raise ExportError(f"{open_prefix} not found")
    if text.find(open_prefix, i + 1, hi) >= 0:
        raise ExportError(f"{open_prefix} is not unique")
    return _block(text, i, open_prefix, close_tag)


def _replace_xhtml(block: str, anchor: str, new_text: str, what: str) -> str:
    """Replace the xhtml text of the first ``anchor`` element (``<ST>``, ``<InterfaceAsPlainText>``)."""
    m = re.compile(re.escape(anchor) + r"\s*" + r"(?:" + re.escape(XHTML) + r"(.*?)</xhtml>|<xhtml [^>]*/>)",
                   re.S).search(block)  # fmt: skip
    if m is None:
        raise ExportError(f"{what}: {anchor} not found")
    head = block[m.start() : m.start() + len(anchor)]
    ws = block[m.start() + len(anchor) : m.start() + len(anchor) + (len(m.group(0)) - len(anchor))]
    ws = ws[: len(ws) - len(ws.lstrip())]
    return block[: m.start()] + head + ws + XHTML + _x(new_text) + "</xhtml>" + block[m.end() :]


def _indent_of(text: str, pos: int) -> str:
    line = text.rfind("\n", 0, pos) + 1
    return text[line:pos]


def _reindent(xml: str, indent: str) -> str:
    return "\n".join((indent + line) if line else line for line in xml.split("\n"))


# ---------------------------------------------------------------------- PLCopen snippets


def _type_xml(t: TypeRef) -> str:
    if isinstance(t, ElemRef):
        return f"<{t.name} />"
    if isinstance(t, DerivedRef):
        return f'<derived name="{t.name}" />'
    if isinstance(t, StringRef):
        return f'<string length="{_x(t.length_expr)}" />'
    if isinstance(t, ArrayRef):
        return (f'<array>\n  <dimension lower="{t.lower_expr}" upper="{t.upper_expr}" />\n  <baseType>\n'
                f"{_reindent(_type_xml(t.element), '    ')}\n  </baseType>\n</array>")  # fmt: skip
    raise ExportError(f"type {t!r} not supported")


def _value_xml(v: InitValue) -> str:
    if isinstance(v, SimpleValue):
        return f'<simpleValue value="{_x(v.text)}" />'
    if isinstance(v, StructValue):
        members = "\n".join(
            f'  <value member="{name}">\n{_reindent(_value_xml(val), "    ")}\n  </value>'
            for name, val in v.members
        )
        return f"<structValue>\n{members}\n</structValue>"
    raise ExportError(f"initial value {v!r} not supported")


def _doc_xml(doc: str) -> str:
    return f"<documentation>\n  {XHTML}{_x(doc)}</xhtml>\n</documentation>"


def _variable_xml(name: str, t: TypeRef, init: InitValue | None, doc: str) -> str:
    parts = [f'<variable name="{name}">', "  <type>", _reindent(_type_xml(t), "    "), "  </type>"]
    if init is not None:
        parts += ["  <initialValue>", _reindent(_value_xml(init), "    "), "  </initialValue>"]
    if doc:
        parts.append(_reindent(_doc_xml(doc), "  "))
    parts.append("</variable>")
    return "\n".join(parts)


# ---------------------------------------------------------------------- declarations


_DECL_LINE = re.compile(r"^\s*(\w+)\s*:\s*([^;:=]+?)\s*(?::=\s*([^;]+?))?\s*;\s*(?://\s*(.*))?$")


def _decl_type(text: str) -> TypeRef:
    t = text.strip()
    if t.upper() in ELEMENTARY:
        return ElemRef(t.upper())
    if re.fullmatch(r"\w+", t):
        return DerivedRef(t)
    raise ExportError(f"declaration type {t!r} not supported (only elementary and named types)")


@dataclass
class _Var:
    name: str
    section: str
    type: TypeRef
    init: InitValue | None
    doc: str


def _vars_of_decl(decl: str) -> list[_Var]:
    """Variables of a simple declaration text (``VAR_x ... END_VAR`` blocks, one variable per line,
    ``///`` doc lines or ``//`` trailing comment)."""
    out: list[_Var] = []
    section: str | None = None
    doc: list[str] = []
    sections = {"VAR_INPUT": "input", "VAR_OUTPUT": "output", "VAR_IN_OUT": "inout", "VAR": "local",
                "VAR_TEMP": "temp"}  # fmt: skip
    for line in decl.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.upper() in sections:
            section, doc = sections[s.upper()], []
        elif s.upper() == "END_VAR":
            section = None
        elif s.startswith("///"):
            doc.append(s[3:].strip())
        elif section is not None and (m := _DECL_LINE.match(s)):
            init = SimpleValue(m.group(3).strip()) if m.group(3) else None
            text = " ".join([*doc, m.group(4) or ""]).strip()
            out.append(_Var(m.group(1), section, _decl_type(m.group(2)), init, text))
            doc = []
        else:
            raise ExportError(f"declaration line {s!r} not supported")
    return out


def _decl_type_of(t: object) -> TypeRef:
    if isinstance(t, TElem):
        return ElemRef(t.name)
    if isinstance(t, TNamed):
        return DerivedRef(t.name)
    if isinstance(t, (TString, TArray)):
        raise ExportError("string/array variables must be added with an explicit declaration text")
    raise ExportError(f"type {t!r} not supported")


def _interface_vars(itf: str) -> list[tuple[str, str]]:
    """(section, name) of the structured PLCopen interface (without method interfaces)."""
    out = []
    for m in re.finditer(
        r"<(inputVars|outputVars|inOutVars|localVars|tempVars)\b[^>]*>(.*?)</\1>", itf, re.S
    ):
        for v in re.finditer(r'<variable name="([^"]+)"', m.group(2)):
            out.append((_TAG_SECTION[m.group(1)], v.group(1)))
    return out


def _sync_interface(itf: str, decl: str, added: dict[str, _Var], what: str) -> str:
    """Make the structured interface match the plain text declaration: remove the variables that
    are no longer declared, add the new ones (``added``: their simple declaration), adapt EXTENDS."""
    parsed = parse_interface(decl)
    # compared by name: the export puts e.g. VAR_IN_OUT pointers of MC_RobotTaskFB into inputVars
    want = [(v.section, v.name) for v in parsed.vars]
    want_names = {n for _, n in want}
    have = _interface_vars(itf)
    have_names = {n for _, n in have}
    for section, name in have:
        if name in want_names:
            continue
        tag = _SECTION_TAG[section]
        sec = re.search(rf"<{tag}\b[^>]*>.*?</{tag}>", itf, re.S)
        assert sec is not None
        body = re.sub(rf'\n[ \t]*<variable name="{re.escape(name)}">.*?</variable>', "", sec.group(0), count=1,
                      flags=re.S)  # fmt: skip
        if not re.search(r"<variable ", body):
            start = itf.rfind("\n", 0, sec.start())
            itf = itf[:start] + itf[sec.end() :]
        else:
            itf = itf[: sec.start()] + body + itf[sec.end() :]
    for section, name in want:
        if name in have_names:
            continue
        var = added.get(name)
        if var is None:
            decl_var = next(v for v in parsed.vars if v.name == name)
            raise ExportError(
                f"{what}: variable {name} ({decl_var.section}) is new but has no simple declaration"
            )
        tag = _SECTION_TAG[section]
        ends = [
            m.end() for m in re.finditer(r"</(?:inputVars|outputVars|inOutVars|localVars|tempVars)>", itf)
        ]
        if ends:
            pos = ends[-1]
        else:
            rt = itf.find("</returnType>")
            pos = rt + len("</returnType>") if rt >= 0 else itf.find(">") + 1
        indent = _indent_of(itf, itf.find("<", itf.find("<") + 1)) if not ends else _indent_of(
            itf, itf.rfind("<", 0, pos))  # fmt: skip
        snippet = (
            f"<{tag}>\n{_reindent(_variable_xml(var.name, var.type, var.init, var.doc), '  ')}\n</{tag}>"
        )
        itf = itf[:pos] + "\n" + _reindent(snippet, indent) + itf[pos:]
    ext = parsed.header.extends[0] if parsed.header.extends else None
    m = re.search(r"<Extends>([^<]*)</Extends>", itf)
    if m and ext and m.group(1) != ext:
        itf = itf[: m.start(1)] + ext + itf[m.end(1) :]
    elif bool(m) != bool(ext):
        raise ExportError(f"{what}: EXTENDS added/removed - not supported")
    after = sorted(n for _, n in _interface_vars(itf))
    if after != sorted(want_names):
        raise ExportError(
            f"{what}: structured interface does not match the declaration: {after} != {sorted(want_names)}"
        )
    return itf


# ---------------------------------------------------------------------- POUs


def _pou_span(text: str, name: str) -> tuple[int, int]:
    return _find_element(text, f'<pou name="{name}" ', "</pou>")


def _method_spans(pou: str) -> dict[str, tuple[int, int]]:
    out = {}
    for m in re.finditer(r'<data name="http://www\.3s-software\.com/plcopenxml/method"[^>]*>\s*<Method name="([^"]+)"',
                         pou):  # fmt: skip
        start = pou.rfind("\n", 0, m.start()) + 1
        end = pou.find("</data>", pou.find("</Method>", m.start())) + len("</data>")
        out[m.group(1).upper()] = (start, end)
    return out


def _pou_level_regions(pou: str) -> tuple[int, int]:
    """End of the POU interface and start of the method data (region of the POU body)."""
    itf_end = pou.find("</interface>") + len("</interface>")
    spans = _method_spans(pou)
    first = min((s for s, _ in spans.values()), default=len(pou))
    return itf_end, first


def _replace_pou_body(pou: str, new: str, what: str) -> str:
    lo, hi = _pou_level_regions(pou)
    if pou.find("<body>", lo, hi) < 0:
        raise ExportError(f"{what}: no body")
    return pou[:lo] + _replace_xhtml(pou[lo:hi], "<ST>", new, what) + pou[hi:]


def _replace_pou_plain(pou: str, new: str, what: str) -> str:
    anchor = '<data name="http://www.3s-software.com/plcopenxml/interfaceasplaintext"'
    i = pou.rfind(anchor)
    if i < 0:
        raise ExportError(f"{what}: no plain text declaration")
    return pou[:i] + _replace_xhtml(pou[i:], "<InterfaceAsPlainText>", new, what) + ""


def _replace_pou_interface(pou: str, decl: str, added: dict[str, _Var], what: str) -> str:
    i = pou.find("<interface>")
    j = pou.find("</interface>") + len("</interface>")
    return pou[:i] + _sync_interface(pou[i:j], decl, added, what) + pou[j:]


def _update_method(block: str, body: str | None, decl: str | None, what: str) -> str:
    if body is not None:
        block = _replace_xhtml(block, "<ST>", body, what)
    if decl is not None:
        block = _replace_xhtml(block, "<InterfaceAsPlainText>", decl, what)
    return block


def _added_decls(cfg: Config) -> tuple[dict[str, str], dict[str, dict[str, _Var]]]:
    """Declaration text appended per POU and the variables it declares (VarAppend)."""
    text: dict[str, str] = {}
    variables: dict[str, dict[str, _Var]] = {}
    for var in cfg.variables:
        key = var.pou.upper()
        text[key] = text.get(key, "") + "\n" + var.decl.strip() + "\n"
        for v in _vars_of_decl(var.decl):
            variables.setdefault(key, {})[v.name] = v
    return text, variables


def _clone_block(text: str, clone: PouClone, final: Pou, orig: dict[str, Pou], result: ExportResult) -> str:
    """New ``<pou>`` element of a cloned POU (see :class:`PouClone`); texts and the structured
    interface are updated afterwards like for every changed POU."""
    s0, s1 = _pou_span(text, clone.source)
    t0, t1 = _pou_span(text, clone.target)
    src, tgt = text[s0:s1], text[t0:t1]

    def fix(xml: str) -> str:
        for old, new in clone.replacements:
            xml = xml.replace(_x(old), _x(new))
        return xml

    tgt_methods = _method_spans(tgt)
    src_methods = _method_spans(src)
    if not tgt_methods or not src_methods:
        raise ExportError(f"clone {clone.target}: POUs without methods are not supported")

    def itf_of(pou: str) -> tuple[int, int]:
        return pou.find("<interface>"), pou.find("</interface>") + len("</interface>")

    si0, si1 = itf_of(src)
    ti0, ti1 = itf_of(tgt)
    itf = tgt[ti0:ti1] if clone.target_decl is not None else fix(src[si0:si1])
    keep = {m.upper() for m in clone.keep_methods}
    blocks = []
    for key in final.methods:
        if key in keep:
            a, b = tgt_methods[key]
            blocks.append(tgt[a:b])
        else:
            a, b = src_methods[key]
            old_id = (
                re.search(r'<Method name="[^"]+" ObjectId="([^"]+)"', tgt[slice(*tgt_methods[key])])
                if key in tgt_methods
                else None
            )
            new_id = (
                old_id.group(1)
                if old_id
                else uuid.uuid5(_UUID_NS, f"{clone.target}.{final.methods[key].name}")
            )
            block = re.sub(
                r'(<Method name="[^"]+" ObjectId=")[^"]+"', rf'\g<1>{new_id}"', fix(src[a:b]), count=1
            )
            blocks.append(block)
    for key, method in orig[clone.target.upper()].methods.items():
        if key not in final.methods:
            result.delete.append(f"{clone.target}.{method.name}")
    first_src = min(a for a, _ in src_methods.values())
    last_tgt = max(b for _, b in tgt_methods.values())
    head = tgt[: tgt.find(">") + 1]
    return head + src[src.find(">") + 1 : si0] + itf + src[si1:first_src] + "\n".join(blocks) + tgt[last_tgt:]


def _structure_children(text: str, pou: str, methods: list[tuple[str, str]]) -> str:
    """Methods of a POU in the ProjectStructure (name, object id)."""
    m = re.search(rf'(\n[ \t]*)<Object Name="{re.escape(pou)}" ObjectId="[^"]+">(.*?)\1</Object>', text, re.S)
    if m is None:
        raise ExportError(f"{pou} not found in the ProjectStructure")
    indent = m.group(1) + "  "
    children = "".join(
        f'{indent}<Object Name="{n}" ObjectId="{i}" />'
        for n, i in sorted(methods, key=lambda x: x[0].upper())
    )
    return text[: m.start(2)] + children + text[m.end(2) :]


# ---------------------------------------------------------------------- data types


def _type_span(text: str, name: str) -> tuple[int, int]:
    return _find_element(text, f'<dataType name="{name}">', "</dataType>")


def _gvl_span(text: str, name: str) -> tuple[int, int]:
    """``<globalVars>`` element and its addData (with the plain text declaration)."""
    a, _ = _find_element(text, f'<globalVars name="{name}"', "</globalVars>")
    start = text.rfind("\n", 0, text.rfind("<data ", 0, a)) + 1
    end = text.find("</data>", text.find("interfaceasplaintext", a)) + len("</data>")
    return start, end


def _struct_names(text: str) -> list[str]:
    return re.findall(r'<dataType name="([^"]+)">\s*<baseType>\s*<struct', text)


def _struct_field_span(block: str, fld: str) -> tuple[int, int] | None:
    m = re.search(rf'\n[ \t]*<variable name="{re.escape(fld)}">.*?</variable>', block, re.S)
    return (m.start(), m.end()) if m else None


def _set_init(var: str, init: InitValue | None) -> str:
    if init is None:
        return var
    indent = _indent_of(var, var.find("<type>"))
    new = _reindent(f"<initialValue>\n{_reindent(_value_xml(init), '  ')}\n</initialValue>", indent)
    m = re.search(r"\n[ \t]*<initialValue>.*?</initialValue>", var, re.S)
    if m:
        return var[: m.start()] + "\n" + new + var[m.end() :]
    t = var.find("</type>") + len("</type>")
    return var[:t] + "\n" + new + var[t:]


def _set_doc(var: str, doc: str) -> str:
    m = re.search(rf"({re.escape(XHTML)})(.*?)(</xhtml>)", var, re.S)
    if m:
        return var[: m.start(2)] + _x(" " + doc) + var[m.end(2) :]
    indent = _indent_of(var, var.find("<type>"))
    end = var.rfind("</variable>")
    line = var.rfind("\n", 0, end)
    return var[:line] + "\n" + _reindent(_doc_xml(" " + doc), indent) + var[line:]


def _fix_note(reason: str) -> str:
    reason = reason.strip()
    return reason if reason.startswith("ST-FIX") else f"ST-FIX {reason}"


# plain text declarations of types and global variables


def _get_plain(block: str) -> str:
    m = re.search(r"<InterfaceAsPlainText>\s*" + re.escape(XHTML) + r"(.*?)</xhtml>", block, re.S)
    if m is None:
        raise ExportError("plain text declaration not found")
    return html.unescape(m.group(1))


def _set_plain(block: str, plain: str, what: str) -> str:
    return _replace_xhtml(block, "<InterfaceAsPlainText>", plain, what)


def _st_type(t: TypeRef) -> str:
    if isinstance(t, (ElemRef, DerivedRef)):
        return t.name
    if isinstance(t, ArrayRef):
        return f"ARRAY[{t.lower_expr}..{t.upper_expr}] OF {_st_type(t.element)}"
    if isinstance(t, StringRef):
        return f"STRING({t.length_expr})"
    raise ExportError(f"type {t!r} not supported")


def _st_value(v: InitValue) -> str:
    if isinstance(v, SimpleValue):
        return v.text
    if isinstance(v, StructValue):
        return "( " + ", ".join(f"{n} := {_st_value(x)}" for n, x in v.members) + ")"
    raise ExportError(f"initial value {v!r} not supported")


def _plain_field(plain: str, name: str) -> re.Match[str]:
    m = re.search(rf"^([ \t]*{re.escape(name)}\s*:\s*)([^;]*?)(\s*;.*)$", plain, re.M)
    if m is None:
        raise ExportError(f"declaration of {name} not found in the plain text")
    return m


def _plain_set_init(plain: str, name: str, init: InitValue) -> str:
    m = _plain_field(plain, name)
    decl_type = m.group(2).split(":=")[0].rstrip()
    return plain[: m.start(2)] + f"{decl_type} := {_st_value(init)}" + plain[m.end(2) :]


def _plain_insert_field(plain: str, after: str | None, line: str) -> str:
    if after is not None:
        m = _plain_field(plain, after)
        return plain[: m.end()] + "\n" + line + plain[m.end() :]
    end = re.search(r"^[ \t]*END_STRUCT", plain, re.M)
    if end is None:
        raise ExportError("END_STRUCT not found in the plain text")
    return plain[: end.start()] + line + "\n" + plain[end.start() :]


def _plain_enum(plain: str, name: str, value: int, note: str) -> str:
    text = f"16#{value:04X}" if "16#" in plain else str(value)
    m = re.search(rf"^([ \t]*{re.escape(name)}\s*:=\s*)([^,\s/]+)", plain, re.M)
    if m:
        return plain[: m.start(2)] + text + plain[m.end(2) :]
    elems = list(re.finditer(r"^([ \t]*)\w+\s*:=\s*[^,\s/]+(,?)", plain, re.M))
    if not elems:
        raise ExportError(f"enum {name}: no elements in the plain text")
    last = elems[-1]
    if not last.group(2):
        plain = plain[: last.end()] + "," + plain[last.end() :]
        last = list(re.finditer(r"^([ \t]*)\w+\s*:=\s*[^,\s/]+(,?)", plain, re.M))[-1]
    eol = plain.find("\n", last.end())
    new = f"\n{last.group(1)}/// {note}\n{last.group(1)}{name} := {text}"
    return plain[:eol] + new + plain[eol:]


def _int(v: str) -> int:
    v = v.replace("_", "")
    return int(v[3:], 16) if v.startswith("16#") else int(v)


def _type_items(block: str) -> tuple[set[object], set[object]]:
    """(structured, plain text) fields of a struct resp. (name, value) of an enum."""
    plain = re.sub(r"\(\*.*?\*\)", "", _get_plain(block), flags=re.S)
    code = "\n".join(line.split("//")[0] for line in plain.splitlines())
    if "<enum>" in block:
        want: set[object] = {
            (n, _int(v)) for n, v in re.findall(r'<value name="([^"]+)" value="([^"]+)" />', block)
        }
        have: set[object] = set()
        for n, v in re.findall(r"^[ \t]*(\w+)\s*:=\s*(16#[0-9A-Fa-f_]+|-?\d+)", code, re.M):
            have.add((n, _int(v)))
        return set(want), have
    want_f = set(re.findall(r'<variable name="([^"]+)">', block))
    have_f = set(re.findall(r"^[ \t]*(\w+)\s*:(?!=)", code[code.find("STRUCT") :], re.M))
    return set(want_f), set(have_f)


def _check_plain_type(before: str, after: str, what: str) -> None:
    """Structured type and plain text declaration got the same changes."""
    w0, h0 = _type_items(before)
    w1, h1 = _type_items(after)
    if (w1 - w0, w0 - w1) != (h1 - h0, h0 - h1):
        raise ExportError(f"{what}: structured and plain text changes differ: {w1 ^ w0} / {h1 ^ h0}")


def _apply_types(text: str, result: ExportResult) -> str:
    def edit_type(name: str, fn: Callable[[str], str]) -> None:
        nonlocal text
        a, b = _type_span(text, name)
        block = fn(text[a:b])
        _check_plain_type(text[a:b], block, name)
        text = text[:a] + block + text[b:]

    for ov in ENUM_OVERRIDES:
        note = _fix_note(ov.reason)

        def enum(block: str, ov: EnumOverride = ov, note: str = note) -> str:
            m = re.search(rf'<value name="{re.escape(ov.name)}" value="([^"]*)" />', block)
            if m:
                value = f"16#{ov.value:04X}" if m.group(1).startswith("16#") else str(ov.value)
                block = block[: m.start(1)] + value + block[m.end(1) :]
            else:
                last = list(re.finditer(r'\n([ \t]*)<value name="[^"]+" value="[^"]*" />', block))[-1]
                new = f'\n{last.group(1)}<value name="{ov.name}" value="{ov.value}" />'
                block = block[: last.end()] + new + block[last.end() :]
                docs = list(re.finditer(r"\n([ \t]*)<EnumValue>.*?</EnumValue>", block, re.S))
                if docs:
                    ind = docs[-1].group(1)
                    entry = (f"\n{ind}<EnumValue>\n{ind}  <Name>{ov.name}</Name>\n{ind}  <Documentation>\n"
                             f"{ind}    {XHTML}{_x(' ' + note)}</xhtml>\n{ind}  </Documentation>\n"
                             f"{ind}</EnumValue>")  # fmt: skip
                    block = block[: docs[-1].end()] + entry + block[docs[-1].end() :]
            return _set_plain(block, _plain_enum(_get_plain(block), ov.name, ov.value, note), ov.enum)

        edit_type(ov.enum, enum)
        result.changed.append(f"type {ov.enum}")
    for fov in FIELD_OVERRIDES:
        found = 0
        for struct in _struct_names(text):
            if not _matches(fov.struct, struct):
                continue
            a, b = _type_span(text, struct)
            if _struct_field_span(text[a:b], fov.field) is None:
                continue
            found += 1

            def field_ov(block: str, fov: FieldOverride = fov) -> str:
                span = _struct_field_span(block, fov.field)
                assert span is not None
                var = _set_init(block[span[0] : span[1]], fov.init)
                note = _fix_note(fov.reason)
                if fov.doc:
                    var = _set_doc(var, f"{fov.doc} ({note})")
                block = block[: span[0]] + var + block[span[1] :]
                plain = _get_plain(block)
                if fov.init is not None:
                    plain = _plain_set_init(plain, fov.field, fov.init)
                    m = _plain_field(plain, fov.field)
                    if "//" not in m.group(3):
                        plain = plain[: m.end()] + f" // {note}" + plain[m.end() :]
                if fov.doc:
                    m = _plain_field(plain, fov.field)
                    ind = m.group(1)[: len(m.group(1)) - len(m.group(1).lstrip())]
                    plain = plain[: m.start()] + f"{ind}/// {fov.doc} ({note})\n" + plain[m.start() :]
                return _set_plain(block, plain, fov.field)

            edit_type(struct, field_ov)
            result.changed.append(f"type {struct}")
        if not found:
            raise ExportError(f"field override {fov.struct}.{fov.field} not found")
    for add in FIELD_ADDS:

        def field_add(block: str, add: FieldAdd = add) -> str:
            note = _fix_note(add.reason)
            var = _variable_xml(add.name, add.type, None, f" {add.doc} ({note})")
            if re.search(r"<struct\s*/>", block):
                m = re.search(r"\n([ \t]*)<struct\s*/>", block)
                assert m is not None
                ind = m.group(1)
                inner = _reindent(var, ind + "  ")
                block = block[: m.start()] + f"\n{ind}<struct>\n{inner}\n{ind}</struct>" + block[m.end() :]
            else:
                if add.after is not None:
                    span = _struct_field_span(block, add.after)
                    if span is None:
                        raise ExportError(f"field add {add.struct}: field {add.after} not found")
                    pos = span[1]
                else:
                    pos = block.rfind("</variable>") + len("</variable>")
                indent = _indent_of(block, block.rfind("<variable ", 0, pos))
                block = block[:pos] + "\n" + _reindent(var, indent) + block[pos:]
            plain = _get_plain(block)
            line = f"  /// {add.doc} ({note})\n  {add.name} : {_st_type(add.type)};"
            return _set_plain(block, _plain_insert_field(plain, add.after, line), add.struct)

        edit_type(add.struct, field_add)
        result.changed.append(f"type {add.struct}")
    for cov in OVERRIDES:
        a, b = _gvl_span(text, cov.group)
        block = text[a:b]
        span = _struct_field_span(block, cov.name)
        if span is None:
            raise ExportError(f"constant {cov.group}.{cov.name} not found")
        var = _set_init(block[span[0] : span[1]], cov.init)
        block = block[: span[0]] + var + block[span[1] :]
        plain = _plain_set_init(_get_plain(block), cov.name, cov.init)
        m = _plain_field(plain, cov.name)
        plain = plain[: m.end()] + f" // {_fix_note(cov.reason)[:100]}" + plain[m.end() :]
        text = text[:a] + _set_plain(block, plain, cov.group) + text[b:]
        result.changed.append(f"GVL {cov.group}")
    return text


# ---------------------------------------------------------------------- export


def _read(xml: Path) -> tuple[str, bool, bool]:
    raw = xml.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    crlf = "\r\n" in text
    return text.replace("\r\n", "\n"), bom, crlf


def _check_roundtrip(text: str, xml: Path) -> None:
    """Every body/declaration is written back with the same escaping as the export."""
    root = ET.fromstring(text)
    ns = "{http://www.plcopen.org/xml/tc6_0200}"
    for st in list(root.iter(f"{ns}ST"))[:200]:
        x = st.find("{http://www.w3.org/1999/xhtml}xhtml")
        if x is None or x.text is None:
            continue
        if XHTML + _x(x.text) + "</xhtml>" not in text:
            raise ExportError(f"{xml.name}: escaping differs from the export - the tool must be adapted")


def _check_enum_literals(text: str, pous: dict[str, Pou]) -> None:
    """``Type.VALUE`` must not be used where a variable has the name of the enum type (e.g. the
    input ``ProcessingMode : ProcessingMode``): the compiler reads it as member access on the
    variable - the library uses the alias types (``ProcessingModeEnum``) there."""
    enums = set(re.findall(r'<dataType name="([^"]+)">\s*<baseType>\s*<enum>', text))
    problems = []
    for pou in pous.values():
        if pou.kind == "INTERFACE":
            continue
        names: set[str] = set()
        cur: Pou | None = pou
        while cur is not None:
            names |= {v.name for v in cur.vars}
            cur = pous.get(cur.extends.upper()) if cur.extends else None
        parts: list[tuple[str, str, set[str]]] = [("body", pou.body.src, set())] + [
            (m.name, m.body.src, {v.name for v in m.vars}) for m in pou.methods.values()
        ]
        for part, src, local in parts:
            for enum in enums & (names | local):
                for m in re.finditer(rf"(?<![.\w]){enum}\.[A-Z_]\w*", src):
                    problems.append(f"{pou.name}.{part}: {m.group(0)}")
    if problems:
        raise ExportError(
            "enum literal hidden by a variable of the same name: " + ", ".join(sorted(set(problems)))
        )


def _well_formed(text: str) -> None:
    ET.fromstring(text)


def export(xml: Path = DEFAULT_XML, cfg: Config = CONFIG) -> ExportResult:
    text, bom, crlf = _read(xml)
    _check_roundtrip(text, xml)
    orig = load_pous(xml)
    final = load_pous(xml)
    from .__main__ import apply_patches  # the same corrections as the transpiler

    apply_patches(final, cfg)
    _check_enum_literals(text, final)
    add_text, add_vars = _added_decls(cfg)
    result = ExportResult("")
    clones = {c.target.upper(): c for c in cfg.clones}

    for key, pou in final.items():
        before = orig.get(key)
        if before is None or pou.kind == "INTERFACE":
            continue
        decl = pou.decl + add_text.get(key, "")
        cloned = key in clones
        if cloned:
            a, b = _pou_span(text, clones[key].target)
            block = _clone_block(text, clones[key], pou, orig, result)
            text = text[:a] + block + text[b:]
            methods = [(m.name, "") for m in pou.methods.values()]
            a, b = _pou_span(text, pou.name)
            ids = dict(re.findall(r'<Method name="([^"]+)" ObjectId="([^"]+)"', text[a:b]))
            text = _structure_children(text, pou.name, [(n, ids[n]) for n, _ in methods])
        a, b = _pou_span(text, pou.name)
        block = text[a:b]
        changed = cloned
        if cloned or pou.body.src != before.body.src:
            block = _replace_pou_body(block, pou.body.src, pou.name)
            changed = True
        if cloned or decl != before.decl:
            block = _replace_pou_plain(block, decl, pou.name)
            block = _replace_pou_interface(block, decl, add_vars.get(key, {}), pou.name)
            changed = True
        spans = _method_spans(block)
        for mkey, method in sorted(pou.methods.items(), key=lambda kv: -spans[kv[0]][0]):
            old = before.methods.get(mkey)
            new_body = method.body.src if cloned or old is None or method.body.src != old.body.src else None
            new_decl = method.decl if cloned or old is None or method.decl != old.decl else None
            if new_body is None and new_decl is None:
                continue
            s, e = spans[mkey]
            block = (
                block[:s]
                + _update_method(block[s:e], new_body, new_decl, f"{pou.name}.{method.name}")
                + block[e:]
            )
            if not cloned:
                result.changed.append(f"{pou.name}.{method.name}")
        if changed:
            result.changed.append(pou.name)
        text = text[:a] + block + text[b:]

    text = _apply_types(text, result)
    _well_formed(text)
    out = text.replace("\n", "\r\n") if crlf else text
    result.xml = ("﻿" if bom else "") + out
    result.changed = sorted(set(result.changed))
    return result


# ---------------------------------------------------------------------- verification


def _strip(source: str) -> str:
    """Python source without comments and doc strings (for the comparison)."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        for name in ("body", "orelse", "finalbody"):
            body = getattr(node, name, None)
            if not isinstance(body, list):
                continue
            body[:] = [
                s
                for s in body
                if not (
                    isinstance(s, ast.Expr)
                    and isinstance(s.value, ast.Constant)
                    and isinstance(s.value.value, str)
                )
            ] or ([ast.Pass()] if name == "body" else [])
    return ast.dump(tree)


def verify(fixed: Path, xml: Path = DEFAULT_XML, cfg: Config = CONFIG) -> list[str]:
    """Differences between the generation from ``xml`` with all corrections and from ``fixed``
    without corrections (only the hand written parts). Empty list: the XML contains everything."""
    from tools.plcopen_gen.emitter import Generator
    from tools.plcopen_gen.overrides import apply_overrides
    from tools.plcopen_gen.parser import parse_library

    from . import __main__ as st2py

    problems: list[str] = []

    # data types
    def types(path: Path, overrides: bool) -> dict[str, str]:
        lib = parse_library(path)
        if overrides:
            apply_overrides(lib)
        gen = Generator(lib, "x")
        return {"enums": gen.emit_enums(), "structs": gen.emit_structs(), "constants": gen.emit_constants()}

    ref_files, fix_files = types(xml, True), types(fixed, False)
    for name in sorted(ref_files):
        if _strip(ref_files[name]) != _strip(fix_files[name]):
            problems.append(f"types: {name} differs")
    # function blocks
    plain = Config(mixins=cfg.mixins)
    ref, ref_err = st2py.generate(xml, cfg)
    fix, fix_err = st2py.generate(fixed, plain, overrides=False)
    problems += [f"st2py (fixed XML): {e}" for e in fix_err if e not in ref_err]
    for path in sorted(set(ref) | set(fix)):
        a, b = ref.get(path), fix.get(path)
        if a is None or b is None:
            problems.append(f"fb: {path.name} only in one generation")
        elif path.suffix == ".py" and _strip(a) != _strip(b):
            problems.append(f"fb: {path.relative_to(ROOT)} differs")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml", type=Path, default=DEFAULT_XML, help="PLCopen export of the PLC library")
    ap.add_argument("-o", "--output", type=Path, required=True, help="fixed PLCopen XML")
    ap.add_argument("--verify", action="store_true", help="check that the XML contains all corrections")
    args = ap.parse_args(argv)
    result = export(args.xml)
    args.output.write_bytes(result.xml.encode("utf-8"))
    print(f"{args.output}: {len(result.changed)} objects changed")
    for name in result.changed:
        print(f"  {name}")
    if result.delete:
        print("delete after the import (no longer part of the cloned POU):")
        for name in result.delete:
            print(f"  {name}")
    if args.verify:
        problems = verify(args.output, args.xml)
        for p in problems:
            print(f"VERIFY: {p}", file=sys.stderr)
        if problems:
            return 1
        print("verified: the generation from the fixed XML without corrections is identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
