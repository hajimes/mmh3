"""Benchmark module for various hash functions."""

import hashlib
import itertools
import math
import random
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


def generate_size(size: int, p: float) -> int:
    """Generate a random size for a buffer.

    Args:
        size: The size of the buffer to hash.
        p: The percentage of the buffer size to vary.

    Returns:
        The random size of the buffer.
    """
    lower = math.ceil(size * (1 - p))
    upper = math.floor(size * (1 + p))

    return random.randint(lower, upper)


def perf_hash(loops: int, f: Callable, size: int) -> float:
    """Benchmark a hash function.

    Args:
        loops: The number of outer loops to run.
        f: The hash function to benchmark
        size: The size of the buffer to hash.

    Returns:
        The time taken to hash the buffer in fractional seconds.
    """
    # pylint: disable=too-many-locals

    if size <= 0:
        raise ValueError("size must be greater than 0")

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
    data9 = bytes(data[9 : size + 9])

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


def perf_hash_random(loops: int, f: Callable, size: int) -> float:
    """Benchmark a hash function with varying data sizes.

    Args:
        loops: The number of outer loops to run.
        f: The hash function to benchmark
        size: The size of the buffer to hash.

    Returns:
        The time taken to hash the buffer in fractional seconds.
    """
    # pylint: disable=too-many-locals

    if size <= 0:
        raise ValueError("size must be greater than 0")

    range_it = itertools.repeat(None, loops)
    random.seed(42)
    inner_loops = 10
    extra_size = 255

    data = bytearray(size + extra_size)
    data = init_buffer(data)

    pos_list = [random.randint(0, extra_size) for _ in range(inner_loops)]
    size_list = [generate_size(size, 0.1) for _ in range(inner_loops)]

    data0 = bytes(data[pos_list[0] : pos_list[0] + size_list[0]])
    data1 = bytes(data[pos_list[1] : pos_list[1] + size_list[1]])
    data2 = bytes(data[pos_list[2] : pos_list[2] + size_list[2]])
    data3 = bytes(data[pos_list[3] : pos_list[3] + size_list[3]])
    data4 = bytes(data[pos_list[4] : pos_list[4] + size_list[4]])
    data5 = bytes(data[pos_list[5] : pos_list[5] + size_list[5]])
    data6 = bytes(data[pos_list[6] : pos_list[6] + size_list[6]])
    data7 = bytes(data[pos_list[7] : pos_list[7] + size_list[7]])
    data8 = bytes(data[pos_list[8] : pos_list[8] + size_list[8]])
    data9 = bytes(data[pos_list[9] : pos_list[9] + size_list[9]])

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


def perf_hash_latency(loops: int, f: Callable, size: int) -> float:
    """Benchmark a hash function with overhead costs with varying data sizes.

    Based on xxHash's ``benchLatency`` function.
    https://github.com/Cyan4973/xxHash/blob/dev/tests/bench/benchHash.c

    Args:
        loops: The number of outer loops to run.
        f: The hash function to benchmark
        size: The size of the buffer to hash.

    Returns:
        The time taken to hash the buffer in fractional seconds.
    """
    # pylint: disable=too-many-locals

    if size <= 0:
        raise ValueError("size must be greater than 0")

    range_it = itertools.repeat(None, loops)
    random.seed(42)

    n = 0

    size0 = generate_size(size, 0.1)
    size1 = generate_size(size, 0.1)
    size2 = generate_size(size, 0.1)
    size3 = generate_size(size, 0.1)
    size4 = generate_size(size, 0.1)
    size5 = generate_size(size, 0.1)
    size6 = generate_size(size, 0.1)
    size7 = generate_size(size, 0.1)
    size8 = generate_size(size, 0.1)
    size9 = generate_size(size, 0.1)

    data = bytearray(math.floor(size * 1.1) + 255)
    view_to_hash = memoryview(bytes(init_buffer(data)))

    t0 = time.perf_counter()
    for _ in range_it:
        n = f(view_to_hash[n : n + size0])[0]
        n = f(view_to_hash[n : n + size1])[0]
        n = f(view_to_hash[n : n + size2])[0]
        n = f(view_to_hash[n : n + size3])[0]
        n = f(view_to_hash[n : n + size4])[0]
        n = f(view_to_hash[n : n + size5])[0]
        n = f(view_to_hash[n : n + size6])[0]
        n = f(view_to_hash[n : n + size7])[0]
        n = f(view_to_hash[n : n + size8])[0]
        n = f(view_to_hash[n : n + size9])[0]

    return time.perf_counter() - t0


def add_cmdline_args(cmd: list, args) -> None:
    """Add command line arguments to the runner.

    Args:
        cmd: The command line arguments to extend.
        args: The parsed command line arguments.
    """
    cmd.extend(("--test-hash", args.test_hash))
    cmd.extend(("--test-type", args.test_type))
    cmd.extend(("--test-buffer-size-max", str(args.test_buffer_size_max)))


# "if hasattr" is used to check for the existence of the function in the
# module, to compare the performance of the current implementation with the
# old one (version 4.1.0), which does not implement the new functions.
# These conditions should be removed in the future.
HASHES = {
    "mmh3_base_hash": mmh3.hash,
    "mmh3_32": (
        mmh3.mmh3_32_digest if hasattr(mmh3, "mmh3_32_digest") else mmh3.hash_bytes
    ),
    "mmh3_128": (
        mmh3.mmh3_x64_128_digest
        if hasattr(mmh3, "mmh3_x64_128_digest")
        else mmh3.hash128
    ),
    "xxh_32": xxhash.xxh32_digest,
    "xxh_64": xxhash.xxh64_digest,
    "xxh3_64": xxhash.xxh3_64_digest,
    "xxh3_128": xxhash.xxh3_128_digest,
    "md5": lambda ba: hashlib.md5(ba).digest(),
    "sha1": lambda ba: hashlib.sha1(ba).digest(),
    "pymmh3_32": pymmh3.hash,
    "pymmh3_128": pymmh3.hash128,
}

BENCHMARKING_TYPES = {
    "naive": perf_hash,
    "random": perf_hash_random,
    "latency": perf_hash_latency,
}


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
        "--test-type",
        type=str,
        help="Type of benchmarking to perform (experimental)",
        choices=BENCHMARKING_TYPES.keys(),
        default="random",
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
            BENCHMARKING_TYPES[process_args.test_type],
            HASHES[process_args.test_hash],
            fib1,
            inner_loops=10,
        )
        fib1, fib2 = fib2, fib1 + fib2
