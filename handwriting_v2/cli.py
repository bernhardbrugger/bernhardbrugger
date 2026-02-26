from __future__ import annotations

import argparse

from .models import RenderRequest
from .pipeline import HandwritingStudio
from .presets import PAPER_PRESETS, STYLE_PRESETS


def main() -> None:
    p = argparse.ArgumentParser(description="Handwriting Studio V2")
    p.add_argument("text")
    p.add_argument("--style", default="balanced-cursive", choices=sorted(STYLE_PRESETS))
    p.add_argument("--paper", default="college-lined", choices=sorted(PAPER_PRESETS))
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output", default="outputs/handwriting_v2.png")
    args = p.parse_args()

    req = RenderRequest(text=args.text, style=args.style, paper=args.paper, seed=args.seed, output_path=args.output)
    path = HandwritingStudio().generate(req)
    print(path)


if __name__ == "__main__":
    main()
