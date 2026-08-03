# Technical Decision

## Status

Accepted

## Context

The previous oracle returned ground truth and therefore validated only the harness. It could report perfect accuracy without reading image pixels. The portfolio claim requires a real, local, reproducible OCR behavior while remaining explicit that synthetic fixed-layout data is not real-road ALPR.

## Selected Option

Use deterministic glyph template matching over seven fixed layout cells. Pillow renders a versioned monospaced bitmap fixture; NumPy compares each observed binary cell against only the characters allowed at that Mercosul position.

The reader receives only `PIL.Image.Image`. Ground truth enters `evaluate_plate` after prediction and is used solely to calculate errors.

## Rejected Options

| Option | Reason |
|---|---|
| Oracle returning metadata | Tautological and invalid as OCR accuracy evidence. |
| PaddleOCR or Ultralytics baseline | Adds model downloads, GPU and external artifact risk before a truthful local baseline exists. |
| Real-road dataset | Licensing, privacy and reproducibility require a separate dataset decision and benchmark version. |
| OpenCV dependency | Fixed cells and binary template distance need only Pillow and NumPy. |
| FastAPI | The proof target is a deterministic batch benchmark, so CLI is the smaller valid boundary. |

## Engineering Principles

- SRP: rendering, fixture generation, prediction, evaluation and serialization are separate modules.
- OCP: a later OCR backend can implement image-to-string without changing result calculation.
- LSP: any reader must predict the same seven-character contract from the image alone.
- ISP: the published reader exposes `read_plate(image) -> str`; it does not accept metadata it could leak into prediction.
- DIP: benchmark orchestration depends on prediction behavior, while metric calculation stays in the application pipeline.
- KISS/YAGNI: no model server, broker, cloud adapter or training pipeline is added.
- DRY: fixture and matcher share one versioned glyph rendering contract.

## Reproducibility

- Docker installs exact runtime versions from `requirements.txt` before installing the package with `--no-deps`.
- `benchmarks/config/alpr-synthetic-v1.json` owns workload and renderer identity.
- The V2 producer records clean source SHA, raw artifact digest, fixture/config/lock digests and image digest.
- `execution.repeat=1`; `workload.measured_iterations=100`.

## Limits

The benchmark measures OCR on synthetic, centered, fixed-size plates rendered from the same versioned glyph family used by the matcher. It does not measure plate detection, perspective correction, blur, illumination, camera artifacts, or real-road generalization.
