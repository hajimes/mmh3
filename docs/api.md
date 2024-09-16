# API Reference

```{caution}
  This reference contains functions and APIs that are not yet released in the
  stable version (4.1.0).
```

## Functions for immutables

The following functions are used to hash immutable types, specifically
`bytes` and `str`. String inputs are automatically converted to `bytes` using
UTF-8 encoding before hashing.

```{eval-rst}
.. autofunction:: mmh3.hash
.. autofunction:: mmh3.hash128
.. autofunction:: mmh3.hash64
.. autofunction:: mmh3.hash_bytes
```

## Functions for Buffer

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
[typing_extensions.Buffer](https://typing-extensions.readthedocs.io/en/latest/#typing_extensions.Buffer),
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
