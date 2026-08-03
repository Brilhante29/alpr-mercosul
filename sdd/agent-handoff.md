# Agent Handoff

Project: `5 - alpr-mercosul`

## Current State

- Oracle label leakage: removed from the benchmark and demo paths.
- Reader contract: `read_plate(image) -> str`.
- Backend: fixed-layout binary template matching over synthetic plate pixels.
- Source tests: pixel mutation, 100-plate read, invalid geometry, workload count and zero-workload rejection.
- Publication evidence: stale until regenerated from the clean source commit.

## Decision Chain

| Decision | Evidence | Status |
|---|---|---|
| Keep pipeline architecture | no transport, database, broker or deployment boundary | accepted |
| Replace oracle with image-only matcher | oracle returned the answer and made accuracy tautological | implemented |
| Keep synthetic fixed-layout workload | local, deterministic first proof; real-road dataset requires separate provenance | accepted with explicit limit |
| Reuse generic V2 producer | single V1 result has two concordant workload counts | synchronized from kit |
| Keep ALPR rendering and matching local | business-specific and not proven reusable by a second project | local |

## Invariants

- Prediction never accepts ground truth or metadata.
- `n_plates` must be at least one.
- Plate format remains `LLL1L23` for workload version 1.0.0.
- Changing geometry, renderer, noise, backend or dataset requires a new workload version or comparability key.
- Synthetic accuracy is never described as real-road or production accuracy.
- `repeat=1` and `measured_iterations=100` for the publication workload.

## Next Action

Commit the image-only source and documentation, run `tools/publish-benchmark.ps1` from that clean commit, validate V1/V2 semantics, then publish only after exact-head CI and central evidence pass.
