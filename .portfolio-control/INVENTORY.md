# Portfolio Control: #5 alpr-mercosul

- **Program:** applied-computer-vision
- **Status:** published
- **Proves:** image-only OCR on a deterministic synthetic Mercosul-format workload
- **Primary benchmark:** character accuracy over 700 characters from 100 plates

| Evidence | Location | State |
|---|---|---|
| Specification and decisions | `sdd/`, `openspec/artifacts/` | complete |
| Raw benchmark | `benchmarks/results/baseline.json` | measured |
| Publication evidence | `benchmarks/publication/alpr-baseline-v2.json` | validated |
| Pixel-mutation leakage test | `tests/` | passing |
| Reuse review | `sdd/reuse-improvement-review.md` | complete |
