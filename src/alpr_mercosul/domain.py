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
    metrics: dict[str, float | int]
    proof: dict[str, Any]
    failures: int
    plates: list[dict[str, Any]]

    def to_json(self, path: Path) -> None:
        path.write_text(json.dumps(dataclasses.asdict(self), indent=2))

    @staticmethod
    def from_metrics(
        character_accuracy: float,
        plate_accuracy: float,
        n_plates: int,
        seed: int,
        command: str,
        output_path: Path,
        plates: list[PlateResult],
        ocr_backend: str,
    ) -> BenchmarkResult:
        incorrect_plates = sum(not plate.correct for plate in plates)
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
                "ocr_backend": ocr_backend,
            },
            metrics={
                "character_accuracy": character_accuracy,
                "plate_accuracy": plate_accuracy,
                "total_plates": n_plates,
                "correct_plates": n_plates - incorrect_plates,
                "correct_characters": sum(
                    plate.total_characters - plate.character_errors for plate in plates
                ),
                "total_characters": sum(plate.total_characters for plate in plates),
            },
            proof={
                "fixture": "synthetic-fixed-layout",
                "fixture_generator": "alpr_mercosul.fixture.generate_plate",
                "ocr_backend": ocr_backend,
                "prediction_input": "image_pixels_only",
                "plate_format": "LLL1L23",
            },
            failures=incorrect_plates,
            plates=[
                {
                    "plate": plate.plate,
                    "predicted": plate.predicted,
                    "correct": plate.correct,
                    "character_errors": plate.character_errors,
                }
                for plate in plates
            ],
        )
