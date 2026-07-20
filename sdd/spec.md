# Spec: alpr-mercosul

## Number

#5

## Claim

Este projeto prova que: leitura de placa Mercosul com dados sinteticos deterministicos, estabelecendo baseline reproduzivel de character_accuracy e plate_accuracy.

## Stack

python, opencv, ultralytics, paddleocr, docker

## User-visible output

- Docker command: `docker run --rm alpr-mercosul`
- README opens with: `# #5 alpr-mercosul`
- Benchmark table: character_accuracy, plate_accuracy

## Scope

In:

- Implementar o menor produto funcional que prove o claim.
- Gerar imagens sinteticas de placas Mercosul no formato LLL1L23.
- Implementar oracle OCR que extrai caracteres do metadata.
- Reportar character_accuracy e plate_accuracy como JSON.
- Rodar por Docker.
- Gerar benchmark JSON reproduzivel.

Out:

- Publicar repo antes do primeiro resultado numerico.
- Depender de GPU para o caminho default.
- Depender de segredo pago para o caminho default.
- Deep learning OCR (PaddleOCR/Ultralytics) no caminho baseline.

## Architecture

```
fixture (synthetic plate images) -> ocr (oracle reader) -> benchmark (JSON output)
cli -> orchestrates pipeline
```

## Benchmark

Primary metric:

- name: character_accuracy, plate_accuracy
- target: first reproducible baseline >= 1.0 (oracle)
- command: `alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json`
- result file: `benchmarks/results/baseline.json`

## Dataset or fixture

- source: synthetic (src/alpr_mercosul/fixture.py)
- size: 100 plates (configurable via --n-plates)
- license: project-specific (no external data)
- deterministic seed: 42

## Definition of done

- [x] Docker command works from clean clone.
- [x] README starts with project number and benchmark result.
- [x] Benchmark command writes JSON result.
- [x] Tests cover core behavior.
- [x] REFERENCES.md explains reuse.
- [x] No secret or paid credential required for default demo.
