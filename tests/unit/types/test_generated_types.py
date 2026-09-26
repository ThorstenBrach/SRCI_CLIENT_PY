"""Consistency of the generated types with RobotLibrary.xml and with the IEC layout."""

from __future__ import annotations

import dataclasses
import typing
import xml.etree.ElementTree as ET
from enum import IntEnum
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from srci import types as T
from srci.types import iec
from srci.types._generated import constants, enums, structs
from tools.plcopen_gen.__main__ import DEFAULT_OUT, DEFAULT_XML, generate

NS = "{http://www.plcopen.org/xml/tc6_0200}"


@cache
def xml_types() -> dict[str, ET.Element]:
    root = ET.parse(DEFAULT_XML).getroot()
    dts = root.find(f"{NS}types/{NS}dataTypes")
    assert dts is not None
    return {dt.get("name", ""): dt for dt in dts}


def xml_kind(dt: ET.Element) -> str:
    base = dt.find(f"{NS}baseType")
    assert base is not None
    return next(iter(base)).tag.replace(NS, "")


STRUCTS = [getattr(structs, n) for n in structs.__all__]
ENUMS = [getattr(enums, n) for n in enums.__all__]


# ------------------------------------------------------------------ generator


def test_generated_files_up_to_date() -> None:
    files = generate(DEFAULT_XML)
    for name, src in files.items():
        stale = f"{name} is stale, run python -m tools.plcopen_gen"
        assert (DEFAULT_OUT / name).read_text("utf-8") == src, stale


def test_generator_is_deterministic() -> None:
    assert generate(DEFAULT_XML) == generate(DEFAULT_XML)


def test_counts_match_xml() -> None:
    kinds = [xml_kind(dt) for dt in xml_types().values()]
    assert len(structs.__all__) == kinds.count("struct") == 591
    real_enums = {n for n in enums.__all__ if getattr(enums, n).__name__ == n}
    assert len(real_enums) == kinds.count("enum") == 81


def test_every_xml_type_is_generated() -> None:
    for name, dt in xml_types().items():
        kind = xml_kind(dt)
        if kind == "struct":
            assert name in structs.__all__
        elif kind == "enum":
            assert name in enums.__all__


# ------------------------------------------------------------------ enums


from tools.plcopen_gen.overrides import ENUM_OVERRIDES  # noqa: E402


@pytest.mark.parametrize("enum", ENUMS, ids=lambda e: e.__name__)
def test_enum_values_match_xml_and_fit_base(enum: type[IntEnum]) -> None:
    dt = xml_types()[enum.__name__]
    base = iec.enum_base(enum)
    values = {v.get("name"): v.get("value", "") for v in dt.iter(f"{NS}value")}
    for ov in ENUM_OVERRIDES:  # documented deviations (F35)
        if ov.enum == enum.__name__:
            values[ov.name] = str(ov.value)
    assert set(values) == set(enum.__members__)
    for member in enum:
        text = values[member.name]
        expected = int(text.split("#")[1], int(text.split("#")[0])) if "#" in text else int(text)
        assert member.value == expected
        assert base.min <= member.value <= base.max, f"{member!r} does not fit {base.name}"


def test_enum_spot_checks() -> None:
    assert T.ArmConfigElbow.USE_CONFIG.value == 0 and T.ArmConfigElbow.UP.value == 4
    assert T.RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID.value == 0x8401
    assert T.SequenceFlagEnum is T.SequenceFlag  # alias in the PLC library
    assert T.LogLevelEnum is T.Severity  # alias chain LogLevelEnum -> LogLevel -> Severity


# ------------------------------------------------------------------ structures


def dataclass_field_names(cls: type) -> list[str]:
    return [f.name for f in dataclasses.fields(cls)]


