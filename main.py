import pygame
from consts import *
from game import Game
from algorithm import minimax

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row, col = int(y // SQUARE_SIZE), int(x // SQUARE_SIZE)
    return row, col


def main(debug=True):
    run = True
    game = Game()
    clock = pygame.time.Clock()
    computer_color = BLACK
    max_player = True if computer_color == WHITE else False
    while run:
        clock.tick(FPS)
        if game.turn == computer_color:
            value, new_board = minimax(game.board, 4, game.turn)
            print(value)
            game.ai_move(new_board)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    game.undo()
                if event.key == pygame.K_d and debug:
                    import ipdb
                    ipdb.set_trace()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                game.select(row, col)

        game.update()
    pygame.quit()


if __name__ == '__main__':
	main()