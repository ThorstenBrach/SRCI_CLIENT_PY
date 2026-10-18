# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.opcua.test_opcua_transport
#  Author:      Thorsten Brach
#  Date:        2026-10-18
#
#  Description:
#    OpcUaTransport against a local asyncua server (real sockets on localhost).
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

"""OpcUaTransport against a local asyncua server (real sockets on localhost)."""

from __future__ import annotations

import socket
import sys
import threading
from collections.abc import Iterator
from typing import Any

import pytest

asyncua = pytest.importorskip("asyncua")

from asyncua import sync, ua  # noqa: E402

from srci.transport import (  # noqa: E402
    OpcUaTransport,
    ReconnectPolicy,
    TransportClosedError,
    TransportConnectError,
    TransportProtocolError,
    TransportState,
    TransportTimeoutError,
)
from srci.transport.opcua import INSTALL_HINT, browse  # noqa: E402

pytestmark = pytest.mark.opcua

SEND, RECV = 16, 24
NS = "urn:srci:test"


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port: int = s.getsockname()[1]
        return port


class Server:
    """asyncua server with the telegram nodes of two encodings.

    ``ns=<i>;s=BS.Out`` / ``BS.In``: ``ByteString``; ``ns=<i>;s=Arr.Out`` / ``Arr.In``: ``Byte[]``;
    ``Num.Out`` / ``Num.In``: ``Double[]`` (number array, e.g. VAL 3 ``num``);
    ``ns=<i>;s=Other``: a Double (no telegram).
    """

    def __init__(self, port: int | None = None) -> None:
        self.port = port or free_port()
        self.endpoint = f"opc.tcp://127.0.0.1:{self.port}"
        self.server = sync.Server()
        self.server.set_endpoint(f"opc.tcp://127.0.0.1:{self.port}/")
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        self.idx = self.server.register_namespace(NS)
        objects = self.server.nodes.objects
        folder = objects.add_folder(self.idx, "SRCI")
        self.nodes: dict[str, Any] = {}
        for name, size, variant in (
            ("BS.Out", SEND, ua.Variant(bytes(SEND), ua.VariantType.ByteString)),
            ("BS.In", RECV, ua.Variant(bytes(RECV), ua.VariantType.ByteString)),
            ("Arr.Out", SEND, ua.Variant([0] * SEND, ua.VariantType.Byte)),
            ("Arr.In", RECV, ua.Variant([0] * RECV, ua.VariantType.Byte)),
            ("Num.Out", SEND, ua.Variant([0.0] * SEND, ua.VariantType.Double)),
            ("Num.In", RECV, ua.Variant([0.0] * RECV, ua.VariantType.Double)),
            ("Scalar", 0, ua.Variant(7, ua.VariantType.Byte)),
            ("Text", 0, ua.Variant("abc", ua.VariantType.String)),
            ("Short", 0, ua.Variant(bytes(3), ua.VariantType.ByteString)),
            ("Other", 0, ua.Variant(1.5, ua.VariantType.Double)),
        ):
            del size
            node = folder.add_variable(f"ns={self.idx};s={name}", name, variant)
            node.set_writable()
            self.nodes[name] = node

    def nid(self, name: str) -> str:
        return f"ns={self.idx};s={name}"

    def start(self) -> Server:
        self.server.start()
        return self

    def stop(self) -> None:
        self.server.stop()

    def value(self, name: str) -> Any:
        return self.nodes[name].read_value()

    def set(self, name: str, value: Any, vtype: Any) -> None:
        self.nodes[name].write_value(ua.DataValue(ua.Variant(value, vtype)))


@pytest.fixture(scope="module")
def server() -> Iterator[Server]:
    s = Server().start()
    try:
        yield s
    finally:
        s.stop()


def transport(server: Server, kind: str = "BS", **kw: Any) -> OpcUaTransport:
    return OpcUaTransport(
        server.endpoint, server.nid(f"{kind}.Out"), server.nid(f"{kind}.In"), SEND, RECV, **kw
    )


