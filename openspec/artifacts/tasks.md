# Tasks: alpr-mercosul

## Truthful OCR

- [x] Remove oracle prediction from benchmark and demo.
- [x] Enforce `read_plate(image) -> str`.
- [x] Add 100-image positive test.
- [x] Add pixel-mutation negative test.
- [x] Reject zero workload.

## Reproducibility

- [x] Pin Docker base, runtime, build and CI dependencies.
- [x] Version workload configuration.
- [x] Synchronize generic V2 producer and Codex/Claude skill.
- [x] Generate V1/V2 from a clean source commit.
- [x] Assert `repeat=1` and `measured_iterations=100`.

## Publication

- [x] Local project and Docker gates pass.
- [x] Exact-head GitHub Actions passes for evidence commit `f22c834`.
- [x] Central evidence is embedded and manifest status is `published`.
