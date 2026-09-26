"""Parser for ST declarations (``InterfaceAsPlainText`` of POUs, methods, properties)."""

from __future__ import annotations

from dataclasses import dataclass, field

from . import ast as A
from .parser import ParseError, Parser

# ---------------------------------------------------------------------- types


@dataclass(frozen=True, eq=False)
class TElem:
    name: str  # upper case elementary name


@dataclass(frozen=True, eq=False)
class TString:
    length: A.Expr | None  # None -> 80


@dataclass(frozen=True, eq=False)
class TArray:
    dims: tuple[tuple[A.Expr, A.Expr] | None, ...]  # None: ARRAY[*] (variable length)
    element: TypeDecl


@dataclass(frozen=True, eq=False)
class TPointer:
    target: TypeDecl


@dataclass(frozen=True, eq=False)
class TReference:
    target: TypeDecl


@dataclass(frozen=True, eq=False)
class TNamed:
    name: str  # struct / enum / alias / FB / interface


TypeDecl = TElem | TString | TArray | TPointer | TReference | TNamed

ELEMENTARY = {
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
}


# ---------------------------------------------------------------------- initial values


@dataclass(eq=False)
class StructInit:
    members: list[tuple[str, Init]]


@dataclass(eq=False)
class ArrayInit:
    items: list[tuple[A.Expr | None, Init]]  # (repetition count, value)


Init = A.Expr | StructInit | ArrayInit


# ---------------------------------------------------------------------- declarations

SECTIONS = {
    "VAR_INPUT": "input",
    "VAR_OUTPUT": "output",
    "VAR_IN_OUT": "inout",
    "VAR": "local",
    "VAR_INST": "inst",
    "VAR_TEMP": "temp",
    "VAR_STAT": "stat",
    "VAR_GLOBAL": "global",
}


@dataclass(eq=False)
class VarDecl:
    name: str
    type: TypeDecl
    section: str  # input, output, inout, local, inst, temp, stat, global
    init: Init | None = None
    constant: bool = False
    doc: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    trailing: str | None = None


@dataclass(eq=False)
class Header:
    kind: str  # FUNCTION_BLOCK, FUNCTION, METHOD, PROPERTY, INTERFACE
    name: str
    access: str | None = None  # PUBLIC, PRIVATE, PROTECTED, INTERNAL
    return_type: TypeDecl | None = None
    extends: list[str] = field(default_factory=list)
    implements: list[str] = field(default_factory=list)
    doc: list[str] = field(default_factory=list)
    attributes: list[str] = field(default_factory=list)
    final: bool = False
    abstract: bool = False


@dataclass(eq=False)
class Interface:
    header: Header
    vars: list[VarDecl]


_ACCESS = {"PUBLIC", "PRIVATE", "PROTECTED", "INTERNAL"}


