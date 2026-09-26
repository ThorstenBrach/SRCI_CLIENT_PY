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

import time

import pytest

from srci.api import CommandError, RobotProgram, SrciClient, WaitTimeoutError
from srci.errors import SrciError
from srci.fb import MC_GroupResetFB, MC_ReadActualPositionCyclicFB, MC_ReadRobotDataFB
from srci.iec.clock import FakeClock
from srci.runtime import Runner
from srci.runtime.runner import CycleContext
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


# ---------------------------------------------------------------------------- background cycle


class FailingProgram(RobotProgram):
    """A program that raises in its 5th cycle (e.g. an error in a user block)."""

    def cycle(self, ctx: CycleContext) -> None:
        if ctx.cycle == 4:
            raise RuntimeError("broken block")
        super().cycle(ctx)


def test_client_runs_the_cycle_in_a_background_thread() -> None:
    """Like a PLC task: the cycle keeps running while the script sleeps; it starts with the
    first helper call (after the configuration) and stops with close()."""
    transport = silent_robot()
    with SrciClient(transport, cycle_time=0.005) as client:
        assert client.background
        time.sleep(0.05)
        assert client.cycle == 0 and not client.runner.running  # not started yet
        client.run(2)
        assert client.runner.running
        before = client.cycle
        time.sleep(0.1)  # plain sleep: the RobotTask LifeSign keeps running
        assert client.cycle >= before + 5
        assert client.run_until(lambda: client.cycle >= before + 30, timeout=2.0) >= 1
    assert not client.runner.running
    with pytest.raises(SrciError):
        client.run()


def test_client_background_execute_error_and_timeout() -> None:
    """execute() waits for the result of the cycle thread, resets Execute and removes the block;
    after a timeout Execute is reset as well and the message says the command may still run."""
    with SrciClient(silent_robot(), cycle_time=0.005) as client:
        with pytest.raises(CommandError) as exc:
            client.execute(MC_GroupResetFB(), timeout=1.0)
        assert exc.value.error_id != 0
        assert not exc.value.block.Execute and client.program.blocks == []
        block = client.start(MC_ReadRobotDataFB())
        assert client.program.blocks == [block] and block.Execute
        with pytest.raises(WaitTimeoutError, match="may still run on the RC"):
            client.wait_done(block, timeout=0.1)
        assert not block.Execute and client.program.blocks == []


def test_client_background_set_add_enable_disable() -> None:
    with SrciClient(silent_robot(), cycle_time=0.005) as client:
        cyclic = client.enable(MC_ReadActualPositionCyclicFB(), timeout=1.0, check=False)
        assert cyclic.Enable and cyclic in client.program.blocks
        client.set(cyclic, Enable=True)
        client.disable(cyclic, timeout=1.0)
        assert not cyclic.Enable and client.program.blocks == []
        reset = client.add(MC_GroupResetFB(), Execute=False)
        assert client.program.blocks == [reset]
        client.remove(reset)
        assert client.program.blocks == []
        client.idle(0.02)


def test_client_background_reports_an_exception_of_the_cycle() -> None:
    client = SrciClient(silent_robot(), FailingProgram(128, 128), cycle_time=0.005)
    with pytest.raises(RuntimeError, match="broken block"):
        client.run_until(lambda: False, timeout=2.0)
    client.close()


def test_client_without_background_removes_finished_blocks() -> None:
    """background=False: cycles only while the script waits (deterministic, e.g. FakeClock)."""
    client = SrciClient(silent_robot(), clock=FakeClock())
    assert not client.background
    client.execute(MC_GroupResetFB(), timeout=0.1, check=False)
    assert client.program.blocks == [] and client.cycle >= 2
    block = client.start(MC_ReadRobotDataFB())
    with pytest.raises(WaitTimeoutError, match="may still run on the RC"):
        client.wait_done(block, timeout=0.05)
    assert not block.Execute and client.program.blocks == []
    cycles = client.cycle
    client.idle(0.05)
    assert client.cycle == cycles + 5
    client.close()
