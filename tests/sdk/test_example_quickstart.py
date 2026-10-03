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

import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "examples" / "quickstart" / "quickstart.py"


def test_quickstart_initializes_enables_moves_and_returns(sdk_library: str) -> None:
    """Initialization with the listed ParCfg, GroupReset, EnableRobot, override, joint move into the
    elbow-bent pose, rectangle with 4 linear moves, back to the start position, disable (the script
    runs from top to bottom, so it is started as a process)."""
    env = {**os.environ, "SRCI_SDK_SIM_LIB": sdk_library}
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sim"],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
        check=False,
    )
    out = result.stdout
    assert result.returncode == 0, result.stderr + out
    for step in (
        "robot enabled: True",
        "1. elbow-bent pose",
        "2. linear to",
        "5. linear to",
        "7. back at start",
        "robot enabled: False",
    ):
        assert step in out
    assert "rectangle skipped" not in out
    start = out.split("start:")[1].splitlines()[0]
    back = out.split("back at start:")[1].splitlines()[0]
    assert start.split("=")[1].strip() == back.split("=")[1].strip()
    assert out.rstrip().endswith("done")
