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
