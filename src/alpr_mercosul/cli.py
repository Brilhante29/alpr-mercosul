from __future__ import annotations

import argparse
import sys
from pathlib import Path

from alpr_mercosul.benchmark import run_benchmark
from alpr_mercosul.fixture import generate_dataset, generate_plate
from alpr_mercosul.ocr import oracle_read


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="alpr-mercosul: Mercosul license plate OCR"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    benchmark_parser = sub.add_parser("benchmark", help="run benchmark")
    benchmark_parser.add_argument(
        "--n-plates", type=int, default=100
    )
    benchmark_parser.add_argument("--seed", type=int, default=42)
    benchmark_parser.add_argument("--output", type=Path, default=None)

    demo_parser = sub.add_parser("demo", help="run quick demo")
    demo_parser.add_argument("--n-plates", type=int, default=5)
    demo_parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args(argv)

    if args.command == "benchmark":
        result = run_benchmark(
            n_plates=args.n_plates,
            seed=args.seed,
            output_path=args.output,
        )
        print(f"character_accuracy={result.value:.6f}")
        print(f"plate_accuracy={result.metrics['plate_accuracy']:.6f}")
        return 0

    if args.command == "demo":
        plates_data = generate_dataset(
            n_plates=args.n_plates, seed=args.seed
        )
        print(f"Mercosul License Plate OCR Demo")
        print(f"{'Plate':>12s} | {'Predicted':>12s} | {'Correct':>8s}")
        print("-" * 38)
        for image, ground_truth in plates_data:
            result = oracle_read(image, ground_truth)
            mark = "OK" if result.correct else "FAIL"
            print(
                f"{result.plate:>12s} | {result.predicted:>12s} | {mark:>8s}"
            )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
