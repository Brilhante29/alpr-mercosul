from __future__ import annotations

import string
from functools import cache

from PIL import Image, ImageDraw, ImageFont

PLATE_WIDTH = 200
PLATE_HEIGHT = 80
PLATE_LENGTH = 7

BASE_CELL_WIDTH = 6
BASE_CELL_HEIGHT = 11
GLYPH_SCALE = 4
CELL_WIDTH = BASE_CELL_WIDTH * GLYPH_SCALE
CELL_HEIGHT = BASE_CELL_HEIGHT * GLYPH_SCALE
TEXT_WIDTH = PLATE_LENGTH * CELL_WIDTH
TEXT_X = (PLATE_WIDTH - TEXT_WIDTH) // 2
TEXT_Y = (PLATE_HEIGHT - CELL_HEIGHT) // 2 + 5

MERCOSUL_PATTERN = (
    string.ascii_uppercase,
    string.ascii_uppercase,
    string.ascii_uppercase,
    string.digits,
    string.ascii_uppercase,
    string.digits,
    string.digits,
)


def validate_plate(plate: str) -> None:
    if len(plate) != PLATE_LENGTH:
        raise ValueError(f"plate must contain {PLATE_LENGTH} characters")
    for index, (character, allowed) in enumerate(zip(plate, MERCOSUL_PATTERN)):
        if character not in allowed:
            raise ValueError(f"invalid character {character!r} at plate position {index}")


@cache
def render_glyph(character: str) -> Image.Image:
    if len(character) != 1 or character not in string.ascii_uppercase + string.digits:
        raise ValueError(f"unsupported glyph: {character!r}")

    canvas = Image.new("L", (BASE_CELL_WIDTH, BASE_CELL_HEIGHT), 255)
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), character, fill=0, font=ImageFont.load_default())
    return canvas.resize((CELL_WIDTH, CELL_HEIGHT), Image.Resampling.NEAREST)


def render_plate_strip(plate: str) -> Image.Image:
    validate_plate(plate)
    strip = Image.new("RGB", (TEXT_WIDTH, CELL_HEIGHT), "white")
    for index, character in enumerate(plate):
        glyph = render_glyph(character)
        rgb_glyph = Image.merge("RGB", (glyph, glyph, glyph))
        strip.paste(rgb_glyph, (index * CELL_WIDTH, 0))
    return strip
