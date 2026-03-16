from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_path = Path(path)
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def generate_calendar_image(
    output_path: str | Path,
    rounds: Iterable[dict[str, str | int]],
    title: str,
    primary_color: str,
    secondary_color: str,
    font_path: str,
    font_bold_path: str,
) -> Path:
    rounds_list = list(rounds)
    width = 1200
    height = 220 + ((len(rounds_list) + 1) // 2) * 110
    image = Image.new("RGB", (width, height), secondary_color)
    draw = ImageDraw.Draw(image)
    title_font = _load_font(font_bold_path, 28)
    text_font = _load_font(font_path, 18)
    draw.text((32, 24), title, fill="white", font=title_font)
    x_positions = [32, 616]
    y = 96
    for index, round_info in enumerate(rounds_list):
        column = index % 2
        if index and column == 0:
            y += 110
        x = x_positions[column]
        draw.rounded_rectangle((x, y, x + 520, y + 80), radius=16, fill="#223047", outline=primary_color, width=2)
        line_1 = f"{round_info['status']} R{round_info['round_number']} — {round_info['track']} {round_info['flag']}"
        line_2 = f"{round_info['date']} às {round_info['time']}"
        draw.text((x + 20, y + 16), line_1, fill="white", font=text_font)
        draw.text((x + 20, y + 46), line_2, fill="#CCCCCC", font=text_font)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG")
    return output
