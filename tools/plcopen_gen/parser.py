"""Parse a PLCopen TC6 XML export (Codesys/TwinCAT) into :mod:`tools.plcopen_gen.model`."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from .model import (
    AliasDef,
    ArrayRef,
    ArrayValue,
    ConstDef,
    ConstGroup,
    DerivedRef,
    ElemRef,
    EnumDef,
    EnumValueDef,
    FieldDef,
    InitValue,
    Library,
    PointerRef,
    SimpleValue,
    StringRef,
    StructDef,
    StructValue,
    TypeRef,
)

NS = "{http://www.plcopen.org/xml/tc6_0200}"
XHTML = "{http://www.w3.org/1999/xhtml}"

ELEMENTARY_TAGS = {
    "BOOL",
    "BYTE",
    "WORD",
    "DWORD",
    "LWORD",
    "SINT",
    "USINT",
    "INT",
    "UINT",
    "DINT",
    "UDINT",
    "LINT",
    "ULINT",
    "REAL",
    "LREAL",
    "TIME",
    "TOD",
    "DATE",
    "DT",
}


class ParseError(Exception):
    pass


def _tag(el: ET.Element) -> str:
    return el.tag.replace(NS, "")


def _text(el: ET.Element | None) -> str:
    """Documentation text of a ``<documentation>``/``<Documentation>`` element."""
    if el is None:
        return ""
    return " ".join("".join(el.itertext()).split())


def _type_doc(el: ET.Element) -> str:
    """``///`` comments in front of TYPE ... in the plain text interface."""
    plain = el.find(f".//{NS}InterfaceAsPlainText")
    if plain is None:
        return ""
    lines: list[str] = []
    for raw in "".join(plain.itertext()).splitlines():
        line = raw.strip()
        if line.upper().startswith(("TYPE", "VAR_GLOBAL")):
            break
        if line.startswith("///"):
            lines.append(line[3:].strip())
    return " ".join(x for x in lines if x)


def parse_type(type_el: ET.Element) -> TypeRef:
    """Parse the single child of a ``<type>`` or ``<baseType>`` element."""
    children = list(type_el)
    if len(children) != 1:
        raise ParseError(f"type element with {len(children)} children")
    c = children[0]
    tag = _tag(c)
    if tag in ELEMENTARY_TAGS:
        return ElemRef(tag)
    if tag in ("string", "wstring"):
        return StringRef(c.get("length", "80"))
    if tag == "derived":
        return DerivedRef(c.get("name", ""))
    if tag == "array":
        dims = c.findall(f"{NS}dimension")
        base = c.find(f"{NS}baseType")
        if base is None:
            raise ParseError("array without baseType")
        elem = parse_type(base)
        # multi-dimensional arrays: nest from the innermost dimension
        for dim in reversed(dims[1:]):
            elem = ArrayRef(dim.get("lower", "0"), dim.get("upper", "0"), elem)
        return ArrayRef(dims[0].get("lower", "0"), dims[0].get("upper", "0"), elem)
    if tag == "pointer":
        base = c.find(f"{NS}baseType")
        target = parse_type(base) if base is not None else DerivedRef("?")
        return PointerRef(target.name if isinstance(target, DerivedRef | ElemRef) else "?")
    raise ParseError(f"unsupported type <{tag}>")


def parse_value(el: ET.Element) -> InitValue:
    tag = _tag(el)
    if tag == "simpleValue":
        return SimpleValue(el.get("value", ""))
    if tag == "arrayValue":
        items: list[tuple[int, InitValue]] = []
        for v in el.findall(f"{NS}value"):
            rep = int(v.get("repetitionValue", "1"))
            items.append((rep, parse_value(v[0])))
        return ArrayValue(tuple(items))
    if tag == "structValue":
        members = tuple((v.get("member", ""), parse_value(v[0])) for v in el.findall(f"{NS}value"))
        return StructValue(members)
    raise ParseError(f"unsupported initial value <{tag}>")


def _init(var: ET.Element) -> InitValue | None:
    iv = var.find(f"{NS}initialValue")
    return parse_value(iv[0]) if iv is not None else None


def _parse_enum(name: str, enum_el: ET.Element, dt: ET.Element) -> EnumDef:
    base_el = enum_el.find(f"{NS}baseType")
    base = "INT"  # IEC/Codesys default
    if base_el is not None:
        b = parse_type(base_el)
        if not isinstance(b, ElemRef):
            raise ParseError(f"enum {name}: unsupported base type {b}")
        base = b.name
    docs: dict[str, str] = {}
    for ev in dt.iter(f"{NS}EnumValue"):
        n = ev.find(f"{NS}Name")
        if n is not None and n.text:
            docs[n.text.strip()] = _text(ev.find(f"{NS}Documentation"))
    values = [
        EnumValueDef(v.get("name", ""), v.get("value", ""), docs.get(v.get("name", ""), ""))
        for v in enum_el.iter(f"{NS}value")
    ]
    return EnumDef(name, base, values, _type_doc(dt))


def _parse_struct(name: str, struct_el: ET.Element, dt: ET.Element) -> StructDef:
    fields: list[FieldDef] = []
    for v in struct_el.findall(f"{NS}variable"):
        t = v.find(f"{NS}type")
        if t is None:
            raise ParseError(f"{name}.{v.get('name')}: no type")
        fields.append(
            FieldDef(v.get("name", ""), parse_type(t), _init(v), _text(v.find(f"{NS}documentation")))
        )
    ext = dt.find(f".//{NS}Inheritance/{NS}Extends")
    extends = ext.text.strip() if ext is not None and ext.text else None
    return StructDef(name, fields, extends, _type_doc(dt))


def parse_library(path: Path) -> Library:
    root = ET.parse(path).getroot()
    lib = Library()
    data_types = root.find(f"{NS}types/{NS}dataTypes")
    if data_types is None:
        raise ParseError("no dataTypes in XML")
    for dt in data_types:
        name = dt.get("name", "")
        base_type = dt.find(f"{NS}baseType")
        if base_type is None:
            raise ParseError(f"{name}: no baseType")
        kind = next(iter(base_type))
        tag = _tag(kind)
        if tag == "enum":
            lib.enums[name] = _parse_enum(name, kind, dt)
        elif tag == "struct":
            lib.structs[name] = _parse_struct(name, kind, dt)
        else:
            lib.aliases[name] = AliasDef(name, parse_type(base_type), _type_doc(dt))

    for gv in root.iter(f"{NS}globalVars"):
        consts: list[ConstDef] = []
        for v in gv.findall(f"{NS}variable"):
            t = v.find(f"{NS}type")
            if t is None:
                continue
            consts.append(
                ConstDef(v.get("name", ""), parse_type(t), _init(v), _text(v.find(f"{NS}documentation")))
            )
        lib.const_groups.append(ConstGroup(gv.get("name", ""), consts))
    return lib
