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

However, when the input size is large, the throughput of `xxhashh` is higher
than that of `mmh3`. The result is exptected because of the speed differences
between the backends of two hash functions.


## Microbenchmarking in Python

### Pregenerated iterator

### 

### Calibration

The default values for calibration:

- autorage of timeit in Python ST
  - 200,000 microseconds
- pytest-benchmark
  - 5 microsconds (chosen as 10 x TIMER_RESOLUTION)
- xxHash:
  - 170 microseconds for small inputs (<= 128 bytes)
  - 490 microseconds for large inputs


## References

- [timeit] (Python Standard Library).
- Yann Collet. [xxHash].
- Ionel Cristian Mărieș.
  [pytest-benchmark].
- Tim Peters. 2002. [Chapter 17. Algorithms: Introduction] in _Python Cookbook_,
  3rd ed. O'Reilly Media. ISBN: 978-0596001674.
- Micha Gorelick and Ian Ozsvald. 2020.
  _[High Performance Python: Practical Performant Programming for Humans]_,
  2nd ed. O'Reilly Media. ISBN: 978-1492055020.

[timeit]: https://docs.python.org/3/library/timeit.html
[xxHash]: https://github.com/Cyan4973/xxHash
[pytest-benchmark]: https://github.com/ionelmc/pytest-benchmark
[Chapter 17. Algorithms: Introduction]: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch17.html
[High Performance Python: Practical Performant Programming for Humans]: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
