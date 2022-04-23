import pygame

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH / COLS
STARTING_PIECES_ROWS = 3
TITLE = "Checkers"
SINGLE = "single_player"
TWO_PLAYERS = "two_players"

LIGHT_BROWN = (255, 204, 102)
DARK_BROWN = (204, 102, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

BLACK_QUEEN = pygame.transform.scale(pygame.image.load('assets/black_queen.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load('assets/white_queen.png'), (SQUARE_SIZE - 20, SQUARE_SIZE - 20))