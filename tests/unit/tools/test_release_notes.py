# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_release_notes
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    tools.release_notes: release body from CHANGELOG.md, tag = package version.
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

"""tools.release_notes: release body from CHANGELOG.md, tag = package version."""

from __future__ import annotations

import pytest

from tools.release_notes import main, package_version, section

LOG = """# Change Log

## [Unreleased]
 - next

## [0.2.0] - 2026-10-01
### Added
 - feature

## [0.1.0] - 2026-09-26
 - first
"""


def test_section_of_a_version() -> None:
    assert section(LOG, "0.2.0") == "### Added\n - feature"
    assert section(LOG, "0.1.0") == "- first"
    assert section(LOG, "9.9.9") is None


def test_tag_must_match_the_package_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["v999.0.0"]) == 1
    assert "does not match" in capsys.readouterr().err


def test_package_version_is_the_one_of_srci() -> None:
    import srci

    assert package_version() == srci.__version__
