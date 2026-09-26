"""ST -> Python transpiler (tools/st2py): lexer, parser, declarations and the semantics
of the generated code (small ST programs are transpiled and executed)."""

from __future__ import annotations

import copy
from collections.abc import Iterator
from dataclasses import replace
from typing import Any

import pytest

from tools.st2py import ast as A
from tools.st2py.__main__ import DEFAULT_XML, PatchError, apply_patches, load
from tools.st2py.config import CONFIG, Config, SourcePatch
from tools.st2py.decl import TArray, TElem, TNamed, TPointer, TReference, TString, parse_interface
from tools.st2py.emit import EmitError
from tools.st2py.lexer import LexError, time_to_ms, tokenize, unescape_string
from tools.st2py.library import Body, Method, Pou, Property
from tools.st2py.module import ModuleEmitter
from tools.st2py.parser import ParseError, parse_body, parse_expression
from tools.st2py.registry import Target
from tools.st2py.sem import TypeEnv

# ---------------------------------------------------------------- lexer


def test_literals() -> None:
    toks = tokenize("16#FF 2#1010 T#1m30s 1.5E2 USINT#5 'a$'b$N' DATE#1970-01-02 x REF= y")
    kinds = [(t.kind, t.value) for t in toks]
    assert kinds[0] == ("int", 255)
    assert kinds[1] == ("int", 10)
    assert kinds[2] == ("time", 90_000)
    assert kinds[3] == ("real", 150.0)
    assert kinds[4][0] == "typed" and kinds[5] == ("int", 5)
    assert kinds[6] == ("string", "a'b\n")
    assert kinds[7] == ("date", 86_400)
    assert [t.text for t in toks[-3:]] == ["x", "REF=", "y"]
    assert time_to_ms("T#-1s") == -1000
    assert unescape_string("'$41$$'") == "A$"
    with pytest.raises(LexError):
        time_to_ms("T#5x")
    with pytest.raises(LexError):
        tokenize("TOD#12:00")
    with pytest.raises(LexError):
        tokenize("a ? b")


def test_comments_and_pragmas_are_tokens() -> None:
    toks = tokenize("a := 1; // c1\n(* block\n c2 *) {warning 'x'}")
    assert [t.kind for t in toks if t.kind in ("comment", "pragma")] == ["comment", "comment", "pragma"]


# ---------------------------------------------------------------- parser


def test_expression_precedence() -> None:
    e = parse_expression("a OR b AND NOT c = d + 2 * -3")
    assert isinstance(e, A.BinOp) and e.op == "OR"
    right = e.right
    assert isinstance(right, A.BinOp) and right.op == "AND"
    cmp = right.right  # IEC: NOT binds tighter than "=" -> (NOT c) = (d + ...)
    assert isinstance(cmp, A.BinOp) and cmp.op == "="
    assert isinstance(cmp.left, A.UnaryOp) and cmp.left.op == "NOT"
    add = cmp.right
    assert isinstance(add, A.BinOp) and add.op == "+"
    mul = add.right
    assert isinstance(mul, A.BinOp) and isinstance(mul.right, A.Literal) and mul.right.value == -3


def test_postfix_expressions() -> None:
    e = parse_expression("p^.a[1, i].b.3")
    assert isinstance(e, A.BitAccess) and e.bit == 3
    assert isinstance(e.obj, A.Member) and e.obj.name == "b"
    idx = e.obj.obj
    assert isinstance(idx, A.Index) and len(idx.indices) == 2
    call = parse_expression("SUPER^.M(x := 1, 2)")
    assert isinstance(call, A.Call) and isinstance(call.func, A.Member) and isinstance(call.func.obj, A.Super)
    assert [a.name for a in call.args] == ["x", None]
    assert isinstance(parse_expression("Enum#Member"), A.EnumLiteral)
    assert isinstance(parse_expression("[1, 2]"), A.ArrayLiteral)
    with pytest.raises(ParseError):
        parse_expression("a b")


