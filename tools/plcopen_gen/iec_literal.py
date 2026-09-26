# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.plcopen_gen.iec_literal
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Translate IEC 61131-3 literals and constant expressions to Python source code.
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

"""Translate IEC 61131-3 literals and constant expressions to Python source code.

Only the subset used by the SRCI PLC library is supported: integer literals in all
bases, REAL literals, TRUE/FALSE, TIME literals, typed literals (``USINT#5``),
strings, qualified names (``Enum.MEMBER``, ``Group.CONST``) and the operators
``+ - * / MOD`` with parentheses.
"""

from __future__ import annotations

import re
from collections.abc import Callable

_TIME_UNITS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1_000, "ms": 1}

_TOKEN = re.compile(
    r"""
    (?P<ws>\s+)
  | (?P<time>(?:T|TIME|LTIME)\#[-0-9a-zA-Z_.]+)
  | (?P<based>(?:2|8|16)\#[0-9A-Fa-f_]+)
  | (?P<typed>[A-Za-z_][A-Za-z0-9_]*\#)
  | (?P<real>\d[\d_]*\.\d[\d_]*(?:[eE][-+]?\d+)?|\d[\d_]*[eE][-+]?\d+)
  | (?P<int>\d[\d_]*)
  | (?P<string>'(?:\$.|[^'$])*')
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)
  | (?P<op>[-+*/()])
    """,
    re.VERBOSE,
)


class LiteralError(ValueError):
    pass


def time_to_ms(text: str) -> int:
    """``T#1m30s`` -> 90000."""
    body = text.split("#", 1)[1].replace("_", "").lower()
    sign = -1 if body.startswith("-") else 1
    body = body.lstrip("-")
    total = 0.0
    for num, unit in re.findall(r"(\d+(?:\.\d+)?)(ms|d|h|m|s)", body):
        total += float(num) * _TIME_UNITS[unit]
    if not re.fullmatch(r"(?:\d+(?:\.\d+)?(?:ms|d|h|m|s))+", body):
        raise LiteralError(f"invalid TIME literal {text!r}")
    return sign * round(total)


def _string(text: str) -> str:
    body = text[1:-1]
    out: list[str] = []
    i = 0
    escapes = {"$": "$", "'": "'", "L": "\n", "N": "\n", "P": "\f", "R": "\r", "T": "\t"}
    while i < len(body):
        ch = body[i]
        if ch == "$" and i + 1 < len(body):
            nxt = body[i + 1]
            if nxt.upper() in escapes:
                out.append(escapes[nxt.upper()])
                i += 2
                continue
            if i + 2 < len(body) and re.fullmatch(r"[0-9A-Fa-f]{2}", body[i + 1 : i + 3]):
                out.append(chr(int(body[i + 1 : i + 3], 16)))
                i += 3
                continue
        out.append(ch)
        i += 1
    return repr("".join(out))


def to_python(expr: str, resolve_name: Callable[[str], str]) -> str:
    """Translate an IEC expression to Python source.

    ``resolve_name`` maps an IEC (possibly qualified) name to Python source code and
    raises :class:`LiteralError` for unknown names.
    """
    pos = 0
    parts: list[str] = []
    text = expr.strip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if m is None:
            raise LiteralError(f"cannot parse {expr!r} at {pos}")
        pos = m.end()
        kind = m.lastgroup
        tok = m.group()
        if kind == "ws" or kind == "typed":
            continue  # typed literal prefix (USINT#5) carries no value information
        if kind == "time":
            parts.append(str(time_to_ms(tok)))
        elif kind == "based":
            base, digits = tok.split("#")
            parts.append(str(int(digits.replace("_", ""), int(base))))
        elif kind == "real":
            parts.append(repr(float(tok.replace("_", ""))))
        elif kind == "int":
            parts.append(str(int(tok.replace("_", ""))))
        elif kind == "string":
            parts.append(_string(tok))
        elif kind == "name":
            upper = tok.upper()
            if upper == "TRUE":
                parts.append("True")
            elif upper == "FALSE":
                parts.append("False")
            elif upper == "MOD":
                parts.append("%")
            else:
                parts.append(resolve_name(tok))
        elif kind == "op":
            parts.append(tok)
    if not parts:
        raise LiteralError(f"empty expression {expr!r}")
    return " ".join(parts)
