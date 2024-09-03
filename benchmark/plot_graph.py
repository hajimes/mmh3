import argparse
import hashlib
import os

import matplotlib.pyplot as plt
import mmh3
import pandas as pd
import pyperf
import xxhash

DIGEST_SIZES = {
    "mmh3_32": mmh3.mmh3_32().digest_size,
    "mmh3_128": mmh3.mmh3_x64_128().digest_size,
    "md5": hashlib.md5().digest_size,
    "sha1": hashlib.sha1().digest_size,
    "xxh_32": xxhash.xxh32().digest_size,
    "xxh_64": xxhash.xxh64().digest_size,
    "xxh3_64": xxhash.xxh3_64().digest_size,
    "xxh3_128": xxhash.xxh3_128().digest_size,
    "pymmh3_32": mmh3.mmh3_32().digest_size,
    "pymmh3_128": mmh3.mmh3_x64_128().digest_size,
}

LATENCY_FILE_NAME = "latency.png"
LATENCY_SMALL_FILE_NAME = "latency_small.png"
OUTPUT_BANDWIDTH_FILE_NAME = "output_bandwidth.png"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    data_result = {}
    data_digest_size_result = {}
    index = []

    for file_name in args.filenames:
        suite = pyperf.BenchmarkSuite.load(file_name)
        base_name = os.path.basename(file_name)
        hash_name = os.path.splitext(base_name)[0]

        data_result[hash_name] = []
        data_digest_size_result[hash_name] = []
        index = []

        for bench_name in suite.get_benchmark_names():
            bench = suite.get_benchmark(bench_name)
            data_size = int(bench_name.split(" ")[0])
            index.append(data_size)
            latency_ns = bench.median() * 1000 * 1000 * 1000
            data_result[hash_name].append(latency_ns)
            data_digest_size_result[hash_name].append(
                (DIGEST_SIZES[hash_name] / bench.median()) / 1024
            )

    df = pd.DataFrame(data_result, index=index)
    df2 = pd.DataFrame(data_digest_size_result, index=index)

    plt.rcParams["figure.dpi"] = 72 * 3

    plt.figure()

    df.plot(xlabel="Input size (bytes)", ylabel="Benchmark time (ns)")
    plt.savefig(LATENCY_FILE_NAME)

    df_small_data = df[df.index < 256]
    df_small_data.plot(
        xlabel="Input size (bytes)", ylabel="Benchmark time (ns)", logy=True
    )
    plt.savefig(LATENCY_SMALL_FILE_NAME)

    df2.plot(xlabel="Input size (bytes)", ylabel="Output bandwidth (kB/s)", logy=True)
    plt.savefig(OUTPUT_BANDWIDTH_FILE_NAME)

    plt.close("all")
