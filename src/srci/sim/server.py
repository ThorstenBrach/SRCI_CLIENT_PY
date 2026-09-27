# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.sim.server
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    SDK server: the SRCI SDK simulator behind a TCP server - for PLC tests (TwinCAT,
#    Codesys).
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

"""SDK server: the SRCI SDK simulator behind a TCP server - for PLC tests (TwinCAT, Codesys).

``python -m srci.sim.server --port 5000 --length 256``

The PLC is the TCP client and the cycle master (like the Python client with ``TcpTransport``):
it sends one raw PLC->RC telegram, the server answers with exactly one RC->PLC telegram
(lockstep, no framing, fixed telegram lengths). Every telegram is one cycle of the simulated
robot controller, so the PLC task should run with the cycle time of the simulator (10 ms).

A new connection starts with a new simulator (like a restart of the robot controller), so a
PLC program can be restarted without restarting the server.

The simulator needs the locally built SDK library (``SRCI_SDK_SIM_LIB``); the SDK is licensed
and not part of the package.
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from types import TracebackType
from typing import Self

from srci.sim.gateway import PlcGatewaySimulator
from srci.sim.sdk import SdkLog, SdkNotAvailableError, SdkSimulator

__all__ = ["SdkServer", "main"]


class SdkServer:
    """SDK simulator + lockstep TCP server; the simulator is reset for every new connection."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 5000,
        request_size: int = 256,
        response_size: int = 256,
        *,
        cycle_time_ms: int = 10,
        move_cycles: int | None = None,
        library: Path | None = None,
    ) -> None:
        if library is not None and not library.is_file():
            raise SdkNotAvailableError(f"SDK simulator library {library} not found")
        self._cycle_time_ms = cycle_time_ms
        self._move_cycles = move_cycles
        self._library = library
        self.on_log: Callable[[SdkLog], None] | None = None
        self.sim = self._new_simulator()
        self.response_size = response_size
        self._connection = 0
        self._lock = threading.Lock()
        # LifeSign PLC -> RC (header byte 1, low nibble) of the current connection
        self.last_number: int | None = None
        self.number_gaps = 0  # telegrams missing between two received ones
        self.number_repeats = 0  # telegrams with the same number as the one before
        self.gateway = PlcGatewaySimulator(self._handle, request_size, response_size, host=host, port=port)

    def _new_simulator(self) -> SdkSimulator:
        sim = SdkSimulator(cycle_time_ms=self._cycle_time_ms, library=self._library)
        if self._move_cycles is not None:
            sim.set_move_cycles(self._move_cycles)
        sim.on_log = self.on_log
        return sim

    @property
    def address(self) -> tuple[str, int]:
        return self.gateway.address

    @property
    def telegrams(self) -> int:
        return self.gateway.requests

    @property
    def connections(self) -> int:
        return self.gateway.connections

    def _handle(self, telegram: bytes) -> bytes:
        with self._lock:
            if self.gateway.connections != self._connection:  # new PLC connection: restart the RC
                self._connection = self.gateway.connections
                self.last_number = None
                self.number_gaps = self.number_repeats = 0
                if self._connection > 1:
                    # a new simulator: SdkSimulator.reset() does not bring the RI back to the
                    # initial state, the next initialization of the RobotTask would time out
                    self.sim.close()
                    self.sim = self._new_simulator()
            self._check_number(telegram)
            return self.sim.exchange(telegram, self.response_size)

    def _check_number(self, telegram: bytes) -> None:
        """Gaps and repeats of the LifeSign PLC -> RC (header byte 1, low nibble 1..15): the
        PLC counts it once per RobotTask cycle, so every telegram must carry the next value."""
        if len(telegram) < 2:
            return
        number = telegram[1] & 0x0F
        if number == 0:  # not initialized yet
            self.last_number = None
            return
        if self.last_number is not None:
            diff = (number - self.last_number) % 15
            if diff == 0:
                self.number_repeats += 1
            elif diff > 1:
                self.number_gaps += diff - 1
        self.last_number = number

    def start(self) -> Self:
        self.gateway.start()
        return self

    def close(self) -> None:
        self.gateway.stop()
        self.sim.close()

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.close()

    def status(self) -> str:
        joints = self.sim.joints
        return (
            f"connections {self.connections}  telegrams {self.telegrams}  "
            f"enabled {self.sim.enabled!s:5}  override {self.sim.override:5.1f}  "
            "J1..J3 "
            + " ".join(f"{j:7.2f}" for j in joints[:3])
            + f"  PLC lifesign {self.last_number}  gaps {self.number_gaps}  repeats {self.number_repeats}"
        )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1", help="address to listen on (0.0.0.0: all interfaces)")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--length", type=int, default=256, help="telegram length in both directions [bytes]")
    ap.add_argument("--request-length", type=int, help="PLC->RC telegram length (default: --length)")
    ap.add_argument("--response-length", type=int, help="RC->PLC telegram length (default: --length)")
    ap.add_argument("--cycle-ms", type=int, default=10, help="cycle time of the simulated RC [ms]")
    ap.add_argument("--move-cycles", type=int, help="duration of a simulated motion [cycles]")
    ap.add_argument("--lib", type=Path, help="SDK simulator library (default: SRCI_SDK_SIM_LIB / SRCI SDK)")
    ap.add_argument("--status", type=float, default=1.0, help="status line every n seconds (0: off)")
    ap.add_argument("--log", action="store_true", help="print the log messages of the SDK")
    args = ap.parse_args(argv)

    try:
        server = SdkServer(
            args.host,
            args.port,
            args.request_length or args.length,
            args.response_length or args.length,
            cycle_time_ms=args.cycle_ms,
            move_cycles=args.move_cycles,
            library=args.lib,
        )
    except SdkNotAvailableError as exc:
        print(f"SDK simulator not available: {exc}", file=sys.stderr)
        return 2
    if args.log:

        def show(entry: SdkLog) -> None:
            print(f"  SDK severity {entry.severity:2} code 16#{entry.error_code:04X}: {entry.text}")

        server.on_log = server.sim.on_log = show
    with server:
        host, port = server.address
        print(f"SRCI SDK server (SDK {server.sim.sdk_version}) on {host}:{port}, telegrams "
              f"{args.request_length or args.length}/{args.response_length or args.length} bytes - Ctrl+C ends")  # fmt: skip
        try:
            while True:
                time.sleep(args.status or 3600.0)
                if args.status:
                    print(server.status(), flush=True)
                for error in server.gateway.errors:
                    print(f"  error: {error}", file=sys.stderr)
                server.gateway.errors.clear()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
