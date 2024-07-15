import gc
import hashlib
import time

import matplotlib.pyplot as plt
import mmh3
import pandas as pd
import pymmh3
import xxhash

"""
The logic of the benchmarking functions is roughly based on the following C libary
https://github.com/Cyan4973/xxHash/tree/dev/tests/bench
"""


TIMELOOP_NANOSEC = 1000000000  # 1 second in nanoseconds


class BenchmarkHashFunction:
    def __init__(self, size, total_microseconds, run_microseconds):
        self._reset(total_microseconds, run_microseconds)

    def _reset(self, total_microseconds, run_microseconds):
        if run_microseconds is None:
            self.run_microseconds = 1
        else:
            self.run_microseconds = run_microseconds

        # Run the benchmark function
        # until the time spent is greater than the run budget.
        # defaults to 1ms (in nanoseconds)
        self.run_budget_nanoseconds = self.run_microseconds * TIMELOOP_NANOSEC / 1000

        self.fastest_nanoseconds_per_run = float("inf")
        self.fastest_run_sum_of_return = -1
        self.number_of_loops = 1

    def benchmark_function(self, params):
        result = {}

        clock_start = time.time_ns()

        for i in range(self.number_of_loops):
            for j in range(params["number_of_blocks"]):
                b = params["source_buffers"][j]
                params["destinations"][j] = params["function"](b)

        clock_end = time.time_ns()
        time_spent = clock_end - clock_start

        result["loop_duration_nanoseconds"] = time_spent
        result["nanoseconds_per_run"] = time_spent / self.number_of_loops

        return result

    def run_timed_benchmarks(self, params):
        time_spent = 0

        WOLKLOAD_MULTIPLIER = 10

        while True:
            run_result = self.benchmark_function(params)

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
                self.number_of_loops *= WOLKLOAD_MULTIPLIER

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


def init_buffer(ba, size):
    K1 = 0b1001111000110111011110011011000110000101111010111100101010000111
    K2 = 0b1100001010110010101011100011110100100111110101001110101101001111
    MASK = 0xFFFFFFFFFFFFFFFF
    acc = K2

    for i in range(size):
        acc = (acc * K1) & MASK
        ba[i] = acc >> 56


def benchmark_hash(f, size, total_microseconds, run_microseconds):
    SIZE_TO_HASH_PER_ROUND = 200000
    HASH_ROUNDS_MAX = 1000

    MARGIN_FOR_LATENCY = 1024

    source_buffer = bytearray(size + MARGIN_FOR_LATENCY)
    init_buffer(source_buffer, size + MARGIN_FOR_LATENCY)

    number_of_blocks = (SIZE_TO_HASH_PER_ROUND / size) + 1
    number_of_blocks = min(number_of_blocks, HASH_ROUNDS_MAX)

    source_buffers = []
    source_sizes = []

    for i in range(number_of_blocks):
        source_sizes.append(size)
        source_buffers.append(memoryview(source_buffer)[0:size])

    params = {}
    params["function"] = f
    params["source_buffers"] = source_buffers
    params["source_sizes"] = source_sizes
    params["number_of_blocks"] = number_of_blocks
    params["destinations"] = [0] * number_of_blocks

    bench = BenchmarkHashFunction(size, total_microseconds, run_microseconds)
    result = bench.run_timed_benchmarks(params)

    return result["nanoseconds_per_run"]


def benchmark_throughput_small_inputs(hashes, small_test_size_min, small_test_size_max):
    BENCH_SMALL_TOTAL_MS = 490
    BENCH_SMALL_ITERATION_MS = 170

    data_result = {}

    for h in hashes:
        result = []
        for i in range(small_test_size_min, small_test_size_max + 1):
            gc.disable()
            result.append(
                benchmark_hash(
                    h["function"], i, BENCH_SMALL_TOTAL_MS, BENCH_SMALL_ITERATION_MS
                )
            )
            gc.enable()
        data_result[h["name"]] = result

    return data_result


if __name__ == "__main__":
    SMALL_SIZE_MIN_DEFAULT = 1
    SMALL_SIZE_MAX_DEFAULT = 127

    hashes = [
        {"name": "mmh3", "fuｂｌnction": lambda x: mmh3.hash_bytes(bytes(x))},
        {"name": "xxhash", "function": lambda x: xxhash.xxh128(bytes(x)).digest()},
        {"name": "pymmh3", "function": lambda x: pymmh3.hash_bytes(bytes(x))},
        {"name": "md5", "function": lambda x: hashlib.md5(bytes(x)).digest()},
        {"name": "sha1", "function": lambda x: hashlib.sha1(bytes(x)).digest()},
    ]

    benchmark_results = benchmark_throughput_small_inputs(
        hashes, SMALL_SIZE_MIN_DEFAULT, SMALL_SIZE_MAX_DEFAULT
    )

    df = pd.DataFrame(
        benchmark_results,
        index=list(range(SMALL_SIZE_MIN_DEFAULT, SMALL_SIZE_MAX_DEFAULT + 1)),
    )

    plt.figure()

    df.plot(
        logy=True,
    )

    plt.savefig("result.png")
    plt.close("all")
