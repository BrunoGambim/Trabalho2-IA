import random
from typing import Tuple

from ..othello.gamestate import GameState
from .board import Opt_Board
from .board import opt_board_from_string
from .hash_table import HashTable
from .mobility_tables import create_mobility_tables

import math

import sys

from threading import Thread

def evaluate_board(board, mobility_table) -> int:
    v = 0
    v += mobility_table[0].get(board.mobility_table_ids[0])
    v += mobility_table[1].get(board.mobility_table_ids[1])
    v += mobility_table[2].get(board.mobility_table_ids[2])
    v += mobility_table[3].get(board.mobility_table_ids[3])
    v += mobility_table[3].get(board.mobility_table_ids[4])
    v += mobility_table[2].get(board.mobility_table_ids[5])
    v += mobility_table[1].get(board.mobility_table_ids[6])
    v += mobility_table[0].get(board.mobility_table_ids[7])

    v += mobility_table[0].get(board.mobility_table_ids[8])
    v += mobility_table[1].get(board.mobility_table_ids[9])
    v += mobility_table[2].get(board.mobility_table_ids[10])
    v += mobility_table[3].get(board.mobility_table_ids[11])
    v += mobility_table[3].get(board.mobility_table_ids[12])
    v += mobility_table[2].get(board.mobility_table_ids[13])
    v += mobility_table[1].get(board.mobility_table_ids[14])
    v += mobility_table[0].get(board.mobility_table_ids[15])

    v += mobility_table[9].get(board.mobility_table_ids[16])
    v += mobility_table[8].get(board.mobility_table_ids[17])
    v += mobility_table[7].get(board.mobility_table_ids[18])
    v += mobility_table[6].get(board.mobility_table_ids[19])
    v += mobility_table[5].get(board.mobility_table_ids[20])
    v += mobility_table[4].get(board.mobility_table_ids[21])
    v += mobility_table[5].get(board.mobility_table_ids[22])
    v += mobility_table[6].get(board.mobility_table_ids[23])
    v += mobility_table[7].get(board.mobility_table_ids[24])
    v += mobility_table[8].get(board.mobility_table_ids[25])
    v += mobility_table[9].get(board.mobility_table_ids[26])
    
    v += mobility_table[9].get(board.mobility_table_ids[27])
    v += mobility_table[8].get(board.mobility_table_ids[28])
    v += mobility_table[7].get(board.mobility_table_ids[29])
    v += mobility_table[6].get(board.mobility_table_ids[30])
    v += mobility_table[5].get(board.mobility_table_ids[31])
    v += mobility_table[4].get(board.mobility_table_ids[32])
    v += mobility_table[5].get(board.mobility_table_ids[33])
    v += mobility_table[6].get(board.mobility_table_ids[34])
    v += mobility_table[7].get(board.mobility_table_ids[35])
    v += mobility_table[8].get(board.mobility_table_ids[36])
    v += mobility_table[9].get(board.mobility_table_ids[37])

    if board.player == board.BLACK:
        return v
    else:
        return -v
    

def evaluate_terminal_board(board):
    if board.piece_count[board.player] == board.piece_count[board.opponent]:
        return 0
    elif board.piece_count[board.player] > board.piece_count[board.opponent]:
        return +30000
    else:
        return -30000

def MAX(board, alpha: int, beta: int, height: int, board_table, mobility_table) -> int:
    if STOP:
        return 0

    if height == 0:
        if len(board.legal_moves(board.player)) == 0 and len(board.legal_moves(board.opponent)) == 0:
            return evaluate_terminal_board(board)
        return evaluate_board(board, mobility_table)

    v = -math.inf

    legal_moves = board.legal_moves(board.player)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.opponent)) == 0:
            return evaluate_terminal_board(board)
        return MIN(board, alpha, beta, height - 1, board_table, mobility_table)

    for successor in legal_moves:
        minimized = MIN(board.make_player_move(successor[0], board_table), alpha, beta, height - 1, board_table, mobility_table)
        
        if minimized > v:
            board.update_player_moves(successor[0], minimized)
            v = minimized

        alpha = max(alpha, v)
        if alpha >= beta:
            break

    return alpha



