PYTHON = python3
TARGET_GRAPH = docs/images/throughput_small_inputs.png

default:
	pip install .

benchmark: $(TARGET_GRAPH)

$(TARGET_GRAPH): benchmark/benchmark.py
	$(PYTHON) benchmark/benchmark.py