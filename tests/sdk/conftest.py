# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.conftest
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    SDK in the loop: tests are skipped if the (private, locally built) SDK simulator is
#    missing.
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

"""SDK in the loop: tests are skipped if the (private, locally built) SDK simulator is missing."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from srci.sim.sdk import SdkNotAvailableError, SdkSimulator, find_sdk_library


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        if "tests/sdk" in item.nodeid.replace("\\", "/"):
            item.add_marker(pytest.mark.sdk)


@pytest.fixture(scope="session")
def sdk_library() -> str:
    try:
        return str(find_sdk_library())
    except SdkNotAvailableError as exc:
        pytest.skip(str(exc))


@pytest.fixture
def sdk(sdk_library: str) -> Iterator[SdkSimulator]:
    with SdkSimulator(cycle_time_ms=10) as sim:
        yield sim
