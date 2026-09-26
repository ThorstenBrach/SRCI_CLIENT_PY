"""Emit Python source code for the generated SRCI types."""

from __future__ import annotations

import keyword
import re
import textwrap
from dataclasses import dataclass
from enum import EnumMeta, IntEnum
from types import SimpleNamespace
from typing import Any

from .iec_literal import LiteralError, to_python
from .model import (
    ArrayRef,
    ArrayValue,
    ElemRef,
    EnumDef,
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

# elementary types that are only aliases of other elementary types in the PLC library
_ELEM_PY = {
    "BOOL": "bool",
    "REAL": "float",
    "LREAL": "float",
}


# standard function blocks of IEC 61131-3 used in structures
STANDARD_FBS = {"R_TRIG", "F_TRIG", "TON", "TOF", "TP"}


# library parameters that the user may change at runtime (srci.configure)
CONFIGURABLE_GROUPS = {"RobotLibraryParameter"}

_PARAM_BOUND = re.compile(r"^\s*RobotLibraryParameter\.(\w+)\s*(?:([+-])\s*(\d+))?\s*$", re.IGNORECASE)


def param_bound(expr: str) -> tuple[str, int] | None:
    """``'RobotLibraryParameter.TOOL_MAX - 1'`` -> ``('TOOL_MAX', -1)``."""
    text = expr.strip()
    while text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    m = _PARAM_BOUND.match(text)
    if m is None:
        if "robotlibraryparameter" in expr.lower():
            raise GenError(f"unsupported parameter dependent array bound {expr!r}")
        return None
    offset = int(m.group(3) or 0) * (-1 if m.group(2) == "-" else 1)
    return m.group(1).upper(), offset


class GenError(Exception):
    pass


# ---------------------------------------------------------------------- resolved types


@dataclass(frozen=True)
class RElem:
    name: str


@dataclass(frozen=True)
class RString:
    length: int


@dataclass(frozen=True)
class RArray:
    lower: int
    upper: int
    element: Resolved
    # bounds that depend on a library parameter: (parameter name, offset)
    lower_param: tuple[str, int] | None = None
    upper_param: tuple[str, int] | None = None

    def bound_code(self, which: str) -> str:
        """Python code of a bound (``_iec.Param(...)`` for parameter dependent bounds)."""
        param = self.lower_param if which == "lower" else self.upper_param
        value = self.lower if which == "lower" else self.upper
        if param is None:
            return str(value)
        return f"_iec.Param({param[0]!r}, {param[1]})" if param[1] else f"_iec.Param({param[0]!r})"

    @property
    def dynamic(self) -> bool:
        return self.lower_param is not None or self.upper_param is not None


@dataclass(frozen=True)
class REnum:
    name: str


@dataclass(frozen=True)
class RStruct:
    name: str


@dataclass(frozen=True)
class RPointer:
    target: str


@dataclass(frozen=True)
class RInstance:
    """Instance of a function block or interface (not a data type)."""

    name: str


Resolved = RElem | RString | RArray | REnum | RStruct | RPointer | RInstance


def py_name(name: str) -> str:
    """Python attribute name for an ST identifier."""
    return name + "_" if keyword.iskeyword(name) or keyword.issoftkeyword(name) else name


def _doc(text: str, indent: str) -> str:
    text = text.replace("\\", "\\\\").replace('"""', "'''").strip()
    if not text:
        return ""
    wrapped = textwrap.wrap(text, width=100 - len(indent))
    if len(wrapped) == 1:
        line = wrapped[0] + (" " if wrapped[0].endswith('"') else "")
        return f'{indent}"""{line}"""\n'
    body = "\n".join(indent + line for line in wrapped)
    return f'{indent}"""\n{body}\n{indent}"""\n'


class Generator:
    def __init__(self, lib: Library, source_note: str) -> None:
        self.lib = lib
        self.source_note = source_note
        self.enum_classes: dict[str, type[IntEnum]] = {}
        # ST identifiers are case insensitive
        self.type_names: dict[str, str] = {n.lower(): n for n in (*lib.enums, *lib.structs, *lib.aliases)}
        self.consts: dict[str, SimpleNamespace] = {}
        self._build_enums()
        self._build_constants()

    # ------------------------------------------------------------------ evaluation

    def _resolve_name(self, name: str, enum_hint: str | None = None) -> str:
        """Map an ST identifier (case insensitive) to Python source for evaluation."""
        conv = re.fullmatch(r"[A-Za-z]+_TO_([A-Za-z]+)", name)
        if conv:  # type conversion function, e.g. DINT_TO_UINT(...)
            target = conv.group(1).upper()
            return {"REAL": "float", "LREAL": "float", "BOOL": "bool"}.get(target, "int")
        scopes: dict[str, Any] = {**self.enum_classes, **self.consts}
        lower_scopes = {k.lower(): k for k in scopes}
        if "." in name:
            head, member = name.split(".", 1)
            key = lower_scopes.get(head.lower())
            if key is None and head.lower() in self.type_names:
                alias = self.lib.aliases.get(self.type_names[head.lower()])
                if alias is not None:
                    r = self.resolve(alias.target)
                    key = r.name if isinstance(r, REnum) else None
            if key is not None:
                return f"{key}.{self._member(scopes[key], member, name)}"
            raise LiteralError(f"unknown name {name}")
        if enum_hint is not None:
            members = {m.lower(): m for m in self.enum_classes[enum_hint].__members__}
            if name.lower() in members:
                return f"{enum_hint}.{members[name.lower()]}"
        for group, ns in self.consts.items():
            for attr in vars(ns):
                if attr.lower() == name.lower():
                    return f"{group}.{attr}"
        raise LiteralError(f"unknown name {name}")

    @staticmethod
    def _member(scope: Any, member: str, full: str) -> str:
        names = scope.__members__ if isinstance(scope, EnumMeta) else vars(scope)
        for n in names:
            if n.lower() == member.lower():
                return str(n)
        raise LiteralError(f"unknown name {full}")

    def eval_expr(self, expr: str, enum_hint: str | None = None) -> Any:
        code = to_python(expr, lambda n: self._resolve_name(n, enum_hint))
        env: dict[str, Any] = {"__builtins__": {}, "int": int, "float": float, "bool": bool}
        env.update(self.enum_classes)
        env.update(self.consts)
        try:
            return eval(code, env)
        except Exception as exc:  # pragma: no cover - reported with context
            raise GenError(f"cannot evaluate {expr!r} ({code}): {exc}") from exc

    def eval_int(self, expr: str) -> int:
        value = self.eval_expr(expr)
        if isinstance(value, float):
            if not value.is_integer():
                raise GenError(f"{expr!r} is not an integer")
            value = int(value)
        return int(value)

    def _build_enums(self) -> None:
        reserved = set(dir(IntEnum))
        for enum in self.lib.enums.values():
            members: dict[str, int] = {}

            def resolve(n: str, known: dict[str, int] = members) -> str:
                return repr(known[n]) if n in known else self._resolve_name(n)

            for v in enum.values:
                if v.name in reserved or not v.name.isidentifier() or keyword.iskeyword(v.name):
                    raise GenError(f"enum {enum.name}: invalid member name {v.name!r}")
                code = to_python(v.value_expr, resolve)
                env: dict[str, Any] = {"__builtins__": {}}
                env.update(self.enum_classes)
                members[v.name] = int(eval(code, env))
            enum_cls: type[IntEnum] = IntEnum(enum.name, members)  # type: ignore[misc]
            self.enum_classes[enum.name] = enum_cls

    def _build_constants(self) -> None:
        for group in self.lib.const_groups:
            ns = SimpleNamespace()
            self.consts[group.name] = ns
            for c in group.constants:
                r = self.resolve(c.type)
                if isinstance(r, RElem | RString | REnum) and isinstance(c.init, SimpleValue):
                    setattr(ns, c.name, self.eval_expr(c.init.text, r.name if isinstance(r, REnum) else None))
                elif isinstance(r, RElem):
                    setattr(ns, c.name, 0)

    # ------------------------------------------------------------------ types

    def resolve(self, t: TypeRef) -> Resolved:
        if isinstance(t, ElemRef):
            return RElem(t.name)
        if isinstance(t, StringRef):
            return RString(self.eval_int(t.length_expr))
        if isinstance(t, ArrayRef):
            return RArray(
                self.eval_int(t.lower_expr),
                self.eval_int(t.upper_expr),
                self.resolve(t.element),
                param_bound(t.lower_expr),
                param_bound(t.upper_expr),
            )
        if isinstance(t, PointerRef):
            return RPointer(t.target)
        name = self.type_names.get(t.name.lower(), t.name)
        if name in self.lib.enums:
            return REnum(name)
        if name in self.lib.structs:
            return RStruct(name)
        if name in self.lib.aliases:
            return self.resolve(self.lib.aliases[name].target)
        # not a data type: function block / interface instance (e.g. R_TRIG)
        return RInstance(name)

    def all_fields(self, struct: StructDef) -> list[FieldDef]:
        base = self.all_fields(self.lib.structs[struct.extends]) if struct.extends else []
        return base + struct.fields

    # ------------------------------------------------------------------ code fragments

    def annotation(self, r: Resolved, conflicts: set[str]) -> str:
        if isinstance(r, RElem):
            return _ELEM_PY.get(r.name, "int")
        if isinstance(r, RString):
            return "str"
        if isinstance(r, RArray):
            inner = self.annotation(r.element, conflicts)
            return f"list[{inner}]" if r.lower == 0 else f"_iec.IecArray[{inner}]"
        if isinstance(r, REnum):
            return f"_e.{r.name}"
        if isinstance(r, RStruct):
            return f"_s.{r.name}" if r.name in conflicts else r.name
        if isinstance(r, RInstance):
            return "Any"
        return "object | None"

    def descriptor(self, r: Resolved) -> str:
        if isinstance(r, RElem):
            return f"_iec.{r.name}"
        if isinstance(r, RString):
            return f"_iec.StringType({r.length})"
        if isinstance(r, RArray):
            return f"_iec.ArrayType({r.bound_code('lower')}, {r.bound_code('upper')}, {self.descriptor(r.element)})"
        if isinstance(r, REnum):
            return f"_iec.EnumType(_e.{r.name})"
        if isinstance(r, RStruct):
            return f"_iec.StructType({r.name})"
        if isinstance(r, RInstance):
            return f"_iec.InstanceType({r.name!r})"
        return f"_iec.PointerType({r.target!r})"

    def enum_member(self, enum: str, value: int) -> str:
        for name, member in self.enum_classes[enum].__members__.items():
            if member.value == value:
                return f"_e.{enum}.{name}"
        raise GenError(f"{enum} has no member with value {value}")

    def default(self, r: Resolved, init: InitValue | None, where: str) -> tuple[str, bool]:
        """Python code of the default value and whether it is mutable."""
        try:
            return self._default(r, init)
        except (GenError, LiteralError) as exc:
            raise GenError(f"{where}: {exc}") from exc

    def _default(self, r: Resolved, init: InitValue | None) -> tuple[str, bool]:
        if isinstance(r, RElem):
            py = _ELEM_PY.get(r.name, "int")
            if init is None:
                return {"bool": "False", "float": "0.0", "int": "0"}[py], False
            if not isinstance(init, SimpleValue):
                raise GenError(f"invalid initial value for {r.name}")
            value = self.eval_expr(init.text)
            if py == "bool":
                return repr(bool(value)), False
            if py == "float":
                return repr(float(value)), False
            return repr(int(value)), False
        if isinstance(r, RString):
            if init is None:
                return "''", False
            if not isinstance(init, SimpleValue):
                raise GenError("invalid STRING initial value")
            return repr(str(self.eval_expr(init.text))), False
        if isinstance(r, REnum):
            if init is None:
                first = next(iter(self.enum_classes[r.name]))
                return self.enum_member(r.name, first.value), False
            if not isinstance(init, SimpleValue):
                raise GenError("invalid enum initial value")
            return self.enum_member(r.name, int(self.eval_expr(init.text, r.name))), False
        if isinstance(r, RStruct):
            if init is None:
                return f"{r.name}()", True
            if not isinstance(init, StructValue):
                raise GenError("invalid struct initial value")
            fields = {f.name: f for f in self.all_fields(self.lib.structs[r.name])}
            args: list[str] = []
            for member, value in init.members:
                if member not in fields:
                    raise GenError(f"{r.name} has no member {member}")
                code, _ = self._default(self.resolve(fields[member].type), value)
                args.append(f"{py_name(member)}={code}")
            return f"{r.name}({', '.join(args)})", True
        if isinstance(r, RArray):
            count = r.upper - r.lower + 1
            items: list[InitValue | None] = []
            if init is not None:
                if not isinstance(init, ArrayValue):
                    # a scalar initialises all elements in Codesys
                    items = [init] * count
                else:
                    for rep, value in init.items:
                        items.extend([value] * rep)
            if len(items) > count:
                raise GenError(f"too many initial values ({len(items)} > {count})")
            items.extend([None] * (count - len(items)))
            codes = [self._default(r.element, v) for v in items]
            mutable_elems = any(m for _, m in codes)
            count_code = str(count)
            if r.dynamic:
                if init is not None:
                    raise GenError("initial values for an array with parameter dependent bounds")
                count_code = f"_iec.array_len({r.bound_code('lower')}, {r.bound_code('upper')})"
            if all(c == codes[0][0] for c, _ in codes):
                if mutable_elems:
                    body = f"[{codes[0][0]} for _ in range({count_code})]"
                else:
                    body = f"[{codes[0][0]}] * {count_code}"
            else:
                body = "[" + ", ".join(c for c, _ in codes) + "]"
            if r.lower != 0:
                body = f"_iec.IecArray({r.lower}, {body})"
            return body, True
        if isinstance(r, RInstance) and (r.name in self.lib.function_blocks or r.name in STANDARD_FBS):
            return f"_iec.new_instance({r.name!r})", True
        return "None", False

    # ------------------------------------------------------------------ modules

    def header(self, what: str) -> str:
        return (
            f'"""SRCI {what} - generated from the PLC library, DO NOT EDIT.\n\n'
            f"{self.source_note}\n"
            'Regenerate with ``python -m tools.plcopen_gen``.\n"""\n'
            "# ruff: noqa\n"
            "# fmt: off\n"
        )

    def emit_enums(self) -> str:
        out = [self.header("enumerations")]
        out.append("from __future__ import annotations\n\n")
        out.append("from srci.types import iec as _iec\n\n")
        names = list(self.lib.enums)
        enum_aliases: list[tuple[str, str]] = []
        for a in self.lib.aliases.values():
            r = self.resolve(a.target)
            if isinstance(r, REnum):
                enum_aliases.append((a.name, r.name))
        out.append(
            "__all__ = [\n" + "".join(f"    {n!r},\n" for n in sorted(names + [a for a, _ in enum_aliases]))
        )
        out.append("]\n")
        for enum in self.lib.enums.values():
            out.append(self._emit_enum(enum))
        if enum_aliases:
            out.append("\n\n# aliases defined in the PLC library\n")
            for alias, target in enum_aliases:
                out.append(f"{alias} = {target}\n")
        return "".join(out)

    def _emit_enum(self, enum: EnumDef) -> str:
        cls = self.enum_classes[enum.name]
        lines = [f"\n\nclass {enum.name}(_iec.IecIntEnum):\n"]
        lines.append(_doc(enum.doc or f"{enum.name} ({enum.base})", "    "))
        for v in enum.values:
            lines.append(f"    {v.name} = {cls[v.name].value}\n")
            lines.append(_doc(v.doc, "    "))
        lines.append(f"\n\n_iec.register_enum({enum.name}, _iec.{enum.base})\n")
        return "".join(lines)

    def _ordered_structs(self) -> list[StructDef]:
        done: set[str] = set()
        order: list[StructDef] = []

        def visit(s: StructDef) -> None:
            if s.name in done:
                return
            if s.extends:
                if s.extends not in self.lib.structs:
                    raise GenError(f"{s.name} extends unknown {s.extends}")
                visit(self.lib.structs[s.extends])
            done.add(s.name)
            order.append(s)

        for s in self.lib.structs.values():
            visit(s)
        return order

    def emit_structs(self) -> str:
        type_names = set(self.lib.structs)
        out = [self.header("structures")]
        out.append(
            "from __future__ import annotations\n\n"
            "from dataclasses import dataclass as _dataclass, field as _field\n"
            "from typing import TYPE_CHECKING, Any, ClassVar\n\n"
            "from srci.types import iec as _iec\n"
            "from srci.types._generated import enums as _e\n\n"
            "if TYPE_CHECKING:\n"
            "    from srci.types._generated import structs as _s\n"
            "else:  # self reference for annotations that clash with field names\n"
            "    import sys as _sys\n\n"
            "    _s = _sys.modules[__name__]\n\n"
        )
        order = self._ordered_structs()
        out.append(
            "__all__ = [\n" + "".join(f"    {s.name!r},\n" for s in sorted(order, key=lambda s: s.name))
        )
        out.append("]\n")
        for s in order:
            field_names = {py_name(f.name) for f in self.all_fields(s)}
            conflicts = field_names & type_names
            base = f"({s.extends})" if s.extends else ""
            out.append(f"\n\n@_dataclass(kw_only=True, slots=True)\nclass {s.name}{base}:\n")
            out.append(_doc(s.doc or s.name, "    "))
            out.append("\n    _IEC_FIELDS_: ClassVar[tuple[_iec.IecField, ...]]\n")
            for f in s.fields:
                r = self.resolve(f.type)
                ann = self.annotation(r, conflicts)
                code, mutable = self.default(r, f.init, f"{s.name}.{f.name}")
                name = py_name(f.name)
                if mutable:
                    out.append(f"    {name}: {ann} = _field(default_factory=lambda: {code})\n")
                else:
                    out.append(f"    {name}: {ann} = {code}\n")
                out.append(_doc(f.doc, "    "))
        out.append("\n\n# ---- IEC layout information (used by srci.codec) ----\n")
        for s in order:
            items: list[str] = []
            for f in s.fields:
                st = "" if py_name(f.name) == f.name else f", st_name={f.name!r}"
                items.append(
                    f"    _iec.IecField({py_name(f.name)!r}, {self.descriptor(self.resolve(f.type))}{st}),\n"
                )
            prefix = f"{s.extends}._IEC_FIELDS_ + " if s.extends else ""
            out.append(f"{s.name}._IEC_FIELDS_ = {prefix}(\n" + "".join(items) + ")\n")
        return "".join(out)

    def emit_constants(self) -> str:
        out = [self.header("constants and library parameters")]
        out.append(
            "from __future__ import annotations\n\n"
            "from typing import ClassVar, Final\n\n"
            "from srci.types import iec as _iec\n"
            "from srci.types._generated import enums as _e\n"
            "from srci.types._generated.structs import *  # noqa: F403\n\n"
        )
        out.append(
            "__all__ = [\n"
            + "".join(f"    {g.name!r},\n" for g in sorted(self.lib.const_groups, key=lambda g: g.name))
        )
        out.append("]\n")
        for group in self.lib.const_groups:
            out.append(f"\n\nclass {group.name}:\n")
            out.append(_doc(f"Global variable list {group.name} of the PLC library.", "    "))
            for c in group.constants:
                r = self.resolve(c.type)
                code, _ = self.default(r, c.init, f"{group.name}.{c.name}")
                ann = self.annotation(r, set())
                typ = (
                    f"Final[{ann}]"
                    if group.constant and group.name not in CONFIGURABLE_GROUPS
                    else f"ClassVar[{ann}]"
                )
                out.append(f"    {c.name}: {typ} = {code}\n")
                out.append(_doc(c.doc, "    "))
        out.append("\n\n_ = _iec  # keep import for type descriptors\n")
        return "".join(out)

    def emit_init(self) -> str:
        return (
            self.header("types")
            + "from srci.types._generated.constants import *  # noqa: F403\n"
            + "from srci.types._generated.enums import *  # noqa: F403\n"
            + "from srci.types._generated.structs import *  # noqa: F403\n"
        )
