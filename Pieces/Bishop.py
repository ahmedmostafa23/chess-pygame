from Pieces.ChessPiece import ChessPiece
from Global import *


class Bishop(ChessPiece):
    def __init__(self, color):
        ChessPiece.__init__(self, color)
        self.name = "Bishop"
        if self.color == "white":
            self.imgurl = resource_path("assets/white_pieces/white bishop.png")
        elif self.color == "black":
            self.imgurl = resource_path("assets/black_pieces/black bishop.png")
        self.image = pygame.image.load(self.imgurl)

    def technically_legal(self):
        legal = {"ne": [], "se": [], "nw": [], "sw": []}

        for col in range(self.column+1, 8): #east
            for row in range(self.row-1, -1, -1): #north
                if row + col == self.row + self.column:
                    legal["ne"].append((row, col))
            for row in range(self.row+1, 8): #south
                if col - row == self.column - self.row:
                    legal["se"].append((row, col))

        for col in range(self.column-1, -1, -1): #west
            for row in range(self.row-1, -1, -1): #north
                if col - row == self.column - self.row:
                    legal["nw"].append((row, col))
            for row in range(self.row+1, 8): #south
                if row + col == self.row + self.column:
                    legal["sw"].append((row, col))

        return legal