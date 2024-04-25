
import pygame
from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN

class Piece:
    '''Clase base que representa una ficha en el juego de damas'''
    PADDING = 15
    OUTLINE = 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        
    def calc_pos(self):
        '''Calcula las coordenadas (x, y) de la ficha en el tablero'''
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
    def make_king(self):
        '''Modifica y marca la ficha como un rey'''
        self.king = True
    
    def draw(self, win):
        '''Dibuja la ficha en el tablero'''
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))
    
    def move(self, row, col):
        '''Mueve la ficha a una nueva posición en el tablero'''
        self.row = row
        self.col = col
        self.calc_pos()
    
    def __repr__(self):
        return str(self.color)