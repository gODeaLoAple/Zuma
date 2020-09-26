from PyQt5.QtWidgets import QMainWindow

from gui.game_window import GameWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.g = GameWindow()
        self.setCentralWidget(self.g)
        self.resize(800, 600)
        self.show()

    def keyPressEvent(self, e):
        self.centralWidget().keyPressEvent(e)