@pytest.mark.parametrize("cls", STRUCTS, ids=lambda c: c.__name__)
def test_struct_layout_matches_dataclass(cls: type) -> None:
    fields = cls._IEC_FIELDS_  # type: ignore[attr-defined]
    assert [f.name for f in fields] == dataclass_field_names(cls)
    # IEC member order = XML order, base type members first
    dt = xml_types()[cls.__name__]
    struct_el = dt.find(f"{NS}baseType/{NS}struct")
    assert struct_el is not None
    own = [v.get("name") for v in struct_el.findall(f"{NS}variable")]
    assert [f.st_name for f in fields[len(fields) - len(own) :]] == own


def check_value(value: Any, t: iec.IecType, where: str) -> None:
    if isinstance(t, iec.Elementary):
        assert type(value) is t.python_type, f"{where}: {value!r} is not {t.python_type.__name__}"
        assert float(t.min) <= typing.cast(float, value) <= float(t.max), where
    elif isinstance(t, iec.StringType):
        assert isinstance(value, str) and len(value) <= t.length, where
    elif isinstance(t, iec.EnumType):
        assert isinstance(value, t.enum), where
    elif isinstance(t, iec.StructType):
        assert type(value) is t.struct, where
        check_struct(value, where)
    elif isinstance(t, iec.ArrayType):
        assert isinstance(value, list) and len(value) == t.count, where
        if t.lower != 0:
            assert isinstance(value, iec.IecArray) and value.lower == t.lower, where
        for i, item in enumerate(value):
            check_value(item, t.element, f"{where}[{i}]")
    elif isinstance(t, iec.PointerType):
        assert value is None, where
    elif isinstance(t, iec.InstanceType):
        # function block instances are created (interfaces stay None)
        if t.name.startswith("I") and t.name[1].isupper():
            assert value is None, where
        else:
            assert type(value).__name__ == t.name, where


def check_struct(obj: Any, where: str) -> None:
    for f in type(obj)._IEC_FIELDS_:
        check_value(getattr(obj, f.name), f.type, f"{where}.{f.name}")


@pytest.mark.parametrize("cls", STRUCTS, ids=lambda c: c.__name__)
def test_defaults_match_iec_types(cls: type) -> None:
    check_struct(cls(), cls.__name__)


def test_defaults_are_independent() -> None:
    a, b = T.RobotCartesianPosition(), T.RobotCartesianPosition()
    a.Config.Elbow = T.ArmConfigElbow.UP
    assert b.Config.Elbow == T.ArmConfigElbow.USE_CONFIG


def test_type_hints_resolve() -> None:
    for cls in STRUCTS:
        typing.get_type_hints(cls, vars(structs))


def test_struct_spot_checks() -> None:
    pos = T.RobotCartesianPosition(X=1.5)
    assert pos.X == 1.5 and pos.E6 == 0.0
    assert isinstance(pos, T.RobotCartesianPositionShort)
    # initial values from the PLC library
    par = T.MoveAxesAbsoluteParCmd()
    assert par.BlendingParameter == [10.0, 0.0]
    # case insensitive type reference in the PLC library (TelegramPlcTorobSequenceHeader)
    header = {f.name: f for f in T.TelegramPlcToRobSequence._IEC_FIELDS_}["Header"]
    assert header.type == iec.StructType(T.TelegramPlcToRobSequenceHeader)
    # function block instances are not data
    fbs = {f.name: f.type for f in T.AxesGroupState._IEC_FIELDS_}
    assert fbs["OnlineChange_R"] == iec.InstanceType("R_TRIG")


def test_constants() -> None:
    p = constants.RobotLibraryParameter
    assert p.TOOL_MAX == p.FRAME_MAX == p.LOAD_MAX == 16
    v = constants.RobotLibraryConstants.SRCIVersion
    assert isinstance(v, T.VersionStruct)


def test_xml_source_is_documented() -> None:
    source = Path(DEFAULT_XML).with_name("SOURCE.md").read_text("utf-8")
    import hashlib

    assert hashlib.sha256(Path(DEFAULT_XML).read_bytes()).hexdigest() in source
