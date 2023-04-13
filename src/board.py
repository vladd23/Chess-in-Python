import copy

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

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temporary_piece = copy.deepcopy(piece)
        temporary_board = copy.deepcopy(self)

        temporary_board.move(temporary_piece, move, testing=True)
        for row in range(rows):
            for col in range(cols):
                if temporary_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temporary_board.squares[row][col].piece
                    temporary_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        # update the console board
        # this is the position our piece is sitting at the moment
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # king castling

        if isinstance(piece, King):
                if self.castling(initial, final) and not testing:
                    diff = final.col - initial.col
                    rook = piece.left_rook if (diff < 0) else piece.right_rook
                    self.move(rook, rook.moves[-1])  # the last move saved in the valid moves for castling for king

        # pawn promotion

        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_valid_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col, bool=True):  # to prevent infinite loop
        """
        Calculate all the possible moves of an specific piece on a specific pos
        """

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            # from row 5 to row 3 in case of the white pieces and from r2 to r4
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # create new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)

                        else:
                            piece.add_move(move)
                    else:
                        # blocked, piece in front of us
                        break
                else:
                    # not on the board
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # we can capture the piece by making a new move
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        final = Square(possible_move_row, possible_move_col, final_piece)
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        final = Square(possible_move_row, possible_move_col, final_piece)  # piece = piece
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)

                        else:
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
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else: break

                        else:
                            # append new valid move to the list
                            piece.add_move(move)

            # castling moves
            if not piece.moved:

                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        # if between the rook and king there are no pieces
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # it works only for king piece
                                # add left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                rook_move = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                king_move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, king_move) and not self.in_check(left_rook, rook_move):
                                        # append new move to rook
                                        left_rook.add_move(rook_move)
                                        # append new move to king
                                        piece.add_move(king_move)

                                else:
                                    # append new move to rook
                                    left_rook.add_move(rook_move)
                                    # append new move to king
                                    piece.add_move(king_move)
                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        # if between the rook and king there are no pieces
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # it works only for king piece
                                # add left rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                rook_move = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                king_move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, king_move) and not self.in_check(right_rook, rook_move):
                                        # append new move to rook
                                        right_rook.add_move(rook_move)
                                        # append new move to king
                                        piece.add_move(king_move)

                                else:
                                    # append new move to rook
                                    right_rook.add_move(rook_move)
                                    # append new move to king
                                    piece.add_move(king_move)

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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece

                        final = Square(possible_move_row, possible_move_col, final_piece)  # piece = piece
                        move = Move(initial, final)

                        # we dont want the piece to jump over the team pieces
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                        # empty square = continue looping
                        elif self.squares[possible_move_row][possible_move_col].is_empty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                                else:
                                    break
                            else:
                                piece.add_move(move)

                        # enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                                else:
                                    break
                            else:
                                piece.add_move(move)
                                break
                            # after the capture the player's turn ends
                    else:
                        break
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

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
