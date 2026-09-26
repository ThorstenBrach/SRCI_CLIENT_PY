"""Common pytest configuration.

``SRCI_REQUIRE_SDK=1`` (CI job "sdk"): the SDK simulator library must be available - the SDK
tests fail instead of being skipped silently (e.g. after a failed or forgotten build).
"""

from __future__ import annotations

import os

import pytest


def pytest_sessionstart(session: pytest.Session) -> None:
    if os.environ.get("SRCI_REQUIRE_SDK", "") not in ("", "0"):
        from srci.sim.sdk import SdkNotAvailableError, find_sdk_library

        try:
            find_sdk_library()
        except SdkNotAvailableError as exc:
            raise pytest.UsageError(f"SRCI_REQUIRE_SDK is set, but {exc}") from None
