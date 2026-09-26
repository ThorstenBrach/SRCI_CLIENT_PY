"""Name resolution: variables, members, methods, properties of POUs."""

from __future__ import annotations

from dataclasses import dataclass, field

from tools.plcopen_gen.emitter import py_name

from .decl import VarDecl
from .library import Method, Pou, Property
from .sem import SType


@dataclass
class Var:
    """A variable visible in a scope."""

    name: str  # canonical ST name
    py: str  # Python name (attribute or local variable)
    type: SType
    kind: str  # local, input, inout, output, retval, member, inst, const, loopvar
    decl: VarDecl | None = None
    owner: Pou | None = None  # for members
    alias: object = None  # python ast node: REFERENCE bound once with REF= (used instead of the name)


@dataclass
class Scope:
    pou: Pou
    method: Method | None = None
    prop: Property | None = None
    accessor: str | None = None  # get / set
    locals: dict[str, Var] = field(default_factory=dict)  # key: upper case ST name
    self_name: str = "self"

    @property
    def is_function(self) -> bool:
        return self.pou.kind == "FUNCTION"

    @property
    def callable_name(self) -> str:
        if self.method is not None:
            return self.method.name
        if self.prop is not None:
            return self.prop.name
        return self.pou.name

    def add_local(self, var: Var) -> None:
        self.locals[var.name.upper()] = var


def local_py(name: str) -> str:
    return py_name(name)


def hierarchy(pou: Pou, pous: dict[str, Pou]) -> list[Pou]:
    """``pou`` and its base function blocks (most derived first)."""
    out: list[Pou] = []
    p: Pou | None = pou
    while p is not None:
        out.append(p)
        p = pous.get(p.extends.upper()) if p.extends else None
    return out


def find_member_var(pou: Pou, name: str, pous: dict[str, Pou]) -> tuple[VarDecl, Pou] | None:
    for p in hierarchy(pou, pous):
        for v in p.vars:
            if v.name.upper() == name.upper():
                return v, p
    return None


def find_method(pou: Pou, name: str, pous: dict[str, Pou], start: int = 0) -> Method | None:
    for p in hierarchy(pou, pous)[start:]:
        m = p.methods.get(name.upper())
        if m is not None:
            return m
        for itf in p.header.implements:
            ip = pous.get(itf.upper())
            if ip is not None:
                m = find_method(ip, name, pous)
                if m is not None:
                    return m
    return None


def find_property(pou: Pou, name: str, pous: dict[str, Pou], start: int = 0) -> Property | None:
    for p in hierarchy(pou, pous)[start:]:
        pr = p.properties.get(name.upper())
        if pr is not None:
            return pr
    return None


def find_inst_var(pou: Pou, name: str, pous: dict[str, Pou]) -> tuple[VarDecl, Method] | None:
    """``VAR_INST`` of a method (stored in the instance)."""
    for p in hierarchy(pou, pous):
        for m in p.methods.values():
            for v in m.vars:
                if v.section == "inst" and v.name.upper() == name.upper():
                    return v, m
    return None


def inst_attr(method: Method, var: VarDecl) -> str:
    return f"_{method.name}_{var.name}"
