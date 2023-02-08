import agents.othello.board as board 
import agents.othello.gamestate as g_state 
import table_compiler as tc
import os
import time
import agents.timer as timer
import importlib
import threading
import numpy as np
import cma
import multiprocessing
import agents.agent1.agent as agent_1
import agents.agent2.agent as agent_2
import agents.agent3.agent as agent_3
import agents.agent4.agent as agent_4
import agents.agent5.agent as agent_5
import agents.agent6.agent as agent_6
import agents.agent7.agent as agent_7
import agents.agent8.agent as agent_8
import agents.agent9.agent as agent_9
import agents.agent10.agent as agent_10
import agents.agent11.agent as agent_11
import agents.agent12.agent as agent_12
import agents.agent13.agent as agent_13
import agents.agent14.agent as agent_14
import agents.agent15.agent as agent_15
import agents.agent16.agent as agent_16
import agents.agent17.agent as agent_17
import agents.agent18.agent as agent_18
import agents.agent19.agent as agent_19
import agents.agent20.agent as agent_20
import agents.agent1.mobility_tables as mobility_tables_1
import agents.agent2.mobility_tables as mobility_tables_2
import agents.agent3.mobility_tables as mobility_tables_3
import agents.agent4.mobility_tables as mobility_tables_4
import agents.agent5.mobility_tables as mobility_tables_5
import agents.agent6.mobility_tables as mobility_tables_6
import agents.agent7.mobility_tables as mobility_tables_7
import agents.agent8.mobility_tables as mobility_tables_8
import agents.agent9.mobility_tables as mobility_tables_9
import agents.agent10.mobility_tables as mobility_tables_10
import agents.agent11.mobility_tables as mobility_tables_11
import agents.agent12.mobility_tables as mobility_tables_12
import agents.agent13.mobility_tables as mobility_tables_13
import agents.agent14.mobility_tables as mobility_tables_14
import agents.agent15.mobility_tables as mobility_tables_15
import agents.agent16.mobility_tables as mobility_tables_16

import random


BLACK = 'B'
WHITE = 'W'

def run(agent1, agent2, board, player):
    op = WHITE if player == BLACK else BLACK
    color_names = ['black', 'white']
    state = g_state.GameState(board, player)
    last_player = None

    delay = 6.5
    pace = 0.00001

    result = None
    finish = None

    player_modules = {
        BLACK: agent1,
        WHITE: agent2,
    }

    start = time.localtime()

    illegal_count = {BLACK: 0, WHITE: 0}

    while True:  
        current_player = state.player
        opponent = WHITE if current_player == BLACK else BLACK

        p1_score = state.board.num_pieces(player) 
        p2_score = state.board.num_pieces(op) 
        if state.is_terminal():
            result = 0 if p1_score > p2_score else 1 if p2_score > p1_score else 2
            finish = time.localtime()

            p1 = 0
            p2 = 0
            if state.board.tiles[0][0] == player:
                p1 += 1
            elif state.board.tiles[0][0] == op:
                p2 += 1

            if state.board.tiles[0][7] == player:
                p1 += 1
            elif state.board.tiles[0][7] == op:
                p2 += 1

            if state.board.tiles[7][0] == player:
                p1 += 1
            elif state.board.tiles[7][0] == op:
                p2 += 1

            if state.board.tiles[7][7] == player:
                p1 += 1
            elif state.board.tiles[7][7] == op:
                p2 += 1

            return (result, p1, p2)
        
        if illegal_count[current_player] >= 5:
            result = 0 if current_player == WHITE else 1
            finish = time.localtime()
            print("acabou por problema")
            return (3, 0, 0)

        if last_player == current_player:
            time.sleep(pace)
        state_copy = state.copy()

        start = time.time()
        function_call = timer.FunctionTimer(player_modules[current_player].make_move, (state_copy,))
        
        move = function_call.run(delay)
            
        elapsed = time.time() - start

        if move is None:
            illegal_count[current_player] += 1
            continue

        move_x, move_y = move

        if not isinstance(move_x, int) or not isinstance(move_y, int):
            move_x = move_y = -1

        if state.is_legal_move(move):   
            last_player = current_player 
            state = state.next_state(move)  

        else:
            illegal_count[current_player] += 1

        if pace - elapsed > 0:
            time.sleep(pace - elapsed)

