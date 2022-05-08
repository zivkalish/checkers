import pygame
from consts import *

class Piece:
    PADDING = 10
    def __init__(self, color, row, col):
        self.color = color
        self.direction = 1 if self.color == WHITE else -1
        self.queen = False
        self.row = row
        self.col = col
        self.calc_pos()        
        
    def make_queen(self):
        self.queen = True
        
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
        if (self.row == 0) and self.color == BLACK:
            self.make_queen()
        if (self.row == ROWS - 1) and self.color == WHITE:
            self.make_queen()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE / 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE / 2
        
    def draw(self, window):
        if not self.queen:
            radius = SQUARE_SIZE / 2 - self.PADDING
            pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        else:
            if self.color == BLACK:
                queen = BLACK_QUEEN
            else:
                queen = WHITE_QUEEN
            window.blit(queen, (self.x - queen.get_width() / 2, self.y - queen.get_height() / 2))
            
    def __repr__(self):
        if self.queen:
            return "ww" if self.color == WHITE else "bb"
        return "w" if self.color == WHITE else "b"
    
    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return True if self.color == other.color and self.queen == other.queen else False
