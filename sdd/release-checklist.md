# Release Checklist

- [x] Docker base and runtime dependencies are pinned.
- [x] `docker build` and one-container default path pass.
- [x] Reader predicts from image pixels without a ground-truth argument.
- [x] Pixel-mutation negative test detects label leakage.
- [x] Zero-workload benchmark is rejected.
- [x] Raw V1 result contains 100 plate records and 700 characters.
- [x] V2 reports `repeat=1` and `measured_iterations=100`.
- [x] V2 source, fixture, config, lock, artifact and image digests are recorded.
- [x] README opens with the measured number and synthetic scope.
- [x] References, SDD, reuse review and OpenSpec artifacts agree.
- [x] Default path requires no network credential or paid secret.
- [x] Exact-head GitHub Actions is green for evidence commit `f22c834` (run `30778167462`).
- [x] Central publication evidence for the evidence commit is embedded and externally verifiable.
