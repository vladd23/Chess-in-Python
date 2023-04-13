
class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def has_piece(self):
        return self.piece is not None

    @staticmethod
    def in_range(*args):
        for argument in args:
            if argument < 0 or argument > 7:
                return False

        return True

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def is_empty(self):
        return not self.has_piece()

    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_enemy_piece(color)
