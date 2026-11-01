# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_group
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the client side of GroupStop, GroupInterrupt, GroupContinue
#    and GroupReset.
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

"""Validation of the client side of GroupStop, GroupInterrupt, GroupContinue and GroupReset.

* a block on an axes group that no RobotTask serves ends with an error, nothing is sent
* GroupStop and GroupInterrupt count up the stop counter (high half byte of the cyclic
  FastStop/LifeSign byte); GroupReset does not touch it
"""

from __future__ import annotations

import pytest

from srci.types import AxesGroup, RobotLibraryErrorIdEnum
from srci.types.iec import new_instance
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import execute, fb, state

GROUP_BLOCKS = ["MC_GroupStopFB", "MC_GroupInterruptFB", "MC_GroupContinueFB", "MC_GroupResetFB"]


@pytest.mark.parametrize("name", GROUP_BLOCKS)
def test_unlinked_axes_group_rejected(name: str) -> None:
    """A group command on an axes group that is not served by a RobotTask ends with ERR_COMMANDS_NOT_ENABLED and is not left Busy."""
    group = AxesGroup()
    block = new_instance(name)
    block.Execute = True
    for _ in range(5):
        block(AxesGroup=group)
    assert block.Error and block.ErrorID == RobotLibraryErrorIdEnum.ERR_COMMANDS_NOT_ENABLED, state(block)
    assert not block.Busy and not block.Done
    assert group.Cyclic.PlcToRob.FastStop == 0


def _header_counter(h: RobotTaskHarness) -> int:
    """Stop counter as sent in the telegram (high half byte of the FastStop/LifeSign byte)."""
    return (h.rt.Telegram.PlcToRob.Header.FastStop_LifeSign >> 4) & 0x0F


@pytest.mark.parametrize("name", ["MC_GroupStopFB", "MC_GroupInterruptFB"])
def test_stop_counter_counts_every_execute(robot: RobotTaskHarness, name: str) -> None:
    """Every executed GroupStop / GroupInterrupt increases the stop counter in the telegram by one; it wraps after 15.

    GroupContinue and GroupReset leave the counter unchanged."""
    start = robot.ag.Cyclic.PlcToRob.FastStop
    for n in range(1, 18):
        execute(robot, fb(robot, name))
        assert robot.ag.Cyclic.PlcToRob.FastStop & 0x0F == (start + n) & 0x0F
        assert _header_counter(robot) == (start + n) & 0x0F
    before = _header_counter(robot)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    execute(robot, fb(robot, "MC_GroupResetFB"))
    assert _header_counter(robot) == before
