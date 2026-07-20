# Benchmark Plan: alpr-mercosul

## Hypothesis

leitura de placa Mercosul, measured by character_accuracy, plate_accuracy.

## Command

```bash
alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json
```

## Environment

- OS: Linux (Docker container, python:3.12-slim)
- CPU: 1+ cores
- RAM: 256MB+
- GPU: none
- Docker version: any with Dockerfile support
- Date: recorded in result JSON

## Inputs

- fixture: synthetic (src/alpr_mercosul/fixture.py)
- dataset size: 100 plates (configurable via --n-plates)
- repetitions: 1
- warmup: none (deterministic pipeline)

## Metrics

| Metric | Unit | Source | Why it matters |
|---|---:|---|---|
| character_accuracy | unit | benchmark script | per-character OCR quality |
| plate_accuracy | unit | benchmark script | full-plate OCR correctness |

## Result schema

Output must be JSON and include project, metric, value, unit, timestamp, environment, and command. See `domain.py` BenchmarkResult for the full schema.

## Post angle

#5 alpr-mercosul: character_accuracy=1.0, plate_accuracy=1.0 as a reproducible portfolio benchmark.
