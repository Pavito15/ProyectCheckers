# king_decorator.py
import pygame
from .constants import CROWN

class KingDecorator:
    def __init__(self, piece):
        self._piece = piece

    def draw(self, win):
        self._piece.draw(win)  # Dibuja la pieza normalmente
        if self._piece.king:
            # Solo añade la corona si la pieza es un rey
            x, y = self._piece.x, self._piece.y
            win.blit(CROWN, (x - CROWN.get_width()//2, y - CROWN.get_height()//2))

    def __getattr__(self, attr):
        # Delega atributos y métodos no definidos a la pieza original
        return getattr(self._piece, attr)
