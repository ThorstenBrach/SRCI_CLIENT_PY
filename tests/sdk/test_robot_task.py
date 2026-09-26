"""MC_RobotTaskFB (transpiled from the PLC library) against the SRCI SDK.

The SDK has 20 tools/frames/loads, so the library parameters are set accordingly
(``srci.configure``). Known problems of the PLC library are marked ``xfail`` with the
finding number of docs/ST_FINDINGS.md.
"""

from __future__ import annotations

import time
from collections.abc import Iterator

import pytest

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.sim.gateway import PlcGatewaySimulator
from srci.sim.sdk import SdkSimulator, sdk_transport
from srci.transport import TcpTransport
from srci.types import RobotLibraryConstants, RobotLibraryErrorIdEnum, SyncMode, TelegramState, VersionStruct
from tests.robot_task_harness import SIZE, RobotTaskHarness

RI_STATE_INITIALIZED, RI_STATE_SYNCHRONIZED = 71, 72
DATA_SETS = ("SWLimits", "DefaultDynamics", "ReferenceDynamics")
CANCEL_TIMEOUT_CYCLES = 520  # T#5S cancel/clear timeout of the enable FBs + margin (10 ms cycles)


@pytest.fixture(autouse=True)
def sdk_parameters() -> Iterator[None]:
    """The SDK has 20 tools/frames/loads (index 0..19)."""
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@pytest.fixture
def clock() -> Iterator[FakeClock]:
    fake = FakeClock()
    with use_clock(fake):
        yield fake


def harness(sdk: SdkSimulator, clock: FakeClock, **kw: object) -> RobotTaskHarness:
    return RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance, **kw)  # type: ignore[arg-type]


def synchronized(h: RobotTaskHarness) -> bool:
    return bool(h.rt.Synchronized)


# ---------------------------------------------------------------- start-up


