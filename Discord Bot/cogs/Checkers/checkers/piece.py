from .consts import RED, WHITE, SQUARE_SIZE, GRAY
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True
    
    def move(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return self.color, self.row, self.col, self.king
