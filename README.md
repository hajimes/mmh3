# mmh3

[![Documentation Status](https://readthedocs.org/projects/mmh3/badge/?version=latest)](https://mmh3.readthedocs.io/en/latest/?badge=latest)
[![GitHub Super-Linter](https://github.com/hajimes/mmh3/workflows/Super-Linter/badge.svg?branch=master)](https://github.com/hajimes/mmh3/actions?query=workflow%3ASuper-Linter+branch%3Amaster)
[![Build](https://github.com/hajimes/mmh3/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/hajimes/mmh3/actions/workflows/build.yml?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/mmh3.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/mmh3/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mmh3.svg)](https://pypi.org/project/mmh3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)
[![Total Downloads](https://static.pepy.tech/badge/mmh3)](https://www.pepy.tech/projects/mmh3?versions=*&versions=5.*&versions=4.*&versions=3.*&versions=2.*)
[![Recent Downloads](https://static.pepy.tech/badge/mmh3/month)](https://www.pepy.tech/projects/mmh3?versions=*&versions=5.*&versions=4.*&versions=3.*&versions=2.*)

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
>>> mmh3.hash(b"foo") # returns a 32-bit signed int
-156908512
>>> mmh3.hash("foo") # accepts str (UTF-8 encoded)
-156908512
>>> mmh3.hash(b"foo", 42) # uses 42 as the seed
-1322301282
>>> mmh3.hash(b"foo", 0, False) # returns a 32-bit unsigned int
4138058784
```

`mmh3.mmh3_x64_128_digest()`, introduced in version 5.0.0, efficienlty hashes
buffer objects that implement the buffer protocol
([PEP 688](https://peps.python.org/pep-0688/)) without internal memory copying.
The function returns a `bytes` object of 16 bytes (128 bits). It is
particularly suited for hashing large memory views, such as
`bytearray`, `memoryview`, and `numpy.ndarray`, and performs faster than
the 32-bit variants like `hash()` on 64-bit machines.

```pycon
>>> mmh3.mmh3_x64_128_digest(numpy.random.rand(100))
b'\x8c\xee\xc6z\xa9\xfeR\xe8o\x9a\x9b\x17u\xbe\xdc\xee'
```

Various alternatives are available, offering different return types (e.g.,
signed integers, tuples of unsigned integers) and optimized for different
architectures. For a comprehensive list of functions, refer to the
[API Reference](https://mmh3.readthedocs.io/en/latest/api.html).

### `hashlib`-style hashers

`mmh3` implements hasher objects with interfaces similar to those in `hashlib`
from the standard library, although they are still experimental. See
[Hasher Classes](https://mmh3.readthedocs.io/en/latest/api.html#hasher-classes)
in the API Reference for more information.

## Changelog

See [Changelog](https://mmh3.readthedocs.io/en/latest/changelog.html) for the
complete changelog.

### [5.0.1] - 2024-09-22

#### Fixed

- Fix the issue that the package cannot be built from the source distribution
  ([#90](https://github.com/hajimes/mmh3/issues/90)).

### [5.0.0] - 2024-09-18

#### Added

- Add support for Python 3.13.
- Improve the performance of the `hash()` function with
  [METH_FASTCALL](https://docs.python.org/3/c-api/structures.html#c.METH_FASTCALL),
  reducing the overhead of function calls. For data sizes between 1–2 KB
  (e.g., 48x48 favicons), performance is 10%–20% faster. For smaller data
  (~500 bytes, like 16x16 favicons), performance increases by approximately 30%
  ([#87](https://github.com/hajimes/mmh3/pull/87)).
- Add `digest` functions that support the new buffer protocol
  ([PEP 688](https://peps.python.org/pep-0688/)) as input
  ([#75](https://github.com/hajimes/mmh3/pull/75)).
  These functions are implemented with `METH_FASTCALL` too, offering improved
  performance ([#84](https://github.com/hajimes/mmh3/pull/84)).
- Slightly improve the performance of the `hash_bytes()` function
  ([#88](https://github.com/hajimes/mmh3/pull/88))
- Add Read the Docs documentation
  ([#54](https://github.com/hajimes/mmh3/issues/54)).
- Document benchmark results
  ([#53](https://github.com/hajimes/mmh3/issues/53)).

#### Changed

- **Backward-incompatible**: The `seed` argument is now strictly validated to
  ensure it falls within the range [0, 0xFFFFFFFF]. A `ValueError` is raised
  if the seed is out of range ([#84](https://github.com/hajimes/mmh3/pull/84)).
- **Backward-incompatible**: Change the constructors of hasher classes to
  accept a buffer as the first argument
  ([#83](https://github.com/hajimes/mmh3/pull/83)).
- The type of flag argumens has been changed from `bool` to `Any`
  ([#84](https://github.com/hajimes/mmh3/pull/84)).
- Change the format of CHANGELOG.md to conform to the
  [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standard
  ([#63](https://github.com/hajimes/mmh3/pull/63)).

#### Deprecated

- Deprecate the `hash_from_buffer()` function.
  Use `mmh3_32_sintdigest()` or `mmh3_32_uintdigest()` as alternatives
  ([#84](https://github.com/hajimes/mmh3/pull/84)).

#### Fixed

- Fix a reference leak in the `hash_from_buffer()` function
  ([#75](https://github.com/hajimes/mmh3/pull/75)).
- Fix type hints ([#76](https://github.com/hajimes/mmh3/pull/76),
  [#77](https://github.com/hajimes/mmh3/pull/77),
  [#84](https://github.com/hajimes/mmh3/pull/84)).

### [4.1.0] - 2024-01-09

#### Added

- Add support for Python 3.12.

#### Fixed

- Fix issues with Bazel by changing the directory structure of the project
  ([#50](https://github.com/hajimes/mmh3/issues/50)).
- Fix incorrect type hints ([#51](https://github.com/hajimes/mmh3/issues/51)).
- Fix invalid results on s390x when the arg `x64arch` of `hash64` or
  `hash_bytes()` is set to `False`
  ([#52](https://github.com/hajimes/mmh3/issues/52)).

## License

[MIT](https://github.com/hajimes/mmh3/blob/master/LICENSE), unless otherwise
noted within a file.

## Known Issues

### Different results from other MurmurHash3-based libraries

By default, `mmh3` returns **signed** values for the 32-bit and 64-bit versions
and **unsigned** values for `hash128` due to historical reasons. To get the
desired result, use the `signed` keyword argument.

Starting from version 4.0.0, **`mmh3` is endian-neutral**, meaning that its
hash functions return the same values on big-endian platforms as they do on
little-endian ones. In contrast, the original C++ library by Appleby is
endian-sensitive. If you need results that comply with the original library on
big-endian systems, please use version 3.\*.

For compatibility with [Google Guava (Java)](https://github.com/google/guava),
see
<https://stackoverflow.com/questions/29932956/murmur3-hash-different-result-between-python-and-java-implementation>.

For compatibility with
[murmur3 (Go)](https://pkg.go.dev/github.com/spaolacci/murmur3), see
<https://github.com/hajimes/mmh3/issues/46>.

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

[5.0.1]: https://github.com/hajimes/mmh3/compare/v5.0.0...v5.0.1
[5.0.0]: https://github.com/hajimes/mmh3/compare/v4.1.0...v5.0.0
[4.1.0]: https://github.com/hajimes/mmh3/compare/v4.0.1...v4.1.0
