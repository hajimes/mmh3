"""Benchmark module for various hash functions."""

import itertools
import time
from typing import Final

import mmh3
import pyperf

K1: Final[int] = 0b1001111000110111011110011011000110000101111010111100101010000111
K2: Final[int] = 0b1100001010110010101011100011110100100111110101001110101101001111
MASK: Final[int] = 0xFFFFFFFFFFFFFFFF


def init_buffer(ba: bytearray) -> bytearray:
    """Initializes a byte array with a pattern.

    Initializes a byte array with a pattern based on xxHash's benchmarking.
    https://github.com/Cyan4973/xxHash/blob/dev/tests/bench/benchHash.c

    Args:
        ba: The byte array to initialize.

    Returns:
        The initialized byte array.
    """
    acc = K2

    for i, _ in enumerate(ba):
        acc = (acc * K1) & MASK
        ba[i] = acc >> 56

    return ba


def mmh3_128_test(loops: int, size: int) -> float:
    """Benchmark the mmh3 hash function.

    Args:
        loops: The number of outer loops to run.
        size: The size of the buffer to hash.

    Returns:
        The time taken to hash the buffer in fractional seconds.
    """
    range_it = itertools.repeat(None, loops)

    data = bytearray(size + 9)
    data = init_buffer(data)

    data0 = bytes(data[0:size])
    data1 = bytes(data[1 : size + 1])
    data2 = bytes(data[2 : size + 2])
    data3 = bytes(data[3 : size + 3])
    data4 = bytes(data[4 : size + 4])
    data5 = bytes(data[5 : size + 5])
    data6 = bytes(data[6 : size + 6])
    data7 = bytes(data[7 : size + 7])
    data8 = bytes(data[8 : size + 8])
    data9 = bytes(data[8 : size + 9])

    t0 = time.perf_counter()
    for _ in range_it:
        mmh3.hash_bytes(data0)
        mmh3.hash_bytes(data1)
        mmh3.hash_bytes(data2)
        mmh3.hash_bytes(data3)
        mmh3.hash_bytes(data4)
        mmh3.hash_bytes(data5)
        mmh3.hash_bytes(data6)
        mmh3.hash_bytes(data7)
        mmh3.hash_bytes(data8)
        mmh3.hash_bytes(data9)

    return time.perf_counter() - t0


if __name__ == "__main__":
    runner = pyperf.Runner()
    bench = runner.bench_time_func(
        "mmh3-128_1024x1024", mmh3_128_test, 1024 * 1024, inner_loops=10
    )
    # bench.dump("mmh3-128_1024x1024.json", replace=True)

    bench = runner.bench_time_func(
        "mmh3-128_64", mmh3_128_test, 64, inner_loops=10
    )
    # bench.dump("mmh3-128_64.json", replace=True)


