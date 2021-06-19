from Pieces.ChessPiece import ChessPiece
from Global import *


class King(ChessPiece):
    def __init__(self, color):
        ChessPiece.__init__(self, color)
        self.name = "King"
        if self.color == "white":
            self.imgurl = resource_path("assets/white_pieces/white king.png")
        elif self.color == "black":
            self.imgurl = resource_path("assets/black_pieces/black king.png")
        self.image = pygame.image.load(self.imgurl)

    def technically_legal(self):
        legals = [(self.row-1, self.column+1), (self.row, self.column+1),
                  (self.row+1, self.column+1), (self.row+1, self.column),
                  (self.row+1, self.column-1), (self.row, self.column-1),
                  (self.row-1, self.column-1), (self.row-1, self.column)]
        legal = []
        for x, y in legals:
            if (7 >= x >= 0) and (7 >= x >= 0):
                legal.append((x, y))
        return legal
