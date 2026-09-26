"""Emit a complete Python module for a POU."""

from __future__ import annotations

import ast as py
from collections.abc import Iterator

from tools.plcopen_gen.emitter import py_name

from . import ast as A
from .decl import ArrayInit, Init, StructInit, VarDecl
from .emit import RT, At, C, Cl, EmitError, N, Out, PouEmitter, R, _comment_lines, _walk_stmts, src
from .library import Body, Method, Pou, Property
from .scope import Scope, Var, hierarchy, inst_attr
from .sem import (
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
    is_aggregate,
)

# mypy error codes disabled in the generated modules (dynamic IEC semantics)
MYPY_DISABLED = (
    "no-any-return",
    "assignment",
    "arg-type",
    "attr-defined",
    "union-attr",
    "operator",
    "index",
    "misc",
    "override",
    "call-arg",
    "comparison-overlap",
    "return-value",
    "has-type",
    "name-defined",
    "no-untyped-def",
    "var-annotated",
    "valid-type",
    "call-overload",
    "unreachable",
    "truthy-function",
)

SECTION_TITLES = {
    "input": "VAR_INPUT",
    "output": "VAR_OUTPUT",
    "inout": "VAR_IN_OUT",
    "local": "VAR",
    "temp": "VAR_TEMP",
    "stat": "VAR_STAT",
    "inst": "VAR_INST",
}


