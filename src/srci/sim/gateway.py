# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.sim.gateway
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    PLC gateway simulator: TCP server that answers each telegram with exactly one telegram.
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

"""PLC gateway simulator: TCP server that answers each telegram with exactly one telegram.

Behaves like the gateway PLC (TCP server, raw telegrams, lockstep). The answer is
computed by a ``handler`` - e.g. an echo for tests or the SRCI SDK server (M5).
For tests, ``script`` can change the behaviour per request (delays, chunks, no
answer, disconnect, extra bytes).
"""

from __future__ import annotations

import contextlib
import socket
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from types import TracebackType
from typing import Self

__all__ = ["GatewayAction", "PlcGatewaySimulator"]

Handler = Callable[[bytes], bytes | bytearray]


@dataclass
class GatewayAction:
    """How the simulator answers one request (default: normal answer)."""

    reply: bool = True
    delay: float = 0.0  # before the answer
    chunks: int = 1  # answer split into n parts
    chunk_delay: float = 0.0
    truncate: int | None = None  # send only the first n bytes
    extra: bytes = b""  # appended to the answer (lockstep violation)
    close_after: bool = False  # close the connection after this request


Script = Callable[[int, bytes], GatewayAction]


class PlcGatewaySimulator:
    """Threaded lockstep TCP server (one client at a time, like the PLC gateway)."""

    def __init__(
        self,
        handler: Handler,
        request_size: int,
        response_size: int,
        host: str = "127.0.0.1",
        port: int = 0,
        script: Script | None = None,
    ) -> None:
        self.handler = handler
        self.request_size = request_size
        self.response_size = response_size
        self.script = script
        self.requests = 0
        self.connections = 0
        self.errors: list[str] = []
        self._server = socket.create_server((host, port), reuse_port=False)
        self._server.settimeout(0.05)
        self.address: tuple[str, int] = self._server.getsockname()[:2]
        self._conn: socket.socket | None = None
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="PlcGatewaySimulator", daemon=True)

    # ------------------------------------------------------------------ lifecycle

    @property
    def port(self) -> int:
        return self.address[1]

    def start(self) -> Self:
        self._thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2.0)
        with contextlib.suppress(OSError):
            self._server.close()
        self.drop_connection()

    def drop_connection(self) -> None:
        conn, self._conn = self._conn, None
        if conn is not None:
            with contextlib.suppress(OSError):
                conn.close()

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.stop()

    # ------------------------------------------------------------------ server

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _ = self._server.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            conn.settimeout(0.05)
            self._conn = conn
            self.connections += 1
            try:
                self._serve(conn)
            except OSError as exc:
                self.errors.append(str(exc))
            finally:
                self.drop_connection()

    def _recv_request(self, conn: socket.socket) -> bytes | None:
        data = bytearray()
        while len(data) < self.request_size:
            if self._stop.is_set():
                return None
            try:
                chunk = conn.recv(self.request_size - len(data))
            except TimeoutError:
                continue
            if not chunk:
                return None
            data += chunk
        return bytes(data)

    def _serve(self, conn: socket.socket) -> None:
        while not self._stop.is_set():
            request = self._recv_request(conn)
            if request is None:
                return
            index = self.requests
            self.requests += 1
            action = self.script(index, request) if self.script else GatewayAction()
            if action.reply:
                answer = bytes(self.handler(request))
                if len(answer) != self.response_size:
                    self.errors.append(f"handler returned {len(answer)} bytes")
                    return
                if action.truncate is not None:
                    answer = answer[: action.truncate]
                answer += action.extra
                if action.delay:
                    time.sleep(action.delay)
                parts = max(1, action.chunks)
                step = max(1, -(-len(answer) // parts))
                for pos in range(0, len(answer), step):
                    conn.sendall(answer[pos : pos + step])
                    if action.chunk_delay:
                        time.sleep(action.chunk_delay)
            if action.close_after:
                return
