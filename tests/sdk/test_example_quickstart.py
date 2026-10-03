# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_example_quickstart
#  Author:      Thorsten Brach
#  Date:        2026-10-03
#
#  Description:
#    examples/quickstart: the compact example runs against the SDK simulator.
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

"""examples/quickstart: the compact example runs against the SDK simulator."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "examples" / "quickstart" / "quickstart.py"


def test_quickstart_initializes_enables_moves_and_returns(
    sdk_library: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Initialization, GroupReset, EnableRobot, override, joint / linear / direct moves and back
    to the start position."""
    spec = importlib.util.spec_from_file_location("quickstart", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.main(["--sim"]) == 0
    out = capsys.readouterr().out
    for step in (
        "1. J1 +20 deg",
        "2. J2/J3 +20 deg",
        "3. linear Z -50 mm",
        "4. direct Z +50 mm",
        "back at start",
    ):
        assert step in out
    start = out.split("start ")[1].splitlines()[0]
    back = out.split("back at start")[1].splitlines()[0]
    assert start.strip() == back.strip()
    assert out.rstrip().endswith("done")
