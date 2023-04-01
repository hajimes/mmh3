# to use list, tuple, dict ... in Python 3.7 and 3.8
from __future__ import annotations

from typing import Union, Protocol


class IntArrayLike(Protocol):
    def __getitem__(self, index) -> int: ...

Hashable = Union[str, bytes, bytearray, memoryview, IntArrayLike]

def hash(key: Hashable, seed: int = 0, signed: bool = True) -> int: ...

def hash_from_buffer(key: Hashable, seed: int = 0, signed: bool = True) -> int: ...

def hash64(key: Hashable, seed: int = 0, signed: bool = True) -> (int, int): ...

def hash128(key: Hashable, seed: int = 0, signed: bool = True) -> int: ...

def hash_bytes(key: Hashable, seed: int = 0, signed: bool = True) -> bytes: ...