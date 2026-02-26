from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class StyleProfile:
    slant: float
    pressure: float
    spacing: int
    jitter: float
    ink_color: tuple[int, int, int]


STYLE_PRESETS: Dict[str, StyleProfile] = {
    "exam-neat": StyleProfile(slant=0.05, pressure=0.7, spacing=4, jitter=0.6, ink_color=(20, 25, 50)),
    "casual-note": StyleProfile(slant=0.12, pressure=0.8, spacing=2, jitter=1.1, ink_color=(18, 18, 40)),
    "architect": StyleProfile(slant=0.0, pressure=0.65, spacing=5, jitter=0.3, ink_color=(25, 35, 65)),
    "vintage-ink": StyleProfile(slant=0.08, pressure=0.9, spacing=3, jitter=1.4, ink_color=(55, 35, 20)),
}

SHEET_PRESETS = {
    "plain": {"base": (246, 244, 236), "rule": None},
    "lined": {"base": (244, 243, 235), "rule": (150, 175, 210)},
    "grid": {"base": (242, 241, 233), "rule": (170, 185, 205)},
    "parchment": {"base": (235, 223, 196), "rule": None},
    "notepad-yellow": {"base": (250, 244, 186), "rule": (214, 205, 152)},
}


def parse_prompt(prompt: str) -> dict[str, str]:
    """Extract basic controls from natural language prompt.

    Supports tags in natural language like:
    - "style: vintage-ink"
    - "sheet: lined"
    - "seed: 7"
    """
    parsed: dict[str, str] = {}
    for chunk in prompt.split(";"):
        if ":" not in chunk:
            continue
        key, value = chunk.split(":", 1)
        parsed[key.strip().lower()] = value.strip().lower()
    return parsed
