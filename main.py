from __future__ import annotations

import random
import sys

from PySide6.QtCore import QTimer, Qt, QRect
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget

from mushroom import Mushroom


CAP_COLORS = [
    QColor("#e84d4d"),  # red
    QColor("#f28a2e"),  # orange
    QColor("#ffd34d"),  # yellow
    QColor("#61c96f"),  # green
    QColor("#4a8df6"),  # blue
    QColor("#8f5bd5"),  # purple
    QColor("#ff75b5"),  # pink
]


class MushroomForestOverlay(QWidget):
    """Transparent always-on-top desktop overlay that grows tiny mushrooms.

    Mushrooms are rendered in a soft, semi-transparent watercolor style and
    grow from the bottom upward. Clicking a mushroom transforms it into a
    burst of rising bubbles. So the overlay stays non-intrusive, only the
    pixels occupied by mushrooms are clickable — clicks anywhere else fall
    through to the desktop via a dynamic input mask.
    """

    def __init__(self) -> None:
        super().__init__()
        self.mushrooms: list[Mushroom] = []
        self.max_mushrooms = 20

        self.setWindowTitle("Tiny Mushroom Forest")
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # NOTE: we intentionally do NOT set WA_TransparentForMouseEvents here.
        # Instead we mask the window down to just the mushroom regions so the
        # desktop stays clickable everywhere else (see _update_input_mask).
        self.setFocusPolicy(Qt.StrongFocus)

        self.repaint_timer = QTimer(self)
        self.repaint_timer.setInterval(16)
        self.repaint_timer.timeout.connect(self._tick)
        self.repaint_timer.start()

        self.showFullScreen()
        self._update_input_mask()
        self._schedule_next_mushroom()

    def _schedule_next_mushroom(self) -> None:
        QTimer.singleShot(random.randint(5_000, 15_000), self._spawn_then_reschedule)

    def _spawn_then_reschedule(self) -> None:
        self.add_mushroom()
        self._schedule_next_mushroom()

    def add_mushroom(self) -> None:
        margin = 80
        width = max(1, self.width())
        height = max(1, self.height())
        x = random.randint(margin, max(margin, width - margin))
        y = random.randint(int(height * 0.35), max(int(height * 0.35), height - margin))
        self.mushrooms.append(Mushroom(x=x, y=y, cap_color=random.choice(CAP_COLORS)))
        if len(self.mushrooms) > self.max_mushrooms:
            self.mushrooms.pop(0)
        self.update()

    def _tick(self) -> None:
        """Per-frame update: drop finished pops, refresh the click mask, repaint."""
        before = len(self.mushrooms)
        self.mushrooms = [m for m in self.mushrooms if not m.is_dead]
        if len(self.mushrooms) != before:
            self._update_input_mask()
        self.update()

    def _update_input_mask(self) -> None:
        """Mask the window to the mushrooms' regions so the rest of the desktop
        remains clickable. Bubbles rise upward, so the regions extend above each
        mushroom to keep the pop animation visible while it plays."""
        if not self.mushrooms:
            # Empty 1px region: the whole window is click-through and invisible.
            self.setMask(QRegion(QRect(0, 0, 0, 0)))
            return
        region = QRegion()
        for m in self.mushrooms:
            r = m.bounding_rect()
            # Extend upward to cover the rising bubble animation.
            rect = QRect(
                int(r.x()),
                int(r.y() - m.full_size * 1.8),
                int(r.width()),
                int(r.height() + m.full_size * 1.8),
            )
            region = region.united(QRegion(rect))
        self.setMask(region)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override name
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        for mushroom in self.mushrooms:
            mushroom.draw(painter)

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt override name
        """Pop the topmost mushroom under the cursor into bubbles."""
        pos = event.position()
        px, py = pos.x(), pos.y()
        # Iterate newest-first so the most recently grown (visually on top) wins.
        for mushroom in reversed(self.mushrooms):
            if mushroom.contains(px, py):
                mushroom.pop()
                self._update_input_mask()
                event.accept()
                return
        event.ignore()

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt override name
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        else:
            super().keyPressEvent(event)


def make_tray_icon(app: QApplication, overlay: MushroomForestOverlay) -> QSystemTrayIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, True)
    Mushroom(32, 54, QColor("#e84d4d"), full_size=42).draw(painter)
    painter.end()

    menu = QMenu()
    grow_action = QAction("Grow one mushroom", menu)
    grow_action.triggered.connect(overlay.add_mushroom)
    quit_action = QAction("Exit", menu)
    quit_action.triggered.connect(app.quit)
    menu.addAction(grow_action)
    menu.addSeparator()
    menu.addAction(quit_action)

    tray = QSystemTrayIcon(QIcon(pixmap), app)
    tray.setToolTip("Tiny Mushroom Forest — click a mushroom to pop it, ESC to exit")
    tray.setContextMenu(menu)
    tray.show()
    return tray


def main() -> int:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    overlay = MushroomForestOverlay()
    tray = make_tray_icon(app, overlay)
    overlay._tray_icon = tray  # keep tray alive for the lifetime of the overlay
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
