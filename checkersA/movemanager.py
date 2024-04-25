from checkersA.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, BLACK, WHITE
from checkersA.constants import ROWS, COLS
from .king_decorator import KingDecorator

class MoveManager:
    @staticmethod
    def move_piece(board, piece, row, col):
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