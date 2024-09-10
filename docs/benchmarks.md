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

## Notes on Python Microbenchmarking

**Microbenchmarking** is a type of benchmarking aimed at measuring the
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
environment in [github-action-benchmark], a GitHub Action for
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

### Clock resolution

In Python, the most basic way to measure time is by using the `time.time()`
function. However, this function may not provide the highest resolution
available on the system. In addition, it doesn't ensure monotonicity, meaning
the time could move backward if the system clock has been set back. As a
result, the difference between two calls might even be negative.

````{danger}
```python
import time


def bench_my_function_1() -> float:
    t0 = time.time()

    my_function()

    # In fractional seconds
    return time.time() - t0
```
````

For higher resolution, you can use `time.perf_counter()`, introduced in
Python 3.3. While it may not have much use in a single call, it provides the
highest available resolution and is monotonic, making it ideal for benchmarking
tasks.

```python
import time


def bench_my_function_2() -> float:
    t0 = time.perf_counter()

    my_function()

    # In fractional seconds
    return time.perf_counter() - t0
```

Since Python 3.7, `time.perf_counter_ns()` is available, returning the time
as an integer in nanoseconds.

```python
import time

def bench_my_function_3() -> int:
    t0 = time.perf_counter_ns()

    my_function()

    # In nanoseconds
    return time.perf_counter_ns() - t0
```

If you're implementing your benchmarking logic from scratch, it is recommended
to use `time.perf_counter_ns()` to avoid the rounding errors that can occur with
with the float-based `time.perf_counter()`. However, the [bench_time_func()]
function of pyperf 2.7.0 expects the return value to be the differences of
`time.perf_counter()`, as the library predates the introduction of
`time.perf_counter_ns()`. Choose the appropriate function depending on your
approach.

### Elminate the function call overhead

```{note}
Key points: for casual microbenchmarking, use
[timeit.Timer.timeit()](https://docs.python.org/3/library/timeit.html#timeit.Timer.timeit)
from the Python Standard Library. For more robust benchmarking, use
[Runner.timeit()](https://pyperf.readthedocs.io/en/latest/api.html#Runner.timeit)
or
[Runner.bench_time_func()](https://pyperf.readthedocs.io/en/latest/api.html#Runner.bench_time_func)
in `pyperf`.
```

Conceptually, benchmarking can be viewed as a dectorator pattern that measures
the time taken to execute a set of statements before and after execution.
In Python 3, such decorators can be implemented cleanly using function
annotations. For most cases, unless microbenchmarking for small functions,
this solution is optimal. Always remember the mantra: "Premature optimization
is the root of all evil" (Donald Knuth). Prioritize elegance and
maintainability as core principles. The following code, based on an example
from Gorelick and Ozsvald (2020), demonstrates a decorator that measures the
execution time of a function.

````{warning}
```{literalinclude} ./examples/benchmark_decorator_example.py
```
````

However, when testing very small functions, the function call overhead can
become non-neglibile. To address this, `pytest-benchmark` provides a convenient
approach by offering the benchmarking function as a fixture for each unit test.
Users can simply pass the function to be tested as an argument to this fixture.

```python
import time


def test_by_pytest_fixture(benchmark):
    # 0.05 is passed as the first argument to the function time.sleep
    benchmark(time.sleep, 0.05)
```

The above approach still has a limitation. If 　 we want to microbenchmark a set
of statements rather than a predefined function, we need to write a wrapper
function for these statements, which introduces overhead.

There are two ways to avoid this overhead.

The first approach is to use the built-in function `compile` to dymamically
create an executable instance of statements from a string. A good example of
this is `timeit.Timer.timeit()` in the Python Standard Library. Gorelick and
Ozsvald (2020) also recommend using `timeit` for benchmarking small functions.

```{literalinclude} ./examples/timeit_timeit.py

```

