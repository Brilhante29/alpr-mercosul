from __future__ import annotations

import random
import string

from PIL import Image, ImageDraw

from alpr_mercosul.rendering import (
    PLATE_HEIGHT,
    PLATE_WIDTH,
    TEXT_X,
    TEXT_Y,
    render_plate_strip,
)


def random_plate(rng: random.Random) -> str:
    letters = "".join(rng.choices(string.ascii_uppercase, k=3))
    digit1 = rng.choice(string.digits)
    letter = rng.choice(string.ascii_uppercase)
    digit2 = rng.choice(string.digits)
    digit3 = rng.choice(string.digits)
    return f"{letters}{digit1}{letter}{digit2}{digit3}"


def generate_plate_image(
    plate: str,
    width: int = PLATE_WIDTH,
    height: int = PLATE_HEIGHT,
    add_noise: bool = True,
    noise_rng: random.Random | None = None,
) -> Image.Image:
    if (width, height) != (PLATE_WIDTH, PLATE_HEIGHT):
        raise ValueError(f"synthetic fixture size must be {PLATE_WIDTH}x{PLATE_HEIGHT}")

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, width - 1, height - 1], outline="blue", width=3)
    draw.rectangle([2, 2, width - 3, 14], fill="blue")
    image.paste(render_plate_strip(plate), (TEXT_X, TEXT_Y))

    if add_noise:
        rng = noise_rng or random.Random()
        for _ in range(width * height // 20):
            x = rng.randint(0, width - 1)
            y = rng.randint(0, height - 1)
            value = rng.randint(0, 30)
            image.putpixel((x, y), (value, value, value))

    ImageDraw.Draw(image).rectangle(
        [0, 0, width - 1, height - 1], outline="blue", width=3
    )
    return image


def generate_plate(
    seed: int | None = None,
    rng: random.Random | None = None,
) -> tuple[Image.Image, str]:
    selected_rng = rng or random.Random(seed)
    plate = random_plate(selected_rng)
    image = generate_plate_image(plate, noise_rng=selected_rng)
    return image, plate


def generate_dataset(
    n_plates: int = 100,
    seed: int = 42,
) -> list[tuple[Image.Image, str]]:
    if n_plates < 1:
        raise ValueError("n_plates must be at least 1")
    rng = random.Random(seed)
    return [generate_plate(rng=rng) for _ in range(n_plates)]
