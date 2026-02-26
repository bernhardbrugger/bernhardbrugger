from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .optimizer import HandwritingOptimizer, SynthesisRequest

app = FastAPI(title="Handwriting Studio API", version="0.1.0")
optimizer = HandwritingOptimizer()


class GenerateBody(BaseModel):
    text: str
    prompt: str = "style: casual-note; sheet: lined; seed: 42"
    output_path: str = "outputs/handwriting.png"


@app.post("/generate")
def generate(body: GenerateBody) -> dict[str, str]:
    output = optimizer.run(
        SynthesisRequest(text=body.text, prompt=body.prompt, output_path=body.output_path)
    )
    return {"image": str(output)}
