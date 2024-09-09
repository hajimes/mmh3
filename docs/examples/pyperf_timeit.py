import pyperf

# pyperf.Runner() spawns multiple processes to run the benchmark
# use `python -o result.json this.py`` to retrieve the final result
runner = pyperf.Runner()
runner.timeit(name="hex", stmt="for i in it: hex(i)", setup="it=range(10)")
