"""Gentle nutrition-themed "bubble whispers".

Each phrase is a short, poetic-but-factual sentence rooted in mainstream,
everyday nutrition knowledge (the kind found in general dietary guidelines).
They are written to feel like a soft, comforting note — not advice, and
certainly not a medical claim.

Safety guardrails for this list:
- No medical, disease, diagnosis, or treatment claims.
- No "detox", "cleanse", "cure", "heal", "boost immunity" promises.
- No weight-loss / dieting / calorie / fat-burning language.
- No "should" / prescriptive commands; these are gentle observations.

If you add phrases, keep them short (they float beside rising bubbles),
keep them kind, and run the smoke check that scans for banned terms.
"""

from __future__ import annotations

import random

# A small, hand-reviewed set. Short, warm, and grounded in mainstream
# nutrition basics (water, fiber, whole grains, protein, colorful plants,
# a balanced plate, healthy fats, etc.).
WHISPERS: tuple[str, ...] = (
    "A glass of water is a quiet kindness.",
    "Fiber feeds the garden within.",
    "Whole grains offer steady energy.",
    "Protein helps the body mend softly.",
    "Colorful plants bring gentle micronutrients.",
    "A balanced plate can be a small act of care.",
    "Leafy greens carry a little quiet iron.",
    "Berries hold a handful of bright antioxidants.",
    "Nuts tuck away warm, friendly fats.",
    "Beans bring both fiber and gentle protein.",
    "A slow breakfast can steady the morning.",
    "Yogurt offers calcium and a calm kind of comfort.",
    "Olive oil lends a soft, golden warmth.",
    "Seeds are tiny pockets of nourishment.",
    "Fruit carries sweetness the body understands.",
    "Vegetables paint the plate with quiet good.",
    "Oats wrap the morning in slow, kind energy.",
    "A cup of tea is a small, warm pause.",
    "Eggs hold a gentle, complete handful of protein.",
    "Variety on the plate is its own quiet care.",
)


def random_whisper(rng: random.Random | None = None) -> str:
    """Return one random comforting nutrition whisper.

    Pass an existing ``random.Random`` to keep selection deterministic
    (useful for tests / reproducible animations); otherwise the module
    uses the global RNG.
    """
    chooser = rng.choice if rng is not None else random.choice
    return chooser(WHISPERS)
