from __future__ import annotations

from functools import cache

import numpy as np
from PIL import Image

from alpr_mercosul.domain import PlateResult
from alpr_mercosul.rendering import (
    CELL_HEIGHT,
    CELL_WIDTH,
    MERCOSUL_PATTERN,
    PLATE_HEIGHT,
    PLATE_WIDTH,
    TEXT_X,
    TEXT_Y,
    render_glyph,
    validate_plate,
)


@cache
def _template_mask(character: str) -> np.ndarray:
    return np.asarray(render_glyph(character), dtype=np.uint8) < 128


def read_plate(image: Image.Image) -> str:
    """Read a fixed-layout synthetic Mercosul plate from image pixels only."""
    if image.size != (PLATE_WIDTH, PLATE_HEIGHT):
        raise ValueError(f"plate image must be {PLATE_WIDTH}x{PLATE_HEIGHT}")

    grayscale = np.asarray(image.convert("L"), dtype=np.uint8)
    predicted: list[str] = []
    for index, allowed_characters in enumerate(MERCOSUL_PATTERN):
        left = TEXT_X + index * CELL_WIDTH
        observed = (
            grayscale[
                TEXT_Y : TEXT_Y + CELL_HEIGHT,
                left : left + CELL_WIDTH,
            ]
            < 128
        )
        best = min(
            allowed_characters,
            key=lambda character: (
                int(np.count_nonzero(observed != _template_mask(character))),
                character,
            ),
        )
        predicted.append(best)
    return "".join(predicted)


def evaluate_plate(image: Image.Image, ground_truth: str) -> PlateResult:
    validate_plate(ground_truth)
    predicted = read_plate(image)
    errors = sum(expected != actual for expected, actual in zip(ground_truth, predicted))
    return PlateResult(
        plate=ground_truth,
        predicted=predicted,
        correct=errors == 0,
        character_errors=errors,
        total_characters=len(ground_truth),
    )
