# -*- coding: utf-8 -*-
import sys

import mmh3
import numpy as np


# see also https://stackoverflow.com/a/1375939
def u32_to_s32(v):
    if v & 0x80000000:
        return -0x100000000 + v
    else:
        return v


# Note that MurmurHash3 is endian-sensitive.
# In big-endian environments, these tests may fail.


def test_hash():
    assert mmh3.hash("foo") == -156908512

    # Several test vectors devised by Ian Boyd
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

    assert mmh3.hash(u"ππππππππ".encode("utf-8"), u32_to_s32(0x9747B28C)) == u32_to_s32(
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


def test_hash_unsigned():
    assert mmh3.hash("foo", signed=False) == 4138058784

    # Several test vectors devised by Ian Boyd
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

    assert (
        mmh3.hash(u"ππππππππ".encode("utf-8"), 0x9747B28C, signed=False) == 0xD58063C1
    )

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


def test_hash2():
    assert mmh3.hash("foo") == -156908512

    # Several test vectors devised by Ian Boyd
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

    assert mmh3.hash(u"ππππππππ".encode("utf-8"), 0x9747B28C) == u32_to_s32(0xD58063C1)

    assert mmh3.hash("a" * 256, 0x9747B28C) == u32_to_s32(0x37405BDC)

    assert mmh3.hash("abc", 0) == u32_to_s32(0xB3DD93FA)
    assert mmh3.hash(
        "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 0
    ) == u32_to_s32(0xEE925B90)

    assert mmh3.hash(
        "The quick brown fox jumps over the lazy dog", 0x9747B28C
    ) == u32_to_s32(0x2FA826CD)


def test_hash_from_buffer():
    mview = memoryview("foo".encode("utf8"))
    assert mmh3.hash_from_buffer(mview) == -156908512
    assert mmh3.hash_from_buffer(mview, signed=False) == 4138058784


def test_hash_bytes():
    assert mmh3.hash_bytes("foo") == b"aE\xf5\x01W\x86q\xe2\x87}\xba+\xe4\x87\xaf~"
    # TODO


def test_hash64():
    assert mmh3.hash64("foo") == (-2129773440516405919, 9128664383759220103)
    assert mmh3.hash64("foo", signed=False) == (
        16316970633193145697,
        9128664383759220103,
    )
    # TODO


def test_hash128():
    assert mmh3.hash128("foo") == 168394135621993849475852668931176482145
    assert mmh3.hash128("foo", 42) == 215966891540331383248189432718888555506
    assert (
        mmh3.hash128("foo", 42, signed=False) == 215966891540331383248189432718888555506
    )
    assert (
        mmh3.hash128("foo", 42, signed=True) == -124315475380607080215185174712879655950
    )
    # TODO


def test_64bit():
    if sys.maxsize < (1 << 32):  # Skip this test under 32-bit environments
        return
    a = np.zeros(2 ** 32, dtype=np.int8)
    assert mmh3.hash(a) == -1988950868
    assert mmh3.hash64(a) == (-6319308327427928234, -8156928649350215884)
    assert mmh3.hash128(a) == 189813591698865711411311444615608766294
    assert mmh3.hash_bytes(a) == b"V\x8f}\xad\x8eNM\xa84\x07FU\x9c\xc4\xcc\x8e"
