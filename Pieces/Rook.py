from Pieces.ChessPiece import ChessPiece
from Global import *


class Rook(ChessPiece):
    def __init__(self, color):
        ChessPiece.__init__(self, color)
        self.name = "Rook"
        if self.color == "white":
            self.imgurl = resource_path("assets/white_pieces/white rook.png")
        elif self.color == "black":
            self.imgurl = resource_path("assets/black_pieces/black rook.png")
        self.image = pygame.image.load(self.imgurl)

    def technically_legal(self):
        legal = {"top": [], "bottom": [], "left": [], "right": []}

        for row in range(self.row+1, 8): #bottom
            legal["bottom"].append((row, self.column))
        for row in range(self.row-1, -1, -1): #top
            legal["top"].append((row, self.column))
        for col in range(self.column+1, 8): #right
            legal["right"].append((self.row, col))
        for col in range(self.column-1, -1, -1): #left
            legal["left"].append((self.row, col))

        return legal