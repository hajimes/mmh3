import mmh3

# Note that MurmurHash3 is endian-sensitive.
# In big-endian environments, these tests may fail.
def test_hash_value():
    assert mmh3.hash('foo') == -156908512