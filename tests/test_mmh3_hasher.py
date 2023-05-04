# -*- coding: utf-8 -*-
import mmh3
from helper import u32_to_s32


def test_hasher32_basic_ops() -> None:
    hasher = mmh3.mmh3_32()
    assert hasher.digest_size == 8


def test_hasher32_sintdigest() -> None:
    hasher = mmh3.mmh3_32()
    hasher.update(b"foo")
    assert hasher.sintdigest() == -156908512

    # Test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    hasher = mmh3.mmh3_32()
    hasher.update(b"")
    assert hasher.sintdigest() == 0

    hasher = mmh3.mmh3_32(seed=1)
    hasher.update(b"")
    assert hasher.sintdigest() == 0x514E28B7

    hasher = mmh3.mmh3_32()
    hasher.update(b"\x21\x43")
    hasher.update(b"\x65")
    assert hasher.sintdigest() == u32_to_s32(0x7E4A8634)

    hasher = mmh3.mmh3_32()
    hasher.update(b"\x21\x43\x65\x87")
    assert hasher.sintdigest() == u32_to_s32(0xF55B516B)

    hasher = mmh3.mmh3_32()
    hasher.update(b"\x21\x43")
    hasher.update(b"\x65\x87")
    assert hasher.sintdigest() == u32_to_s32(0xF55B516B)

    hasher = mmh3.mmh3_32(seed=0x9747B28C)
    hasher.update(b"Hello, world!")
    assert hasher.sintdigest() == u32_to_s32(0x24884CBA)

    hasher = mmh3.mmh3_32(seed=0x9747B28C)
    hasher.update(b"Hello,")
    hasher.update(b" world!")
    assert hasher.sintdigest() == u32_to_s32(0x24884CBA)

    hasher = mmh3.mmh3_32(seed=0x9747B28C)
    hasher.update(b"The quick brown fo")
    hasher.update(b"x jumps over the lazy dog")
    assert hasher.sintdigest() == u32_to_s32(0x2FA826CD)


def test_hasher32_uintdigest() -> None:
    hasher = mmh3.mmh3_32()
    hasher.update(b"foo")
    assert hasher.uintdigest() == 4138058784

    # Test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    hasher = mmh3.mmh3_32()
    hasher.update(b"")
    assert hasher.uintdigest() == 0

    hasher = mmh3.mmh3_32(seed=1)
    hasher.update(b"")
    assert hasher.uintdigest() == 0x514E28B7

    hasher = mmh3.mmh3_32()
    hasher.update(b"\x21\x43")
    hasher.update(b"\x65")
    assert hasher.uintdigest() == 0x7E4A8634

    hasher = mmh3.mmh3_32()
    hasher.update(b"\x21\x43\x65\x87")
    assert hasher.uintdigest() == 0xF55B516B

    hasher = mmh3.mmh3_32()
    hasher.update(b"\x21\x43")
    hasher.update(b"\x65\x87")
    assert hasher.uintdigest() == 0xF55B516B

    hasher = mmh3.mmh3_32(seed=0x9747B28C)
    hasher.update(b"Hello, world!")
    assert hasher.uintdigest() == 0x24884CBA

    hasher = mmh3.mmh3_32(seed=0x9747B28C)
    hasher.update(b"Hello,")
    hasher.update(b" world!")
    assert hasher.uintdigest() == 0x24884CBA

    hasher = mmh3.mmh3_32(seed=0x9747B28C)
    hasher.update(b"The quick brown fo")
    hasher.update(b"x jumps over the lazy dog")
    assert hasher.uintdigest() == 0x2FA826CD
