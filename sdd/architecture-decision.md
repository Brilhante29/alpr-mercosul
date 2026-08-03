# Architecture Decision

## Status

Accepted

## Problem Forces

- Domain complexity: low.
- Data and ML reproducibility: high.
- Integration pressure: low.
- Auditability: high because prediction must not access labels.
- Independent deployability: low.

## Decision

Use a single-process pipeline:

```text
rendering contract -> synthetic fixture -> image-only OCR -> evaluation -> V1/V2 evidence
```

Dependency direction:

- `domain.py` depends only on the standard library.
- `rendering.py` owns glyph geometry and Pillow rendering.
- `fixture.py` creates labeled images using the rendering contract.
- `ocr.py` receives only image pixels and returns a prediction; it never receives ground truth.
- `benchmark.py` owns orchestration and compares predictions with labels.
- `cli.py` is the composition boundary.

## Rejected Alternatives

| Alternative | Reason |
|---|---|
| Hexagonal architecture | There is no infrastructure or transport adapter in the current scope. The critical boundary is label isolation, which modules and signatures enforce directly. |
| MVC or MVVM | There is no interactive UI state. |
| Microservices | One deterministic CPU pipeline has no independent deployment boundary. |

## Tests

- Unit: result calculation, renderer validation and invalid workload.
- Behavioral: 100 seeded images are read from pixels.
- Negative: replacing one rendered cell changes prediction while the expected label remains unchanged.
- Integration: CLI/Docker writes V1 JSON and the shared producer emits V2 provenance.

## Consequences

The result is truthful for a narrow synthetic fixed-layout workload and reproducible without network or GPU. Generalization to real imagery is intentionally unproven and must use a new workload version, dataset provenance and architecture review.
