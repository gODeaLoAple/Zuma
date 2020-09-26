from engine.ball import GameBall
from engine.mover import BallsMover


class Game:

    def __init__(self, player_position, path):
        self.player = GameBall(player_position)
        self._start_ball = GameBall(path[0])
        self._mover = BallsMover(path)

    def step(self):
        if self._mover.can_add_ball(self._start_ball):
            color = GameBall.generate_color_except([b.ball.color for b in self._mover.last_checkpointers])
            self._mover.add_ball(GameBall(self._start_ball.position, color))
        self._mover.move()
        self._mover.resolve_collisions()
        self._mover.remove_same_color_segments()

    def shot(self, vector):
        self._mover.add_shot(self.player, vector)
        self.player = GameBall(self.player.position)

    @property
    def is_game_end(self):
        return self._mover.is_any_on_last_checkpoint()

    @property
    def balls(self):
        yield from self._mover.balls
        yield self.player

