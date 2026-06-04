from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
import time

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QRadialGradient,
)
from PySide6.QtCore import Qt


# How long the bubble-transformation animation lasts once a mushroom is clicked.
POP_SECONDS = 1.1


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
    # Overall watercolor translucency (1.0 = as drawn, lower = more see-through).
    opacity: float = 0.72
    # Set to a monotonic timestamp when the mushroom is clicked / popped.
    popping_at: float | None = None
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
    def is_dead(self) -> bool:
        """True once the pop animation has fully finished (ready for removal)."""
        return self.popping_at is not None and self.pop_progress >= 1.0

    @property
    def current_size(self) -> float:
        return self.full_size * self.scale

    def pop(self) -> None:
        """Begin the bubble transformation. Idempotent."""
        if self.popping_at is not None:
            return
        self.popping_at = time.monotonic()
        rng = random.Random(self._paint_seed ^ 0xB0BB1E)
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

    def contains(self, px: float, py: float) -> bool:
        """Hit-test in screen coordinates against the mushroom's bounding shape."""
        if self.is_popping:
            return False
        size = self.current_size
        stem_h = size * 0.82
        cap_w = size * 1.08
        # Generous rounded bounding box covering stem + cap.
        left = self.x - cap_w * 0.6
        right = self.x + cap_w * 0.6
        top = self.y - stem_h - size * 0.7
        bottom = self.y + size * 0.15
        return left <= px <= right and top <= py <= bottom

    def bounding_rect(self) -> QRectF:
        """Screen-space rect used to build the window's click mask."""
        size = max(self.current_size, self.full_size * 0.2)
        stem_h = size * 0.82
        cap_w = size * 1.2
        return QRectF(
            self.x - cap_w * 0.6,
            self.y - stem_h - size * 0.8,
            cap_w * 1.2,
            stem_h + size * 0.95,
        )

    # ------------------------------------------------------------------ drawing

    def draw(self, painter: QPainter) -> None:
        if self.is_popping:
            self._draw_bubbles(painter)
            return
        self._draw_mushroom(painter)

    def _draw_mushroom(self, painter: QPainter) -> None:
        size = self.current_size
        stem_h = size * 0.82
        stem_w = size * 0.26
        cap_w = size * 1.08
        cap_h = size * 0.56
        rng = random.Random(self._paint_seed)
        sway = random.Random(int(self.sway_seed * 1000)).uniform(-0.8, 0.8)
        jit = max(0.6, size * 0.03)  # hand-drawn edge wobble, scales with size

        base_x = self.x
        base_y = self.y
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(base_x, base_y)
        painter.setOpacity(self.opacity)

        # Soft watercolor shadow / ground bleed.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(60, 50, 40, 26))
        painter.drawEllipse(QPointF(0, 2), size * 0.46, size * 0.11)

        # ---- Stem: layered translucent washes for a watercolor body. ----
        stem = QPainterPath()
        stem.moveTo(_jitter(rng, (-stem_w * 0.42, 0), jit))
        stem.cubicTo(
            _jitter(rng, (-stem_w * 0.70, -stem_h * 0.32), jit),
            _jitter(rng, (-stem_w * 0.42 + sway, -stem_h * 0.70), jit),
            _jitter(rng, (-stem_w * 0.18 + sway, -stem_h), jit),
        )
        stem.lineTo(_jitter(rng, (stem_w * 0.18 + sway, -stem_h), jit))
        stem.cubicTo(
            _jitter(rng, (stem_w * 0.42 + sway, -stem_h * 0.70), jit),
            _jitter(rng, (stem_w * 0.70, -stem_h * 0.30), jit),
            _jitter(rng, (stem_w * 0.42, 0), jit),
        )
        stem.closeSubpath()
        # Two overlapping washes (lighter base + a soft inner shadow) read as paint.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(248, 236, 206, 150))
        painter.drawPath(stem)
        painter.setBrush(QColor(214, 190, 150, 70))
        painter.save()
        painter.translate(stem_w * 0.18, 0)
        painter.drawPath(stem)
        painter.restore()
        # Faint, slightly broken outline = ink/pencil line.
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(126, 91, 55, 90), max(1.0, size * 0.02)))
        painter.drawPath(stem)

        # ---- Cap: radial watercolor gradient + jittered hand-drawn edge. ----
        cap = QPainterPath()
        cap_top = -stem_h - cap_h * 0.08
        cap.moveTo(_jitter(rng, (-cap_w * 0.52, cap_top + cap_h * 0.62), jit))
        cap.cubicTo(
            _jitter(rng, (-cap_w * 0.48, cap_top + cap_h * 0.08), jit),
            _jitter(rng, (-cap_w * 0.18, cap_top - cap_h * 0.10), jit),
            _jitter(rng, (0, cap_top), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.28, cap_top - cap_h * 0.08), jit),
            _jitter(rng, (cap_w * 0.50, cap_top + cap_h * 0.10), jit),
            _jitter(rng, (cap_w * 0.54, cap_top + cap_h * 0.62), jit),
        )
        cap.cubicTo(
            _jitter(rng, (cap_w * 0.28, cap_top + cap_h * 0.82), jit),
            _jitter(rng, (-cap_w * 0.28, cap_top + cap_h * 0.82), jit),
            _jitter(rng, (-cap_w * 0.52, cap_top + cap_h * 0.62), jit),
        )
        cap.closeSubpath()

        # Radial gradient: saturated near the crown, washing out toward the rim.
        center = QPointF(-cap_w * 0.08, cap_top + cap_h * 0.10)
        grad = QRadialGradient(center, cap_w * 0.75)
        core = QColor(self.cap_color)
        core.setAlpha(205)
        mid = QColor(self.cap_color)
        mid.setAlpha(150)
        edge = QColor(self.cap_color.lighter(118))
        edge.setAlpha(95)
        grad.setColorAt(0.0, core)
        grad.setColorAt(0.55, mid)
        grad.setColorAt(1.0, edge)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawPath(cap)

        # A second, smaller off-center wash = pooled pigment (watercolor bloom).
        bloom = QColor(self.cap_color.darker(120))
        bloom.setAlpha(60)
        painter.setBrush(bloom)
        painter.drawEllipse(
            QPointF(cap_w * 0.16, cap_top + cap_h * 0.30), cap_w * 0.22, cap_h * 0.30
        )

        # Broken pigment edge.
        edge_pen = QColor(self.cap_color.darker(150))
        edge_pen.setAlpha(120)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(edge_pen, max(1.0, size * 0.022)))
        painter.drawPath(cap)

        # Cap underside — soft translucent crescent.
        painter.setBrush(QColor(255, 238, 214, 120))
        painter.setPen(QPen(QColor(115, 71, 48, 60), max(1.0, size * 0.015)))
        painter.drawEllipse(
            QPointF(0, cap_top + cap_h * 0.62), cap_w * 0.42, cap_h * 0.12
        )

        # ---- Spots: irregular translucent dots, like dabbed paint. ----
        painter.setPen(Qt.NoPen)
        spots = [(-0.22, 0.27, 0.075), (0.05, 0.18, 0.060), (0.27, 0.36, 0.052), (-0.04, 0.45, 0.045)]
        for sx, sy, sr in spots:
            dab = QColor(255, 255, 244, 150)
            painter.setBrush(dab)
            cx = cap_w * sx + rng.uniform(-jit, jit)
            cy = cap_top + cap_h * sy + rng.uniform(-jit, jit)
            painter.drawEllipse(QPointF(cx, cy), size * sr, size * sr * 0.82)

        # Granular pigment specks for paper texture.
        speck = QColor(self.cap_color.darker(160))
        speck.setAlpha(45)
        painter.setBrush(speck)
        for _ in range(int(size * 0.5)):
            gx = rng.uniform(-cap_w * 0.45, cap_w * 0.45)
            gy = cap_top + rng.uniform(0, cap_h * 0.7)
            painter.drawEllipse(QPointF(gx, gy), max(0.5, size * 0.012), max(0.5, size * 0.012))

        painter.restore()

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
