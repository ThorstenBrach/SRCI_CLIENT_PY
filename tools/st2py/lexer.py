# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.lexer
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Tokenizer for IEC 61131-3 Structured Text (Codesys dialect, statement part).
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

"""Tokenizer for IEC 61131-3 Structured Text (Codesys dialect, statement part).

Comments and pragmas are kept as tokens so that the generated Python code keeps the
comments of the ST source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

KEYWORDS = {
    "IF",
    "THEN",
    "ELSIF",
    "ELSE",
    "END_IF",
    "CASE",
    "OF",
    "END_CASE",
    "FOR",
    "TO",
    "BY",
    "DO",
    "END_FOR",
    "WHILE",
    "END_WHILE",
    "REPEAT",
    "UNTIL",
    "END_REPEAT",
    "EXIT",
    "CONTINUE",
    "RETURN",
    "AND",
    "OR",
    "XOR",
    "NOT",
    "MOD",
    "AND_THEN",
    "OR_ELSE",
    "TRUE",
    "FALSE",
    "SUPER",
    "THIS",
}


class LexError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Token:
    kind: str  # ident, kw, int, real, time, typed, string, op, comment, pragma, nl
    text: str
    line: int
    value: object = None


_TOKEN = re.compile(
    r"""
    (?P<nl>\r?\n)
  | (?P<ws>[ \t\f]+)
  | (?P<lcomment>//[^\n]*)
  | (?P<bcomment>\(\*.*?\*\))
  | (?P<pragma>\{[^}]*\})
  | (?P<time>(?:T|TIME|LTIME|TOD|TIME_OF_DAY|D|DATE|DT|DATE_AND_TIME)\#[-0-9a-zA-Z_.:]+)
  | (?P<based>(?:2|8|16)\#[0-9A-Fa-f_]+)
  | (?P<typed>[A-Za-z_][A-Za-z0-9_]*\#)
  | (?P<real>\d[\d_]*\.\d[\d_]*(?:[eE][-+]?\d+)?|\d[\d_]*[eE][-+]?\d+)
  | (?P<int>\d[\d_]*)
  | (?P<string>'(?:\$.|[^'$])*')
  | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<op>:=|REF=|=>|<>|<=|>=|\.\.|\*\*|[-+*/()\[\],;:.^=<>&])
    """,
    re.VERBOSE | re.DOTALL,
)

_TIME_UNITS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1_000, "ms": 1}


def time_to_ms(text: str) -> int:
    """``T#1m30s`` -> 90000."""
    body = text.split("#", 1)[1].replace("_", "").lower()
    sign = -1 if body.startswith("-") else 1
    body = body.lstrip("-")
    if not re.fullmatch(r"(?:\d+(?:\.\d+)?(?:ms|d|h|m|s))+", body):
        raise LexError(f"invalid TIME literal {text!r}")
    total = 0.0
    for num, unit in re.findall(r"(\d+(?:\.\d+)?)(ms|d|h|m|s)", body):
        total += float(num) * _TIME_UNITS[unit]
    return sign * round(total)


_ESCAPES = {"$": "$", "'": "'", "L": "\n", "N": "\n", "P": "\f", "R": "\r", "T": "\t"}


def unescape_string(text: str) -> str:
    body = text[1:-1]
    out: list[str] = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "$" and i + 1 < len(body):
            nxt = body[i + 1]
            if nxt.upper() in _ESCAPES:
                out.append(_ESCAPES[nxt.upper()])
                i += 2
                continue
            if i + 2 < len(body) and re.fullmatch(r"[0-9A-Fa-f]{2}", body[i + 1 : i + 3]):
                out.append(chr(int(body[i + 1 : i + 3], 16)))
                i += 3
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def tokenize(src: str, first_line: int = 1) -> list[Token]:
    tokens: list[Token] = []
    pos = 0
    line = first_line
    while pos < len(src):
        m = _TOKEN.match(src, pos)
        if m is None:
            raise LexError(f"line {line}: cannot tokenize {src[pos : pos + 30]!r}")
        pos = m.end()
        kind = m.lastgroup
        text = m.group()
        assert kind is not None
        if kind == "ws":
            continue
        if kind == "nl":
            tokens.append(Token("nl", text, line))
            line += 1
            continue
        if kind == "lcomment":
            tokens.append(Token("comment", text[2:].rstrip(), line))
            continue
        if kind == "bcomment":
            tokens.append(Token("comment", text, line))
            line += text.count("\n")
            continue
        if kind == "pragma":
            tokens.append(Token("pragma", text, line))
            line += text.count("\n")
            continue
        if kind == "time":
            prefix = text.split("#", 1)[0].upper()
            if prefix in ("T", "TIME", "LTIME"):
                tokens.append(Token("time", text, line, time_to_ms(text)))
                continue
            if prefix in ("D", "DATE"):
                import datetime as _dt

                y, mo, d = (int(x) for x in text.split("#", 1)[1].split("-"))
                secs = int((_dt.date(y, mo, d) - _dt.date(1970, 1, 1)).total_seconds())
                tokens.append(Token("date", text, line, secs))
                continue
            raise LexError(f"line {line}: unsupported literal {text!r}")
        if kind == "based":
            base, digits = text.split("#")
            tokens.append(Token("int", text, line, int(digits.replace("_", ""), int(base))))
            continue
        if kind == "int":
            tokens.append(Token("int", text, line, int(text.replace("_", ""))))
            continue
        if kind == "real":
            tokens.append(Token("real", text, line, float(text.replace("_", ""))))
            continue
        if kind == "string":
            tokens.append(Token("string", text, line, unescape_string(text)))
            continue
        if kind == "typed":
            tokens.append(Token("typed", text[:-1], line))
            continue
        if kind == "ident":
            up = text.upper()
            if up in KEYWORDS:
                tokens.append(Token("kw", up, line))
            elif up == "REF" and src.startswith("=", pos):
                pos += 1
                tokens.append(Token("op", "REF=", line))
            else:
                tokens.append(Token("ident", text, line))
            continue
        tokens.append(Token("op", text, line))
    return tokens
