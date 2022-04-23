import pygame
from board import Board
from consts import *


class Game:
    def __init__(self, board=None):
        self.window = pygame.display.set_mode(size=(WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self._init(board)
        

    def _init(self, board):
        self.selected_piece = None
        self.board = board or Board()
        self.turn = WHITE
        self.valid_moves = dict()
        

    def reset(self):
        self._init()
        

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves()
        pygame.display.update()
        

    def change_turn(self):
        self.turn = WHITE if self.turn == BLACK else BLACK
        

    def select(self, row, col):
        """
        select a piece to move or select a destination if piece is already selected
        """
        # if selected a piece try and move it
        if self.selected_piece:
            result = self._move(row, col)
            # if the move is illegal try again and select a new piece
            if not result:
                self.selected_piece = None
                self.select(row, col)
        # select a piece
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            valid_boards = self.board.calc_valid_boards(self.selected_piece)
            self.valid_moves = self.diff(valid_boards)
            return True
        self.valid_moves = dict()
        return False
            
        
    def _move(self, row, col):
        dest = self.board.get_piece(row, col)
        if (self.selected_piece) and ((row, col) in self.valid_moves):
            self.board.move(self.selected_piece, row, col)
            eaten_pieces = self.valid_moves[(row, col)]
            self.board.remove(eaten_pieces)
            for eaten_piece in eaten_pieces:
                if eaten_piece.row == 1 and self.turn == BLACK:
                    self.selected_piece.make_queen()
                if eaten_piece.row == ROWS - 2 and self.turn == WHITE:
                    self.selected_piece.make_queen()
            self.change_turn()
            return True
        return False
    
    
    def diff(self, boards):
        valid_moves = dict()
        for other in boards:
            move = self.board.diff(other, self.turn)
            valid_moves.update(move)
        return valid_moves
    
    
    def draw_valid_moves(self):
        for row, col in self.valid_moves:
            center = (col * SQUARE_SIZE + SQUARE_SIZE / 2,
                      row * SQUARE_SIZE + SQUARE_SIZE / 2)
            radius = 10
            pygame.draw.circle(self.window, BLUE, center, radius)


    def ai_move(self, board):
        self.board = board
        self.change_turn()