def test_statements_and_comments() -> None:
    src = """
// leading
a := 1; // trailing
IF a > 0 THEN
  b := 2;
ELSIF a < 0 THEN
  b := 3;
ELSE
  // in else
  b := 4;
END_IF

CASE a OF
  0, 1: x := 1;
  2..5: x := 2;
  Kind.A: ;
ELSE
  x := 3;
END_CASE;
FOR i := 1 TO 10 BY 2 DO EXIT; END_FOR
WHILE a DO a := FALSE; END_WHILE
REPEAT a := TRUE; UNTIL a END_REPEAT
a := b := c;
f(x := 1);
RETURN;
// tail
"""
    stmts, tail = parse_body(src)
    assert stmts[0].comments == [" leading"] and stmts[0].trailing == " trailing"
    assert isinstance(stmts[1], A.If) and len(stmts[1].branches) == 2 and stmts[1].else_body
    assert stmts[1].else_body[0].comments == [" in else"]
    case = stmts[2]
    assert isinstance(case, A.Case) and case.blank_before
    assert [len(b.labels) for b in case.branches] == [2, 1, 1] and case.branches[1].labels[0].high is not None
    assert isinstance(stmts[3], A.For) and stmts[3].step is not None
    assert isinstance(stmts[4], A.While) and isinstance(stmts[5], A.Repeat)
    chained = stmts[6]
    assert isinstance(chained, A.Assign) and len(chained.chain) == 1
    assert isinstance(stmts[7], A.ExprStmt) and isinstance(stmts[8], A.Return)
    assert tail == [" tail"]


def test_parse_errors() -> None:
    with pytest.raises(ParseError):
        parse_body("a := ;")
    with pytest.raises(ParseError):
        parse_body("a;")
    with pytest.raises(ParseError):
        parse_body("IF a THEN b := 1;")


# ---------------------------------------------------------------- declarations


def test_interface_declarations() -> None:
    itf = parse_interface(
        """/// doc line
METHOD PROTECTED Foo : STRING(20)
VAR_INPUT
  /// input doc
  {attribute 'hide'}
  a, b : ARRAY[1..3, 0..1] OF INT := [6(1)];
  p : POINTER TO BYTE;
  r : REFERENCE TO Tool;
  s : Struct := (x := 1, y := [1, 2]);
  arr : ARRAY[*] OF BYTE;
END_VAR
VAR_INST
  first : BOOL := TRUE; // trailing
END_VAR
VAR CONSTANT
  C : DINT := 5;
END_VAR
"""
    )
    h = itf.header
    assert (h.kind, h.name, h.access, h.doc) == ("METHOD", "Foo", "PROTECTED", ["doc line"])
    assert isinstance(h.return_type, TString)
    a, b, p, r, _s, arr, first, c = itf.vars
    assert (
        a.name == "a" and b.name == "b" and a.doc == ["input doc"] and a.attributes == ["{attribute 'hide'}"]
    )
    assert isinstance(a.type, TArray) and len(a.type.dims) == 2 and isinstance(a.type.element, TElem)
    assert (
        isinstance(p.type, TPointer) and isinstance(r.type, TReference) and isinstance(r.type.target, TNamed)
    )
    assert isinstance(arr.type, TArray) and arr.type.dims == (None,)
    assert first.section == "inst" and first.trailing == " trailing"
    assert c.constant and c.section == "local"
    ext = parse_interface("FUNCTION_BLOCK X EXTENDS Base IMPLEMENTS I1, I2\nVAR\nEND_VAR\nEND_FUNCTION_BLOCK")
    assert ext.header.extends == ["Base"] and ext.header.implements == ["I1", "I2"]


# ---------------------------------------------------------------- transpile & execute


@pytest.fixture(scope="module")
def env_reg() -> tuple[TypeEnv, dict[str, Target]]:
    return load(DEFAULT_XML, CONFIG)


