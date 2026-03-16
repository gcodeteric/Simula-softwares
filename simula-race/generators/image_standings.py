from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

from utils.strings import S


def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_path = Path(path)
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def generate_standings_image(
    output_path: str | Path,
    rows: Iterable[dict[str, str | int]],
    season_name: str,
    subtitle: str,
    primary_color: str,
    secondary_color: str,
    font_path: str,
    font_bold_path: str,
) -> Path:
    rows_list = list(rows)
    width = 1200
    height = 140 + max(1, len(rows_list)) * 40
    image = Image.new("RGB", (width, height), secondary_color)
    draw = ImageDraw.Draw(image)
    title_font = _load_font(font_bold_path, 28)
    text_font = _load_font(font_path, 18)
    draw.text((32, 24), S.STANDINGS_IMAGE_TITLE.format(season_name=season_name), fill="white", font=title_font)
    draw.text((32, 64), subtitle, fill="#CCCCCC", font=text_font)
    y = 110
    for index, row in enumerate(rows_list):
        band = secondary_color if index % 2 == 0 else "#223047"
        draw.rectangle((24, y - 6, width - 24, y + 28), fill=band)
        if index < 3:
            draw.rectangle((24, y - 6, 34, y + 28), fill=primary_color)
        line = S.STANDINGS_IMAGE_ROW.format(
            position=row["position"],
            name=row["name"],
            points=row["points"],
            wins=row["wins"],
            podiums=row["podiums"],
        )
        draw.text((42, y), line, fill="white", font=text_font)
        y += 40
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG")
    return output
