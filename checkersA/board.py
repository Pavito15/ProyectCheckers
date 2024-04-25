import pygame

from .piece import Piece
from .movemanager import MoveManager
from .king_decorator import KingDecorator
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE 

class Board:
    '''Esta clase representa el tablero del juego de damas'''
    def __init__(self):
        '''Se inicializa el tablero'''
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_square(self, win):
        '''Dibuja los cuadros del tablero'''
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):  
                pygame.draw.rect(win, RED, (row *SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def promote_to_king(self, piece, row, col):
        if not piece.king:
            piece.make_king()
            # Aplica el decorador y actualiza la posición en el tablero
            self.board[row][col] = KingDecorator(piece)

    def move(self, piece, row, col):
        """Mueve una pieza a una nueva posición. Retorna las piezas saltadas si hay alguna."""
        MoveManager.move_piece(self, piece, row, col)
        if (row == 0 or row == ROWS - 1) and not piece.king:
            piece.make_king()
            self.promote_to_king(piece, row, col)

        #verificacion de rey
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings +=1
            else:
                self.red_kings +=1

    #obtenemos las piezas
    def get_piece(self, row, col):
        '''Obtiene una pieza en una posición especifica en el tablero'''
        return self.board[row][col]        
        
    #creacion del tablero
    def create_board(self):
        '''Crea el tablero incial del juego'''
        for row in range(ROWS):
            self.board.append([])
            for col in range (COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE ))          
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
                    
    #dibujamos las piezas
    def draw(self, win):
        '''Dibuja las piezas en el tablero'''
        self.draw_square(win)  
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def remove(self, pieces):
        '''Elimina piezas del tablero'''
        MoveManager.remove_pieces(self, pieces)
    
    def winner(self):
        '''Determina si hay un ganador'''
        if self.red_left == 0 :
            return 'WHITE'
        if self.white_left == 0 :
            return 'RED'
        return None



    def get_value_moves(self, piece):
        '''Obtiene los posibles movimientos validos para una pieza'''
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(MoveManager._traverse_left(self, row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(MoveManager._traverse_right(self, row - 1, max(row - 3, -1), -1, piece.color, right))
            
        if piece.color == WHITE or piece.king:
            moves.update(MoveManager._traverse_left(self,row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(MoveManager._traverse_right(self,row + 1, min(row + 3, ROWS), 1, piece.color, right))
        
        return moves