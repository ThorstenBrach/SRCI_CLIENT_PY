"""TcpTransport against the PLC gateway simulator (real sockets on localhost)."""

from __future__ import annotations

import socket
import time
from collections.abc import Iterator

import pytest

from srci.sim.gateway import GatewayAction, PlcGatewaySimulator
from srci.transport import (
    ReconnectPolicy,
    TcpTransport,
    TransportClosedError,
    TransportConnectError,
    TransportProtocolError,
    TransportState,
    TransportTimeoutError,
)

pytestmark = pytest.mark.tcp

SEND, RECV = 16, 24
TIMEOUT = 0.2


def answer(request: bytes) -> bytes:
    """Deterministic answer: counter byte + inverted request + padding."""
    return bytes([request[0]]) + bytes(b ^ 0xFF for b in request) + bytes(RECV - 1 - SEND)


def request(n: int) -> bytes:
    return bytes([n % 256]) + bytes(range(1, SEND))


@pytest.fixture
def sim() -> Iterator[PlcGatewaySimulator]:
    with PlcGatewaySimulator(answer, SEND, RECV) as s:
        yield s


def transport(sim: PlcGatewaySimulator, **kw: object) -> TcpTransport:
    return TcpTransport("127.0.0.1", sim.port, SEND, RECV, response_timeout=TIMEOUT, **kw)  # type: ignore[arg-type]


def test_lockstep_cycles(sim: PlcGatewaySimulator) -> None:
    with transport(sim) as t:
        for n in range(200):
            assert t.exchange(request(n)) == answer(request(n))
        s = t.statistics
        assert (s.exchanges, s.connects, s.errors) == (200, 1, 0)
        assert s.bytes_sent == 200 * SEND and s.bytes_received == 200 * RECV
        assert 0 < s.max_rtt < TIMEOUT
    assert t.state is TransportState.CLOSED
    assert sim.requests == 200


def test_connects_on_first_exchange(sim: PlcGatewaySimulator) -> None:
    t = transport(sim)
    assert t.state is TransportState.DISCONNECTED
    assert t.exchange(request(1)) == answer(request(1))
    assert t.connected
    t.close()


