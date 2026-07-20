# #5 alpr-mercosul

**Status:** benchmarked

**Proves:** leitura de placa Mercosul (Mercosul license plate reading) with deterministic synthetic data and oracle OCR baseline.

**Stack:** python, pillow, numpy, docker

## Benchmark

`python -m alpr_mercosul benchmark --n-plates 100 --seed 42`

| Metric | Value | Unit |
|---|---:|---|
| character_accuracy | 1.000000 | unit |
| plate_accuracy | 1.000000 | unit |
| total_plates | 100 | count |
| correct_plates | 100 | count |
| total_characters | 700 | count |
| correct_characters | 700 | count |

*Environment: Python 3.10.11, seed=42, oracle OCR backend.*

## Architecture

```
fixture (synthetic plate image generation) -> ocr (oracle reader) -> benchmark (JSON output)
cli -> orchestrates pipeline
```

Mercosul plates follow the pattern `LLL1L23` (3 letters, 1 digit, 1 letter, 2 digits). The fixture generates random valid plates and renders them as synthetic images with blue border and controlled noise. The oracle OCR reads the ground truth from metadata (simulating perfect OCR) and character-level accuracy is computed against the expected plate.

## Run

```bash
docker build -t alpr-mercosul .
docker run --rm alpr-mercosul
```

## Commands

| Command | Description |
|---|---|
| `alpr-mercosul demo` | Show sample plate readings |
| `alpr-mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json` | Run full benchmark |

## Benchmark

```bash
docker run --rm alpr-mercosul benchmark
```

Or natively:

```bash
pip install -e .
python -m alpr_mercosul benchmark --n-plates 100 --seed 42 --output benchmarks/results/baseline.json
```

## References

See REFERENCES.md.
