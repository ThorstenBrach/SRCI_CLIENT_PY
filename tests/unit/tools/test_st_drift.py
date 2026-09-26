from pathlib import Path

from tools.st_drift import find_markers, main, st_hash, st_units

ST = """FUNCTION_BLOCK X
END_FUNCTION_BLOCK
METHOD PRIVATE Foo : DINT
  Foo := 1;
END_METHOD
PROPERTY PROTECTED Bar : BOOL
GET
END_GET
END_PROPERTY
"""


def test_units_and_hash_ignore_line_endings(tmp_path: Path) -> None:
    assert set(st_units(ST)) == {"Foo", "Bar"}
    a, b = tmp_path / "a.st", tmp_path / "b.st"
    a.write_bytes(ST.encode())
    b.write_bytes(ST.replace("\n", "\r\n").encode())
    assert st_hash(a) == st_hash(b)
    assert st_hash(a, "Foo") == st_hash(b, "Foo") != st_hash(a, "Bar")


def test_report_and_update(tmp_path: Path) -> None:
    lib, src = tmp_path / "lib", tmp_path / "src" / "srci"
    lib.mkdir()
    src.mkdir(parents=True)
    (lib / "X.st").write_text(ST)
    py = src / "x.py"
    py.write_text(
        "# ST-Source: X.st#Foo  sha256: 0000000000000000\n# ST-Source: X.st  sha256: 0000000000000000\n"
    )
    assert len(find_markers(src)) == 2
    assert main([str(lib), "--src", str(src)]) == 1
    assert main([str(lib), "--src", str(src), "--update"]) == 0
    assert main([str(lib), "--src", str(src)]) == 0
    text = py.read_text()
    assert st_hash(lib / "X.st", "Foo") in text.splitlines()[0]
    assert st_hash(lib / "X.st") in text.splitlines()[1]
    (lib / "X.st").write_text(ST.replace("Foo := 1", "Foo := 2"))
    assert main([str(lib), "--src", str(src)]) == 1


def test_missing_unit_is_reported(tmp_path: Path) -> None:
    lib, src = tmp_path / "lib", tmp_path / "src" / "srci"
    lib.mkdir()
    src.mkdir(parents=True)
    (lib / "X.st").write_text(ST)
    (src / "x.py").write_text("# ST-Source: X.st#Nope  sha256: 0000000000000000\n")
    assert main([str(lib), "--src", str(src)]) == 1
