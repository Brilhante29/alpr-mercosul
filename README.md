# #5 alpr-mercosul

**Status:** scaffold

**Proves:** leitura de placa Mercosul.

**Benchmark target:** character_accuracy, plate_accuracy.

**Stack:** python, opencv, ultralytics, paddleocr, docker.

## Next milestone

Implement the smallest Docker-runnable version and produce the first JSON benchmark under enchmarks/results/.

## Run

`ash
docker build -t alpr-mercosul .
docker run --rm alpr-mercosul
`

## Benchmark

`ash
docker run --rm alpr-mercosul benchmark
`

| Metric | Value | Unit |
|---|---:|---|
| character_accuracy, plate_accuracy | pending | pending |

## Architecture

Defined in sdd/spec.md before implementation.

## References

See REFERENCES.md.