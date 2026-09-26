"""Recursive descent parser for ST statements (bodies of POUs, methods, properties)."""

from __future__ import annotations

from dataclasses import dataclass

from . import ast as A
from .lexer import Token, tokenize


class ParseError(ValueError):
    pass


@dataclass
class _Sig:
    """Significant token with the comments in front of it."""

    tok: Token
    comments: list[tuple[str, int]]  # (text, line)
    blank_before: bool


def _significant(tokens: list[Token]) -> tuple[list[_Sig], list[tuple[str, int]], bool]:
    sig: list[_Sig] = []
    pending: list[tuple[str, int]] = []
    newlines = 0
    blank = False
    for t in tokens:
        if t.kind == "nl":
            newlines += 1
            if newlines >= 2:
                blank = True
            continue
        if t.kind in ("comment", "pragma"):
            pending.append((t.text, t.line))
            newlines = 0 if t.kind == "comment" and not t.text.startswith("(*") else newlines
            continue
        sig.append(_Sig(t, pending, blank))
        pending = []
        newlines = 0
        blank = False
    return sig, pending, blank


BINARY_PRECEDENCE: list[set[str]] = [
    {"OR", "OR_ELSE"},
    {"XOR"},
    {"AND", "AND_THEN", "&"},
    {"=", "<>"},
    {"<", ">", "<=", ">="},
    {"+", "-"},
    {"*", "/", "MOD"},
]


