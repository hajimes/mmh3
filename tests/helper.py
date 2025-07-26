"""Helper functions for tests."""


# see also https://stackoverflow.com/a/1375939
def u32_to_s32(v: int) -> int:
    """Convert unsigned 32-bit integer to signed 32-bit integer.

    Args:
        v: Unsigned 32-bit integer.

    Returns:
        Signed 32-bit representation of the input.
    """
    if v & 0x80000000:
        return -0x100000000 + v
    return v
