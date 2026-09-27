# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.sim.sdk
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    SRCI SDK simulator (SDK in the loop) via ctypes.
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

"""SRCI SDK simulator (SDK in the loop) via ctypes.

The SRCI SDK is licensed and **not** part of this repository. It is built locally
together with a simulated robot (``srci_py_harness`` in the private SDK folder) to a
shared library ``srci_sdk_sim`` (.dll/.so/.dylib). This module only loads it.

Search order for the library:

1. environment variable ``SRCI_SDK_SIM_LIB`` (path of the library file)
2. environment variable ``SRCI_SDK_DIR`` -> ``<dir>/srci_py_harness/bin/``
3. ``../SRCI SDK/srci_py_harness/bin/`` next to this repository (default layout)
"""

from __future__ import annotations

import ctypes
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Self

from srci.transport.loopback import LoopbackTransport

__all__ = [
    "SdkLog",
    "SdkNotAvailableError",
    "SdkSimulator",
    "SdkStates",
    "find_sdk_library",
    "sdk_transport",
]

API_VERSION = 4  # 2: srci_sim_layout, 3: generated commands (C-003), 4: command errors
MAX_TELEGRAM_SIZE = 512
REPO_ROOT = Path(__file__).resolve().parents[3]


class SdkNotAvailableError(RuntimeError):
    """The SDK simulator library was not found (it has to be built locally)."""


def _library_name() -> str:
    if sys.platform == "win32":
        return "srci_sdk_sim.dll"
    if sys.platform == "darwin":
        return "srci_sdk_sim.dylib"
    return "srci_sdk_sim.so"


def find_sdk_library() -> Path:
    candidates: list[Path] = []
    if lib := os.environ.get("SRCI_SDK_SIM_LIB"):
        candidates.append(Path(lib))
    if sdk_dir := os.environ.get("SRCI_SDK_DIR"):
        candidates.append(Path(sdk_dir) / "srci_py_harness" / "bin" / _library_name())
    candidates.append(REPO_ROOT.parent / "SRCI SDK" / "srci_py_harness" / "bin" / _library_name())
    for path in candidates:
        if path.is_file():
            return path
    raise SdkNotAvailableError(
        "SRCI SDK simulator library not found (build it in 'SRCI SDK/srci_py_harness', "
        "or set SRCI_SDK_SIM_LIB / SRCI_SDK_DIR). Searched: " + ", ".join(str(p) for p in candidates)
    )


class _States(ctypes.Structure):
    _fields_ = [
        ("valid", ctypes.c_int),
        ("ri_state", ctypes.c_int),
        ("ra_power_state", ctypes.c_int),
        ("ra_sequence_state", ctypes.c_int),
        ("operation_mode", ctypes.c_int),
        ("is_moving", ctypes.c_int),
        ("error_pending", ctypes.c_int),
    ]


_LOG_CB = ctypes.CFUNCTYPE(
    None, ctypes.c_int, ctypes.c_int, ctypes.c_uint32, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p
)


@dataclass(frozen=True)
class SdkLog:
    severity: int  # SrciApiTypes::Severity (Debug 4, Info 5, Warning 20, Error 28, Fatal 29)
    msg_type: int  # RI 1, RC 2, RA 3, CMD 4, Internal 5
    error_code: int
    layer: int  # Application 1, CmdManagement 2, Transport 3, Network 4, Firmware 5
    text: str


@dataclass(frozen=True)
class SdkStates:
    """States the SDK reports to the robot (``provideInterpreterStates``)."""

    valid: bool
    ri_state: int  # 0 not initialized, 71 initialized, 72 synchronized
    ra_power_state: int  # 0 not enabled, 1 enabling, 2 enabled, 3 disabling
    ra_sequence_state: int  # 91 idle, 92 executing, 93 interrupt active, ...
    operation_mode: int
    is_moving: bool
    error_pending: bool


_lib_cache: dict[Path, ctypes.CDLL] = {}


