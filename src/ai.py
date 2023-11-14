from const import *
from board import Board
from square import Square
from piece import *
from move import Move
import copy
import numpy

class Heuristics:

    # The tables denote the points scored for the position of the chess pieces on the board.

    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0, -1,  0,  0,  0,  0, -1,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    KING_TABLE = numpy.array([
        [ -30, -40, -40, -50, -50, -40, -40, -30],
        [ -30, -40, -40, -50, -50, -40, -40, -30],
        [ -30, -40, -40, -50, -50, -40, -40, -30],
        [ -30, -40, -40, -50, -50, -40, -40, -30],
        [ -20, -30, -30, -40, -40, -30, -30, -20],
        [ -10, -20, -20, -20, -20, -20, -20, -10],
        [  20,  20,   0,   0,   0,   0,  20,  20],
        [  20,  30,  10,   0,   0,  10,  30,  20]
    ])

    def get_value(piece, row, col):
        sign = 1 if piece.color == 'white' else -1
        Row = row if piece.color == 'white' else ROWS-1-row

        if isinstance(piece, Pawn):
            return piece.value + Heuristics.PAWN_TABLE[Row][col] * sign
        if isinstance(piece, Knight):
            return piece.value + Heuristics.KNIGHT_TABLE[Row][col] * sign
        if isinstance(piece, Bishop):
            return piece.value + Heuristics.BISHOP_TABLE[Row][col] * sign
        if isinstance(piece, Rook):
            return piece.value + Heuristics.ROOK_TABLE[Row][col] * sign
        if isinstance(piece, Queen):
            return piece.value + Heuristics.QUEEN_TABLE[Row][col] * sign
        if isinstance(piece, King):
            return piece.value + Heuristics.KING_TABLE[Row][col] * sign


    @staticmethod
    def evaluate(board):
        total = 0

        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    total += Heuristics.get_value(board.squares[row][col].piece, row, col)
        
        return total

class AI:
    @staticmethod
    def get_best_move(board, color):
        best_move = None
        best_piece = None
        best_score = INFINITE

        for moves in board.get_possible_moves(color, bool=False):
            piece, move = moves
            temp_board = copy.deepcopy(board)
            temp_piece = copy.deepcopy(piece)

            temp_board.move(temp_piece, move)

            score = AI.alphabeta(temp_board, 2, -INFINITE, INFINITE, True)
        
            if score < best_score:
                if not temp_board.in_check(temp_piece, move=None):
                    best_score = score
                    best_move = move
                    best_piece = piece

        print(f"\nbest score {best_score} with moving piece {best_piece.color} {best_piece.name} at {best_move.initial.row},{best_move.initial.col}")
        return best_piece, best_move

    @staticmethod
    def alphabeta(board, depth, a, b, maximizing):
        if depth == 0:
            return Heuristics.evaluate(board)
            
            # res = Heuristics.evaluate(board)
            # print(f'{res}')
            # return res
        
        if maximizing:
            best_score = -INFINITE

            for moves in board.get_possible_moves('white', bool=False):
                piece, move = moves
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)

                best_score = max(best_score, AI.alphabeta(temp_board, depth-1, a, b, False))
                a = max(a, best_score)
                if b <= a:
                    break
            return best_score
        else:
            best_score = INFINITE
            
            for moves in board.get_possible_moves('black', bool=False):
                piece, move = moves
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)

                best_score = min(best_score, AI.alphabeta(temp_board, depth-1, a, b, True))
                b = min(b, best_score)
                if b <= a:
                    break
            return best_score