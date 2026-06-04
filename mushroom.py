from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
import time

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetricsF,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QRadialGradient,
)
from PySide6.QtCore import Qt

from whispers import random_whisper


# Script / cursive font preferences for the comforting whisper text, with a
# graceful fallback chain across macOS, Windows, and generic systems. The final
# fallback (a serif rendered italic below) keeps the words readable everywhere.
WHISPER_FONT_FAMILIES = (
    "Snell Roundhand",
    "Apple Chancery",
    "Brush Script MT",
    "Segoe Script",
    "Bradley Hand",
    "Comic Sans MS",
    "serif",
)


# How long the bubble-transformation animation lasts once a mushroom is clicked.
POP_SECONDS = 1.1

# How long the comforting whisper stays fully visible after a pop. The whisper
# is intentionally decoupled from the (shorter) bubble animation so the words
# remain readable for a relaxed, deliberate window. Requirement: >= 3 seconds,
# black, bold, cursive, and fully opaque during the hold. We use 4.2s with a
# short fade tail so the FULLY OPAQUE portion alone comfortably exceeds 3s.
WHISPER_SECONDS = 4.2
# Within WHISPER_SECONDS, the fraction reserved for a gentle fade-out at the
# very end. The whisper is held fully opaque until this final tail, so the
# required visible window is never rendered transparent. 4.2 * (1 - 0.14) =
# ~3.6s of guaranteed-opaque display — well past the 3s requirement.
WHISPER_FADE_TAIL = 0.14


# Real-mushroom-inspired morphology variants. Each value selects a distinct
# silhouette + cap-drawing routine while keeping the gentle watercolor style.
# Avoid iconic poisonous-species silhouettes (especially fly agaric / amanita)
# so the toy cannot be mistaken for a mushroom-identification guide.
SHAPES = (
    "button",      # simple rounded cap, intentionally no fly-agaric spots
    "chanterelle", # funnel / trumpet, flaring upward
    "oyster",      # shelf / fan growing sideways off the stem
    "shiitake",    # low brown convex cap with pale cracks
    "enoki",       # very slender, tall, tiny pale cap
    "porcini",     # stout bulbous stem, broad rounded cap
    "inkcap",      # tall narrow bell, slightly ragged rim
    "morel",       # pitted conical honeycomb cap
)


def _jitter(rng: random.Random, point: tuple[float, float], amount: float) -> QPointF:
    """Offset a point by a small deterministic amount for a hand-drawn feel."""
    return QPointF(
        point[0] + rng.uniform(-amount, amount),
        point[1] + rng.uniform(-amount, amount),
    )


@dataclass
class Bubble:
    """A single bubble released when a mushroom is popped."""

    dx: float
    dy: float
    radius: float
    drift: float
    speed: float
    hue: QColor


