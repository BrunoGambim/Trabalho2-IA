import random
from typing import Tuple

from ..othello.gamestate import GameState

import math

from threading import Thread

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.



"""
função MIN(s,𝛼,β): retorna um valor de utilidade e a ação que tem aquele valor
se TERMINAL(s): retorna UTILIDADE(s)
v ← +∞; a = NULL
para cada s’,a’ em SUCESSORES(s)
v ← min(v, MAX(s’,𝛼,β)); a ← a’
β ← min(β , v)
se β ≤ 𝛼: break //sai do loop: o MAX que chamou tem uma alternativa 𝛼 melhor que β.
retorna v, a
"""

"""
função MAX(s,𝛼,β): retorna um valor de utilidade e a ação que tem aquele valor
se TERMINAL(s): retorna UTILIDADE(s)
v ← -∞; a = NULL
para cada s’,a’ em SUCESSORES(s)
v ← max(v, MIN(s’,𝛼,β)); a ← a’
𝛼 ← max(𝛼, v)
se 𝛼 ≥ β: break //sai do loop: o MIN que chamou tem uma alternativa β melhor que 𝛼.
retorna v, a
"""

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

def evaluate_state(state: GameState) -> int:
    global PLAYER
    v = 0
    for x in range(0, len(static_weights)):
        for y in range(0, len(static_weights[x])):
            if state.board.tiles[x][y] == PLAYER:
                v = static_weights[x][y] + COIN_PARITY_OFFSET
            else:
                v = -static_weights[x][y] - COIN_PARITY_OFFSET
    return v

def MAX(state: GameState, alpha: int, beta: int, height: int) -> int:
    if STOP:
        return 0
        
    if state.is_terminal() or height == 0:
        return evaluate_state(state)
    
    v = -math.inf

    for successor in state.board.legal_moves(state.player):
        v = max(v, MIN(state.next_state(successor), alpha, beta, height - 1))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    
    return v



def MIN(state: GameState, alpha: int, beta: int, height: int) -> int:
    if STOP:
        return 0
    if state.is_terminal() or height == 0:
        return evaluate_state(state)
    
    v = +math.inf

    for successor in state.board.legal_moves(state.player):
        v = min(v, MAX(state.next_state(successor), alpha, beta, height - 1))
        beta = min(beta, v)
        if beta <= alpha:
            break
    
    return v

def MAX_ROOT(state: GameState, alpha: int, beta: int, height: int) -> Tuple[int, int]:
    if state.is_terminal() or height == 0:
        return evaluate_state(state)
    
    v = -math.inf

    best_successor = None
    
    for successor in state.board.legal_moves(state.player):
        minimized = MIN(state.next_state(successor), alpha, beta, height - 1)
        if minimized > v:
            v = minimized
            best_successor = successor
        alpha = max(alpha, v)
        if alpha >= beta:
            break
        
    return best_successor

STATE = None
RESULT = None

MAX_DEPTH = 100

STOP = False


def a_b_pruning():
    global PLAYER, STATE, RESULT, MAX_DEPTH, STOP
    for x in range(5, MAX_DEPTH):
        maximized_root = MAX_ROOT(STATE, -math.inf, +math.inf, x)
        if STOP:
            return
        RESULT = maximized_root

def make_move(state: GameState) -> Tuple[int, int]:
    global STATE, RESULT, MAX_DEPTH, PLAYER, STOP
    RESULT = None
    STATE = state
    STOP = False
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada com as pretas.
    # Remova-o e coloque a sua implementacao da poda alpha-beta
    PLAYER = state.player
    

    thread = Thread(target=a_b_pruning)
    

    
    
    thread.start()
    thread.join(4)
    STOP = True
    thread.join()

    return RESULT

