import glob
import json
import os
from PyQt5.QtGui import QVector2D


def load_levels(directory):
    os.chdir(directory)
    levels = []
    for path in glob.glob("*.json"):
        try:
            levels.append(load_level(path))
        except Exception as e:
            ...
    return levels


def load_level(path):
    with open(path, "r", encoding="utf8") as f:
        level = json.load(f)
    path = [QVector2D(x[0], x[1]) for x in level["path"]]
    player = QVector2D(level["player"][0], level["player"][1])
    return Level(level["name"], path, level["scores"], player)


class Level:
    def __init__(self, name, path, scores_to_win, player_position):
        self.name = name
        self.path = path
        self.scores_to_win = scores_to_win
        self.player_position = player_position
