# to use list, tuple, dict ... in Python 3.7 and 3.8
from __future__ import annotations

import sys
from typing import Union, final

if sys.version_info >= (3, 12):
    from collections.abc import Buffer
else:
    from _typeshed import ReadableBuffer as Buffer

def hash(key: Union[bytes, str], seed: int = 0, signed: bool = True) -> int: ...
def hash_from_buffer(
    key: Union[Buffer, str], seed: int = 0, signed: bool = True
) -> int: ...
def hash64(
    key: Union[bytes, str], seed: int = 0, x64arch: bool = True, signed: bool = True
) -> tuple[int, int]: ...
def hash128(
    key: Union[bytes, str], seed: int = 0, x64arch: bool = True, signed: bool = False
) -> int: ...
def hash_bytes(
    key: Union[bytes, str], seed: int = 0, x64arch: bool = True
) -> bytes: ...
def mmh3_32_digest(key: Union[Buffer, str], seed: int = 0) -> bytes: ...
def mmh3_32_sintdigest(key: Union[Buffer, str], seed: int = 0) -> int: ...
def mmh3_32_uintdigest(key: Union[Buffer, str], seed: int = 0) -> int: ...
def mmh3_x64_128_digest(key: Union[Buffer, str], seed: int = 0) -> bytes: ...
def mmh3_x64_128_sintdigest(key: Union[Buffer, str], seed: int = 0) -> int: ...
def mmh3_x64_128_uintdigest(key: Union[Buffer, str], seed: int = 0) -> int: ...
def mmh3_x64_128_stupledigest(
    key: Union[Buffer, str], seed: int = 0
) -> tuple[int, int]: ...
def mmh3_x64_128_utupledigest(
    key: Union[Buffer, str], seed: int = 0
) -> tuple[int, int]: ...
def mmh3_x86_128_digest(key: Union[Buffer, str], seed: int = 0) -> bytes: ...
def mmh3_x86_128_sintdigest(key: Union[Buffer, str], seed: int = 0) -> int: ...
def mmh3_x86_128_uintdigest(key: Union[Buffer, str], seed: int = 0) -> int: ...
def mmh3_x86_128_stupledigest(
    key: Union[Buffer, str], seed: int = 0
) -> tuple[int, int]: ...
def mmh3_x86_128_utupledigest(
    key: Union[Buffer, str], seed: int = 0
) -> tuple[int, int]: ...

class Hasher:
    def __init__(self, seed: int = 0) -> None: ...
    def update(self, data: Buffer) -> None: ...
    def digest(self) -> bytes: ...
    def sintdigest(self) -> int: ...
    def uintdigest(self) -> int: ...
    def copy(self) -> Hasher: ...
    @property
    def digest_size(self) -> int: ...
    @property
    def block_size(self) -> int: ...
    @property
    def name(self) -> str: ...

@final
class mmh3_32(Hasher): ...

@final
class mmh3_x64_128(Hasher):
    def stupledigest(self) -> tuple[int, int]: ...
    def utupledigest(self) -> tuple[int, int]: ...

@final
class mmh3_x86_128(Hasher):
    def stupledigest(self) -> tuple[int, int]: ...
    def utupledigest(self) -> tuple[int, int]: ...
