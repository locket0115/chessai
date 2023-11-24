import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from piece import *
from ai import AI

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        t = 0

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            # game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)
            
            if t == 2:
                if board.get_possible_moves('white', True) == []:
                    if board.in_check(King('white'), None):
                        print('Black Wins by Checkmate!')
                    else:
                        print('Stalemate')
                    game.next_player = None
                elif board.get_possible_moves('black', True) == []:
                    if board.in_check(King('black'), None):
                        print('White Wins by Checkmate!')
                    else:
                        print('Stalemate')
                    game.next_player = None

            if game.next_player == 'black' and t > 5:
                p, move = AI.get_best_move(board, 'black')
                board.move(p, move)
                game.next_turn()

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if Square.in_range(clicked_row, clicked_col):
                        # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            # vaild piece (color) ?
                            if piece.color == game.next_player and game.next_player == 'white':
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    

                    if Square.in_range(motion_row, motion_col):
                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            # game.show_hover(screen)
                            dragger.update_blit(screen)

                #click release
                elif event.type == pygame.MOUSEBUTTONUP:
                                        
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        if Square.in_range(released_row, released_col):
                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # vaild move ?
                            if board.vaild_move(dragger.piece, move):
                                # normal capture
                                captured = board.squares[released_row][released_col].has_piece()
                                en_passanted = isinstance(dragger.piece, Pawn) and (initial.col != released_col)
                                board.move(dragger.piece, move)

                                board.set_true_en_passant(dragger.piece)

                                # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()
                                t = 0

                        # clear moves
                        dragger.piece.clear_moves()

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:

                    # changing theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # reset game
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                #quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            t = t+1
            pygame.display.update()


main = Main()
main.mainloop()