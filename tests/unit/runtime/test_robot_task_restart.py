# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.runtime.test_robot_task_restart
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    ST-FIX F152: a RobotTask that meets an RC still initialized from an earlier connection.
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

"""ST-FIX F152: a RobotTask that meets an RC still initialized from an earlier connection."""

from __future__ import annotations

from srci.api.program import RobotProgram
from srci.types import ControlHalfByte, TelegramState

SIZE = 256


def telegram(state: int, count: int) -> bytes:
    data = bytearray(SIZE)
    life = (count % 15 + 1) << 4
    data[0], data[1], data[3], data[SIZE - 1] = 0x25, life, state, life
    data[4:8] = bytes.fromhex("24100000")
    return bytes(data)


def test_rc_still_initialized_gets_a_reset() -> None:
    program = RobotProgram(SIZE, SIZE)
    states = [TelegramState.INITIALIZED] * 5 + [TelegramState.READY_FOR_INITIALIZATION] * 5
    seen = []
    for count, state in enumerate(states):
        program.step(telegram(int(state), count))
        seen.append(program.axes_group.Cyclic.PlcToRob.Control)
    assert ControlHalfByte.RESET in seen
    assert seen[-1] == ControlHalfByte.INITIALIZE
    assert not program.robot_task.Initialized
