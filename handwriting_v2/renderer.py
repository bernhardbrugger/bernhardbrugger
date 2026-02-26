from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .models import PaperPreset, RenderRequest, StylePreset


class Renderer:
    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def render(self, req: RenderRequest, style: StylePreset, paper: PaperPreset) -> Image.Image:
        canvas = Image.new("RGB", (req.width, req.height), paper.base)
        draw = ImageDraw.Draw(canvas)
        self._paper_texture(draw, req, paper)
        self._paper_rules(draw, req, paper)
        self._write_text(canvas, req, style)
        return self._camera_finish(canvas)

    def _paper_texture(self, draw: ImageDraw.ImageDraw, req: RenderRequest, paper: PaperPreset) -> None:
        amount = (req.width * req.height) // 130
        for _ in range(amount):
            x = self.rng.randrange(0, req.width)
            y = self.rng.randrange(0, req.height)
            delta = self.rng.randint(-paper.texture_strength, paper.texture_strength)
            px = tuple(max(0, min(255, c + delta)) for c in paper.base)
            draw.point((x, y), fill=px)

    def _paper_rules(self, draw: ImageDraw.ImageDraw, req: RenderRequest, paper: PaperPreset) -> None:
        if not paper.rule or paper.line_mode == "none":
            return
        rule = paper.rule
        if paper.line_mode == "lined":
            for y in range(req.margin, req.height - req.margin, req.line_height):
                draw.line([(req.margin, y), (req.width - req.margin, y)], fill=rule, width=1)
        elif paper.line_mode == "grid":
            for y in range(req.margin, req.height - req.margin, req.line_height):
                draw.line([(req.margin, y), (req.width - req.margin, y)], fill=rule, width=1)
            for x in range(req.margin, req.width - req.margin, req.line_height):
                draw.line([(x, req.margin), (x, req.height - req.margin)], fill=rule, width=1)
        elif paper.line_mode == "dots":
            for y in range(req.margin, req.height - req.margin, req.line_height):
                for x in range(req.margin, req.width - req.margin, req.line_height):
                    draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=rule)

    def _write_text(self, canvas: Image.Image, req: RenderRequest, style: StylePreset) -> None:
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()
        max_w = req.width - (2 * req.margin)

        words = req.text.split()
        lines: list[str] = []
        line: list[str] = []
        for w in words:
            candidate = " ".join(line + [w])
            if line and draw.textlength(candidate, font=font) > max_w:
                lines.append(" ".join(line))
                line = [w]
            else:
                line.append(w)
        if line:
            lines.append(" ".join(line))

        y = req.margin
        for full_line in lines:
            x = req.margin + int(self.rng.uniform(-3, 3))
            baseline_shift = int(math.sin(y / 85) * style.baseline_wobble)

            for ch in full_line:
                jitter_x = self.rng.uniform(-style.jitter, style.jitter)
                jitter_y = self.rng.uniform(-style.jitter, style.jitter)
                alpha = int(170 + style.pressure * 85 + self.rng.uniform(-20, 20))

                glyph = Image.new("RGBA", (60, 80), (0, 0, 0, 0))
                gdraw = ImageDraw.Draw(glyph)
                gdraw.text((12, 20), ch, font=font, fill=(*style.ink, alpha))

                slant = style.slant + self.rng.uniform(-0.03, 0.03)
                transformed = glyph.transform(
                    glyph.size,
                    Image.Transform.AFFINE,
                    (1, slant, 0, 0, 1, 0),
                    resample=Image.Resampling.BICUBIC,
                )

                stroke = transformed.filter(ImageFilter.GaussianBlur(radius=max(0.2, style.stroke_blur)))
                canvas.paste(stroke, (int(x + jitter_x), int(y - 45 + baseline_shift + jitter_y)), stroke)
                x += int(draw.textlength(ch, font=font)) + style.spacing

            y += req.line_height + int(self.rng.uniform(-2, 2))
            if y > req.height - req.margin:
                break

    def _camera_finish(self, image: Image.Image) -> Image.Image:
        width, height = image.size
        mask = Image.new("L", image.size, 255)
        d = ImageDraw.Draw(mask)
        for r in range(0, max(width, height), 20):
            shade = max(175, 255 - int(r / 3.2))
            d.ellipse((r - width // 2, r - height // 2, width - r + width // 2, height - r + height // 2), outline=shade)
        mask = mask.filter(ImageFilter.GaussianBlur(90))
        image.putalpha(mask)
        return image.convert("RGB")
