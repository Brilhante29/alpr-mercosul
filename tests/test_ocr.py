from __future__ import annotations

from PIL import Image

from alpr_mercosul.fixture import generate_dataset, generate_plate, generate_plate_image
from alpr_mercosul.ocr import evaluate_plate, read_plate
from alpr_mercosul.rendering import CELL_WIDTH, TEXT_X, TEXT_Y, render_glyph


class TestTemplateOCR:
    def test_reads_pixels_without_ground_truth_argument(self):
        image, ground_truth = generate_plate(seed=42)
        assert read_plate(image) == ground_truth

    def test_reads_full_publication_workload(self):
        dataset = generate_dataset(n_plates=100, seed=42)
        assert all(read_plate(image) == ground_truth for image, ground_truth in dataset)

    def test_prediction_changes_when_pixels_change_but_label_does_not(self):
        ground_truth = "QAH3E18"
        image = generate_plate_image(ground_truth, add_noise=False)
        replacement = render_glyph("B")
        image.paste(
            Image.merge("RGB", (replacement, replacement, replacement)), (TEXT_X, TEXT_Y)
        )

        result = evaluate_plate(image, ground_truth)

        assert result.predicted == "BAH3E18"
        assert not result.correct
        assert result.character_errors == 1

    def test_rejects_unknown_image_geometry(self):
        image = Image.new("RGB", (CELL_WIDTH, CELL_WIDTH), "white")
        try:
            read_plate(image)
        except ValueError as error:
            assert "200x80" in str(error)
        else:
            raise AssertionError("invalid image geometry was accepted")

    def test_plate_format(self):
        _, ground_truth = generate_plate(seed=42)
        assert len(ground_truth) == 7
        assert ground_truth[0:3].isalpha()
        assert ground_truth[3].isdigit()
        assert ground_truth[4].isalpha()
        assert ground_truth[5:7].isdigit()
