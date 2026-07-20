# Technical Decision

## Status

Accepted

## Decision Type

stack, library, runtime

## Context

Project: `5 - alpr-mercosul`
Problem: Leitura de placa Mercosul com dados sinteticos deterministicos
Portfolio program: applied-computer-vision
Public signal: reproducible OCR benchmark em Docker
Benchmark: character_accuracy, plate_accuracy

## Selected Option

Selected: synthetic fixture (Pillow) + oracle OCR

Reason:

Mercosul plates seguem formato LLL1L23 (7 caracteres). A geracao de imagem sintetica com Pillow permite controle deterministico sobre o ground truth. Oracle OCR retorna o metadata diretamente, estabelecendo um baseline perfeito (accuracy=1.0) que valida o pipeline de benchmark.

## Decision Brain Fields

- Stack profile: python-ml
- API style: cli
- Messaging: none
- Cloud mode: none
- Database/runtime: none (synthetic data in memory)
- Library policy: Pillow para geracao de imagem; argparse para CLI; numpy para futuras operacoes de array

## Engineering Principles

Coupling boundary:

Domain types (PlateResult, BenchmarkResult) depend only on standard library. Fixture imports Pillow. CLI imports argparse.

SOLID application:

- SRP: fixture generation, OCR reading, and benchmark output are separate modules.
- OCP: real OCR backends (PaddleOCR, Ultralytics) can be added without modifying oracle code.
- LSP: PlateResult is substitutable for any OCR backend output shape.
- ISP: CLI depends on small function signatures (generate_dataset, oracle_read, run_benchmark).
- DIP: benchmark orchestrates high-level functions, not class hierarchies.

Simplicity:

- KISS: one fixture, one oracle OCR, one JSON output.
- YAGNI: no model serving, no experiment tracking, no hyperparameter optimization.
- DRY: character accuracy computed once by benchmark module.

Testability evidence:

- Domain types test PlateResult/ BenchmarkResult construction and JSON roundtrip.
- OCR tests verify deterministic correctness for known plates.
- No network, database, or cloud dependency required for any test.

## Rejected Options

| Option | Why rejected |
|---|---|
| PaddleOCR/Ultralytics real OCR | GPU dependency and complex installation; oracle baseline is sufficient for reproducible benchmark |
| Real license plate dataset | Network dependency and licensing risk; synthetic fixture is deterministic |
| FastAPI serving endpoint | No UI or API requirement; CLI is sufficient |

## API Contract

Contract artifact: CLI argparse (`demo`, `benchmark` subcommands)

## Cloud Local-First

Local provider: none
Real provider target: none
Config switch: none

## Benchmark Impact

Expected impact: character_accuracy = 1.0, plate_accuracy = 1.0 with 100 synthetic plates, seed 42

Validation command:

```powershell
alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/validation.json
```

## Operational Cost

- Docker services added: none
- Local demo complexity: low
- Failure case required: no

## Follow-up

- N/A
