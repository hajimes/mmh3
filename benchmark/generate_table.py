# pylint: disable=R0801
"""An ad-hoc script to generate a markdown table of benchmarking results.

This file should be incoporated into the main plot module before merging into
the main branch.
"""

import argparse
import hashlib
import os
from typing import TypeVar

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
    "mmh3_base_hash": mmh3.mmh3_32().digest_size,
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

XXHASH_REFERENCE = {
    "mmh3_32": 3.9,
    "mmh3_128": None,
    "xxh_32": 9.7,
    "xxh_64": 9.1,
    "xxh3_64": 31.5,
    "xxh3_128": 29.6,
    "md5": 0.6,
    "sha1": 0.8,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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

    df_t = df_latency.copy()
    df_t = df_t[df_t.index <= 256]

    small_data_velocity = 0.000001 / df_t.mean()

    max_row = df_latency.iloc[-1]

    max_row = float(index[-1]) / max_row
    max_row = max_row / (2**30)

    input_bandwidth_df = pd.DataFrame(max_row)
    input_bandwidth_df.index.name = "Hash"
    input_bandwidth_df.columns = ["Bandwidth"]

    digest_size_series = pd.Series(DIGEST_SIZES)[ordered_hash_names]
    input_bandwidth_df["Width"] = digest_size_series * 8
    input_bandwidth_df.sort_values("Bandwidth", ascending=False, inplace=True)
    input_bandwidth_df = input_bandwidth_df[["Width", "Bandwidth"]]

    input_bandwidth_df["Small Data Velocity"] = small_data_velocity

    input_bandwidth_df["✕ Width"] = (
        input_bandwidth_df["Width"] * input_bandwidth_df["Small Data Velocity"]
    ).round(0)

    input_bandwidth_df["cf. Collet (2020)"] = pd.Series(XXHASH_REFERENCE)

    # Prettify the table
    input_bandwidth_df["Bandwidth"] = input_bandwidth_df["Bandwidth"].map(
        lambda x: f"{x:.2f} GiB/s"
    )
    input_bandwidth_df["Small Data Velocity"] = input_bandwidth_df[
        "Small Data Velocity"
    ].map(lambda x: f"{x:.2f}")
    input_bandwidth_df["cf. Collet (2020)"] = input_bandwidth_df[
        "cf. Collet (2020)"
    ].map(lambda x: f"{x:.1f} GiB/s" if pd.notna(x) else "N/A")

    print(input_bandwidth_df.to_markdown())
