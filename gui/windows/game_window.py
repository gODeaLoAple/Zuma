from PyQt5.QtGui import QVector2D, QPainter, QColor, QImage, QBitmap, QTransform, QPixmap, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedLayout
from PyQt5.Qt import Qt, QTimer, QSound, QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl, QRectF, QPoint
from engine.game import Game
from engine.bonuses import Bonuses
import random
import gui.utils as utils
import math


class GameWindow(QWidget):
    FPS = 60

    def __init__(self, parent=None):
        super().__init__(parent)
        self._game = None
        self.timer = QTimer(self)
        self.timer.setInterval(1000 / GameWindow.FPS)
        self.timer.timeout.connect(self.step)
        self.score_label = None
        self.score_text = None
        self.time_label = None
        self.time_text = None
        self._player = QMediaPlayer(self)
        self._combo_player = QMediaPlayer(self)
        self._background_player = QMediaPlayer(self)
        self._background_player.setVolume(10)
        self._background_playlist = QMediaPlaylist(self)
        self._mouse_position = QVector2D(0, 0)
        self._frog_size = 100
        self.initUI()

    def initUI(self):
        self.score_label = QLabel(self)
        self.score_label.move(25, 0)
        self.score_label.setFixedSize(200, 100)

        self.score_text = QLabel("Scores: 0", self)
        self.score_text.move(self.score_label.x() + 25, -5)
        self.score_text.setFixedSize(100, 100)

        self.time_label = QLabel(self)
        self.time_label.setFixedSize(200, 100)
        self.time_label.move(self.parent().parent().width() - self.time_label.width() - 25, 0)

        self.time_text = QLabel("Time: 0", self)
        self.time_text.move(self.time_label.x() + 25, - 5)
        self.time_text.setFixedSize(100, 100)

        for sound in random.choices(utils.Sound.BACKGROUND):
            self._background_playlist.addMedia(sound)
        self._background_player.setPlaylist(self._background_playlist)

        self.releaseKeyboard()

    def restart(self):
        if self.timer.isActive():
            self.timer.stop()
        self._game.reset()
        self.timer.start()
        self._background_player.play()

    def start(self, level):
        if self.timer.isActive():
            self.timer.stop()
        self._game = Game(self.size(), level)
        self._game.on_combo = self.play_combo
        self.timer.start()
        self._background_player.play()

    def play_combo(self):
        self._combo_player.setMedia(random.choice(utils.Sound.COMBO))
        self._combo_player.play()

    def step(self):
        if self._game.is_game_end:
            self.timer.stop()
            self.on_game_end()
            return
        self._game.step(self.timer.interval())
        self.score_text.setText(f"Scores: {self._game.score}")
        s = self._game.time_to_defeat // 1000
        self.time_text.setText(f"Time: {s // 60}:{s % 60}")
        self.score_label.setPixmap(QPixmap.fromImage(utils.UI.LABEL))
        self.time_label.setPixmap(QPixmap.fromImage(utils.UI.LABEL))
        self.update()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self._draw_path(painter)
        self._draw_player(painter)
        self._draw_balls(painter)
        self._draw_skull(painter)
        self._draw_bonuses(painter)
        painter.end()

    def _draw_path(self, painter):
        path = self._game.checkpoints
        for i in range(len(path) - 1):
            x, y = path[i:i+2]
            painter.setPen(QPen())
            painter.drawLine(x.x() + 20, x.y() + 20, y.x() + 20, y.y() + 20)

    def _draw_player(self, painter):
        player_position = self._game.player.position
        player_radius = self._game.player.radius
        angle = self._extract_angle()
        dx, dy = player_position.x() + player_radius, player_position.y() + player_radius

        painter.translate(dx, dy)
        painter.rotate(-angle)
        painter.drawImage(QRectF(-self._frog_size / 2, -self._frog_size / 2, self._frog_size, self._frog_size),
                          utils.Images.FROG)
        ball = utils.Images.BALLS[self._game.player.color]
        ball_pos = QRectF(
            -self._player_ball_distance - player_radius / 2,
            self._player_ball_distance + player_radius / 2,
            player_radius * 2,
            player_radius * 2)
        painter.drawImage(ball_pos, ball)
        painter.rotate(angle)
        painter.translate(-dx, -dy)

    @property
    def _player_ball_distance(self):
        return self._frog_size / 8

    def _extract_angle(self):
        vector = self._mouse_position - self._game.player.position
        vector2 = QVector2D(1, 0)
        angle = math.acos(QVector2D.dotProduct(vector, vector2) / (vector.length() * vector2.length()))
        if vector.y() > 0:
            angle = 2 * math.pi - angle
        return (angle + math.pi / 2) * 180 / math.pi

    def _draw_balls(self, painter):
        eps = 5
        for ball in self._game.balls:
            rect = QRectF(ball.position.x(), ball.position.y(), 2 * ball.radius + eps, 2 * ball.radius + eps)
            painter.drawImage(rect, utils.Images.BALLS[ball.color])

    def _draw_bonuses(self, painter):
        for ball in self._game.bonuses_balls:
            rect = QRectF(ball.position.x() + ball.radius / 2, ball.position.y() + ball.radius / 2,
                          ball.radius,  ball.radius)
            painter.setBrush(QColor(255, 255, 255, 128))
            painter.drawEllipse(rect)

    def _draw_skull(self, painter):
        pos = self._game.level.path[-1]
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(QRectF(pos.x(), pos.y(), 50, 50))

    def mouseMoveEvent(self, event):
        self._mouse_position = QVector2D(event.localPos())

    def mousePressEvent(self, event):
        dx = event.x() - self._game.player.position.x() - self._player_ball_distance
        dy = event.y() - self._game.player.position.y() - self._player_ball_distance
        self._game.shot(QVector2D(dx, dy))
        self.play_sound(random.choice(utils.Sound.SHOT))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self._game.add_bonus(Bonuses.REVERSE_MOVING, 1000)
        elif event.key() == Qt.Key_S:
            self._game.add_bonus(Bonuses.SLOW_MOVING, 1000)
        elif event.key() == Qt.Key_F:
            self._game.add_bonus(Bonuses.FAST_SHOT, 1000)
        elif event.key() == Qt.Key_B:
            self._game.add_bonus(Bonuses.BOOM, 1000)
        elif event.key() == Qt.Key_Q:
            self._game.add_bonus(Bonuses.QUEUE, 1000)

    def on_game_end(self):
        self._background_player.stop()
        if self._game.is_win:
            self.on_win()
        else:
            self.on_defeat()

    def on_defeat(self):
        self.play_sound(random.choice(utils.Sound.DEFEAT))
        self.parent().open_defeat_menu()

    def on_win(self):
        self.play_sound(random.choice(utils.Sound.WIN))
        self.parent().open_win_menu()

    def play_sound(self, sound):
        self._player.setMedia(sound)
        self._player.play()
