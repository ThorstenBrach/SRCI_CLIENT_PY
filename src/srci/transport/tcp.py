"""TCP transport to the PLC gateway.

Protocol (agreed with the PLC gateway):

* Python is TCP client, the PLC is TCP server.
* Raw SRCI telegrams, no additional header: every cycle Python sends exactly
  ``send_size`` bytes, the PLC answers with exactly ``recv_size`` bytes (lockstep).
* The SRCI telegram itself carries the integrity mechanisms (LifeSign, sequence ACKs).

Because there is no framing, a late answer would shift all following telegrams. After a
timeout or any other error the connection is therefore closed; the next ``exchange``
reconnects and starts with a clean byte stream.
"""

from __future__ import annotations

import contextlib
import socket
import time

from srci.transport.base import (
    Clock,
    ReconnectPolicy,
    Transport,
    TransportClosedError,
    TransportConnectError,
    TransportError,
    TransportProtocolError,
    TransportState,
    TransportTimeoutError,
)

__all__ = ["TcpTransport"]


class TcpTransport(Transport):
    """Lockstep TCP client for the PLC gateway."""

    def __init__(
        self,
        host: str,
        port: int,
        send_size: int,
        recv_size: int,
        *,
        response_timeout: float = 0.1,
        connect_timeout: float = 1.0,
        reconnect: ReconnectPolicy | None = None,
        check_extra_bytes: bool = True,
        clock: Clock = time.monotonic,
    ) -> None:
        super().__init__(send_size, recv_size, clock)
        self.host = host
        self.port = port
        self.response_timeout = response_timeout
        self.connect_timeout = connect_timeout
        self.reconnect = reconnect if reconnect is not None else ReconnectPolicy()
        self.check_extra_bytes = check_extra_bytes
        self._sock: socket.socket | None = None
        self._user_closed = False
        self._buffer = bytearray(recv_size)

    # ------------------------------------------------------------------ connection

    def connect(self) -> None:
        self._user_closed = False
        self._drop(TransportState.DISCONNECTED)
        try:
            sock = socket.create_connection((self.host, self.port), timeout=self.connect_timeout)
        except OSError as exc:
            self.reconnect.failed(self.clock())
            self._state = TransportState.ERROR
            raise TransportConnectError(f"cannot connect to {self.host}:{self.port}: {exc}") from exc
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._sock = sock
        self._state = TransportState.CONNECTED
        self.reconnect.succeeded()
        self.statistics.connects += 1

    def close(self) -> None:
        self._user_closed = True
        self._drop(TransportState.CLOSED)

    def _drop(self, state: TransportState) -> None:
        sock, self._sock = self._sock, None
        if sock is not None:
            with contextlib.suppress(OSError):
                sock.close()
        self._state = state

    def _ensure_connected(self) -> socket.socket:
        if self._sock is not None:
            return self._sock
        if self._user_closed:
            raise TransportClosedError("transport was closed")
        if self.statistics.connects > 0 or self._state is TransportState.ERROR:
            if not self.reconnect.enabled:
                raise TransportConnectError("connection lost and reconnect is disabled")
            now = self.clock()
            if not self.reconnect.allowed(now):
                wait = self.reconnect.next_attempt - now
                raise TransportConnectError(f"reconnect to {self.host}:{self.port} delayed ({wait:.3f} s)")
        self.connect()
        return self._current_socket()

    def _current_socket(self) -> socket.socket:
        if self._sock is None:  # pragma: no cover - connect() raises instead
            raise TransportConnectError("not connected")
        return self._sock

    # ------------------------------------------------------------------ exchange

    def _exchange(self, out: bytes) -> bytes:
        sock = self._ensure_connected()
        got = 0
        try:
            deadline = self.clock() + self.response_timeout
            sock.settimeout(self.response_timeout)
            sock.sendall(out)
            view = memoryview(self._buffer)
            while got < self.recv_size:
                remaining = deadline - self.clock()
                if remaining <= 0:
                    raise TransportTimeoutError(
                        f"no complete answer within {self.response_timeout * 1000:.0f} ms ({got}/{self.recv_size} bytes)"
                    )
                sock.settimeout(remaining)
                n = sock.recv_into(view[got:], self.recv_size - got)
                if n == 0:
                    raise TransportClosedError(f"peer closed the connection ({got}/{self.recv_size} bytes)")
                got += n
            if self.check_extra_bytes:
                self._check_no_extra_bytes(sock)
            return bytes(self._buffer)
        except TransportError:
            self._drop(TransportState.ERROR)
            raise
        except TimeoutError as exc:
            self._drop(TransportState.ERROR)
            raise TransportTimeoutError(
                f"no complete answer within {self.response_timeout * 1000:.0f} ms ({got}/{self.recv_size} bytes)"
            ) from exc
        except OSError as exc:
            self._drop(TransportState.ERROR)
            raise TransportClosedError(f"connection error: {exc}") from exc

    def _check_no_extra_bytes(self, sock: socket.socket) -> None:
        """In lockstep the PLC sends exactly one telegram per request."""
        sock.settimeout(0.0)
        try:
            extra = sock.recv(1, socket.MSG_PEEK)
        except (BlockingIOError, InterruptedError):
            return
        if extra:
            raise TransportProtocolError("received more bytes than one telegram (lockstep violated)")
        # b"" -> peer closed after its answer; detected by the next exchange
