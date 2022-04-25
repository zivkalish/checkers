import pygame
from numpy import array
from consts import *
from copy import deepcopy
from piece import Piece


class Board:
    def __init__(self):
        self.set_starting_board()
        self.moving_piece = None
        self.last_moven_piece = None


    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        for row, other_row in zip(self.board, other.board):
            for piece, other_piece in zip(row, other_row):
                if not piece == other_piece:
                    return False
        return True
    

    def __lt__(self, other):
        return self.count_pieces() < other.count_pieces()
    

    def __iter__(self):
        return iter(self.board)


    def __str__(self):
        return str(array(self.board))


    def clone(self):
        cloned_board = deepcopy(self)
        for row_index, row in enumerate(self):
            for col_index, piece in enumerate(row):
                cloned_board.board[row_index][col_index] = deepcopy(piece)
        return cloned_board
    

    def set_starting_board(self):
        board = []
        for row_index in range(ROWS):
            row = []
            for col_index in range(COLS):
                if col_index % 2 == (row_index + 1) % 2:
                    if row_index < STARTING_PIECES_ROWS:
                        piece = Piece(WHITE, row_index, col_index)
                    elif row_index >= ROWS - STARTING_PIECES_ROWS:
                        piece = Piece(BLACK, row_index, col_index)
                    else:
                        piece = 0
                else:
                    piece = 0
                row.append(piece)
            board.append(row)            
        self.board = board
       

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        self.last_moven_piece = piece
        
        
    def get_piece(self, row, col):
        return self.board[row][col]
    

    def draw_squares(self, window):
        window.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, LIGHT_BROWN,
                                (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if isinstance(piece, Piece):
                    piece.draw(window)
    

    def empty_square_filter(self, positions):
        return [(row, col) for (row, col) in self.bound_filter(positions) if self.get_piece(row, col) == 0]
    
    
    def bound_filter(self, positions):
        return [(row, col) for (row, col) in positions if (0 <= col < COLS) and (0 <= row < ROWS)]
    
    
    def get_adjacent_squares(self, piece):
        adjacent_squares = []
        if piece.queen:
            adjacent_squares += [(piece.row - 1, piece.col - 1),
                                 (piece.row + 1, piece.col + 1),
                                 (piece.row + 1, piece.col - 1),
                                 (piece.row - 1, piece.col + 1)]
        else:
            adjacent_squares += [(piece.row + piece.direction, piece.col + 1),
                                 (piece.row + piece.direction, piece.col - 1)]
        return self.bound_filter(adjacent_squares)
    
    
    def get_possible_jumps(self, piece):
        """
        return all positions two diagonal squares across the given piece
        if the adjacent diagonal square is occupied by an opposite color piece
        :return type: Dict[Tuple[int, int]:List[Piece]]
        """
        adjacent_squares = self.get_adjacent_squares(piece)
        possible_jumps = dict()
        destinations = list()
        for row, col in adjacent_squares:
            adjacent_piece = self.get_piece(row, col)
            if isinstance(adjacent_piece, Piece):
                if adjacent_piece.color != piece.color:
                    dest = (piece.row + 2 * (row - piece.row),
                            piece.col + 2 * (col - piece.col))
                    possible_jumps[dest] = [adjacent_piece]
                    destinations.append(dest)
        legal_destinations = self.empty_square_filter(destinations)
        return {key:value for key, value in possible_jumps.items() if key in legal_destinations}
    

    def get_one_jump_boards(self, piece):
        """
        return a list of all the possible boards where the given piece jumped once.
        :return type: List[Board]
        """
        boards = []
        for dest, eaten_pieces in self.get_possible_jumps(piece).items():
            temp_board = self.move2board(piece, dest, eaten_pieces)
            boards.append(temp_board)
        return boards
    
    
    def get_none_jumps_boards(self, piece):
        moves = {dest:[] for dest in self.empty_square_filter(self.get_adjacent_squares(piece))}
        return [self.move2board(piece, dest, eaten_pieces) for (dest, eaten_pieces) in moves.items()]
    

    def move2board(self, piece, dest, eaten_pieces):
        """
        :param1: Piece
        :param2: Tuple[int, int]
        :param3: List[Pieces]
        :return: Board
        """
        new_board = deepcopy(self)
        new_piece = new_board.get_piece(piece.row, piece.col)
        new_board.move(new_piece, *dest)
        new_board.remove(eaten_pieces)
        new_board.moving_piece = new_piece
        return new_board
        

    def remove(self, pieces):
        for piece in pieces:
            if piece == 0:
                continue
            self.board[piece.row][piece.col] = 0
            

    def calc_valid_boards(self, piece):
        """
        return all the possible moves of a given piece.
        """
        tasks = self.get_one_jump_boards(piece)
        valid_boards = []
        for board in tasks:
            if board in valid_boards:
                continue
            tasks += board.get_one_jump_boards(board.moving_piece)
            valid_boards.append(board)
        valid_boards += self.get_none_jumps_boards(piece)
        return valid_boards
    

    @staticmethod
    def filter_boards(boards):
        """
        return the boards with the least pieces
        """
        min_value = min(boards, key=Board.count_pieces).count_pieces()
        return [board for board in boards if board.count_pieces() == min_value]
    

    def count_pieces(self, color=None):
        counter = 0
        for row in self:
            for piece in row:
                if not isinstance(piece, Piece):
                    continue
                if (piece.color == color) or (color == None):
                    counter += 1
        return counter

    def count_queens(self, color):
        counter = 0
        for row in self:
            for piece in row:
                if not isinstance(piece, Piece):
                    continue
                if not piece.queen:
                    continue
                if piece.color == color:
                    counter += 1
        return counter
    
    
    def diff(self, other, turn):
        eaten_pieces = []
        for row, other_row in zip(self, other):
            for piece, other_piece in zip(row, other_row):
                if (other_piece == 0) and isinstance(piece, Piece) and piece.color != turn:
                    eaten_pieces.append(piece)
        dest = other.last_moven_piece.row, other.last_moven_piece.col
        return {dest:eaten_pieces}


    def get_all_pieces(self, color):
        pieces = []
        for row in self:
            for piece in row:
                if not isinstance(piece, Piece):
                    continue
                if piece.color == color:
                    pieces.append(piece)
        return pieces


    def evaluate(self, turn):
        if self.winner(turn) == WHITE:
            return float("inf")
        elif self.winner == BLACK:
            return float("-inf")
        return self.count_pieces(WHITE) - self.count_pieces(BLACK) + self.count_queens(WHITE) * 0.5 - self.count_queens(BLACK) * 0.5


    def no_move_detection(self, color):
        for row in self:
            for piece in row:
                if not isinstance(piece, Piece):
                    continue
                if not piece.color == color:
                    continue
                jumps = self.get_one_jump_boards(piece)
                regular_moves = self.get_none_jumps_boards(piece)
                if jumps or regular_moves:
                    return False
        return True


    def winner(self, turn):
        if self.no_move_detection(turn):
            return WHITE if turn == BLACK else BLACK
        return None