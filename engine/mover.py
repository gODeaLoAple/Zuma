import collections
import itertools
from engine.ball import GameBall


class GameBallDecorator:
    def __init__(self, ball):
        self._ball = ball

    def move(self):
        ...

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


class Checkpointer(GameBallDecorator):
    SPEED = 0.7

    def __init__(self, ball, checkpoints):
        super().__init__(ball)
        self._checkpoints = checkpoints
        self._currentIndex = 0

    @property
    def next_checkpoints(self):
        return self._checkpoints[self._currentIndex:]

    @property
    def current_checkpoint(self):
        return self._checkpoints[self._currentIndex]

    def move(self):
        vector = self.current_checkpoint - self._ball.position
        self._ball.move(vector.normalized() * Checkpointer.SPEED)
        if vector.length() <= Checkpointer.SPEED / 2:
            self._currentIndex += 1

    def is_on_last_checkpoint(self):
        return len(self._checkpoints) == self._currentIndex


class Shot(GameBallDecorator):
    SPEED = 10

    def __init__(self, ball, vector):
        super().__init__(ball)
        self._vector = vector.normalized() * Shot.SPEED

    def move(self):
        self._ball.move(self._vector)


class BallsMover:
    LINE_MIN_LENGTH = 3

    def __init__(self, checkpoints, balls=None):
        self._checkpoints = tuple(checkpoints)
        self._balls = [Checkpointer(ball, self._checkpoints) for ball in (balls or [])]
        self._shot_balls = []

    @property
    def last_checkpointers(self):
        return self._balls[-(BallsMover.LINE_MIN_LENGTH + 1): -1]

    @property
    def balls(self):
        return (x.ball for x in itertools.chain(self._balls, self._shot_balls))

    @property
    def checkpoint_balls(self):
        return (x.ball for x in self._balls)

    def can_add_ball(self, ball):
        return can_add_ball(ball, self._balls)

    def add_ball(self, ball):
        self._balls.append(Checkpointer(ball, self._checkpoints))

    def add_shot(self, ball, vector):
        self._shot_balls.append(Shot(ball, vector))

    def move(self):
        for ball in itertools.chain(self._balls, self._shot_balls):
            ball.move()

    def resolve_collisions(self):
        for shot, index in self.get_collisions():
            self._shot_balls.remove(shot)
            self.insert_ball(index, shot.ball)

    def get_collisions(self):
        collisions = {}
        for shot in self._shot_balls:
            for index, checkpointer in enumerate(self._balls):
                distance = shot.position.distanceToPoint(checkpointer.position)
                previous = self._balls[collisions.get(shot, index)]
                if shot.position.distanceToPoint(previous.position) <= distance < shot.ball.radius:
                    collisions[shot] = index
        return collisions.items()

    def insert_ball(self, index, ball):
        next_balls = self._balls[:index + 1]
        last_ball = next_balls[-1]
        checkpointer = Checkpointer(GameBall(last_ball.position, ball.color), last_ball.next_checkpoints)
        while not can_add_ball(checkpointer.ball, next_balls):
            for x in next_balls:
                x.move()
        self._balls.insert(index + 1, checkpointer)

    def count_same_color_in_line_balls(self):
        same_value_segments = get_same_value_segments([b.ball.color for b in self._balls])
        return sum(stop - start for stop, start in same_value_segments if stop - start >= BallsMover.LINE_MIN_LENGTH)

    def remove_same_color_segments(self):
        for start, stop in get_same_value_segments([b.ball.color for b in self._balls]):
            if stop - start >= BallsMover.LINE_MIN_LENGTH:
                del self._balls[start:stop]

    def is_any_on_last_checkpoint(self):
        return any(ball.is_on_last_checkpoint() for ball in self._balls)


def get_same_value_segments(values):
    start = 0
    segments = []
    for stop, color in enumerate(values):
        if color != values[start]:
            segments.append((start, stop))
            start = stop
    segments.append((start, len(values)))
    return segments


def can_add_ball(ball, balls):
    return not any(ball.is_intersected_by(other) for other in balls if other != ball)
