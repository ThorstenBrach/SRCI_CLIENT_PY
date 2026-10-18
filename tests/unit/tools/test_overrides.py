# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_overrides
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#
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

import copy
from pathlib import Path

import pytest

from srci.types import RobotLibraryConstants, VersionStruct
from tools.plcopen_gen.__main__ import DEFAULT_XML
from tools.plcopen_gen.model import StructValue
from tools.plcopen_gen.overrides import OVERRIDES, ConstOverride, OverrideError, apply_overrides
from tools.plcopen_gen.parser import parse_library


@pytest.fixture(scope="module")
def lib_xml():  # parsed once, copied per test
    return parse_library(Path(DEFAULT_XML))


def test_srci_version_is_1_5() -> None:
    # the PLC library exported 1.3.0 until 2026-10 (was an override), SDK implements 1.5
    assert RobotLibraryConstants.SRCIVersion == VersionStruct(MajorVersion=1, MinorVersion=5, PatchVersion=0)


def test_overrides_apply_and_are_documented(lib_xml) -> None:
    lib = copy.deepcopy(lib_xml)
    apply_overrides(lib)
    consts = {c.name: c for g in lib.const_groups for c in g.constants}
    for ov in OVERRIDES:
        assert consts[ov.name].init == ov.init
        assert "Override" in consts[ov.name].doc


# an override with the value the XML already has (SRCIVersion 1.5.0 since the export of 2026-10-17)
def _srci_version() -> StructValue:
    for g in parse_library(Path(DEFAULT_XML)).const_groups:
        for c in g.constants:
            if c.name == "SRCIVersion":
                assert isinstance(c.init, StructValue)
                return c.init
    raise AssertionError("SRCIVersion not found")


_SAME = ConstOverride("RobotLibraryConstants", "SRCIVersion", _srci_version(), "x")


def test_obsolete_override_fails(lib_xml) -> None:
    with pytest.raises(OverrideError, match="obsolete"):
        apply_overrides(copy.deepcopy(lib_xml), (_SAME,))


def test_unknown_target_fails(lib_xml) -> None:
    bad = (ConstOverride("RobotLibraryConstants", "DOES_NOT_EXIST", _SAME.init, "x"),)
    with pytest.raises(OverrideError, match="not found"):
        apply_overrides(copy.deepcopy(lib_xml), bad)
