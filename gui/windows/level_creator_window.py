from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QBrush, QVector2D
import json
import random
import time
import os


LEVELS_DIR = os.path.join(os.getcwd(), "levels")
CHECKPOINT_STATE = 0
PLAYER_STATE = 1


class LevelCreatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = []
        self.player = None
        self._creator = CreatorPaintWindow(self)
        self.init_ui()

    def init_ui(self):
        button_size = 100
        checkpoint_button = QPushButton("Checkpoint")
        checkpoint_button.clicked.connect(self.choose_checkpoint)
        checkpoint_button.setFixedSize(button_size, button_size)

        player_button = QPushButton("Player")
        player_button.clicked.connect(self.choose_player)
        player_button.setFixedSize(button_size, button_size)

        create_button = QPushButton("Create")
        create_button.clicked.connect(self.create_level)
        create_button.setFixedSize(button_size, button_size)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.exit_creator)
        exit_button.setFixedSize(button_size, button_size)

        widget = QWidget(self)
        vbox = QVBoxLayout(widget)
        vbox.setAlignment(Qt.AlignRight)
        vbox.addWidget(checkpoint_button)
        vbox.addWidget(player_button)
        vbox.addWidget(create_button)
        vbox.addWidget(exit_button)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self._creator, stretch=1)
        hbox.addWidget(widget)

    @pyqtSlot()
    def choose_checkpoint(self):
        self._creator.state = CHECKPOINT_STATE

    @pyqtSlot()
    def choose_player(self):
        self._creator.state = PLAYER_STATE

    @pyqtSlot()
    def create_level(self):
        with open(os.path.join(LEVELS_DIR, f"level{time.time()}.json"), "w+", encoding="utf8") as f:
            json.dump(self._creator.get_level_data(), f)

    @pyqtSlot()
    def exit_creator(self):
        self.parent().open_main_menu()


class CreatorPaintWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = CHECKPOINT_STATE
        self.points = []
        self.player = None
        self.init_ui()

    def get_level_data(self):
        x, y = self.size().width(), self.size().height()
        return {
            "time": random.randint(2, 5) * 60 * 1000,
            "name": "level",
            "player": self._parse_point(self.player, x, y),
            "path": [self._parse_point(point, x, y) for point in self.points],
            "scores": random.randint(300, 500)
        }

    def _parse_point(self, p: QVector2D, x, y):
        return (p.x() / x, p.y() / y)

    def init_ui(self):
        self.update()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setBackground(QBrush(QColor(0, 0, 0)))
        qp.setBrush(QBrush(QColor(0, 0, 0)))
        for a in self.points:
            qp.drawEllipse(a.x(), a.y(), 20, 20)

        if self.player:
            qp.setBrush(QBrush(QColor(255, 0, 0)))
            qp.drawEllipse(self.player.x(), self.player.y(), 20, 20)

    def mousePressEvent(self, e):
        print(e.x(), e.y())
        point = QVector2D(e.x() - 10, e.y() - 10)
        if self.state == CHECKPOINT_STATE:
            if e.button() == Qt.LeftButton:
                self.points.append(point)
            elif e.button() == Qt.RightButton:
                self.delete_near_point(point)
        elif self.state == PLAYER_STATE:
            self.player = point
        self.update()

    def delete_near_point(self, vec):
        m = None
        for a in self.points:
            if not m or m.distanceToPoint(vec) > a.distanceToPoint(vec):
                m = a
        if m:
            self.points.remove(m)
