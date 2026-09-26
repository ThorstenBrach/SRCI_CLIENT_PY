# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_file_header
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    tools.file_header: the file header of all Python files (like the ST sources).
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

"""tools.file_header: the file header of all Python files (like the ST sources)."""

from __future__ import annotations

from tools.file_header import ROOT, add_header, files, has_header, module_name, render, st_fields

ST_DECL = """FUNCTION_BLOCK X
// -------------------------------------------------------------------------
//  Object:      X
//  Author:      Thorsten Brach
//  Date:        2024-06-01
// -------------------------------------------------------------------------
"""


def test_render_like_the_st_header() -> None:
    text = render("srci.api.client", "2024-06-01", "Run a program.")
    assert text.startswith("# ----") and text.endswith("-\n")
    for part in ("Object:      srci.api.client", "Author:      Thorsten Brach", "Date:        2024-06-01",
                 "Run a program.", "(C) 2024 Thorsten Brach. All rights reserved",
                 "Licensed under the MIT License.", "Disclaimer:"):  # fmt: skip
        assert part in text
    assert has_header(text)


def test_author_and_date_from_the_st_source() -> None:
    assert st_fields(ST_DECL) == ("Thorsten Brach", "2024-06-01")
    assert st_fields("FUNCTION_BLOCK Y")[0] == "Thorsten Brach"


def test_add_header_keeps_the_content() -> None:
    import tools.file_header as fh

    f = ROOT / "src" / "srci" / "_tmp_header_test.py"
    try:
        f.write_text('"""Doc line."""\n\nX = 1\n', encoding="utf-8")
        assert add_header(f)
        text = f.read_text(encoding="utf-8")
        assert has_header(text) and text.endswith('"""Doc line."""\n\nX = 1\n')
        assert "Object:      srci._tmp_header_test" in text and "#    Doc line." in text
        assert not add_header(f)  # only once
    finally:
        f.unlink(missing_ok=True)
    assert fh.module_name(ROOT / "tools" / "st2py" / "__init__.py") == "tools.st2py"


def test_every_python_file_has_the_header() -> None:
    missing = [str(p.relative_to(ROOT)) for p in files() if not has_header(p.read_text(encoding="utf-8"))]
    assert missing == []
    assert module_name(ROOT / "src" / "srci" / "api" / "client.py") == "srci.api.client"
