from pathlib import Path

import pytest

from handwriting_lab.prompts import parse_prompt


@pytest.mark.parametrize(
    "prompt,expected",
    [
        ("style: vintage-ink; sheet: parchment; seed: 7", {"style": "vintage-ink", "sheet": "parchment", "seed": "7"}),
        ("style: exam-neat;sheet: lined", {"style": "exam-neat", "sheet": "lined"}),
    ],
)
def test_parse_prompt_extracts_keys(prompt: str, expected: dict[str, str]):
    parsed = parse_prompt(prompt)
    for key, value in expected.items():
        assert parsed[key] == value


def test_optimizer_generates_output(tmp_path: Path):
    pytest.importorskip("PIL")
    from handwriting_lab.optimizer import HandwritingOptimizer, SynthesisRequest

    out = tmp_path / "sample.png"
    req = SynthesisRequest(
        text="Hello optimized handwriting",
        prompt="style: exam-neat; sheet: lined; seed: 5",
        output_path=str(out),
    )
    result = HandwritingOptimizer().run(req)
    assert result.exists()
    assert result.stat().st_size > 0
