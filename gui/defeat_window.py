from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStaticText


class DefeatWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        text_label = QLabel("You are defeat", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFixedSize(200, 50)

        restart_button = QPushButton("Restart", self)
        restart_button.setFixedSize(200, 50)
        restart_button.clicked.connect(self.on_restart_click)

        open_main_menu_button = QPushButton("Main menu", self)
        open_main_menu_button.setFixedSize(200, 50)
        open_main_menu_button.clicked.connect(self.on_to_main_menu_click)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(text_label)
        vbox.addWidget(restart_button)
        vbox.addWidget(open_main_menu_button)

    @pyqtSlot()
    def on_restart_click(self):
        self.parent().restart_level()

    @pyqtSlot()
    def on_to_main_menu_click(self):
        self.parent().open_main_menu()
