import sys
# TODO научиться двигать по чекпоинтам 1 шарик - OK
# TODO научиться двигать по чекпоинтам n шаров - OK
# TODO научиться двигать по чекпоинтам динамически появляющиеся шары - OK
# TODO научиться удалять одноцветные шары - ОК
# TODO научиться добавлять шар в середину "змейки" - ОК
# TODO научиться стрелять шаром - ОК
# TODO научиться обрабатывать коллизии между выстреленным шаром и шарами из
#  змейки - ОК

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
