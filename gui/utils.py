from PyQt5.Qt import QImage, QMediaContent, QUrl, QPixmap, QBitmap, QFont
from PyQt5 import QtGui
import os

IMAGES_DIR = os.path.join(os.getcwd(), "src", "img")
SOUND_DIR = os.path.join(os.getcwd(), "src", "sound")
FONTS_DIR = os.path.join(os.getcwd(), "src", "fonts")


def extract_components(image_path):
    image = QImage(image_path)
    return {
        "label": image.copy(390, 230, 200, 60)
    }


class UI:
    COMMON = extract_components(os.path.join(IMAGES_DIR, "UI", "components.png"))
    LABEL = COMMON["label"]


def extract_balls(path):
    columns, rows = 4, 3
    balls = QImage(path)
    x_step, y_step = balls.width() / columns, balls.height() / rows
    return [balls.copy(x * x_step, y * y_step, x_step, y_step) for x in range(columns) for y in range(rows)]


class Images:
    FROG = QImage(os.path.join(IMAGES_DIR, "entities", "frog.png"))
    BALLS = extract_balls(os.path.join(IMAGES_DIR, "entities", "balls.png"))

    BACKGROUND = [
        QImage(os.path.join(IMAGES_DIR, "background", x)) for x in [
            "background1.jpg",
            "background2.jpg",
            "background3.jpg",
            "background4.jpg",
        ]
    ]

    SILENT_HILL = [
        QImage(os.path.join(IMAGES_DIR, "background", x)) for x in [
            "silenthill.png",
            "silenthill2.jpg",
            "silenthill3.jpg",
        ]
    ]


def extract_sound(path):
    return QMediaContent(QUrl.fromLocalFile(path))


class Sound:
    WIN = [
        extract_sound(os.path.join(SOUND_DIR, "win", x)) for x in [
            "win1.mp3",
            "win2.mp3",
            "win3.mp3"
        ]
    ]

    DEFEAT = [
        extract_sound(os.path.join(SOUND_DIR, "defeat", x)) for x in [
            "defeat1.mp3",
            "defeat2.mp3",
            "defeat3.mp3",
        ]
    ]

    SHOT = [
        extract_sound(os.path.join(SOUND_DIR, "shot", x)) for x in [
            "shot1.mp3",
            "shot2.mp3",
            "shot3.mp3",
            "shot4.mp3",
            "shot5.mp3",
        ]
    ]

    COMBO = [
        extract_sound(os.path.join(SOUND_DIR, "combo", x)) for x in [
            "combo1.mp3"
        ]
    ]

    BACKGROUND = [
        extract_sound(os.path.join(SOUND_DIR, "background", x)) for x in [
            "Rick Astley - Never Gonna Give You Up.mp3",
            "GACHI_-_-_right_version_Gachi_Remix.mp3"
        ]
    ]


class Fonts:
    DIMBO_REGULAR = os.path.join(FONTS_DIR, "Dimbo Regular.ttf")
