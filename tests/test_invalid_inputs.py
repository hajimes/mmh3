# pylint: disable=missing-module-docstring, missing-function-docstring
# pylint: disable=no-value-for-parameter, too-many-function-args
from typing import no_type_check

import mmh3
import pytest


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


@no_type_check
def test_hash_raises_valueerror() -> None:
    with pytest.raises(ValueError):
        mmh3.hash(b"hello, world", -1)
    with pytest.raises(ValueError):
        mmh3.hash(b"hello, world", 2**32)


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
