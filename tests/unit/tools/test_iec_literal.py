import pytest

from tools.plcopen_gen.iec_literal import LiteralError, time_to_ms, to_python


def ident(name: str) -> str:
    return f"<{name}>"


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("0", "0"),
        ("1_000", "1000"),
        ("16#A1", "161"),
        ("16#8401", str(0x8401)),
        ("2#0101", "5"),
        ("8#17", "15"),
        ("-5", "- 5"),
        ("1.5", "1.5"),
        ("1.0E3", "1000.0"),
        ("TRUE", "True"),
        ("false", "False"),
        ("USINT#5", "5"),
        ("T#1s", "1000"),
        ("TIME#1m30s", "90000"),
        ("T#100ms", "100"),
        ("'abc'", "'abc'"),
        ("'it$'s'", '"it\'s"'),
        ("'a$Nb'", repr("a\nb")),
        ("'$41'", "'A'"),
        ("(Group.MAX - 1)", "( <Group.MAX> - 1 )"),
        ("Enum.MEMBER", "<Enum.MEMBER>"),
        ("7 MOD 3", "7 % 3"),
    ],
)
def test_to_python(expr: str, expected: str) -> None:
    assert to_python(expr, ident) == expected


def test_time_units() -> None:
    assert time_to_ms("T#1d2h3m4s5ms") == 86_400_000 + 2 * 3_600_000 + 3 * 60_000 + 4_000 + 5
    assert time_to_ms("T#-2s") == -2000
    assert time_to_ms("T#1.5s") == 1500


@pytest.mark.parametrize("expr", ["", "T#abc", "1 ? 2"])
def test_invalid(expr: str) -> None:
    with pytest.raises(LiteralError):
        to_python(expr, ident)
