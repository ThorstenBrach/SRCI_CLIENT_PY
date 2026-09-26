# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_export_xml
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    tools.st2py.export_xml: the corrections of the Python port written back into the PLCopen
#    XML.
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

"""tools.st2py.export_xml: the corrections of the Python port written back into the PLCopen XML."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest

from tools.st2py.export_xml import DEFAULT_XML, ExportResult, export, verify


@pytest.fixture(scope="module")
def fixed(tmp_path_factory: pytest.TempPathFactory) -> tuple[ExportResult, Path]:
    result = export()
    path = tmp_path_factory.mktemp("export") / "RobotLibrary_fixed.xml"
    path.write_bytes(result.xml.encode("utf-8"))
    return result, path


def test_fixed_xml_contains_every_correction(fixed: tuple[ExportResult, Path]) -> None:
    """Without any correction the generators produce from the fixed XML the same types and
    function blocks as from the original XML with all corrections."""
    assert verify(fixed[1]) == []


def test_fixed_xml_keeps_format_and_object_ids(fixed: tuple[ExportResult, Path]) -> None:
    result, path = fixed
    raw, orig = path.read_bytes(), DEFAULT_XML.read_bytes()
    assert raw[:3] == orig[:3] == b"\xef\xbb\xbf"
    assert raw.count(b"\r\n") == raw.count(b"\n")  # CRLF like the export
    text, before = raw.decode("utf-8-sig"), orig.decode("utf-8-sig")
    ids = Counter(a or b for a, b in re.findall(r'ObjectId="([^"]+)"|<ObjectId>([^<]+)</ObjectId>', text))
    assert set(ids.values()) == {2}  # every object once as object and once in the ProjectStructure
    old = set(re.findall(r'ObjectId="([^"]+)"', before))
    assert old <= set(re.findall(r'ObjectId="([^"]+)"', text))  # no object ID is lost
    # every object without a correction stays byte-identical
    touched = {c.split(".")[0] for c in result.changed}
    unchanged = [
        m.group(0)
        for m in re.finditer(r'<pou name="([^"]+)" .*?</pou>', before, re.S)
        if m.group(1) not in touched
    ]
    assert len(unchanged) > 100
    assert all(block in text for block in unchanged)
    assert "MC_MeasuringInputFB" in result.changed  # F12
    assert "type CmdType" in result.changed  # F35


def test_fixed_xml_declares_added_variables_twice(fixed: tuple[ExportResult, Path]) -> None:
    """Added variables are in the plain text and in the structured interface."""
    text = fixed[1].read_bytes().decode("utf-8-sig")
    pou = re.search(r'<pou name="MC_GroupStopFB" .*?</pou>', text, re.S)
    assert pou is not None
    itf = pou.group(0)[: pou.group(0).find("</interface>")]
    assert '<variable name="Active">' in itf
    assert re.search(r"VAR_OUTPUT\s+Active : BOOL;", pou.group(0))
