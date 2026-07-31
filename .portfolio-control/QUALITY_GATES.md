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
- [x] RESOLVED: the "Validate portfolio contract" blocker is closed.
      Two defects were behind it.

      1. Silent reporting. `tools/validate-project.ps1` sets
         `$ErrorActionPreference = "Stop"`, which makes `Write-Error` terminating,
         so `$failures | ForEach-Object { Write-Error $_ }` threw on the first
         entry and neither the remaining failures nor the explicit `exit 1` ran.
         With three broken gates the script printed nothing on stdout and one
         failure on stderr, so no CI log named the failing gate. Fixed by listing
         every failure and emitting `::error::` annotations under Actions.

      2. Wrong test runner. With reporting fixed, CI named the gate:
         `python unittest failed with exit code 5`. The tests are pytest-style,
         so `unittest discover` collects zero tests — exit 0 on Python 3.11
         (a false green, and why three local repros passed) but exit 5 on
         Python 3.12, which `setup-python` installs. Fixed by selecting pytest
         when the project configures it.

      A third defect was introduced and fixed during the work: the validator now
      runs pytest, so a happy-path test invoking the validator from inside that
      suite recursed until the job was killed (run 30639032942, exit 143). That
      test was removed; the green path is covered by this CI step.

      Evidence: run 30640505436 on head 8c046de — every step success, including
      Validate portfolio contract, Build image, Run demo and Run benchmark.
      https://github.com/Brilhante29/alpr-mercosul/actions/runs/30640505436
