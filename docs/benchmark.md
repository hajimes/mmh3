# Benchmarks

## Settings

- Python environment
  - CPython 3.12.5 (64-bit)
- Ubuntu 22.04 instance on GitHub Actions
- Hash libraries
  - mmh3 5.0.0-dev
  - xxhash 3.5.0
- pyperf 2.7.0

## Results

### Graphs

```{figure} _static/latency_small.png
:alt: Latency
:align: center

Figure 2: Latency for small data. Smaller is better.
```

```{figure} _static/latency.png
:alt: Latency
:align: center

Figure 1: Latency for large data. Smaller is better.
```

```{figure} _static/bandwidth_small.png
:alt: Latency
:align: center

Figure 2: Output bandwidth for small data. Larger is better.
```

```{figure} _static/bandwidth.png
:alt: Latency
:align: center

Figure 1: Output bandwidth for large data. Larger is better. The y-axis is logscale.
```

### JSON files for the results

[mmh3-benchmarks/results/2024-09-17_30da46e](https://github.com/hajimes/mmh3-benchmarks/tree/main/results/2024-09-17_30da46e)
