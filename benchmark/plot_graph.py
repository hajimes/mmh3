"""Plot the graph of the benchmark results."""

import argparse
import hashlib
import os
from typing import TypeVar

import matplotlib.pyplot as plt
import mmh3
import pandas as pd
import pyperf
import xxhash

T = TypeVar("T")


def pad_with_nan(data: dict[T, list[float]]) -> dict[T, list[float]]:
    """Pad the data with NaN values to make the length of all lists equal.

    Args:
        data: The data to pad.

    Returns:
        The padded data.
    """

    max_len = max(len(v) for v in data.values())
    for k, v in data.items():
        data[k] = v + [float("nan")] * (max_len - len(v))

    return data


def ordered_intersection(list1: list[T], list2: list[T]) -> list[T]:
    """Return the intersection of two lists in the order of the first list.

    Args:
        list1: The first list.
        list2: The second list.

    Returns:
        The intersection of the two lists in the order of the first list.
    """

    return [item for item in list1 if item in list2]


DIGEST_SIZES = {
    "mmh3_32": mmh3.mmh3_32().digest_size,
    "mmh3_128": mmh3.mmh3_x64_128().digest_size,
    "xxh_32": xxhash.xxh32().digest_size,
    "xxh_64": xxhash.xxh64().digest_size,
    "xxh3_64": xxhash.xxh3_64().digest_size,
    "xxh3_128": xxhash.xxh3_128().digest_size,
    "md5": hashlib.md5().digest_size,
    "sha1": hashlib.sha1().digest_size,
    "pymmh3_32": mmh3.mmh3_32().digest_size,
    "pymmh3_128": mmh3.mmh3_x64_128().digest_size,
}

BANDWIDTH_FILE_NAME = "bandwidth.png"
BANDWIDTH_SMALL_FILE_NAME = "bandwidth_small.png"
LATENCY_FILE_NAME = "latency.png"
LATENCY_SMALL_FILE_NAME = "latency_small.png"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    result_latency: dict[str, list[float]] = {}
    result_bandwidth: dict[str, list[float]] = {}
    index: list[int] = []

    for file_name in args.filenames:
        suite = pyperf.BenchmarkSuite.load(file_name)
        base_name = os.path.basename(file_name)
        hash_name = os.path.splitext(base_name)[0]

        result_bandwidth[hash_name] = []
        result_latency[hash_name] = []
        index = []

        for bench_name in suite.get_benchmark_names():
            bench = suite.get_benchmark(bench_name)
            data_size = int(bench_name.split(" ")[0])
            index.append(data_size)
            latency_seconds = bench.median()

            result_bandwidth[hash_name].append(
                DIGEST_SIZES[hash_name] / latency_seconds
            )
            result_latency[hash_name].append(latency_seconds)

    result_bandwidth = pad_with_nan(result_bandwidth)
    result_latency = pad_with_nan(result_latency)

    ordered_hash_names = ordered_intersection(
        list(DIGEST_SIZES.keys()), list(result_bandwidth.keys())
    )
    df_bandwidth = pd.DataFrame(result_bandwidth, index=index)
    df_bandwidth = df_bandwidth[ordered_hash_names]
    df_latency = pd.DataFrame(result_latency, index=index)
    df_latency = df_latency[ordered_hash_names]

    plt.rcParams["figure.dpi"] = 72 * 3

    plt.figure()

    df_bandwidth_all = df_bandwidth / 1024
    df_bandwidth_all.index = df_bandwidth_all.index / (1024 * 1024)
    df_bandwidth_all.plot(
        xlabel="Input size (MB)", ylabel="Output bandwidth (kB/s)", logy=True
    )
    plt.savefig(os.path.join(args.output_dir, BANDWIDTH_FILE_NAME))

    df_bandwidth_small = df_bandwidth / 1024 / 1024
    df_bandwidth_small = df_bandwidth_small.drop(columns=["md5", "sha1"])
    df_bandwidth_small = df_bandwidth_small[df_bandwidth_small.index <= 1024]
    df_bandwidth_small.plot(
        xlabel="Input size (bytes)", ylabel="Output bandwidth (MB/s)"
    )
    plt.savefig(os.path.join(args.output_dir, BANDWIDTH_SMALL_FILE_NAME))

    df_latency_all = df_latency * 1000
    df_latency_all.index = df_latency_all.index / (1024 * 1024)
    df_latency_all.plot(xlabel="Input size (MB)", ylabel="Latency (ms)")
    plt.savefig(os.path.join(args.output_dir, LATENCY_FILE_NAME))

    df_latency_small = df_latency * 1000 * 1000 * 1000
    df_latency_small = df_latency_small.drop(columns=["md5", "sha1"])
    df_latency_small = df_latency_small[df_latency_small.index <= 1024]
    df_latency_small.plot(xlabel="Input size (bytes)", ylabel="Latency (ns)")
    plt.savefig(os.path.join(args.output_dir, LATENCY_SMALL_FILE_NAME))

    df_bandwidth = pd.DataFrame(
        result_bandwidth, index=df_latency.index / (1024 * 1024)
    )

    plt.close("all")
