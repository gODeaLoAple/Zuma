from PyQt5.QtWidgets import QStackedWidget

from gui.game_window import GameWindow
from gui.start_window import StartWindow
from gui.defeat_window import DefeatWindow
from gui.win_window import WinWindow
from gui.choose_level_window import LevelsWindow


class ApplicationWindow(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.game = GameWindow(self)
        self._levels = LevelsWindow(self)
        self._start = StartWindow(self)
        self._defeat = DefeatWindow(self)
        self._win = WinWindow(self)
        self.init_ui()

    def init_ui(self):
        self.addWidget(self.game)
        self.addWidget(self._levels)
        self.addWidget(self._start)
        self.addWidget(self._defeat)
        self.addWidget(self._win)
        self.open_main_menu()

    def start_game(self, level):
        self.set_menu(self.game)
        self.game.start(level)

    def exit(self):
        self.parent().close()

    def restart_level(self):
        self.game.restart()
        self.set_menu(self.game)

    def open_main_menu(self):
        self.set_menu(self._start)

    def open_win_menu(self):
        self.set_menu(self._win)

    def open_defeat_menu(self):
        self.set_menu(self._defeat)

    def open_choose_level_menu(self):
        self.set_menu(self._levels)

    def set_menu(self, widget):
        self.setCurrentWidget(widget)
