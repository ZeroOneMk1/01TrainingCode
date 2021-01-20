import pygame

ROWS, COLS = 8, 8
SQUARE_SIZE = 100

WIDTH, HEIGHT = COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25))