class DeclParser(Parser):
    """Uses the statement/expression parser for types and initial values."""

    def _doc_and_attrs(self, idx: int) -> tuple[list[str], list[str]]:
        if idx >= len(self.sig):
            return [], []
        s = self.sig[idx]
        prev_line = self.sig[idx - 1].tok.line if idx > 0 else -1
        doc: list[str] = []
        attrs: list[str] = []
        for text, line in s.comments:
            if line == prev_line:
                continue
            if text.startswith("{"):
                attrs.append(text)
            elif text.startswith("/"):  # '///' doc comment ('//' already stripped)
                doc.append(text[1:].strip())
        self.consumed.add(idx)
        return doc, attrs

    def ident(self) -> str:
        t = self.next()
        if t.kind not in ("ident", "kw"):
            raise ParseError(f"line {t.line}: identifier expected, got {t.text!r}")
        return t.text

    def at_word(self, *words: str) -> bool:
        t = self.peek()
        return t is not None and t.kind in ("ident", "kw") and t.text.upper() in words

    def parse_type(self) -> TypeDecl:
        t = self.next()
        word = t.text.upper()
        if word == "ARRAY":
            self.expect_op("[")
            dims: list[tuple[A.Expr, A.Expr] | None] = []
            while True:
                if self.at_op("*"):
                    self.next()
                    dims.append(None)
                else:
                    low = self.parse_expr()
                    self.expect_op("..")
                    high = self.parse_expr()
                    dims.append((low, high))
                if self.at_op(","):
                    self.next()
                    continue
                break
            self.expect_op("]")
            if self.ident().upper() != "OF":
                raise ParseError(f"line {t.line}: OF expected")
            return TArray(tuple(dims), self.parse_type())
        if word in ("POINTER", "REFERENCE"):
            if self.ident().upper() != "TO":
                raise ParseError(f"line {t.line}: TO expected")
            target = self.parse_type()
            return TPointer(target) if word == "POINTER" else TReference(target)
        if word in ("STRING", "WSTRING"):
            length: A.Expr | None = None
            if self.at_op("("):
                self.next()
                length = self.parse_expr()
                self.expect_op(")")
            elif self.at_op("["):
                self.next()
                length = self.parse_expr()
                self.expect_op("]")
            return TString(length)
        if word in ELEMENTARY:
            return TElem({"TIME_OF_DAY": "TOD", "DATE_AND_TIME": "DT"}.get(word, word))
        name = t.text
        while self.at_op("."):  # qualified (namespace) names
            self.next()
            name += "." + self.ident()
        return TNamed(name)

    def parse_init(self) -> Init:
        if self.at_op("(") and self.at("ident", None, 1) and self.at("op", ":=", 2):
            self.next()
            members: list[tuple[str, Init]] = []
            while True:
                name = self.ident()
                self.expect_op(":=")
                members.append((name, self.parse_init()))
                if self.at_op(","):
                    self.next()
                    continue
                break
            self.expect_op(")")
            return StructInit(members)
        if self.at_op("["):
            self.next()
            items: list[tuple[A.Expr | None, Init]] = []
            while True:
                value: Init
                if self.at("int") and self.at("op", "(", 1):
                    count = self.parse_primary()
                    self.expect_op("(")
                    value = self.parse_init()
                    self.expect_op(")")
                    items.append((count, value))
                else:
                    items.append((None, self.parse_init()))
                if self.at_op(","):
                    self.next()
                    continue
                break
            self.expect_op("]")
            return ArrayInit(items)
        return self.parse_expr()

    def parse_header(self) -> Header:
        doc, attrs = self._doc_and_attrs(self.pos)
        kind = self.ident().upper()
        if kind not in ("FUNCTION_BLOCK", "FUNCTION", "METHOD", "PROPERTY", "INTERFACE", "PROGRAM"):
            raise ParseError(f"unsupported POU kind {kind}")
        h = Header(kind, "", doc=doc, attributes=attrs)
        while self.at_word(*_ACCESS, "FINAL", "ABSTRACT"):
            w = self.ident().upper()
            if w in _ACCESS:
                h.access = w
            elif w == "FINAL":
                h.final = True
            else:
                h.abstract = True
        h.name = self.ident()
        while True:
            if self.at_op(":"):
                self.next()
                h.return_type = self.parse_type()
            elif self.at_word("EXTENDS"):
                self.next()
                h.extends.append(self.ident())
                while self.at_op(","):
                    self.next()
                    h.extends.append(self.ident())
            elif self.at_word("IMPLEMENTS"):
                self.next()
                h.implements.append(self.ident())
                while self.at_op(","):
                    self.next()
                    h.implements.append(self.ident())
            else:
                break
        self.skip_semis()
        return h

    def parse_var_sections(self) -> list[VarDecl]:
        out: list[VarDecl] = []
        while self.pos < len(self.sig):
            if not self.at_word(*SECTIONS):
                break
            section = SECTIONS[self.ident().upper()]
            constant = False
            while self.at_word("CONSTANT", "RETAIN", "PERSISTENT"):
                if self.ident().upper() == "CONSTANT":
                    constant = True
            while not self.at_word("END_VAR"):
                doc, attrs = self._doc_and_attrs(self.pos)
                names = [self.ident()]
                while self.at_op(","):
                    self.next()
                    names.append(self.ident())
                self.expect_op(":")
                type_ = self.parse_type()
                init: Init | None = None
                if self.at_op(":="):
                    self.next()
                    init = self.parse_init()
                end = self.pos
                self.expect_op(";")
                trailing = self._trailing(end)
                for n in names:
                    out.append(VarDecl(n, type_, section, init, constant, list(doc), list(attrs), trailing))
            self.ident()  # END_VAR
            self.skip_semis()
        return out


def parse_interface(src: str) -> Interface:
    p = DeclParser(src)
    header = p.parse_header()
    vars_ = p.parse_var_sections()
    if header.kind == "PROPERTY":
        return Interface(header, vars_)
    if p.pos < len(p.sig):
        t = p.peek()
        assert t is not None
        # END_FUNCTION_BLOCK etc. may follow in some exports
        if not (t.kind in ("ident", "kw") and t.text.upper().startswith("END_")):
            raise ParseError(f"line {t.line}: unexpected {t.text!r} in declaration")
    return Interface(header, vars_)


def parse_accessor_vars(src: str) -> list[VarDecl]:
    """Declarations of a property accessor (``VAR ... END_VAR`` only)."""
    p = DeclParser(src)
    vars_ = p.parse_var_sections()
    return vars_
