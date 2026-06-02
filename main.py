from __future__ import annotations

import random
import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QAction, QColor, QIcon, QPainter, QPixmap
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
    """Transparent always-on-top desktop overlay that grows tiny mushrooms."""

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
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setFocusPolicy(Qt.StrongFocus)

        self.repaint_timer = QTimer(self)
        self.repaint_timer.setInterval(16)
        self.repaint_timer.timeout.connect(self.update)
        self.repaint_timer.start()

        self.showFullScreen()
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

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override name
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        for mushroom in self.mushrooms:
            mushroom.draw(painter)

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
    tray.setToolTip("Tiny Mushroom Forest — ESC or tray menu to exit")
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
