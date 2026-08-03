# Verification

## Local Evidence

| Gate | Result |
|---|---|
| Focused OCR/domain/benchmark tests | 11 passed |
| Full project suite | 11 passed, 1 intentional validator recursion skip |
| Ruff | passed |
| Project schema | zero errors |
| Project validator | passed |
| Docker build | passed |
| Docker demo | 5/5 correct |
| Docker benchmark | 100/100 plates, 700/700 characters |
| Codex and Claude skill validation | passed |

## Remote Evidence

| Gate | Result |
|---|---|
| Evidence commit | `f22c834ca92c14eb6ae1a6a7cd5c5c45dc354666` |
| Exact-head GitHub Actions | [run 30778167462](https://github.com/Brilhante29/alpr-mercosul/actions/runs/30778167462), all steps passed |
| Embedded publication proof | `.portfolio-control/PUBLICATION_EVIDENCE.json` |

The central `portfolio-reuse-kit` registry is authoritative for the latest metadata HEAD, avoiding a self-referential evidence file that would change the commit it attempts to identify.
