from engine.ball import GameBall
from engine.mover import BallsMover
from engine.level import Level
from PyQt5.QtCore import QSizeF
from engine.bonuses import Bonuses
import random


class Game:
    SCORE_PER_BALL = 5

    def __init__(self, size: QSizeF, level: Level):
        self.level = level.scale(size.width(), size.height())
        self.player = None
        self._start_ball = None
        self._mover = None
        self._score = None
        self.on_combo = None
        self.timer = None
        self.bonuses = None
        self.reset()

    def reset(self):
        self.player = GameBall(self.level.player_position)
        self._start_ball = GameBall(self.level.path[0])
        self._mover = BallsMover(self.level.path)
        self._mover.on_balls_remove = self.on_balls_remove
        self.bonuses = {bonus: 0 for bonus in Bonuses.COLLECTION}
        self._score = 0
        self.timer = 0

    def step(self, dt):
        self.handle_bonuses(dt)
        self.timer += dt
        self._mover.move()
        self._mover.resolve_collisions()
        if not self.is_game_end and not self.has_bonus(Bonuses.REVERSE_MOVING):
            self.try_add_ball()

    def on_balls_remove(self, balls):
        for ball in balls:
            if ball.is_bonus():
                self.add_bonus(ball.bonus, random.randint(3_000, 5_000))
        if len(balls) > 0:
            self.on_combo()
        self._score += len(balls) * Game.SCORE_PER_BALL

    def try_add_ball(self):
        if self._mover.can_add_ball(self._start_ball):
            color = GameBall.generate_color_except([b.ball.color for b in self._mover.last_checkpointers])
            self._mover.add_ball(GameBall(self._start_ball.position, color))

    def shot(self, vector):
        self._mover.add_shot(self.player, vector)
        self.player = GameBall(self.player.position)

    def _on_combo(self):
        if self.on_combo:
            self.on_combo()

    def handle_bonuses(self, dt):
        for bonus in self.bonuses:
            self.decrease_bonus(bonus, dt)

    def add_bonus(self, bonus, time):
        if self.bonuses[bonus] == 0:
            bonus.set(self)
        self.bonuses[bonus] += time

    def has_bonus(self, bonus):
        return self.bonuses[bonus] > 0

    def decrease_bonus(self, bonus, dt):
        self.bonuses[bonus] = max(0, self.bonuses[bonus] - dt)
        if self.bonuses[bonus] == 0:
            bonus.unset(self)

    @property
    def mover(self):
        return self._mover

    @property
    def score(self):
        return self._score

    @property
    def is_game_end(self):
        return self.is_win or self.is_defeat

    @property
    def is_defeat(self):
        return self.time_to_defeat <= 0 or self._mover.is_any_on_last_checkpoint()

    @property
    def is_win(self):
        return self._score >= self.level.scores_to_win

    @property
    def balls(self):
        yield from self._mover.balls

    @property
    def bonuses_balls(self):
        yield from self._mover.bonuses

    @property
    def checkpoints(self):
        return self._mover.checkpoints

    @property
    def time_to_defeat(self):
        return self.level.time - self.timer
