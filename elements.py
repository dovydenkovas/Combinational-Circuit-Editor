from enum import Enum
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage


class ElementTypes(Enum):
    OR = 0
    AND = 1
    NOT = 2
    INPUT = 3


class ElementState:
    DEFAULT = 0
    TRIGGERED = 1
    CHOOSING = 2


class Element:
    _textures = {
        ElementTypes.OR: [QImage("images/or.bmp"),
                          QImage("images/or_triggered.bmp"),
                          QImage("images/or_choosen.bmp")],
        ElementTypes.AND: [QImage("images/and.bmp"),
                           QImage("images/and_triggered.bmp"),
                           QImage("images/and_choosen.bmp")],
        ElementTypes.NOT: [QImage("images/not.bmp"),
                           QImage("images/not_triggered.bmp"),
                           QImage("images/not_choosen.bmp")],
        ElementTypes.INPUT: [QImage("images/input.png"),
                             QImage("images/input_triggered.png"),
                             QImage("images/input_choosen.png")]
        }

    def __init__(self, element_type, x, y):
        self.x = x
        self.y = y
        self.state = ElementState.DEFAULT
        if element_type == ElementTypes.INPUT:
            self.width = 30
            self.height = 30
        else:
            self.width = 80
            self.height = 80

        self.element_type = element_type

    def draw(self, qpainter):
        """ Draw Element. """
        qpainter.drawImage(QRect(self.x, self.y, self.width, self.height), Element._textures[self.element_type][self.state])


