import random
from typing import Tuple

from ..othello.gamestate import GameState
from .board import Opt_Board
from .board import opt_board_from_string
from .hash_table import HashTable

import math

from threading import Thread

def evaluate_board(board) -> int:
    v = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if board.tiles[x][y] == board.player:
                v += static_weights[x][y]
            elif board.tiles[x][y] == board.opponent:
                v -= static_weights[x][y]

    #for move in board.legal_moves(board.player):
    #    v += move[0]
    #for move in board.legal_moves(board.opponent):
    #    v -= move[0]

    return v

def MAX(board, alpha: int, beta: int, height: int) -> int:
    global BOARD_TABLE
    if STOP:
        return 0
        
    if height == 0:
        return evaluate_board(board)
    
    v = -math.inf

    legal_moves = board.legal_moves(board.player)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.opponent)) == 0:
            return evaluate_board(board)
        return MIN(board, alpha, beta, height - 1)


    for successor in legal_moves:
        v = max(v, MIN(board.make_player_move(successor, BOARD_TABLE), alpha, beta, height - 1))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    
    return v



def MIN(board, alpha: int, beta: int, height: int) -> int:
    global BOARD_TABLE
    if STOP:
        return 0

    if  height == 0:
        return evaluate_board(board)
    
    v = +math.inf

    legal_moves = board.legal_moves(board.opponent)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.player)) == 0:
            return evaluate_board(board)
        return MAX(board, alpha, beta, height - 1)

    for successor in legal_moves:
        v = min(v, MAX(board.make_opponent_move(successor, BOARD_TABLE), alpha, beta, height - 1))
        beta = min(beta, v)
        if beta <= alpha:
            break
    
    return v

def MAX_ROOT(board, alpha: int, beta: int, height: int) -> Tuple[int, int]:
    global BOARD_TABLE
    if height == 0:
        return evaluate_board(board)
    
    v = -math.inf

    best_successor = None
    legal_moves = board.legal_moves(board.player)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.opponent)) == 0:
            return evaluate_board(board)
    
    for successor in legal_moves:
        minimized = MIN(board.make_player_move(successor, BOARD_TABLE), alpha, beta, height - 1)
        
        if minimized > v:
            v = minimized
            best_successor = successor
        alpha = max(alpha, v)
        if alpha >= beta:
            break     
    
    return best_successor

PLAYER = None

static_weights = [
    [4,-3,2,2,2,2,-3,4],
    [-3,-4,-1,-1,-1,-1,-4,-3],
    [2,-1,1,0,0,1,-1,2],
    [2,-1,0,1,1,0,-1,2],
    [2,-1,0,1,1,0,-1,2],
    [2,-1,1,0,0,1,-1,2],
    [-3,-4,-1,-1,-1,-1,-4,-3],
    [4,-3,2,2,2,2,-3,4]
]

COIN_PARITY_OFFSET = 4

BOARD = None
RESULT = None

MAX_DEPTH = 100
MEAN_DEPTH = [0] * 100
MEAN_DEPTH_COUNTER = 0

BOARD_TABLE = None

STOP = False

def a_b_pruning():
    global BOARD, RESULT, MAX_DEPTH, STOP, MEAN_DEPTH, MEAN_DEPTH_COUNTER

    for x in range(1, MAX_DEPTH):
        maximized_root = MAX_ROOT(BOARD, -math.inf, +math.inf, x)
        if STOP:
            return
        MEAN_DEPTH[MEAN_DEPTH_COUNTER] = x
        RESULT = maximized_root

def make_move(state: GameState) -> Tuple[int, int]:
    global BOARD, RESULT, MAX_DEPTH, STOP, MEAN_DEPTH_COUNTER, BOARD_TABLE
    RESULT = None
    STOP = False
    BOARD_TABLE = HashTable()
    
    BOARD = opt_board_from_string(str(state.board), state.player)
    thread = Thread(target=a_b_pruning)

    thread.start()
    thread.join(1)
    STOP = True
    thread.join()

    mean = 0
    MEAN_DEPTH_COUNTER = MEAN_DEPTH_COUNTER + 1
    i = 0
    while i < MEAN_DEPTH_COUNTER:
        mean += MEAN_DEPTH[i]
        i += 1
    mean = mean / MEAN_DEPTH_COUNTER
    #print(MEAN_DEPTH[MEAN_DEPTH_COUNTER - 1],mean)

    return RESULT

