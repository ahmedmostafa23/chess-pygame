from Global import *
from abc import ABC, abstractmethod


class ChessPiece(ABC):
    def __init__(self, color):
        self.name = ""
        self.imgurl = resource_path("assets/white_pieces/q.png")
        self.image = pygame.image.load(self.imgurl)
        self.row = 0
        self.column = 0
        if color == "black" or "white":
            self.color = color
        else:
            raise ValueError

    def __str__(self):
        return f'This is a {self.color} {self.name} currently at row: {self.row} and column: {self.column}'

    def __repr__(self):
        return f'{self.color} {self.name}'

    def set_pos(self, row=None, col=None):
        if row or row == 0:
            if 7 >= row >= 0:
                self.row = row
            else:
                raise IndexError
        if col or col == 0:
            if 7 >= col >= 0:
                self.column = col
            else:
                raise IndexError

    def get_pos(self):
        pos = (self.row, self.column)
        return pos

    def set_image(self, image):
        self.image = pygame.image.load(image)

    def get_image(self):
        return self.image

    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    @abstractmethod
    def technically_legal(self):
        pass
