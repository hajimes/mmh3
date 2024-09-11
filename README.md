# mmh3

[![Documentation Status](https://readthedocs.org/projects/mmh3/badge/?version=latest)](https://mmh3.readthedocs.io/en/latest/?badge=latest)
[![GitHub Super-Linter](https://github.com/hajimes/mmh3/workflows/Super-Linter/badge.svg?branch=master)](https://github.com/hajimes/mmh3/actions?query=workflow%3ASuper-Linter+branch%3Amaster)
[![Build](https://github.com/hajimes/mmh3/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/hajimes/mmh3/actions/workflows/build.yml?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/mmh3.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/mmh3/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mmh3.svg)](https://pypi.org/project/mmh3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)
[![Total Downloads](https://static.pepy.tech/badge/mmh3)](https://pepy.tech/project/mmh3?versions=*&versions=4.*&versions=3.*&versions=2.*)
[![Recent Downloads](https://static.pepy.tech/badge/mmh3/month)](https://pepy.tech/project/mmh3?versions=*&versions=4.*&versions=3.*&versions=2.*)

`mmh3` is a Python extension for
[MurmurHash (MurmurHash3)](https://en.wikipedia.org/wiki/MurmurHash), a set of
fast and robust non-cryptographic hash functions invented by Austin Appleby.

By combining `mmh3` with probabilistic techniques like
[Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter),
[MinHash](https://en.wikipedia.org/wiki/MinHash), and
[feature hashing](https://en.wikipedia.org/wiki/Feature_hashing), you can
develop high-performance systems in fields such as data mining, machine
learning, and natural language processing.

Another popular use of `mmh3` is to
[calculate favicon hashes](https://gist.github.com/yehgdotnet/b9dfc618108d2f05845c4d8e28c5fc6a),
which are utilized by [Shodan](https://www.shodan.io), the world's first IoT
search engine.

This page provides a quick start guide. For more comprehensive information,
please refer to the [documentation](https://mmh3.readthedocs.io/en/latest/).

## Installation

```shell
pip install mmh3
```

## Usage

### Basic usage

```pycon
>>> import mmh3
>>> mmh3.hash("foo") # returns a 32-bit signed int
-156908512
>>> mmh3.hash("foo", 42) # uses 42 as the seed
-1322301282
>>> mmh3.hash("foo", signed=False) # returns a 32-bit unsigned int
4138058784
```

Other functions:

```pycon
>>> mmh3.hash64("foo") # two 64-bit signed ints using the 128-bit algorithm
(-2129773440516405919, 9128664383759220103)
>>> mmh3.hash64("foo", signed=False) # two 64-bit unsigned ints
(16316970633193145697, 9128664383759220103)
>>> mmh3.hash128("foo", 42) # 128-bit unsigned int
215966891540331383248189432718888555506
>>> mmh3.hash128("foo", 42, signed=True) # 128-bit signed int
-124315475380607080215185174712879655950
>>> mmh3.hash_bytes("foo") # 128-bit value as bytes
'aE\xf5\x01W\x86q\xe2\x87}\xba+\xe4\x87\xaf~'
>>> import numpy as np
>>> a = np.zeros(2 ** 32, dtype=np.int8)
>>> mmh3.hash_bytes(a)
b'V\x8f}\xad\x8eNM\xa84\x07FU\x9c\xc4\xcc\x8e'
```

Beware that `hash64` returns **two** values, because it uses the 128-bit version
of MurmurHash3 as its backend.

`hash_from_buffer` hashes byte-likes without memory copying. The method is
suitable when you hash a large memory-view such as `numpy.ndarray`.

```pycon
>>> mmh3.hash_from_buffer(numpy.random.rand(100))
-2137204694
>>> mmh3.hash_from_buffer(numpy.random.rand(100), signed=False)
3812874078
```

`hash64`, `hash128`, and `hash_bytes` have the third argument for architecture
optimization (keyword arg: `x64arch`). Use True for x64 and False for x86
(default: True):

```pycon
>>> mmh3.hash64("foo", 42, True)
(-840311307571801102, -6739155424061121879)
```

### `hashlib`-style hashers

`mmh3` implements hashers with interfaces similar to those in `hashlib` from
the standard library: `mmh3_32()` for 32-bit hashing, `mmh3_x64_128()` for
128-bit hashing optimized for x64 architectures, and `mmh3_x86_128()` for
128-bit hashing optimized for x86 architectures.

In addition to the standard `digest()` method, each hasher provides
`sintdigest()`, which returns a signed integer, and `uintdigest()`, which
returns an unsigned integer. The 128-bit hashers also include `stupledigest()`
and `utupledigest()`, which return two 64 bit integers.

Please note that as of version 4.1.0, the implementation is still experimental,
and performance may be unsatisfactory (particularly `mmh3_x86_128()`).
Additionally, `hexdigest()` is not supported; use `digest().hex()` instead.

```pycon
>>> import mmh3
>>> hasher = mmh3.mmh3_x64_128(seed=42)
>>> hasher.update(b"foo")
>>> hasher.update(b"bar")
>>> hasher.update("foo") # str inputs are not allowed for hashers
TypeError: Strings must be encoded before hashing
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
>>> hasher.digest()
b'\x82_n\xdd \xac\xb6j\xef\x99\xb1e\xc4\n\xc9\xfd'
>>> hasher.sintdigest() # 128 bit signed int
-2943813934500665152301506963178627198
>>> hasher.uintdigest() # 128 bit unsigned int
337338552986437798311073100468589584258
>>> hasher.stupledigest() # two 64 bit signed ints
(7689522670935629698, -159584473158936081)
>>> hasher.utupledigest() # two 64 bit unsigned ints
(7689522670935629698, 18287159600550615535)
```

## Changelog

See [Changelog](https://mmh3.readthedocs.io/en/latest/changelog_link.html) for the
complete changelog.

### [Unreleased]

#### Added

- Add `digest` functions that accept a non-immutable buffer as input
  and process it without internal copying
  ([#75](https://github.com/hajimes/mmh3/issues/75)).
- Slightly improve the performance of the `hash_bytes` function.
- Add support for Python 3.13.
- Add Read the Docs documentation
  ([#54](https://github.com/hajimes/mmh3/issues/54)).
- (planned: Document benchmark results
  ([#53](https://github.com/hajimes/mmh3/issues/53))).

#### Changed

- Change the format of CHANGELOG.md to conform to the
  [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standard
  ([#63](https://github.com/hajimes/mmh3/issues/63)).

#### Fixed

- Fix a reference leak in the `hash_from_buffer()` function
  ([#75](https://github.com/hajimes/mmh3/issues/75)).
- Fix type hints.

### [4.1.0] - 2024-01-09

#### Added

- Add support for Python 3.12.

#### Fixed

- Fix issues with Bazel by changing the directory structure of the project
  (<https://github.com/hajimes/mmh3/issues/50>).
- Fix incorrect type hints (<https://github.com/hajimes/mmh3/issues/51>).
- Fix invalid results on s390x when the arg `x64arch` of `hash64` or
  `hash_bytes` is set to `False` (<https://github.com/hajimes/mmh3/issues/52>).

### [4.0.1] - 2023-07-14

#### Changed

- Refactor the project structure (<https://github.com/hajimes/mmh3/issues/48>).

#### Fixed

- Fix incorrect type hints.

## License

[MIT](https://github.com/hajimes/mmh3/blob/master/LICENSE), unless otherwise
noted within a file.

## Known Issues

### Different results from other MurmurHash3-based libraries

By default, `mmh3` returns **signed** values for the 32-bit and 64-bit versions
and **unsigned** values for `hash128` due to historical reasons. To get the
desired result, use the `signed` keyword argument.

Starting from version 4.0.0, `mmh3` returns the same values on big-endian
platforms as it does on little-endian ones, whereas the original C++ library is
endian-sensitive. If you need results that comply with the original library on
big-endian systems, please use version 3.\*.

For compatibility with [Google Guava (Java)](https://github.com/google/guava),
see
<https://stackoverflow.com/questions/29932956/murmur3-hash-different-result-between-python-and-java-implementation>.

For compatibility with
[murmur3 (Go)](https://pkg.go.dev/github.com/spaolacci/murmur3), see
<https://github.com/hajimes/mmh3/issues/46>.

### Unexpected results when given non 32-bit seeds

In version 2.4, the type of a seed was changed from a signed 32-bit integer to
an unsigned 32-bit integer. However, the resulting values for signed seeds
remain unchanged from previous versions, as long as they are 32-bit.

```pycon
>>> mmh3.hash("aaaa", -1756908916) # signed representation for 0x9747b28c
1519878282
>>> mmh3.hash("aaaa", 2538058380) # unsigned representation for 0x9747b28c
1519878282
```

Be careful so that these seeds do not exceed 32-bit. Unexpected results may
happen with invalid values.

```pycon
>>> mmh3.hash("foo", 2 ** 33)
-156908512
>>> mmh3.hash("foo", 2 ** 34)
-156908512
```

## Contributing Guidelines

See [Contributing](https://mmh3.readthedocs.io/en/latest/CONTRIBUTING.html).

## Authors

MurmurHash3 was originally developed by Austin Appleby and distributed under
public domain
[https://github.com/aappleby/smhasher](https://github.com/aappleby/smhasher).

Ported and modified for Python by Hajime Senuma.

## External Tutorials

### High-performance computing

The following textbooks and tutorials are great resources for learning how to
use `mmh3` (and other hash algorithms in general) for high-performance computing.

- Chapter 11: _Using Less Ram_ in Micha Gorelick and Ian Ozsvald. 2014. _High
  Performance Python: Practical Performant Programming for Humans_. O'Reilly
  Media. [ISBN: 978-1-4493-6159-4](https://www.amazon.com/dp/1449361595).
  - 2nd edition of the above (2020).
    [ISBN: 978-1492055020](https://www.amazon.com/dp/1492055026).
- Max Burstein. February 2, 2013.
  _[Creating a Simple Bloom Filter](http://www.maxburstein.com/blog/creating-a-simple-bloom-filter/)_.
- Duke University. April 14, 2016.
  _[Efficient storage of data in memory](http://people.duke.edu/~ccc14/sta-663-2016/20B_Big_Data_Structures.html)_.
- Bugra Akyildiz. August 24, 2016.
  _[A Gentle Introduction to Bloom Filter](https://www.kdnuggets.com/2016/08/gentle-introduction-bloom-filter.html)_.
  KDnuggets.

### Internet of things

[Shodan](https://www.shodan.io), the world's first
[IoT](https://en.wikipedia.org/wiki/Internet_of_things) search engine, uses
MurmurHash3 hash values for [favicons](https://en.wikipedia.org/wiki/Favicon)
(icons associated with web pages). [ZoomEye](https://www.zoomeye.org) follows
Shodan's convention.
[Calculating these values with mmh3](https://gist.github.com/yehgdotnet/b9dfc618108d2f05845c4d8e28c5fc6a)
is useful for OSINT and cybersecurity activities.

- Jan Kopriva. April 19, 2021.
  _[Hunting phishing websites with favicon hashes](https://isc.sans.edu/diary/Hunting+phishing+websites+with+favicon+hashes/27326)_.
  SANS Internet Storm Center.
- Nikhil Panwar. May 2, 2022.
  _[Using Favicons to Discover Phishing & Brand Impersonation Websites](https://bolster.ai/blog/how-to-use-favicons-to-find-phishing-websites)_.
  Bolster.
- Faradaysec. July 25, 2022.
  _[Understanding Spring4Shell: How used is it?](https://faradaysec.com/understanding-spring4shell/)_.
  Faraday Security.
- Debjeet. August 2, 2022.
  _[How To Find Assets Using Favicon Hashes](https://payatu.com/blog/favicon-hash/)_.
  Payatu.

## Related Libraries

- <https://github.com/wc-duck/pymmh3>: mmh3 in pure python (Fredrik Kihlander
  and Swapnil Gusani)
- <https://github.com/escherba/python-cityhash>: Python bindings for CityHash
  (Eugene Scherba)
- <https://github.com/veelion/python-farmhash>: Python bindings for FarmHash
  (Veelion Chong)
- <https://github.com/escherba/python-metrohash>: Python bindings for MetroHash
  (Eugene Scherba)
- <https://github.com/ifduyue/python-xxhash>: Python bindings for xxHash (Yue
  Du)

[unreleased]: https://github.com/hajimes/mmh3/compare/v4.1.0...HEAD
[4.1.0]: https://github.com/hajimes/mmh3/compare/v4.0.1...v4.1.0
[4.0.1]: https://github.com/hajimes/mmh3/compare/v4.0.0...v4.0.1