class ModuleEmitter(PouEmitter):
    # ------------------------------------------------------------------ values

    def default(self, t: SType, init: Init | None) -> py.expr:
        if init is not None:
            if isinstance(init, StructInit):
                if not isinstance(t, SStruct):
                    raise EmitError(f"structure initial value for {t}")
                kw: list[tuple[str, py.expr]] = []
                for name, value in init.members:
                    f = self.env.struct_field(t.name, name)
                    if f is None:
                        raise EmitError(f"{t.name} has no member {name}")
                    kw.append((f[0], self.default(f[1], value)))
                return Cl(self.use_type(t.name), kw=kw)
            if isinstance(init, ArrayInit):
                if not isinstance(t, SArray) or t.lower is None or t.upper is None or t.dynamic:
                    raise EmitError(f"array initial value for {t}")
                items: list[py.expr] = []
                for repeat, value in init.items:
                    n = 1 if repeat is None else self.const_eval(repeat)
                    items.extend(self.default(t.elem, value) for _ in range(n))
                count = t.upper - t.lower + 1
                while len(items) < count:
                    items.append(self.default(t.elem, None))
                init_list = py.List(elts=items, ctx=py.Load())
                if t.lower == 0:
                    return init_list
                return Cl(At(self.use_iec(), "IecArray"), [C(t.lower), init_list])
            v = self.expr(init)
            if is_aggregate(t):
                raise EmitError("aggregate initialised from an expression")
            return self.coerce(v, t)
        if isinstance(t, SElem):
            return C(False if t.name == "BOOL" else 0.0 if t.name in ("REAL", "LREAL") else 0)
        if isinstance(t, SString):
            return C("")
        if isinstance(t, SEnum):
            first = next(iter(self.env.gen.enum_classes[t.name].__members__))
            return At(self.use_type(t.name), first)
        if isinstance(t, SStruct):
            return Cl(self.use_type(t.name))
        if isinstance(t, SArray):
            if t.lower is None or t.upper is None:
                return py.List(elts=[], ctx=py.Load())
            size: py.expr = C(t.upper - t.lower + 1)
            if t.dynamic:
                size = Cl(At(self.use_iec(), "array_len"), [self.bound(t, "lower"), self.bound(t, "upper")])
            elem = self.default(t.elem, None)
            if isinstance(elem, py.Constant) or (
                isinstance(elem, py.Attribute) and isinstance(t.elem, SEnum)
            ):
                lst: py.expr = py.BinOp(left=py.List(elts=[elem], ctx=py.Load()), op=py.Mult(), right=size)
            else:
                comp = py.comprehension(
                    target=py.Name(id="_", ctx=py.Store()), iter=Cl(N("range"), [size]), ifs=[], is_async=0
                )
                lst = py.ListComp(elt=elem, generators=[comp])
            if t.lower == 0:
                return lst
            return Cl(At(self.use_iec(), "IecArray"), [C(t.lower), lst])
        if isinstance(t, SFb):
            if t.name in ("R_TRIG", "F_TRIG", "TON", "TOF", "TP"):
                return Cl(self.use("srci.iec.standard", t.name))
            return Cl(self.use_pou(t.name))
        return C(None)

    # ------------------------------------------------------------------ module

    def emit_module(self) -> str:
        body = Out()
        if self.pou.kind == "FUNCTION":
            self.emit_function(body)
        elif self.pou.kind == "INTERFACE":
            self.emit_interface(body)
        else:
            self.emit_fb(body)
        return self.module_header() + "\n".join(body.lines).rstrip() + "\n"

    def module_header(self) -> str:
        doc = (" ".join(self.pou.header.doc) or self.pou.name).replace("\\", "\\\\").replace('"', '\\"')
        lines = [
            f'"""{doc}',
            "",
            f"ST-Source: {self.pou.st_path}",
            "Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.",
            '"""',
            "",
            "# ruff: noqa",
            "# fmt: off",
            f'# mypy: disable-error-code="{",".join(MYPY_DISABLED)}"',
            "from __future__ import annotations",
            "",
            "from typing import TYPE_CHECKING, Any",
            "",
        ]
        plain = sorted(k for k in self.imports if k.startswith(("import ", "from ")))
        for k in plain:
            lines.append(k)
        for module in sorted(k for k in self.imports if not k.startswith(("import ", "from "))):
            names = sorted(self.imports[module])
            if module == f"{self.reg[self.pou.name.upper()].module}":
                continue
            lines.append(f"from {module} import {', '.join(names)}")
        tc = {m: n - self.imports.get(m, set()) for m, n in self.tc_imports.items()}
        tc = {m: n for m, n in tc.items() if n and m != self.reg[self.pou.name.upper()].module}
        if tc:
            lines.append("")
            lines.append("if TYPE_CHECKING:")
            for module in sorted(tc):
                lines.append(f"    from {module} import {', '.join(sorted(tc[module]))}")
        lines.append("")
        lines.append(f"__all__ = [{self.pou.name!r}]")
        lines.append("")
        lines.append("")
        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------ interface

    def emit_interface(self, out: Out) -> None:
        self.imports.setdefault("typing", set()).add("Protocol")
        out.add(0, f"class {self.pou.name}(Protocol):")
        for m in self.pou.methods.values():
            params = self.signature(m.vars, m.owner or self.pou)
            ret = self._method_return(m)
            ann = self.ann(ret) if m.header.return_type else "None"
            out.add(1, f"def {m.name}(self{params}) -> {ann}: ...")
        for p in self.pou.properties.values():
            out.add(1, f"{p.name}: {self.ann(self.type_of_prop(p))}")
        if not self.pou.methods and not self.pou.properties:
            out.add(1, "pass")

    # ------------------------------------------------------------------ functions

    def emit_function(self, out: Out) -> None:
        pou = self.pou
        self.scope = Scope(pou)
        ret_t = (
            self.env.from_decl(pou.header.return_type, self.const_eval) if pou.header.return_type else None
        )
        params = self.signature(pou.vars, pou)
        ann = self.ann(ret_t) if ret_t is not None else "None"
        out.add(0, f"def {pou.name}(*{params}) -> {ann}:")
        self.doc(out, 1, pou.header.doc)
        self.function_body(out, 1, pou.vars, pou.body, ret_t, pou.name)

    def doc(self, out: Out, indent: int, doc: list[str]) -> None:
        text = " ".join(d for d in doc if d).replace("\\", "\\\\").replace('"', '\\"')
        if text:
            out.add(indent, f'"""{text}"""')

    def signature(self, vars_: list[VarDecl], owner: Pou) -> str:
        parts: list[str] = []
        for v in vars_:
            if v.section not in ("input", "inout", "output"):
                continue
            t = self._decl_type_in(v, owner)
            name = py_name(v.name)
            if v.section == "inout":
                parts.append(f"{name}: {self.ann(t)}")
            elif (
                is_aggregate(t)
                or isinstance(t, SFb)
                or (v.init is not None and not isinstance(v.init, A.Literal | A.EnumLiteral | A.Member))
            ):
                parts.append(f"{name}: {self.ann(t)} | None = None")
            else:
                saved = self.shadow
                self.shadow = set()
                try:
                    default = src(self.default(t, v.init))
                finally:
                    self.shadow = saved
                parts.append(f"{name}: {self.ann(t)} = {default}")
        return (", " + ", ".join(parts)) if parts else ""

    def function_body(
        self,
        out: Out,
        indent: int,
        vars_: list[VarDecl],
        body: Body | None,
        ret_t: SType | None,
        ret_name: str,
        self_first: bool = False,
    ) -> None:
        """Local variables, parameter handling, statements and the return."""
        self.shadow = {py_name(v.name) for v in vars_} | ({py_name(ret_name)} if ret_t is not None else set())
        self.scope.locals = {}
        for v in vars_:
            if v.section == "inst":
                continue
            kind = {"input": "input", "inout": "inout", "output": "output"}.get(v.section, "local")
            t = self.type_of_decl(v)
            self.scope.add_local(Var(v.name, py_name(v.name), t, kind, v))
        if ret_t is not None:
            self.scope.add_local(Var(ret_name, py_name(ret_name), ret_t, "retval"))
        stmts = body.stmts if body is not None else []
        tail = body.tail_comments if body is not None else []
        # local REFERENCEs bound once with REF= at the top level become aliases
        for var in self.scope.locals.values():
            if not isinstance(var.type, SRef) or var.kind != "local":
                continue
            binds = [
                x
                for x in _walk_stmts(stmts)
                if isinstance(x, A.Assign)
                and x.ref
                and isinstance(x.target, A.Name)
                and x.target.id.upper() == var.name.upper()
            ]
            if not binds or (len(binds) == 1 and binds[0] in stmts):
                var.kind = "refalias"
            elif not isinstance(var.type.target, SStruct | SArray | SFb):
                raise EmitError(f"REFERENCE TO scalar {var.name} must be bound exactly once at the top level")
        mutated = _mutated_names(stmts)
        # parameters: defaults of aggregates, copies of inputs that are changed
        for v in vars_:
            if v.section != "input":
                continue
            var = self.scope.locals[v.name.upper()]
            t = var.type
            name = var.py
            if (
                is_aggregate(t)
                or isinstance(t, SFb)
                or (v.init is not None and not isinstance(v.init, A.Literal | A.EnumLiteral | A.Member))
            ):
                out.add(indent, f"if {name} is None:")
                out.add(indent + 1, f"{name} = {src(self.default(t, v.init))}")
                if (is_aggregate(t) or isinstance(t, SFb)) and v.name.upper() in mutated:
                    out.add(indent, "else:")
                    out.add(
                        indent + 1,
                        f"{name} = {src(Cl(self.use_rt('copy_value'), [N(name)]))}  # VAR_INPUT is a copy in ST",
                    )
            elif isinstance(t, SString) and not isinstance(t, SAny):
                pass
        # return value and local variables
        if ret_t is not None:
            out.add(indent, f"{py_name(ret_name)}: {self.ann(ret_t)} = {src(self.default(ret_t, None))}")
        for v in vars_:
            if v.section in ("input", "inout", "output", "inst"):
                continue
            var = self.scope.locals[v.name.upper()]
            if var.kind == "refalias":
                for d in v.doc:
                    out.add(indent, f"# {d}")
                out.add(indent, f"# {var.py}: REFERENCE TO ... (alias, see REF= below)")
                continue
            for d in v.doc:
                out.add(indent, f"# {d}")
            out.add(indent, f"{var.py}: {self.ann(var.type)} = {src(self.default(var.type, v.init))}")
        has_locals = ret_t is not None or any(
            v.section not in ("input", "inout", "output", "inst") for v in vars_
        )
        if has_locals and stmts:
            out.add(0, "")
        self.block(out, indent, stmts, tail)
        if ret_t is not None and not (stmts and isinstance(stmts[-1], A.Return)):
            out.add(indent, f"return {py_name(ret_name)}")

    # ------------------------------------------------------------------ function blocks

    def bases(self) -> list[str]:
        out: list[str] = []
        mixin = self.cfg.mixins.get(self.pou.name)
        if mixin is not None:
            out.append(src(self.use(mixin.module, mixin.name)))
        if self.pou.extends:
            out.append(src(self.use_pou(self.pou.extends)))
        else:
            out.append(src(self.use("srci.iec.fb", "FunctionBlock")))
        return out

    def emit_fb(self, out: Out) -> None:
        pou = self.pou
        out.add(0, f"class {pou.name}({', '.join(self.bases())}):")
        self.doc(out, 1, pou.header.doc)
        self.emit_vars(out)
        self.emit_call(out)
        for m in sorted(pou.methods.values(), key=lambda m: m.name.upper()):
            if m.name.upper() in self.hand_methods:
                continue
            self.emit_method(out, m)
        for p in sorted(pou.properties.values(), key=lambda p: p.name.upper()):
            self.emit_property(out, p)

    def emit_vars(self, out: Out) -> None:
        pou = self.pou
        self.scope = Scope(pou)
        self.shadow = set()
        out.add(0, "")
        out.add(1, "def _init_vars_(self) -> None:")
        section = None
        n = 0
        for v in pou.vars:
            title = SECTION_TITLES.get(v.section, "VAR") + (" CONSTANT" if v.constant else "")
            if title != section:
                out.add(2, f"# {title}")
                section = title
            for d in v.doc:
                out.add(2, f"# {d}")
            for a in v.attributes:
                out.add(2, f"# {a}")
            t = self.type_of_decl(v)
            value = C(None) if v.section == "inout" else self.default(t, v.init)
            trailing = f"  # {v.trailing}" if v.trailing else ""
            out.add(2, f"self.{py_name(v.name)}: {self.ann(t)} = {src(value)}{trailing}")
            n += 1
        for m in pou.methods.values():
            inst = [v for v in m.vars if v.section == "inst"]
            if inst and m.name.upper() not in self.hand_methods:
                out.add(2, f"# VAR_INST of {m.name}")
                self.scope = Scope(pou, m)
                for v in inst:
                    t = self.type_of_decl(v)
                    out.add(2, f"self.{inst_attr(m, v)}: {self.ann(t)} = {src(self.default(t, v.init))}")
                    n += 1
        if n == 0:
            out.add(2, "pass")

    def emit_call(self, out: Out) -> None:
        pou = self.pou
        self.scope = Scope(pou)
        self.shadow = set()
        params: list[tuple[VarDecl, Pou]] = []
        seen: set[str] = set()
        for p in hierarchy(pou, self.pous):
            for v in p.vars:
                if v.section in ("input", "inout") and v.name.upper() not in seen:
                    params.append((v, p))
                    seen.add(v.name.upper())
        sig = ", ".join(
            f"{py_name(v.name)}: {self.ann(self._decl_type_in(v, p))} | None = None" for v, p in params
        )
        out.add(0, "")
        out.add(1, f"def __call__(self{', *, ' + sig if sig else ''}) -> None:")
        for v, p in params:
            t = self._decl_type_in(v, p)
            name = py_name(v.name)
            out.add(2, f"if {name} is not None:")
            if v.section == "inout" or isinstance(t, SFb | SItf | SPtr | SRef):
                out.add(3, f"self.{name} = {name}")
            elif is_aggregate(t):
                out.add(3, f"{src(Cl(self.use_rt('copy_into'), [At(N('self'), name), N(name)]))}")
            else:
                out.add(3, f"self.{name} = {src(self.coerce(R(N(name), SAny()), t))}")
        body = pou.body
        out.add(2, "self.__body()")
        out.add(0, "")
        out.add(1, "def __body(self) -> None:")
        self.scope = Scope(pou)
        self.shadow = set()
        self.block(out, 2, body.stmts, body.tail_comments)

    def emit_method(self, out: Out, m: Method) -> None:
        self.scope = Scope(self.pou, m)
        self.shadow = {py_name(v.name) for v in m.vars} | {py_name(m.name)}
        ret_t = self._method_return(m) if m.header.return_type else None
        params = self.signature(m.vars, self.pou)
        ann = self.ann(ret_t) if ret_t is not None else "None"
        out.add(0, "")
        access = f"  # {m.header.access}" if m.header.access else ""
        star = ", *" if params else ""
        out.add(1, f"def {m.name}(self{star}{params}) -> {ann}:{access}")
        self.doc(out, 2, m.header.doc)
        self.function_body(out, 2, m.vars, m.body, ret_t, m.name)

    def emit_property(self, out: Out, p: Property) -> None:
        t = self.type_of_prop(p)
        getter = setter = "None"
        if p.get_body is not None:
            self.scope = Scope(self.pou, prop=p, accessor="get")
            out.add(0, "")
            out.add(1, f"def _get_{p.name}(self) -> {self.ann(t)}:")
            self.doc(out, 2, p.header.doc)
            self.function_body(out, 2, p.get_vars or [], p.get_body, t, p.name)
            getter = f"_get_{p.name}"
        if p.set_body is not None:
            self.scope = Scope(self.pou, prop=p, accessor="set")
            out.add(0, "")
            out.add(1, f"def _set_{p.name}(self, {py_name(p.name)}: {self.ann(t)}) -> None:")
            vars_ = [VarDecl(p.name, p.type, "input"), *(p.set_vars or [])]
            self.function_body_setter(out, 2, vars_, p.set_body)
            setter = f"_set_{p.name}"
        out.add(0, "")
        access = f"  # {p.header.access}" if p.header.access else ""
        out.add(1, f"{p.name} = property({getter}, {setter}){access}")

    def function_body_setter(self, out: Out, indent: int, vars_: list[VarDecl], body: Body) -> None:
        self.function_body(out, indent, vars_, body, None, "")


