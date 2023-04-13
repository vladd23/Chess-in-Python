import os


class Piece:
    def __init__(self, name, color, value, texture=None, textureRectangle=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1  # for ai to know which is white and which is black
        self.value = value_sign * value
        self.set_texture()
        self.textureRectangle = textureRectangle
        self.moves = []
        self.moved = False

    def __eq__(self, other):
        return self.name == other.name

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png'
            # f'assets/images/v3/{self.color}_{self.name}.png'

        )

    def add_move(self, move):
        self.moves.append(move)

    def clear_valid_moves(self):
        self.moves = []


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)


class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)


class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)


class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)


class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)


class King(Piece):

    def __init__(self, color):
        super().__init__('king', color, 10000.0)
