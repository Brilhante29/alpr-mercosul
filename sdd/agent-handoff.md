# Agent Handoff

Project: `5 - alpr-mercosul`

## Current State

- Oracle label leakage: removed from benchmark and demo paths.
- Reader contract: `read_plate(image) -> str`.
- Backend: `template-matching-v1` over synthetic fixed-layout plate pixels.
- Clean benchmark source: `b23be43c2f11168218a14520f6dc02dafbe501a0`.
- V1: 100 plates, 700 characters, 1.0 character accuracy, 1.0 plate accuracy, zero failures.
- V2: `repeat=1`, `measured_iterations=100`, clean source and immutable image digest.
- Local tests, Ruff, project validator, Docker demo and Docker benchmark: passed.
- Publication status: benchmarked; exact-head CI and central evidence remain.

## Decision Chain

| Decision | Evidence | Status |
|---|---|---|
| Keep pipeline architecture | no transport, database, broker or deployment boundary | accepted |
| Replace oracle with image-only matcher | oracle returned the answer and made accuracy tautological | completed |
| Keep synthetic fixed-layout workload | deterministic first proof; real-road data requires separate provenance | accepted with explicit limit |
| Reuse generic V2 producer | V1 exposes two concordant workload counts | completed |
| Keep ALPR rendering and matching local | business-specific and not proven reusable by a second project | local |

## Invariants

- Prediction never accepts ground truth or metadata.
- `n_plates` is at least one.
- Workload version 1.0.0 is 100 seeded `LLL1L23` plates at 200x80.
- Geometry, renderer, noise, backend or dataset changes require a new workload version or comparability key.
- Synthetic accuracy is never described as real-road or production accuracy.
- One publication run reports `repeat=1` and `measured_iterations=100`.

## Next Action

Commit V1/V2 evidence and final documentation, push the branch, require exact-head CI, inspect every job step, then promote to published and refresh central evidence.
