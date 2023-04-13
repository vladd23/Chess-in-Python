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
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

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

                        # check if valid piece color
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # for the mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // squareSize
                    motion_col = event.pos[0] // squareSize

                    sq = Square(motion_row, motion_col)
                    if sq.in_range(motion_row, motion_col):
                        game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
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
                            game.show_moves(screen)
                            game.show_pieces(screen)

                            #next turn
                            game.next_turn()

                    dragger.undrag_piece()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # restart game function
                        game.reset()
                        game = self.game
                        dragger = game.dragger
                        board = game.board

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.main_loop()
