from Pieces.ChessPiece import ChessPiece
from Global import *


class Queen(ChessPiece):
    def __init__(self, color):
        ChessPiece.__init__(self, color)
        self.name = "Queen"
        if self.color == "white":
            self.image = pygame.image.load("assets/white_pieces/white queen.png")
        elif self.color == "black":
            self.image = pygame.image.load("assets/black_pieces/black queen.png")

    def technically_legal(self):
        legal = {"top": [], "bottom": [], "left": [], "right": [],
                 "ne": [], "se": [], "nw": [], "sw": []}

        # horizontal and vertical movements
        for row in range(self.row + 1, 8):  # bottom
            legal["bottom"].append((row, self.column))
        for row in range(self.row - 1, -1, -1):  # top
            legal["top"].append((row, self.column))
        for col in range(self.column + 1, 8):  # right
            legal["right"].append((self.row, col))
        for col in range(self.column - 1, -1, -1):  # left
            legal["left"].append((self.row, col))

        # diagonal movements
        for col in range(self.column+1, 8):  # east
            for row in range(self.row-1, -1, -1):  # north
                if row + col == self.row + self.column:
                    legal["ne"].append((row, col))
            for row in range(self.row+1, 8):  # south
                if col - row == self.column - self.row:
                    legal["se"].append((row, col))

        for col in range(self.column-1, -1, -1):  # west
            for row in range(self.row-1, -1, -1):  # north
                if col - row == self.column - self.row:
                    legal["nw"].append((row, col))
            for row in range(self.row+1, 8):  # south
                if row + col == self.row + self.column:
                    legal["sw"].append((row, col))

        return legal
