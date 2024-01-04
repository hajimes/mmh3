# -*- coding: utf-8 -*-
import sys

import mmh3
from helper import u32_to_s32


def test_hash() -> None:
    assert mmh3.hash("foo") == -156908512

    # Test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    assert mmh3.hash(b"", seed=0) == 0
    assert mmh3.hash(b"", seed=1) == 0x514E28B7
    assert mmh3.hash(b"", seed=u32_to_s32(0xFFFFFFFF)) == u32_to_s32(0x81F16F39)
    assert mmh3.hash(b"\x21\x43\x65\x87", 0) == u32_to_s32(0xF55B516B)
    assert mmh3.hash(b"\x21\x43\x65\x87", u32_to_s32(0x5082EDEE)) == u32_to_s32(
        0x2362F9DE
    )
    assert mmh3.hash(b"\x21\x43\x65", 0) == u32_to_s32(0x7E4A8634)
    assert mmh3.hash(b"\x21\x43", 0) == u32_to_s32(0xA0F7B07A)
    assert mmh3.hash(b"\x21", 0) == u32_to_s32(0x72661CF4)
    assert mmh3.hash(b"\xff\xff\xff\xff", 0) == u32_to_s32(0x76293B50)
    assert mmh3.hash(b"\x00\x00\x00\x00", 0) == u32_to_s32(0x2362F9DE)
    assert mmh3.hash(b"\x00\x00\x00", 0) == u32_to_s32(0x85F0B427)
    assert mmh3.hash(b"\x00\x00", 0) == u32_to_s32(0x30F4C306)
    assert mmh3.hash(b"\x00", 0) == u32_to_s32(0x514E28B7)

    assert mmh3.hash("aaaa", u32_to_s32(0x9747B28C)) == u32_to_s32(0x5A97808A)
    assert mmh3.hash("aaa", u32_to_s32(0x9747B28C)) == u32_to_s32(0x283E0130)
    assert mmh3.hash("aa", u32_to_s32(0x9747B28C)) == u32_to_s32(0x5D211726)
    assert mmh3.hash("a", u32_to_s32(0x9747B28C)) == u32_to_s32(0x7FA09EA6)

    assert mmh3.hash("abcd", u32_to_s32(0x9747B28C)) == u32_to_s32(0xF0478627)
    assert mmh3.hash("abc", u32_to_s32(0x9747B28C)) == u32_to_s32(0xC84A62DD)
    assert mmh3.hash("ab", u32_to_s32(0x9747B28C)) == u32_to_s32(0x74875592)
    assert mmh3.hash("a", u32_to_s32(0x9747B28C)) == u32_to_s32(0x7FA09EA6)

    assert mmh3.hash("Hello, world!", u32_to_s32(0x9747B28C)) == u32_to_s32(0x24884CBA)

    assert mmh3.hash("ππππππππ".encode("utf-8"), u32_to_s32(0x9747B28C)) == u32_to_s32(
        0xD58063C1
    )

    assert mmh3.hash("a" * 256, u32_to_s32(0x9747B28C)) == u32_to_s32(0x37405BDC)

    assert mmh3.hash("abc", 0) == u32_to_s32(0xB3DD93FA)
    assert mmh3.hash(
        "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 0
    ) == u32_to_s32(0xEE925B90)

    assert mmh3.hash(
        "The quick brown fox jumps over the lazy dog", u32_to_s32(0x9747B28C)
    ) == u32_to_s32(0x2FA826CD)

    assert mmh3.hash(
        "The quick brown fox jumps over the lazy dog", u32_to_s32(0x9747B28C)
    ) == u32_to_s32(0x2FA826CD)


