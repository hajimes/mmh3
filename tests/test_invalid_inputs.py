# pylint: disable=missing-module-docstring, missing-function-docstring
# pylint: disable=no-value-for-parameter, too-many-function-args
from typing import no_type_check

import pytest

import mmh3


@no_type_check
def test_hash_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.hash()
    with pytest.raises(TypeError):
        mmh3.hash(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.hash(b"hello, world", 42, True, 1234)
    with pytest.raises(TypeError):
        mmh3.hash(b"hello, world", seed="42")
    with pytest.raises(TypeError):
        mmh3.hash([1, 2, 3], 42)
    # pylint: disable=redundant-keyword-arg
    with pytest.raises(TypeError):
        mmh3.hash(b"hello, world", key=b"42")


@no_type_check
def test_hash_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.hash(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.hash(b"hello, world", 2**32)


@no_type_check
def test_hash128_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.hash128()
    with pytest.raises(TypeError):
        mmh3.hash128(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.hash128(b"hello, world", 42, True, False, 1234)
    with pytest.raises(TypeError):
        mmh3.hash128(b"hello, world", seed="42")
    with pytest.raises(TypeError):
        mmh3.hash128([1, 2, 3], 42)


@no_type_check
def test_hash128_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.hash128(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.hash128(b"hello, world", 2**32)


@no_type_check
def test_hash64_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.hash64()
    with pytest.raises(TypeError):
        mmh3.hash64(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.hash64(b"hello, world", 42, True, False, 1234)
    with pytest.raises(TypeError):
        mmh3.hash64(b"hello, world", seed="42")
    with pytest.raises(TypeError):
        mmh3.hash64([1, 2, 3], 42)


@no_type_check
def test_hash64_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.hash64(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.hash64(b"hello, world", 2**32)


@no_type_check
def test_hash_bytes_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.hash_bytes()
    with pytest.raises(TypeError):
        mmh3.hash_bytes(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.hash_bytes(b"hello, world", 42, True, 1234)
    with pytest.raises(TypeError):
        mmh3.hash_bytes(b"hello, world", seed="42")
    with pytest.raises(TypeError):
        mmh3.hash_bytes([1, 2, 3], 42)


@no_type_check
def test_hash_bytes_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.hash_bytes(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.hash_bytes(b"hello, world", 2**32)


@no_type_check
def test_hash_from_buffer_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.hash_from_buffer()
    with pytest.raises(TypeError):
        mmh3.hash_from_buffer(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.hash_from_buffer(b"hello, world", 42, True, 1234)
    with pytest.raises(TypeError):
        mmh3.hash_from_buffer(b"hello, world", seed="42")
    with pytest.raises(TypeError):
        mmh3.hash_from_buffer([1, 2, 3], 42)


@no_type_check
def test_hash_from_buffer_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.hash_from_buffer(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.hash_from_buffer(b"hello, world", 2**32)


@no_type_check
def test_mmh3_32_digest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_32_digest()
    with pytest.raises(TypeError):
        mmh3.mmh3_32_digest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_32_digest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_32_digest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_32_digest([1, 2, 3], 42)


@no_type_check
def test_mmh3_32_digest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_32_digest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_32_digest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_32_sintdigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_32_sintdigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_32_sintdigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_32_sintdigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_32_sintdigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_32_sintdigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_32_sintdigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_32_sintdigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_32_sintdigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_32_uintdigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_32_uintdigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_32_uintdigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_32_uintdigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_32_uintdigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_32_uintdigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_32_uintdigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_32_uintdigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_32_uintdigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x64_128_digest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_digest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_digest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_digest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_digest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_digest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x64_128_digest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_digest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_digest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x64_128_sintdigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_sintdigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_sintdigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_sintdigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_sintdigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_sintdigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x64_128_sintdigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_sintdigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_sintdigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x64_128_uintdigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_uintdigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_uintdigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_uintdigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_uintdigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_uintdigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x64_128_uintdigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_uintdigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_uintdigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x64_128_stupledigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_stupledigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_stupledigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_stupledigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_stupledigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_stupledigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x64_128_stupledigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_stupledigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_stupledigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x64_128_utupledigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_utupledigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_utupledigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_utupledigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_utupledigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128_utupledigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x64_128_utupledigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_utupledigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128_utupledigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x86_128_digest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_digest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_digest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_digest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_digest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_digest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x86_128_digest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_digest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_digest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x86_128_sintdigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_sintdigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_sintdigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_sintdigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_sintdigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_sintdigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x86_128_sintdigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_sintdigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_sintdigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x86_128_uintdigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_uintdigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_uintdigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_uintdigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_uintdigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_uintdigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x86_128_uintdigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_uintdigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_uintdigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x86_128_stupledigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_stupledigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_stupledigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_stupledigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_stupledigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_stupledigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x86_128_stupledigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_stupledigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_stupledigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x86_128_utupledigest_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_utupledigest()
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_utupledigest(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_utupledigest("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_utupledigest(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128_utupledigest([1, 2, 3], 42)


@no_type_check
def test_mmh3_x86_128_utupledigest_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_utupledigest(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128_utupledigest(b"hello, world", 2**32)


@no_type_check
def test_mmh3_32_init_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_32(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_32("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_32(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_32([1, 2, 3], 42)


@no_type_check
def test_mmh3_32_init_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_32(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_32(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x64_128_init_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x64_128([1, 2, 3], 42)


@no_type_check
def test_mmh3_x64_128_init_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x64_128(b"hello, world", 2**32)


@no_type_check
def test_mmh3_x86_128_init_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128(b"hello, world", 42, 1234)
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128("hello, world")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128(b"hello, world", "42")
    with pytest.raises(TypeError):
        mmh3.mmh3_x86_128([1, 2, 3], 42)


@no_type_check
def test_mmh3_x86_128_init_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.mmh3_x86_128(b"hello, world", 2**32)


ONE_SHOT_HASHERS = [mmh3.hash, mmh3.hash64, mmh3.hash128, mmh3.hash_bytes]


class _BadBool:  # pylint: disable=too-few-public-methods
    def __bool__(self) -> bool:
        raise ZeroDivisionError("bad __bool__")


@no_type_check
@pytest.mark.parametrize("func", ONE_SHOT_HASHERS)
def test_one_shot_raises_typeerror_on_missing_key(func) -> None:
    with pytest.raises(TypeError, match="missing required argument 'key'"):
        func(seed=1)


@no_type_check
@pytest.mark.parametrize("func", ONE_SHOT_HASHERS)
def test_one_shot_raises_unicodeencodeerror_on_surrogate_key(func) -> None:
    with pytest.raises(UnicodeEncodeError):
        func("\ud800")
    with pytest.raises(UnicodeEncodeError):
        func(key="\ud800")


@no_type_check
@pytest.mark.parametrize("func", ONE_SHOT_HASHERS)
def test_one_shot_raises_unicodeencodeerror_on_surrogate_kwname(func) -> None:
    with pytest.raises(UnicodeEncodeError):
        func(b"hello, world", **{"\ud800": 1})


@no_type_check
@pytest.mark.parametrize(
    "func, nflags",
    [(mmh3.hash, 1), (mmh3.hash64, 2), (mmh3.hash128, 2), (mmh3.hash_bytes, 1)],
)
def test_one_shot_propagates_bool_error(func, nflags) -> None:
    for pos in range(nflags):
        flags = [True] * nflags
        flags[pos] = _BadBool()
        with pytest.raises(ZeroDivisionError):
            func(b"hello, world", 0, *flags)

    names = ["signed"] if func is mmh3.hash else ["x64arch", "signed"][:nflags]
    for name in names:
        with pytest.raises(ZeroDivisionError):
            func(b"hello, world", **{name: _BadBool()})