class Transpiler:
    def __init__(self, env_reg: tuple[TypeEnv, dict[str, Target]]) -> None:
        env, reg = env_reg
        self.env = TypeEnv(env.gen, dict(env.pous))
        self.reg = dict(reg)

    def add(
        self,
        decl: str,
        body: str = "",
        methods: dict[str, str] | None = None,
        props: dict[str, tuple[str, str]] | None = None,
    ) -> Pou:
        itf = parse_interface(decl)
        pou = Pou(itf.header, itf.vars, Body(body), ["Library", "POUs", "Test"])
        for mdecl, mbody in (methods or {}).items():
            m_itf = parse_interface(mdecl)
            pou.methods[m_itf.header.name.upper()] = Method(m_itf.header, m_itf.vars, Body(mbody), pou)
        for pdecl, (get_body, set_body) in (props or {}).items():
            p_itf = parse_interface(pdecl)
            prop = Property(
                p_itf.header,
                [],
                Body(get_body) if get_body else None,
                [],
                Body(set_body) if set_body else None,
                pou,
            )
            pou.properties[p_itf.header.name.upper()] = prop
        self.env.pous[pou.name.upper()] = pou
        self.reg[pou.name.upper()] = Target(f"tests_generated.{pou.name}", pou.name)
        return pou

    def source(self, pou: Pou) -> str:
        return ModuleEmitter(self.env, self.reg, pou, Config()).emit_module()

    def build(self, pou: Pou) -> Any:
        code = self.source(pou)
        ns: dict[str, Any] = {"__name__": f"tests_generated.{pou.name}"}
        exec(compile(code, f"<{pou.name}>", "exec"), ns)
        return ns[pou.name]


@pytest.fixture
def tp(env_reg: tuple[TypeEnv, dict[str, Target]]) -> Transpiler:
    return Transpiler(env_reg)


def fn(tp: Transpiler, decl: str, body: str) -> Any:
    return tp.build(tp.add(decl, body))


def test_integer_wrap_and_division(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : DINT\nVAR_INPUT a : USINT; b : DINT; END_VAR\nVAR u : USINT; d : DINT; END_VAR",
        "u := a + 1; d := b / 2; F := u * 1000 + d;",
    )
    assert f(a=255, b=-7) == -3
    assert f(a=1, b=7) == 2003


def test_non_short_circuit_and(tp: Transpiler) -> None:
    fb = tp.build(
        tp.add(
            "FUNCTION_BLOCK FB1\nVAR_OUTPUT n : DINT; ok : BOOL; END_VAR",
            "n := 0; ok := A() AND B();",
            {
                "METHOD A : BOOL": "n := n + 1; A := FALSE;",
                "METHOD B : BOOL": "n := n + 10; B := TRUE;",
            },
        )
    )
    x = fb()
    x()
    assert x.n == 11 and x.ok is False  # both methods called like in ST


def test_case_ranges_and_else(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : DINT\nVAR_INPUT a : DINT; END_VAR",
        "CASE a OF 0, 1: F := 10; 2..5: F := 20; -1: F := 30; ELSE F := 40; END_CASE",
    )
    assert [f(a=v) for v in (0, 1, 3, 5, -1, 6)] == [10, 10, 20, 20, 30, 40]


def test_case_on_enum(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : DINT\nVAR_INPUT s : CmdMessageState; END_VAR",
        "CASE s OF CmdMessageState.DONE: F := 1; CmdMessageState.ERROR: F := 2; END_CASE",
    )
    from srci.types import CmdMessageState

    assert (f(s=CmdMessageState.DONE), f(s=CmdMessageState.ERROR), f(s=CmdMessageState.ACTIVE)) == (1, 2, 0)


def test_for_loop_variable_after_loop(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : DINT\nVAR_INPUT stop : DINT; END_VAR\nVAR i : DINT; END_VAR",
        "FOR i := 1 TO 5 DO IF i = stop THEN EXIT; END_IF END_FOR F := i;",
    )
    assert f(stop=3) == 3
    assert f(stop=9) == 6  # ST: end value + step after a complete loop
    g = fn(
        tp,
        "FUNCTION G : DINT\nVAR i, s : DINT; END_VAR",
        "FOR i := 10 TO 1 BY -3 DO s := s + i; END_FOR G := s;",
    )
    assert g() == 10 + 7 + 4 + 1


def test_while_repeat_return(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : DINT\nVAR i : DINT; END_VAR",
        "WHILE i < 3 DO i := i + 1; END_WHILE REPEAT i := i + 10; UNTIL i > 30 END_REPEAT F := i; RETURN; F := 0;",
    )
    assert f() == 33


def test_strings_are_truncated(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : STRING(5)\nVAR_INPUT s : STRING(20); END_VAR",
        "F := CONCAT(s, '12345');",
    )
    assert f(s="ab") == "ab123"


def test_struct_assignment_copies_and_input_copy(tp: Transpiler) -> None:
    from srci.types import SWLimits

    f = fn(
        tp,
        "FUNCTION F : SWLimits\nVAR_INPUT v : SWLimits; END_VAR",
        "v.J1LowerLimit := 5.0; F := v;",
    )
    arg = SWLimits()
    result = f(v=arg)
    assert result.J1LowerLimit == 5.0
    assert arg.J1LowerLimit == 0.0  # VAR_INPUT is a copy
    assert result is not arg