def test_hash_unsigned() -> None:
    assert mmh3.hash("foo", signed=False) == 4138058784

    # Test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    assert mmh3.hash(b"", seed=0, signed=False) == 0
    assert mmh3.hash(b"", seed=1, signed=False) == 0x514E28B7
    assert mmh3.hash(b"", seed=0xFFFFFFFF, signed=False) == 0x81F16F39
    assert mmh3.hash(b"\x21\x43\x65\x87", 0, signed=False) == 0xF55B516B
    assert mmh3.hash(b"\x21\x43\x65\x87", 0x5082EDEE, signed=False) == 0x2362F9DE
    assert mmh3.hash(b"\x21\x43\x65", 0, signed=False) == 0x7E4A8634
    assert mmh3.hash(b"\x21\x43", 0, signed=False) == 0xA0F7B07A
    assert mmh3.hash(b"\x21", 0, signed=False) == 0x72661CF4
    assert mmh3.hash(b"\xff\xff\xff\xff", 0, signed=False) == 0x76293B50
    assert mmh3.hash(b"\x00\x00\x00\x00", 0, signed=False) == 0x2362F9DE
    assert mmh3.hash(b"\x00\x00\x00", 0, signed=False) == 0x85F0B427
    assert mmh3.hash(b"\x00\x00", 0, signed=False) == 0x30F4C306
    assert mmh3.hash(b"\x00", 0, signed=False) == 0x514E28B7

    assert mmh3.hash("aaaa", 0x9747B28C, signed=False) == 0x5A97808A
    assert mmh3.hash("aaa", 0x9747B28C, signed=False) == 0x283E0130
    assert mmh3.hash("aa", 0x9747B28C, signed=False) == 0x5D211726
    assert mmh3.hash("a", 0x9747B28C, signed=False) == 0x7FA09EA6

    assert mmh3.hash("abcd", 0x9747B28C, signed=False) == 0xF0478627
    assert mmh3.hash("abc", 0x9747B28C, signed=False) == 0xC84A62DD
    assert mmh3.hash("ab", 0x9747B28C, signed=False) == 0x74875592
    assert mmh3.hash("a", 0x9747B28C, signed=False) == 0x7FA09EA6

    assert mmh3.hash("Hello, world!", 0x9747B28C, signed=False) == 0x24884CBA

    assert mmh3.hash("ππππππππ".encode("utf-8"), 0x9747B28C, signed=False) == 0xD58063C1

    assert mmh3.hash("a" * 256, 0x9747B28C, signed=False) == 0x37405BDC

    assert mmh3.hash("abc", 0, signed=False) == 0xB3DD93FA
    assert (
        mmh3.hash(
            "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 0, signed=False
        )
        == 0xEE925B90
    )

    assert (
        mmh3.hash(
            "The quick brown fox jumps over the lazy dog", 0x9747B28C, signed=False
        )
        == 0x2FA826CD
    )

    assert (
        mmh3.hash(
            "The quick brown fox jumps over the lazy dog", 0x9747B28C, signed=False
        )
        == 0x2FA826CD
    )


def test_hash2() -> None:
    assert mmh3.hash("foo") == -156908512

    # Test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    assert mmh3.hash(b"", seed=0) == 0
    assert mmh3.hash(b"", seed=1) == 0x514E28B7
    assert mmh3.hash(b"", seed=0xFFFFFFFF) == u32_to_s32(0x81F16F39)
    assert mmh3.hash(b"\x21\x43\x65\x87", 0) == u32_to_s32(0xF55B516B)
    assert mmh3.hash(b"\x21\x43\x65\x87", 0x5082EDEE) == u32_to_s32(0x2362F9DE)
    assert mmh3.hash(b"\x21\x43\x65", 0) == u32_to_s32(0x7E4A8634)
    assert mmh3.hash(b"\x21\x43", 0) == u32_to_s32(0xA0F7B07A)
    assert mmh3.hash(b"\x21", 0) == u32_to_s32(0x72661CF4)
    assert mmh3.hash(b"\xff\xff\xff\xff", 0) == u32_to_s32(0x76293B50)
    assert mmh3.hash(b"\x00\x00\x00\x00", 0) == u32_to_s32(0x2362F9DE)
    assert mmh3.hash(b"\x00\x00\x00", 0) == u32_to_s32(0x85F0B427)
    assert mmh3.hash(b"\x00\x00", 0) == u32_to_s32(0x30F4C306)
    assert mmh3.hash(b"\x00", 0) == u32_to_s32(0x514E28B7)

    assert mmh3.hash("aaaa", 0x9747B28C) == u32_to_s32(0x5A97808A)
    assert mmh3.hash("aaa", 0x9747B28C) == u32_to_s32(0x283E0130)
    assert mmh3.hash("aa", 0x9747B28C) == u32_to_s32(0x5D211726)
    assert mmh3.hash("a", 0x9747B28C) == u32_to_s32(0x7FA09EA6)

    assert mmh3.hash("abcd", 0x9747B28C) == u32_to_s32(0xF0478627)
    assert mmh3.hash("abc", 0x9747B28C) == u32_to_s32(0xC84A62DD)
    assert mmh3.hash("ab", 0x9747B28C) == u32_to_s32(0x74875592)
    assert mmh3.hash("a", 0x9747B28C) == u32_to_s32(0x7FA09EA6)

    assert mmh3.hash("Hello, world!", 0x9747B28C) == u32_to_s32(0x24884CBA)

    assert mmh3.hash("ππππππππ".encode("utf-8"), 0x9747B28C) == u32_to_s32(0xD58063C1)

    assert mmh3.hash("a" * 256, 0x9747B28C) == u32_to_s32(0x37405BDC)

    assert mmh3.hash("abc", 0) == u32_to_s32(0xB3DD93FA)
    assert mmh3.hash(
        "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 0
    ) == u32_to_s32(0xEE925B90)

    assert mmh3.hash(
        "The quick brown fox jumps over the lazy dog", 0x9747B28C
    ) == u32_to_s32(0x2FA826CD)


