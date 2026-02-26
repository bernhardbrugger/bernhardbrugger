"""Prompt-driven handwriting synthesis toolkit with realistic sheet rendering."""

__all__ = ["HandwritingOptimizer", "SynthesisRequest"]


def __getattr__(name: str):
    if name in {"HandwritingOptimizer", "SynthesisRequest"}:
        from .optimizer import HandwritingOptimizer, SynthesisRequest

        return {"HandwritingOptimizer": HandwritingOptimizer, "SynthesisRequest": SynthesisRequest}[name]
    raise AttributeError(name)