def test_inout_struct_is_a_reference(tp: Transpiler) -> None:
    from srci.types import SWLimits

    f = fn(
        tp,
        "FUNCTION F : BOOL\nVAR_IN_OUT v : SWLimits; END_VAR\nVAR tmp : SWLimits; END_VAR",
        "tmp.J2UpperLimit := 7.0; v := tmp; F := TRUE;",
    )
    arg = SWLimits()
    ts = arg.Timestamp
    f(v=arg)
    assert arg.J2UpperLimit == 7.0 and arg.Timestamp is ts


def test_bit_access_and_enum_coercion(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : CmdMessageState\nVAR_INPUT w : WORD; END_VAR\nVAR b : BOOL; END_VAR",
        "b := w.3; w.0 := b; F := w;",
    )
    from srci.types import CmdMessageState

    result = f(w=8)
    assert result == 9 and isinstance(result, CmdMessageState)


def test_ref_alias_for_scalars(tp: Transpiler) -> None:
    fb = tp.build(
        tp.add(
            "FUNCTION_BLOCK FB2\nVAR_OUTPUT step1, step2 : DINT; END_VAR",
            "Inc(first := TRUE); Inc(first := FALSE); Inc(first := FALSE);",
            {
                "METHOD Inc\nVAR_INPUT first : BOOL; END_VAR\nVAR rStep : REFERENCE TO DINT; END_VAR": (
                    "rStep REF= step1; rStep := rStep + 1; step2 := rStep;"
                ),
            },
        )
    )
    x = fb()
    x()
    assert (x.step1, x.step2) == (3, 3)
    src = tp.source(tp.env.pous["FB2"])
    assert "self.step1 = self.step1 + 1" in src


def test_fb_inputs_are_kept_between_calls_and_super(tp: Transpiler) -> None:
    tp.add(
        "FUNCTION_BLOCK BaseFB\nVAR_INPUT x : DINT; END_VAR\nVAR_OUTPUT base_calls : DINT; END_VAR",
        "base_calls := base_calls + 1;",
        {"METHOD Twice : DINT\nVAR_INPUT v : DINT; END_VAR": "Twice := 2 * v;"},
    )
    derived = tp.add(
        "FUNCTION_BLOCK DerivedFB EXTENDS BaseFB\nVAR_OUTPUT y : DINT; END_VAR",
        "SUPER^(); y := x + SUPER^.Twice(v := x);",
        {"METHOD Twice : DINT\nVAR_INPUT v : DINT; END_VAR": "Twice := 0;"},
    )
    # the base class module must exist for the import of the derived one
    base_cls = tp.build(tp.env.pous["BASEFB"])
    import sys
    import types

    module = types.ModuleType("tests_generated.BaseFB")
    module.BaseFB = base_cls  # type: ignore[attr-defined]
    sys.modules["tests_generated.BaseFB"] = module
    try:
        d = tp.build(derived)()
        d(x=4)
        d()
        assert (d.x, d.y, d.base_calls) == (4, 12, 2)
    finally:
        del sys.modules["tests_generated.BaseFB"]


def test_properties(tp: Transpiler) -> None:
    fb = tp.build(
        tp.add(
            "FUNCTION_BLOCK FB3\nVAR _v : DINT; END_VAR",
            "",
            props={"PROPERTY Value : DINT": ("Value := _v * 2;", "_v := Value;")},
        )
    )
    x = fb()
    x.Value = 21
    assert x._v == 21 and x.Value == 42


def test_pointer_to_fb_and_null(tp: Transpiler) -> None:
    fb = tp.build(
        tp.add(
            "FUNCTION_BLOCK FB4\nVAR p : POINTER TO FB4; END_VAR\nVAR_OUTPUT isNull, isSelf : BOOL; END_VAR",
            "isNull := p = 0; p := ADR(THIS^); isSelf := p <> RobotLibraryConstants.NULL_POINTER;",
        )
    )
    x = fb()
    x()
    assert x.isNull and x.isSelf and x.p is x


