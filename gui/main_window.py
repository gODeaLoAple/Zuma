from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5 import QtCore, QtWidgets, QtGui
from gui.application_window import ApplicationWindow
import gui.utils as utils

WIDTH, HEIGHT = 800, 600


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Zuma"
        self.menu = None
        self.init_ui()

    def init_ui(self):
        QtGui.QFontDatabase.addApplicationFont(utils.Fonts.DIMBO_REGULAR)
        self.setWindowTitle(self.title)
        self.setFixedSize(WIDTH, HEIGHT)
        self.setFont(QtGui.QFont("Dimbo Regular", (self.width() + self.height() // 2) // 60))
        self.menu = ApplicationWindow(self)
        self.setCentralWidget(self.menu)
        self.setMouseTracking(True)
        self.show()

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QtCore.QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    ...
                recursive_set(child)

        QtWidgets.QWidget.setMouseTracking(self, flag)
        recursive_set(self)
