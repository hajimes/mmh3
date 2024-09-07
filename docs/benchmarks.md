# Benchmarks

## Settings

- Python environment
  - CPython 3.12.5 (64-bit)
- Ubuntu 22.04 instance on GitHub Actions
- Hash libraries
  - mmh3 4.2.0: dev version
  - xxhash 3.5.0
- pyperf 2.7.0

## Results

### Graphs

```{figure} _static/bandwidth.png
:alt: Latency
:align: center

Figure 1: Output bandwidth. Larger is better. The y-axis is logscale.
```

```{figure} _static/bandwidth_small.png
:alt: Latency
:align: center

Figure 2: Output bandwidth for small data. Larger is better.
```

```{figure} _static/latency.png
:alt: Latency
:align: center

Figure 3: Latency. Smaller is better.
```

```{figure} _static/latency_small.png
:alt: Latency
:align: center

Figure 4: Latency for small data. Smaller is better.
```

## Microbenchmarking Techniques and Tools

**Microbenchmarking** is a specialized type of benchmarking to measure the
performance of a small piece of code. It is crucial to compare the performance
of different implementations of a group of related algorithms or to measure the
impact of a change in the code. Although conceptually simple, microbenchmarking
can be challenging in practice, particularly in Python, a scripting language.

### Tools

There are three popular libraries for microbenchmarking in Python: [pyperf],
[pytest-benchmark], and [airspeed velocity] (also known as `asv`).

**pyperf** is a general-purpose Python performance benchmarking tool, focused
on providing reliable and accurate benchmarks with detailed reporting and
statistical analysis. It is the primary backend for [pyperformance], an
authoritative benchmark suite for Python interpreters, which in turn is used as
the backend of [Python Speed Center](https://speed.python.org), the official
performance dashboard for CPython.

**pytest-benchmark** is a plugin for pytest that provides a fixture to
benchmark. It is designed to be user-friendly, offering a simple interface for
benchmarking by allowing users to write benchmarks that integrate seamlessly
with unit tests. It is also used as the primary backend for the Python
environment in <code>[github-action-benchmark]</code>, a GitHub Action for
continuous benchmarking.

**airspeed velocity** (`asv`) is a tool that supports continuous benchmarking
for indiviual projects, with built-in native support for a web interface.
It also features a command-line interface similart to Git, making it to manage
the history of benchmarks. Both
[NumPy](https://numpy.org/devdocs/benchmarking.html) and
[SciPy](https://docs.scipy.org/doc/scipy/dev/contributor/benchmarking.html)
use asv as their benchmarking tool.

Each tool has its strengths and weaknesses. Both `pytest-benchmark` and
`asv` are tailored for specific use cases and excel in those contexts. While
`pyperf` requires more manual coding and setup for benchmarking, it offers
greater flexiblity and can be applied to a broader range of scenarios.

### Iterator pre-instantiation

In its simplest form, mircrobenchmarking a function involves writing a loop
that calls the function multiple times and measures the total time taken.
This total is then divided by the number of iterations to calculate the average
execution time per call.

```python
import time

def bench_my_function_1(loops: int) -> float:
    t0 = time.perf_counter()

    for _ in range(loops):
        my_function()

    # After return, divide the result by loops to get the average time
    return time.perf_counter() - t0
```

However, when microbenchmarking a small function, even the time taken to
instantiate the iterator (`range(n)`) can be significant. To mitigate this,
create the iterator before starting the timer.

```python
import time

def bench_my_function_2(loops: int) -> float:
    it = range(loops)
    t0 = time.perf_counter()

    for _ in it:
        your_function()

    # After return, divide the result by loops to get the average time
    return time.perf_counter() - t0
```

The `timeit` module in the Standard Library uses `itertools.repeat(None, n)`
as the iterator. This can be marginally faster than using `range(n)`, because
`itertools.repeat(None, n)` does not need to calculate the next value in the
loop.

```python
import itertools
import time

def bench_my_function_3(loops: int) -> float:
    it = itertools.repeat(None, loops)
    t0 = time.perf_counter()

    for _ in it:
        your_function()

    # After return, divide the result by loops to get the average time
    return time.perf_counter() - t0
```

References:

- Tim Peters. 2002. [Chapter 17. Algorithms: Introduction] in _Python Cookbook_,
  3rd ed. O'Reilly Media. ISBN: 978-0596001674.
- Python Standard Library. [timeit.py].

[airspeed velocity]: https://github.com/airspeed-velocity/asv
[github-action-benchmark]: https://github.com/marketplace/actions/continuous-benchmark
[pyperf]: https://github.com/psf/pyperf
[pyperformance]: https://github.com/python/pyperformance
[pytest-benchmark]: https://github.com/ionelmc/pytest-benchmark
[timeit.py]: https://github.com/python/cpython/blob/3.12/Lib/timeit.py
[Chapter 17. Algorithms: Introduction]: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch17.html
