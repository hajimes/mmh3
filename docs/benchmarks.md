# Benchmarks

## Data

```{figure} images/throughput_small_inputs.png
:alt: Throughput for small inputs
:align: center

Figure 1: Throughput (reciprocal) for small inputs. Smaller is better.
```

As you see, the throughput of `mmh3` is significantly
higher than that of `hashlib` (`md5` and `sha1`) for small inputs.

```{figure} images/throughput_large_inputs.png
:alt: Throughput for large inputs
:align: center

Figure 2: Throughput (reciprocal) for large inputs. Smaller is better.
```

However, when the input size is large, the throughput of `xxhashh` is higher than that of `mmh3`.
The result is exptected because of the speed differences between the backends of two hash functions.

## References

- Yann Collet. [xxHash].
- Ionel Cristian Mărieș.
  [pytest-benchmark].
- Micha Gorelick and Ian Ozsvald. 2020.
  _[High Performance Python: Practical Performant Programming for Humans]_,
  2nd ed. O'Reilly Media. ISBN: 978-1492055020.

[xxHash]: https://github.com/Cyan4973/xxHash
[pytest-benchmark]: https://github.com/ionelmc/pytest-benchmark
[High Performance Python: Practical Performant Programming for Humans]: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
