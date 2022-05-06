from consts import BLACK, WHITE
COUNTER = 0

def minimax(board, depth, turn, opponent_best_score=None):
	global COUNTER
	COUNTER += 1
	if depth == 0 or board.winner(turn):
		return board.evaluate(turn), board
	if turn == WHITE:
		best_score = float("-inf")
		opponent_best_score = opponent_best_score or float("inf")
		next_turn = BLACK
		optimizer_func = max
		should_prune = lambda score, opponent_best_explored_score: score >= opponent_best_explored_score
	else:
		best_score = float("inf")
		opponent_best_score = opponent_best_score or float("-inf")
		next_turn = WHITE
		optimizer_func = min
		should_prune = lambda score, opponent_best_explored_score: score <= opponent_best_explored_score
	best_board = None
	for simulated_board in get_all_boards(board, turn):
		score = minimax(simulated_board, depth-1, next_turn, best_score)[0]
		best_score = optimizer_func(score, best_score)
		if best_score == score:
			best_board = simulated_board
		if should_prune(best_score, opponent_best_score):
		#	print(f"turn is: {turn}\ndepth is: {depth}\n simulated_board score is {best_score}\nopponent best score is: {opponent_best_score}")
			break
	return best_score, best_board


def get_all_boards(board, color):
	all_valid_boards = []
	for piece in board.get_all_pieces(color):
		valid_boards = board.calc_valid_boards(piece)
		all_valid_boards += valid_boards
	return all_valid_boards

def init_counter():
	global COUNTER
	value = COUNTER
	COUNTER = 0
	return value