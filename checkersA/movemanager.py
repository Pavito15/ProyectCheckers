from checkersA.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, BLACK, WHITE
from checkersA.constants import ROWS, COLS
from .king_decorator import KingDecorator

class MoveManager:
    @staticmethod
    def move_piece(board, piece, row, col):
        """Mueve una pieza en el tablero a una nueva posicion y realiza las acciones necesarias

        Args:
            board (Board): el tablero de juego
            piece (Piece): la pieza que se movera
            row (int): la fila a la que se mueve la pieza
            col (int): la columna a la que se movera la pieza
        """
        # Intercambia las posiciones en el tablero
        piece_to_move = board.get_piece(piece.row, piece.col)
        piece_to_move_at_target = board.get_piece(row, col)
        board.board[piece.row][piece.col], board.board[row][col] = piece_to_move_at_target, piece_to_move
        piece.move(row, col)

        # Verificación de rey
        if row == len(board.board) - 1 or row == 0:
            piece.make_king()
            board.board[row][col] = KingDecorator(piece)
            if piece.color == WHITE:
                board.white_kings += 1
            else:
                board.red_kings += 1


    @staticmethod
    def remove_pieces(board, pieces):
        """Elimina las piezas especificadas del tablero y actualiza el recuento restantes

        Args:
            board (Board): tablero del juego
            pieces (list): lista d epiezas a eliminar
        """
        for piece in pieces:
            current_piece = board.board[piece.row][piece.col]
            board.board[piece.row][piece.col] = 0
            if current_piece.color == RED:
                board.red_left -= 1
            elif current_piece.color == WHITE:
                board.white_left -= 1

            # Debug print statement
            print(f"Removed {current_piece.color} piece at ({piece.row}, {piece.col}).")
            print(f"Red pieces left: {board.red_left}, White pieces left: {board.white_left}")


    @staticmethod
    def _traverse_left(board, start, stop, step, color, left, skipped=[]):
        '''
        Realiza un movimiento de exploración hacia la izquierda desde una posición inicial.

            Args:
                board (Board): El tablero de juego.
                start (int): Fila de inicio para la exploración.
                stop (int): Fila de detención para la exploración.
                step (int): Dirección del movimiento (1 para abajo, -1 para arriba).
                color (tuple): Color de la pieza.
                left (int): Columna de inicio para la exploración.
                skipped (list): Lista de piezas saltadas durante el movimiento.

        Returns:
            dict: Diccionario de movimientos válidos encontrados.
        '''
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = board.get_piece(r, left)
            if current == 0:
                if skipped and not last:
                    break
                
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                    
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(MoveManager._traverse_left(board, r+step, row, step, color, left-1, skipped=last))
                    moves.update(MoveManager._traverse_right(board, r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
                
            left -= 1
        return moves

    @staticmethod
    def _traverse_right(board, start, stop, step, color, right, skipped=[]):
        '''Realiza un movimiento de exploración hacia la derecha desde una posición inicial
           '''
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS or right < 0:  # Chequeo de límites para 'right'
                break
            current = board.get_piece(r, right)
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    row = min(r + 3, ROWS) if step == 1 else max(r - 3, -1)
                    moves.update(MoveManager._traverse_left(board, r + step, row, step, color, right - 1, skipped=last))
                    moves.update(MoveManager._traverse_right(board, r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += step  # Incrementa o decrementa right adecuadamente
        return moves