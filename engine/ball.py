import random
from PyQt5.QtGui import QVector2D


class Ball:
    COUNTER = 0

    def __init__(self, radius, start_position: QVector2D):
        self.position = QVector2D(start_position)
        self.radius = radius
        self._id = Ball.COUNTER
        Ball.COUNTER += 1

    def __hash__(self):
        return self._id


class GameBall(Ball):
    BALL_RADIUS = 20
    COLORS = list(range(12))

    def __init__(self, start_position, color=None):
        super().__init__(GameBall.BALL_RADIUS, start_position)
        if color is None:
            color = generate_except(GameBall.COLORS)
        self.color = color

    def move(self, vector):
        self.position += vector

    def is_intersected_by(self, other):
        return self.position.distanceToPoint(other.position) <= self.radius + other.radius

    @staticmethod
    def generate_color_except(exceptions):
        return generate_except(GameBall.COLORS, exceptions)


def generate_except(available, exceptions=None):
    exceptions = set(exceptions or [])
    available = set(available)
    return random.choice(list(available.difference(exceptions)))
