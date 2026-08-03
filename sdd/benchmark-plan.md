# Benchmark Plan: alpr-mercosul

## Hypothesis

The image-only template matcher can decode deterministic synthetic Mercosul-format plates without label leakage.

## Workload

- Config: `benchmarks/config/alpr-synthetic-v1.json`.
- 100 plates and 700 characters.
- Seed 42.
- Fixed 200x80 images with 800 deterministic dark-noise pixels each.
- One measured run, no warmup, concurrency one.

`execution.repeat` counts independent runs. `workload.measured_iterations` counts plates, so this workload must report `repeat=1` and `measured_iterations=100`.

## Commands

```powershell
alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json
./tools/publish-benchmark.ps1
```

## Metrics

| Metric | Unit | Direction | Meaning |
|---|---|---|---|
| `character_accuracy` | unit | higher | correctly decoded characters / 700 |
| `plate_accuracy` | unit | higher | completely correct plates / 100 |
| `failures` | count | lower | plates with at least one wrong character |

## Required Evidence

- Raw V1 JSON retains all 100 expected/predicted pairs.
- V2 metric value and samples match V1.
- V2 workload equals V1 `metrics.total_plates` and `environment.n_plates`.
- Reader signature and mutation test prove prediction cannot consume ground truth.
- Source tree is clean before execution and the Docker image digest is immutable.
- README labels the result synthetic and does not imply real-road accuracy.
