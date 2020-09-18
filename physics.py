import math
import time
from tkinter import Tk, Canvas

# TODO научиться двигать по чекпоинтам 1 шарик - OK
# TODO научиться двигать по чекпоинтам n шаров - OK
# TODO научиться двигать по чекпоинтам динамически появляющиеся шары - OK
# TODO научиться удалять одноцветные шары (голова останавливается,
#  хвост движется)
# TODO научиться добавлять шар в середину "змейки"
# TODO научиться стрелять шаром
# TODO научиться обрабатывать коллизии между выстреленным шаром и шарами из
#  змейки

from PyQt5.QtCore import QPointF
from enum import Enum
import itertools
import random


class Ball:
    def __init__(self, radius, start_position):
        self.position = start_position
        self.radius = radius


class GameBall(Ball):
    BALL_RADIUS = 10

    def __init__(self, start_position, color=None):
        super().__init__(GameBall.BALL_RADIUS, start_position)
        self.color = color or "black"
        self.velocity = QPointF(1, 0)

    def is_in_front_of_when_collide_with(self, other):
        vector_between_centers = other.position - self.position
        return QPointF.dotProduct(other.velocity, vector_between_centers) >= 0

    def move(self, x, y):
        self.position.setX(x)
        self.position.setY(y)

class Direction(Enum):
    Right = QPointF(1, 0),
    Up = QPointF(0, -1),
    Left = QPointF(-1, 0),
    Down = QPointF(0, 1)


class Drawer:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=800, height=600)
        self.canvas.pack()

    def clear(self):
        self.canvas.create_rectangle(0, 0, 800, 600, fill="white")

    def draw_ball(self, ball):
        x = ball.position[0]
        y = ball.position[1]
        r = ball.radius
        color = ball.color
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)

    def invalidate(self):
        self.root.update()


class Interval:
    OPENED = 0
    LEFT_CLOSED_ONLY = 1
    RIGHT_CLOSED_ONLY = 2
    CLOSED = 3

    def __init__(self, left_side, right_side, close_type=CLOSED):
        self.min = min(left_side, right_side)
        self.max = max(left_side, right_side)
        self.type = close_type

    def __contains__(self, item):
        try:
            if self.type == Interval.OPENED:
                return self.min < item < self.max
            if self.type == Interval.RIGHT_CLOSED_ONLY:
                return self.min < item <= self.max
            if self.type == Interval.LEFT_CLOSED_ONLY:
                return self.min <= item < self.max
            if self.type == Interval.CLOSED:
                return self.min <= item <= self.max
            raise ValueError("Неопределенный тип интервала")
        except TypeError:
            print("Ожидалось число")


class Function:
    def __init__(self, function, domain):
        self.f = function
        self.domain = domain

    def __call__(self, x):
        try:
            is_in_domain = x in self.domain
        except ValueError:
            is_in_domain = False
        if is_in_domain:
            return self.f(x)
        raise ValueError(f"Значение функции не определено в точке {x}")


def construct_function(functions):
    def f(x):
        for function in functions:
            if x in function.domain:
                return function(x)
    return f


def construct_domain(domains):
    return Interval(min(d.min for d in domains), max(d.max for d in domains))


class PartialFunction(Function):
    def __init__(self, *functions):
        function = construct_function(functions)
        domain = construct_domain(list(f.domain for f in functions))
        super().__init__(function, domain)


def linear(kx, ky, x0=0, y0=0):
    return lambda t: (kx * t + x0, ky * t + y0)


def circle(r, x0=0, y0=0):
    return lambda t: (r * math.cos(t * 2 * math.pi) + x0,
                      r * math.sin(t * 2 * math.pi) + y0)

def squared_distance(coords1, coords2):
    return (coords2[0] - coords1[0]) ** 2 + (coords2[1] - coords2[1]) ** 2

def main():
    path = Function(circle(50, 100, 100), Interval(0, 1))
    t = 0
    start = path(0)
    balls = [GameBall(start)]
    timers = [0]
    drawer = Drawer()
    min_dist = (GameBall.BALL_RADIUS * 2)
    delay = 0.01
    while True:
        drawer.clear()
        for i in range(len(balls)):
            timers[i] += delay
            if timers[i] >= path.domain.max:
                timers[i] = path.domain.min
            balls[i].position = path(timers[i])
            drawer.draw_ball(balls[i])
        if squared_distance(balls[-1].position, start) > min_dist:
            balls.append(GameBall(start))
            timers.append(0)

        drawer.invalidate()


main()
