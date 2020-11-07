import itertools
from engine.ball import GameBall

from engine.ball_decorators import GameBallDecorator, Checkpointer, Shot


class MoverStates:
    FORWARD = 0
    REVERSED = 1


class BoomStates:
    OFF = 0
    ON = 1


class ShotQueueStates:
    OFF = 0
    ON = 1


class BallsMover:
    LINE_MIN_LENGTH = 3
    BALLS_SPEED = 0.5
    SHOTS_SPEED = 15

    def __init__(self, checkpoints, balls=None):
        self._checkpoints = tuple(checkpoints)
        self._balls = [Checkpointer(ball, self._checkpoints) for ball in (balls or [])]
        self._shot_balls = []
        self._free_balls_start_index = -1
        self.on_balls_remove = lambda x: ...
        self.balls_speed = BallsMover.BALLS_SPEED
        self.shots_speed = BallsMover.SHOTS_SPEED
        self.state = MoverStates.FORWARD
        self.boom_state = BoomStates.OFF
        self.shot_queue_state = ShotQueueStates.OFF

    @property
    def checkpoints(self):
        return self._checkpoints

    @property
    def last_checkpointers(self):
        return self._balls[-(BallsMover.LINE_MIN_LENGTH + 1): -1]

    @property
    def balls(self):
        return (x.ball for x in itertools.chain(self._balls, self._shot_balls))

    @property
    def bonuses(self):
        return (x.ball for x in self._balls if x.is_bonus())

    @property
    def checkpoint_balls(self):
        return (x.ball for x in self._balls)

    def set_slow_balls(self, toggle):
        self.balls_speed = 0.3 if toggle else BallsMover.BALLS_SPEED

    def set_fast_shots(self, toggle):
        self.shots_speed = 20 if toggle else BallsMover.SHOTS_SPEED

    def set_reverse(self, toggle):
        self.state = MoverStates.REVERSED if toggle else MoverStates.FORWARD

    def set_boom(self, toggle):
        self.boom_state = BoomStates.ON if toggle else BoomStates.OFF

    def set_shot_queue(self, toggle):
        self.shot_queue_state = ShotQueueStates.ON if toggle else ShotQueueStates.OFF

    def can_add_ball(self, ball):
        return can_add_ball(ball, self._balls)

    def add_ball(self, ball):
        self._balls.append(Checkpointer(ball, self._checkpoints))

    def add_shot(self, ball, vector):
        if self.shot_queue_state == ShotQueueStates.OFF:
            self._shot_balls.append(Shot(ball, vector))
        elif self.shot_queue_state == ShotQueueStates.ON:
            shot = Shot(ball, vector)
            for i in range(3):
                while self._shot_balls and shot.ball.is_intersected_by(self._shot_balls[-1].ball):
                    self._move_shots()
                self._shot_balls.append(shot.copy())

    def move(self):
        if self.state == MoverStates.FORWARD:
            self.move_forward()
        elif self.state == MoverStates.REVERSED:
            self.move_reverse()
        else:
            raise Exception(f"Непредвиденное значение 'BallsMover.state' = {self.state}")

    def move_reverse(self):
        for ball in self._balls:
            ball.move_reverse(self.balls_speed)
        self._move_shots()

    def move_forward(self):
        if self.has_free_balls():
            self._move_only_free_balls()
        else:
            self._move_all_balls()
            self._align_balls()
        self._move_shots()

    def _move_shots(self):
        for ball in self._shot_balls:
            ball.move(self.shots_speed)

    def has_free_balls(self):
        return self._free_balls_start_index != -1

    def _move_only_free_balls(self):
        for i in range(self._free_balls_start_index):
            self._balls[i].move_reverse(3)
        self._update_free_balls_start_index()

    def _update_free_balls_start_index(self):
        self._free_balls_start_index = self._find_last_space_between_checkpointers_index()

    def _align_balls(self):
        for i in range(len(self._balls) - 1):
            current_ball, next_ball = self._balls[i:i + 2]
            if current_ball.position.distanceToPoint(next_ball.position) > 2 * current_ball.radius:
                next_ball.move(self.balls_speed)

    def _find_last_space_between_checkpointers_index(self):
        index = -1
        for i in range(1, len(self._balls)):
            previous, current = self._balls[i - 1:i + 1]
            if not previous.ball.is_intersected_by(current.ball):
                index = i
        return index

    def _move_all_balls(self):
        for ball in self._balls:
            ball.move(self.balls_speed)

    def resolve_collisions(self):
        for shot, index in self.get_collisions():
            self._shot_balls.remove(shot)
            self.insert_ball(index, shot.ball)
            if self.boom_state == BoomStates.ON:
                self.boom_near_balls(index + 1)
            elif self.boom_state == BoomStates.OFF and not self.has_free_balls():
                self.remove_same_color_segments()

    def boom_near_balls(self, index):
        b = min((2 * index + BallsMover.LINE_MIN_LENGTH) // 2, len(self._balls))
        a = max((2 * index - BallsMover.LINE_MIN_LENGTH) // 2, 0)
        self.on_balls_remove(self._balls[a:b])
        del self._balls[a:b]

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
                    x.move(self.balls_speed)
                else:
                    return
        self._balls.insert(index + 1, checkpointer)

    def remove_same_color_segments(self):
        for start, stop in get_same_value_segments([b.ball.color for b in self._balls]):
            if stop - start >= BallsMover.LINE_MIN_LENGTH:
                self.on_balls_remove(self._balls[start:stop])
                del self._balls[start:stop]
                self._update_free_balls_start_index()

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
