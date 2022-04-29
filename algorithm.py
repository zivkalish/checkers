from copy import deepcopy
import pygame
from consts import BLACK, WHITE

def minimax(board, depth, max_player, game):
	if depth == 0 or board.winner(game.turn):
		return board.evaluate(game.turn), board
	if max_player:
		color = WHITE
		max_eval = float("-inf")
		max_func = max
	else:
		color = BLACK
		max_eval = float("inf")
		max_func = min
	best_board = None
	for simulated_board in get_all_boards(board, color):
		evaluation = minimax(simulated_board, depth-1, not(max_player), game)[0]
		max_eval = max_func(max_eval, evaluation)
		if max_eval == evaluation:
			best_board = simulated_board
	return max_eval, best_board


def get_all_boards(board, color):
	all_valid_boards = []
	for piece in board.get_all_pieces(color):
		valid_boards = board.calc_valid_boards(piece)
		all_valid_boards += valid_boards
	return all_valid_boards
