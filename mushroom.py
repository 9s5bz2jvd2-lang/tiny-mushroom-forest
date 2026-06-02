from __future__ import annotations

from dataclasses import dataclass, field
import random
import time

from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush
from PySide6.QtCore import Qt


@dataclass
class Mushroom:
    """A small animated mushroom drawn entirely with QPainter."""

    x: float
    y: float
    cap_color: QColor
    born_at: float = field(default_factory=time.monotonic)
    full_size: float = field(default_factory=lambda: random.uniform(34.0, 66.0))
    sway_seed: float = field(default_factory=lambda: random.uniform(0.0, 6.28))
    growth_seconds: float = 2.0

    @property
    def age(self) -> float:
        return max(0.0, time.monotonic() - self.born_at)

    @property
    def scale(self) -> float:
        # Smooth growth from 10% to 100% in two seconds.
        t = min(1.0, self.age / self.growth_seconds)
        eased = 1.0 - (1.0 - t) ** 3
        return 0.10 + 0.90 * eased

    def draw(self, painter: QPainter) -> None:
        size = self.full_size * self.scale
        stem_h = size * 0.82
        stem_w = size * 0.26
        cap_w = size * 1.08
        cap_h = size * 0.56
        sway = random.Random(int(self.sway_seed * 1000)).uniform(-0.8, 0.8)

        base_x = self.x
        base_y = self.y
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(base_x, base_y)

        # Soft shadow.
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 38))
        painter.drawEllipse(QPointF(0, 2), size * 0.42, size * 0.10)

        # Stem.
        stem = QPainterPath()
        stem.moveTo(-stem_w * 0.42, 0)
        stem.cubicTo(-stem_w * 0.70, -stem_h * 0.32, -stem_w * 0.42 + sway, -stem_h * 0.70, -stem_w * 0.18 + sway, -stem_h)
        stem.lineTo(stem_w * 0.18 + sway, -stem_h)
        stem.cubicTo(stem_w * 0.42 + sway, -stem_h * 0.70, stem_w * 0.70, -stem_h * 0.30, stem_w * 0.42, 0)
        stem.closeSubpath()
        painter.setBrush(QColor(248, 236, 206, 235))
        painter.setPen(QPen(QColor(126, 91, 55, 110), max(1.0, size * 0.025)))
        painter.drawPath(stem)

        # Cap.
        cap = QPainterPath()
        cap_top = -stem_h - cap_h * 0.08
        cap.moveTo(-cap_w * 0.52, cap_top + cap_h * 0.62)
        cap.cubicTo(-cap_w * 0.48, cap_top + cap_h * 0.08, -cap_w * 0.18, cap_top - cap_h * 0.10, 0, cap_top)
        cap.cubicTo(cap_w * 0.28, cap_top - cap_h * 0.08, cap_w * 0.50, cap_top + cap_h * 0.10, cap_w * 0.54, cap_top + cap_h * 0.62)
        cap.cubicTo(cap_w * 0.28, cap_top + cap_h * 0.82, -cap_w * 0.28, cap_top + cap_h * 0.82, -cap_w * 0.52, cap_top + cap_h * 0.62)
        cap.closeSubpath()
        painter.setBrush(QBrush(self.cap_color))
        painter.setPen(QPen(self.cap_color.darker(145), max(1.0, size * 0.025)))
        painter.drawPath(cap)

        # Cap underside.
        painter.setBrush(QColor(255, 238, 214, 210))
        painter.setPen(QPen(QColor(115, 71, 48, 85), max(1.0, size * 0.018)))
        painter.drawEllipse(QPointF(0, cap_top + cap_h * 0.62), cap_w * 0.42, cap_h * 0.12)

        # Spots.
        spot_color = QColor(255, 255, 238, 220)
        painter.setBrush(spot_color)
        painter.setPen(Qt.NoPen)
        spots = [(-0.22, 0.27, 0.075), (0.05, 0.18, 0.060), (0.27, 0.36, 0.052), (-0.04, 0.45, 0.045)]
        for sx, sy, sr in spots:
            painter.drawEllipse(QPointF(cap_w * sx, cap_top + cap_h * sy), size * sr, size * sr * 0.82)

        painter.restore()
