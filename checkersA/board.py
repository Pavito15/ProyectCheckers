import pygame  # Importa la biblioteca Pygame

# Importa la clase Piece desde el archivo piece.py y algunas constantes desde el archivo constants.py
from .piece import Piece  
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE  

# Definición de la clase Board
class Board:
    def __init__(self):
        # Inicializa las variables del tablero y las piezas restantes
        self.board = []  
        self.red_left = self.white_left = 12  
        self.red_kings = self.white_kings = 0  
        self.create_board()  # Llama al método para crear el tablero

    # Método para dibujar el tablero
    def draw_square(self, win):  
        win.fill(BLACK)  # Rellena la ventana con color negro
        for row in range(ROWS):  # Itera sobre las filas del tablero
            for col in range(row % 2, COLS, 2):  
                # Dibuja un cuadrado rojo en las posiciones pares del tablero
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  

    # Método para mover una pieza en el tablero
    def move(self, piece, row, col):  
        # Intercambia las posiciones en el tablero
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]  
        piece.move(row, col)  # Actualiza la posición de la pieza

        # Verifica si la pieza se convierte en rey
        if row == ROWS - 1 or row == 0:  
            piece.make_king()  # Convierte la pieza en rey
            if piece.color == WHITE:
                self.white_kings += 1  # Incrementa el contador de reyes blancos
            else:
                self.red_kings += 1  # Incrementa el contador de reyes rojos

    # Método para obtener una pieza en una posición dada del tablero
    def get_piece(self, row, col):  
        return self.board[row][col]  # Retorna la pieza en la posición dada

    # Método para crear el tablero de juego
    def create_board(self):  
        for row in range(ROWS):  # Itera sobre las filas del tablero
            self.board.append([])  # Agrega una lista vacía para cada fila
            for col in range(COLS):  # Itera sobre las columnas del tablero
                if col % 2 == ((row + 1) % 2):  
                    # Coloca piezas en las posiciones iniciales del tablero
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE ))  # Agrega una pieza blanca
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))  # Agrega una pieza roja
                    else:
                        self.board[row].append(0)  # Agrega una casilla vacía
                else:
                    self.board[row].append(0)  # Agrega una casilla vacía

    # Método para dibujar el tablero y las piezas
    def draw(self, win):  
        self.draw_square(win)  # Llama al método para dibujar el tablero
        for row in range(ROWS):  # Itera sobre las filas del tablero
            for col in range(COLS):  # Itera sobre las columnas del tablero
                piece = self.board[row][col]  # Obtiene la pieza en la posición actual
                if piece != 0:  # Si hay una pieza en la posición actual
                    piece.draw(win)  # Dibuja la pieza en la ventana

    # Método para eliminar piezas del tablero
    def remove(self, pieces):  
        for piece in pieces:  # Itera sobre las piezas a eliminar
            self.board[piece.row][piece.col] = 0  # Elimina la pieza del tablero
            if piece != 0:  
                self.red_left -= 1  # Decrementa el contador de piezas rojas restantes
            else:
                self.white_left -= 1  # Decrementa el contador de piezas blancas restantes

    # Método para determinar al ganador del juego
    def winner(self):  
        if self.red_left <= 0:  
            return WHITE  # Retorna WHITE si no quedan piezas rojas
        elif self.white_left <= 0:
            return RED  # Retorna RED si no quedan piezas blancas

        return None  # Retorna None si el juego aún no ha terminado

    # Método para obtener los posibles movimientos válidos de una pieza
    def get_value_moves(self, piece):  
        moves = {}  # Diccionario para almacenar los movimientos válidos
        left = piece.col - 1  # Posición a la izquierda de la pieza
        right = piece.col + 1  # Posición a la derecha de la pieza
        row = piece.row  # Fila de la pieza

        if piece.color == RED or piece.king:  
            # Si la pieza es roja o es un rey, se calculan los movimientos hacia arriba
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))  
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:  
            # Si la pieza es blanca o es un rey, se calculan los movimientos hacia abajo
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves  # Retorna los movimientos válidos

    # Método privado para calcular los movimientos hacia la izquierda de una pieza
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):  
        moves = {}  # Diccionario para almacenar los movimientos válidos
        last = []  # Lista para almacenar las piezas saltadas
        for r in range(start, stop, step):  # Itera sobre las filas
            if left < 0:  
                break
            
            current = self.board[r][left]  # Obtiene la pieza en la posición actual
            if current == 0:  
                # Si la casilla está vacía
                if skipped and not last:  
                    break
                
                elif skipped:
                    moves[(r, left)] = last + skipped  
                else:
                    moves[(r, left)] = last
                    
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:  
                # Si la pieza en la posición actual es del mismo color, se detiene la iteración
                break
            else:
                last = [current]  
                
            left -= 1  # Decrementa la posición hacia la izquierda
        return moves  # Retorna los movimientos válidos

    # Método privado para calcular los movimientos hacia la derecha de una pieza
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):  
        moves = {}  # Diccionario para almacenar los movimientos válidos
        last = []  # Lista para almacenar las piezas saltadas
        for r in range(start, stop, step):  # Itera sobre las filas
            if right >= COLS or right < 0:  
                break
            current = self.board[r][right]  # Obtiene la pieza en la posición actual
            if current == 0:  
                # Si la casilla está vacía
                if skipped and not last:  
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    row = min(r + 3, ROWS) if step == 1 else max(r - 3, -1)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:  
                # Si la pieza en la posición actual es del mismo color, se detiene la iteración
                break
            else:
                last = [current]  
            right += step  # Incrementa la posición hacia la derecha
        return moves  # Retorna los movimientos válidos
