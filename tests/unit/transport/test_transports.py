"""Transport base, loopback and fault injection (no sockets)."""

from __future__ import annotations

import contextlib

import pytest

from srci.transport import (
    Fault,
    FaultInjectingTransport,
    FaultPlan,
    LoopbackTransport,
    ReconnectPolicy,
    TransportClosedError,
    TransportError,
    TransportProtocolError,
    TransportState,
    TransportTimeoutError,
)


def echo(size: int = 4) -> LoopbackTransport:
    return LoopbackTransport(lambda b: b[:size] + bytes(max(0, size - len(b))), send_size=4, recv_size=size)


def test_loopback_exchange_and_statistics() -> None:
    t = echo()
    assert t.state is TransportState.DISCONNECTED
    assert t.exchange(b"\x01\x02\x03\x04") == b"\x01\x02\x03\x04"
    assert t.connected and t.statistics.exchanges == 1 and t.statistics.connects == 1
    t.close()
    with pytest.raises(TransportClosedError):
        t.exchange(b"\x00" * 4)


def test_loopback_checks_sizes() -> None:
    t = LoopbackTransport(lambda b: b"\x00", send_size=4, recv_size=2)
    with pytest.raises(ValueError):
        t.exchange(b"\x00")
    with pytest.raises(TransportProtocolError):
        t.exchange(b"\x00" * 4)
    assert t.statistics.errors == 1
    with pytest.raises(ValueError):
        LoopbackTransport(lambda b: b, 0, 1)


def test_context_manager() -> None:
    with echo() as t:
        assert t.connected
    assert t.state is TransportState.CLOSED


def test_reconnect_policy_backoff() -> None:
    p = ReconnectPolicy(initial_delay=0.5, max_delay=2.0, factor=2.0)
    assert p.allowed(0.0)
    p.failed(10.0)
    assert not p.allowed(10.4) and p.allowed(10.5)
    p.failed(10.5)
    assert p.next_attempt == 11.5
    p.failed(11.5)
    p.failed(13.5)
    assert p.next_attempt == 15.5  # capped at max_delay
    p.succeeded()
    assert p.allowed(0.0)


@pytest.mark.parametrize(
    ("fault", "error"),
    [
        (Fault.TIMEOUT, TransportTimeoutError),
        (Fault.DROP_REQUEST, TransportTimeoutError),
        (Fault.DISCONNECT, TransportClosedError),
        (Fault.PROTOCOL, TransportProtocolError),
    ],
)
def test_fault_errors(fault: Fault, error: type[TransportError]) -> None:
    calls: list[bytes] = []

    def handler(b: bytes) -> bytes:
        calls.append(b)
        return b

    inner = LoopbackTransport(handler, 2, 2)
    t = FaultInjectingTransport(inner, FaultPlan(at={1: fault}))
    t.exchange(b"\x00\x01")
    with pytest.raises(error):
        t.exchange(b"\x00\x02")
    assert t.exchange(b"\x00\x03") == b"\x00\x03"
    assert t.injected == [(1, fault)]
    assert t.statistics.errors == 1
    assert len(calls) == (2 if fault is Fault.DROP_REQUEST or fault is Fault.DISCONNECT else 3)


def test_fault_corrupt_and_stale() -> None:
    inner = LoopbackTransport(lambda b: b, 4, 4)
    t = FaultInjectingTransport(inner, FaultPlan(at={1: Fault.CORRUPT, 2: Fault.STALE}, seed=3))
    first = t.exchange(b"\x10\x20\x30\x40")
    corrupt = t.exchange(b"\x10\x20\x30\x40")
    diff = [a ^ b for a, b in zip(first, corrupt, strict=True)]
    assert sum(bin(d).count("1") for d in diff) == 1  # exactly one bit flipped
    assert t.exchange(b"\x99\x99\x99\x99") == corrupt  # stale answer repeated


def test_random_faults_are_reproducible() -> None:
    def run() -> list[tuple[int, Fault]]:
        t = FaultInjectingTransport(LoopbackTransport(lambda b: b, 1, 1), FaultPlan(probability=0.2, seed=9))
        for _ in range(100):
            with contextlib.suppress(TransportError):
                t.exchange(b"\x00")
        return t.injected

    first = run()
    assert first == run() and 5 < len(first) < 40
    assert t_state_passthrough()


def t_state_passthrough() -> bool:
    inner = LoopbackTransport(lambda b: b, 1, 1)
    t = FaultInjectingTransport(inner, FaultPlan())
    t.connect()
    ok = t.state is TransportState.CONNECTED
    t.close()
    return ok and t.state is TransportState.CLOSED
