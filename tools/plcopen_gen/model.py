"""Intermediate model of the PLCopen types (independent of XML and of Python output)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ElemRef:
    """Elementary type, e.g. ``REAL``."""

    name: str


@dataclass(frozen=True)
class StringRef:
    length_expr: str


@dataclass(frozen=True)
class ArrayRef:
    lower_expr: str
    upper_expr: str
    element: TypeRef


@dataclass(frozen=True)
class DerivedRef:
    """Reference to a user defined type (enum, struct or alias)."""

    name: str


@dataclass(frozen=True)
class PointerRef:
    target: str


TypeRef = ElemRef | StringRef | ArrayRef | DerivedRef | PointerRef


# ---------------------------------------------------------------------- initial values


@dataclass(frozen=True)
class SimpleValue:
    text: str


@dataclass(frozen=True)
class ArrayValue:
    items: tuple[tuple[int, InitValue], ...]  # (repetition count, value)


@dataclass(frozen=True)
class StructValue:
    members: tuple[tuple[str, InitValue], ...]


InitValue = SimpleValue | ArrayValue | StructValue


# ---------------------------------------------------------------------- definitions


@dataclass
class EnumValueDef:
    name: str
    value_expr: str
    doc: str = ""


@dataclass
class EnumDef:
    name: str
    base: str  # elementary base type name
    values: list[EnumValueDef]
    doc: str = ""


@dataclass
class FieldDef:
    name: str
    type: TypeRef
    init: InitValue | None = None
    doc: str = ""


@dataclass
class StructDef:
    name: str
    fields: list[FieldDef]
    extends: str | None = None
    doc: str = ""


@dataclass
class AliasDef:
    name: str
    target: TypeRef
    doc: str = ""


@dataclass
class ConstDef:
    name: str
    type: TypeRef
    init: InitValue | None
    doc: str = ""


@dataclass
class ConstGroup:
    name: str
    constants: list[ConstDef]


@dataclass
class Library:
    enums: dict[str, EnumDef] = field(default_factory=dict)
    structs: dict[str, StructDef] = field(default_factory=dict)
    aliases: dict[str, AliasDef] = field(default_factory=dict)
    const_groups: list[ConstGroup] = field(default_factory=list)
