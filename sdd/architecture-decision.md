# Architecture Decision

## Status

Accepted

## Context

Project: `5 - alpr-mercosul`
Claim: leitura de placa Mercosul
Benchmark: character_accuracy, plate_accuracy

Problem forces:

- Domain complexity: low
- Integration pressure: low
- UI state complexity: none
- Data/ML reproducibility: high
- Auditability/event history: medium
- Throughput/async pressure: low
- Independent deployability need: low

## Decision

Chosen architecture: `pipeline`

Reason:

A three-stage pipeline (fixture generation -> OCR reading -> benchmark output) maps directly to the problem. Data flows in one direction with no branching, state machine, or event loop. The CLI wraps all three stages and provides `demo` and `benchmark` subcommands.

Dependency rule:

fixture depends only on Pillow; OCR depends on domain types; benchmark depends on fixture and OCR; CLI depends on all three inward.

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| hexagonal | No infrastructure boundary worth isolating; no ports/adapters needed without cloud, database, or transport |
| microservices | Single-process pipeline has no deploy boundary; splitting adds distributed cost without benefit |

## Folder Layout

```
src/
  alpr_mercosul/
    __init__.py
    __main__.py
    cli.py
    domain.py
    fixture.py
    ocr.py
    benchmark.py
tests/
  test_domain.py
  test_ocr.py
benchmarks/
  results/
    baseline.json
```

## Testing Strategy

- Unit tests: domain types (PlateResult, BenchmarkResult construction and serialization)
- Integration tests: oracle OCR correctness with known plates
- Benchmark: full pipeline via CLI or Docker, outputs JSON to benchmarks/results/

## Consequences

Positive:

- Simple three-stage pipeline is easy to understand and modify.
- Deterministic synthetic data ensures reproducible benchmarks across environments.
- No external dependencies for default path.

Tradeoffs:

- Oracle OCR assumes perfect reading; real-world accuracy would be lower.
- Synthetic plates may not reflect real-world imaging conditions; the claim is about OCR benchmark reproducibility, not production-grade recognition.
