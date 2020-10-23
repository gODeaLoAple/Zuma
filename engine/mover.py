import collections
import itertools
from engine.ball import GameBall


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


class Checkpointer(GameBallDecorator):
    def __init__(self, ball, checkpoints):
        super().__init__(ball)
        self._checkpoints = checkpoints
        self._current_index = 0

    def set_current_checkpoint_index(self, value):
        if not 0 < value <= len(self._checkpoints):
            raise IndexError()
        self._current_index = value

    def get_current_checkpoint_index(self):
        return self._current_index

    @property
    def next_checkpoints(self):
        return self._checkpoints[self._current_index:]

    @property
    def current_checkpoint(self):
        return self._checkpoints[self._current_index]

    @property
    def previous_checkpoint(self):
        return self._checkpoints[self._current_index - 1]

    def move(self, speed=0.7):
        if not self.is_on_last_checkpoint():
            vector = self.current_checkpoint - self._ball.position
            self._ball.move(vector.normalized() * speed)
            if vector.length() <= speed / 2:
                self._current_index += 1

    def move_reverse(self, speed=1):
        if self._current_index >= 0:
            vector = self.previous_checkpoint - self._ball.position
            self._ball.move(vector.normalized() * speed)
            if vector.length() <= speed / 2:
                self._current_index -= 1

    def is_on_last_checkpoint(self):
        return len(self._checkpoints) == self._current_index


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
        self._free_balls_start_index = -1

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
        if self.has_free_balls():
            self._move_only_free_balls()
        else:
            self._move_all_balls()
        for ball in self._shot_balls:
            ball.move()

    def has_free_balls(self):
        return self._free_balls_start_index != -1

    def _move_only_free_balls(self):
        for i in range(self._free_balls_start_index):
            self._balls[i].move_reverse(3)
        self._update_free_balls_start_index()

    def _update_free_balls_start_index(self):
        self._free_balls_start_index = self._find_last_space_between_checkpointers_index()
        if self._free_balls_start_index == -1:
            self._align_balls()

    def _align_balls(self):
        for i in range(len(self._balls) - 1):
            current_ball, next_ball = self._balls[i:i + 2]
            while not current_ball.ball.is_intersected_by(next_ball.ball):
                next_ball.move()

    def _find_last_space_between_checkpointers_index(self):
        index = -1
        for i in range(1, len(self._balls)):
            previous, current = self._balls[i - 1:i + 1]
            if not previous.ball.is_intersected_by(current.ball):
                index = i
        return index

    def _move_all_balls(self):
        for ball in self._balls:
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
        checkpointer = Checkpointer(GameBall(last_ball.position, ball.color), self._checkpoints)
        checkpointer.set_current_checkpoint_index(last_ball.get_current_checkpoint_index())
        while not can_add_ball(checkpointer.ball, next_balls):
            for x in next_balls:
                if not x.is_on_last_checkpoint():
                    x.move()
                else:
                    return
        self._balls.insert(index + 1, checkpointer)

    def remove_same_color_segments_and_return_count_of_removed_balls(self):
        for start, stop in get_same_value_segments([b.ball.color for b in self._balls]):
            if stop - start >= BallsMover.LINE_MIN_LENGTH:
                del self._balls[start:stop]
                self._update_free_balls_start_index()
                return stop - start
        return 0

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
