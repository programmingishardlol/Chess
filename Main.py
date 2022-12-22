import pygame
import sys
# from constant import all
from constant import *
from game import Game
from square import *
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        dragger = self.game.dragger
        board = self.game.board

        while True:
            self.game.show_background(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
            self.game.show_hover(self.screen)
            
            if dragger.dragging:
                dragger.update_blit(self.screen)

            for event in pygame.event.get():

                # dragger
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQUARESIZE
                    clicked_col = dragger.mouseX // SQUARESIZE
                    # if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # if it is a valid color piece
                        if piece.color == self.game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            self.game.show_background(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_moves(self.screen)
                            self.game.show_pieces(self.screen)

                # moving a piece
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARESIZE
                    motion_col = event.pos[0] // SQUARESIZE
                    self.game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        self.game.show_background(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.show_hover(self.screen)
                        dragger.update_blit(self.screen)

                # put down a piece
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQUARESIZE
                        released_col = dragger.mouseX // SQUARESIZE
                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)
                            board.set_true_en_passant(dragger.piece)
                            # play sound 
                            self.game.play_sound(captured)
                            # show method
                            self.game.show_background(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_pieces(self.screen)
                            # next player
                            self.game.next_turn()

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.change_theme()
                    
                    # restart
                    if event.key == pygame.K_r:
                        self.game.reset()
                        dragger = self.game.dragger
                        board = self.game.board

                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()
