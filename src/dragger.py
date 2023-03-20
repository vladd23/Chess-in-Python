import pygame
from constants import *


class Dragger:
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.piece = None
        self.dragging = False

    # blit methods

    def update_mouse(self, position):
        self.mouseX, self.mouseY = position  # position = (X, Y)

    def save_initial(self, position):
        self.initial_row = position[1] // squareSize
        self.initial_col = position[0] // squareSize

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    def update_blit(self, surface):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        # image
        img = pygame.image.load(texture)

        # rectangle
        img_center = (self.mouseX, self.mouseY)
        self.piece.textureRectangle = img.get_rect(center=img_center)

        # blit
        surface.blit(img, self.piece.textureRectangle)