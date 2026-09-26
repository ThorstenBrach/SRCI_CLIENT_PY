"""Documented deviations from RobotLibrary.xml.

Use only for known bugs in the PLC library that are not yet fixed in the XML export.
Every override must name the reason. When the XML already contains the overridden
value, generation fails so that the obsolete override gets removed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .model import (
    ArrayRef,
    DerivedRef,
    ElemRef,
    EnumValueDef,
    FieldDef,
    InitValue,
    Library,
    SimpleValue,
    StructValue,
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


_F41 = (
    "ST-FIX F41: spec 5.x robot dynamics parameter: '<0 %: use default' (default); the library "
    "had 0.0 = internal minimal value (the RC rejects 0 for DecelerationRate/JerkRate)"
)
FIELD_OVERRIDES: tuple[FieldOverride, ...] = (
    *(
        FieldOverride("*ParCmd", rate, SimpleValue("-1.0"), _F41)
        for rate in ("VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate")
    ),
    FieldOverride(
        "ExchangeConfigurationParCmd",
        "LifeSignTimeOut",
        SimpleValue("50"),
        "ST-FIX F44: spec 5.6.6: LifeSignTimeOut default 50 ms (min 10 ms); the library had 0 (invalid)",
    ),
    FieldOverride(
        "StopSubprogramOutCmd",
        "OriginID",
        None,
        "ST-FIX F46: comment missing",
        doc="OriginID of the stopped subprogram (spec 5.5.12.4 EmitterID, ListenerID, FollowID and OriginID)",
    ),
    FieldOverride(
        "ReadRobotDataOutCmd",
        "RCInterpreterVersion",
        None,
        "ST-FIX F46: comment missing",
        doc="Version of the server implementation in the format X.X.X (spec table 6-18)",
    ),
)


@dataclass(frozen=True)
class FieldAdd:
    """Field added to a structure (value of the specification the PLC library does not have)."""

    struct: str
    name: str
    type: TypeRef
    doc: str
    reason: str
    after: str | None = None  # None: at the end


FIELD_ADDS: tuple[FieldAdd, ...] = (
    FieldAdd(
        "GroupStopRecvData",
        "AbortedSequence",
        ElemRef("SINT"),
        "Sequence whose commands were aborted",
        "ST-FIX F32: byte 4 of the response (spec GroupStop)",
    ),
    FieldAdd(
        "CallSubprogramOutCmd",
        "Progress",
        ElemRef("UINT"),
        "Progress of the subprogram [%] (spec output Progress)",
        "ST-FIX F45",
    ),
    FieldAdd(
        "SetTriggerLimitOutCmd",
        "Data",
        ArrayRef("0", "11", ElemRef("REAL")),
        "Actual values of the monitored data (spec output Data)",
        "ST-FIX F45",
    ),
    FieldAdd(
        "ExchangeConfigurationRecvData",
        "NumberOfServerLogs",
        ElemRef("UINT"),
        "Number of server log entries",
        "ST-FIX F32: bytes 28..29 of the response",
    ),
    FieldAdd(
        "ExchangeConfigurationOutCmd",
        "NumberOfServerLogs",
        ElemRef("UINT"),
        "Number of server log entries",
        "ST-FIX F32",
    ),
    FieldAdd(
        "AxesGroupCyclicOptionalDataCartesianPosition",
        "CurrentCoordinateSystem",
        DerivedRef("RobotCoordinateSystemParameters"),
        "Tool and frame currently used by the RC (bytes 36..37 of the optional cyclic Cartesian position)",
        "ST-FIX F59: CoordinateSystem is the tool/frame of the returned position (bytes 34..35), "
        "the currently used tool/frame needs an own field (spec table 5-89, 6.1.6)",
        after="CoordinateSystem",
    ),
    FieldAdd(
        "ReadRobotSWLimitsOutCmd",
        "DataChanged",
        ElemRef("BOOL"),
        "The limits were changed on the RC since the last synchronization",
        "ST-FIX F32: byte 106 of the response",
    ),
)


def apply_field_adds(lib: Library, adds: tuple[FieldAdd, ...] = FIELD_ADDS) -> None:
    for add in adds:
        struct = lib.structs.get(add.struct)
        if struct is None:
            raise OverrideError(f"field add target {add.struct} not found")
        if any(f.name == add.name for f in struct.fields):
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
        apply_field_overrides(lib)
        apply_field_adds(lib)