def _load(path: Path) -> ctypes.CDLL:
    if path in _lib_cache:
        return _lib_cache[path]
    lib = ctypes.CDLL(str(path))
    lib.srci_sim_api_version.restype = ctypes.c_int
    lib.srci_sim_sdk_version.restype = ctypes.c_char_p
    lib.srci_sim_create.argtypes = [ctypes.c_uint16]
    lib.srci_sim_create.restype = ctypes.c_void_p
    lib.srci_sim_destroy.argtypes = [ctypes.c_void_p]
    lib.srci_sim_exchange.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_size_t,
        ctypes.c_void_p,
        ctypes.c_size_t,
    ]
    lib.srci_sim_exchange.restype = ctypes.c_int
    lib.srci_sim_last_error.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    lib.srci_sim_last_error.restype = ctypes.c_size_t
    lib.srci_sim_set_log_callback.argtypes = [ctypes.c_void_p, _LOG_CB, ctypes.c_void_p]
    lib.srci_sim_set_move_cycles.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.srci_sim_set_motion_error.argtypes = [ctypes.c_void_p, ctypes.c_uint16]
    lib.srci_sim_set_fail_enable.argtypes = [ctypes.c_void_p, ctypes.c_int]
    lib.srci_sim_get_joints.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
    lib.srci_sim_set_joints.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
    lib.srci_sim_is_enabled.argtypes = [ctypes.c_void_p]
    lib.srci_sim_is_enabled.restype = ctypes.c_int
    lib.srci_sim_get_override.argtypes = [ctypes.c_void_p]
    lib.srci_sim_get_override.restype = ctypes.c_double
    lib.srci_sim_get_states.argtypes = [ctypes.c_void_p, ctypes.POINTER(_States)]
    lib.srci_sim_reset.argtypes = [ctypes.c_void_p]
    lib.srci_sim_layout.argtypes = [ctypes.c_int, ctypes.c_uint16, ctypes.c_void_p, ctypes.c_size_t]
    lib.srci_sim_layout.restype = ctypes.c_int
    lib.srci_sim_last_command.argtypes = [ctypes.c_void_p, ctypes.c_uint16, ctypes.c_char_p, ctypes.c_size_t]
    lib.srci_sim_last_command.restype = ctypes.c_size_t
    lib.srci_sim_set_response_value.argtypes = [
        ctypes.c_void_p,
        ctypes.c_uint16,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    lib.srci_sim_clear_response_values.argtypes = [ctypes.c_void_p]
    lib.srci_sim_set_command_error.argtypes = [ctypes.c_void_p, ctypes.c_uint16, ctypes.c_uint16]
    lib.srci_sim_set_all_functions_supported.argtypes = [ctypes.c_void_p, ctypes.c_int]
    version = lib.srci_sim_api_version()
    if version != API_VERSION:
        raise SdkNotAvailableError(
            f"SDK simulator API version {version}, expected {API_VERSION} - rebuild it"
        )
    _lib_cache[path] = lib
    return lib


def layout_pattern(index: int) -> int:
    """Byte ``index`` of the pattern of :func:`sdk_layout` (host byte order)."""
    return 0x41 + (index * 7) % 60


def sdk_layout(cmd_type: int, response: bool, library: Path | None = None) -> bytes | None:
    """CMD/RSP structure of the SDK for ``cmd_type``, filled with :func:`layout_pattern` and
    converted to wire byte order like the SDK does it (multi-byte fields reversed).

    ``None``: the SDK has no structure for it (only the header is used)."""
    lib = _load(library or find_sdk_library())
    out = ctypes.create_string_buffer(MAX_TELEGRAM_SIZE)
    size = lib.srci_sim_layout(1 if response else 0, cmd_type, out, len(out))
    if size < 0:
        raise RuntimeError(f"srci_sim_layout({cmd_type}) failed")
    return out.raw[:size] if size else None


def _last_error(lib: ctypes.CDLL) -> str:
    buf = ctypes.create_string_buffer(1024)
    lib.srci_sim_last_error(buf, len(buf))
    return buf.value.decode("utf-8", errors="replace")


class SdkSimulator:
    """SRCI SDK (robot controller side) with a simulated robot.

    ``exchange(telegram)`` performs one lockstep cycle: the robot simulation advances by
    one tick, then the SDK processes the PLC->RC telegram and returns the RC->PLC telegram.
    """

    def __init__(self, cycle_time_ms: int = 10, library: Path | None = None) -> None:
        self.library = library or find_sdk_library()
        self._lib = _load(self.library)
        handle = self._lib.srci_sim_create(cycle_time_ms)
        if not handle:
            raise RuntimeError(_last_error(self._lib))
        self._handle: int | None = handle
        self.logs: list[SdkLog] = []
        self.on_log: Callable[[SdkLog], None] | None = None
        self._log_cb = _LOG_CB(self._receive_log)  # keep a reference as long as the simulator lives
        self._lib.srci_sim_set_log_callback(self._handle, self._log_cb, None)
        self.cycles = 0

    # ------------------------------------------------------------------ lifecycle

    @property
    def sdk_version(self) -> str:
        value: bytes = self._lib.srci_sim_sdk_version()
        return value.decode()

    def close(self) -> None:
        if getattr(self, "_handle", None) is not None:  # also after a failed __init__
            self._lib.srci_sim_destroy(self._handle)
            self._handle = None

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def _h(self) -> int:
        if self._handle is None:
            raise RuntimeError("SDK simulator was closed")
        return self._handle

    # ------------------------------------------------------------------ cycle

    def exchange(self, telegram: bytes | bytearray, response_size: int) -> bytes:
        if len(telegram) > MAX_TELEGRAM_SIZE or response_size > MAX_TELEGRAM_SIZE:
            raise ValueError(f"telegrams are limited to {MAX_TELEGRAM_SIZE} bytes by the SDK")
        out = ctypes.create_string_buffer(response_size)
        rc = self._lib.srci_sim_exchange(self._h(), bytes(telegram), len(telegram), out, response_size)
        if rc != 0:
            raise RuntimeError(_last_error(self._lib))
        self.cycles += 1
        return out.raw

    def reset(self) -> None:
        self._lib.srci_sim_reset(self._h())

    # ------------------------------------------------------------------ robot simulation

    @property
    def enabled(self) -> bool:
        return bool(self._lib.srci_sim_is_enabled(self._h()))

    @property
    def override(self) -> float:
        value: float = self._lib.srci_sim_get_override(self._h())
        return value

    @property
    def joints(self) -> list[float]:
        arr = (ctypes.c_double * 12)()
        self._lib.srci_sim_get_joints(self._h(), arr)
        return list(arr)

    @joints.setter
    def joints(self, values: list[float]) -> None:
        if len(values) != 12:
            raise ValueError("12 joint values (J1..J6, E1..E6) expected")
        self._lib.srci_sim_set_joints(self._h(), (ctypes.c_double * 12)(*values))

    def set_move_cycles(self, cycles: int) -> None:
        """Duration of a move command in simulation cycles."""
        self._lib.srci_sim_set_move_cycles(self._h(), cycles)

    def set_motion_error(self, code: int) -> None:
        """Inject a motion error (e.g. 0x6C02), 0 clears it."""
        self._lib.srci_sim_set_motion_error(self._h(), code)

    def set_fail_enable(self, fail: bool) -> None:
        self._lib.srci_sim_set_fail_enable(self._h(), int(fail))

    # ------------------------------------------------------------------ bilateral tests

    def last_command(self, cmd_type: int) -> dict[str, str] | None:
        """Fields of the last command of ``cmd_type`` as the SDK decoded them (payload tables of
        the specification, generated into the harness): ``{"ToolNo": "3", ...}``."""
        size = self._lib.srci_sim_last_command(self._h(), cmd_type, None, 0)
        if size == 0:
            return None
        buf = ctypes.create_string_buffer(size)
        self._lib.srci_sim_last_command(self._h(), cmd_type, buf, size)
        text = buf.value.decode("latin-1")
        return dict(line.split("=", 1) for line in text.splitlines() if "=" in line)

    def set_response(self, cmd_type: int, values: dict[str, object]) -> None:
        """Values of response fields (names of the specification, e.g. ``"Values[0]"``,
        ``"IntValue_1"``) for the commands the SDK does not implement itself; the other
        fields of the response are 0."""
        for name, value in values.items():
            text = str(int(value)) if isinstance(value, bool) else str(value)
            self._lib.srci_sim_set_response_value(self._h(), cmd_type, name.encode(), text.encode("latin-1"))

    def set_command_error(self, cmd_type: int, error_code: int) -> None:
        """Commands of ``cmd_type`` (not implemented by the SDK itself) are answered with
        ``error_code`` (0: normal answer again)."""
        self._lib.srci_sim_set_command_error(self._h(), cmd_type, error_code)

    def clear_responses(self) -> None:
        self._lib.srci_sim_clear_response_values(self._h())

    def set_all_functions_supported(self, supported: bool) -> None:
        """ReadRobotData: all functions (default) or only those of the original SDK."""
        self._lib.srci_sim_set_all_functions_supported(self._h(), 1 if supported else 0)

    @property
    def states(self) -> SdkStates:
        s = _States()
        self._lib.srci_sim_get_states(self._h(), ctypes.byref(s))
        return SdkStates(
            bool(s.valid),
            s.ri_state,
            s.ra_power_state,
            s.ra_sequence_state,
            s.operation_mode,
            bool(s.is_moving),
            bool(s.error_pending),
        )

    def _receive_log(
        self, severity: int, msg_type: int, error_code: int, layer: int, text: bytes | None, user: int | None
    ) -> None:
        entry = SdkLog(severity, msg_type, error_code, layer, (text or b"").decode("utf-8", errors="replace"))
        self.logs.append(entry)
        if self.on_log is not None:
            self.on_log(entry)


def sdk_transport(sim: SdkSimulator, send_size: int, recv_size: int) -> LoopbackTransport:
    """In-process transport to the SDK simulator (lockstep, deterministic)."""
    return LoopbackTransport(lambda telegram: sim.exchange(telegram, recv_size), send_size, recv_size)
