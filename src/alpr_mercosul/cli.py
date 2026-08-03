from __future__ import annotations

import argparse
from pathlib import Path

from alpr_mercosul.benchmark import run_benchmark
from alpr_mercosul.fixture import generate_dataset
from alpr_mercosul.ocr import evaluate_plate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="alpr-mercosul: synthetic plate OCR")
    subparsers = parser.add_subparsers(dest="command", required=True)

    benchmark_parser = subparsers.add_parser("benchmark", help="run benchmark")
    benchmark_parser.add_argument("--n-plates", type=int, default=100)
    benchmark_parser.add_argument("--seed", type=int, default=42)
    benchmark_parser.add_argument("--output", type=Path, default=None)

    demo_parser = subparsers.add_parser("demo", help="run quick demo")
    demo_parser.add_argument("--n-plates", type=int, default=5)
    demo_parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args(argv)
    if args.command == "benchmark":
        result = run_benchmark(args.n_plates, args.seed, args.output)
        print(f"character_accuracy={result.value:.6f}")
        print(f"plate_accuracy={result.metrics['plate_accuracy']:.6f}")
        return 0

    plates_data = generate_dataset(args.n_plates, args.seed)
    print("Mercosul Synthetic Plate OCR Demo")
    print(f"{'Plate':>12s} | {'Predicted':>12s} | {'Correct':>8s}")
    print("-" * 38)
    for image, ground_truth in plates_data:
        result = evaluate_plate(image, ground_truth)
        mark = "OK" if result.correct else "FAIL"
        print(f"{result.plate:>12s} | {result.predicted:>12s} | {mark:>8s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
