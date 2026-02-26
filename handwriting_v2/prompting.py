from __future__ import annotations

from .models import RenderRequest


def parse_prompt(text: str, *, default_text: str) -> RenderRequest:
    """Parse directives like: style: gel-pen; paper: legal-pad; seed: 7."""
    data: dict[str, str] = {}
    for chunk in text.split(";"):
        if ":" not in chunk:
            continue
        key, value = chunk.split(":", 1)
        data[key.strip().lower()] = value.strip().lower()

    return RenderRequest(
        text=default_text,
        style=data.get("style", "balanced-cursive"),
        paper=data.get("paper", "college-lined"),
        seed=int(data.get("seed", "42")),
        width=int(data.get("width", "1600")),
        height=int(data.get("height", "2100")),
    )
