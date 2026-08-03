# Benchmark Proof

Canonical sources: `sdd/benchmark-plan.md`, `benchmarks/config/alpr-synthetic-v1.json`, V1 and V2 JSON artifacts.

## Claim

The `template-matching-v1` reader predicts 700/700 characters and 100/100 complete plates from 100 deterministic synthetic images without receiving ground truth.

## Evidence

- Source commit: `b23be43c2f11168218a14520f6dc02dafbe501a0`.
- V1: `benchmarks/results/baseline.json`.
- V2: `benchmarks/publication/alpr-baseline-v2.json`.
- Character accuracy: `1.0`.
- Plate accuracy: `1.0`.
- Failures: `0`.
- Execution repetitions: `1`.
- Measured plates: `100`.
- Image digest: `sha256:399b8ba8e00b4855fb0d7605682899a7b02345b3e31237a7755aa97f8f748e37`.

## Limit

This proves a synthetic fixed-layout OCR workload only. Real-road detection and generalization remain out of scope.
