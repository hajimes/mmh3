# pylint: disable=missing-module-docstring, missing-function-docstring
# pylint: disable=no-value-for-parameter, too-many-function-args
from typing import no_type_check

import mmh3
import pytest


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
