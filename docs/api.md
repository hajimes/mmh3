# API Reference

```{caution}
  This reference contains functions that are not yet released in the stable
  version.
```

## Functions for immutables

The following functions are used to hash immutables, that is, `bytes` and `str`.
 The string inputs are converted to bytes with `utf-8` encoding.


```{eval-rst}
.. autofunction:: mmh3.hash
.. autofunction:: mmh3.hash128
.. autofunction:: mmh3.hash64
.. autofunction:: mmh3.hash_bytes
```

## Functions for Buffer

The following functions are used to hash non-immutable buffers.

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
