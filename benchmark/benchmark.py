"""Benchmark module for various hash functions."""

import hashlib
import itertools
import time
from collections.abc import Callable
from typing import Final

import mmh3
import pymmh3
import pyperf
import xxhash

K1: Final[int] = 0b1001111000110111011110011011000110000101111010111100101010000111
K2: Final[int] = 0b1100001010110010101011100011110100100111110101001110101101001111
MASK: Final[int] = 0xFFFFFFFFFFFFFFFF

HASHES = {
    "mmh3_32": mmh3.mmh3_32_digest,
    "mmh3_128": mmh3.mmh3_x64_128_digest,
    "xxh_32": xxhash.xxh32_digest,
    "xxh_64": xxhash.xxh64_digest,
    "xxh3_64": xxhash.xxh3_64_digest,
    "xxh3_128": xxhash.xxh3_128_digest,
    "md5": lambda ba: hashlib.md5(ba).digest(),
    "sha1": lambda ba: hashlib.sha1(ba).digest(),
    "pymmh3_32": pymmh3.hash,
    "pymmh3_128": pymmh3.hash128,
}


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


def perf_hash(loops: int, f: Callable, size: int) -> float:
    """Benchmark the mmh3 hash function.

    Args:
        loops: The number of outer loops to run.
        f: The hash function to benchmark
        size: The size of the buffer to hash.

    Returns:
        The time taken to hash the buffer in fractional seconds.
    """
    # pylint: disable=too-many-locals

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
        f(data0)
        f(data1)
        f(data2)
        f(data3)
        f(data4)
        f(data5)
        f(data6)
        f(data7)
        f(data8)
        f(data9)

    return time.perf_counter() - t0


def add_cmdline_args(cmd: list, args) -> None:
    """Add command line arguments to the runner.

    Args:
        cmd: The command line arguments to extend.
        args: The parsed command line arguments.
    """
    cmd.extend(("--test-hash", args.test_hash))
    cmd.extend(("--test-buffer-size-max", str(args.test_buffer_size_max)))


if __name__ == "__main__":
    runner = pyperf.Runner(add_cmdline_args=add_cmdline_args)

    runner.argparser.add_argument(
        "--test-hash",
        type=str,
        help="Type of hash function to benchmark",
        required=True,
        choices=HASHES.keys(),
    )

    runner.argparser.add_argument(
        "--test-buffer-size-max",
        type=int,
        help="The maximum size of the buffer to hash (default: 1024)",
        default=1024,
    )

    process_args = runner.parse_args()
    fib1, fib2 = 1, 2

    while fib1 <= process_args.test_buffer_size_max:
        runner.bench_time_func(
            f"{fib1} bytes",
            perf_hash,
            HASHES[process_args.test_hash],
            fib1,
            inner_loops=10,
        )
        fib1, fib2 = fib2, fib1 + fib2
