from __future__ import annotations

import argparse
from pathlib import Path

from alpr_mercosul.domain import BenchmarkResult, PlateResult
from alpr_mercosul.fixture import generate_dataset
from alpr_mercosul.ocr import evaluate_plate

OCR_BACKEND = "template-matching-v1"


def run_benchmark(
    n_plates: int = 100,
    seed: int = 42,
    output_path: Path | None = None,
) -> BenchmarkResult:
    plates_data = generate_dataset(n_plates=n_plates, seed=seed)
    results: list[PlateResult] = [
        evaluate_plate(image, ground_truth) for image, ground_truth in plates_data
    ]

    total_characters = sum(result.total_characters for result in results)
    total_errors = sum(result.character_errors for result in results)
    character_accuracy = (total_characters - total_errors) / total_characters
    plate_accuracy = sum(result.correct for result in results) / len(results)

    final_result = BenchmarkResult.from_metrics(
        character_accuracy=character_accuracy,
        plate_accuracy=plate_accuracy,
        n_plates=n_plates,
        seed=seed,
        command=(
            f"alpr-mercosul benchmark --n-plates {n_plates} --seed {seed}"
            f" --output {output_path or 'stdout'}"
        ),
        output_path=output_path or Path("benchmarks/results/default.json"),
        plates=results,
        ocr_backend=OCR_BACKEND,
    )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_result.to_json(output_path)
    return final_result


def main() -> int:
    parser = argparse.ArgumentParser(description="alpr-mercosul benchmark harness")
    parser.add_argument("--n-plates", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = run_benchmark(args.n_plates, args.seed, args.output)
    print(f"character_accuracy={result.value:.6f}")
    print(f"plate_accuracy={result.metrics['plate_accuracy']:.6f}")
    print(f"total_plates={result.metrics['total_plates']}")
    print(f"correct_plates={result.metrics['correct_plates']}")
    print(f"total_characters={result.metrics['total_characters']}")
    print(f"correct_characters={result.metrics['correct_characters']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
