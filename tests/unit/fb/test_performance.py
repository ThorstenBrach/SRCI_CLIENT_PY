# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.fb.test_performance
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Time budget: telegram coding must be far below a 10 ms cycle (measured ~40 us).
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

"""Time budget: telegram coding must be far below a 10 ms cycle (measured ~40 us)."""

from __future__ import annotations

import struct
import time

from tests.helpers import Host, new_axes_group
from tests.unit.fb.test_robot_task_telegram import fill_header, rc_header, rc_telegram


def test_telegram_coding_budget() -> None:
    host, (ag, _) = Host(), new_axes_group()
    fill_header(host)
    host.Telegram.PlcToRob.Header.TelegramLengthPlcToRob = 256
    host._parCfg.Com.TelegramLengthPlcToRob = 256
    ag.CyclicOptional.RobToPlc.CartesianPosition.Active = True
    ag.CyclicOptional.RobToPlc.JointPosition.Active = True
    out = bytearray(256)
    data = rc_telegram(rc_header() + bytes(40) + bytes(30) + struct.pack(">HH", 0, 0), 256)
    n = 300
    start = time.perf_counter()
    for _ in range(n):
        host.CreateSendPayload(ag, out)
        host.ParseRecvPayload(ag, data)
    mean = (time.perf_counter() - start) / n
    assert mean < 1e-3, f"{mean * 1e6:.0f} us per cycle"
