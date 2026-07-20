# Agent Handoff

Project: `5 - alpr-mercosul`

## Principal Agent Summary

- Objective: Leitura de placa Mercosul com dados sinteticos deterministicos.
- Portfolio program: applied-computer-vision
- Public proof claim: leitura de placa Mercosul
- Primary benchmark: character_accuracy
- Default runnable path: `docker run --rm alpr-mercosul`

## Subagent Decisions

| Role | Decision | Evidence Path | Status |
|---|---|---|---|
| `program-planner` | applied-computer-vision | `project.yaml`, `sdd/spec.md` | done |
| `architecture-selector` | pipeline | `sdd/architecture-decision.md` | done |
| `engineering-principles-reviewer` | SOLID + KISS/YAGNI | `project.yaml`, `sdd/technical-decision.md` | done |
| `stack-decision-agent` | python, pillow, numpy | `project.yaml`, `sdd/technical-decision.md` | done |
| `api-style-agent` | CLI (argparse) | CLI contract in README | done |
| `cloud-local-first-agent` | none | Docker-only runtime | done |
| `messaging-agent` | none | `sdd/technical-decision.md` | done |
| `language-profile-agent` | python-ml | repo layout, tests, tooling | done |
| `benchmark-harness-agent` | character_accuracy benchmark | `sdd/benchmark-plan.md`, `benchmarks/results/baseline.json` | done |
| `design-system-agent` | README with benchmark table | `README.md` | done |
| `security-reuse-reviewer` | no secrets, no network | `REFERENCES.md`, release checklist | done |
| `release-ci-publisher` | validation and CI | CI workflow, validation | done |

## Local-First Runtime

- Docker command: `docker run --rm alpr-mercosul`
- Local services: none
- Kumo services, if any: none
- Real cloud adapter target, if any: none
- Config switch: none
- Default path requires paid secret: no

## Architecture Boundaries

- Domain boundaries: alpr_mercosul/domain.py (pure dataclasses)
- Use-case boundaries: fixture -> ocr -> benchmark
- Ports: function signatures (generate_dataset, oracle_read, run_benchmark)
- Adapters: none (no infrastructure boundaries)
- Dependency direction rule: CLI imports benchmark/ocr/fixture; benchmark imports ocr/fixture; ocr imports domain

## Benchmark Handoff

- Metric: character_accuracy
- Unit: unit (0-1 scale)
- Higher or lower is better: higher
- Command: `alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json`
- Result path: `benchmarks/results/baseline.json`
- Dataset or fixture: synthetic (src/alpr_mercosul/fixture.py)

## Open Risks

- None

## Publication Gates

- [x] Docker path works
- [x] benchmark result exists
- [x] README starts with number, claim, and benchmark
- [x] references are documented
- [x] no secret in files or git remote
- [x] validation passes
