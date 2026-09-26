"""Documented deviations from RobotLibrary.xml.

Use only for known bugs in the PLC library that are not yet fixed in the XML export.
Every override must name the reason. When the XML already contains the overridden
value, generation fails so that the obsolete override gets removed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .model import InitValue, Library, SimpleValue, StructValue


class OverrideError(Exception):
    pass


@dataclass(frozen=True)
class ConstOverride:
    group: str
    name: str
    init: InitValue
    reason: str


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
)


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
