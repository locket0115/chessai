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
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [ 0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [ 0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [ 0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ])

    BISHOP_TABLE = numpy.array([
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
        [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
        [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
        [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
        [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ])

    ROOK_TABLE = numpy.array([
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
    ])

    QUEEN_TABLE = numpy.array([
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
    ])

    KING_TABLE = numpy.array([
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
        [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
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

        if best_move != None:
            print(f"best score {best_score} with moving {best_piece.color} {best_piece.name} at {best_move.initial.row},{best_move.initial.col} to {best_move.final.row},{best_move.final.col}")
        return best_piece, best_move

    @staticmethod
    def alphabeta(board, depth, a, b, maximizing):
        if depth == 0:
            return Heuristics.evaluate(board)
        
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