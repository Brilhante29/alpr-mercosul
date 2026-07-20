from __future__ import annotations

import random
import string
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


MERCOSUL_CHARS = string.ascii_uppercase + string.digits

FONT_PATH = Path(__file__).parent / "assets" / "DejaVuSansMono-Bold.ttf"


def _load_font(size: int = 36) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if FONT_PATH.exists():
        return ImageFont.truetype(str(FONT_PATH), size)
    return ImageFont.load_default()


def random_plate(rng: random.Random) -> str:
    letters = "".join(rng.choices(string.ascii_uppercase, k=3))
    digit1 = rng.choice(string.digits)
    letter = rng.choice(string.ascii_uppercase)
    digit2 = rng.choice(string.digits)
    digit3 = rng.choice(string.digits)
    return f"{letters}{digit1}{letter}{digit2}{digit3}"


def generate_plate_image(
    plate: str,
    width: int = 200,
    height: int = 80,
    add_noise: bool = True,
    noise_rng: random.Random | None = None,
) -> Image.Image:
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width - 1, height - 1], outline="blue", width=3)
    draw.rectangle([2, 2, width - 3, 14], fill="blue")

    font = _load_font(32)

    bbox = draw.textbbox((0, 0), plate, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (width - tw) // 2
    y = (height - th) // 2 + 5

    draw.text((x, y), plate, fill="black", font=font)

    if add_noise:
        nrng = noise_rng or random.Random()
        for _ in range(width * height // 20):
            px = nrng.randint(0, width - 1)
            py = nrng.randint(0, height - 1)
            v = nrng.randint(0, 30)
            img.putpixel((px, py), (v, v, v))

    draw.rectangle([0, 0, width - 1, height - 1], outline="blue", width=3)

    return img


_rng_instance: random.Random | None = None


def _get_rng(seed: int | None) -> random.Random:
    global _rng_instance
    if seed is not None:
        return random.Random(seed)
    if _rng_instance is None:
        _rng_instance = random.Random()
    return _rng_instance


def generate_plate(
    seed: int | None = None,
    rng: random.Random | None = None,
) -> tuple[Image.Image, str]:
    global _rng_instance
    if rng is None:
        if seed is not None:
            rng = random.Random(seed)
        else:
            if _rng_instance is None:
                _rng_instance = random.Random()
            rng = _rng_instance
    plate = random_plate(rng)
    img = generate_plate_image(plate, noise_rng=rng)
    return img, plate


def generate_dataset(
    n_plates: int = 100,
    seed: int = 42,
) -> list[tuple[Image.Image, str]]:
    rng = random.Random(seed)
    return [generate_plate(rng=rng) for _ in range(n_plates)]