def _mutated_names(stmts: list[A.Stmt]) -> set[str]:
    """Root names that are assigned, called with methods or passed to ADR."""
    names: set[str] = set()

    def root(e: A.Expr) -> str | None:
        while isinstance(e, A.Member | A.Index | A.BitAccess | A.Deref):
            e = e.obj
        return e.id.upper() if isinstance(e, A.Name) else None

    def exprs(e: object) -> Iterator[A.Expr]:
        if isinstance(e, A.Expr):
            yield e
            for v in vars(e).values():
                if isinstance(v, A.Expr):
                    yield from exprs(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, A.Arg):
                            yield from exprs(item.value)
                        else:
                            yield from exprs(item)

    for s in _walk_stmts(stmts):
        if isinstance(s, A.Assign):
            for t in [s.target, *s.chain]:
                r = root(t)
                if r:
                    names.add(r)
        for v in vars(s).values():
            candidates = (
                [v]
                if isinstance(v, A.Expr)
                else [x for x in v if isinstance(x, A.Expr)]
                if isinstance(v, list)
                else []
            )
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, tuple):
                        candidates.extend(x for x in item if isinstance(x, A.Expr))
            for c in candidates:
                for e in exprs(c):
                    if isinstance(e, A.Call):
                        if isinstance(e.func, A.Member):
                            r = root(e.func.obj)
                            if r:
                                names.add(r)
                        if isinstance(e.func, A.Name) and e.func.id.upper() == "ADR":
                            r = root(e.args[0].value)
                            if r:
                                names.add(r)
    return names


__all__ = ["RT", "ModuleEmitter", "_comment_lines"]
