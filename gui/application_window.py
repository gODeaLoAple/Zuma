from PyQt5.QtWidgets import QStackedWidget
from PyQt5.Qt import QMediaPlayer, QMediaContent, QImage
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QPalette, QBrush
from gui.windows import *
from gui import utils
import random


class ApplicationWindow(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.game = GameWindow(self)
        self._levels = LevelsWindow(self)
        self._start = StartWindow(self)
        self._defeat = DefeatWindow(self)
        self._win = WinWindow(self)
        self._creator = LevelCreatorWindow(self)
        self.init_ui()

    def init_ui(self):
        self.addWidget(self.game)
        self.addWidget(self._levels)
        self.addWidget(self._start)
        self.addWidget(self._defeat)
        self.addWidget(self._win)
        self.addWidget(self._creator)
        self.open_main_menu()

    def start_game(self, level):
        self.setBackground(random.choice(utils.Images.BACKGROUND))
        self.set_menu(self.game)
        self.game.start(level)

    def exit(self):
        self.parent().close()

    def restart_level(self):
        self.setBackground(random.choice(utils.Images.BACKGROUND))
        self.game.restart()
        self.set_menu(self.game)

    def setBackground(self, image_path):
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QImage(image_path).scaled(self.parent().size())))
        self.parent().setPalette(palette)

    def open_main_menu(self):
        self.setBackground(utils.Images.SILENT_HILL[1])
        self.set_menu(self._start)

    def open_creator_menu(self):
        self.set_menu(self._creator)

    def open_win_menu(self):
        self.setBackground(utils.Images.SILENT_HILL[2])
        self.set_menu(self._win)

    def open_defeat_menu(self):
        self.setBackground(utils.Images.SILENT_HILL[0])
        self.set_menu(self._defeat)

    def open_choose_level_menu(self):
        self.removeWidget(self._levels)
        self._levels = LevelsWindow(self)
        self.addWidget(self._levels)
        self._levels.load_levels()
        self.setBackground(utils.Images.SILENT_HILL[0])
        self.set_menu(self._levels)

    def set_menu(self, widget):
        self.setCurrentWidget(widget)
