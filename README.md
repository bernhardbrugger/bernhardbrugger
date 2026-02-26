## Hey, I'm Bernhard 👋

**AI/ML Engineer & Quantitative Developer** from Salzburg, Austria 🏔️

I build things at the intersection of **deep learning**, **statistics**, and **finance** — from neural networks that generate handwriting to algorithms that scan markets for alpha.

### 🔬 What I work on

- **Deep Learning** — generative models, sequence modeling, neural synthesis
- **Quantitative Finance** — algorithmic trading, market microstructure, arbitrage detection
- **Applied Statistics** — Bayesian inference, time series analysis, anomaly detection
- **AI Infrastructure** — building tools that make ML workflows faster and more reproducible

### 🛠️ Tech Stack

`Python` `PyTorch` `TensorFlow` `scikit-learn` `TypeScript` `React` `Node.js` `PostgreSQL`

### 📊 Currently exploring

- AI agents for autonomous financial analysis
- Real-world asset tokenization & DeFi analytics
- Intersection of LLMs and structured data

### 📫 Get in touch

- 🌐 [produktfinder.at](https://produktfinder.at)

## ✍️ Handwriting Studio (new optimization concept)

I added a prompt-driven prototype inspired by modern handwriting synthesis projects, with a focus on **realistic sheet simulation** and **creative controllability**:

- Prompt parsing (`style`, `sheet`, `seed`) from natural language-like directives.
- Procedural paper generation with grain/noise and optional ruled/grid sheets.
- Ink rendering with jitter, slant, pressure, and blur to emulate pen dynamics.
- FastAPI endpoint + CLI for generation workflows.

### Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m handwriting_lab.cli "This is a realistic generated note" --prompt "style: vintage-ink; sheet: parchment; seed: 8"
```

### API

```bash
uvicorn handwriting_lab.api:app --reload
# POST /generate {"text":"...","prompt":"style: casual-note; sheet: lined; seed: 42"}
```
