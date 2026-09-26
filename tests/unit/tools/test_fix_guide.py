# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_fix_guide
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    docs/ST_Finding_Solve_Guide.md: instructions to fix the findings in the PLC library
#    (ST).
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

"""docs/ST_Finding_Solve_Guide.md: instructions to fix the findings in the PLC library (ST)."""

from __future__ import annotations

import re
from pathlib import Path

from tools.st2py import fix_guide

ROOT = Path(__file__).resolve().parents[3]
HAND_WRITTEN = (
    "src/srci/fb/General/MC_RobotTask/MC_RobotTaskFB_Telegram.py",
    "src/srci/fb/_internal/Send/RobotLibrarySendDataBaseFB.py",
    "src/srci/fb/_internal/Recv/RobotLibraryRecvDataBaseFB.py",
    "src/srci/functions/Convert/Misc.py",
)


def test_guide_is_up_to_date() -> None:
    """Regenerate with ``python -m tools.st2py.fix_guide``."""
    assert fix_guide.GUIDE.read_text(encoding="utf-8") == fix_guide.build()


def test_hand_written_fixes_are_described() -> None:
    """Every ST-FIX of hand written Python has an ST description in fix_guide_manual.md."""
    manual = fix_guide.MANUAL.read_text(encoding="utf-8")
    described = {int(m) for m in re.findall(r"^### F(\d+)", manual, flags=re.M)}
    used = {
        int(m)
        for path in HAND_WRITTEN
        for m in re.findall(r"ST-FIX F(\d+)", (ROOT / path).read_text(encoding="utf-8"))
    }
    assert used <= described


def test_every_step_changes_the_st_text() -> None:
    guide = fix_guide.collect()
    assert guide.steps
    assert all(any(line.startswith("+") for line in step.diff) for step in guide.steps)
