from threading import Timer

from PyQt5.QtGui import QVector2D, QPainter, QColor
from PyQt5.QtWidgets import QWidget

from engine.game import Game


class GameWindow(QWidget):
    FPS = 1 / 100

    def __init__(self, parent=None):
        super().__init__(parent)
        self._game = Game(QVector2D(300, 300),
            [
               QVector2D(0, 0),
               QVector2D(50, 0),
            ])
        self.timer = Timer(GameWindow.FPS, self.step)

        self.initUI()

    def restart(self):
        self.timer.cancel()
        self._game = Game(QVector2D(300, 300),
                          [
                              QVector2D(0, 0),
                              QVector2D(500, 0),
                              QVector2D(500, 200),
                              QVector2D(100, 200),
                              QVector2D(100, 400),
                              QVector2D(500, 400)
                          ])
        self.timer = Timer(GameWindow.FPS, self.step)
        self.start()

    def start(self):
        self.timer.start()

    def step(self):
        if self._game.is_game_end:
            self.on_win()
            return
        self._game.step()
        self.update()
        Timer(GameWindow.FPS, self.step).start()

    def initUI(self):
        self.releaseKeyboard()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        for ball in self._game.balls:
            painter.setBrush(QColor(*ball.color))
            painter.drawEllipse(ball.position.x(), ball.position.y(), 2 * ball.radius, 2 * ball.radius)
        painter.end()

    def mousePressEvent(self, event):
        dx = event.x() - self._game.player.position.x()
        dy = event.y() - self._game.player.position.y()
        self._game.shot(QVector2D(dx, dy))

    def on_defeat(self):
        self.parent().open_defeat_menu()

    def on_win(self):
        self.parent().open_win_menu()