In addition, `pyperf` provides an [advanced implementation of
timeit()](https://pyperf.readthedocs.io/en/latest/api.html#Runner.timeit).

```{literalinclude} ./examples/pyperf_timeit.py

```

The second approach is to have the user write a function that returns the
execution time of statemets, and then pass this function to the benchmarking
tool. The
[bench_time_func()](https://pyperf.readthedocs.io/en/latest/api.html#Runner.bench_time_func)
function in pyperf follows this method.

```{literalinclude} ./examples/bench_time_func_example.py

```

While this approach can be more tedious, it has the advantage of being fully
supported by linters and IDEs, as the code is not embedded in a string.

```{seealso}
- Python Standard Library.
  [timeit.Timer.timeit()](https://docs.python.org/3/library/timeit.html#timeit.Timer.timeit)
- [pytest-benchmark: Usage](https://pytest-benchmark.readthedocs.io/en/latest/usage.html)
- [pyperf: Runner class](https://pyperf.readthedocs.io/en/latest/api.html#runner-class)
- Micha Gorelick and Ian Ozsvald. 2020.
  High Performance Python: Practical Performant Programming for Humans,
  2nd ed. O'Reilly Media. ISBN: 978-1492055020. pp. 30-33.
```

### Iterator pre-instantiation

```{note}
Key points: call `range()` or `itertools.repeat()` before starting the timer.
```

In its simplest form, mircrobenchmarking a function involves writing a loop
that calls the function multiple times and measures the total time taken.
This total is then divided by the number of iterations to calculate the average
execution time per call.

However, when microbenchmarking a small function in an interpreted language
like Python, even the time taken to instantiate the iterator (`range(n)`) can be
significant.

````{warning}
```python
import time


def bench_my_function_1(loops: int) -> float:
    t0 = time.perf_counter()

    for _ in range(loops):
        my_function()

    # After return, divide the result by loops to get the average time
    return time.perf_counter() - t0
```
````

To mitigate this, create the iterator before starting the timer.

```python
import time


def bench_my_function_2(loops: int) -> float:
    it = range(loops)
    t0 = time.perf_counter()

    for _ in it:
        my_function()

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
        my_function()

    # After return, divide the result by loops to get the average time
    return time.perf_counter() - t0
```

```{seealso}
- Tim Peters. 2002.
[Chapter 17. Algorithms: Introduction](https://www.oreilly.com/library/view/python-cookbook/0596001673/ch17.html)
in _Python Cookbook_,
  3rd ed. O'Reilly Media. ISBN: 978-0596001674.
- Python Standard Library. [timeit.py](https://github.com/python/cpython/blob/3.12/Lib/timeit.py).
```

### Mean, minimum, or median?

```{note}
Short answer: **mean, provided that the system is well-tuned and the number of
warmups and runs is sufficient**. The median is a good alternative when the
system is untuned or unstable. Avoid using the minimum.
```

When microbenchmarking a function in multiple sets of runs, the question
arises: which statistic should serve as the most representative result? Common
choices include the mean, minimum, and median.

Traditionally, the minimum value has been favored to minimize the impact of
outliers. For instance, the note on
[timeit.Timer.repeat()](https://docs.python.org/3/library/timeit.html#timeit.Timer.repeat)
in the Python Standard Library recommends using the minimum value.
This is because higher values are likely the results of influence by external
factors such as other processes. As a result, the lowest value is often
considered the most reliable indicator. A preprint paper by Chen and Revels
(2016) on benchmarking in the Julia language supports this view, suggesting that
the minimum is the most robust estimator. Similarly, the
[bechmarking program of xxHash](https://github.com/Cyan4973/xxHash/blob/release/tests/bench/benchfn.c)
(written in C) uses the minimum value.

However, Victor Stinner (2016; pyperf issues #75), the lead author of `pyperf`,
strongly opposes the use of minimum and advocates for the mean instead.
With proper system tuning and a sufficiently large number of warmups/runs,
the noises and outliers caued by external factors should be significantly
reduced and follow a normal distribution. In such cases, relying on the
minimum can overlook important outliers caused by _internal_ factors within the
function being tested, making the mean a more reliable indicator of performance.

In fact, the `timeit` function in Jupyter and IPython, which initially used
the minimum, switched to using the mean and standard deviation in 2016
(Gorelick and Ozsvald, 2020, p. 32). That same year,
[PyPy2.7 v5.6](https://github.com/pypy/pypy/blob/f7cadf679738f8f6cf54b707c5516c7a0343dea0/pypy/doc/whatsnew-pypy2-5.6.0.rst)
also adopted the mean and standard deviation for `timeit`, stating that the
minimum can often be misleading.

Gorelick and Ozsvald (2020, p. 32) recognizes the flaws of both the mean and
minimum, emphasizing that consistency in metric selection is key.
They do not endorse a single metric but advise choosing one and sticking to it.

Alternatively, the median, paired with the median absolute deviation (MAD),
serves as a compromise between the mean (paired with the standard deviation)
and the minimum, when the the system is not well-tuned or stable. For more
details, refer to
[pyerf: Analyze benchmark results](https://pyperf.readthedocs.io/en/latest/analyze.html)
and
[pyperf issues #1: Use a better measures than average and standard deviation #1](https://github.com/psf/pyperf/issues/1).

```{seealso}
- Python Standard Library.
  [Note on timeit.Timer.repeat()](https://docs.python.org/3/library/timeit.html#timeit.Timer.repeat)
- [What's new in PyPy2.7 5.6](https://github.com/pypy/pypy/blob/f7cadf679738f8f6cf54b707c5516c7a0343dea0/pypy/doc/whatsnew-pypy2-5.6.0.rst)
- [pyerf: Analyze benchmark results](https://pyperf.readthedocs.io/en/latest/analyze.html)
- [pyperf issues #1: Use a better measures than average and standard deviation #1](https://github.com/psf/pyperf/issues/1)
- [pyperf issues #75: Reconsidering min()?](https://github.com/psf/pyperf/issues/75)
- Jiahao Chen and Jarrett Revels. 2016.
  [Robust benchmarking in noisy environments](https://arxiv.org/abs/1608.04295).
  arXiv:1608.04295
- Micha Gorelick and Ian Ozsvald. 2020.
  High Performance Python: Practical Performant Programming for Humans,
  2nd ed. O'Reilly Media. ISBN: 978-1492055020.
- Victor Stinner. 2016. [My journey to stable benchmark, part 3 (average)](https://vstinner.github.io/journey-to-stable-benchmark-average.html)
```

### System tuning

To obtain reliable results from microbenchmarks, a stable environment is
crucial. Ideally, benchmarking should be performed on a dedicated machine.
Even then, it's important to fine-tune the system to minimize the impact of
other processes. This is where pyperf excels shines, offering the `system tune`
command for Linux systems.

```shell
sudo python -m pyperf system tune
```

airspeed velocity also
[recommends pyperf for machine tuning](https://asv.readthedocs.io/en/v0.6.1/tuning.html).

However, as of version 2.7.0, the `pyperf system tune` command does not support
Ubuntu instances on GitHub Actions.

```{seealso}
- [pyperf: Tune the system for benchmarks](https://pyperf.readthedocs.io/en/latest/system.html)
- Manuel Bernhardt. 2023.
[On pinning and isolating CPU cores](https://manuel.bernhardt.io/posts/2023-11-16-core-pinning/)
- Jaime Rodríguez-Guerra. 2021.
[Is GitHub Actions suitable for running benchmarks?](https://labs.quansight.org/blog/2021/08/github-actions-benchmarks)
- Victor Stinner. 2016.
[My journey to stable benchmark, part 1 (system)](https://vstinner.github.io/journey-to-stable-benchmark-system.html)
```

[airspeed velocity]: https://github.com/airspeed-velocity/asv
[bench_time_func()]: https://pyperf.readthedocs.io/en/latest/api.html#Runner.bench_time_func
[github-action-benchmark]: https://github.com/marketplace/actions/continuous-benchmark
[pyperf]: https://github.com/psf/pyperf
[pyperformance]: https://github.com/python/pyperformance
[pytest-benchmark]: https://github.com/ionelmc/pytest-benchmark
