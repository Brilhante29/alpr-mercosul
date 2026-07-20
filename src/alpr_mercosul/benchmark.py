from __future__ import annotations

import argparse
import time
from pathlib import Path

from alpr_mercosul.domain import BenchmarkResult, PlateResult
from alpr_mercosul.fixture import generate_dataset
from alpr_mercosul.ocr import oracle_read


def run_benchmark(
    n_plates: int = 100,
    seed: int = 42,
    output_path: Path | None = None,
) -> BenchmarkResult:
    plates_data = generate_dataset(n_plates=n_plates, seed=seed)
    results: list[PlateResult] = []

    for image, ground_truth in plates_data:
        result = oracle_read(image, ground_truth)
        results.append(result)

    total_chars = sum(r.total_characters for r in results)
    total_errors = sum(r.character_errors for r in results)
    character_accuracy = (total_chars - total_errors) / total_chars if total_chars else 1.0
    plate_accuracy = sum(1 for r in results if r.correct) / len(results) if results else 1.0

    final_result = BenchmarkResult.from_metrics(
        character_accuracy=character_accuracy,
        plate_accuracy=plate_accuracy,
        n_plates=n_plates,
        seed=seed,
        command=(
            f"alpr-mercosul benchmark"
            f" --n-plates {n_plates}"
            f" --seed {seed}"
            f" --output {output_path or 'stdout'}"
        ),
        output_path=output_path or Path("benchmarks/results/default.json"),
        plates=results,
    )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_result.to_json(output_path)

    return final_result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="alpr-mercosul benchmark harness"
    )
    parser.add_argument(
        "--n-plates",
        type=int,
        default=100,
        help="number of synthetic plates",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="random seed",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="output JSON path",
    )
    args = parser.parse_args()

    result = run_benchmark(
        n_plates=args.n_plates,
        seed=args.seed,
        output_path=args.output,
    )

    print(f"character_accuracy={result.value:.6f}")
    print(f"plate_accuracy={result.metrics['plate_accuracy']:.6f}")
    print(f"total_plates={result.metrics['total_plates']}")
    print(f"correct_plates={result.metrics['correct_plates']}")
    print(f"total_characters={result.metrics['total_characters']}")
    print(f"correct_characters={result.metrics['correct_characters']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
