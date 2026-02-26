## Handwriting Studio V2

A modern, creative handwriting synthesis playground focused on **realistic handwritten output**, many writing styles, and many paper formats.

### What is new in V2

- 8 writing styles (cursive, neat, fountain pen, pencil, marker, etc.)
- 8 paper formats (college-lined, wide-lined, legal pad, dot grid, math grid, parchment, recycled, plain)
- deterministic seed-based generation
- realistic paper textures + ruling + ink rendering effects
- CLI workflow and a minimal browser web app for quick testing

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m handwriting_v2.cli "This is V2 handwriting" --style fountain-pen --paper legal-pad --seed 12
```

Generated image:

- `outputs/handwriting_v2.png`

## Basic web app

```bash
python webapp.py
# open http://localhost:8000
```

Use the form to pick text, style, paper format, and seed, then generate instantly.

## Prompt-based controls

You can also parse controls from prompt-like directives:

- `style: gel-pen; paper: dot-grid; seed: 7; width: 1400; height: 2000`

(see `handwriting_v2/prompting.py`)

## Project structure

- `handwriting_v2/presets.py` → style + paper preset catalogs
- `handwriting_v2/renderer.py` → sheet + handwriting rendering engine
- `handwriting_v2/pipeline.py` → generation pipeline
- `handwriting_v2/cli.py` → command-line generation
- `webapp.py` → minimal UI for interactive testing
- `tests/test_v2.py` → core tests
