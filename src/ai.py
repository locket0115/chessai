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
        [ 0,  0,  0,  0,  0,  0,  0,  0]
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

    @staticmethod
    def evaluate(board):
        material = Heuristics.get_material_score(board)

        pawns = Heuristics.get_position_score(board, Pawn, Heuristics.PAWN_TABLE)
        knights = Heuristics.get_position_score(board, Knight, Heuristics.KNIGHT_TABLE)
        bishops = Heuristics.get_position_score(board, Bishop, Heuristics.BISHOP_TABLE)
        rooks = Heuristics.get_position_score(board, Rook, Heuristics.ROOK_TABLE)
        queens = Heuristics.get_position_score(board, Queen, Heuristics.QUEEN_TABLE)

        return material + pawns + knights + bishops + rooks + queens

    @staticmethod
    def get_position_score(board, piece_type, table):
        sum = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if isinstance(piece, piece_type):
                        if piece.color == 'white':
                            sum += table[row][col]
                        else:
                            sum -= table[ROWS-1-row][col]

        return sum

    @staticmethod
    def get_material_score(board):
        sum = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    sum += piece.value

        return sum
        

class AI:

    @staticmethod
    def get_best_move(board):
        best_move = None
        best_score = INFINITE

        for move in board.get_possible_moves('black'):
            temp_board = copy.deepcopy(board)
            piece = temp_board.squares[move.initial.row][move.initial.col].piece
            if temp_board.in_check(piece, move):
                continue

            temp_board.move(piece, move)

            score = AI.alphabeta(temp_board, 2, -INFINITE, INFINITE, True)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    @staticmethod
    def alphabeta(board, depth, a, b, maximizing):
        if depth == 0:
            print('', end='1')
            return Heuristics.evaluate(board)
        
        if maximizing:
            best_score = -INFINITE
            for move in board.get_possible_moves('white'):
                temp_board = copy.deepcopy(board)
                temp_board.move(temp_board.squares[move.initial.row][move.initial.col].piece, move)

                best_score = max(best_score, AI.alphabeta(temp_board, depth-1, a, b, False))
                a = max(a, best_score)
                if b <= a:
                    break
            return best_score
        else:
            best_score = INFINITE
            for move in board.get_possible_moves('black'):
                temp_board = copy.deepcopy(board)
                temp_board.move(temp_board.squares[move.initial.row][move.initial.col].piece, move)

                best_score = min(best_score, AI.alphabeta(temp_board, depth-1, a, b, True))
                a = min(a, best_score)
                if b <= a:
                    break
            return best_score