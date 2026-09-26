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
from tools.plcopen_gen.overrides import OVERRIDES, ConstOverride, OverrideError, apply_overrides
from tools.plcopen_gen.parser import parse_library


@pytest.fixture(scope="module")
def lib_xml():  # parsed once, copied per test
    return parse_library(Path(DEFAULT_XML))


def test_srci_version_is_1_5() -> None:
    # PLC library still exports 1.3.0 (forgotten update), SDK implements 1.5
    assert RobotLibraryConstants.SRCIVersion == VersionStruct(MajorVersion=1, MinorVersion=5, PatchVersion=0)


def test_overrides_apply_and_are_documented(lib_xml) -> None:
    lib = copy.deepcopy(lib_xml)
    apply_overrides(lib)
    consts = {c.name: c for g in lib.const_groups for c in g.constants}
    for ov in OVERRIDES:
        assert consts[ov.name].init == ov.init
        assert "Override" in consts[ov.name].doc


def test_obsolete_override_fails(lib_xml) -> None:
    lib = copy.deepcopy(lib_xml)
    apply_overrides(lib)  # now the "XML" already contains the values
    with pytest.raises(OverrideError, match="obsolete"):
        apply_overrides(lib)


def test_unknown_target_fails(lib_xml) -> None:
    bad = (ConstOverride("RobotLibraryConstants", "DOES_NOT_EXIST", OVERRIDES[0].init, "x"),)
    with pytest.raises(OverrideError, match="not found"):
        apply_overrides(copy.deepcopy(lib_xml), bad)
