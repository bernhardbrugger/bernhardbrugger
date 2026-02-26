from __future__ import annotations

import math
import random
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .prompts import SHEET_PRESETS, StyleProfile


@dataclass
class SheetConfig:
    width: int = 1400
    height: int = 1900
    margin: int = 120
    line_height: int = 70


class HandwritingRenderer:
    """Renderer that simulates ink flow over procedurally generated paper textures."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def render(self, text: str, style: StyleProfile, sheet: str, config: SheetConfig | None = None) -> Image.Image:
        config = config or SheetConfig()
        img = self._build_sheet(sheet, config)
        self._draw_handwriting(img, text, style, config)
        return self._post_process(img)

    def _build_sheet(self, sheet: str, config: SheetConfig) -> Image.Image:
        preset = SHEET_PRESETS.get(sheet, SHEET_PRESETS["plain"])
        img = Image.new("RGB", (config.width, config.height), preset["base"])
        draw = ImageDraw.Draw(img)

        # Fiber/noise texture
        for _ in range((config.width * config.height) // 180):
            x = self.rng.randrange(0, config.width)
            y = self.rng.randrange(0, config.height)
            delta = self.rng.randint(-7, 7)
            px = tuple(max(0, min(255, c + delta)) for c in preset["base"])
            draw.point((x, y), fill=px)

        if preset["rule"]:
            rule = preset["rule"]
            if sheet == "grid":
                for y in range(config.margin, config.height - config.margin, config.line_height):
                    draw.line([(config.margin, y), (config.width - config.margin, y)], fill=rule, width=1)
                for x in range(config.margin, config.width - config.margin, config.line_height):
                    draw.line([(x, config.margin), (x, config.height - config.margin)], fill=rule, width=1)
            else:
                for y in range(config.margin, config.height - config.margin, config.line_height):
                    draw.line([(config.margin, y), (config.width - config.margin, y)], fill=rule, width=1)

        return img

    def _draw_handwriting(self, image: Image.Image, text: str, style: StyleProfile, config: SheetConfig) -> None:
        draw = ImageDraw.Draw(image)
        base_font = ImageFont.load_default()

        max_width = image.width - config.margin * 2
        words = text.split()
        lines, current = [], []
        for word in words:
            trial = " ".join(current + [word])
            if draw.textlength(trial, font=base_font) > max_width and current:
                lines.append(" ".join(current))
                current = [word]
            else:
                current.append(word)
        if current:
            lines.append(" ".join(current))

        y = config.margin
        for line in lines:
            x = config.margin + int(self.rng.uniform(-2, 2))
            for char in line:
                jitter_x = self.rng.uniform(-style.jitter, style.jitter)
                jitter_y = self.rng.uniform(-style.jitter, style.jitter)
                pressure = max(1, int(1 + style.pressure * 2 + self.rng.uniform(-0.4, 0.4)))
                char_img = Image.new("RGBA", (40, 60), (0, 0, 0, 0))
                cdraw = ImageDraw.Draw(char_img)
                alpha = int(180 + style.pressure * 65 + self.rng.uniform(-20, 20))
                cdraw.text((8, 10), char, font=base_font, fill=(*style.ink_color, alpha))

                shear = style.slant + self.rng.uniform(-0.02, 0.02)
                sheared = char_img.transform(
                    char_img.size,
                    Image.Transform.AFFINE,
                    (1, shear, 0, 0, 1, 0),
                    resample=Image.Resampling.BICUBIC,
                )
                blurred = sheared.filter(ImageFilter.GaussianBlur(radius=max(0.3, pressure / 5)))
                image.paste(blurred, (int(x + jitter_x), int(y + jitter_y - 35)), blurred)
                x += int(draw.textlength(char, font=base_font)) + style.spacing

            y += config.line_height + int(math.sin(y / 90) * 2)
            if y > image.height - config.margin:
                break

    def _post_process(self, image: Image.Image) -> Image.Image:
        v = Image.new("L", image.size, 255)
        vd = ImageDraw.Draw(v)
        width, height = image.size
        for r in range(0, max(width, height), 25):
            shade = max(180, 255 - r // 4)
            vd.ellipse([r - width // 2, r - height // 2, width - r + width // 2, height - r + height // 2], outline=shade)
        vignette = v.filter(ImageFilter.GaussianBlur(radius=80))
        image.putalpha(vignette)
        return image.convert("RGB")
