from __future__ import annotations

import dataclasses
import json
import platform
import time
from pathlib import Path
from typing import Any


@dataclasses.dataclass(frozen=True)
class PlateResult:
    plate: str
    predicted: str
    correct: bool
    character_errors: int
    total_characters: int


@dataclasses.dataclass(frozen=True)
class BenchmarkResult:
    project: str
    metric: str
    value: float
    unit: str
    timestamp: str
    command: str
    environment: dict[str, Any]
    metrics: dict[str, float]
    proof: dict[str, Any]
    failures: int
    plates: list[dict[str, Any]]

    def to_json(self, path: Path) -> None:
        path.write_text(
            json.dumps(dataclasses.asdict(self), indent=2, default=str)
        )

    @staticmethod
    def from_metrics(
        character_accuracy: float,
        plate_accuracy: float,
        n_plates: int,
        seed: int,
        command: str,
        output_path: Path,
        plates: list[PlateResult],
    ) -> BenchmarkResult:
        return BenchmarkResult(
            project="5-alpr-mercosul",
            metric="character_accuracy",
            value=character_accuracy,
            unit="unit",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            command=command,
            environment={
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "seed": seed,
                "n_plates": n_plates,
                "ocr_backend": "oracle",
            },
            metrics={
                "character_accuracy": character_accuracy,
                "plate_accuracy": plate_accuracy,
                "total_plates": n_plates,
                "correct_plates": sum(1 for p in plates if p.correct),
                "correct_characters": sum(
                    p.total_characters - p.character_errors
                    for p in plates
                ),
                "total_characters": sum(p.total_characters for p in plates),
            },
            proof={
                "fixture": "synthetic",
                "fixture_generator": "alpr_mercosul.fixture.generate_plate",
                "ocr_backend": "oracle",
                "plate_format": "LLL1L23",
            },
            failures=0,
            plates=[
                {
                    "plate": p.plate,
                    "predicted": p.predicted,
                    "correct": p.correct,
                    "character_errors": p.character_errors,
                }
                for p in plates
            ],
        )