@dataclass
class Mushroom:
    """A small watercolor mushroom drawn entirely with QPainter.

    The mushroom grows from the bottom upward, is rendered in a soft,
    semi-transparent watercolor style, and bursts into rising bubbles
    when clicked.
    """

    x: float
    y: float
    cap_color: QColor
    born_at: float = field(default_factory=time.monotonic)
    full_size: float = field(default_factory=lambda: random.uniform(34.0, 66.0))
    sway_seed: float = field(default_factory=lambda: random.uniform(0.0, 6.28))
    growth_seconds: float = 2.0
    # Real-mushroom-inspired silhouette (see SHAPES). Chosen at random by default.
    shape: str = field(default_factory=lambda: random.choice(SHAPES))
    # Overall watercolor translucency (1.0 = as drawn, lower = more see-through).
    opacity: float = 0.72
    # Set to a monotonic timestamp when the mushroom is clicked / popped.
    popping_at: float | None = None
    # A gentle nutrition-themed whisper, chosen once when the mushroom is popped.
    whisper: str | None = None
    _bubbles: list[Bubble] = field(default_factory=list)
    _paint_seed: int = field(default_factory=lambda: random.randint(0, 1_000_000))

    @property
    def age(self) -> float:
        return max(0.0, time.monotonic() - self.born_at)

    @property
    def scale(self) -> float:
        # Smooth growth from 10% to 100% in two seconds.
        t = min(1.0, self.age / self.growth_seconds)
        eased = 1.0 - (1.0 - t) ** 3
        return 0.10 + 0.90 * eased

    @property
    def is_popping(self) -> bool:
        return self.popping_at is not None

    @property
    def pop_progress(self) -> float:
        """0.0 at the moment of the click, 1.0 when the bubbles have faded."""
        if self.popping_at is None:
            return 0.0
        return min(1.0, max(0.0, (time.monotonic() - self.popping_at) / POP_SECONDS))

    @property
    def whisper_progress(self) -> float:
        """0.0 at the click, 1.0 once the whisper's full visible window ends.

        Runs over ``WHISPER_SECONDS`` — deliberately longer than the bubble
        animation so the comforting words linger and stay readable.
        """
        if self.popping_at is None:
            return 0.0
        return min(1.0, max(0.0, (time.monotonic() - self.popping_at) / WHISPER_SECONDS))

    @property
    def is_dead(self) -> bool:
        """True once both the pop animation and the whisper window have finished.

        The whisper outlives the bubbles, so the mushroom is only ready for
        removal after the whisper's full (>= 3s) display window completes.
        """
        return self.popping_at is not None and self.whisper_progress >= 1.0

    @property
    def current_size(self) -> float:
        return self.full_size * self.scale

    def pop(self) -> None:
        """Begin the bubble transformation. Idempotent."""
        if self.popping_at is not None:
            return
        self.popping_at = time.monotonic()
        rng = random.Random(self._paint_seed ^ 0xB0BB1E)
        # Pick one comforting nutrition whisper to float up with the bubbles.
        self.whisper = random_whisper(rng)
        size = self.current_size
        # Tint bubbles with a gentle blend of the cap color and white so the
        # 🫧 feel reads as "made of the mushroom".
        for _ in range(rng.randint(7, 11)):
            tint = QColor(self.cap_color)
            tint = QColor(
                (tint.red() + 255) // 2,
                (tint.green() + 255) // 2,
                (tint.blue() + 255) // 2,
            )
            self._bubbles.append(
                Bubble(
                    dx=rng.uniform(-size * 0.5, size * 0.5),
                    dy=rng.uniform(-size * 0.9, -size * 0.1),
                    radius=size * rng.uniform(0.10, 0.26),
                    drift=rng.uniform(-size * 0.25, size * 0.25),
                    speed=rng.uniform(0.7, 1.4),
                    hue=tint,
                )
            )

    def _silhouette_extent(self) -> tuple[float, float, float]:
        """Return (top_y_offset, bottom_y_offset, half_width) above/below the base.

        Used by both the hit-test and the click-mask rect so every variant —
        including the tall inkcap/morel/enoki and the wide oyster shelf — is
        fully covered. Offsets are signed screen-space deltas from ``self.y``
        (negative = above the base).
        """
        size = max(self.current_size, self.full_size * 0.2)
        stem_h, stem_w, bulge = self._stem_proportions()
        # Tall-capped shapes lift their crown well above ``cap_top``.
        cap_lift = {
            "inkcap": size * 0.66,
            "morel": size * 0.70,
            "enoki": size * 0.10,
        }.get(self.shape, size * 0.10)
        top = -stem_h - cap_lift - size * 0.30
        bottom = size * 0.18
        half = max(size * 0.66, (stem_w + bulge) * 0.7)
        if self.shape == "oyster":
            half = size * 0.95   # shelf reaches sideways
        elif self.shape in ("porcini",):
            half = size * 0.80
        return top, bottom, half

    def contains(self, px: float, py: float) -> bool:
        """Hit-test in screen coordinates against the mushroom's bounding shape."""
        if self.is_popping:
            return False
        top, bottom, half = self._silhouette_extent()
        left = self.x - half
        right = self.x + half
        return left <= px <= right and (self.y + top) <= py <= (self.y + bottom)

    def bounding_rect(self) -> QRectF:
        """Screen-space rect used to build the window's click mask.

        The rect is intentionally wide so the comforting whisper text, which
        floats above the rising bubbles while popping, stays inside the window
        mask and is never clipped. (The mask in ``main.py`` also extends the
        region upward to cover the rising-bubble animation.)
        """
        top, bottom, half = self._silhouette_extent()
        # Whispers can be a couple of dozen characters; give them room on both
        # sides of the mushroom so nothing gets cut off by the input mask.
        whisper_half_w = max(half, self.full_size * 4.2)
        return QRectF(
            self.x - whisper_half_w,
            self.y + top,
            whisper_half_w * 2.0,
            (bottom - top),
        )

    # ------------------------------------------------------------------ drawing

    def draw(self, painter: QPainter) -> None:
        if self.is_popping:
            # Bubbles play out over their short window; the whisper lingers on
            # its own (longer) timeline so the words stay readable for >= 3s.
            if self.pop_progress < 1.0:
                self._draw_bubbles(painter)
            self._draw_whisper(painter)
            return
        self._draw_mushroom(painter)

    def _stem_proportions(self) -> tuple[float, float, float]:
        """Return (stem_h, stem_w, bulge) scaled to ``current_size`` per shape.

        ``bulge`` is an extra widening applied near the base (porcini) or kept
        slim/tall (enoki, inkcap). All values are in screen pixels.
        """
        size = self.current_size
        shape = self.shape
        if shape == "enoki":
            return size * 1.35, size * 0.13, 0.0          # very tall + slender
        if shape == "inkcap":
            return size * 1.20, size * 0.16, 0.0          # tall, thin
        if shape == "porcini":
            return size * 0.70, size * 0.40, size * 0.22  # short + stout/bulbous
        if shape == "oyster":
            return size * 0.50, size * 0.22, 0.0          # short side stem
        if shape == "chanterelle":
            return size * 0.86, size * 0.30, 0.0          # solid funnel foot
        if shape == "morel":
            return size * 0.74, size * 0.28, 0.06 * size
        if shape == "shiitake":
            return size * 0.66, size * 0.30, 0.0          # short, sturdy
        return size * 0.82, size * 0.26, 0.0              # button / generic rounded cap

    def _draw_mushroom(self, painter: QPainter) -> None:
        size = self.current_size
        stem_h, stem_w, bulge = self._stem_proportions()
        rng = random.Random(self._paint_seed)
        sway = random.Random(int(self.sway_seed * 1000)).uniform(-0.8, 0.8)
        jit = max(0.6, size * 0.03)  # hand-drawn edge wobble, scales with size

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.x, self.y)
        painter.setOpacity(self.opacity)

        # Soft watercolor shadow / ground bleed.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(60, 50, 40, 26))
        painter.drawEllipse(QPointF(0, 2), size * 0.46, size * 0.11)

        # ---- Stem: layered translucent washes for a watercolor body. ----
        self._draw_stem(painter, rng, size, stem_h, stem_w, bulge, sway, jit)

        # ---- Cap: dispatch to the shape-specific routine. ----
        cap_top = -stem_h
        ctx = dict(rng=rng, size=size, stem_h=stem_h, cap_top=cap_top, sway=sway, jit=jit)
        drawer = {
            "chanterelle": self._cap_chanterelle,
            "oyster": self._cap_oyster,
            "shiitake": self._cap_shiitake,
            "enoki": self._cap_enoki,
            "porcini": self._cap_porcini,
            "inkcap": self._cap_inkcap,
            "morel": self._cap_morel,
        }.get(self.shape, self._cap_button)
        drawer(painter, **ctx)

        painter.restore()

    # --------------------------------------------------------------- stem + caps

    def _draw_stem(self, painter, rng, size, stem_h, stem_w, bulge, sway, jit) -> None:
        """Watercolor stem. ``bulge`` swells the base for stout shapes."""
        base_w = stem_w + bulge
        stem = QPainterPath()
        stem.moveTo(_jitter(rng, (-base_w * 0.5, 0), jit))
        stem.cubicTo(
            _jitter(rng, (-base_w * 0.62, -stem_h * 0.30), jit),
            _jitter(rng, (-stem_w * 0.42 + sway, -stem_h * 0.70), jit),
            _jitter(rng, (-stem_w * 0.18 + sway, -stem_h), jit),
        )
        stem.lineTo(_jitter(rng, (stem_w * 0.18 + sway, -stem_h), jit))
        stem.cubicTo(
            _jitter(rng, (stem_w * 0.42 + sway, -stem_h * 0.70), jit),
            _jitter(rng, (base_w * 0.62, -stem_h * 0.30), jit),
            _jitter(rng, (base_w * 0.5, 0), jit),
        )
        stem.closeSubpath()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(248, 236, 206, 150))
        painter.drawPath(stem)
        painter.setBrush(QColor(214, 190, 150, 70))
        painter.save()
        painter.translate(stem_w * 0.18, 0)
        painter.drawPath(stem)
        painter.restore()
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(126, 91, 55, 90), max(1.0, size * 0.02)))
        painter.drawPath(stem)

    def _fill_cap(self, painter, cap: QPainterPath, size, cap_w, cap_h, cap_top,
                  *, center_x_frac=-0.08, edge_lighter=118) -> None:
        """Shared watercolor cap fill: radial gradient + bloom + broken edge."""
        center = QPointF(cap_w * center_x_frac, cap_top + cap_h * 0.10)
        grad = QRadialGradient(center, max(4.0, cap_w * 0.75))
        core = QColor(self.cap_color); core.setAlpha(205)
        mid = QColor(self.cap_color); mid.setAlpha(150)
        edge = QColor(self.cap_color.lighter(edge_lighter)); edge.setAlpha(95)
        grad.setColorAt(0.0, core)
        grad.setColorAt(0.55, mid)
        grad.setColorAt(1.0, edge)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawPath(cap)

        bloom = QColor(self.cap_color.darker(120)); bloom.setAlpha(60)
        painter.setBrush(bloom)
        painter.drawEllipse(
            QPointF(cap_w * 0.16, cap_top + cap_h * 0.30), cap_w * 0.22, cap_h * 0.30
        )

        edge_pen = QColor(self.cap_color.darker(150)); edge_pen.setAlpha(120)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(edge_pen, max(1.0, size * 0.022)))
        painter.drawPath(cap)

    def _cap_specks(self, painter, rng, size, cap_w, cap_h, cap_top) -> None:
        """Granular pigment specks for paper texture (shared)."""
        speck = QColor(self.cap_color.darker(160)); speck.setAlpha(45)
        painter.setPen(Qt.NoPen)
        painter.setBrush(speck)
        for _ in range(int(size * 0.5)):
            gx = rng.uniform(-cap_w * 0.45, cap_w * 0.45)
            gy = cap_top + rng.uniform(0, cap_h * 0.7)
            painter.drawEllipse(QPointF(gx, gy), max(0.5, size * 0.012), max(0.5, size * 0.012))

    def _domed_cap_path(self, rng, cap_w, cap_h, cap_top, jit, *, lift=0.0) -> QPainterPath:
        """A rounded cap path. ``lift`` raises the crown."""
        cap = QPainterPath()
        crown = cap_top - cap_h * lift
        cap.moveTo(_jitter(rng, (-cap_w * 0.52, cap_top + cap_h * 0.62), jit))
        cap.cubicTo(
            _jitter(rng, (-cap_w * 0.48, cap_top + cap_h * 0.08), jit),
            _jitter(rng, (-cap_w * 0.18, crown - cap_h * 0.10), jit),
            _jitter(rng, (0, crown), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.28, crown - cap_h * 0.08), jit),
            _jitter(rng, (cap_w * 0.50, cap_top + cap_h * 0.10), jit),
            _jitter(rng, (cap_w * 0.54, cap_top + cap_h * 0.62), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.28, cap_top + cap_h * 0.82), jit),
            _jitter(rng, (-cap_w * 0.28, cap_top + cap_h * 0.82), jit),
            _jitter(rng, (-cap_w * 0.52, cap_top + cap_h * 0.62), jit),
        )
        cap.closeSubpath()
        return cap

    def _cap_underside(self, painter, size, cap_w, cap_h, cap_top, *, y_frac=0.62, w_frac=0.42) -> None:
        painter.setBrush(QColor(255, 238, 214, 120))
        painter.setPen(QPen(QColor(115, 71, 48, 60), max(1.0, size * 0.015)))
        painter.drawEllipse(
            QPointF(0, cap_top + cap_h * y_frac), cap_w * w_frac, cap_h * 0.12
        )

    def _cap_button(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Plain rounded cap without fly-agaric-style white spots."""
        cap_w = size * 1.02
        cap_h = size * 0.50
        cap = self._domed_cap_path(rng, cap_w, cap_h, cap_top, jit)
        self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top)
        self._cap_underside(painter, size, cap_w, cap_h, cap_top)
        # Keep only low-opacity pigment granulation so it reads as watercolor,
        # not as the white warts/spots associated with fly agaric.
        self._cap_specks(painter, rng, size, cap_w, cap_h, cap_top)

    def _cap_chanterelle(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Chanterelle: a funnel/trumpet whose rim flares up and dips in the center."""
        cap_w = size * 1.10
        cap_h = size * 0.50
        cap = QPainterPath()
        dip = cap_top + cap_h * 0.30  # central depression
        cap.moveTo(_jitter(rng, (-cap_w * 0.58, cap_top - cap_h * 0.10), jit))  # raised left rim
        cap.cubicTo(
            _jitter(rng, (-cap_w * 0.30, cap_top + cap_h * 0.10), jit),
            _jitter(rng, (-cap_w * 0.16, dip), jit),
            _jitter(rng, (0, dip), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.16, dip), jit),
            _jitter(rng, (cap_w * 0.30, cap_top + cap_h * 0.10), jit),
            _jitter(rng, (cap_w * 0.58, cap_top - cap_h * 0.10), jit),  # raised right rim
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.34, cap_top + cap_h * 0.70), jit),
            _jitter(rng, (-cap_w * 0.34, cap_top + cap_h * 0.70), jit),
            _jitter(rng, (-cap_w * 0.58, cap_top - cap_h * 0.10), jit),
        )
        cap.closeSubpath()
        self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top, center_x_frac=0.0)
        # Soft false-gill ridges radiating from the funnel.
        ridge = QColor(self.cap_color.darker(130)); ridge.setAlpha(70)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(ridge, max(0.8, size * 0.015)))
        for k in range(-3, 4):
            fx = cap_w * 0.16 * k
            painter.drawLine(QPointF(0, dip), QPointF(fx, cap_top + cap_h * 0.66))
        self._cap_specks(painter, rng, size, cap_w, cap_h, cap_top)

    def _cap_oyster(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Oyster: a fan-shaped shelf growing sideways, offset from the stem."""
        cap_w = size * 1.24
        cap_h = size * 0.50
        off_x = cap_w * 0.28  # shelf reaches out to one side
        top = cap_top + cap_h * 0.05
        cap = QPainterPath()
        cap.moveTo(_jitter(rng, (off_x - cap_w * 0.62, top + cap_h * 0.40), jit))
        cap.cubicTo(
            _jitter(rng, (off_x - cap_w * 0.40, top - cap_h * 0.22), jit),
            _jitter(rng, (off_x + cap_w * 0.20, top - cap_h * 0.28), jit),
            _jitter(rng, (off_x + cap_w * 0.58, top + cap_h * 0.12), jit),
        )
        cap.cubicTo(
            _jitter(rng, (off_x + cap_w * 0.40, top + cap_h * 0.66), jit),
            _jitter(rng, (off_x - cap_w * 0.10, top + cap_h * 0.78), jit),
            _jitter(rng, (off_x - cap_w * 0.62, top + cap_h * 0.40), jit),
        )
        cap.closeSubpath()
        self._fill_cap(painter, cap, size, cap_w, cap_h, top, center_x_frac=0.20)
        # Fan gills fanning out from the attachment point.
        gill = QColor(255, 244, 226, 120)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(gill, max(0.8, size * 0.016)))
        anchor = QPointF(off_x - cap_w * 0.58, top + cap_h * 0.42)
        for k in range(7):
            ex = off_x + cap_w * (-0.30 + 0.14 * k)
            painter.drawLine(anchor, QPointF(ex, top + cap_h * 0.72))

    def _cap_shiitake(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Shiitake: a low convex brown cap with pale cracked patches."""
        cap_w = size * 1.06
        cap_h = size * 0.44
        cap = self._domed_cap_path(rng, cap_w, cap_h, cap_top, jit, lift=0.05)
        self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top, edge_lighter=108)
        self._cap_underside(painter, size, cap_w, cap_h, cap_top, y_frac=0.58)
        # Pale irregular cracks, like a dried shiitake surface.
        crack = QColor(236, 222, 198, 150)
        painter.setPen(Qt.NoPen)
        painter.setBrush(crack)
        for _ in range(6):
            cx = rng.uniform(-cap_w * 0.34, cap_w * 0.34)
            cy = cap_top + rng.uniform(cap_h * 0.05, cap_h * 0.45)
            w = size * rng.uniform(0.05, 0.11)
            painter.drawEllipse(QPointF(cx, cy), w, w * rng.uniform(0.35, 0.6))
        self._cap_specks(painter, rng, size, cap_w, cap_h, cap_top)

    def _cap_enoki(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Enoki: a very small pale rounded knob atop the long slender stem."""
        cap_w = size * 0.40
        cap_h = size * 0.34
        cap = self._domed_cap_path(rng, cap_w, cap_h, cap_top, jit, lift=0.30)
        # Enoki are pale ivory; wash the cap color toward white.
        pale = QColor(
            (self.cap_color.red() + 3 * 255) // 4,
            (self.cap_color.green() + 3 * 255) // 4,
            (self.cap_color.blue() + 3 * 255) // 4,
        )
        saved = self.cap_color
        try:
            self.cap_color = pale
            self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top)
        finally:
            self.cap_color = saved
        self._cap_underside(painter, size, cap_w, cap_h, cap_top, w_frac=0.34)

    def _cap_porcini(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Porcini: a broad, low, bun-like rounded cap over the stout stem."""
        cap_w = size * 1.30
        cap_h = size * 0.52
        cap = self._domed_cap_path(rng, cap_w, cap_h, cap_top, jit, lift=0.10)
        self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top, edge_lighter=112)
        self._cap_underside(painter, size, cap_w, cap_h, cap_top, y_frac=0.60, w_frac=0.50)
        # A soft pale rim, like the lighter margin of a porcino cap.
        rim = QColor(244, 232, 210, 110)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(rim, max(1.0, size * 0.03)))
        painter.drawArc(
            QRectF(-cap_w * 0.5, cap_top + cap_h * 0.20, cap_w, cap_h * 0.7),
            200 * 16, 140 * 16,
        )
        self._cap_specks(painter, rng, size, cap_w, cap_h, cap_top)

    def _cap_inkcap(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Inky cap: a tall narrow bell with a slightly ragged, melting rim."""
        cap_w = size * 0.62
        cap_h = size * 0.92
        cap = QPainterPath()
        cap.moveTo(_jitter(rng, (-cap_w * 0.48, cap_top + cap_h * 0.30), jit))
        cap.cubicTo(
            _jitter(rng, (-cap_w * 0.46, cap_top - cap_h * 0.30), jit),
            _jitter(rng, (-cap_w * 0.16, cap_top - cap_h * 0.62), jit),
            _jitter(rng, (0, cap_top - cap_h * 0.66), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.16, cap_top - cap_h * 0.62), jit),
            _jitter(rng, (cap_w * 0.46, cap_top - cap_h * 0.30), jit),
            _jitter(rng, (cap_w * 0.48, cap_top + cap_h * 0.30), jit),
        )
        # Ragged melting rim.
        cap.lineTo(_jitter(rng, (cap_w * 0.30, cap_top + cap_h * 0.40), jit * 2.2))
        cap.lineTo(_jitter(rng, (cap_w * 0.10, cap_top + cap_h * 0.30), jit * 2.2))
        cap.lineTo(_jitter(rng, (-cap_w * 0.12, cap_top + cap_h * 0.42), jit * 2.2))
        cap.lineTo(_jitter(rng, (-cap_w * 0.30, cap_top + cap_h * 0.30), jit * 2.2))
        cap.closeSubpath()
        self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top - cap_h * 0.30,
                       center_x_frac=0.0)
        # Faint vertical striations down the bell.
        stria = QColor(self.cap_color.darker(135)); stria.setAlpha(60)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(stria, max(0.7, size * 0.012)))
        for k in range(-2, 3):
            x = cap_w * 0.16 * k
            painter.drawLine(QPointF(x, cap_top - cap_h * 0.50),
                             QPointF(x * 1.4, cap_top + cap_h * 0.28))

    def _cap_morel(self, painter, rng, size, stem_h, cap_top, sway, jit) -> None:
        """Morel: a tall conical cap with a pitted honeycomb surface."""
        cap_w = size * 0.78
        cap_h = size * 1.00
        cap = QPainterPath()
        cap.moveTo(_jitter(rng, (-cap_w * 0.50, cap_top + cap_h * 0.30), jit))
        cap.cubicTo(
            _jitter(rng, (-cap_w * 0.44, cap_top - cap_h * 0.30), jit),
            _jitter(rng, (-cap_w * 0.14, cap_top - cap_h * 0.66), jit),
            _jitter(rng, (0, cap_top - cap_h * 0.70), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.14, cap_top - cap_h * 0.66), jit),
            _jitter(rng, (cap_w * 0.44, cap_top - cap_h * 0.30), jit),
            _jitter(rng, (cap_w * 0.50, cap_top + cap_h * 0.30), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.28, cap_top + cap_h * 0.46), jit),
            _jitter(rng, (-cap_w * 0.28, cap_top + cap_h * 0.46), jit),
            _jitter(rng, (-cap_w * 0.50, cap_top + cap_h * 0.30), jit),
        )
        cap.closeSubpath()
        self._fill_cap(painter, cap, size, cap_w, cap_h, cap_top - cap_h * 0.30,
                       center_x_frac=0.0, edge_lighter=108)
        # Honeycomb pits: darker hollows separated by pale ridges.
        pit = QColor(self.cap_color.darker(165)); pit.setAlpha(110)
        painter.setPen(Qt.NoPen)
        rows = [(-0.50, 0.16), (-0.30, 0.20), (-0.10, 0.22), (0.10, 0.20), (0.30, 0.16)]
        for ry, rw in rows:
            cy = cap_top + cap_h * ry
            span = cap_w * rw
            n = max(2, int(span / max(1.0, size * 0.10)))
            for i in range(n):
                cx = -span + (2 * span) * (i / max(1, n - 1))
                painter.setBrush(pit)
                painter.drawEllipse(QPointF(cx, cy), size * 0.07, size * 0.085)

    def _draw_bubbles(self, painter: QPainter) -> None:
        """Render the 🫧 bubble transformation: rising, expanding, fading bubbles."""
        p = self.pop_progress
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.x, self.y)
        painter.setPen(Qt.NoPen)

        # The mushroom briefly "dissolves": fade the original out over the first
        # third of the animation while bubbles emerge.
        ghost = max(0.0, 1.0 - p * 3.0)
        if ghost > 0.01:
            painter.setOpacity(self.opacity * ghost * 0.6)
            faded = QColor(self.cap_color)
            faded.setAlpha(120)
            painter.setBrush(faded)
            size = self.current_size
            painter.drawEllipse(QPointF(0, -size * 0.7), size * 0.5, size * 0.6)

        for b in self._bubbles:
            # Each bubble rises and grows as the animation progresses.
            rise = b.dy - p * b.speed * self.current_size * 1.6
            sway = math.sin((p * 6.0) + b.drift) * b.drift * 0.4
            grow = 0.6 + p * 0.9
            alpha = max(0.0, 1.0 - p)
            center = QPointF(b.dx + sway, rise)
            r = b.radius * grow

            # Bubble fill: translucent radial sheen.
            grad = QRadialGradient(
                QPointF(center.x() - r * 0.3, center.y() - r * 0.3), r * 1.3
            )
            inner = QColor(b.hue)
            inner.setAlpha(int(150 * alpha))
            outer = QColor(b.hue)
            outer.setAlpha(int(40 * alpha))
            grad.setColorAt(0.0, QColor(255, 255, 255, int(180 * alpha)))
            grad.setColorAt(0.35, inner)
            grad.setColorAt(1.0, outer)
            painter.setOpacity(1.0)
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(center, r, r)

            # Rim highlight ring for that glassy bubble look.
            ring = QColor(255, 255, 255, int(110 * alpha))
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(ring, max(0.8, r * 0.08)))
            painter.drawEllipse(center, r, r)
            painter.setPen(Qt.NoPen)

            # Tiny specular dot.
            spec = QColor(255, 255, 255, int(200 * alpha))
            painter.setBrush(spec)
            painter.drawEllipse(
                QPointF(center.x() - r * 0.32, center.y() - r * 0.34),
                r * 0.16,
                r * 0.16,
            )

        painter.restore()

    def _whisper_font(self, point_size: float) -> QFont:
        """Build a bold script/cursive font, walking the fallback chain.

        Qt's font matcher substitutes a system font if a family is missing, so
        we register the whole preference list as substitutes and rely on the
        final serif to stay readable everywhere. The text is bold and cursive
        per the display requirements.
        """
        font = QFont()
        font.setFamilies(list(WHISPER_FONT_FAMILIES))
        font.setStyleHint(QFont.Cursive)
        font.setPointSizeF(max(9.0, point_size))
        font.setBold(True)            # required: bold whisper text
        font.setItalic(True)          # keeps the serif fallback feeling hand-lettered
        font.setLetterSpacing(QFont.PercentageSpacing, 102.0)
        return font

    def _draw_whisper(self, painter: QPainter) -> None:
        """Draw the comforting nutrition whisper: black, bold, cursive, opaque.

        The whisper runs on its own (>= 3s) timeline via ``whisper_progress``,
        independent of the shorter bubble animation. It is held FULLY OPAQUE for
        the entire required display window and only eases out over a short tail
        at the very end — it is never rendered transparent during the >= 3s hold.
        Coordinates are relative to the mushroom base; this method translates the
        painter to ``self.x, self.y`` itself.
        """
        if not self.whisper:
            return

        wp = self.whisper_progress
        # Hold fully opaque for the whole window, then ease out over the final
        # tail only. Requirement: no transparency during the required display.
        if wp < (1.0 - WHISPER_FADE_TAIL):
            alpha = 1.0
        else:
            tail = (wp - (1.0 - WHISPER_FADE_TAIL)) / WHISPER_FADE_TAIL
            alpha = max(0.0, 1.0 - tail)
        if alpha <= 0.0:
            return

        size = self.current_size
        # Float gently upward over the whole window — the words may move, but
        # they stay opaque and legible the entire time.
        base_y = -size * 1.15 - wp * size * 1.6
        point_size = max(12.0, size * 0.32)

        painter.save()
        painter.translate(self.x, self.y)
        painter.setOpacity(1.0)
        font = self._whisper_font(point_size)
        painter.setFont(font)

        metrics = QFontMetricsF(font)
        text_w = metrics.horizontalAdvance(self.whisper)
        text_h = metrics.height()
        # A roomy text rect, centered over the mushroom, so the script font is
        # never clipped even with its generous ascenders/descenders.
        rect = QRectF(
            -text_w * 0.5 - size * 0.4,
            base_y - text_h,
            text_w + size * 0.8,
            text_h * 1.6,
        )

        # Soft pale halo so black text stays legible over any desktop. This is a
        # backdrop only — the ink itself is solid black and fully opaque.
        halo = QColor(255, 255, 255, int(210 * alpha))
        painter.setPen(QPen(halo))
        for ox, oy in ((1.6, 1.6), (-1.6, 1.6), (1.6, -1.6), (-1.6, -1.6),
                       (0.0, 2.0), (0.0, -2.0), (2.0, 0.0), (-2.0, 0.0)):
            painter.drawText(
                rect.translated(ox, oy), Qt.AlignHCenter | Qt.AlignVCenter, self.whisper
            )

        # Solid black ink. Opaque during the full required window (alpha == 1.0).
        ink = QColor(0, 0, 0)
        ink.setAlphaF(alpha)
        painter.setPen(QPen(ink))
        painter.drawText(rect, Qt.AlignHCenter | Qt.AlignVCenter, self.whisper)

        painter.restore()
