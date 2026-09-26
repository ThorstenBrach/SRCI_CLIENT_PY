"""Time budget: telegram coding must be far below a 10 ms cycle (measured ~40 us)."""

from __future__ import annotations

import struct
import time

from tests.unit.fb.test_robot_task_telegram import Host, fill_header, new_axes_group, rc_header, rc_telegram


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
