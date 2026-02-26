from pathlib import Path

import pytest

from handwriting_v2.models import RenderRequest
from handwriting_v2.prompting import parse_prompt
from handwriting_v2.presets import PAPER_PRESETS, STYLE_PRESETS


def test_presets_are_rich():
    assert len(STYLE_PRESETS) >= 8
    assert len(PAPER_PRESETS) >= 8


def test_parse_prompt_maps_controls():
    req = parse_prompt("style: gel-pen; paper: legal-pad; seed: 5; width: 1200; height: 1500", default_text="hello")
    assert req.style == "gel-pen"
    assert req.paper == "legal-pad"
    assert req.seed == 5
    assert req.width == 1200
    assert req.height == 1500


def test_generate_png(tmp_path: Path):
    pytest.importorskip("PIL")
    from handwriting_v2.pipeline import HandwritingStudio

    out = tmp_path / "v2.png"
    req = RenderRequest(
        text="V2 generation test sample",
        style="fountain-pen",
        paper="dot-grid",
        seed=9,
        output_path=str(out),
    )
    result = HandwritingStudio().generate(req)
    assert result.exists()
    assert result.stat().st_size > 1000
