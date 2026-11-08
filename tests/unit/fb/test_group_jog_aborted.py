# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.fb.test_group_jog_aborted
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    ST-FIX F154: GroupJog sets CommandAborted when the RC reports the infos 16#6C14 /
#    16#6C15.
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

"""ST-FIX F154: GroupJog sets CommandAborted when the RC reports the infos 16#6C14 / 16#6C15."""

from __future__ import annotations

import pytest

from srci.fb import MC_GroupJogFB
from srci.types import CmdMessageState


@pytest.mark.parametrize("info", [0x6C14, 0x6C15])
def test_interrupted_with_abort_info_sets_command_aborted(info: int) -> None:
    fb = MC_GroupJogFB()
    fb._response.AlarmMessageCode = info
    fb.OnUpdateStateFlags(State=CmdMessageState.INTERRUPTED)
    assert fb.CommandAborted


def test_interrupted_without_abort_info_keeps_command_aborted_false() -> None:
    fb = MC_GroupJogFB()
    fb._response.AlarmMessageCode = 0x6F01
    fb.OnUpdateStateFlags(State=CmdMessageState.INTERRUPTED)
    assert not fb.CommandAborted
