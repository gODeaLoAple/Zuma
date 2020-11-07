from engine.bonuses import Bonuses
from engine.ball import GameBall
import random


class GameBallDecorator:
    def __init__(self, ball):
        self._ball = ball

    @property
    def ball(self):
        return self._ball

    @property
    def radius(self):
        return self._ball.radius

    @property
    def position(self):
        return self._ball.position

    def __hash__(self):
        return hash(self._ball)


def generate_random_bonus():
    return random.choice(Bonuses.COLLECTION)


def random_true(percent):
    return random.randint(0, 100) < percent


class Checkpointer(GameBallDecorator):

    def __init__(self, ball, checkpoints):
        super().__init__(ball)
        self._checkpoints = checkpoints
        self._current_index = 0
        self.bonus = generate_random_bonus() if random_true(5) else Bonuses.NULL

    def set_current_checkpoint_index(self, value):
        if not 0 <= value < len(self._checkpoints):
            raise IndexError()
        self._current_index = value

    def get_current_checkpoint_index(self):
        return self._current_index

    def is_bonus(self):
        return not self.bonus.is_null()

    @property
    def next_checkpoints(self):
        return self._checkpoints[self._current_index:]

    @property
    def current_checkpoint(self):
        return self._checkpoints[self._current_index]

    @property
    def previous_checkpoint(self):
        return self._checkpoints[self._current_index - 1]

    def move(self, speed):
        if not self.is_on_last_checkpoint():
            vector = self.current_checkpoint - self._ball.position
            self._ball.move(vector.normalized() * speed)
            if vector.length() <= speed / 2:
                self._current_index += 1

    def move_reverse(self, speed):
        if self._current_index > 0:
            vector = self.previous_checkpoint - self._ball.position
            if vector.length() <= speed / 2:
                self._current_index -= 1
        else:
            vector = self._checkpoints[0] - self._checkpoints[1]
        self._ball.move(vector.normalized() * speed)

    def is_on_last_checkpoint(self):
        return len(self._checkpoints) == self._current_index


class Shot(GameBallDecorator):
    def __init__(self, ball, vector):
        super().__init__(ball)
        self._vector = vector.normalized()

    def move(self, speed):
        self._ball.move(self._vector * speed)

    def copy(self):
        return Shot(GameBall(self.position, self.ball.color), self._vector)
