"""Emit Python source for one POU (function block, function or interface)."""

from __future__ import annotations

import ast as py
import copy
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, ClassVar

from tools.plcopen_gen.emitter import py_name

from . import ast as A
from .config import Config
from .decl import VarDecl
from .library import Method, Pou, Property
from .registry import Target
from .scope import (
    Scope,
    Var,
    find_inst_var,
    find_member_var,
    find_method,
    find_property,
    hierarchy,
    inst_attr,
)
from .sem import (
    ANY,
    BOOL,
    DINT,
    INT_TYPES,
    REAL,
    STANDARD_FBS,
    STRING,
    SAny,
    SArray,
    SElem,
    SEnum,
    SFb,
    SItf,
    SPtr,
    SRef,
    SString,
    SStruct,
    SType,
    TypeEnv,
    int_name,
    is_aggregate,
    is_bool,
    is_int,
    is_real,
)


class EmitError(Exception):
    pass


# ---------------------------------------------------------------------- python ast helpers


def N(name: str) -> py.expr:
    return py.Name(id=name, ctx=py.Load())


def At(obj: py.expr, name: str) -> py.expr:
    return py.Attribute(value=obj, attr=name, ctx=py.Load())


def C(value: Any) -> py.expr:
    return py.Constant(value=value)


def Cl(
    func: py.expr, args: list[py.expr] | None = None, kw: list[tuple[str, py.expr]] | None = None
) -> py.expr:
    return py.Call(func=func, args=args or [], keywords=[py.keyword(arg=k, value=v) for k, v in (kw or [])])


def src(node: py.AST) -> str:
    return py.unparse(py.fix_missing_locations(node))


def has_call(node: py.AST) -> bool:
    return any(isinstance(n, py.Call) for n in py.walk(node))


# ---------------------------------------------------------------------- translated expressions


@dataclass
class R:
    """Translated expression."""

    node: py.expr
    type: SType
    kind: str = "value"  # value, enumtype, group, func, super, this, typename, method
    extra: Any = None
    arith: bool = False  # contains + - * or unary minus (integer wrap needed on assignment)


@dataclass
class Lv:
    """Assignment target."""

    node: py.expr  # Store context is set on emission
    type: SType
    bit: tuple[Lv, int] | None = None  # bit access target (base, bit)
    kind: str = "value"  # value, retval, local, pointer


@dataclass
class Out:
    lines: list[str] = field(default_factory=list)

    def add(self, indent: int, text: str) -> None:
        self.lines.append("    " * indent + text if text else "")


# ---------------------------------------------------------------------- builtins

CONV_RE = re.compile(r"^([A-Z_]+?)_TO_([A-Z_]+)$", re.IGNORECASE)
ELEMS = {
    "BOOL",
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
    "REAL",
    "LREAL",
    "TIME",
    "LTIME",
    "TOD",
    "TIME_OF_DAY",
    "DATE",
    "DT",
    "DATE_AND_TIME",
    "STRING",
    "WSTRING",
}

RT = "srci.iec.rt"
CONV = "srci.iec.conv"
TYPES = "srci.types"


def ann_elem(name: str) -> str:
    if name == "BOOL":
        return "bool"
    if name in ("REAL", "LREAL"):
        return "float"
    return "int"


# ---------------------------------------------------------------------- emitter


