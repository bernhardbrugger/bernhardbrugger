from __future__ import annotations

from pathlib import Path

from .models import RenderRequest
from .presets import PAPER_PRESETS, STYLE_PRESETS
from .renderer import Renderer


class HandwritingStudio:
    def generate(self, req: RenderRequest) -> Path:
        style = STYLE_PRESETS.get(req.style, STYLE_PRESETS["balanced-cursive"])
        paper = PAPER_PRESETS.get(req.paper, PAPER_PRESETS["college-lined"])

        image = Renderer(seed=req.seed).render(req, style, paper)
        out = Path(req.output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        image.save(out)
        return out
