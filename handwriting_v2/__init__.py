"""Handwriting Studio V2."""

__all__ = ["HandwritingStudio", "RenderRequest"]


def __getattr__(name: str):
    if name == "RenderRequest":
        from .models import RenderRequest

        return RenderRequest
    if name == "HandwritingStudio":
        from .pipeline import HandwritingStudio

        return HandwritingStudio
    raise AttributeError(name)
