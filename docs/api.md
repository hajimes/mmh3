<!-- markdownlint-disable MD051 -->

# API Reference

The MurmurHash3 algorithm has three variants:

- MurmurHash3_x86_32: Generates 32-bit hashes using 32-bit arithmetic.
- MurmurHash3_x64_128: Generates 128-bit hashes using 64-bit arithmetic.
- MurmurHash3_x86_128: Generates 128-bit hashes using 32-bit arithmetic.

The `mmh3` library provides functions and classes for each variant.

Although this API reference is comprehensive, you may find the following
functions particularly useful:

- [mmh3.hash()](#mmh3.hash): Uses the 32-bit variant as its backend and accepts
  `bytes` or `str` as input (strings are UTF-8 encoded). This
  function is slower than the x64_128 variant in 64-bit environments but is
  portable across different architectures. It can also be used to calculate
  favicon hash footprints for platforms like
  [Shodan](https://www.shodan.io) and [ZoomEye](https://www.zoomeye.hk).
- [mmh3.mmh3_x64_128_digest()](#mmh3.mmh3_x64_128_digest): Uses the x64_128
  variant as its backend. This function accepts a buffer (e.g., `bytes`,
  `bytearray`, `memoryview`, and `numpy` arrays) and returns a 128-bit hash as
  a `bytes` object, similar to the `hashlib` module in the Python Standard
  Library. It performs faster than the 32-bit variant on 64-bit machines.

Note that **`mmh3` is endian-neutral**, while the original C++ library is
endian-sensitive (see also
[Frequently Asked Questions](https://github.com/hajimes/mmh3#frequently-asked-questions)).
This feature of `mmh3` is essential when portability across different
architectures is required, such as when calculating hash footprints for web
services.

```{caution}
[Buffer-accepting hash functions](#buffer-accepting-hash-functions) (except the
deprecated `hash_from_buffer`) accept positional-arguments only. Using keyword
arguments will raise a `TypeError`.
```

```{note}
Support for no-GIL mode (officially introduced in Python 3.14) was added in
version 5.2.0.
- Basic hash functions are inherently thread-safe by design.
- Buffer-accepting hash functions are thread-safe,
  **provided the input buffer is thread-safe**.
- Hasher classes are thread-safe,
  again **assuming the input buffer is thread-safe**.

However, thread safety under the no-GIL variant has not yet been
fully tested as of 5.2.0. If you encounter any issues, please report them via
the [issue tracker](https://github.com/hajimes/mmh3/issues).
```

## Basic Hash Functions

The following functions are used to hash immutable types, specifically
`bytes` and `str`. String inputs are automatically converted to `bytes` using
UTF-8 encoding before hashing.

Although `hash128()`, `hash64()`, and `mmh3.hash_bytes()` are provided for
compatibility with previous versions and are not marked for deprecation,
the [buffer-accepting hash functions](#buffer-accepting-hash-functions)
introduced in version 5.1.0 are recommended for new code.

```{eval-rst}
.. autofunction:: mmh3.hash
.. autofunction:: mmh3.hash128
.. autofunction:: mmh3.hash64
.. autofunction:: mmh3.hash_bytes
```

## Buffer-Accepting Hash Functions

The following functions are used to hash types that implement the buffer
protocol such as `bytes`, `bytearray`, `memoryview`, and `numpy` arrays.

```{seealso}
The buffer protocol,
[originally implemented as a part of Python/C API](https://docs.python.org/3/c-api/buffer.html),
was formally defined as a Python-level API in
[PEP 688](https://peps.python.org/pep-0688/)
in 2022 and its corresponding type hint was introduced as
[collections.abc.Buffer](https://docs.python.org/3/library/collections.abc.html#collections.abc.Buffer)
in Python 3.12. For earlier Python versions, `mmh3` uses a type alias for the
type hint
[\_typeshed.ReadableBuffer](https://github.com/python/typeshed/blob/d326c9bd424ad60c2b63c2ca1c5c1006c61c3562/stdlib/_typeshed/__init__.pyi#L281),
which is itself an alias for
[typing_extensions.Buffer](https://typing-extensions.readthedocs.io/en/stable/#typing_extensions.Buffer),
the backported type hint for `collections.abc.Buffer`.
```

```{eval-rst}
.. autofunction:: mmh3.hash_from_buffer
.. autofunction:: mmh3.mmh3_32_digest
.. autofunction:: mmh3.mmh3_32_sintdigest
.. autofunction:: mmh3.mmh3_32_uintdigest
.. autofunction:: mmh3.mmh3_x64_128_digest
.. autofunction:: mmh3.mmh3_x64_128_sintdigest
.. autofunction:: mmh3.mmh3_x64_128_stupledigest
.. autofunction:: mmh3.mmh3_x64_128_uintdigest
.. autofunction:: mmh3.mmh3_x64_128_utupledigest
.. autofunction:: mmh3.mmh3_x86_128_digest
.. autofunction:: mmh3.mmh3_x86_128_sintdigest
.. autofunction:: mmh3.mmh3_x86_128_stupledigest
.. autofunction:: mmh3.mmh3_x86_128_uintdigest
.. autofunction:: mmh3.mmh3_x86_128_utupledigest
```

## Hasher Classes

`mmh3` implements hashers with interfaces similar to those in `hashlib` from
the standard library: `mmh3_32()` for 32-bit hashing, `mmh3_x64_128()` for
128-bit hashing optimized for x64 architectures, and `mmh3_x86_128()` for
128-bit hashing optimized for x86 architectures.

In addition to the standard `digest()` method, each hasher provides
`sintdigest()`, which returns a signed integer, and `uintdigest()`, which
returns an unsigned integer. The 128-bit hashers also include `stupledigest()`
and `utupledigest()`, which return two 64 bit integers.

Please note that as of version 5.0.0, the implementation is still experimental,
and performance may be unsatisfactory (particularly `mmh3_x86_128()`).
Additionally, `hexdigest()` is not supported; use `digest().hex()` instead.

```pycon
>>> import mmh3
>>> hasher = mmh3.mmh3_x64_128(b"foo", 42) # seed=42
>>> hasher.update(b"bar")
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

```{eval-rst}
.. autoclass:: mmh3.mmh3_32
   :members:
```

```{eval-rst}
.. autoclass:: mmh3.mmh3_x64_128
   :members:
```

```{eval-rst}
.. autoclass:: mmh3.mmh3_x86_128
   :members:
```
