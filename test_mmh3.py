# -*- coding: utf-8 -*-
import mmh3

# see also https://stackoverflow.com/a/1375939
def u32_to_s32(v):
    if(v & 0x80000000):
        return -0x100000000 + v
    else:
        return v

# Note that MurmurHash3 is endian-sensitive.
# In big-endian environments, these tests may fail.
def test_hash_value():
    assert mmh3.hash('foo') == -156908512
    
    # Several test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    assert mmh3.hash(b'', seed=0) == 0
    assert mmh3.hash(b'', seed=1) == 0x514E28B7
    assert mmh3.hash(b'', seed=u32_to_s32(0xffffffff)) == u32_to_s32(0x81F16F39)
    assert mmh3.hash(b'\x21\x43\x65\x87', 0) == u32_to_s32(0xF55B516B)
    assert mmh3.hash(b'\x21\x43\x65\x87',
        u32_to_s32(0x5082EDEE)) == u32_to_s32(0x2362F9DE)
    assert mmh3.hash(b'\x21\x43\x65', 0) == u32_to_s32(0x7E4A8634)
    assert mmh3.hash(b'\x21\x43', 0) == u32_to_s32(0xA0F7B07A)
    assert mmh3.hash(b'\x21', 0) == u32_to_s32(0x72661CF4)
    assert mmh3.hash(b'\xff\xff\xff\xff', 0) == u32_to_s32(0x76293B50)
    assert mmh3.hash(b'\x00\x00\x00\x00', 0) == u32_to_s32(0x2362F9DE)
    assert mmh3.hash(b'\x00\x00\x00', 0) == u32_to_s32(0x85F0B427)
    assert mmh3.hash(b'\x00\x00', 0) == u32_to_s32(0x30F4C306)
    assert mmh3.hash(b'\x00', 0) == u32_to_s32(0x514E28B7)
    
    assert mmh3.hash('aaaa', u32_to_s32(0x9747b28c)) == u32_to_s32(0x5A97808A)
    assert mmh3.hash('aaa', u32_to_s32(0x9747b28c)) == u32_to_s32(0x283E0130)
    assert mmh3.hash('aa', u32_to_s32(0x9747b28c)) == u32_to_s32(0x5D211726)
    assert mmh3.hash('a', u32_to_s32(0x9747b28c)) == u32_to_s32(0x7FA09EA6)

    assert mmh3.hash('abcd', u32_to_s32(0x9747b28c)) == u32_to_s32(0xF0478627)
    assert mmh3.hash('abc', u32_to_s32(0x9747b28c)) == u32_to_s32(0xC84A62DD)
    assert mmh3.hash('ab', u32_to_s32(0x9747b28c)) == u32_to_s32(0x74875592)
    assert mmh3.hash('a', u32_to_s32(0x9747b28c)) == u32_to_s32(0x7FA09EA6)

    assert mmh3.hash('Hello, world!',
        u32_to_s32(0x9747b28c)) == u32_to_s32(0x24884CBA)
    
    assert mmh3.hash(u'ππππππππ'.encode('utf-8'),
        u32_to_s32(0x9747b28c)) == u32_to_s32(0xD58063C1)
        
    assert mmh3.hash('a'*256, u32_to_s32(0x9747b28c)) == u32_to_s32(0x37405BDC)

    assert mmh3.hash('abc', 0) == u32_to_s32(0xB3DD93FA)
    assert mmh3.hash('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
        0) == u32_to_s32(0xEE925B90)

    assert mmh3.hash('The quick brown fox jumps over the lazy dog',
        u32_to_s32(0x9747b28c)) == u32_to_s32(0x2FA826CD)