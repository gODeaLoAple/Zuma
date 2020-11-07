from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLayout
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QPixmap
from gui import utils


class StartWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        start_button = QPushButton("Start game", self)
        start_button.clicked.connect(self.on_start_click)
        start_button.setFixedSize(200, 50)

        create_level_button = QPushButton("Create level", self)
        create_level_button.clicked.connect(self.on_create_click)
        create_level_button.setFixedSize(200, 50)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.on_exit_click)
        exit_button.setFixedSize(200, 50)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(start_button)
        vbox.addWidget(create_level_button)
        vbox.addWidget(exit_button)

    @pyqtSlot()
    def on_start_click(self):
        self.parent().open_choose_level_menu()

    @pyqtSlot()
    def on_create_click(self):
        self.parent().open_creator_menu()
        
    @pyqtSlot()
    def on_exit_click(self):
        self.parent().exit()


