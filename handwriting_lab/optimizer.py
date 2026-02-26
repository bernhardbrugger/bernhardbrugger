from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .prompts import STYLE_PRESETS, parse_prompt
from .renderer import HandwritingRenderer


@dataclass
class SynthesisRequest:
    text: str
    prompt: str
    output_path: str = "outputs/handwriting.png"


class HandwritingOptimizer:
    """Optimization layer over prompt-driven handwriting synthesis.

    Core idea:
    1) Parse prompt into sheet/style/seed controls.
    2) Select and tune render profile.
    3) Render with realistic paper + ink simulation.
    """

    def run(self, request: SynthesisRequest) -> Path:
        parsed = parse_prompt(request.prompt)
        style_name = parsed.get("style", "casual-note")
        sheet_name = parsed.get("sheet", "lined")
        seed = int(parsed.get("seed", "42"))

        style = STYLE_PRESETS.get(style_name, STYLE_PRESETS["casual-note"])
        renderer = HandwritingRenderer(seed=seed)
        img = renderer.render(request.text, style=style, sheet=sheet_name)

        out = Path(request.output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out)
        return out