def test_answer_in_pieces_is_assembled(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(chunks=RECV, chunk_delay=0.002)
    with transport(sim) as t:
        assert t.exchange(request(7)) == answer(request(7))


def test_wrong_telegram_size_is_rejected(sim: PlcGatewaySimulator) -> None:
    with transport(sim) as t, pytest.raises(ValueError):
        t.exchange(b"\x00" * (SEND - 1))


def test_no_answer_times_out_and_next_cycle_reconnects(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(reply=(i != 1))
    with transport(sim) as t:
        t.exchange(request(0))
        start = time.monotonic()
        with pytest.raises(TransportTimeoutError):
            t.exchange(request(1))
        assert TIMEOUT * 0.9 <= time.monotonic() - start < TIMEOUT + 0.5
        assert t.state is TransportState.ERROR
        assert t.exchange(request(2)) == answer(request(2))  # new connection
        assert t.statistics.connects == 2 and t.statistics.timeouts == 1


def test_late_answer_does_not_shift_the_stream(sim: PlcGatewaySimulator) -> None:
    """Without framing a late answer would be taken as the answer of the next request."""
    sim.script = lambda i, req: GatewayAction(delay=TIMEOUT * 2 if i == 1 else 0.0)
    with transport(sim) as t:
        t.exchange(request(0))
        with pytest.raises(TransportTimeoutError):
            t.exchange(request(1))
        time.sleep(TIMEOUT * 2)
        for n in range(2, 6):
            assert t.exchange(request(n)) == answer(request(n))


def test_partial_answer_then_silence_is_a_timeout(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(truncate=RECV // 2)
    with transport(sim) as t, pytest.raises(TransportTimeoutError, match=f"{RECV // 2}/{RECV}"):
        t.exchange(request(0))


def test_peer_closes_during_answer(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(truncate=5, close_after=True) if i == 0 else GatewayAction()
    with transport(sim) as t:
        with pytest.raises(TransportClosedError):
            t.exchange(request(0))
        assert t.exchange(request(1)) == answer(request(1))


def test_peer_closes_after_answer(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(close_after=(i == 0))
    with transport(sim) as t:
        assert t.exchange(request(0)) == answer(request(0))
        time.sleep(0.05)
        with pytest.raises((TransportClosedError, TransportTimeoutError)):
            t.exchange(request(1))
        assert t.exchange(request(2)) == answer(request(2))


def test_extra_bytes_violate_lockstep(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(extra=b"\x00" if i == 0 else b"")
    with transport(sim) as t:
        with pytest.raises(TransportProtocolError):
            t.exchange(request(0))
        assert t.exchange(request(1)) == answer(request(1))


def test_extra_byte_check_can_be_disabled(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(extra=b"\x00")
    with transport(sim, check_extra_bytes=False) as t:
        t.exchange(request(0))


def test_server_restart_on_same_port() -> None:
    first = PlcGatewaySimulator(answer, SEND, RECV).start()
    port = first.port
    t = TcpTransport(
        "127.0.0.1", port, SEND, RECV, response_timeout=TIMEOUT, reconnect=ReconnectPolicy(initial_delay=0)
    )
    assert t.exchange(request(0)) == answer(request(0))
    first.stop()
    with pytest.raises((TransportClosedError, TransportTimeoutError)):
        t.exchange(request(1))
    second = PlcGatewaySimulator(answer, SEND, RECV, port=port).start()
    try:
        deadline = time.monotonic() + 3
        while True:
            try:
                assert t.exchange(request(2)) == answer(request(2))
                break
            except (TransportConnectError, TransportClosedError, TransportTimeoutError):
                assert time.monotonic() < deadline
                time.sleep(0.05)
    finally:
        t.close()
        second.stop()


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port: int = s.getsockname()[1]
    return port


def test_connect_refused_and_backoff() -> None:
    now = [100.0]
    t = TcpTransport(
        "127.0.0.1",
        free_port(),
        SEND,
        RECV,
        connect_timeout=0.5,
        reconnect=ReconnectPolicy(initial_delay=1.0, max_delay=4.0),
        clock=lambda: now[0],
    )
    with pytest.raises(TransportConnectError, match="cannot connect"):
        t.exchange(request(0))
    with pytest.raises(TransportConnectError, match="delayed"):
        t.exchange(request(0))  # no new attempt within 1 s
    now[0] += 1.0
    with pytest.raises(TransportConnectError, match="cannot connect"):
        t.exchange(request(0))
    now[0] += 1.5  # delay is now 2 s
    with pytest.raises(TransportConnectError, match="delayed"):
        t.exchange(request(0))
    assert t.statistics.errors == 4


def test_reconnect_disabled(sim: PlcGatewaySimulator) -> None:
    sim.script = lambda i, req: GatewayAction(reply=(i != 0))
    t = transport(sim, reconnect=ReconnectPolicy(enabled=False))
    with pytest.raises(TransportTimeoutError):
        t.exchange(request(0))
    with pytest.raises(TransportConnectError, match="disabled"):
        t.exchange(request(1))
    t.connect()  # explicit connect still works
    assert t.exchange(request(2)) == answer(request(2))
    t.close()


def test_exchange_after_close_raises(sim: PlcGatewaySimulator) -> None:
    t = transport(sim)
    t.connect()
    t.close()
    t.close()  # idempotent
    with pytest.raises(TransportClosedError):
        t.exchange(request(0))


def test_many_cycles_with_random_faults(sim: PlcGatewaySimulator) -> None:
    """Soak test: random delays/chunks/drops - every successful answer must match its request."""
    import random

    rnd = random.Random(42)

    def script(i: int, req: bytes) -> GatewayAction:
        r = rnd.random()
        if r < 0.03:
            return GatewayAction(reply=False)
        if r < 0.06:
            return GatewayAction(delay=TIMEOUT * 1.5)
        if r < 0.3:
            return GatewayAction(chunks=rnd.randint(2, 6))
        return GatewayAction()

    sim.script = script
    ok = errors = 0
    with transport(sim, reconnect=ReconnectPolicy(initial_delay=0)) as t:
        for n in range(150):
            try:
                assert t.exchange(request(n)) == answer(request(n))
                ok += 1
            except (TransportTimeoutError, TransportClosedError, TransportConnectError):
                errors += 1
    assert ok > 120 and errors > 0


def test_simulator_serves_one_client_after_another(sim: PlcGatewaySimulator) -> None:
    for _ in range(3):
        with transport(sim) as t:
            t.exchange(request(1))
    deadline = time.monotonic() + 1
    while sim.connections < 3 and time.monotonic() < deadline:
        time.sleep(0.01)
    assert sim.connections == 3