def game(agent1, agent2, queue, state_points):
    print("starting game", agent2)
    state = state_points[0]
    points = state_points[1]

    fixed_agent = [agent_13, agent_14, agent_15, agent_16]
    fixed_m3_agent = [agent_17, agent_18, agent_19, agent_20]
    agents = [agent_1, agent_2, agent_3, agent_4, agent_5, agent_6,agent_7, agent_8, agent_9, agent_10, agent_11, agent_12]
    result = 0
    value = (3, 0, 0)
    while value[0] == 3:
        value = run(fixed_agent[agent1], agents[agent2], state.board, state.player)
    """if value == 1:
        result -= 2*points
    elif value == 2:
        result -= 1*points"""
    result -= value[2]
    print("end of the game", agent2, value)

    value = (3, 0, 0)
    while value[0] == 3:
        value = run(agents[agent2], fixed_agent[agent1], state.board, state.player)
    """if value == 0:
        result -= 2*points
    elif value == 2:
        result -= 1*points"""
    result -= value[1]
    print("end of the game", agent2, value)
    
    value = (3, 0, 0)
    while value[0] == 3:
        value = run(fixed_m3_agent[agent1], agents[agent2], state.board, state.player)
    print("end of the game", agent2, value)

    """
    if value[0] == 1:
        print("vitoria", agent2)
        result -= 2*points
    elif value[0] == 2:
        print("empate", agent2)
        result -= 1*points"""
    
    result -= value[2]
    
    value = (3, 0, 0)
    while value[0] == 3:
        value = run(agents[agent2], fixed_m3_agent[agent1], state.board, state.player)
    print("end of the game", agent2, value)
    """
    if value[0] == 0:
        print("vitoria", agent2)
        result -= 2*points
    elif value[0] == 2:
        print("empate", agent2)
        result -= 1*points"""
    result -= value[1]
    
    print("fim", agent2, result)
    queue.put(result)

AGENTES_NA_RODADA = 4

def create_random_state(height):
    state = g_state.GameState(board.Board(), BLACK)
    for i in range(height):
        legal_moves = list(state.legal_moves())
        move = random.choice(legal_moves) if len(legal_moves) > 0 else (-1, -1)
        state = state.next_state(move) 

    return state


def start_learning():
    inital_vars = [ 13.26624121,  -2.15330555,   7.98142546,   0.86147208,
       -14.33692948,  -5.19374529,  -2.25052133,   6.80119674,
         2.30210902,   2.31156192,  -0.12208649,  13.0689021 ,
        10.6203269 ]

    es = cma.CMAEvolutionStrategy(inital_vars, 2.5)


    tc.compileTable(12, inital_vars)
    tc.compileTable(13, inital_vars)
    tc.compileTable(14, inital_vars)
    tc.compileTable(15, inital_vars)

    importlib.reload(mobility_tables_13)
    importlib.reload(mobility_tables_14)
    importlib.reload(mobility_tables_15)
    importlib.reload(mobility_tables_16)
    importlib.reload(agent_13)
    importlib.reload(agent_14)
    importlib.reload(agent_15)
    importlib.reload(agent_16)

    for generation in range(50):
        result = [0,0,0,0,0,0,0,0,0,0,0]
        var_list = es.ask()
        print("starting new generation", generation,len(var_list))
        for i in range(11):
            tc.compileTable(i, var_list[i])

        importlib.reload(mobility_tables_1)
        importlib.reload(mobility_tables_2)
        importlib.reload(mobility_tables_3)
        importlib.reload(mobility_tables_4)
        importlib.reload(mobility_tables_5)
        importlib.reload(mobility_tables_6)
        importlib.reload(mobility_tables_7)
        importlib.reload(mobility_tables_8)
        importlib.reload(mobility_tables_9)
        importlib.reload(mobility_tables_10)
        importlib.reload(mobility_tables_11)
        importlib.reload(mobility_tables_12)
        importlib.reload(agent_1)
        importlib.reload(agent_2)
        importlib.reload(agent_3)
        importlib.reload(agent_4)
        importlib.reload(agent_5)
        importlib.reload(agent_6)
        importlib.reload(agent_7)
        importlib.reload(agent_8)
        importlib.reload(agent_9)
        importlib.reload(agent_10)
        importlib.reload(agent_11)
        importlib.reload(agent_12)

        rounds = []
        states = [(create_random_state(0), 10), (create_random_state(2), 6), (create_random_state(2), 6)]
        for state in states:
            for i in range(11):

                rounds.append((i, state))

                if len(rounds) == AGENTES_NA_RODADA or (state == states[(len(states)-1)] and i == 10 ):
                    print("starting new round", rounds)
                    threads = [0] * len(rounds)
                    queues = [0] * len(rounds)
                    for k in range(len(rounds)):
                        queue = multiprocessing.Queue()
                        thread = multiprocessing.Process(target=game, args=(k, rounds[k][0], queue, rounds[k][1]))
                        queues[k] = queue
                        threads[k] = thread
                        thread.start()
                        threads.append(thread)
        
                    for thread in threads:
                        thread.join()

                    for k in range(len(rounds)):
                        value = queues[k].get()
                        agent_index = rounds[k][0]
                        result[agent_index] += value
                    print(result)

                    rounds = []

        solutions = []
        for i in range(11):
            solutions.append((var_list[i], result[i]))
        es.tell(var_list, result)

        f = open("result.txt", "a")
        string = "\generation: " + str(generation) + "\nresults:\n" + str(solutions)  + "\nbest:" + str(es.result.xbest) + "\nb value:" + str(es.result.fbest)
        f.write(string)
        f.close()


        


if __name__ == "__main__":
    start_learning()
