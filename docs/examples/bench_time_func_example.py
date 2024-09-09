import itertools
import time

import pyperf


def bench_hex(loops):
    it = itertools.repeat(None, loops)
    t0 = time.perf_counter()

    for _ in it:
        hex(0)
        hex(1)
        hex(2)
        hex(3)
        hex(4)
        hex(5)
        hex(6)
        hex(7)
        hex(8)
        hex(9)

    return time.perf_counter() - t0


# pyperf.Runner() spawns multiple processes to run the benchmark
# use `python -o result.json this.py`` to retrieve the final result
runner = pyperf.Runner()
# we test hex() for 0...9, so we need to specify inner_loops = 10 here
runner.bench_time_func("hex", bench_hex, inner_loops=10)
