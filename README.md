# #5 alpr-mercosul

**Status:** implementation verified; publication evidence is being regenerated

**Proves:** deterministic Mercosul-format plate OCR from synthetic image pixels. The reader receives no ground-truth text.

**Stack:** Python 3.12, Pillow 10.4.0, NumPy 1.26.4, pytest, Docker

## Evidence Scope

The workload contains 100 seeded `LLL1L23` plates rendered at 200x80 with controlled pixel noise. A fixed-layout template matcher predicts seven characters from the image. Ground truth is used only after prediction to calculate character and plate accuracy.

This is a synthetic OCR baseline. It does not claim vehicle detection, plate localization, perspective correction, real-road generalization, or production accuracy.

## Architecture

```text
glyph rendering contract -> synthetic fixture -> image-only OCR -> evaluation -> JSON evidence
```

The critical boundary is enforced by the API: `read_plate(image) -> str`. A negative test replaces one glyph in the image while preserving the expected label and confirms that the prediction follows the changed pixels.

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

- Publication workload: `benchmarks/config/alpr-synthetic-v1.json`.
- Runtime dependencies: exact versions in `requirements.txt` and installed by Docker.
- Publication producer: `tools/generate-publication-benchmark.py`, synchronized from `portfolio-reuse-kit`.
- `execution.repeat` counts runs; `workload.measured_iterations` counts plates.

## References

See [REFERENCES.md](REFERENCES.md).
