# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.sem
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Semantic types and the type environment of the transpiler.
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

"""Semantic types and the type environment of the transpiler."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property

from tools.plcopen_gen.emitter import (
    Generator,
    RArray,
    REnum,
    RInstance,
    RPointer,
    RString,
    RStruct,
    py_name,
)
from tools.plcopen_gen.model import TypeRef

from .decl import TArray, TElem, TPointer, TReference, TString, TypeDecl
from .library import Pou

# ---------------------------------------------------------------------- semantic types


@dataclass(frozen=True)
class SElem:
    name: str  # BOOL, BYTE, ..., REAL, LREAL, TIME, TOD, DATE, DT


@dataclass(frozen=True)
class SString:
    length: int


@dataclass(frozen=True)
class SArray:
    lower: int | None  # None: ARRAY[*]
    upper: int | None
    elem: SType
    # bounds that depend on a library parameter (name, offset) - value above is the default
    lower_param: tuple[str, int] | None = field(default=None, compare=False)
    upper_param: tuple[str, int] | None = field(default=None, compare=False)
    # upper bound only known at runtime (e.g. SIZEOF of a type with parameter dependent size)
    upper_expr: object = field(default=None, compare=False)

    @property
    def dynamic(self) -> bool:
        return self.lower_param is not None or self.upper_param is not None or self.upper_expr is not None


@dataclass(frozen=True)
class SEnum:
    name: str


@dataclass(frozen=True)
class SStruct:
    name: str


@dataclass(frozen=True)
class SFb:
    name: str  # library function block, hand written or standard FB (TON, R_TRIG)


@dataclass(frozen=True)
class SItf:
    name: str


@dataclass(frozen=True)
class SPtr:
    target: SType


@dataclass(frozen=True)
class SRef:
    target: SType


@dataclass(frozen=True)
class SAny:
    pass


SType = SElem | SString | SArray | SEnum | SStruct | SFb | SItf | SPtr | SRef | SAny

ANY = SAny()
BOOL = SElem("BOOL")
DINT = SElem("DINT")
REAL = SElem("REAL")
STRING = SString(255)

INT_TYPES = {
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
    "TIME",
    "LTIME",
    "TOD",
    "DATE",
    "DT",
}
BIT_TYPES = {"BYTE", "WORD", "DWORD", "LWORD"}
REAL_TYPES = {"REAL", "LREAL"}
WRAP_AS = {"TIME": "UDINT", "LTIME": "ULINT", "TOD": "UDINT", "DATE": "UDINT", "DT": "UDINT"}
ELEM_SIZE = {
    "BOOL": 1,
    "BYTE": 1,
    "WORD": 2,
    "DWORD": 4,
    "LWORD": 8,
    "SINT": 1,
    "USINT": 1,
    "INT": 2,
    "UINT": 2,
    "DINT": 4,
    "UDINT": 4,
    "LINT": 8,
    "ULINT": 8,
    "REAL": 4,
    "LREAL": 8,
    "TIME": 4,
    "LTIME": 8,
    "TOD": 4,
    "DATE": 4,
    "DT": 4,
}
POINTER_SIZE = 8

# standard function blocks: inputs, outputs (all scalar)
STANDARD_FBS: dict[str, tuple[dict[str, SType], dict[str, SType]]] = {
    "R_TRIG": ({"CLK": BOOL}, {"Q": BOOL}),
    "F_TRIG": ({"CLK": BOOL}, {"Q": BOOL}),
    "TON": ({"IN": BOOL, "PT": SElem("TIME")}, {"Q": BOOL, "ET": SElem("TIME")}),
    "TOF": ({"IN": BOOL, "PT": SElem("TIME")}, {"Q": BOOL, "ET": SElem("TIME")}),
    "TP": ({"IN": BOOL, "PT": SElem("TIME")}, {"Q": BOOL, "ET": SElem("TIME")}),
}


class TypeLookupError(Exception):
    pass


def is_int(t: SType) -> bool:
    return (isinstance(t, SElem) and t.name in INT_TYPES) or isinstance(t, SEnum)


def is_real(t: SType) -> bool:
    return isinstance(t, SElem) and t.name in REAL_TYPES


def is_bool(t: SType) -> bool:
    return isinstance(t, SElem) and t.name == "BOOL"


def is_scalar(t: SType) -> bool:
    return isinstance(t, SElem | SString | SEnum)


def is_aggregate(t: SType) -> bool:
    """Structure or array: assignment copies (``copy_into``)."""
    return isinstance(t, SStruct | SArray)


def int_name(t: SType, env: TypeEnv) -> str | None:
    """IEC integer type name of an integer or enum type (for wrap around)."""
    if isinstance(t, SElem) and t.name in INT_TYPES:
        return WRAP_AS.get(t.name, t.name)
    if isinstance(t, SEnum):
        return env.enum_base(t.name)
    return None


class TypeEnv:
    def __init__(self, gen: Generator, pous: dict[str, Pou]) -> None:
        self.gen = gen
        self.pous = pous
        self.type_names = gen.type_names  # lower -> canonical (enums, structs, aliases)

    # ------------------------------------------------------------------ lookups

    def pou(self, name: str) -> Pou | None:
        return self.pous.get(name.upper())

    def canonical_type(self, name: str) -> str | None:
        return self.type_names.get(name.lower())

    def enum_base(self, name: str) -> str:
        return self.gen.lib.enums[name].base

    def enum_member(self, enum: str, member: str) -> str | None:
        members = self.gen.enum_classes[enum].__members__
        for m in members:
            if m.lower() == member.lower():
                return m
        return None

    def const_group(self, name: str) -> str | None:
        for g in self.gen.consts:
            if g.lower() == name.lower():
                return g
        return None

    def const_member(self, group: str, member: str) -> tuple[str, SType] | None:
        for g in self.gen.lib.const_groups:
            if g.name == group:
                for c in g.constants:
                    if c.name.lower() == member.lower():
                        return c.name, self.from_ref(c.type)
        return None

    def const_value(self, group: str, member: str) -> object:
        ns = self.gen.consts[group]
        for attr in vars(ns):
            if attr.lower() == member.lower():
                return getattr(ns, attr)
        return None

    @cached_property
    def _struct_fields(self) -> dict[str, dict[str, tuple[str, SType]]]:
        out: dict[str, dict[str, tuple[str, SType]]] = {}
        for s in self.gen.lib.structs.values():
            fields: dict[str, tuple[str, SType]] = {}
            for f in self.gen.all_fields(s):
                fields[f.name.upper()] = (py_name(f.name), self.from_ref(f.type))
            out[s.name] = fields
        return out

    def struct_field(self, struct: str, name: str) -> tuple[str, SType] | None:
        return self._struct_fields[struct].get(name.upper())

    def struct_fields(self, struct: str) -> list[tuple[str, SType]]:
        return list(self._struct_fields[struct].values())

    def struct_is_a(self, struct: str, base: str) -> bool:
        s: str | None = struct
        while s is not None:
            if s == base:
                return True
            s = self.gen.lib.structs[s].extends
        return False

    def fb_is_a(self, fb: str, base: str) -> bool:
        p = self.pou(fb)
        while p is not None:
            if p.name.upper() == base.upper():
                return True
            if base.upper() in (i.upper() for i in p.header.implements):
                return True
            p = self.pou(p.extends) if p.extends else None
        return False

    # ------------------------------------------------------------------ type conversion

    def named(self, name: str) -> SType:
        if name.upper() in ELEM_SIZE:
            return SElem(name.upper())
        canonical = self.canonical_type(name)
        if canonical is not None:
            r = self.gen.resolve(_derived(canonical))
            return self.from_resolved(r)
        if name.upper() in STANDARD_FBS:
            return SFb(name.upper())
        p = self.pou(name)
        if p is not None:
            if p.kind == "INTERFACE":
                return SItf(p.name)
            if p.kind == "FUNCTION_BLOCK":
                return SFb(p.name)
        if name.upper() in ("STRING", "WSTRING"):
            return SString(80)
        raise TypeLookupError(f"unknown type {name}")

    def from_resolved(self, r: object) -> SType:
        if isinstance(r, RStruct):
            return SStruct(r.name)
        if isinstance(r, REnum):
            return SEnum(r.name)
        if isinstance(r, RString):
            return SString(r.length)
        if isinstance(r, RArray):
            return SArray(r.lower, r.upper, self.from_resolved(r.element), r.lower_param, r.upper_param)
        if isinstance(r, RPointer):
            return SPtr(self.named(r.target) if r.target != "?" else ANY)
        if isinstance(r, RInstance):
            return self.named(r.name)
        name = getattr(r, "name", None)
        if isinstance(name, str):
            return SElem(name)
        raise TypeLookupError(f"cannot convert {r}")

    def from_ref(self, t: TypeRef) -> SType:
        return self.from_resolved(self.gen.resolve(t))

    def from_decl(self, t: TypeDecl, const_eval: Callable[[object], int]) -> SType:
        if isinstance(t, TElem):
            return SElem(t.name)
        if isinstance(t, TString):
            return SString(80 if t.length is None else int(const_eval(t.length)))
        if isinstance(t, TArray):
            elem = self.from_decl(t.element, const_eval)
            for dim in reversed(t.dims):
                if dim is None:
                    elem = SArray(None, None, elem)
                else:
                    try:
                        upper: int = int(const_eval(dim[1]))
                        upper_expr = None
                    except Exception:
                        upper, upper_expr = -1, dim[1]  # evaluated at runtime
                    elem = SArray(
                        int(const_eval(dim[0])),
                        upper,
                        elem,
                        param_of(dim[0]),
                        param_of(dim[1]),
                        upper_expr,
                    )
            return elem
        if isinstance(t, TPointer):
            return SPtr(self.from_decl(t.target, const_eval))
        if isinstance(t, TReference):
            return SRef(self.from_decl(t.target, const_eval))
        return self.named(t.name)

    # ------------------------------------------------------------------ size

    def sizeof(self, t: SType) -> int | None:
        if isinstance(t, SElem):
            return ELEM_SIZE[t.name]
        if isinstance(t, SString):
            return t.length + 1
        if isinstance(t, SEnum):
            return ELEM_SIZE[self.enum_base(t.name)]
        if isinstance(t, SArray):
            if t.lower is None or t.upper is None or t.dynamic:
                return None
            inner = self.sizeof(t.elem)
            return None if inner is None else (t.upper - t.lower + 1) * inner
        if isinstance(t, SStruct):
            total = 0
            for _, ft in self.struct_fields(t.name):
                size = self.sizeof(ft)
                if size is None:
                    return None
                total += size
            return total
        if isinstance(t, SPtr | SRef | SItf | SFb):
            return POINTER_SIZE if isinstance(t, SPtr | SRef | SItf) else None
        return None


def param_of(e: object) -> tuple[str, int] | None:
    """``RobotLibraryParameter.X [+-] n`` -> ``('X', +-n)``."""
    from . import ast as A

    offset = 0
    if (
        isinstance(e, A.BinOp)
        and e.op in ("+", "-")
        and isinstance(e.right, A.Literal)
        and e.right.kind == "int"
    ):
        assert isinstance(e.right.value, int)
        offset = e.right.value if e.op == "+" else -e.right.value
        e = e.left
    if isinstance(e, A.Member) and isinstance(e.obj, A.Name) and e.obj.id.upper() == "ROBOTLIBRARYPARAMETER":
        return e.name.upper(), offset
    return None


def _derived(name: str) -> TypeRef:
    from tools.plcopen_gen.model import DerivedRef

    return DerivedRef(name)
