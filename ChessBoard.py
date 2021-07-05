from Global import *
from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from random import randint, choice


class ChessBoard:
    def __init__(self, image, size, x_a, y_a):
        self.vmurl = resource_path("assets/highlight_squares/valid green.png")
        self.valid_move = pygame.image.load(self.vmurl)    # the green box image
        self.csurl = resource_path("assets/highlight_squares/selection gold.png")
        self.currently_selected = pygame.image.load(self.csurl)    # the gold box image
        self.wurl = resource_path("assets/highlight_squares/warning red.png")
        self.warning = pygame.image.load(self.wurl)
        self.teurl = resource_path("assets/highlight_squares/technical blue.png")
        self.telegal = pygame.image.load(self.teurl)
        self.durl = resource_path("assets/highlight_squares/red square.png")
        self.danger = pygame.image.load(self.durl)
        self.selection = None   # row and column of the current selection
        self.selection_moves = {"telegal: ": [], "legal": [], "allowed": [], "danger": []}
        self.image = pygame.image.load(image)  # the background picture of the actual chess board squares
        self.image_size = size  # the side length of the square image
        self.squares = [[] for i in range(8)]
        self.moves = []  # this will be a stack where moves will be pushed and pieces "eaten" at said step
        self.x_a = x_a  # coordinates of the top left corner of the image with respect to the game window
        self.y_a = y_a
        self.white_king = (7, 4)
        self.black_king = (0, 4)

        for r in range(8):
            for c in range(8):
                if r % 2 == 0:
                    if c % 2 == 0:
                        self.squares[r].append({"color": "white", "piece": None})
                    else:
                        self.squares[r].append({"color": "black", "piece": None})
                else:
                    if c % 2 == 0:
                        self.squares[r].append({"color": "black", "piece": None})
                    else:
                        self.squares[r].append({"color": "white", "piece": None})

        for col in range(8):
            self.insert(Pawn("white"), 6, col)
            self.insert(Pawn("black"), 1, col)
        self.insert(Rook("white"), 7, 0)
        self.insert(Knight("white"), 7, 1)
        self.insert(Bishop("white"), 7, 2)
        self.insert(Queen("white"), 7, 3)
        self.insert(King("white"), 7, 4)
        self.insert(Bishop("white"), 7, 5)
        self.insert(Knight("white"), 7, 6)
        self.insert(Rook("white"), 7, 7)
        self.insert(Rook("black"), 0, 0)
        self.insert(Knight("black"), 0, 1)
        self.insert(Bishop("black"), 0, 2)
        self.insert(Queen("black"), 0, 3)
        self.insert(King("black"), 0, 4)
        self.insert(Bishop("black"), 0, 5)
        self.insert(Knight("black"), 0, 6)
        self.insert(Rook("black"), 0, 7)

    def set_board_cords(self, x_a, y_a):
        self.x_a = x_a
        self.y_a = y_a

    def get_board_cords(self):
        x = (self.x_a, self.y_a)
        return x

    def get_selection(self):
        return self.selection

    def deselect(self):
        self.selection = None

    def set_image(self, image, size):
        self.image = pygame.image.load(image)
        self.image_size = size

    def get_image(self):
        return self.image

    def get_image_size(self):
        return self.image_size

    def insert(self, piece, row, col):
        self.squares[row][col]["piece"] = piece
        self.squares[row][col]["piece"].set_pos(row, col)

    def get_piece(self, row, col):
        if (7 >= row >= 0) and (7 >= col >= 0):
            x = self.squares[row][col]["piece"]
            if x:
                return x
        else:
            raise IndexError

    def remove(self, row, col):
        if (7 >= row >= 0) and (7 >= col >= 0):
            self.squares[row][col]["piece"] = None
        else:
            raise IndexError

    def square_cords(self, row, col):
        if (7 >= row >= 0) and (7 >= col >= 0):
            x = col * (self.image_size / 8) + self.x_a
            y = row * (self.image_size / 8) + self.y_a
            z = (x, y)
            return z
        else:
            raise IndexError

    def xy_to_rowcol(self, x, y):
        x = x - self.x_a
        y = y - self.y_a
        row = floor(y/(self.image_size/8))
        col = floor(x/(self.image_size/8))
        rc = (row, col)
        return rc

    def ready_pieces(self):
        pieces = []
        z = ""
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    z = (piece.get_image(), self.square_cords(row, col))
                    pieces.append(z)
        return pieces

    def display_board(self):
        display_board(self)

    def display_pieces(self):
        display_pieces(self)

    def display(self, img, row, col):
        cords = self.square_cords(row, col)
        display(img, cords)

    def legal(self, row, col):
        piece = self.get_piece(row, col)
        legal = []
        occupied = ""
        if piece:
            technically_legal = piece.technically_legal()
            if isinstance(piece, Knight) or isinstance(piece, King):  # discrete pieces
                for r, c in technically_legal:
                    if c < 0:
                        c = 0
                    elif c > 7:
                        c = 7
                    occupied = self.get_piece(r, c)
                    if not occupied:
                        legal.append((r, c))
                    else:
                        if piece.get_color() != occupied.get_color():
                            legal.append((r, c))

            elif isinstance(piece, Pawn):
                for row, col in technically_legal["side"]:  # discrete piece of Pawn
                    occupied = self.get_piece(row, col)
                    if occupied:
                        if occupied.get_color() != piece.get_color():
                            legal.append((row, col))

                for row, col in technically_legal["front"]:  # continuous part of Pawn
                    occupied = self.get_piece(row, col)
                    if not occupied:
                        legal.append((row, col))
                    else:
                        break

            elif isinstance(piece, Rook) or isinstance(piece, Bishop) or isinstance(piece, Queen):
                for direction, list_value in technically_legal.items():  # continuous pieces
                    for row, col in list_value:
                        occupied = self.get_piece(row, col)
                        if not occupied:
                            legal.append((row, col))
                        elif occupied:
                            if piece.get_color() != occupied.get_color():
                                legal.append((row, col))
                            else:
                                pass
                            break

        return legal

    def show_technically_legal(self, row, col):
        piece = self.get_piece(row, col)
        if piece:
            cords = self.square_cords(row, col)
            display(self.currently_selected, cords)
            technically_legal = piece.technically_legal()
            if isinstance(piece, Pawn) or isinstance(piece, Rook) or \
                    isinstance(piece, Queen) or isinstance(piece, Bishop):
                for key, list_value in technically_legal.items():
                    for t in list_value:
                        display(self.telegal, self.square_cords(*t))
            elif isinstance(piece, Knight) or isinstance(piece, King):
                for t in technically_legal:
                    display(self.telegal, self.square_cords(*t))

    def show_legal(self, row, col):
        piece = self.get_piece(row, col)
        if piece:
            cords = self.square_cords(row, col)
            display(self.currently_selected, cords)
            legal = self.legal(row, col)
            for row, col in legal:
                cords = self.square_cords(row, col)
                display(self.valid_move, cords)

    def track_king(self, piece):
        if isinstance(piece, King):
            if piece.get_color() == "white":
                self.white_king = piece.get_pos()
            else:
                self.black_king = piece.get_pos()

    def promote_pawn(self, piece):
        if isinstance(piece, Pawn):
            if piece.get_color() == "white" and piece.get_pos()[0] == 0:
                self.insert(Queen("white"), *piece.get_pos())
            elif piece.get_color() == "black" and piece.get_pos()[0] == 7:
                self.insert(Queen("black"), *piece.get_pos())
            return True
        return False

    def move1(self, old, new):
        piece = self.get_piece(*old)
        if piece:
            self.moves.append([old, new, self.get_piece(*new), False])
            self.insert(piece, *new)
            self.track_king(piece)
            self.remove(*old)

    def allowed(self, square):
        moves = {"allowed": [], "danger": []}
        piece = self.get_piece(*square)
        if piece:
            legal = self.legal(*square)
            for t in legal:
                self.move1(square, t)
                if self.check_threat(piece.get_color()):
                    moves["danger"].append(t)
                else:
                    moves["allowed"].append(t)
                self.undo()
                self.selection = square
            return moves

    def show_moves(self, row, col):
        piece = self.get_piece(row, col)
        if piece:
            cords = self.square_cords(row, col)
            display(self.currently_selected, cords)
            moves = self.allowed((row, col))
            allowed = moves["allowed"]
            danger = moves["danger"]
            for row, col in allowed:
                cords = self.square_cords(row, col)
                display(self.valid_move, cords)
            for row, col in danger:
                cords = self.square_cords(row, col)
                display(self.danger, cords)

    def true_move(self, turn, new):
        if self.selection:  # if I'm already selecting something
            if self.selection == new:  # deselect if I select same piece again
                self.deselect()
                return False
            piece = self.get_piece(*self.selection)
            if new in self.allowed(self.selection)["allowed"]:  # In the case of a valid move command:
                self.moves.append([piece.get_pos(), new, self.get_piece(*new), False])  # needs to be copy else passed by ref
                self.insert(piece, *new)
                self.track_king(piece)
                if self.promote_pawn(piece):
                    self.moves[len(self.moves)-1][3] = True
                self.remove(*self.selection)
                self.deselect()
                return True
            else:
                existing = self.get_piece(*new)
                if existing:
                    if existing.get_color() == turn:
                        self.selection = new
                        return False

        else:  # if I'm not selecting anything right now
            if self.get_piece(*new):
                if self.get_piece(*new).get_color() == turn:
                    self.selection = new
                    return False

    def check_threat(self, color):
        checked = False
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    if piece.get_color() != color:
                        pos_rc = piece.get_pos()
                        pos_xy = self.square_cords(*pos_rc)
                        if color == "white":
                            if self.white_king in self.legal(*pos_rc):  # needs to be in allowed
                                display(self.warning, pos_xy)
                                checked = True
                        else:
                            if self.black_king in self.legal(*pos_rc):
                                display(self.warning, pos_xy)
                                checked = True
        return checked

    def undo(self):
        self.selection = None
        try:
            cords = self.moves.pop()
            old = cords[0]
            new = cords[1]
            eaten = cords[2]
            promoted = cords[3]
            piece = self.get_piece(*new)
            if not promoted:
                self.insert(piece, *old)
            else:
                self.insert(Pawn(piece.get_color()), *old)
            self.track_king(piece)
            self.remove(*new)
            if eaten:
                self.insert(eaten, *new)
            return True
        except IndexError:
            return False

    def checkmate(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    if piece.get_color() == color:
                        piece_allowed = self.allowed(piece.get_pos())["allowed"]
                        if len(piece_allowed) != 0:
                            self.selection = None
                            return False
        return True

    def selected_info(self):
        x = self.selection
        if x:
            print("currently selected: ", x)
            print("confirmation: ", self.get_piece(*x))
            print("technically legal moves: ", self.get_piece(*x).technically_legal())
            print("legal moves: ", self.legal(*x))
            print("allowed moves: ", self.allowed(x)["allowed"])
            print("danger moves: ", self.allowed(x)["danger"])
            print(f"white king is at {self.white_king}")
            print(f"black king is at {self.black_king}")
            print("SELECTED ANOTHER PIECE\n\n")
        else:
            print("nothing is selected")

    def random_move(self, color):
        while True:
            row_old = randint(0, 7)
            col_old = randint(0, 7)
            piece_to_be_moved = self.get_piece(row_old, col_old)
            if piece_to_be_moved:
                if piece_to_be_moved.get_color() == color:
                    allowed = self.allowed((row_old, col_old))["allowed"]
                    if len(allowed) > 0:
                        new = choice(allowed)
                        self.selection = (row_old, col_old)
                        print(piece_to_be_moved.get_color(), piece_to_be_moved.get_name(), "moved from: ",
                              (row_old, col_old), " to: ", new, " by the computer")
                        self.selected_info()
                        self.true_move(color, new)
                        break