def test_hash_from_buffer() -> None:
    mview = memoryview("foo".encode("utf8"))
    assert mmh3.hash_from_buffer(mview) == -156908512
    assert mmh3.hash_from_buffer(mview, signed=False) == 4138058784


def test_hash_bytes() -> None:
    assert mmh3.hash_bytes("foo") == b"aE\xf5\x01W\x86q\xe2\x87}\xba+\xe4\x87\xaf~"
    assert (
        mmh3.hash_bytes("foo", 0, True)
        == b"aE\xf5\x01W\x86q\xe2\x87}\xba+\xe4\x87\xaf~"
    )

    # Test vectors from https://github.com/PeterScott/murmur3/blob/master/test.c
    assert mmh3.hash_bytes("Hello, world!", 123, x64arch=False) == (
        0x9E37C886A41621625A1AACD761C9129E
    ).to_bytes(16, "little")
    assert mmh3.hash_bytes("", 123, x64arch=False) == (
        0x26F3E79926F3E79926F3E799FEDC5245
    ).to_bytes(16, "little")
    # TODO


def test_hash64() -> None:
    assert mmh3.hash64("foo") == (-2129773440516405919, 9128664383759220103)
    assert mmh3.hash64("foo", signed=False) == (
        16316970633193145697,
        9128664383759220103,
    )

    assert mmh3.hash64("The quick brown fox jumps over the lazy dog", 0x9747B28C) == (
        8325606756057297185,
        -484854449282476315,
    )
    assert mmh3.hash64(
        "The quick brown fox jumps over the lazy dog", 0x9747B28C, signed=False
    ) == (
        8325606756057297185,
        17961889624427075301,
    )
    assert mmh3.hash64("foo", signed=False, x64arch=True) == (
        16316970633193145697,
        9128664383759220103,
    )

    # Test vectors from https://github.com/PeterScott/murmur3/blob/master/test.c
    assert mmh3.hash64("Hello, world!", 123, signed=False, x64arch=False) == (
        0x5A1AACD761C9129E,
        0x9E37C886A4162162,
    )

    assert mmh3.hash64("", 123, False, False) == (
        0x26F3E799FEDC5245,
        0x26F3E79926F3E799,
    )


def test_hash128() -> None:
    assert mmh3.hash128("foo") == 168394135621993849475852668931176482145
    assert mmh3.hash128("foo", 42) == 215966891540331383248189432718888555506
    assert (
        mmh3.hash128("foo", 42, signed=False) == 215966891540331383248189432718888555506
    )
    assert (
        mmh3.hash128("foo", 42, signed=True) == -124315475380607080215185174712879655950
    )
    # Test vectors from https://github.com/PeterScott/murmur3/blob/master/test.c
    assert (
        mmh3.hash128("Hello, world!", 123, signed=False, x64arch=False)
        == 0x9E37C886A41621625A1AACD761C9129E
    )
    assert mmh3.hash128("", 123, False, False) == 0x26F3E79926F3E79926F3E799FEDC5245


def test_64bit() -> None:
    if sys.maxsize < (1 << 32):  # Skip this test under 32-bit environments
        return
    a = bytes(2**32 + 1)
    assert mmh3.hash(a) == -1710109261
    assert (
        mmh3.hash_bytes(a) == b"\x821\x93\x0c\xe7\xa8\x02\x9d\xe5 \xa6\xf9\xeb8\xd6\x0e"
    )