@pytest.mark.parametrize("kind", ["BS", "Arr", "Num"])
def test_write_and_read(server: Server, kind: str) -> None:
    """The telegram is written to out_node and the telegram of in_node is read (ByteString, Byte[], Double[])."""
    answer = bytes(range(100, 100 + RECV))
    if kind == "BS":
        server.set("BS.In", answer, ua.VariantType.ByteString)
    elif kind == "Arr":
        server.set("Arr.In", list(answer), ua.VariantType.Byte)
    else:
        server.set("Num.In", [float(b) for b in answer], ua.VariantType.Double)
    with transport(server, kind) as t:
        assert t.state is TransportState.CONNECTED
        for n in range(20):
            out = bytes([n]) + bytes(range(1, SEND))
            assert t.exchange(out) == answer
            written = server.value(f"{kind}.Out")
            assert bytes(int(v) for v in written) == out
            assert type(written) is {"BS": bytes, "Arr": list, "Num": list}[kind]  # the encoding is kept
            if kind == "Num":
                assert all(isinstance(v, float) for v in written)
        s = t.statistics
        assert (s.exchanges, s.connects, s.errors) == (20, 1, 0)
        assert s.bytes_sent == 20 * SEND and s.bytes_received == 20 * RECV
        assert s.max_rtt > 0
    assert t.state is TransportState.CLOSED


def test_close_is_idempotent_and_final(server: Server) -> None:
    """close twice; an exchange after close raises TransportClosedError."""
    t = transport(server)
    t.connect()
    t.close()
    t.close()
    with pytest.raises(TransportClosedError):
        t.exchange(bytes(SEND))


def test_connects_on_first_exchange(server: Server) -> None:
    """Without connect() the first exchange opens the connection."""
    server.set("BS.In", bytes(RECV), ua.VariantType.ByteString)
    t = transport(server)
    try:
        assert t.exchange(bytes(SEND)) == bytes(RECV)
        assert t.statistics.connects == 1
    finally:
        t.close()


@pytest.mark.parametrize(
    ("out", "inp", "message"),
    [
        ("Missing", "BS.In", "out_node"),
        ("BS.Out", "Missing", "in_node"),
        ("Other", "BS.In", "Double is no array"),
        ("Scalar", "BS.In", "Byte is no array"),
        ("BS.Out", "Text", "String cannot carry"),
        ("Short", "BS.In", "has 3 bytes"),
        ("BS.Out", "Arr.Out", "has 16 bytes"),
    ],
)
def test_connect_checks_nodes(server: Server, out: str, inp: str, message: str) -> None:
    """Unknown NodeId, wrong data type and wrong length are reported on connect."""
    t = OpcUaTransport(server.endpoint, server.nid(out), server.nid(inp), SEND, RECV)
    with pytest.raises(TransportConnectError, match=message):
        t.connect()
    assert t.state is TransportState.ERROR


def test_length_check_can_be_disabled(server: Server) -> None:
    """check_lengths=False accepts a node with another length; a wrong answer is a protocol error."""
    t = OpcUaTransport(
        server.endpoint, server.nid("BS.Out"), server.nid("Short"), SEND, RECV, check_lengths=False
    )
    with t, pytest.raises(TransportProtocolError, match="3 bytes"):
        t.exchange(bytes(SEND))


def test_wrong_answer_length_is_protocol_error(server: Server) -> None:
    """The RC writes an answer of the wrong length: TransportProtocolError, the connection stays."""
    with transport(server) as t:
        server.set("BS.In", bytes(RECV - 1), ua.VariantType.ByteString)
        with pytest.raises(TransportProtocolError):
            t.exchange(bytes(SEND))
        assert t.state is TransportState.CONNECTED
        server.set("BS.In", bytes(RECV), ua.VariantType.ByteString)
        assert t.exchange(bytes(SEND)) == bytes(RECV)
        assert t.statistics.connects == 1


def test_no_server() -> None:
    """No server at the endpoint: TransportConnectError, reconnect backoff starts."""
    t = OpcUaTransport(f"opc.tcp://127.0.0.1:{free_port()}", "ns=2;s=a", "ns=2;s=b", SEND, RECV, timeout=0.5)
    with pytest.raises(TransportConnectError, match="cannot connect"):
        t.connect()
    assert t.state is TransportState.ERROR
    with pytest.raises(TransportConnectError, match="delayed"):
        t.exchange(bytes(SEND))


def test_silent_server_times_out() -> None:
    """A server that accepts but never answers: connect fails within the timeout."""
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        port = listener.getsockname()[1]
        t = OpcUaTransport(f"opc.tcp://127.0.0.1:{port}", "ns=2;s=a", "ns=2;s=b", SEND, RECV, timeout=0.3)
        with pytest.raises(TransportConnectError):
            t.connect()


