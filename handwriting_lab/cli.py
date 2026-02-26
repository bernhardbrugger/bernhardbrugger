from __future__ import annotations

import argparse

from .optimizer import HandwritingOptimizer, SynthesisRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate realistic prompt-driven handwriting on different sheets.")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--prompt", default="style: casual-note; sheet: lined; seed: 42")
    parser.add_argument("--output", default="outputs/handwriting.png")
    args = parser.parse_args()

    req = SynthesisRequest(text=args.text, prompt=args.prompt, output_path=args.output)
    out = HandwritingOptimizer().run(req)
    print(f"Saved output to {out}")


if __name__ == "__main__":
    main()
