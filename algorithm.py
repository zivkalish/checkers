from copy import deepcopy
import pygame
from consts import BLACK, WHITE

def minimax(board, depth, max_player, game):
	if depth == 0 or board.winner:
		return board.evaluate(), board
	if max_player:
		max_eval = float('-inf')
		best_board = None
		for simulated_board in get_all_boards(board, WHITE, game):
			evaluation = minimax(simulated_board, depth-1, False, game)[0]
			max_eval = max(max_eval, evaluation)
			if max_eval == evaluation:
				best_board = simulated_board
		return max_eval, best_board
	else:
		min_eval = float('inf')
		best_board = None
		for simulated_board in get_all_boards(board, BLACK, game):
			evaluation = minimax(simulated_board, depth-1, True, game)[0]
			min_eval = min(min_eval, evaluation)
			if min_eval == evaluation:
				best_board = simulated_board
		return min_eval, best_board


def get_all_boards(board, color, game):
	all_valid_boards = []
	for piece in board.get_all_pieces(color):
		valid_boards = board.calc_valid_boards(piece)
		all_valid_boards += valid_boards
	return all_valid_boards