def test_server_restart_and_reconnect() -> None:
    """The server goes down: TransportClosedError; after the restart the transport reconnects."""
    s = Server().start()
    port = s.port
    now = [0.0]
    t = OpcUaTransport(
        s.endpoint,
        s.nid("BS.Out"),
        s.nid("BS.In"),
        SEND,
        RECV,
        timeout=0.5,
        reconnect=ReconnectPolicy(initial_delay=0.1, max_delay=0.1),
        clock=lambda: now[0],
    )
    try:
        assert t.exchange(bytes(SEND)) == bytes(RECV)
        s.stop()
        with pytest.raises((TransportClosedError, TransportTimeoutError)):
            t.exchange(bytes(SEND))
        assert t.state is TransportState.ERROR
        with pytest.raises(TransportConnectError, match="cannot connect"):
            t.exchange(bytes(SEND))  # server still down
        s = Server(port).start()
        with pytest.raises(TransportConnectError, match="delayed"):
            t.exchange(bytes(SEND))  # backoff
        now[0] += 1.0
        assert t.exchange(bytes(SEND)) == bytes(RECV)
        assert t.statistics.connects == 2
        assert t.statistics.errors >= 1
    finally:
        t.close()
        s.stop()


def test_reconnect_disabled(server: Server) -> None:
    """With reconnect disabled a lost connection stays lost."""
    t = transport(server, reconnect=ReconnectPolicy(enabled=False))
    t.connect()
    t._drop(TransportState.ERROR)  # connection lost
    with pytest.raises(TransportConnectError, match="disabled"):
        t.exchange(bytes(SEND))
    t.close()


def test_timeout_and_errors_of_a_request_drop_the_connection(server: Server) -> None:
    """A timeout of a request is a TransportTimeoutError, any other error a TransportClosedError."""
    with transport(server) as t:
        t.connect()

        def timeout(_value: Any) -> None:
            raise TimeoutError

        t._out.write_value = timeout
        with pytest.raises(TransportTimeoutError):
            t.exchange(bytes(SEND))
        assert t.state is TransportState.ERROR
        assert t.statistics.timeouts == 1

        t.connect()

        def bad(_value: Any) -> None:
            raise ConnectionResetError("connection lost")

        t._out.write_value = bad
        with pytest.raises(TransportClosedError, match="OPC UA error"):
            t.exchange(bytes(SEND))
        assert t.state is TransportState.ERROR


def test_username_password_are_passed(server: Server, monkeypatch: pytest.MonkeyPatch) -> None:
    """User and password are given to the client (anonymous server: the login is rejected or ignored)."""
    seen: dict[str, str] = {}
    monkeypatch.setattr(sync.Client, "set_user", lambda self, u: seen.__setitem__("user", u))
    monkeypatch.setattr(sync.Client, "set_password", lambda self, p: seen.__setitem__("pw", p))
    with transport(server, username="robot", password="secret"):
        pass
    assert seen == {"user": "robot", "pw": "secret"}


def test_missing_asyncua(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without asyncua the connect explains how to install it."""
    monkeypatch.setitem(sys.modules, "asyncua", None)
    t = OpcUaTransport("opc.tcp://127.0.0.1:4840", "ns=2;s=a", "ns=2;s=b", SEND, RECV)
    with pytest.raises(TransportConnectError, match=r"srci-client\[opcua\]"):
        t.connect()
    assert "pip install" in INSTALL_HINT


def test_browse_lists_telegram_candidates(server: Server) -> None:
    """browse lists the variables with data type, length and write access."""
    infos = {i.node_id: i for i in browse(server.endpoint)}
    bs = infos[server.nid("BS.Out")]
    assert (bs.data_type, bs.length, bs.writable, bs.telegram_candidate) == ("ByteString", SEND, True, True)
    assert bs.path.endswith("SRCI/BS.Out")
    arr = infos[server.nid("Arr.In")]
    assert (arr.data_type, arr.is_array, arr.length, arr.telegram_candidate) == ("Byte", True, RECV, True)
    assert not infos[server.nid("Other")].telegram_candidate
    assert not any("/Server/" in i.path for i in infos.values())  # the server object is skipped


def test_browse_no_server() -> None:
    """browse of an unreachable endpoint raises TransportConnectError."""
    with pytest.raises(TransportConnectError):
        browse(f"opc.tcp://127.0.0.1:{free_port()}", timeout=0.5)


def test_parallel_transports(server: Server) -> None:
    """Two transports (two robots) on one server in two threads."""
    server.set("BS.In", bytes(RECV), ua.VariantType.ByteString)
    server.set("Arr.In", [1] * RECV, ua.VariantType.Byte)
    errors: list[BaseException] = []

    def run(kind: str, answer: bytes) -> None:
        try:
            with transport(server, kind) as t:
                for _ in range(10):
                    assert t.exchange(bytes(SEND)) == answer
        except BaseException as exc:
            errors.append(exc)

    threads = [
        threading.Thread(target=run, args=("BS", bytes(RECV))),
        threading.Thread(target=run, args=("Arr", bytes([1] * RECV))),
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join(30)
    assert not errors