def test_memory_functions_on_locals(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : UINT\nVAR_INPUT b : ARRAY[0..1] OF BYTE; END_VAR\nVAR v : UINT; END_VAR",
        "SysDepMemCpy(pDest := ADR(v), pSrc := ADR(b), DataLen := SIZEOF(v)); F := v;",
    )
    assert f(b=[0x34, 0x12]) == 0x1234
    g = fn(
        tp,
        "FUNCTION G : UINT\nVAR_INPUT v : UINT; END_VAR",
        "SwapBytes(ADR(v), SIZEOF(v)); G := v;",
    )
    assert g(v=0x1234) == 0x3412


def test_sizeof_and_chained_assignment(tp: Transpiler) -> None:
    f = fn(
        tp,
        "FUNCTION F : UDINT\nVAR a, b : UDINT; s : SWLimits; END_VAR",
        "a := b := SIZEOF(s) + SIZEOF(DINT); F := a + b;",
    )
    from srci.iec.rt import type_size
    from srci.types import SWLimits, iec

    assert f() == 2 * (type_size(iec.StructType(SWLimits)) + 4)


def test_unknown_names_are_errors(tp: Transpiler) -> None:
    with pytest.raises(EmitError):
        tp.source(tp.add("FUNCTION F1 : DINT", "F1 := unknown;"))
    with pytest.raises(EmitError):
        tp.source(tp.add("FUNCTION F2 : DINT", "F2 := 1; FOR i := 1 TO 2 DO END_FOR"))


# ---------------------------------------------------------------- configuration


def test_source_patches(env_reg: tuple[TypeEnv, dict[str, Target]]) -> None:
    env, _ = env_reg
    pous = copy.deepcopy({"MC_ROBOTTASKFB": env.pous["MC_ROBOTTASKFB"]})
    patch = SourcePatch("MC_RobotTaskFB", "OnCall", "does not exist", "x", "test")
    with pytest.raises(PatchError):
        apply_patches(pous, Config(patches=[patch]))
    with pytest.raises(PatchError):
        apply_patches(pous, Config(patches=[replace(patch, pou="Unknown")]))


def test_all_patches_applied(env_reg: tuple[TypeEnv, dict[str, Target]]) -> None:
    env, _ = env_reg
    for patch in CONFIG.patches:
        pou = env.pous[patch.pou.upper()]
        body = pou.body if patch.method is None else pou.methods[patch.method.upper()].body
        marker = (
            patch.new.split("\n", 1)[0].replace("\\1", "").replace("\\2", "") if patch.template else patch.new
        )
        assert marker in body.src and patch.reason


def test_mixin_methods_exist() -> None:
    import importlib

    for pou_name, mixin in CONFIG.mixins.items():
        cls = getattr(importlib.import_module(mixin.module), mixin.name)
        for method in mixin.methods:
            assert hasattr(cls, method), f"{pou_name}.{method}"


# ---------------------------------------------------------------- generated library


def test_generated_files_are_up_to_date() -> None:
    from tools.st2py.__main__ import generate

    files, errors = generate(DEFAULT_XML, CONFIG)
    assert errors == []
    stale = [
        str(p)
        for p, text in files.items()
        if p.name != "__init__.py" and (not p.exists() or p.read_text("utf-8") != text)
    ]
    assert stale == [], "run: python -m tools.st2py"


def all_function_blocks() -> Iterator[tuple[str, str]]:
    from srci.fb._registry import FB_MODULES
    from tools.st2py.registry import HAND_MODULES

    yield from sorted((n, m) for n, m in FB_MODULES.items() if m not in HAND_MODULES)


@pytest.mark.parametrize(("name", "module"), list(all_function_blocks()))
def test_every_function_block_can_be_called(name: str, module: str) -> None:
    """Smoke test: create each FB and call it with a fresh AxesGroup (nothing executed)."""
    import importlib

    from srci.types import AxesGroup

    cls = getattr(importlib.import_module(module), name)
    fb = cls()
    kwargs: dict[str, Any] = {}
    if (
        "AxesGroup"
        in cls.__call__.__code__.co_varnames[
            : cls.__call__.__code__.co_argcount + cls.__call__.__code__.co_kwonlyargcount
        ]
    ):
        kwargs["AxesGroup"] = AxesGroup()
    if name == "MC_RobotTaskFB":
        pytest.skip("covered by tests/sdk/test_robot_task.py")
    fb(**kwargs)
    fb(**kwargs)
