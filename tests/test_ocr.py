from __future__ import annotations

from alpr_mercosul.fixture import generate_plate
from alpr_mercosul.ocr import oracle_read


class TestOracleOCR:
    def test_correct_read(self):
        image, ground_truth = generate_plate(seed=42)
        result = oracle_read(image, ground_truth)
        assert result.correct
        assert result.predicted == ground_truth
        assert result.character_errors == 0
        assert result.total_characters == 7

    def test_multiple_plates(self):
        for seed in range(10):
            image, ground_truth = generate_plate(seed=seed)
            result = oracle_read(image, ground_truth)
            assert result.correct
            assert result.predicted == ground_truth

    def test_plate_format(self):
        image, ground_truth = generate_plate(seed=42)
        assert len(ground_truth) == 7
        assert ground_truth[0:3].isalpha()
        assert ground_truth[3].isdigit()
        assert ground_truth[4].isalpha()
        assert ground_truth[5:7].isdigit()
