# #5 alpr-mercosul

**Measured result:** `1.000000` character accuracy on `700` characters from `100` synthetic Mercosul-format plates; `1.000000` full-plate accuracy and `0` failures.

**Status:** published. The provenance-rich V2 evidence binds the clean benchmark source, immutable OCI image, workload, fixture, dependency lock and raw V1 result.

**Proves:** deterministic `LLL1L23` plate OCR from synthetic image pixels. The reader receives no ground-truth text.

**Stack:** Python 3.12, Pillow 10.4.0, NumPy 1.26.4, pytest, Docker

## Benchmark

| Metric | Value | Workload |
|---|---:|---:|
| Character accuracy | 1.000000 | 700 characters |
| Full-plate accuracy | 1.000000 | 100 plates |
| Incorrect plates | 0 | 100 plates |

Publication semantics: one independent run (`repeat=1`) measuring 100 plates (`measured_iterations=100`). The clean source commit is `b23be43`; the executed image digest is `sha256:399b8ba8e00b4855fb0d7605682899a7b02345b3e31237a7755aa97f8f748e37`.

## Evidence Scope

The versioned workload renders 100 seeded plates at 200x80 with 800 controlled dark-noise pixels per image. A fixed-layout template matcher predicts seven characters from each image. Ground truth is used only after prediction to calculate accuracy.

This is a synthetic OCR baseline. It does not claim vehicle detection, plate localization, perspective correction, real-road generalization, or production accuracy.

## Architecture

```text
glyph rendering contract -> synthetic fixture -> image-only OCR -> evaluation -> JSON evidence
```

The boundary is executable: `read_plate(image) -> str`. A negative test replaces one glyph in the image while preserving the expected label and confirms that prediction follows changed pixels.

## Run

```bash
docker build -t alpr-mercosul .
docker run --rm alpr-mercosul
```

## Commands

| Command | Purpose |
|---|---|
| `alpr-mercosul demo --n-plates 5 --seed 42` | Show expected and image-derived predictions. |
| `alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json` | Produce raw V1 evidence. |
| `./tools/publish-benchmark.ps1` | Build the image and produce V1 plus provenance-rich V2 evidence. |
| `./tools/validate-project.ps1` | Run project, test, content and Docker gates. |

## Reproducibility

- Workload config: `benchmarks/config/alpr-synthetic-v1.json`.
- Raw result: `benchmarks/results/baseline.json`.
- V2 result: `benchmarks/publication/alpr-baseline-v2.json`.
- Exact runtime pins: `requirements.txt` and the Docker base digest.
- Shared producer and Codex/Claude skills are synchronized from `portfolio-reuse-kit`.

## References

See [REFERENCES.md](REFERENCES.md).
