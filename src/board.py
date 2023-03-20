from constants import *
from square import *
from piece import *
from src.move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(cols)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):

        for row in range(rows):
            for col in range(cols):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):

        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(cols):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

    def calc_moves(self, piece, row, col):
        """
        Calculate all the possible moves of an specific piece on a specific pos
        """

        def knight_moves():
            # 8 possible moves
            possible_knight_moves = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row - 1, col - 2),
                (row - 1, col + 2),
                (row + 1, col - 2),
                (row + 1, col + 2),
                (row + 2, col - 1),
                (row + 2, col + 1)
            ]

            for possible_move in possible_knight_moves:
                possible_move_row, possible_move_col = possible_move
                # if the square is on the table or it is existing
                if Square.in_range(possible_move_row, possible_move_col):
                    # it s on the bord
                    # if the square is empty or it has a rival piece on it
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece = piece
                        move = Move(initial, final)
                        piece.add_move(move)
                        # append new valid move to the list

        if isinstance(piece, Pawn):
            pass
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            pass
        elif isinstance(piece, Rook):
            pass
        elif isinstance(piece, Queen):
            pass
        elif isinstance(piece, King):
            pass