from __future__ import annotations

import json
from pathlib import Path

from alpr_mercosul.domain import BenchmarkResult, PlateResult


class TestPlateResult:
    def test_correct_plate(self):
        r = PlateResult(
            plate="ABC1D23",
            predicted="ABC1D23",
            correct=True,
            character_errors=0,
            total_characters=7,
        )
        assert r.correct
        assert r.character_errors == 0
        assert r.plate == "ABC1D23"

    def test_wrong_plate(self):
        r = PlateResult(
            plate="ABC1D23",
            predicted="ABC1E23",
            correct=False,
            character_errors=1,
            total_characters=7,
        )
        assert not r.correct
        assert r.character_errors == 1


class TestBenchmarkResult:
    def test_from_metrics_builds_valid_result(self):
        plates = [
            PlateResult("ABC1D23", "ABC1D23", True, 0, 7),
            PlateResult("XYZ9A45", "XYZ9A45", True, 0, 7),
        ]
        result = BenchmarkResult.from_metrics(
            character_accuracy=1.0,
            plate_accuracy=1.0,
            n_plates=2,
            seed=42,
            command="alpr-mercosul benchmark --n-plates 2",
            output_path=Path("benchmarks/results/test.json"),
            plates=plates,
        )
        assert result.project == "5-alpr-mercosul"
        assert result.metric == "character_accuracy"
        assert result.value == 1.0
        assert result.metrics["plate_accuracy"] == 1.0
        assert result.metrics["total_plates"] == 2
        assert result.metrics["correct_plates"] == 2
        assert result.failures == 0
        assert len(result.plates) == 2

    def test_to_json_roundtrip(self, tmp_path: Path):
        plates = [
            PlateResult("ABC1D23", "ABC1D23", True, 0, 7),
        ]
        path = tmp_path / "result.json"
        result = BenchmarkResult.from_metrics(
            character_accuracy=1.0,
            plate_accuracy=1.0,
            n_plates=1,
            seed=7,
            command="test",
            output_path=path,
            plates=plates,
        )
        result.to_json(path)
        assert path.exists()
        data = json.loads(path.read_text())
        assert data["project"] == "5-alpr-mercosul"
        assert data["value"] == 1.0
        assert data["metrics"]["plate_accuracy"] == 1.0
        assert len(data["plates"]) == 1
        assert data["plates"][0]["plate"] == "ABC1D23"
