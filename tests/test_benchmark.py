from __future__ import annotations

import pytest

from alpr_mercosul.benchmark import run_benchmark


def test_benchmark_reads_pixels_and_counts_workload():
    result = run_benchmark(n_plates=25, seed=42)
    assert result.environment["ocr_backend"] == "template-matching-v1"
    assert result.proof["prediction_input"] == "image_pixels_only"
    assert result.metrics["total_plates"] == 25
    assert result.metrics["total_characters"] == 175
    assert result.failures == 0


def test_benchmark_rejects_zero_workload():
    with pytest.raises(ValueError, match="n_plates must be at least 1"):
        run_benchmark(n_plates=0)