class PouEmitter:
    def __init__(self, env: TypeEnv, reg: dict[str, Target], pou: Pou, cfg: Config) -> None:
        self.env = env
        self.reg = reg
        self.pou = pou
        self.cfg = cfg
        self.pous = env.pous
        self.imports: dict[str, set[str]] = {}
        self.tc_imports: dict[str, set[str]] = {}
        self.out = Out()
        self.scope = Scope(pou)
        self.shadow: set[str] = set()  # python names of locals in the current function
        self.loop_after: list[set[str]] = []
        self.hand_methods = cfg.hand_methods.get(pou.name, {})
        self.warnings: list[str] = []
        self.box_names: dict[str, str] = {}

    # ------------------------------------------------------------------ imports

    def use(self, module: str, name: str) -> py.expr:
        self.imports.setdefault(module, set()).add(name)
        if name in self.shadow:
            alias = "_T" if module == TYPES else None
            if alias is None:
                raise EmitError(f"{name} is shadowed by a local variable")
            self.imports.setdefault("import srci.types as _T", set())
            return At(N("_T"), name)
        return N(name)

    def use_type(self, name: str) -> py.expr:
        return self.use(TYPES, name)

    def use_rt(self, name: str) -> py.expr:
        return self.use(RT, name)

    def use_conv(self, name: str) -> py.expr:
        return self.use(CONV, name)

    def use_iec(self) -> py.expr:
        self.imports.setdefault("from srci.types import iec as _iec", set())
        return N("_iec")

    def use_pou(self, name: str, runtime: bool = True) -> py.expr:
        t = self.reg.get(name.upper())
        if t is None:
            raise EmitError(f"unknown POU {name}")
        if t.name == self.pou.name and not t.hand:
            return N(t.name)
        if runtime:
            return self.use(t.module, t.name)
        self.tc_imports.setdefault(t.module, set()).add(t.name)
        return N(t.name)

    # ------------------------------------------------------------------ annotations

    def ann(self, t: SType, runtime: bool = False) -> str:
        if isinstance(t, SElem):
            return ann_elem(t.name)
        if isinstance(t, SString):
            return "str"
        if isinstance(t, SEnum | SStruct):
            self.tc_imports.setdefault(TYPES, set()).add(t.name)
            if t.name in self.shadow:
                self.imports.setdefault("import srci.types as _T", set())
                return f"_T.{t.name}"
            return t.name
        if isinstance(t, SArray):
            inner = self.ann(t.elem)
            if t.lower is None and isinstance(t.elem, SElem) and t.elem.name in ("BYTE", "USINT"):
                return "list[int] | bytearray"  # ARRAY[*] OF BYTE: bytes buffers are fine
            if t.lower == 0 or t.lower is None:
                return f"list[{inner}]"
            self.use_iec()
            return f"_iec.IecArray[{inner}]"
        if isinstance(t, SFb | SItf):
            if t.name in STANDARD_FBS:
                self.tc_imports.setdefault("srci.iec.standard", set()).add(t.name)
                return t.name
            self.use_pou(t.name, runtime=False)
            return t.name
        if isinstance(t, SPtr):
            if isinstance(t.target, SFb | SItf):
                return f"{self.ann(t.target)} | None"
            self.tc_imports.setdefault(RT, set()).add("Ptr")
            return "Ptr | None"
        if isinstance(t, SRef):
            return f"{self.ann(t.target)} | None"
        return "Any"

    # ------------------------------------------------------------------ descriptors (ADR)

    def desc(self, t: SType, value: py.expr | None = None) -> py.expr:
        iec = self.use_iec()
        if isinstance(t, SElem):
            name = {"TIME_OF_DAY": "TOD", "DATE_AND_TIME": "DT", "LTIME": "LWORD"}.get(t.name, t.name)
            return At(iec, name)
        if isinstance(t, SString):
            return Cl(At(iec, "StringType"), [C(t.length)])
        if isinstance(t, SEnum):
            return Cl(At(iec, "EnumType"), [self.use_type(t.name)])
        if isinstance(t, SStruct):
            return Cl(At(iec, "StructType"), [self.use_type(t.name)])
        if isinstance(t, SArray):
            if t.lower is None or t.upper is None:
                if value is None:
                    raise EmitError("ADR of ARRAY[*] without value")
                return Cl(self.use_rt("array_type"), [value, self.desc(t.elem)])
            return Cl(
                At(iec, "ArrayType"), [self.bound(t, "lower"), self.bound(t, "upper"), self.desc(t.elem)]
            )
        if isinstance(t, SPtr | SRef | SItf):
            return Cl(At(iec, "PointerType"), [C("?")])
        if isinstance(t, SFb):
            return Cl(At(iec, "InstanceType"), [C(t.name)])
        raise EmitError(f"no descriptor for {t}")

    def bound(self, t: SArray, which: str) -> py.expr:
        """Bound of an array type (``_iec.Param(...)`` if it depends on a library parameter)."""
        param = t.lower_param if which == "lower" else t.upper_param
        value = t.lower if which == "lower" else t.upper
        if which == "upper" and t.upper_expr is not None:
            assert isinstance(t.upper_expr, A.Expr)
            return self.expr(t.upper_expr).node
        if param is None:
            return C(value)
        args: list[py.expr] = [C(param[0])] + ([C(param[1])] if param[1] else [])
        return Cl(At(self.use_iec(), "Param"), args)

    # ------------------------------------------------------------------ constant evaluation

    def const_eval(self, e: object) -> int:
        assert isinstance(e, A.Expr)
        if isinstance(e, A.Literal) and e.kind == "int":
            assert isinstance(e.value, int)
            return e.value
        if isinstance(e, A.BinOp) and e.op in ("+", "-", "*", "/"):
            a, b = self.const_eval(e.left), self.const_eval(e.right)
            return {"+": a + b, "-": a - b, "*": a * b, "/": a // b if b else 0}[e.op]
        if isinstance(e, A.UnaryOp) and e.op == "-":
            return -self.const_eval(e.operand)
        if isinstance(e, A.Member) and isinstance(e.obj, A.Name):
            group = self.env.const_group(e.obj.id)
            if group is not None:
                value = self.env.const_value(group, e.name)
                if isinstance(value, int):
                    return value
        if isinstance(e, A.Call) and isinstance(e.func, A.Name) and e.func.id.upper() == "SIZEOF":
            arg = e.args[0].value
            t = self._sizeof_type(arg)
            size = self.env.sizeof(t)
            if size is not None:
                return size
        if isinstance(e, A.Name):
            for p in hierarchy(self.pou, self.pous):
                for v in p.vars:
                    if v.name.upper() == e.id.upper() and v.constant and isinstance(v.init, A.Expr):
                        return self.const_eval(v.init)
        raise EmitError(f"cannot evaluate constant expression at line {e.line}")

    def _sizeof_type(self, arg: A.Expr) -> SType:
        if isinstance(arg, A.Name):
            try:
                return self.env.named(arg.id)
            except Exception:
                pass
            var = self._lookup_var(arg.id)
            if var is not None:
                return var.type
            # variable of the POU declared later (e.g. SIZEOF(_command) in a method)
            found = find_member_var(self.pou, arg.id, self.pous)
            if found is not None:
                return self.env.from_decl(found[0].type, self.const_eval)
        return self.expr(arg).type

    def type_of_decl(self, v: VarDecl) -> SType:
        return self.env.from_decl(v.type, self.const_eval)

    # ------------------------------------------------------------------ name lookup

    def _lookup_var(self, name: str) -> Var | None:
        key = name.upper()
        if key in self.scope.locals:
            return self.scope.locals[key]
        if self.scope.is_function:
            return None
        found = find_member_var(self.pou, name, self.pous)
        if found is not None:
            v, owner = found
            kind = "const" if v.constant else "member"
            return Var(v.name, f"self.{py_name(v.name)}", self.type_of_decl(v), kind, v, owner)
        inst = find_inst_var(self.pou, name, self.pous)
        if inst is not None:
            v, m = inst
            return Var(v.name, f"self.{inst_attr(m, v)}", self.type_of_decl(v), "inst", v)
        return None

    def name_expr(self, e: A.Name) -> R:
        var = self._lookup_var(e.id)
        if var is not None:
            node: py.expr
            if var.alias is not None:
                assert isinstance(var.alias, py.expr)
                return R(
                    copy.deepcopy(var.alias),
                    var.type.target if isinstance(var.type, SRef) else var.type,
                    extra=var,
                )
            if var.py.startswith("self."):
                node = At(N(self.scope.self_name), var.py[5:])
            else:
                node = N(var.py)
            return R(node, var.type, extra=var)
        if not self.scope.is_function:
            prop = find_property(self.pou, e.id, self.pous)
            if prop is not None:
                return R(At(N("self"), prop.name), self.type_of_prop(prop))
            m = find_method(self.pou, e.id, self.pous)
            if m is not None:
                return R(At(N("self"), m.name), ANY, "method", m)
        up = e.id.upper()
        group = self.env.const_group(e.id)
        if group is not None:
            return R(self.use_type(group), ANY, "group", group)
        canonical = self.env.canonical_type(e.id)
        if canonical is not None:
            if canonical in self.env.gen.lib.enums:
                return R(self.use_type(canonical), ANY, "enumtype", canonical)
            return R(self.use_type(canonical), self.env.named(canonical), "typename", canonical)
        if up in self.pous or up in STANDARD_FBS:
            pou = self.pous.get(up)
            if pou is not None and pou.kind == "FUNCTION":
                return R(self.use_pou(pou.name), ANY, "func", pou)
            return R(self.use_pou(e.id), self.env.named(e.id), "typename", e.id)
        if up in ("TRUE", "FALSE"):
            return R(C(up == "TRUE"), BOOL)
        raise EmitError(f"line {e.line}: unknown name {e.id}")

    def type_of_prop(self, prop: Property) -> SType:
        return self.env.from_decl(prop.type, self.const_eval)

    # ------------------------------------------------------------------ member access

    def member(self, obj: R, name: str, line: int) -> R:
        if obj.kind == "group":
            found = self.env.const_member(obj.extra, name)
            if found is None:
                raise EmitError(f"line {line}: {obj.extra} has no member {name}")
            return R(At(obj.node, found[0]), found[1])
        if obj.kind == "enumtype":
            m = self.env.enum_member(obj.extra, name)
            if m is None:
                raise EmitError(f"line {line}: enum {obj.extra} has no member {name}")
            return R(At(obj.node, m), SEnum(obj.extra))
        t = obj.type
        if isinstance(t, SRef):
            t = t.target
        if isinstance(t, SPtr) and isinstance(t.target, SFb | SItf):
            t = t.target  # pointer to FB is a reference in Python (p^ is p)
        if isinstance(t, SEnum):
            # Codesys: enum value via a variable of the enum type (e.g. Severity.ERROR)
            m = self.env.enum_member(t.name, name)
            if m is not None:
                return R(At(self.use_type(t.name), m), t)
        if isinstance(t, SStruct):
            f = self.env.struct_field(t.name, name)
            if f is None:
                raise EmitError(f"line {line}: struct {t.name} has no member {name}")
            return R(At(obj.node, f[0]), f[1])
        if isinstance(t, SFb | SItf):
            if t.name in STANDARD_FBS:
                ins, outs = STANDARD_FBS[t.name]
                for k, v in {**ins, **outs}.items():
                    if k.upper() == name.upper():
                        return R(At(obj.node, k), v)
                raise EmitError(f"line {line}: {t.name} has no member {name}")
            pou = self.env.pou(t.name)
            if pou is None:
                raise EmitError(f"line {line}: unknown FB {t.name}")
            member_var = find_member_var(pou, name, self.pous)
            if member_var is not None:
                return R(At(obj.node, member_var[0].name), self._decl_type_in(member_var[0], member_var[1]))
            member_prop = find_property(pou, name, self.pous)
            if member_prop is not None:
                return R(At(obj.node, member_prop.name), self.type_of_prop(member_prop))
            member_method = find_method(pou, name, self.pous)
            if member_method is not None:
                return R(At(obj.node, member_method.name), ANY, "method", member_method)
            raise EmitError(f"line {line}: {t.name} has no member {name}")
        if isinstance(t, SAny):
            self.warnings.append(f"line {line}: member {name} of untyped expression")
            return R(At(obj.node, name), ANY)
        raise EmitError(f"line {line}: member {name} of {t}")

    def _decl_type_in(self, v: VarDecl, owner: Pou) -> SType:
        saved = self.pou
        try:
            self.pou = owner
            return self.type_of_decl(v)
        finally:
            self.pou = saved

    # ------------------------------------------------------------------ expressions

    def expr(self, e: A.Expr) -> R:
        if isinstance(e, A.Literal):
            return self.literal(e)
        if isinstance(e, A.EnumLiteral):
            canonical = self.env.canonical_type(e.type_name)
            if canonical is None or canonical not in self.env.gen.lib.enums:
                raise EmitError(f"line {e.line}: unknown enum {e.type_name}")
            m = self.env.enum_member(canonical, e.member)
            if m is None:
                raise EmitError(f"line {e.line}: {canonical} has no member {e.member}")
            return R(At(self.use_type(canonical), m), SEnum(canonical))
        if isinstance(e, A.Name):
            return self.name_expr(e)
        if isinstance(e, A.This):
            return R(N(self.scope.self_name), SFb(self.pou.name), "this")
        if isinstance(e, A.Super):
            return R(N("super"), SFb(self.pou.extends or ""), "super")
        if isinstance(e, A.Member):
            obj = self.expr(e.obj)
            if obj.kind == "super":
                base_method = find_method(self.pou, e.name, self.pous, start=1)
                if base_method is not None:
                    return R(At(Cl(N("super")), base_method.name), ANY, "method", base_method)
                prop = find_property(self.pou, e.name, self.pous, start=1)
                if prop is not None:
                    return R(At(Cl(N("super")), prop.name), self.type_of_prop(prop))
                raise EmitError(f"line {e.line}: SUPER^ has no member {e.name}")
            if obj.kind == "this":
                inner = A.Name(e.name, line=e.line)
                saved = self.scope.locals
                self.scope.locals = {}  # THIS^.x: member, not the local x
                try:
                    return self.name_expr(inner)
                finally:
                    self.scope.locals = saved
            return self.member(obj, e.name, e.line)
        if isinstance(e, A.BitAccess):
            obj = self.expr(e.obj)
            return R(Cl(self.use_rt("bit"), [obj.node, C(e.bit)]), BOOL)
        if isinstance(e, A.Index):
            obj = self.expr(e.obj)
            node = obj.node
            t = obj.type
            for idx in e.indices:
                i = self.expr(idx)
                node = py.Subscript(value=node, slice=i.node, ctx=py.Load())
                if isinstance(t, SArray):
                    t = t.elem
                elif isinstance(t, SString):
                    t = SElem("BYTE")
                else:
                    t = ANY
            return R(node, t)
        if isinstance(e, A.Deref):
            obj = self.expr(e.obj)
            t = obj.type
            if isinstance(t, SPtr):
                if isinstance(t.target, SFb | SItf):
                    return R(obj.node, t.target)
                return R(Cl(At(obj.node, "deref"), [self.desc(t.target)]), t.target)
            raise EmitError(f"line {e.line}: dereference of non pointer")
        if isinstance(e, A.Call):
            return self.call(e)
        if isinstance(e, A.UnaryOp):
            return self.unary(e)
        if isinstance(e, A.BinOp):
            return self.binop(e)
        if isinstance(e, A.ArrayLiteral):
            items = [self.expr(i) for i in e.items]
            return R(
                py.List(elts=[i.node for i in items], ctx=py.Load()), SArray(0, len(items) - 1, items[0].type)
            )
        raise EmitError(f"line {e.line}: unsupported expression {type(e).__name__}")

    def literal(self, e: A.Literal) -> R:
        if e.kind == "bool":
            return R(C(bool(e.value)), BOOL)
        if e.kind == "string":
            assert isinstance(e.value, str)
            return R(C(e.value), SString(max(len(e.value), 1)))
        if e.kind == "real":
            assert isinstance(e.value, int | float)
            return R(C(float(e.value)), REAL)
        if e.kind in ("time", "date"):
            return R(C(e.value), SElem("TIME" if e.kind == "time" else "DATE"))
        t: SType = SElem(e.type_prefix) if e.type_prefix in ELEMS else DINT
        if e.type_prefix is not None and e.type_prefix not in ELEMS:
            raise EmitError(f"line {e.line}: typed literal {e.type_prefix}#")
        if is_real(t):
            assert isinstance(e.value, int | float)
            return R(C(float(e.value)), t)
        return R(C(e.value), t, extra="literal")

    def unary(self, e: A.UnaryOp) -> R:
        v = self.expr(e.operand)
        if e.op == "-":
            return R(py.UnaryOp(op=py.USub(), operand=v.node), v.type, arith=True)
        if e.op == "+":
            return v
        # NOT
        if is_bool(v.type) or isinstance(v.type, SAny):
            return R(py.UnaryOp(op=py.Not(), operand=v.node), BOOL)
        if is_int(v.type):
            name = int_name(v.type, self.env) or "DWORD"
            mask = (1 << (8 * _size(name))) - 1
            node = py.BinOp(left=py.UnaryOp(op=py.Invert(), operand=v.node), op=py.BitAnd(), right=C(mask))
            return R(node, v.type)
        raise EmitError(f"line {e.line}: NOT of {v.type}")

    _CMP: ClassVar[dict[str, type[py.cmpop]]] = {
        "=": py.Eq,
        "<>": py.NotEq,
        "<": py.Lt,
        ">": py.Gt,
        "<=": py.LtE,
        ">=": py.GtE,
    }
    _ARITH: ClassVar[dict[str, type[py.operator]]] = {"+": py.Add, "-": py.Sub, "*": py.Mult, "**": py.Pow}

    def binop(self, e: A.BinOp) -> R:
        a = self.expr(e.left)
        b = self.expr(e.right)
        op = e.op
        if op in self._CMP:
            # pointer / interface comparison with 0 / NULL_POINTER
            for x, y in ((a, b), (b, a)):
                if isinstance(x.type, SPtr | SItf | SRef) and self._is_null(y):
                    cmp_op: py.cmpop = py.Is() if op == "=" else py.IsNot()
                    if op not in ("=", "<>"):
                        raise EmitError(f"line {e.line}: pointer comparison {op}")
                    return R(py.Compare(left=x.node, ops=[cmp_op], comparators=[C(None)]), BOOL)
            if isinstance(a.type, SPtr | SItf) and isinstance(b.type, SPtr | SItf):
                cmp_op = py.Is() if op == "=" else py.IsNot()
                return R(py.Compare(left=a.node, ops=[cmp_op], comparators=[b.node]), BOOL)
            return R(py.Compare(left=a.node, ops=[self._CMP[op]()], comparators=[b.node]), BOOL)
        if op in ("AND", "OR", "XOR", "&", "AND_THEN", "OR_ELSE"):
            if (is_bool(a.type) or isinstance(a.type, SAny)) and (
                is_bool(b.type) or isinstance(b.type, SAny)
            ):
                if op == "XOR":
                    return R(py.Compare(left=a.node, ops=[py.NotEq()], comparators=[b.node]), BOOL)
                short = op in ("AND_THEN", "OR_ELSE") or not has_call(b.node)
                if short:
                    bop: py.boolop = py.And() if op in ("AND", "&", "AND_THEN") else py.Or()
                    return R(py.BoolOp(op=bop, values=[a.node, b.node]), BOOL)
                # ST evaluates both operands (side effects of calls)
                bit_op: py.operator = py.BitAnd() if op in ("AND", "&") else py.BitOr()
                return R(py.BinOp(left=a.node, op=bit_op, right=b.node), BOOL)
            bit_op = {"AND": py.BitAnd, "&": py.BitAnd, "OR": py.BitOr, "XOR": py.BitXor}[op]()
            return R(
                py.BinOp(left=a.node, op=bit_op, right=b.node),
                a.type if not isinstance(a.type, SAny) else b.type,
            )
        if op in ("/", "MOD"):
            if is_real(a.type) or is_real(b.type):
                if op == "MOD":
                    raise EmitError(f"line {e.line}: MOD of REAL")
                return R(py.BinOp(left=a.node, op=py.Div(), right=b.node), REAL)
            f = "idiv" if op == "/" else "imod"
            return R(Cl(self.use_rt(f), [a.node, b.node]), self._arith_type(a.type, b.type), arith=True)
        if op in self._ARITH:
            t = self._arith_type(a.type, b.type)
            node = py.BinOp(left=a.node, op=self._ARITH[op](), right=b.node)
            if isinstance(a.type, SPtr) or isinstance(b.type, SPtr):
                return R(node, a.type if isinstance(a.type, SPtr) else b.type)
            if isinstance(a.type, SString) and op == "+":
                return R(node, STRING)
            return R(node, t, arith=not is_real(t))
        raise EmitError(f"line {e.line}: operator {op}")

    def _arith_type(self, a: SType, b: SType) -> SType:
        if is_real(a) or is_real(b):
            return REAL
        if isinstance(a, SElem) and a.name in INT_TYPES:
            if isinstance(b, SElem) and b.name in INT_TYPES and _size(b.name) > _size(a.name):
                return b
            return a
        if isinstance(b, SElem):
            return b
        return a if not isinstance(a, SAny) else DINT

    def _is_null(self, r: R) -> bool:
        if isinstance(r.node, py.Constant) and r.node.value == 0:
            return True
        return isinstance(r.node, py.Attribute) and r.node.attr.upper() == "NULL_POINTER"

    # ------------------------------------------------------------------ calls

    def call(self, e: A.Call) -> R:
        f = e.func
        # builtins by name
        if isinstance(f, A.Name):
            up = f.id.upper()
            if self._lookup_var(f.id) is None and not self._is_method(f.id):
                b = self.builtin(up, e)
                if b is not None:
                    return b
        if isinstance(f, A.Super):
            base = self.pous.get((self.pou.extends or "").upper())
            if base is None:
                raise EmitError(f"line {e.line}: SUPER^() without base")
            kw = self.fb_call_args(base, e.args, e.line)
            return R(Cl(At(Cl(N("super")), "__call__"), kw=kw), ANY, "stmt")
        callee = self.expr(f)
        if callee.kind == "method":
            m: Method = callee.extra
            kw = self.method_args(m, e.args, e.line)
            rt = self._method_return(m)
            return R(Cl(callee.node, kw=kw), rt)
        if callee.kind == "func":
            pou: Pou = callee.extra
            kw = self.function_args(pou, e.args, e.line)
            rt = (
                self.env.from_decl(pou.header.return_type, self.const_eval) if pou.header.return_type else ANY
            )
            return R(Cl(callee.node, kw=kw), rt)
        t = callee.type
        if isinstance(t, SFb):
            if t.name in STANDARD_FBS:
                ins, _ = STANDARD_FBS[t.name]
                kw = []
                for a in e.args:
                    if a.name is None:
                        raise EmitError(f"line {e.line}: positional argument for {t.name}")
                    key = next((k for k in ins if k.upper() == a.name.upper()), None)
                    if key is None:
                        raise EmitError(f"line {e.line}: {t.name} has no input {a.name}")
                    kw.append((key, self.expr(a.value).node))
                return R(Cl(callee.node, kw=kw), ANY, "stmt")
            pou_fb = self.env.pou(t.name)
            if pou_fb is None:
                raise EmitError(f"line {e.line}: unknown FB {t.name}")
            kw = self.fb_call_args(pou_fb, e.args, e.line)
            return R(Cl(callee.node, kw=kw), ANY, "stmt")
        raise EmitError(f"line {e.line}: cannot call {src(callee.node)}")

    def _is_method(self, name: str) -> bool:
        return not self.scope.is_function and find_method(self.pou, name, self.pous) is not None

    def _method_return(self, m: Method) -> SType:
        if m.header.return_type is None:
            return ANY
        assert m.owner is not None
        saved = self.pou
        try:
            self.pou = m.owner if m.owner.kind != "INTERFACE" else self.pou
            return self.env.from_decl(m.header.return_type, self.const_eval)
        finally:
            self.pou = saved

    def _params(
        self, params: list[VarDecl], args: list[A.Arg], line: int, owner: Pou
    ) -> list[tuple[str, py.expr]]:
        kw: list[tuple[str, py.expr]] = []
        by_name = {p.name.upper(): p for p in params}
        for i, a in enumerate(args):
            if a.output:
                raise EmitError(f"line {line}: output assignment '=>' not supported")
            if a.name is None:
                if i >= len(params):
                    raise EmitError(f"line {line}: too many arguments")
                p = params[i]
            else:
                p0 = by_name.get(a.name.upper())
                if p0 is None:
                    raise EmitError(f"line {line}: unknown parameter {a.name}")
                p = p0
            pt = self._decl_type_in(p, owner)
            kw.append((py_name(p.name), self.arg_value(a.value, pt, p.section)))
        return kw

    def arg_value(self, value: A.Expr, t: SType, section: str) -> py.expr:
        v = self.expr(value)
        if section == "inout":
            return v.node
        return self.coerce(v, t)

    def method_args(self, m: Method, args: list[A.Arg], line: int) -> list[tuple[str, py.expr]]:
        assert m.owner is not None
        return self._params(m.params(), args, line, m.owner)

    def function_args(self, pou: Pou, args: list[A.Arg], line: int) -> list[tuple[str, py.expr]]:
        params = [v for v in pou.vars if v.section in ("input", "inout", "output")]
        kw = self._params(params, args, line, pou)
        target = self.reg.get(pou.name.upper())
        if target is not None and target.hand:
            mapped: list[tuple[str, py.expr]] = []
            for name, value in kw:
                py_param = target.param(name)
                if py_param is None:
                    raise EmitError(f"line {line}: hand written {pou.name} has no parameter {name}")
                mapped.append((py_param, value))
            return mapped
        return kw

    def fb_call_args(self, pou: Pou, args: list[A.Arg], line: int) -> list[tuple[str, py.expr]]:
        params: list[VarDecl] = []
        owners: dict[str, Pou] = {}
        for p in hierarchy(pou, self.pous):
            for v in p.vars:
                if v.section in ("input", "inout"):
                    params.append(v)
                    owners[v.name.upper()] = p
        kw: list[tuple[str, py.expr]] = []
        for a in args:
            if a.name is None:
                raise EmitError(f"line {line}: positional argument in FB call")
            param = next((x for x in params if x.name.upper() == a.name.upper()), None)
            if param is None:
                raise EmitError(f"line {line}: {pou.name} has no input {a.name}")
            pt = self._decl_type_in(param, owners[param.name.upper()])
            kw.append((py_name(param.name), self.arg_value(a.value, pt, param.section)))
        return kw

    # ------------------------------------------------------------------ builtin functions

    def builtin(self, up: str, e: A.Call) -> R | None:
        args = e.args
        m = CONV_RE.match(up)
        if m and m.group(1) in ELEMS and m.group(2) in ELEMS and up.upper() not in self.pous:
            v = self.expr(args[0].value)
            dst = m.group(2)
            dst = {"TIME_OF_DAY": "TOD", "DATE_AND_TIME": "DT"}.get(dst, dst)
            t: SType = STRING if dst in ("STRING", "WSTRING") else SElem(dst)
            return R(Cl(self.use_conv(up), [v.node]), t)
        if up in (
            "LIMIT",
            "MIN",
            "MAX",
            "CONCAT",
            "LEN",
            "LEFT",
            "RIGHT",
            "MID",
            "FIND",
            "REPLACE",
            "INSERT",
            "DELETE",
        ):
            vals = [self.expr(a.value) for a in args]
            names = {
                "LIMIT": ["MN", "IN", "MX"],
                "MID": ["STR", "LEN", "POS"],
                "LEFT": ["STR", "SIZE"],
                "RIGHT": ["STR", "SIZE"],
                "FIND": ["STR1", "STR2"],
                "LEN": ["STR"],
                "REPLACE": ["STR1", "STR2", "L", "P"],
                "INSERT": ["STR1", "STR2", "POS"],
                "DELETE": ["STR", "LEN", "POS"],
            }.get(up)
            if any(a.name is not None for a in args):
                if names is None:
                    raise EmitError(f"line {e.line}: named arguments for {up}")
                order = {n: i for i, n in enumerate(names)}
                keyed = [
                    (order[a.name.upper()] if a.name else i, v)
                    for i, (a, v) in enumerate(zip(args, vals, strict=True))
                ]
                vals = [v for _, v in sorted(keyed, key=lambda p: p[0])]
            rt: SType
            if up in ("CONCAT", "LEFT", "RIGHT", "MID", "REPLACE", "INSERT", "DELETE"):
                rt = STRING
            elif up in ("LEN", "FIND"):
                rt = SElem("INT")
            else:
                rt = vals[1].type if up == "LIMIT" else vals[0].type
                for v in vals:
                    if is_real(v.type):
                        rt = REAL
            return R(Cl(self.use_rt(up), [v.node for v in vals]), rt)
        if up == "TRUNC":
            v = self.expr(args[0].value)
            return R(Cl(self.use_conv("TRUNC"), [v.node]), DINT)
        if up == "SIZEOF":
            arg = args[0].value
            t = self._sizeof_type(arg)
            size = self.env.sizeof(t)
            if size is not None:
                return R(C(size), SElem("UDINT"), extra="literal")
            if isinstance(t, SArray) and (t.lower is None or t.upper is None):
                v = self.expr(arg)
                return R(Cl(self.use_rt("sizeof_value"), [v.node, self.desc(t.elem)]), SElem("UDINT"))
            # size depends on library parameters
            return R(Cl(self.use_rt("type_size"), [self.desc(t)]), SElem("UDINT"))
        if up == "ADR":
            return self.adr(args[0].value)
        if up == "__ISVALIDREF":
            v = self.expr(args[0].value)
            return R(py.Compare(left=v.node, ops=[py.IsNot()], comparators=[C(None)]), BOOL)
        if up in ("SHR", "SHL", "ROL", "ROR"):
            v = self.expr(args[0].value)
            n = self.expr(args[1].value)
            if up == "SHR":
                return R(py.BinOp(left=v.node, op=py.RShift(), right=n.node), v.type)
            if up == "SHL":
                return R(py.BinOp(left=v.node, op=py.LShift(), right=n.node), v.type, arith=True)
            name = int_name(v.type, self.env) or "DWORD"
            return R(Cl(self.use_rt(up), [v.node, n.node, C(name)]), v.type)
        if up in ("LOWER_BOUND", "UPPER_BOUND"):
            v = self.expr(args[0].value)
            return R(Cl(self.use_rt(up), [v.node]), DINT)
        if up.startswith("SYSDEP"):
            return self.sysdep(up, e)
        return None

    def adr(self, arg: A.Expr) -> R:
        if isinstance(arg, A.This):
            return R(N(self.scope.self_name), SPtr(SFb(self.pou.name)))
        if isinstance(arg, A.Index) and len(arg.indices) == 1:
            arr = self.expr(arg.obj)
            if isinstance(arr.type, SArray):
                idx = self.expr(arg.indices[0])
                elem = arr.type.elem
                if not isinstance(elem, SFb | SItf):
                    node = Cl(self.use_rt("ADR_ELEM"), [arr.node, idx.node, self.desc(elem)])
                    return R(node, SPtr(elem))
        v = self.expr(arg)
        t = v.type
        if isinstance(t, SFb | SItf):
            return R(v.node, SPtr(t))
        node = v.node
        if isinstance(node, py.Attribute):
            owner, key = node.value, C(node.attr)
        elif isinstance(node, py.Subscript):
            owner, key = node.value, node.slice
        elif isinstance(node, py.Name) and is_aggregate(t):
            owner, key = node, C(None)
        elif isinstance(node, py.Name):
            box = getattr(self, "box_names", {}).get(node.id)
            if box is not None:
                return R(N(box), SPtr(t), "localptr", node.id)
            return R(Cl(self.use_rt("ADR_VALUE"), [node, self.desc(t)]), SPtr(t), "localptr", node.id)
        else:
            raise EmitError(f"line {arg.line}: ADR of {src(node)}")
        return R(Cl(self.use_rt("ADR"), [owner, key, self.desc(t, node)]), SPtr(t))

    def sysdep(self, up: str, e: A.Call) -> R:
        names = {
            "SYSDEPMEMCPY": ("SysDepMemCpy", ["pDest", "pSrc", "DataLen"]),
            "SYSDEPMEMSET": ("SysDepMemSet", ["pDest", "Value", "DataLen"]),
            "SYSDEPMEMCMP": ("SysDepMemCmp", ["pData1", "pData2", "DataLen"]),
            "SYSDEPISVALIDREAL": ("SysDepIsValidReal", ["Value"]),
        }
        if up not in names:
            raise EmitError(f"line {e.line}: unknown system function {up}")
        name, params = names[up]
        kw: list[tuple[str, py.expr]] = []
        for i, a in enumerate(e.args):
            pname = params[i] if a.name is None else next(p for p in params if p.upper() == a.name.upper())
            kw.append((pname, self.expr(a.value).node))
        rt = BOOL if up == "SYSDEPISVALIDREAL" else DINT
        return R(Cl(self.use_rt(name), kw=kw), rt)

    # ------------------------------------------------------------------ coercion on assignment

    def coerce(self, v: R, t: SType) -> py.expr:
        """Value ``v`` converted for an assignment to type ``t`` (scalars only)."""
        if isinstance(t, SRef):
            t = t.target
        node = v.node
        if isinstance(t, SString):
            if isinstance(v.type, SString) and v.type.length <= t.length:
                return node
            if isinstance(node, py.Constant) and isinstance(node.value, str) and len(node.value) <= t.length:
                return node
            return Cl(self.use_rt("trunc_str"), [node, C(t.length)])
        if isinstance(t, SEnum):
            if isinstance(v.type, SEnum) and v.type.name == t.name:
                return node
            if isinstance(node, py.Constant) and isinstance(node.value, int):
                enum_cls = self.env.gen.enum_classes[t.name]
                for mname, member in enum_cls.__members__.items():
                    if member.value == node.value:
                        return At(self.use_type(t.name), mname)
            inner = node
            if v.arith:
                inner = Cl(self.use_rt("wrap"), [node, C(self.env.enum_base(t.name))])
            return Cl(self.use_type(t.name), [inner])
        if isinstance(t, SElem):
            if t.name in INT_TYPES:
                name = int_name(t, self.env)
                assert name is not None
                if (
                    isinstance(node, py.Constant)
                    and isinstance(node.value, int)
                    and not isinstance(node.value, bool)
                ):
                    lo, hi = _range(name)
                    if lo <= node.value <= hi:
                        return node
                    return C(_wrap(node.value, name))
                if (
                    isinstance(node, py.UnaryOp)
                    and isinstance(node.op, py.USub)
                    and isinstance(node.operand, py.Constant)
                ):
                    val = node.operand.value
                    assert isinstance(val, int)
                    return C(_wrap(-val, name))
                if v.arith and name in ("DINT", "LINT") and self._fits(v.type, name):
                    return node  # no wrap around for 32/64 bit signed arithmetic (readability)
                if v.arith or not self._fits(v.type, name):
                    if is_real(v.type):
                        return Cl(self.use_conv(f"REAL_TO_{name}"), [node])
                    return Cl(self.use_rt("wrap"), [node, C(name)])
                return node
            if t.name in ("REAL", "LREAL"):
                if (
                    isinstance(node, py.Constant)
                    and isinstance(node.value, int)
                    and not isinstance(node.value, bool)
                ):
                    return C(float(node.value))
                if is_int(v.type):
                    return Cl(N("float"), [node])
                return node
            if t.name == "BOOL" and is_int(v.type):
                return Cl(N("bool"), [node])
        if isinstance(t, SPtr) and self._is_null(v) and not isinstance(v.type, SPtr):
            return C(None)
        if isinstance(t, SPtr) and isinstance(v.type, SArray):
            # Codesys: an ARRAY[*] (VAR_IN_OUT, passed as pointer) assigned to a POINTER
            return Cl(self.use_rt("ADR"), [node, C(None), self.desc(v.type, node)])
        return node

    def _fits(self, vt: SType, target: str) -> bool:
        name = int_name(vt, self.env)
        if name is None:
            return isinstance(vt, SAny) or is_bool(vt)
        if name == target:
            return True
        lo, hi = _range(name)
        tlo, thi = _range(target)
        return tlo <= lo and hi <= thi

    # ------------------------------------------------------------------ assignment targets

    def lvalue(self, e: A.Expr) -> Lv:
        if isinstance(e, A.BitAccess):
            base = self.lvalue(e.obj)
            return Lv(base.node, BOOL, bit=(base, e.bit))
        if (
            isinstance(e, A.Name)
            and self.scope.callable_name.upper() == e.id.upper()
            and e.id.upper() not in self.scope.locals
        ):
            raise EmitError(f"line {e.line}: return value not declared")
        r = self.expr(e)
        if (
            isinstance(r.node, py.Call)
            and isinstance(r.node.func, py.Attribute)
            and r.node.func.attr == "deref"
        ):
            return Lv(r.node, r.type, kind="pointer")
        if not isinstance(r.node, py.Name | py.Attribute | py.Subscript):
            raise EmitError(f"line {e.line}: cannot assign to {src(r.node)}")
        kind = "value"
        if isinstance(r.extra, Var) and r.extra.kind == "retval":
            kind = "retval"
        return Lv(r.node, r.type, kind=kind)

    # ------------------------------------------------------------------ statements

    def comments(self, out: Out, indent: int, comments: list[str]) -> None:
        for c in comments:
            for line in _comment_lines(c):
                out.add(indent, line)

    def block(self, out: Out, indent: int, stmts: list[A.Stmt], tail: list[str] | None = None) -> None:
        start = len(out.lines)
        code_lines = 0
        for i, s in enumerate(stmts):
            after = self._names_after(stmts[i + 1 :])
            self.loop_after.append(after)
            try:
                before = len(out.lines)
                self.stmt(out, indent, s, first=(i == 0))
                code_lines += sum(
                    1 for ln in out.lines[before:] if ln.strip() and not ln.strip().startswith("#")
                )
            finally:
                self.loop_after.pop()
        if tail:
            self.comments(out, indent, tail)
        if code_lines == 0:
            out.add(indent, "pass")
        _ = start

    def _names_after(self, stmts: list[A.Stmt]) -> set[str]:
        names: set[str] = set()
        for s in stmts:
            for n in _walk_names(s):
                names.add(n.upper())
        for outer in self.loop_after:
            names |= outer
        return names

    def stmt(self, out: Out, indent: int, s: A.Stmt, first: bool = False) -> None:
        if s.blank_before and not first:
            out.add(0, "")
        self.comments(out, indent, s.comments)
        trailing = f"  # {_one_line(s.trailing)}" if s.trailing else ""
        try:
            self._stmt(out, indent, s, trailing)
        except EmitError:
            raise
        except Exception as exc:
            raise EmitError(f"line {s.line}: {type(exc).__name__}: {exc}") from exc

    def _stmt(self, out: Out, indent: int, s: A.Stmt, trailing: str) -> None:
        if isinstance(s, A.Empty):
            if trailing:
                out.add(indent, trailing.strip())
            return
        if isinstance(s, A.Assign):
            self.assign(out, indent, s, trailing)
            return
        if isinstance(s, A.ExprStmt):
            if isinstance(s.expr, A.Call) and self._memcpy_to_local(out, indent, s.expr, trailing):
                return
            boxes = self._local_adr_args(s.expr)
            for local, t in boxes:
                out.add(
                    indent,
                    f"_adr_{local} = {src(Cl(self.use_rt('ADR_VALUE'), [N(local), self.desc(t)]))}  # ADR({local})",
                )
            self.box_names = {local: f"_adr_{local}" for local, _ in boxes}
            try:
                r = self.expr(s.expr)
            finally:
                self.box_names = {}
            out.add(indent, src(r.node) + trailing)
            for local, _ in boxes:
                out.add(indent, f"{local} = _adr_{local}.value")
            return
        if isinstance(s, A.If):
            for i, (cond, body) in enumerate(s.branches):
                c = self.expr(cond)
                kw = "if" if i == 0 else "elif"
                out.add(indent, f"{kw} {src(c.node)}:" + (trailing if i == 0 else ""))
                self.block(out, indent + 1, body)
            if s.else_body is not None:
                out.add(indent, "else:")
                self.comments(out, indent + 1, s.else_comments)
                self.block(out, indent + 1, s.else_body)
            return
        if isinstance(s, A.Case):
            self.case(out, indent, s, trailing)
            return
        if isinstance(s, A.For):
            self.for_(out, indent, s, trailing)
            return
        if isinstance(s, A.While):
            c = self.expr(s.cond)
            out.add(indent, f"while {src(c.node)}:" + trailing)
            self.block(out, indent + 1, s.body)
            return
        if isinstance(s, A.Repeat):
            out.add(indent, "while True:" + trailing)
            self.block(out, indent + 1, s.body)
            c = self.expr(s.until)
            out.add(indent + 1, f"if {src(c.node)}:")
            out.add(indent + 2, "break")
            return
        if isinstance(s, A.Exit):
            out.add(indent, "break" + trailing)
            return
        if isinstance(s, A.Continue):
            out.add(indent, "continue" + trailing)
            return
        if isinstance(s, A.Return):
            out.add(indent, self.return_stmt() + trailing)
            return
        raise EmitError(f"line {s.line}: unsupported statement {type(s).__name__}")

    def return_stmt(self) -> str:
        ret = self.scope.locals.get(self.scope.callable_name.upper())
        if ret is not None and ret.kind == "retval":
            return f"return {ret.py}"
        return "return"

    def _local_adr_args(self, e: A.Expr) -> list[tuple[str, SType]]:
        """Local scalars passed as ``ADR(x)`` to a call (may be written through the pointer)."""
        if not isinstance(e, A.Call):
            return []
        out: list[tuple[str, SType]] = []
        for a in e.args:
            v = a.value
            if (
                isinstance(v, A.Call)
                and isinstance(v.func, A.Name)
                and v.func.id.upper() == "ADR"
                and isinstance(v.args[0].value, A.Name)
            ):
                var = self.scope.locals.get(v.args[0].value.id.upper())
                if (
                    var is not None
                    and not is_aggregate(var.type)
                    and not isinstance(var.type, SFb | SItf | SRef | SPtr)
                ):
                    out.append((var.py, var.type))
        return out

    def _memcpy_to_local(self, out: Out, indent: int, e: A.Call, trailing: str) -> bool:
        """``SysDepMemCpy(ADR(localScalar), src, n)`` -> ``local = mem_read(src, T, n, local)``."""
        if not (isinstance(e.func, A.Name) and e.func.id.upper() in ("SYSDEPMEMCPY", "SYSDEPMEMSET")):
            return False
        names = ["PDEST", "PSRC" if e.func.id.upper() == "SYSDEPMEMCPY" else "VALUE", "DATALEN"]
        args: dict[str, A.Expr] = {}
        for i, a in enumerate(e.args):
            args[a.name.upper() if a.name else names[i]] = a.value
        dest = args.get("PDEST")
        if not (isinstance(dest, A.Call) and isinstance(dest.func, A.Name) and dest.func.id.upper() == "ADR"):
            return False
        d = self.adr(dest.args[0].value)
        if d.kind != "localptr":
            return False
        if e.func.id.upper() == "SYSDEPMEMSET":
            raise EmitError(f"line {e.line}: SysDepMemSet of a local scalar is not supported")
        local = d.extra
        assert isinstance(d.type, SPtr)
        n = self.expr(args["DATALEN"]).node
        srcp = self.expr(args["PSRC"]).node
        call = Cl(self.use_rt("mem_read"), [srcp, self.desc(d.type.target), n, N(local)])
        out.add(indent, f"{local} = {src(call)}" + trailing)
        return True

    def assign(self, out: Out, indent: int, s: A.Assign, trailing: str) -> None:
        if s.ref and isinstance(s.target, A.Name):
            var = self.scope.locals.get(s.target.id.upper())
            if var is not None and var.kind == "refalias":
                value = self.expr(s.value)
                var.alias = value.node
                out.add(
                    indent,
                    f"# {var.name} REF= {src(value.node)}  (reference: {var.name} is replaced by it)"
                    + trailing,
                )
                return
        targets = [s.target, *s.chain]
        value = self.expr(s.value)
        # assign right to left: a := b := c  ->  b = c; a = b
        for i, target in enumerate(reversed(targets)):
            lv = self.lvalue(target)
            line = self.assign_one(lv, value, s.ref)
            out.add(indent, line + (trailing if i == len(targets) - 1 else ""))
            value = self.expr(target)

    def assign_one(self, lv: Lv, value: R, ref: bool) -> str:
        if lv.bit is not None:
            base, bitno = lv.bit
            node = Cl(self.use_rt("set_bit"), [base.node, C(bitno), value.node])
            return f"{src(base.node)} = {src(node)}"
        t = lv.type
        if ref:
            return f"{src(lv.node)} = {src(value.node)}"
        if lv.kind == "pointer":
            if is_aggregate(t):
                return src(Cl(self.use_rt("copy_into"), [lv.node, value.node]))
            assert isinstance(lv.node, py.Call) and isinstance(lv.node.func, py.Attribute)
            store = Cl(At(lv.node.func.value, "store"), [lv.node.args[0], self.coerce(value, t)])
            return src(store)
        if isinstance(t, SRef):
            t = t.target
        if is_aggregate(t):
            if isinstance(value.type, SAny) and not isinstance(value.node, py.Call):
                self.warnings.append(f"aggregate assignment from untyped value {src(value.node)}")
            return src(Cl(self.use_rt("copy_into"), [lv.node, value.node]))
        if isinstance(t, SPtr) and value.kind == "localptr":
            raise EmitError("pointer to a local variable stored")
        return f"{src(lv.node)} = {src(self.coerce(value, t))}"

    def case(self, out: Out, indent: int, s: A.Case, trailing: str) -> None:
        sel = self.expr(s.selector)
        out.add(indent, f"match {src(sel.node)}:" + trailing)
        for br in s.branches:
            if br.blank_before:
                out.add(0, "")
            self.comments(out, indent + 1, br.comments)
            patterns: list[str] = []
            guards: list[str] = []
            for lab in br.labels:
                low = (
                    self.coerce(self.expr(lab.low), sel.type)
                    if isinstance(sel.type, SEnum)
                    else self.expr(lab.low).node
                )
                if lab.high is not None:
                    high = self.expr(lab.high).node
                    guards.append(f"{src(low)} <= {src(sel.node)} <= {src(high)}")
                elif isinstance(low, py.Name | py.Call):
                    guards.append(f"{src(sel.node)} == {src(low)}")
                else:
                    patterns.append(src(low))
            if guards:
                cond = " or ".join([*(f"{src(sel.node)} == {p}" for p in patterns), *guards])
                out.add(indent + 1, f"case _ if {cond}:")
            else:
                out.add(indent + 1, f"case {' | '.join(patterns)}:")
            self.block(out, indent + 2, br.body)
        if s.else_body is not None:
            out.add(indent + 1, "case _:")
            self.comments(out, indent + 2, s.else_comments)
            self.block(out, indent + 2, s.else_body)

    def for_(self, out: Out, indent: int, s: A.For, trailing: str) -> None:
        var = self.expr(A.Name(s.var, line=s.line))
        start = self.expr(s.start)
        end = self.expr(s.end)
        step = self.expr(s.step) if s.step is not None else None
        step_value: int | None = 1
        if step is not None:
            step_value = None
            if isinstance(step.node, py.Constant) and isinstance(step.node.value, int):
                step_value = step.node.value
            if (
                isinstance(step.node, py.UnaryOp)
                and isinstance(step.node.operand, py.Constant)
                and isinstance(step.node.operand.value, int)
            ):
                step_value = -step.node.operand.value
        args: list[py.expr] = [start.node]
        if step_value is None:
            assert step is not None
            rng = Cl(self.use_rt("st_range"), [start.node, end.node, step.node])
        else:
            if isinstance(end.node, py.Constant) and isinstance(end.node.value, int):
                stop: py.expr = C(end.node.value + (1 if step_value > 0 else -1))
            else:
                op: py.operator = py.Add() if step_value > 0 else py.Sub()
                stop = py.BinOp(left=end.node, op=op, right=C(1))
            args.append(stop)
            if step_value != 1:
                args.append(C(step_value))
            rng = Cl(N("range"), args)
        target = src(var.node)
        assigned = any(
            isinstance(x, A.Assign) and isinstance(x.target, A.Name) and x.target.id.upper() == s.var.upper()
            for x in _walk_stmts(s.body)
        )
        if assigned:
            raise EmitError(f"line {s.line}: FOR variable {s.var} is changed in the loop")
        out.add(indent, f"for {target} in {src(rng)}:" + trailing)
        self.block(out, indent + 1, s.body)
        if s.var.upper() in (self.loop_after[-1] if self.loop_after else set()):
            end_args = [start.node, end.node] + ([step.node] if step is not None else [])
            out.add(indent, "else:")
            out.add(indent + 1, f"{target} = {src(Cl(self.use_rt('st_for_end'), end_args))}")


# ---------------------------------------------------------------------- helpers


def _size(name: str) -> int:
    from .sem import ELEM_SIZE, WRAP_AS

    return ELEM_SIZE[WRAP_AS.get(name, name)]


def _range(name: str) -> tuple[int, int]:
    from .sem import WRAP_AS

    name = WRAP_AS.get(name, name)
    bits = _size(name) * 8
    if name in ("SINT", "INT", "DINT", "LINT"):
        return -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    return 0, (1 << bits) - 1


def _wrap(value: int, name: str) -> int:
    lo, hi = _range(name)
    mod = hi - lo + 1
    v = value % mod
    if lo < 0 and v > hi:
        v -= mod
    return v


def _one_line(text: str) -> str:
    return " ".join(text.split())


def _comment_lines(c: str) -> list[str]:
    if c.startswith("(*"):
        body = c[2:-2]
        lines = body.splitlines() or [""]
        # keep relative indentation of block comments (often commented out code)
        stripped = [ln.rstrip() for ln in lines]
        while stripped and not stripped[0].strip():
            stripped.pop(0)
        while stripped and not stripped[-1].strip():
            stripped.pop()
        margin = min((len(ln) - len(ln.lstrip()) for ln in stripped if ln.strip()), default=0)
        return [("# " + ln[margin:]).rstrip() for ln in stripped] or ["#"]
    if c.startswith("{"):
        return ["# " + _one_line(c)]
    text = c[1:] if c.startswith("/") else c  # '///' doc comment
    return [("# " + text.strip()).rstrip() if text.strip() else "#"]


def _walk_stmts(stmts: list[A.Stmt]) -> Iterator[A.Stmt]:
    for s in stmts:
        yield s
        if isinstance(s, A.If):
            for _, body in s.branches:
                yield from _walk_stmts(body)
            if s.else_body:
                yield from _walk_stmts(s.else_body)
        elif isinstance(s, A.Case):
            for br in s.branches:
                yield from _walk_stmts(br.body)
            if s.else_body:
                yield from _walk_stmts(s.else_body)
        elif isinstance(s, A.For | A.While | A.Repeat):
            yield from _walk_stmts(s.body)


def _walk_expr_names(e: object) -> Iterator[str]:
    if isinstance(e, A.Name):
        yield e.id
    elif isinstance(e, A.Member | A.BitAccess | A.Deref):
        yield from _walk_expr_names(e.obj)
    elif isinstance(e, A.Index):
        yield from _walk_expr_names(e.obj)
        for i in e.indices:
            yield from _walk_expr_names(i)
    elif isinstance(e, A.Call):
        yield from _walk_expr_names(e.func)
        for a in e.args:
            yield from _walk_expr_names(a.value)
    elif isinstance(e, A.BinOp):
        yield from _walk_expr_names(e.left)
        yield from _walk_expr_names(e.right)
    elif isinstance(e, A.UnaryOp):
        yield from _walk_expr_names(e.operand)


def _walk_names(s: A.Stmt) -> Iterator[str]:
    for x in _walk_stmts([s]):
        for v in vars(x).values():
            if isinstance(v, A.Expr):
                yield from _walk_expr_names(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, A.Expr):
                        yield from _walk_expr_names(item)
                    elif isinstance(item, tuple):
                        for y in item:
                            if isinstance(y, A.Expr):
                                yield from _walk_expr_names(y)
                    elif isinstance(item, A.CaseBranch):
                        for lab in item.labels:
                            yield from _walk_expr_names(lab.low)
        if isinstance(x, A.For):
            yield x.var


__all__ = ["EmitError", "PouEmitter"]
