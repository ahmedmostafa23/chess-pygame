from Pieces.ChessPiece import ChessPiece
from Global import *


class Pawn(ChessPiece):
    def __init__(self, color):
        ChessPiece.__init__(self, color)
        self.name = "Pawn"
        if self.color == "white":
            self.imgurl = resource_path("assets/white_pieces/white pawn.png")
        elif self.color == "black":
            self.imgurl = resource_path("assets/black_pieces/black pawn.png")
        self.image = pygame.image.load(self.imgurl)

    def technically_legal(self):
        legal = {"front": [], "side": []}
        
        if self.color == "white":
            if self.row-1 >= 0 and self.column-1 >= 0:  # side left
                legal["side"].append((self.row-1, self.column-1))
            if self.row-1 >= 0:  # front 1
                legal["front"].append((self.row-1, self.column))
            if self.row-1 >= 0 and self.column+1 <= 7: # side right
                legal["side"].append((self.row-1, self.column+1))
            if self.row == 6 and self.row-2 >= 0:  # front 2
                legal["front"].append((self.row-2, self.column))

        elif self.color == "black":
            if self.row+1 <= 7 and self.column-1 >= 0:  # side left
                legal["side"].append((self.row+1, self.column-1))
            if self.row+1 <= 7:  # front 1
                legal["front"].append((self.row+1, self.column))
            if self.row+1 <= 7 and self.column+1 <= 7:  # side right
                legal["side"].append((self.row+1, self.column+1))
            if self.row == 1 and self.row+2 <= 7:  # front 2
                legal["front"].append((self.row+2, self.column))

        return legal