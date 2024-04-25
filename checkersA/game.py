import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Bucket:
    INSTANCES = {}
    
def singleton(clase):
    def obtener_instancia(*args, **kwargs):
        if clase not in Bucket.INSTANCES:
            Bucket.INSTANCES[clase] = clase(*args, **kwargs)
        return Bucket.INSTANCES[clase]
    return obtener_instancia

@singleton
class Game:
    def __init__(self, win):
        '''Inicializa el juego
            Args:   win : Es la ventana de Pygame en la que se renderiza el juego
        '''
        self.win = win
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
    
    def update(self):
        '''Actualiza la pantalla del juego con el tablero y los moviemientos validos para las fichas'''
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def winner(self):
        '''Determina si hay un ganador en el juego
            Return:  0 si no hay ganador
                    RED si las piezas rojas ganan
                    BLACK si las piezas negras ganan
        '''
        return self.board.winner()
        
    
    def reset(self):
        '''Reinicia el juego'''
        self.__init__
    
    def select(self, row, col):
        '''Selecciona una pieza y muestra sus movimientos válidos'''
        if self.selected: #si se selecciona una pieza
            result = self._move(row, col)  # Cambio hecho aquí
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_value_moves(piece)
            return True
        
        return False
  
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves):
        '''Dibuja los movimientos validos en la pantalla'''
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)       
    
    def change_turn(self):
        '''Cambia el turno del jugador'''
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED