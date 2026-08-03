from __future__ import annotations

import json
from pathlib import Path

from alpr_mercosul.domain import BenchmarkResult, PlateResult


class TestPlateResult:
    def test_correct_plate(self):
        result = PlateResult("ABC1D23", "ABC1D23", True, 0, 7)
        assert result.correct
        assert result.character_errors == 0

    def test_wrong_plate(self):
        result = PlateResult("ABC1D23", "ABC1E23", False, 1, 7)
        assert not result.correct
        assert result.character_errors == 1


class TestBenchmarkResult:
    def test_from_metrics_records_backend_and_failures(self):
        plates = [
            PlateResult("ABC1D23", "ABC1D23", True, 0, 7),
            PlateResult("XYZ9A45", "XYZ9A46", False, 1, 7),
        ]
        result = BenchmarkResult.from_metrics(
            character_accuracy=13 / 14,
            plate_accuracy=0.5,
            n_plates=2,
            seed=42,
            command="alpr-mercosul benchmark --n-plates 2",
            output_path=Path("benchmarks/results/test.json"),
            plates=plates,
            ocr_backend="template-matching-v1",
        )
        assert result.project == "5-alpr-mercosul"
        assert result.metrics["correct_plates"] == 1
        assert result.failures == 1
        assert result.environment["ocr_backend"] == "template-matching-v1"
        assert result.proof["prediction_input"] == "image_pixels_only"

    def test_to_json_roundtrip(self, tmp_path: Path):
        path = tmp_path / "result.json"
        result = BenchmarkResult.from_metrics(
            character_accuracy=1.0,
            plate_accuracy=1.0,
            n_plates=1,
            seed=7,
            command="test",
            output_path=path,
            plates=[PlateResult("ABC1D23", "ABC1D23", True, 0, 7)],
            ocr_backend="template-matching-v1",
        )
        result.to_json(path)
        data = json.loads(path.read_text())
        assert data["project"] == "5-alpr-mercosul"
        assert data["metrics"]["plate_accuracy"] == 1.0
        assert data["plates"][0]["predicted"] == "ABC1D23"
