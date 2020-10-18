from engine.ball import GameBall
from engine.mover import BallsMover
import enum


class Game:
    SCORE_TO_WIN = 100
    SCORE_PER_BALL = 5

    def __init__(self, player_position, path):
        self.player = GameBall(player_position)
        self._start_ball = GameBall(path[0])
        self._mover = BallsMover(path)
        self._score = 0

    def step(self):
        self.try_add_ball()
        self._mover.move()
        self._mover.resolve_collisions()
        self._score += self._mover.remove_same_color_segments_and_return_count_of_removed_balls() * Game.SCORE_PER_BALL

    def try_add_ball(self):
        if self._mover.can_add_ball(self._start_ball):
            color = GameBall.generate_color_except([b.ball.color for b in self._mover.last_checkpointers])
            self._mover.add_ball(GameBall(self._start_ball.position, color))

    def shot(self, vector):
        self._mover.add_shot(self.player, vector)
        self.player = GameBall(self.player.position)

    @property
    def score(self):
        return self._score

    @property
    def is_game_end(self):
        return self.is_win or self.is_defeat

    @property
    def is_defeat(self):
        return self._mover.is_any_on_last_checkpoint()

    @property
    def is_win(self):
        return self._score >= Game.SCORE_TO_WIN

    @property
    def balls(self):
        yield from self._mover.balls
        yield self.player

