"""Benchmark hash functions.

A module to benchmark the throughput of hash functions.
The logic of the benchmarking functions is roughly based on the following C libary
https://github.com/Cyan4973/xxHash/tree/dev/tests/bench

"""

# for list / dict notation in 3.8
from __future__ import annotations

import gc
import hashlib
import time
from typing import Any, Callable, Final

import matplotlib.pyplot as plt
import mmh3
import pandas as pd
import pymmh3
import xxhash

TIMELOOP_NANOSEC = 1000000000  # 1 second in nanoseconds
K1 = 0b1001111000110111011110011011000110000101111010111100101010000111
K2 = 0b1100001010110010101011100011110100100111110101001110101101001111
MASK = 0xFFFFFFFFFFFFFFFF


class Benchmarker:
    """A class to benchmark a hash function."""

    # pylint: disable=too-few-public-methods

    SIZE_TO_HASH_PER_ROUND: Final[int] = 200000
    HASH_ROUNDS_MAX: Final[int] = 1000

    MARGIN_FOR_LATENCY: Final[int] = 1024

    WOLKLOAD_MULTIPLIER: Final[int] = 10

    def __init__(self, round_budget_ms: int, total_budget_ms: int):
        """Initializes the Benchmarker.

        Args:
            round_budget_ms: The minimum time for each round to spend running
                the hash function in milliseconds.
            total_budget_ms: The total minimum time to spend benchmarking in
                milliseconds.
        """

        # Run the benchmark function
        # until the time spent is greater than the run budget.
        # defaults to 1ms (in nanoseconds)
        self.run_budget_nanoseconds = round_budget_ms * TIMELOOP_NANOSEC / 1000

        self.total_budget_ms = total_budget_ms

        self.fastest_nanoseconds_per_run = float("inf")
        self.fastest_run_sum_of_return = -1
        self.number_of_loops = 1

    def _warmup(self, destinations: list[int]) -> None:
        """Warm up the CPU by running the benchmark function.

        The current implmentation follows the logic of the following C code:
        https://github.com/Cyan4973/xxHash/blob/dbea33e47e7c0fe0b7c8592cd931c7430c1f130d/tests/bench/benchfn.c
        It just fills the destination buffer with a constant value.

        However, when bencharmking functions in PyPy, a warmup requires the actual
        function to be called. See the faq of pytest-benchmark, as well as its code.
        https://pytest-benchmark.readthedocs.io/en/latest/faq.html#frequently-asked-questions

        As of version 4.1.0, mmh3 does not officially realase PyPy, so the warmup
        simply follows that of xxhash. However, the future version of mmh3 may
        support PyPy, so this code may need to be adjusted.

        Args:
            params: The parameters for the benchmark function.
        """

        # pylint: disable=invalid-name
        for i, _ in enumerate(destinations):
            destinations[i] = 0xE5

    def _benchmark_function(
        self,
        f: Callable,
        number_of_blocks: int,
        source_buffers: list[memoryview],
        destinations: list[int],
    ) -> dict[str, float | int]:
        result = {}

        self._warmup(destinations)

        clock_start = time.time_ns()

        for _ in range(self.number_of_loops):
            for i in range(number_of_blocks):
                b = source_buffers[i]
                destinations[i] = f(b)

        clock_end = time.time_ns()
        time_spent = clock_end - clock_start

        result["loop_duration_nanoseconds"] = time_spent
        result["nanoseconds_per_run"] = time_spent / self.number_of_loops

        return result

    def run_calibrated_benchmark(
        self, f: Callable, size: int
    ) -> dict[str, float | int]:
        """Runs the benchmark until the time spent is greater than therun budget.

        Runs the benchmark function with a number of loops that is automatically
        adjusted based on the time spent in the previous run. This technique is called
        the "calibration" in pytest-benchmark, whereas a budget is called a "round".

        Args:
            params: The parameters for the benchmark function.

        Returns:
            A dictionary containing the results of the benchmark.
        """
        # pylint: disable=invalid-name

        time_spent = 0

        source_buffer = bytearray(size + Benchmarker.MARGIN_FOR_LATENCY)
        init_buffer(source_buffer)

        number_of_blocks = (Benchmarker.SIZE_TO_HASH_PER_ROUND // size) + 1
        number_of_blocks = min(number_of_blocks, Benchmarker.HASH_ROUNDS_MAX)

        source_buffers = []
        source_sizes = []

        for _ in range(number_of_blocks):
            source_sizes.append(size)
            source_buffers.append(memoryview(source_buffer)[0:size])

        destinations = [0] * number_of_blocks

        while True:
            run_result = self._benchmark_function(
                f, number_of_blocks, source_buffers, destinations
            )

            time_spent += run_result["loop_duration_nanoseconds"]

            if run_result["loop_duration_nanoseconds"] > (
                self.run_budget_nanoseconds / 50
            ):
                fastest_run_ns = min(
                    self.fastest_nanoseconds_per_run, run_result["nanoseconds_per_run"]
                )
                self.number_of_loops = (
                    int(self.run_budget_nanoseconds / fastest_run_ns) + 1
                )
            else:
                self.number_of_loops *= Benchmarker.WOLKLOAD_MULTIPLIER

            if (
                run_result["loop_duration_nanoseconds"]
                < self.run_budget_nanoseconds / 2
            ):
                continue

            if run_result["nanoseconds_per_run"] < self.fastest_nanoseconds_per_run:
                self.fastest_nanoseconds_per_run = run_result["nanoseconds_per_run"]
                self.fastest_run_sum_of_return = run_result["loop_duration_nanoseconds"]

            break

        result = {}
        result["loop_duration_nanoseconds"] = time_spent
        result["nanoseconds_per_run"] = self.fastest_nanoseconds_per_run

        return result


def init_buffer(ba: bytearray) -> None:
    """Initializes a buffer with a pattern.

    Args:
        ba: The buffer to initialize.
    """
    acc = K2

    for i, _ in enumerate(ba):
        acc = (acc * K1) & MASK
        ba[i] = acc >> 56


def benchmark_hash(
    f: Callable, size: int, total_microseconds: int, run_microseconds: int
) -> float:
    """Benchmarks a hash function by running it on a buffer of a given size.

    Args:
        f: The hash function to benchmark.
        size: The size of the buffer to hash.
        total_microseconds: The total time to spend benchmarking.
        run_microseconds: The time to spend running the hash function.

    Returns:
        The time taken to hash the buffer in nanoseconds.
    """
    # pylint: disable=invalid-name
    bench = Benchmarker(run_microseconds, total_microseconds)
    result = bench.run_calibrated_benchmark(f, size)

    return result["nanoseconds_per_run"]


def benchmark_throughput_small_inputs(
    hashes: list[dict[str, Any]], small_test_size_min: int, small_test_size_max: int
):
    """Benchmarks the throughput of a hash function on small inputs.

    Args:
        hashes: The hash functions to benchmark.
        small_test_size_min: The minimum size of the input.
        small_test_size_max: The maximum size of the input.

    Returns: A dictionary containing the results of the benchmark.
    """
    # pylint: disable=invalid-name

    BENCH_SMALL_TOTAL_MS = 490
    BENCH_SMALL_ITERATION_MS = 170

    data_result = {}

    for h in hashes:
        result = []
        for i in range(small_test_size_min, small_test_size_max + 1):
            print(h["name"], i)
            gc.disable()
            result.append(
                benchmark_hash(
                    h["function"], i, BENCH_SMALL_TOTAL_MS, BENCH_SMALL_ITERATION_MS
                )
            )
            gc.enable()
        data_result[h["name"]] = result

    return data_result


def benchmark_large_inputs(
    hashes: list[dict[str, Any]], large_test_log_min: int, large_test_log_max: int
):
    """Benchmarks the throughput of a hash function on large inputs.

    Args:
        hashes: The hash functions to benchmark.
        large_test_log_min: The minimum log2 size of the input.
        large_test_log_max: The maximum log2 size of the input.

    Returns: A dictionary containing the results of the benchmark.
    """
    # pylint: disable=invalid-name

    BENCH_LARGE_TOTAL_MS = 1010
    BENCH_LARGE_ITERATION_MS = 490

    data_result = {}

    for h in hashes:
        result = []
        for i in range(large_test_log_min, large_test_log_max + 1):
            print(h["name"], i)
            gc.disable()
            result.append(
                benchmark_hash(
                    h["function"],
                    1 << i,
                    BENCH_LARGE_TOTAL_MS,
                    BENCH_LARGE_ITERATION_MS,
                )
            )
            gc.enable()
        data_result[h["name"]] = result

    return data_result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Benchmark hash functions.")
    parser.add_argument(
        "--benchmark-type",
        type=str,
        choices=["all", "large", "small-throughput-sequential"],
        default="all",
        help="The type of benchmarking to perform (default: all).",
    )

    SMALL_SIZE_MIN_DEFAULT = 1
    SMALL_SIZE_MAX_DEFAULT = 127
    LARGE_SIZELOG_MIN_DEFAULT = 9
    LARGE_SIZELOG_MAX_DEFAULT = 27

    HASHES = [
        {"name": "mmh3", "function": lambda x: mmh3.hash_bytes(bytes(x))},
        {"name": "xxhash", "function": lambda x: xxhash.xxh128(bytes(x)).digest()},
        {"name": "pymmh3", "function": lambda x: pymmh3.hash_bytes(bytes(x))},
        {"name": "md5", "function": lambda x: hashlib.md5(bytes(x)).digest()},
        {"name": "sha1", "function": lambda x: hashlib.sha1(bytes(x)).digest()},
    ]

    args = parser.parse_args()

    print(args.benchmark_type)

    if args.benchmark_type in ["small-throughput-sequential", "all"]:
        print("Benchmarking the throughput of small inputs sequentially")
        benchmark_results = benchmark_throughput_small_inputs(
            HASHES, SMALL_SIZE_MIN_DEFAULT, SMALL_SIZE_MAX_DEFAULT
        )

        print("Generating plot")
        df = pd.DataFrame(
            benchmark_results,
            index=list(range(SMALL_SIZE_MIN_DEFAULT, SMALL_SIZE_MAX_DEFAULT + 1)),
        )

        plt.figure()

        df.plot(
            xlabel="Input size (bytes)",
            ylabel="Reciprocal throughput (ns/bytes)",
            logy=True,
        )

        plt.savefig("docs/images/throughput_small_inputs.png")
        plt.close("all")

    if args.benchmark_type in ["large", "all"]:
        print("Benchmarking the throughput of large inputs sequentially")
        benchmark_results = benchmark_large_inputs(
            HASHES, LARGE_SIZELOG_MIN_DEFAULT, LARGE_SIZELOG_MAX_DEFAULT
        )

        print("Generating plot")
        df = pd.DataFrame(
            benchmark_results,
            index=list(range(LARGE_SIZELOG_MIN_DEFAULT, LARGE_SIZELOG_MAX_DEFAULT + 1)),
        )

        plt.figure()

        df.plot(
            logy=True,
        )

        plt.savefig("docs/images/throughput_large_inputs.png")
        plt.close("all")
