# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.conftest
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Common pytest configuration.
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
