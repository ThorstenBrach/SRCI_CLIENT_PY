"""Read the POUs (function blocks, functions, interfaces) of the PLCopen XML export."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from . import ast as A
from .decl import Header, TypeDecl, VarDecl, parse_accessor_vars, parse_interface
from .parser import parse_body

NS = "{http://www.plcopen.org/xml/tc6_0200}"


def _text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    return "".join(el.itertext())


@dataclass(eq=False)
class Body:
    src: str
    _parsed: tuple[list[A.Stmt], list[str]] | None = None

    @property
    def stmts(self) -> list[A.Stmt]:
        return self.parsed[0]

    @property
    def tail_comments(self) -> list[str]:
        return self.parsed[1]

    @property
    def parsed(self) -> tuple[list[A.Stmt], list[str]]:
        if self._parsed is None:
            self._parsed = parse_body(self.src)
        return self._parsed


@dataclass(eq=False)
class Method:
    header: Header
    vars: list[VarDecl]
    body: Body
    owner: Pou | None = None

    @property
    def name(self) -> str:
        return self.header.name

    def params(self) -> list[VarDecl]:
        return [v for v in self.vars if v.section in ("input", "inout", "output")]


@dataclass(eq=False)
class Property:
    header: Header
    get_vars: list[VarDecl] | None
    get_body: Body | None
    set_vars: list[VarDecl] | None
    set_body: Body | None
    owner: Pou | None = None

    @property
    def name(self) -> str:
        return self.header.name

    @property
    def type(self) -> TypeDecl:
        assert self.header.return_type is not None
        return self.header.return_type


@dataclass(eq=False)
class Pou:
    header: Header
    vars: list[VarDecl]
    body: Body
    folder: list[str]
    methods: dict[str, Method] = field(default_factory=dict)  # key: upper case name
    properties: dict[str, Property] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.header.name

    @property
    def kind(self) -> str:
        return self.header.kind

    @property
    def extends(self) -> str | None:
        return self.header.extends[0] if self.header.extends else None

    @property
    def st_path(self) -> str:
        """Path of the .st file in the PLC repository (``POUs/Read/.../X.st``)."""
        parts = self.folder[1:] if self.folder and self.folder[0] == "Library" else self.folder
        return "/".join([*parts, self.name + ".st"])


def _folders(root: ET.Element) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    ps = root.find(f".//{NS}ProjectStructure")
    if ps is None:
        return out

    def walk(el: ET.Element, path: list[str]) -> None:
        for c in el:
            tag = c.tag.replace(NS, "")
            if tag == "Folder":
                walk(c, [*path, c.get("Name", "")])
            elif tag == "Object":
                out.setdefault(c.get("Name", ""), path)

    walk(ps, [])
    return out


def _plain(el: ET.Element) -> str:
    for d in el.findall(f"{NS}addData/{NS}data"):
        if d.get("name", "").endswith("interfaceasplaintext"):
            return _text(d)
    p = el.find(f"{NS}InterfaceAsPlainText")
    return _text(p)


def _st_body(el: ET.Element | None) -> str:
    if el is None:
        return ""
    st = el.find(f"{NS}ST")
    return _text(st)


def load_pous(xml: Path) -> dict[str, Pou]:
    """All POUs of the library, key: upper case name."""
    root = ET.parse(xml).getroot()
    folders = _folders(root)
    pous: dict[str, Pou] = {}
    container = root.find(f"{NS}types/{NS}pous")
    assert container is not None
    for el in container:
        name = el.get("name", "")
        plain = _plain(el)
        itf = parse_interface(plain)
        pou = Pou(itf.header, itf.vars, Body(_st_body(el.find(f"{NS}body"))), folders.get(name, []))
        for m_el in el.iter(f"{NS}Method"):
            m_itf = parse_interface(_text(m_el.find(f"{NS}InterfaceAsPlainText")))
            m = Method(m_itf.header, m_itf.vars, Body(_st_body(m_el.find(f"{NS}body"))), pou)
            pou.methods[m.name.upper()] = m
        for p_el in el.iter(f"{NS}Property"):
            p_itf = parse_interface(_text(p_el.find(f"{NS}InterfaceAsPlainText")))
            get_el = p_el.find(f"{NS}GetAccessor")
            set_el = p_el.find(f"{NS}SetAccessor")
            prop = Property(
                p_itf.header,
                parse_accessor_vars(_text(get_el.find(f"{NS}InterfaceAsPlainText")))
                if get_el is not None
                else None,
                Body(_st_body(get_el.find(f"{NS}body"))) if get_el is not None else None,
                parse_accessor_vars(_text(set_el.find(f"{NS}InterfaceAsPlainText")))
                if set_el is not None
                else None,
                Body(_st_body(set_el.find(f"{NS}body"))) if set_el is not None else None,
                pou,
            )
            pou.properties[prop.name.upper()] = prop
        pous[name.upper()] = pou
    # interfaces (addData "interface")
    for d in root.iter(f"{NS}data"):
        if not d.get("name", "").endswith("/interface"):
            continue
        for itf_el in d.iter(f"{NS}Interface"):
            name = itf_el.get("name", "")
            ext = (
                [e.text or "" for e in itf_el.iter(f"{NS}Extends")]
                if itf_el.find(f".//{NS}Extends") is not None
                else []
            )
            header = Header("INTERFACE", name, extends=ext)
            pou = Pou(header, [], Body(""), folders.get(name, []))
            for m_el in itf_el.iter(f"{NS}Method"):
                txt = _text(m_el.find(f"{NS}InterfaceAsPlainText"))
                if not txt.strip():
                    continue
                m_itf = parse_interface(txt)
                pou.methods[m_itf.header.name.upper()] = Method(m_itf.header, m_itf.vars, Body(""), pou)
            for p_el in itf_el.iter(f"{NS}Property"):
                txt = _text(p_el.find(f"{NS}InterfaceAsPlainText"))
                if not txt.strip():
                    continue
                p_itf = parse_interface(txt)
                pou.properties[p_itf.header.name.upper()] = Property(p_itf.header, [], None, None, None, pou)
            pous[name.upper()] = pou
    return pous