def test_initialized_without_synchronization(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    n = h.run(100, until=lambda: bool(h.rt.Initialized))
    assert n < 30
    h.run(50)
    assert h.rt.Initialized and not h.rt.Error, h.history
    # spec 5.6.7.1: without any data set enabled for synchronization the RI state stays "Initialized"
    assert not h.rt.Synchronized
    assert h.ag.Cyclic.RobToPlc.TelegramState == TelegramState.INITIALIZED
    assert sdk.states.ri_state == RI_STATE_INITIALIZED
    data = h.ag.State.RobotData
    assert data.RCManufacturer == "SRCI_PY SimRobot"
    assert data.RCSupportedFunctions.ReadToolData and data.RCSupportedFunctions.WriteRobotSWLimits


def test_synchronized_client_to_server(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.sync(SyncMode.CLIENT_TO_SERVER, *DATA_SETS)
    n = h.run(300, until=lambda: synchronized(h))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    assert n < 100
    h.run(3)  # the RC takes the RI state from the next telegram
    assert sdk.states.ri_state == RI_STATE_SYNCHRONIZED
    rc = h.ag.State.SyncStateRc.InSync
    plc = h.ag.State.SyncStatePlc.InSync
    assert rc.SwLimits and rc.DefaultDynamics and rc.ReferenceDynamics
    assert plc.SwLimits and plc.DefaultDynamics and plc.ReferenceDynamics
    h.run(200)
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID


def test_client_to_server_keeps_the_plc_data(sdk: SdkSimulator, clock: FakeClock) -> None:
    """F16: the internal start-up read must not overwrite the user data with the RC data."""
    h = harness(sdk, clock)
    h.sync(SyncMode.CLIENT_TO_SERVER, "SWLimits")
    h.run(300, until=lambda: synchronized(h))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    assert h.sw_limits.J1LowerLimit == -170.0 and h.sw_limits.J1UpperLimit == 170.0
    assert any("WriteSWLimits" in log.text for log in sdk.logs)


def test_synchronized_tools_client_to_server(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.sync(SyncMode.CLIENT_TO_SERVER, "Tool", "Frame", "Load", *DATA_SETS)
    h.run(1500, until=lambda: synchronized(h) or bool(h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error, h.history


def test_synchronized_server_to_client(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.sync(SyncMode.SERVER_TO_CLIENT, *DATA_SETS)
    h.run(1000, until=lambda: synchronized(h) or bool(h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error, h.history


def test_server_to_client_reads_rc_data(sdk: SdkSimulator, clock: FakeClock) -> None:
    """The start-up phase of SERVER_TO_CLIENT copies the RC data into the user data."""
    h = harness(sdk, clock)
    h.sync(SyncMode.SERVER_TO_CLIENT, *DATA_SETS, after_startup=False)
    h.run(200)
    assert not h.rt.Error, h.history
    assert h.sw_limits.J1LowerLimit == -360.0 and h.sw_limits.J1UpperLimit == 360.0
    assert h.sw_limits.E2LowerLimit == 0.0  # only J1..J6, E1 exist in the simulation
    assert h.default_dynamics.VelocityRate > 0
    assert h.ag.State.SyncStatePlc.InSync.SwLimits


# ---------------------------------------------------------------- errors and recovery


def test_invalid_telegram_length_is_an_error(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.cfg.Com.TelegramLengthPlcToRob = 32  # at least 64 bytes
    h.run(20)
    assert h.rt.Error and not h.rt.Initialized


def test_incompatible_srci_major_version(
    sdk: SdkSimulator, clock: FakeClock, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The RC rejects the telegram version; after the init timeout (5 s) the state is the error."""
    monkeypatch.setattr(RobotLibraryConstants, "SRCIVersion", VersionStruct(MajorVersion=2, MinorVersion=0))
    h = harness(sdk, clock)
    h.run(30)
    assert any("SRCI version not supported" in log.text for log in sdk.logs)
    assert not h.rt.Error  # the RobotTask retries (ACK_ERROR / RESET / INITIALIZE) until the timeout
    h.run(CANCEL_TIMEOUT_CYCLES)
    assert h.rt.Error and not h.rt.Initialized
    assert h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0xA4


def freeze_lifesign(h: RobotTaskHarness, seconds: float) -> None:
    """The PLC hangs: the same telegram (same LifeSign) is sent for ``seconds`` (real time)."""
    frozen = bytes(h.rout)
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        h.rin[:] = h.transport.exchange(frozen)
        time.sleep(0.005)


def test_lifesign_timeout_and_restart(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.sync(SyncMode.CLIENT_TO_SERVER, *DATA_SETS)
    h.run(300, until=lambda: synchronized(h))
    assert h.rt.Synchronized
    freeze_lifesign(h, 0.3)  # LifeSignTimeOut default 50 ms
    assert any("Lifesign timeout" in log.text for log in sdk.logs)
    h.run(20)
    # ST-FIX F65: the RI error of the RC in the telegram state (16#A5 lifesign timeout), not 16#80A2
    assert h.rt.Error and h.rt.ErrorID == TelegramState.ERROR_165_LIFESIGN_TIMEOUT
    assert not h.rt.Synchronized
    # the user acknowledges by disabling the RobotTask (a quick restart: test_quick_restart, F23)
    h.enable = False
    h.run(CANCEL_TIMEOUT_CYCLES)
    assert not h.rt.Error and not h.rt.Busy
    h.enable = True
    h.run(300, until=lambda: synchronized(h))
    assert h.rt.Synchronized and not h.rt.Error, h.history


def test_quick_restart(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.run(100, until=lambda: bool(h.rt.Initialized))
    h.enable = False
    h.run(5)
    h.enable = True
    h.run(300, until=lambda: bool(h.rt.Initialized))
    assert h.rt.Initialized, h.history


# ---------------------------------------------------------------- long run, TCP


@pytest.mark.slow
def test_long_run_10000_cycles(sdk: SdkSimulator, clock: FakeClock) -> None:
    h = harness(sdk, clock)
    h.sync(SyncMode.CLIENT_TO_SERVER, *DATA_SETS)
    h.run(300, until=lambda: synchronized(h))
    start = time.perf_counter()
    h.run(10_000)
    per_cycle = (time.perf_counter() - start) / 10_000
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history[-5:]
    assert h.ag.Cyclic.RobToPlc.TelegramState == TelegramState.INITIALIZED
    assert per_cycle < 0.01, f"{per_cycle * 1000:.2f} ms per cycle"


def test_synchronized_over_tcp(sdk: SdkSimulator) -> None:
    """PLC gateway (TCP server) in front of the SDK, real time with 10 ms cycles."""
    with PlcGatewaySimulator(lambda telegram: sdk.exchange(telegram, SIZE), SIZE, SIZE) as gateway:
        transport = TcpTransport("127.0.0.1", gateway.port, SIZE, SIZE, response_timeout=0.5)
        with transport:
            h = RobotTaskHarness(transport)
            h.sync(SyncMode.CLIENT_TO_SERVER, *DATA_SETS)
            for _ in range(400):
                t0 = time.monotonic()
                h.cycle()
                if h.rt.Synchronized:
                    break
                time.sleep(max(0.0, 0.01 - (time.monotonic() - t0)))
            assert h.rt.Synchronized and not h.rt.Error, h.history
    assert gateway.errors == []


def test_logging_to_python(sdk: SdkSimulator, clock: FakeClock, caplog: pytest.LogCaptureFixture) -> None:
    import logging

    from srci.logging_bridge import PythonLogger

    h = harness(sdk, clock)
    h.rt.ExternalLogger = PythonLogger()
    with caplog.at_level(logging.INFO, logger="srci.plc"):
        h.run(100, until=lambda: bool(h.rt.Initialized))
    texts = [r.getMessage() for r in caplog.records]
    assert any("to INITIALIZED (255)" in t for t in texts)
    assert any("ACR-ID [1]: Added" in t for t in texts)
    assert h.system_log[0]  # the ring buffer (output SystemLog) is filled as well
