# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.plcopen_gen.overrides
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Documented deviations from RobotLibrary.xml.
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

"""Documented deviations from RobotLibrary.xml.

Use only for known bugs in the PLC library that are not yet fixed in the XML export.
Every override must name the reason. When the XML already contains the overridden
value, generation fails so that the obsolete override gets removed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .model import (
    EnumValueDef,
    FieldDef,
    InitValue,
    Library,
    SimpleValue,
    TypeRef,
)


class OverrideError(Exception):
    pass


@dataclass(frozen=True)
class ConstOverride:
    group: str
    name: str
    init: InitValue
    reason: str


@dataclass(frozen=True)
class EnumOverride:
    """Value of an enum element (added when the element does not exist)."""

    enum: str
    name: str
    value: int
    reason: str


@dataclass(frozen=True)
class FieldOverride:
    """Initial value of a structure field; ``struct`` ending with ``*`` is a prefix,
    starting with ``*`` a suffix (e.g. ``"*ParCmd"``)."""

    struct: str
    field: str
    init: InitValue | None  # None: keep the initial value
    reason: str
    doc: str = ""  # comment of the field (for fields without comment)


def _matches(pattern: str, name: str) -> bool:
    if pattern.startswith("*"):
        return name.endswith(pattern[1:])
    if pattern.endswith("*"):
        return name.startswith(pattern[:-1])
    return name == pattern


FIELD_OVERRIDES: tuple[FieldOverride, ...] = ()


@dataclass(frozen=True)
class FieldAdd:
    """Field added to a structure (value of the specification the PLC library does not have)."""

    struct: str
    name: str
    type: TypeRef
    doc: str
    reason: str
    after: str | None = None  # None: at the end


FIELD_ADDS: tuple[FieldAdd, ...] = ()


def apply_field_adds(lib: Library, adds: tuple[FieldAdd, ...] = FIELD_ADDS) -> None:
    for add in adds:
        struct = lib.structs.get(add.struct)
        if struct is None:
            raise OverrideError(f"field add target {add.struct} not found")
        if any(f.name.lower() == add.name.lower() for f in struct.fields):  # ST: case-insensitive
            raise OverrideError(
                f"field add {add.struct}.{add.name} is obsolete (the field exists) - remove it"
            )
        fld = FieldDef(add.name, add.type, None, f"{add.doc} [Override: {add.reason}]")
        index = len(struct.fields)
        if add.after is not None:
            index = next(i for i, f in enumerate(struct.fields) if f.name == add.after) + 1
        struct.fields.insert(index, fld)


def apply_field_overrides(lib: Library, overrides: tuple[FieldOverride, ...] = FIELD_OVERRIDES) -> None:
    for ov in overrides:
        found = 0
        for struct in lib.structs.values():
            if not _matches(ov.struct, struct.name):
                continue
            for i, fld in enumerate(struct.fields):
                if fld.name != ov.field:
                    continue
                found += 1
                if ov.init is not None and fld.init == ov.init:
                    raise OverrideError(
                        f"field override {struct.name}.{ov.field} is obsolete (XML already has the value)"
                    )
                if ov.doc and fld.doc.strip():
                    raise OverrideError(
                        f"field override {struct.name}.{ov.field}: the field has a comment now"
                    )
                doc = f"{ov.doc or fld.doc} [Override: {ov.reason}]".strip()
                init = fld.init if ov.init is None else ov.init
                struct.fields[i] = replace(fld, init=init, doc=doc)
        if not found:
            raise OverrideError(f"field override target {ov.struct}.{ov.field} not found")


# F35: command types of the PLC library that contradict the specification V1.5.9
ENUM_OVERRIDES: tuple[EnumOverride, ...] = ()

OVERRIDES: tuple[ConstOverride, ...] = tuple(
    ConstOverride(
        group="RobotLibraryParameter",
        name=name,
        init=SimpleValue("16"),
        reason="default of the library (16); the export of 2026-10-17 came from SRCI_PLC_TEST with 20",
    )
    for name in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")
)


def apply_enum_overrides(lib: Library, overrides: tuple[EnumOverride, ...] = ENUM_OVERRIDES) -> None:
    for ov in overrides:
        enum = lib.enums.get(ov.enum)
        if enum is None:
            raise OverrideError(f"override target enum {ov.enum} not found")
        for i, value in enumerate(enum.values):
            if value.name.lower() == ov.name.lower():  # ST names are case-insensitive
                if value.value_expr.strip() == str(ov.value):
                    raise OverrideError(
                        f"override {ov.enum}.{ov.name} is obsolete (XML already has the value) - remove it"
                    )
                doc = f"{value.doc} [Override: {ov.reason}]".strip()
                enum.values[i] = replace(value, value_expr=str(ov.value), doc=doc)
                break
        else:
            enum.values.append(EnumValueDef(ov.name, str(ov.value), f"[Override: {ov.reason}]"))


def apply_overrides(lib: Library, overrides: tuple[ConstOverride, ...] = OVERRIDES) -> None:
    for ov in overrides:
        group = next((g for g in lib.const_groups if g.name == ov.group), None)
        if group is None:
            raise OverrideError(f"override target group {ov.group} not found")
        for i, const in enumerate(group.constants):
            if const.name == ov.name:
                if const.init == ov.init:
                    raise OverrideError(
                        f"override {ov.group}.{ov.name} is obsolete (XML already has the value) - remove it"
                    )
                doc = f"{const.doc} [Override: {ov.reason}]".strip()
                group.constants[i] = replace(const, init=ov.init, doc=doc)
                break
        else:
            raise OverrideError(f"override target {ov.group}.{ov.name} not found")
    if overrides is OVERRIDES:
        apply_enum_overrides(lib)
        apply_field_overrides(lib)
        apply_field_adds(lib)
