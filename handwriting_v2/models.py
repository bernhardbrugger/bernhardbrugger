from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StylePreset:
    name: str
    slant: float
    pressure: float
    jitter: float
    baseline_wobble: float
    spacing: int
    stroke_blur: float
    ink: tuple[int, int, int]


@dataclass(frozen=True)
class PaperPreset:
    name: str
    base: tuple[int, int, int]
    rule: tuple[int, int, int] | None
    texture_strength: int
    line_mode: str  # none|lined|grid|dots


@dataclass
class RenderRequest:
    text: str
    style: str = "balanced-cursive"
    paper: str = "college-lined"
    seed: int = 42
    width: int = 1600
    height: int = 2100
    margin: int = 140
    line_height: int = 74
    output_path: str = "outputs/handwriting_v2.png"
