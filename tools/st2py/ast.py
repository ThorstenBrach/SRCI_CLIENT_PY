# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.ast
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    AST of ST statements and expressions.
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

"""AST of ST statements and expressions."""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------- expressions


@dataclass(eq=False)
class Expr:
    line: int = field(default=0, kw_only=True)


@dataclass(eq=False)
class Name(Expr):
    id: str


@dataclass(eq=False)
class This(Expr):
    """``THIS^``"""


@dataclass(eq=False)
class Super(Expr):
    """``SUPER^``"""


@dataclass(eq=False)
class Member(Expr):
    obj: Expr
    name: str


@dataclass(eq=False)
class BitAccess(Expr):
    obj: Expr
    bit: int


@dataclass(eq=False)
class Index(Expr):
    obj: Expr
    indices: list[Expr]


@dataclass(eq=False)
class Deref(Expr):
    obj: Expr


@dataclass(eq=False)
class Arg:
    name: str | None
    value: Expr
    output: bool = False  # ``=>``


@dataclass(eq=False)
class Call(Expr):
    func: Expr
    args: list[Arg]


@dataclass(eq=False)
class BinOp(Expr):
    op: str  # + - * / MOD ** = <> < > <= >= AND OR XOR AND_THEN OR_ELSE &
    left: Expr
    right: Expr


@dataclass(eq=False)
class UnaryOp(Expr):
    op: str  # - NOT +
    operand: Expr


@dataclass(eq=False)
class Literal(Expr):
    kind: str  # int, real, bool, string, time
    value: object
    raw: str = ""
    type_prefix: str | None = None  # USINT#5 -> USINT


@dataclass(eq=False)
class EnumLiteral(Expr):
    """``TypeName#Member``"""

    type_name: str
    member: str


@dataclass(eq=False)
class ArrayLiteral(Expr):
    items: list[Expr]


# ---------------------------------------------------------------------- statements


@dataclass(eq=False)
class Stmt:
    line: int = field(default=0, kw_only=True)
    comments: list[str] = field(default_factory=list, kw_only=True)  # comment lines before
    blank_before: bool = field(default=False, kw_only=True)
    trailing: str | None = field(default=None, kw_only=True)  # comment on the same line


@dataclass(eq=False)
class Assign(Stmt):
    target: Expr
    value: Expr
    ref: bool = False  # REF=
    chain: list[Expr] = field(default_factory=list)  # further targets: target := chain[0] := value


@dataclass(eq=False)
class ExprStmt(Stmt):
    expr: Expr


@dataclass(eq=False)
class If(Stmt):
    branches: list[tuple[Expr, list[Stmt]]]
    else_body: list[Stmt] | None = None
    else_comments: list[str] = field(default_factory=list)


@dataclass(eq=False)
class CaseLabel:
    low: Expr
    high: Expr | None = None  # range low..high


@dataclass(eq=False)
class CaseBranch:
    labels: list[CaseLabel]
    body: list[Stmt]
    comments: list[str] = field(default_factory=list)
    blank_before: bool = False


@dataclass(eq=False)
class Case(Stmt):
    selector: Expr
    branches: list[CaseBranch]
    else_body: list[Stmt] | None = None
    else_comments: list[str] = field(default_factory=list)


@dataclass(eq=False)
class For(Stmt):
    var: str
    start: Expr
    end: Expr
    step: Expr | None
    body: list[Stmt]


@dataclass(eq=False)
class While(Stmt):
    cond: Expr
    body: list[Stmt]


@dataclass(eq=False)
class Repeat(Stmt):
    body: list[Stmt]
    until: Expr


@dataclass(eq=False)
class Exit(Stmt):
    pass


@dataclass(eq=False)
class Continue(Stmt):
    pass


@dataclass(eq=False)
class Return(Stmt):
    pass


@dataclass(eq=False)
class Empty(Stmt):
    """Only comments (at the end of a block) or a lone ``;``."""
