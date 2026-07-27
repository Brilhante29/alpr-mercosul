# Quality Gates: #5 alpr-mercosul

Completion requires evidence, not intent.

- [ ] README opens with `#5 <name>` and reports the current benchmark number.
- [ ] `project.yaml` names the problem, architecture, stack, primary metric, and result path.
- [ ] SDD and OpenSpec artifacts agree with the implementation.
- [ ] Domain logic is isolated from transport, persistence, broker, provider, and vendor details.
- [ ] SOLID, DRY, KISS, YAGNI, and Law of Demeter review has no unexplained exception.
- [ ] Tests cover the contract and the failure paths that affect the claim.
- [ ] Docker runs the documented default path from a clean checkout.
- [ ] CI runs the same meaningful checks without mutable dependencies or secrets.
- [ ] Benchmark writes valid JSON under `benchmarks/results/` and can be repeated.
- [ ] README, benchmark JSON, and `project.yaml` report the same primary metric.
- [ ] Reuse review records every kit improvement, backlog item, or rejected duplication.
- [ ] Independent review found no blocker and publication has not happened before this gate.

---
## Session note 2026-07-27 — CI status

- [x] Dependencies install in CI (setup-python pinned + `pip install -e ".[dev]"`).
      Fixed `ModuleNotFoundError: No module named 'PIL'`.
- [x] Real test suite executes in CI. Added explicit `pytest` step; the tests are
      pytest-style (no `unittest.TestCase`) so the validator's `unittest discover`
      collected 0 tests — a false green now closed. CI "Run tests" step: **success**
      (7 tests). Verified locally in python:3.12 container: 7 passed.
- [ ] BLOCKER: CI "Validate portfolio contract" step still fails on run 30295887717
      (head b6accd1). Not reproducible in any local Linux + pwsh 7 + Python 3.12
      container, including a clean `git archive HEAD` checkout and GitHub's exact
      pwsh preamble (`$ErrorActionPreference='stop'`, `$PSNativeCommandUseErrorActionPreference=$true`)
      — the validator prints "portfolio project validation passed" and exits 0 every time.
      Resolving this requires the GitHub Actions step log (needs authenticated access),
      which is unavailable in this environment. Handed to user.
