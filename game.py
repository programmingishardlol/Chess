import pygame
from constant import *
from board import Board
from dragger import Dragger
from configuration import Configuration
from square import Square

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = "white"
        self.hovered_sqr = None
        self.configuration = Configuration()

    def show_background(self, surface):
        theme = self.configuration.theme

        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row+col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col*SQUARESIZE, row*SQUARESIZE, SQUARESIZE, SQUARESIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    label = self.configuration.font.render(str(ROWS-row), 1, color)
                    label_pos = (5, 5 + row*SQUARESIZE)
                    surface.blit(label, label_pos)
                # col coordinates
                if row == 7:
                    color = theme.bg.dark if (row+col) % 2 == 0 else theme.bg.light
                    label = self.configuration.font.render(Square.get_alphacol(col), 1, color)
                    label_pos = (col * SQUARESIZE + SQUARESIZE - 20, HEIGHT-20)
                    surface.blit(label, label_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # is there a piece on that square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # blit all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture()
                        img = pygame.image.load(piece.texture)
                        img_center = col*SQUARESIZE + SQUARESIZE//2, row*SQUARESIZE + SQUARESIZE//2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.configuration.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col*SQUARESIZE, move.final.row*SQUARESIZE, SQUARESIZE, SQUARESIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.configuration.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col*SQUARESIZE, pos.row*SQUARESIZE, SQUARESIZE, SQUARESIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col*SQUARESIZE, self.hovered_sqr.row*SQUARESIZE, SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(surface, color, rect, width=3)


    def next_turn(self):
        self.next_player = "white" if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.configuration.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.configuration.capture_sound.play()
        else:
            self.configuration.move_sound.play()

    def reset(self):
        self.__init__()
