import glob
import json
import os
from PyQt5.QtGui import QVector2D
from PyQt5.Qt import QTime


def load_levels(directory):
    levels = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            levels.append(load_level(os.path.join(directory, file)))
    return levels


def load_level(path):
    with open(path, "r", encoding="utf8") as f:
        level = json.load(f)
    path = [QVector2D(x[0], x[1]) for x in level["path"]]
    player = QVector2D(level["player"][0], level["player"][1])
    return Level(level["name"], path, level["scores"], player, level["time"])


class Level:
    def __init__(self, name, path, scores_to_win, player_position, time):
        self.name = name
        self.path = path
        self.scores_to_win = scores_to_win
        self.player_position = player_position
        self.time = time

    def scale(self, scale_x, scale_y):
        factor = QVector2D(scale_x, scale_y)
        return Level(
            self.name,
            [point * factor for point in self.path],
            self.scores_to_win,
            self.player_position * factor,
            self.time
        )
