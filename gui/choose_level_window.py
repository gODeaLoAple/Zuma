from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt
from engine.level import load_levels
import os
import functools


class LevelsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._levels = load_levels(os.path.join(os.getcwd(), "levels"))
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)

        for level in self._levels:
            level_button = QPushButton(level.name, self)
            level_button.clicked.connect(functools.partial(self.on_level_click, level))
            level_button.setFixedSize(200, 50)
            vbox.addWidget(level_button)

        exit_button = QPushButton("Back", self)
        exit_button.clicked.connect(self.on_exit_click)
        exit_button.setFixedSize(200, 50)
        vbox.addWidget(exit_button)

    @pyqtSlot()
    def on_level_click(self, level):
        self.parent().start_game(level)

    @pyqtSlot()
    def on_exit_click(self):
        self.parent().open_main_menu()