class Parser:
    def __init__(self, src: str, first_line: int = 1) -> None:
        self.sig, self.tail_comments, self.tail_blank = _significant(tokenize(src, first_line))
        self.pos = 0
        self.consumed: set[int] = set()  # indices of _Sig whose comments were used

    # ------------------------------------------------------------------ helpers

    def peek(self, offset: int = 0) -> Token | None:
        i = self.pos + offset
        return self.sig[i].tok if i < len(self.sig) else None

    def at(self, kind: str, text: str | None = None, offset: int = 0) -> bool:
        t = self.peek(offset)
        if t is None or t.kind != kind:
            return False
        return text is None or t.text == text

    def at_kw(self, *names: str) -> bool:
        t = self.peek()
        return t is not None and t.kind == "kw" and t.text in names

    def at_op(self, *ops: str) -> bool:
        t = self.peek()
        return t is not None and t.kind == "op" and t.text in ops

    def next(self) -> Token:
        if self.pos >= len(self.sig):
            raise ParseError("unexpected end of source")
        t = self.sig[self.pos].tok
        self.pos += 1
        return t

    def expect_kw(self, name: str) -> Token:
        t = self.next()
        if t.kind != "kw" or t.text != name:
            raise ParseError(f"line {t.line}: expected {name}, got {t.text!r}")
        return t

    def expect_op(self, op: str) -> Token:
        t = self.next()
        if t.kind != "op" or t.text != op:
            raise ParseError(f"line {t.line}: expected {op!r}, got {t.text!r}")
        return t

    def skip_semis(self) -> None:
        while self.at_op(";"):
            self.pos += 1

    def _leading(self, idx: int) -> tuple[list[str], bool]:
        """Comments in front of significant token ``idx`` (not trailing the previous one)."""
        if idx >= len(self.sig) or idx in self.consumed:
            return [], idx < len(self.sig) and self.sig[idx].blank_before
        s = self.sig[idx]
        prev_line = self.sig[idx - 1].tok.line if idx > 0 else -1
        out = [text for text, line in s.comments if line != prev_line]
        self.consumed.add(idx)
        return out, s.blank_before

    def _trailing(self, end_idx: int) -> str | None:
        """Comment on the same line after the token ``end_idx`` (stored at ``end_idx + 1``)."""
        line = self.sig[end_idx].tok.line
        nxt = end_idx + 1
        items = self.sig[nxt].comments if nxt < len(self.sig) else self.tail_comments
        same = [text for text, ln in items if ln == line]
        return " ".join(same) if same else None

    def _inner(self, start: int, end: int) -> list[str]:
        """Comments between the tokens start+1..end (inside a simple statement)."""
        out: list[str] = []
        for i in range(start + 1, end + 1):
            if i in self.consumed:
                continue
            prev_line = self.sig[i - 1].tok.line
            out.extend(text for text, line in self.sig[i].comments if line != prev_line or i > start + 1)
            self.consumed.add(i)
        return out

    # ------------------------------------------------------------------ statements

    def parse_body(self) -> tuple[list[A.Stmt], list[str]]:
        stmts = self.parse_stmts(set())
        if self.pos < len(self.sig):
            t = self.peek()
            assert t is not None
            raise ParseError(f"line {t.line}: unexpected {t.text!r}")
        tail = [text for text, _ in self.tail_comments]
        if self.sig:
            last_line = self.sig[-1].tok.line
            tail = [text for text, line in self.tail_comments if line != last_line]
        return stmts, tail

    def parse_stmts(self, terminators: set[str], case_labels: bool = False) -> list[A.Stmt]:
        stmts: list[A.Stmt] = []
        while self.pos < len(self.sig):
            t = self.peek()
            assert t is not None
            if t.kind == "kw" and t.text in terminators:
                break
            if case_labels and self._at_case_label():
                break
            stmts.append(self.parse_stmt())
        return stmts

    def _at_case_label(self) -> bool:
        depth = 0
        i = self.pos
        while i < len(self.sig):
            t = self.sig[i].tok
            if t.kind == "op":
                if t.text in ("(", "["):
                    depth += 1
                elif t.text in (")", "]"):
                    depth -= 1
                elif depth == 0 and t.text in (";", ":=", "REF="):
                    return False
                elif depth == 0 and t.text == ":":
                    return True
            elif t.kind == "kw" and t.text not in ("TRUE", "FALSE"):
                return False
            i += 1
        return False

    def parse_stmt(self) -> A.Stmt:
        start = self.pos
        comments, blank = self._leading(start)
        t = self.peek()
        assert t is not None
        line = t.line
        stmt: A.Stmt
        simple = True
        if t.kind == "op" and t.text == ";":
            self.pos += 1
            stmt = A.Empty(line=line)
        elif t.kind == "kw" and t.text == "IF":
            stmt = self.parse_if()
            simple = False
        elif t.kind == "kw" and t.text == "CASE":
            stmt = self.parse_case()
            simple = False
        elif t.kind == "kw" and t.text == "FOR":
            stmt = self.parse_for()
            simple = False
        elif t.kind == "kw" and t.text == "WHILE":
            stmt = self.parse_while()
            simple = False
        elif t.kind == "kw" and t.text == "REPEAT":
            stmt = self.parse_repeat()
            simple = False
        elif t.kind == "kw" and t.text in ("EXIT", "CONTINUE", "RETURN"):
            self.pos += 1
            stmt = {"EXIT": A.Exit, "CONTINUE": A.Continue, "RETURN": A.Return}[t.text](line=line)
            self._end_simple()
        else:
            target = self.parse_expr()
            if self.at_op(":=", "REF="):
                ref = self.next().text == "REF="
                value = self.parse_expr()
                chain: list[A.Expr] = []
                while self.at_op(":="):  # a := b := c
                    self.next()
                    chain.append(value)
                    value = self.parse_expr()
                stmt = A.Assign(target, value, ref, chain, line=line)
            elif isinstance(target, A.Call):
                stmt = A.ExprStmt(target, line=line)
            else:
                raise ParseError(f"line {line}: expression statement without call: {t.text!r}")
            self._end_simple()
        end = self.pos - 1
        if simple:
            comments = comments + self._inner(start, end)
        stmt.comments = comments + stmt.comments
        stmt.blank_before = blank
        stmt.trailing = self._trailing(end)
        if stmt.trailing is not None and end + 1 < len(self.sig):
            # do not repeat the trailing comment in front of the next statement
            nxt = self.sig[end + 1]
            nxt.comments = [(text, ln) for text, ln in nxt.comments if ln != self.sig[end].tok.line]
        return stmt

    def _opt_semi(self) -> None:
        if self.at_op(";"):
            self.pos += 1

    def _end_simple(self) -> None:
        if self.at_op(";"):
            self.pos += 1
        else:
            t = self.peek()
            if (
                t is not None
                and not (t.kind == "kw" and t.text.startswith("END_"))
                and not (t.kind == "kw" and t.text in ("ELSE", "ELSIF", "UNTIL"))
            ):
                raise ParseError(f"line {t.line}: expected ';', got {t.text!r}")

    def _cond_comments(self, start: int) -> list[str]:
        return self._inner(start, self.pos - 1)

    def parse_if(self) -> A.If:
        line = self.expect_kw("IF").line
        start = self.pos - 1
        branches: list[tuple[A.Expr, list[A.Stmt]]] = []
        cond = self.parse_expr()
        self.expect_kw("THEN")
        extra = self._cond_comments(start)
        body = self.parse_stmts({"ELSIF", "ELSE", "END_IF"})
        branches.append((cond, body))
        else_body: list[A.Stmt] | None = None
        else_comments: list[str] = []
        while self.at_kw("ELSIF"):
            s = self.pos
            self.next()
            cond = self.parse_expr()
            self.expect_kw("THEN")
            extra += self._cond_comments(s)
            branches.append((cond, self.parse_stmts({"ELSIF", "ELSE", "END_IF"})))
        if self.at_kw("ELSE"):
            else_comments, _ = self._leading(self.pos)
            self.next()
            else_body = self.parse_stmts({"END_IF"})
        end_comments, _ = self._leading(self.pos)
        self.expect_kw("END_IF")
        self._opt_semi()
        node = A.If(branches, else_body, else_comments, line=line)
        node.comments = extra
        self._append_block_tail(else_body if else_body is not None else branches[-1][1], end_comments)
        return node

    @staticmethod
    def _append_block_tail(body: list[A.Stmt], comments: list[str]) -> None:
        if comments:
            body.append(A.Empty(comments=comments))

    def parse_case(self) -> A.Case:
        line = self.expect_kw("CASE").line
        start = self.pos - 1
        selector = self.parse_expr()
        self.expect_kw("OF")
        extra = self._cond_comments(start)
        branches: list[A.CaseBranch] = []
        else_body: list[A.Stmt] | None = None
        else_comments: list[str] = []
        while not self.at_kw("END_CASE", "ELSE"):
            comments, blank = self._leading(self.pos)
            labels: list[A.CaseLabel] = []
            while True:
                low = self.parse_expr()
                high = None
                if self.at_op(".."):
                    self.next()
                    high = self.parse_expr()
                labels.append(A.CaseLabel(low, high))
                if self.at_op(","):
                    self.next()
                    continue
                break
            self.expect_op(":")
            body = self.parse_stmts({"END_CASE", "ELSE"}, case_labels=True)
            branches.append(A.CaseBranch(labels, body, comments, blank))
        if self.at_kw("ELSE"):
            else_comments, _ = self._leading(self.pos)
            self.next()
            else_body = self.parse_stmts({"END_CASE"})
        end_comments, _ = self._leading(self.pos)
        self.expect_kw("END_CASE")
        self._opt_semi()
        node = A.Case(selector, branches, else_body, else_comments, line=line)
        node.comments = extra
        if else_body is not None:
            self._append_block_tail(else_body, end_comments)
        elif branches:
            self._append_block_tail(branches[-1].body, end_comments)
        return node

    def parse_for(self) -> A.For:
        line = self.expect_kw("FOR").line
        start = self.pos - 1
        var = self.next()
        if var.kind != "ident":
            raise ParseError(f"line {line}: FOR needs a variable")
        self.expect_op(":=")
        first = self.parse_expr()
        self.expect_kw("TO")
        last = self.parse_expr()
        step = None
        if self.at_kw("BY"):
            self.next()
            step = self.parse_expr()
        self.expect_kw("DO")
        extra = self._cond_comments(start)
        body = self.parse_stmts({"END_FOR"})
        end_comments, _ = self._leading(self.pos)
        self.expect_kw("END_FOR")
        self._opt_semi()
        self._append_block_tail(body, end_comments)
        node = A.For(var.text, first, last, step, body, line=line)
        node.comments = extra
        return node

    def parse_while(self) -> A.While:
        line = self.expect_kw("WHILE").line
        start = self.pos - 1
        cond = self.parse_expr()
        self.expect_kw("DO")
        extra = self._cond_comments(start)
        body = self.parse_stmts({"END_WHILE"})
        end_comments, _ = self._leading(self.pos)
        self.expect_kw("END_WHILE")
        self._opt_semi()
        self._append_block_tail(body, end_comments)
        node = A.While(cond, body, line=line)
        node.comments = extra
        return node

    def parse_repeat(self) -> A.Repeat:
        line = self.expect_kw("REPEAT").line
        body = self.parse_stmts({"UNTIL"})
        self.expect_kw("UNTIL")
        cond = self.parse_expr()
        self.expect_kw("END_REPEAT")
        self._opt_semi()
        return A.Repeat(body, cond, line=line)

    # ------------------------------------------------------------------ expressions

    def parse_expr(self, level: int = 0) -> A.Expr:
        if level == len(BINARY_PRECEDENCE):
            return self.parse_power()
        left = self.parse_expr(level + 1)
        ops = BINARY_PRECEDENCE[level]
        while True:
            t = self.peek()
            if t is None:
                break
            text = t.text
            if not ((t.kind == "kw" or t.kind == "op") and text in ops):
                break
            self.next()
            right = self.parse_expr(level + 1)
            left = A.BinOp(text, left, right, line=t.line)
        return left

    def parse_power(self) -> A.Expr:
        left = self.parse_unary()
        while self.at_op("**"):
            t = self.next()
            right = self.parse_unary()
            left = A.BinOp("**", left, right, line=t.line)
        return left

    def parse_unary(self) -> A.Expr:
        t = self.peek()
        if t is not None and (
            (t.kind == "op" and t.text in ("-", "+")) or (t.kind == "kw" and t.text == "NOT")
        ):
            self.next()
            operand = self.parse_unary()
            if t.text == "-" and isinstance(operand, A.Literal) and operand.kind in ("int", "real"):
                assert isinstance(operand.value, int | float)
                return A.Literal(
                    operand.kind, -operand.value, "-" + operand.raw, operand.type_prefix, line=t.line
                )
            return A.UnaryOp(t.text, operand, line=t.line)
        return self.parse_postfix()

    def parse_postfix(self) -> A.Expr:
        expr = self.parse_primary()
        while True:
            if self.at_op("."):
                t = self.next()
                nxt = self.next()
                if nxt.kind == "ident" or nxt.kind == "kw":
                    expr = A.Member(expr, nxt.text, line=t.line)
                elif nxt.kind == "int":
                    assert isinstance(nxt.value, int)
                    expr = A.BitAccess(expr, nxt.value, line=t.line)
                else:
                    raise ParseError(f"line {t.line}: unexpected {nxt.text!r} after '.'")
            elif self.at_op("["):
                t = self.next()
                indices = [self.parse_expr()]
                while self.at_op(","):
                    self.next()
                    indices.append(self.parse_expr())
                self.expect_op("]")
                expr = A.Index(expr, indices, line=t.line)
            elif self.at_op("^"):
                t = self.next()
                expr = A.Deref(expr, line=t.line)
            elif self.at_op("("):
                t = self.next()
                expr = A.Call(expr, self.parse_args(), line=t.line)
            else:
                return expr

    def parse_args(self) -> list[A.Arg]:
        args: list[A.Arg] = []
        if self.at_op(")"):
            self.next()
            return args
        while True:
            if self.at("ident") and (self.at("op", ":=", 1) or self.at("op", "=>", 1)):
                name = self.next().text
                output = self.next().text == "=>"
                args.append(A.Arg(name, self.parse_expr(), output))
            else:
                args.append(A.Arg(None, self.parse_expr()))
            if self.at_op(","):
                self.next()
                continue
            self.expect_op(")")
            return args

    def parse_primary(self) -> A.Expr:
        t = self.next()
        if t.kind == "int":
            return A.Literal("int", t.value, t.text, line=t.line)
        if t.kind == "real":
            return A.Literal("real", t.value, t.text, line=t.line)
        if t.kind in ("time", "date"):
            return A.Literal(t.kind, t.value, t.text, line=t.line)
        if t.kind == "string":
            return A.Literal("string", t.value, t.text, line=t.line)
        if t.kind == "kw" and t.text in ("TRUE", "FALSE"):
            return A.Literal("bool", t.text == "TRUE", t.text, line=t.line)
        if t.kind == "kw" and t.text in ("THIS", "SUPER"):
            self.expect_op("^")
            return A.This(line=t.line) if t.text == "THIS" else A.Super(line=t.line)
        if t.kind == "typed":
            nxt = self.next()
            if nxt.kind in ("int", "real"):
                return A.Literal(nxt.kind, nxt.value, nxt.text, t.text.upper(), line=t.line)
            if nxt.kind == "kw" and nxt.text in ("TRUE", "FALSE"):
                return A.Literal("bool", nxt.text == "TRUE", nxt.text, t.text.upper(), line=t.line)
            if nxt.kind == "op" and nxt.text == "-":
                num = self.next()
                assert isinstance(num.value, int | float)
                return A.Literal(num.kind, -num.value, "-" + num.text, t.text.upper(), line=t.line)
            if nxt.kind == "ident":
                return A.EnumLiteral(t.text, nxt.text, line=t.line)
            raise ParseError(f"line {t.line}: unsupported typed literal {t.text}#{nxt.text}")
        if t.kind == "ident":
            return A.Name(t.text, line=t.line)
        if t.kind == "op" and t.text == "(":
            expr = self.parse_expr()
            self.expect_op(")")
            return expr
        if t.kind == "op" and t.text == "[":
            items = [self.parse_expr()]
            while self.at_op(","):
                self.next()
                items.append(self.parse_expr())
            self.expect_op("]")
            return A.ArrayLiteral(items, line=t.line)
        raise ParseError(f"line {t.line}: unexpected {t.text!r}")


def parse_body(src: str, first_line: int = 1) -> tuple[list[A.Stmt], list[str]]:
    """Parse a statement list; returns the statements and trailing comments."""
    return Parser(src, first_line).parse_body()


def parse_expression(src: str) -> A.Expr:
    p = Parser(src)
    e = p.parse_expr()
    if p.pos != len(p.sig):
        raise ParseError(f"trailing tokens in expression {src!r}")
    return e
