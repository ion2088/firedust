def is_unix_timestamp(timestamp: int | float) -> bool:
    """
    Check if the provided integer is a valid UNIX timestamp.

    UNIX timestamps are typically in the range from 0 to 2**31 - 1,
    covering dates from 1970-01-01 to 2038-01-19.

    Source: https://www.unixtimestamp.com/

    Args:
        timestamp (int): The integer to check.

    Returns:
        bool: True if the integer is a valid UNIX timestamp, False otherwise.
    """

    MIN_UNIX_TIMESTAMP = 0  # 1 January 1970
    MAX_UNIX_TIMESTAMP = 2**31 - 1  # 19 January 2038 for a 32-bit signed integer
    return MIN_UNIX_TIMESTAMP <= timestamp <= MAX_UNIX_TIMESTAMP
