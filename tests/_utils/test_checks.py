from firedust.utils.checks import is_unix_timestamp


def test_is_unix_timestamp() -> None:
    # Test valid unix timestamp
    assert is_unix_timestamp(1625097600) is True
    assert is_unix_timestamp(1625097600.5) is True
    assert is_unix_timestamp(0) is True

    # Before 1970
    assert is_unix_timestamp(-1) is False

    # After 2038
    assert is_unix_timestamp(2**31) is False
