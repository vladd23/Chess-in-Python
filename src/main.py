import pygame
import sys

from constants import *
from game import Game
from src.move import Move
from src.square import Square


class Main:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('MyChess')
        self.game = Game()

    def main_loop(self):

        game = self.game
        screen = self.screen
        dragger = game.dragger
        board = game.board

        while True:

            game.show_background(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # for click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // squareSize
                    clicked_col = dragger.mouseX // squareSize

                    # if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # show methods
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                # for the mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                # for click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // squareSize
                        released_col = dragger.mouseX // squareSize

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # if valid move
                        if board.valid_move(dragger.piece, move):
                            # move the piece
                            board.move(dragger.piece, move)
                            # show methods
                            game.show_background(screen)
                            game.show_pieces(screen)

                    dragger.undrag_piece()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.main_loop()
