import unittest
from engine.ball import generate_except, GameBall
from PyQt5.QtGui import QVector2D


class TestGeneration(unittest.TestCase):
    def test_throw_exception_if_available_is_none(self):
        available = None
        self.assertRaises(TypeError, generate_except, available)

    def test_throw_exception_if_available_is_empty(self):
        available = []
        self.assertRaises(IndexError, generate_except, available)

    def test_generate_without_exceptions(self):
        available = [0]
        self.assertEqual(generate_except(available), 0)

    def test_generate_with_exceptions(self):
        available = [1, 2]
        exceptions = [1]
        self.assertEqual(generate_except(available, exceptions), 2)


class TestBall(unittest.TestCase):
    @staticmethod
    def are_intersected(a, b):
        return a.is_intersected_by(b) and b.is_intersected_by(a)

    def test_intersected_when_not_intersected(self):
        a = GameBall(QVector2D(0, 0))
        b = GameBall(a.position + QVector2D(GameBall.BALL_RADIUS * 2 + 1, 0))
        self.assertFalse(TestBall.are_intersected(a, b))

    def test_intersected_when_intersected(self):
        a = GameBall(QVector2D(0, 0))
        b = GameBall(a.position)
        self.assertTrue(TestBall.are_intersected(a, b))

    def test_intersected_when_intersect_by_only_border(self):
        a = GameBall(QVector2D(0, 0))
        b = GameBall(a.position + QVector2D(GameBall.BALL_RADIUS * 2, 0))
        self.assertTrue(TestBall.are_intersected(a, b))


if __name__ == "__main__":
    unittest.main()
