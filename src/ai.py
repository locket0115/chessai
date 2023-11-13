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

        if isinstance(piece, Pawn):
            return piece.value + Heuristics.PAWN_TABLE[row if piece.color == 'white' else ROWS-1-row][col] * sign
        if isinstance(piece, Knight):
            return piece.value + Heuristics.KNIGHT_TABLE[row if piece.color == 'white' else ROWS-1-row][col] * sign
        if isinstance(piece, Bishop):
            return piece.value + Heuristics.BISHOP_TABLE[row if piece.color == 'white' else ROWS-1-row][col] * sign
        if isinstance(piece, Rook):
            return piece.value + Heuristics.ROOK_TABLE[row if piece.color == 'white' else ROWS-1-row][col] * sign
        if isinstance(piece, Queen):
            return piece.value + Heuristics.QUEEN_TABLE[row if piece.color == 'white' else ROWS-1-row][col] * sign
        if isinstance(piece, King):
            return piece.value + Heuristics.KING_TABLE[row if piece.color == 'white' else ROWS-1-row][col] * sign


    @staticmethod
    def evaluate(board):
        total = 0

        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    total += Heuristics.get_value(board.squares[row][col].piece, row, col)
        
        return total

    # @staticmethod
    # def evaluate(board):
    #     material = Heuristics.get_material_score(board)

    #     pawns = Heuristics.get_position_score(board, Pawn, Heuristics.PAWN_TABLE)
    #     knights = Heuristics.get_position_score(board, Knight, Heuristics.KNIGHT_TABLE)
    #     bishops = Heuristics.get_position_score(board, Bishop, Heuristics.BISHOP_TABLE)
    #     rooks = Heuristics.get_position_score(board, Rook, Heuristics.ROOK_TABLE)
    #     queens = Heuristics.get_position_score(board, Queen, Heuristics.QUEEN_TABLE)
    #     kings = Heuristics.get_position_score(board, King, Heuristics.KING_TABLE)

    #     return material + pawns + knights + bishops + rooks + queens + kings

    # @staticmethod
    # def get_position_score(board, piece_type, table):
    #     sum = 0
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             if board.squares[row][col].has_piece():
    #                 piece = board.squares[row][col].piece
    #                 if isinstance(piece, piece_type):
    #                     if piece.color == 'white':
    #                         sum += table[row][col]
    #                     else:
    #                         sum -= table[ROWS-1-row][col]

    #     return sum

    # @staticmethod
    # def get_material_score(board):
    #     sum = 0
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             if board.squares[row][col].has_piece():
    #                 sum += board.squares[row][col].piece.value

    #     return sum
        

class AI:

    @staticmethod
    def get_best_move(board, color):
        best_move = None
        best_piece = None
        best_score = -INFINITE

        for moves in board.get_possible_moves(color, bool=False):
            piece, move = moves
            temp_board = copy.deepcopy(board)
            temp_piece = copy.deepcopy(piece)

            temp_board.move(temp_piece, move)

            score = AI.alphabeta(temp_board, 2, -INFINITE, INFINITE, True)
        
            if score > best_score:

                s = move.initial
                m = Move(s, s)

                if not temp_board.in_check(temp_piece, m):
                    best_score = score
                    best_move = move
                    best_piece = piece

        return best_piece, best_move

    @staticmethod
    def alphabeta(board, depth, a, b, maximizing):
        if depth == 0:
            return Heuristics.evaluate(board)
        
        if maximizing:
            best_score = -INFINITE

            for moves in board.get_possible_moves('white'):
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
            for moves in board.get_possible_moves('black'):
                piece, move = moves
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)

                best_score = min(best_score, AI.alphabeta(temp_board, depth-1, a, b, True))
                a = min(a, best_score)
                if b <= a:
                    break
            return best_score