def MIN(board, alpha: int, beta: int, height: int, board_table, mobility_table) -> int:
    if STOP:
        return 0

    if  height == 0:
        if len(board.legal_moves(board.player)) == 0 and len(board.legal_moves(board.opponent)) == 0:
            return evaluate_terminal_board(board)
        return evaluate_board(board, mobility_table)

    v = +math.inf

    legal_moves = board.legal_moves(board.opponent)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.player)) == 0:
            return evaluate_terminal_board(board)
        return MAX(board, alpha, beta, height - 1, board_table, mobility_table)

    for successor in legal_moves:
        maximized = MAX(board.make_opponent_move(successor[0], board_table), alpha, beta, height - 1, board_table, mobility_table)
        
        if maximized < v:
            v = maximized
            board.update_opponent_moves(successor[0], maximized)

        beta = min(beta, v)
        if beta <= alpha:
            break

    return beta

def MAX_ROOT(board, alpha: int, beta: int, height: int, board_table, mobility_table) -> Tuple[int, int]:
    v = -math.inf

    best_successor = -1

    for successor in board.legal_moves(board.player):
        minimized = MIN(board.make_player_move(successor[0], board_table), alpha, beta, height - 1, board_table, mobility_table)
        board.update_player_moves(successor[0], minimized)
        if minimized > v:
            v = minimized
            best_successor = successor
            alpha = minimized

    return best_successor[0]

def MAX_ENDGAME(board, alpha: int, beta: int) -> int:
    if STOP:
        return 0

    v = -math.inf

    legal_moves = board.legal_moves(board.player)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.opponent)) == 0:
            return evaluate_terminal_board(board)
        return MIN_ENDGAME(board, alpha, beta)

    for successor in board.legal_moves(board.player):
        v = max(v, MIN_ENDGAME(board.make_player_move_endgame(successor[0]), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    
    return alpha

def MIN_ENDGAME(board, alpha: int, beta: int) -> int:
    if STOP:
        return 0

    v = +math.inf

    legal_moves = board.legal_moves(board.opponent)
    if len(legal_moves) == 0:
        if len(board.legal_moves(board.player)) == 0:
            return evaluate_terminal_board(board)
        return MAX_ENDGAME(board, alpha, beta)

    for successor in legal_moves:
        v = min(v, MAX_ENDGAME(board.make_opponent_move_endgame(successor[0]), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break

    return beta

def MAX_ROOT_ENDGAME(board, alpha: int, beta: int) -> Tuple[int, int]:      
    v = -math.inf

    best_successor = [None]
    legal_moves = board.legal_moves(board.player)
    for successor in legal_moves:
        maximized = MIN_ENDGAME(board.make_player_move_endgame(successor[0]), alpha, beta)
        if maximized > v and not STOP:
            v = maximized
            best_successor = successor
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    
    return best_successor[0]

def a_b_pruning(board, result):
    if board.piece_count[board.EMPTY] > 11:
        mobility_table = create_mobility_tables()
        board_table = HashTable()
        
        alpha = -math.inf
        beta = +math.inf
        for x in range(1, board.piece_count[board.EMPTY] + 2):
            maximized_root = MAX_ROOT(board, alpha, beta, x, board_table, mobility_table)
            if STOP:
                break
            result[0] = maximized_root
    else:
        alpha = -math.inf
        beta = +math.inf
        maximized_root = MAX_ROOT_ENDGAME(board, alpha, beta)
        result[0] = maximized_root

STOP = False

def make_move(state: GameState) -> Tuple[int, int]:
    global STOP
    STOP = False
    result = [None]

    board = opt_board_from_string(str(state.board), state.player)
    if len(board.legal_moves(board.player)) == 0:
        return (-1,-1)

    thread = Thread(target=a_b_pruning, args=(board, result))

    thread.start()
    thread.join(1)
    STOP = True
    thread.join()
    if result[0] != None:
        return result[0]
    else:
        return board.legal_moves(board.player)[0][0]
