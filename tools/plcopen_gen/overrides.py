"""Documented deviations from RobotLibrary.xml.

Use only for known bugs in the PLC library that are not yet fixed in the XML export.
Every override must name the reason. When the XML already contains the overridden
value, generation fails so that the obsolete override gets removed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .model import EnumValueDef, InitValue, Library, SimpleValue, StructValue


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


# F35: command types of the PLC library that contradict the specification V1.5.9
ENUM_OVERRIDES: tuple[EnumOverride, ...] = (
    EnumOverride("CmdType", "MoveCircularAbsolute", 2106, "F35: spec 6.3.13 Type 2106 (library 2109)"),
    EnumOverride("CmdType", "MoveCircularRelative", 2107, "F35: spec Type 2107 (library 2106)"),
    EnumOverride(
        "CmdType", "MoveLinearAbsoluteJ", 2109, "F35: spec 6.3.12 Type 2109 (missing in the library)"
    ),
    EnumOverride("CmdType", "SoftSwitchTcp", 7300, "F35: spec Type 7300 (missing in the library)"),
)

OVERRIDES: tuple[ConstOverride, ...] = (
    ConstOverride(
        group="RobotLibraryConstants",
        name="SRCIVersion",
        init=StructValue(
            (
                ("MajorVersion", SimpleValue("1")),
                ("MinorVersion", SimpleValue("5")),
                ("PatchVersion", SimpleValue("0")),
            )
        ),
        reason="PLC library still says 1.3.0, but implements SRCI 1.5 (SDK: SRCI_VERSION 1.5)",
    ),
    ConstOverride(
        group="RobotLibraryParameter",
        name="FRAGMENT_MAX",
        init=SimpleValue("31"),
        reason="ST-FIX F52: 10 fragments (0..9) per telegram are too few - a 256 byte telegram holds up to "
        "27 fragments (header 8 bytes + at least 1 byte payload); fragments behind the array were dropped "
        "although the telegram was acknowledged -> responses lost",
    ),
)


def apply_enum_overrides(lib: Library, overrides: tuple[EnumOverride, ...] = ENUM_OVERRIDES) -> None:
    for ov in overrides:
        enum = lib.enums.get(ov.enum)
        if enum is None:
            raise OverrideError(f"override target enum {ov.enum} not found")
        for i, value in enumerate(enum.values):
            if value.name == ov.name:
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
