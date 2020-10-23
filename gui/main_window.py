from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from gui.application_window import ApplicationWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Zuma"
        self.menu = ApplicationWindow(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.menu)
        self.setFixedSize(800, 600)
        self.show()
