# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.api.test_api
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    srci.api: RobotProgram and SrciClient without a robot (loopback transport).
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

"""srci.api: RobotProgram and SrciClient without a robot (loopback transport)."""

from __future__ import annotations

import pytest

from srci.api import CommandError, RobotProgram, SrciClient, WaitTimeoutError
from srci.fb import MC_GroupResetFB, MC_ReadRobotDataFB
from srci.iec.clock import FakeClock
from srci.runtime import Runner
from srci.transport import LoopbackTransport


def silent_robot(size: int = 128) -> LoopbackTransport:
    """A robot controller that never answers anything but zeros."""
    return LoopbackTransport(lambda telegram: bytes(size), size, size)


def test_fb_package_exports_all_function_blocks() -> None:
    import srci.fb
    from srci.fb._registry import FB_MODULES

    assert srci.fb.MC_GroupResetFB is MC_GroupResetFB
    assert set(FB_MODULES) <= set(dir(srci.fb))
    with pytest.raises(AttributeError):
        getattr(srci.fb, "MC_DoesNotExistFB")  # noqa: B009


def test_program_builds_a_telegram_of_the_configured_length() -> None:
    program = RobotProgram(send_size=128, recv_size=128)
    assert program.config.Com.TelegramLengthPlcToRob == 128
    out = program.step(bytes(128))
    assert len(out) == 128
    assert not program.initialized and not program.commands_enabled


def test_program_add_calls_blocks_and_checks_inputs() -> None:
    program = RobotProgram(send_size=128, recv_size=128)
    block = program.add(MC_GroupResetFB(), Execute=False)
    assert program.blocks == [block]
    with pytest.raises(AttributeError):
        program.add(MC_GroupResetFB(), NoSuchInput=True)
    program.step(bytes(128))
    program.remove(block)
    assert program.blocks == []


def test_program_runs_with_the_runner() -> None:
    clock = FakeClock()
    runner = Runner(silent_robot(), RobotProgram(128, 128), 0.01, clock=clock)
    runner.run(cycles=5)
    assert runner.cycle == 5


def test_client_wait_times_out_without_robot() -> None:
    client = SrciClient(silent_robot(), clock=FakeClock())
    with pytest.raises(WaitTimeoutError):
        client.wait_initialized(timeout=0.2)
    assert client.cycle == 20


def test_client_execute_reports_a_failed_command() -> None:
    """Without an initialized RobotTask the block ends with ERR_COMMANDS_NOT_ENABLED."""
    client = SrciClient(silent_robot(), clock=FakeClock())
    with pytest.raises(CommandError) as exc:
        client.execute(MC_GroupResetFB(), timeout=1.0)
    assert exc.value.error_id != 0
    assert "MC_GroupResetFB" in str(exc.value)
    block = client.execute(MC_GroupResetFB(), timeout=1.0, check=False)
    assert not block.Execute and not block.Done
    # ReadRobotData is part of the initialization (no error), but without an answer: timeout
    with pytest.raises(WaitTimeoutError):
        client.execute(MC_ReadRobotDataFB(), timeout=0.1)
