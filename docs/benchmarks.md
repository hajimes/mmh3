# Benchmarks

## Settings
- Python environment
  - CPython 3.12.5 (64-bit)
- Ubuntu 22.04 instance on GitHub Actions
- Hash libraries
  - mmh3 4.2.0: dev version
  - xxhash 3.5.0
- pyperf 2.7.0

## Results

### Graphs

```{figure} _static/bandwidth.png
:alt: Latency
:align: center

Figure 1: Output bandwidth. Larger is better. The y-axis is logscale.
```

```{figure} _static/bandwidth_small.png
:alt: Latency
:align: center

Figure 2: Output bandwidth for small data. Larger is better.
```

```{figure} _static/latency.png
:alt: Latency
:align: center

Figure 3: Latency. Smaller is better.
```

```{figure} _static/latency_small.png
:alt: Latency
:align: center

Figure 4: Latency for small data. Smaller is better.
```