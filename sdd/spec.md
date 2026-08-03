# Spec: alpr-mercosul

## Number

#5

## Claim

This project proves deterministic Mercosul-format plate OCR from synthetic image pixels, measured by character and full-plate accuracy. It does not claim real-road detection or production accuracy.

## Stack

Python 3.12, Pillow 10.4.0, NumPy 1.26.4, pytest, Docker.

## In Scope

- Generate deterministic `LLL1L23` plate images with controlled pixel noise.
- Predict all seven characters from image pixels without passing ground truth to the reader.
- Evaluate character accuracy, plate accuracy, failures, and workload size.
- Reject zero-item benchmarks.
- Produce V1 execution output and V2 provenance evidence through Docker.

## Out Of Scope

- Vehicle or plate localization in unconstrained photographs.
- Real-road datasets and a production accuracy claim.
- PaddleOCR, Ultralytics, GPU training, HTTP serving, cloud, or paid secrets.

## Architecture

```text
synthetic fixture -> fixed-layout pixel OCR -> benchmark evaluation -> JSON evidence
                               ^
                     shared glyph rendering contract
```

## Benchmark

- Primary metric: `character_accuracy`, higher is better.
- Secondary metric: `plate_accuracy`.
- Workload: 100 deterministic plates, 700 characters, seed 42.
- V1 command: `alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json`.
- Publication command: `./tools/publish-benchmark.ps1`.

## Definition Of Done

- [x] Reader accepts the image only; ground truth is confined to evaluation.
- [x] A pixel-mutation test proves prediction follows pixels rather than labels.
- [x] Zero workload fails.
- [x] Fresh Docker benchmark and V2 evidence are ready to commit.
- [ ] Exact-head CI and central publication evidence are green.
