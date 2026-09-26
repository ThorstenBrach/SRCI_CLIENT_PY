import srci


def test_version_and_profile() -> None:
    assert srci.__version__
    assert srci.SRCI_PROFILE_VERSION == "1.5.9"
