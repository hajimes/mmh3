import mmh3


# Note that MurmurHash3 is endian-sensitive.
# In big-endian environments, these tests may fail.
def test_hash_value():
    assert mmh3.hash('foo') == -156908512
    
    # Several test vectors devised by Ian Boyd
    # https://stackoverflow.com/a/31929528
    assert mmh3.hash('', seed=0) == 0
    assert mmh3.hash('', seed=1) == 0x514E28B7
    assert mmh3.hash('\0\0\0\0', seed=0) == 0x2362F9DE
    # To be added