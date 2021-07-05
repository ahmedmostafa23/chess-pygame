from Pieces.ChessPiece import ChessPiece
from Global import *


class Knight(ChessPiece):
    def __init__(self, color):
        ChessPiece.__init__(self, color)
        self.name = "Knight"
        if self.color == "white":
            self.imgurl = resource_path("assets/white_pieces/white knight.png")
        elif self.color == "black":
            self.imgurl = resource_path("assets/black_pieces/black knight.png")
        self.image = pygame.image.load(self.imgurl)

    def technically_legal(self):
        legals = [(self.row-2, self.column+1), (self.row-1, self.column+2),
                 (self.row+1, self.column+2), (self.row+2, self.column+1),
                 (self.row+2, self.column-1), (self.row+1, self.column-2),
                 (self.row-1, self.column-2), (self.row-2, self.column-1)]
        legal = []
        for row, col in legals:
            if (7 >= row >= 0) and (7 >= col >= 0):
                legal.append((row, col))
        return legal

