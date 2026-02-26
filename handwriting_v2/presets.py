from __future__ import annotations

from .models import PaperPreset, StylePreset

STYLE_PRESETS: dict[str, StylePreset] = {
    "balanced-cursive": StylePreset("balanced-cursive", 0.09, 0.82, 0.9, 1.4, 3, 0.8, (24, 26, 52)),
    "exam-neat": StylePreset("exam-neat", 0.03, 0.72, 0.5, 0.8, 4, 0.5, (16, 24, 44)),
    "fast-notes": StylePreset("fast-notes", 0.14, 0.85, 1.5, 2.0, 2, 1.0, (14, 16, 35)),
    "architect-print": StylePreset("architect-print", 0.0, 0.66, 0.3, 0.4, 5, 0.4, (25, 35, 64)),
    "fountain-pen": StylePreset("fountain-pen", 0.08, 0.95, 1.0, 1.2, 3, 1.2, (36, 24, 18)),
    "gel-pen": StylePreset("gel-pen", 0.06, 0.88, 0.7, 1.0, 3, 0.6, (22, 38, 89)),
    "soft-pencil": StylePreset("soft-pencil", 0.05, 0.58, 1.1, 1.7, 2, 1.6, (62, 62, 62)),
    "marker-bold": StylePreset("marker-bold", 0.02, 0.99, 0.4, 0.6, 3, 0.2, (30, 30, 30)),
}

PAPER_PRESETS: dict[str, PaperPreset] = {
    "plain-white": PaperPreset("plain-white", (248, 248, 245), None, 10, "none"),
    "college-lined": PaperPreset("college-lined", (245, 244, 238), (157, 180, 217), 14, "lined"),
    "wide-lined": PaperPreset("wide-lined", (244, 243, 236), (163, 182, 218), 12, "lined"),
    "math-grid": PaperPreset("math-grid", (243, 242, 235), (176, 192, 212), 12, "grid"),
    "dot-grid": PaperPreset("dot-grid", (246, 245, 238), (180, 190, 208), 11, "dots"),
    "legal-pad": PaperPreset("legal-pad", (248, 242, 181), (207, 200, 150), 14, "lined"),
    "parchment": PaperPreset("parchment", (235, 223, 195), None, 22, "none"),
    "recycled-gray": PaperPreset("recycled-gray", (225, 226, 220), (170, 176, 181), 24, "lined"),
}
