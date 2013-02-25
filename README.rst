mmh3
====

Python wrapper for MurmurHash (MurmurHash3), a set of fast and robust hash functions.

mmh3 2.2 supports both Python 2.7 and 3.x.

Usage
-----

Sample Usage::

    >>> import mmh3
    >>> mmh3.hash('foo') # 32 bit signed int
    -156908512
    >>> mmh3.hash64('foo') # two 64 bit signed ints
    (-2129773440516405919, 9128664383759220103)
    >>> mmh3.hash_bytes('foo') # 128 bit value as bytes
    'aE\xf5\x01W\x86q\xe2\x87}\xba+\xe4\x87\xaf~'
    >>> mmh3.hash('foo', 42) # uses 42 for its seed
    -1322301282

hash64 and hash_bytes have the third argument for architecture optimization. Use True for x64 and False for x86 (default: True).::

    >>> mmh3.hash64('foo', 42, True) 
    (-840311307571801102, -6739155424061121879)

Changes
=======
2.2 (2013-03-03)
----------------
* Improve portability to support systems with old gcc (version < 4.4) such as CentOS/RHEL 5.x. (Commit from Micha Gorelick. Thanks!)

2.1 (2013-02-25)
----------------

* Add `__version__` constant. Check if it exists when the following revision matters for your application.
* Incorporate the revision r147, which includes robustness improvement and minor tweaks.

Beware that due to this revision, **the result of 32-bit version of 2.1 is NOT the same as that of 2.0**. E.g.,::

    >>> mmh3.hash('foo') # in mmh3 2.0
    -292180858
    >>> mmh3.hash('foo') # in mmh3 2.1
    -156908512

The results of hash64 and hash_bytes remain unchanged. Austin Appleby, the author of Murmurhash, ensured this revision was the final modification to MurmurHash3's results and any future changes would be to improve performance only.

License
=======

Public Domain

Authors
=======

MurmurHash3 was created by Austin Appleby

* http://code.google.com/p/smhasher/

Modified by Hajime Senuma

* http://pypi.python.org/pypi/mmh3
* http://github.com/hajimes/mmh3
