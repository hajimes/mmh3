import mmh3


def test_function_docstrings():
    assert "__doc__" in dir(mmh3.hash)
    assert mmh3.hash.__doc__.startswith("hash(key[, seed=0, signed=True])")

    assert "__doc__" in dir(mmh3.hash_from_buffer)
    assert mmh3.hash_from_buffer.__doc__.startswith(
        "hash_from_buffer(key[, seed=0, signed=True]) ->"
    )

    assert "__doc__" in dir(mmh3.hash64)
    assert mmh3.hash64.__doc__.startswith(
        "hash64(key[, seed=0, x64arch=True, signed=True]) ->"
    )

    assert "__doc__" in dir(mmh3.hash128)
    assert mmh3.hash128.__doc__.startswith(
        "hash128(key[, seed=0, x64arch=True, signed=False]])"
    )

    assert "__doc__" in dir(mmh3.hash_bytes)
    assert mmh3.hash_bytes.__doc__.startswith(
        "hash_bytes(key[, seed=0, x64arch=True]) -> bytes"
    )


def test_module_docstring():
    assert "__doc__" in dir(mmh3)
    assert mmh3.__doc__.startswith("mmh3 is a Python front-end to MurmurHash3")
