class Bonus:
    def __init__(self, bonus_id):
        self.bonus_id = bonus_id

    def __hash__(self):
        return self.bonus_id

    def is_null(self):
        return False


class NullBonus(Bonus):
    def __init__(self, bonus_id):
        super().__init__(bonus_id)

    def set(self, game):
        ...

    def unset(self, game):
        ...

    def is_null(self):
        return True


class ReverseMoveBonus(Bonus):
    def __init__(self, bonus_id):
        super().__init__(bonus_id)

    def set(self, game):
        game.mover.set_reverse(True)

    def unset(self, game):
        game.mover.set_reverse(False)


class SlowMoveBonus(Bonus):
    def __init__(self, bonus_id):
        super().__init__(bonus_id)

    def set(self, game):
        game.mover.set_slow_balls(True)

    def unset(self, game):
        game.mover.set_slow_balls(False)


class FastShotBonus(Bonus):
    def __init__(self, bonus_id):
        super().__init__(bonus_id)

    def set(self, game):
        game.mover.set_fast_shots(True)

    def unset(self, game):
        game.mover.set_fast_shots(False)


class BoomBonus(Bonus):
    def __init__(self, bonus_id):
        super().__init__(bonus_id)

    def set(self, game):
        game.mover.set_boom(True)

    def unset(self, game):
        game.mover.set_boom(False)


class QueueBonus(Bonus):
    def __init__(self, bonus_id):
        super().__init__(bonus_id)

    def set(self, game):
        game.mover.set_shot_queue(True)

    def unset(self, game):
        game.mover.set_shot_queue(False)


class Bonuses:
    NULL = NullBonus(0)
    REVERSE_MOVING = ReverseMoveBonus(1)
    SLOW_MOVING = SlowMoveBonus(2)
    FAST_SHOT = FastShotBonus(3)
    BOOM = BoomBonus(4)
    QUEUE = QueueBonus(5)


Bonuses.COLLECTION = [x for x in Bonuses.__dict__.values() if isinstance(x, Bonus)]