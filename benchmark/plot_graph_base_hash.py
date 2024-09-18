# pylint: disable=R0801
"""An ad-hoc script to plot the graph of the benchmark results for mmh3.hash.

This file should be incoporated into the main plot module in the future.
"""

import argparse
import os
from typing import TypeVar

import matplotlib.pyplot as plt
import mmh3
import pandas as pd
import pyperf

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
    "mmh3_base_hash_500": mmh3.mmh3_32().digest_size,
    "mmh3_base_hash_410": mmh3.mmh3_32().digest_size,
    "mmh3_32_500": mmh3.mmh3_32().digest_size,
}

LATENCY_FILE_NAME = "latency_hash.png"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    result_latency: dict[str, list[float]] = {}
    index: list[int] = []

    for file_name in args.filenames:
        suite = pyperf.BenchmarkSuite.load(file_name)
        base_name = os.path.basename(file_name)
        hash_name = os.path.splitext(base_name)[0]

        result_latency[hash_name] = []
        index = []

        for bench_name in suite.get_benchmark_names():
            bench = suite.get_benchmark(bench_name)
            data_size = int(bench_name.split(" ")[0])
            index.append(data_size)
            latency_seconds = bench.median()

            result_latency[hash_name].append(latency_seconds)

    result_latency = pad_with_nan(result_latency)

    ordered_hash_names = ordered_intersection(
        list(DIGEST_SIZES.keys()), list(result_latency.keys())
    )

    df_latency = pd.DataFrame(result_latency, index=index)
    df_latency = df_latency[ordered_hash_names]

    plt.rcParams["figure.dpi"] = 72 * 3

    plt.figure()

    df_latency_small = df_latency * 1000 * 1000 * 1000
    df_latency_small = df_latency_small.drop(columns=["mmh3_32_500"])
    df_latency_small = df_latency_small.rename(
        columns={
            "mmh3_base_hash_410": "hash() in mmh3 4.1.0",
            "mmh3_base_hash_500": "hash() in mmh3 5.0.0",
        }
    )
    df_latency_small = df_latency_small[df_latency_small.index <= 2**12]
    df_latency_small.plot(xlabel="Input size (bytes)", ylabel="Latency (ns)")
    plt.savefig(os.path.join(args.output_dir, LATENCY_FILE_NAME))

    plt.close("all")
