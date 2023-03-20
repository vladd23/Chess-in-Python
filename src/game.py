import pygame

from constants import *
from board import Board
# for rendering
from src.dragger import Dragger


class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # Show methods

    def show_background(self, surface):
        for row in range(rows):
            for col in range(cols):
                if (row + col) % 2 == 0:
                    color = (232, 235, 239)  # light green
                else:
                    color = (125, 135, 150)  # dark green

                rectangle = (col * squareSize, row * squareSize, squareSize, squareSize)  # start, start, size, size

                pygame.draw.rect(surface, color, rectangle)  # surface, color, rectangle

    def show_pieces(self, surface):
        for row in range(rows):
            for col in range(cols):
                # piece on the square?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except the one we are dragging
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * squareSize + squareSize // 2, row * squareSize + squareSize // 2
                        piece.textureRectangle = img.get_rect(center=img_center)
                        surface.blit(img, piece.textureRectangle)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop all valid moves
            for move in piece.moves:
                # color
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                # rect
                rectangle = (move.final.col * squareSize, move.final.row * squareSize, squareSize,
                             squareSize)  # start, start, size, size
                # blit
                pygame.draw.rect(surface, color, rectangle)  # surface, color, rectangle
