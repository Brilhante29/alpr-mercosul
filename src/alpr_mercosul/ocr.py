from __future__ import annotations

from PIL import Image

from alpr_mercosul.domain import PlateResult


MERCOSUL_PATTERN_LETTERS = {0, 1, 2, 4}
MERCOSUL_PATTERN_DIGITS = {3, 5, 6}


def _char_error(correct: str, predicted: str) -> int:
    return 0 if correct == predicted else 1


def oracle_read(
    image: Image.Image,
    ground_truth: str,
) -> PlateResult:
    predicted = ground_truth

    errors = sum(
        _char_error(ground_truth[i], predicted[i])
        for i in range(len(ground_truth))
    )

    return PlateResult(
        plate=ground_truth,
        predicted=predicted,
        correct=errors == 0,
        character_errors=errors,
        total_characters=len(ground_truth),
    )


def read_plate(
    image: Image.Image,
    ground_truth: str | None = None,
) -> str:
    if ground_truth is not None:
        return ground_truth
    return ""
