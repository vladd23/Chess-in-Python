from constants import *
from square import *
from piece import *
from src.move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(cols)]
        self.last_move = None
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

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # update the console board
        # this is the position our piece is sitting at the moment
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_valid_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        """
        Calculate all the possible moves of an specific piece on a specific pos
        """

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            # from row 5 to row 3 in case of the white pieces and from r2 to r4
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # create new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        # blocked, piece in front of us
                        break
                else:
                    # not on the board
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # we can capture the piece by making a new move
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append the new move
                        piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_knight_moves = [
                (row + 2, col - 1),
                (row + 2, col + 1),
                (row + 1, col - 2),
                (row + 1, col + 2),
                (row - 1, col - 2),
                (row - 1, col + 2),
                (row - 2, col - 1),
                (row - 2, col + 1)
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

        def king_moves():
            possible_king_moves = [
                (row - 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row, col - 1),
                (row, col + 1),
                (row + 1, col - 1),
                (row + 1, col),
                (row + 1, col + 1)
            ]

            for possible_move in possible_king_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    # it s on the board
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece = piece
                        move = Move(initial, final)
                        piece.add_move(move)
                        # append new valid move to the list

        # for queen, bishop and rook
        def straightline_move(increments_list):
            for inc in increments_list:
                row_inc, col_inc = inc
                possible_move_row = row + row_inc
                possible_move_col = col + col_inc

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece = piece
                        move = Move(initial, final)

                        # we dont want the piece to jump over the team pieces
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                        # empty square = continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)
                        # enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                            # after the capture the player's turn ends
                    else: break
                    # incrementing the increments
                    possible_move_row = possible_move_row + row_inc
                    possible_move_col = possible_move_col + col_inc

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_move([
                (-1, 1),  # up right
                (-1, -1),  # up left
                (1, 1),  # down right
                (1, -1)  # down left
            ])
        elif isinstance(piece, Rook):
            straightline_move([
                (-1, 0),  # up
                (0, 1),  # right
                (0, -1),  # left
                (1, 0),  # down
            ])
        elif isinstance(piece, Queen):
            # combination between rook and bishop
            straightline_move([
                (-1, 0),  # up
                (0, 1),  # right
                (0, -1),  # left
                (1, 0),  # down
                (-1, 1),  # up right
                (-1, -1),  # up left
                (1, 1),  # down right
                (1, -1)  # down left
            ])
        elif isinstance(piece, King):
            king_moves()
