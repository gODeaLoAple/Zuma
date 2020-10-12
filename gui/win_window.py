from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot, Qt


class WinWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        text_label = QLabel("You are win!", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFixedSize(200, 50)

        restart_button = QPushButton("Next Level", self)
        restart_button.setFixedSize(200, 50)
        restart_button.clicked.connect(self.on_next_level_click)

        open_main_menu_button = QPushButton("Main menu", self)
        open_main_menu_button.setFixedSize(200, 50)
        open_main_menu_button.clicked.connect(self.on_main_menu_click)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(text_label)
        vbox.addWidget(restart_button)
        vbox.addWidget(open_main_menu_button)

    @pyqtSlot()
    def on_next_level_click(self):
        self.parent().restart_level()

    @pyqtSlot()
    def on_main_menu_click(self):
        self.parent().open_main_menu()
