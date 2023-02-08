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

"""                
                                        .!!OQQQOQO6QOOIOI66OQ6QOQOOQQQOI^.                                      
                                   |I!OOQQOOO6O6O66I6IIOIII66OO6QO66QOQOQOQQOQQOI                                  
                              !6QOIQO6OOO|II||I||||||||I|IIII6Q|6O6O6Q66OQOQQQOQQQQO                               
                          .|OOOQ6QOOI|6II6!!!!!!!!!|!!!|!||!|||IIIO6QIOO6O6QOQOOQQQQOOO!                           
                       IO66OQI||III66|||!!!!^!!^!^!!!^!!!!|!||||||I66OOOOOOOO6O66OQQQOQQQQOO||.                    
                      OO66|I!!||I6I|!^!!^!!^!^^!^!^!^^!!!!!!||!|||IIIIIOOQQOO6I6QOOQOOOOOOQOQQQ|.                  
                 .I6|||||!6OI6OO|!!^!^!!^^^!!^!^^!!^!!!!!!!!||!!|||II|6I666O6OOQ6I6QO6OOQQOOQOOQQO6                
                |66OI|6I66666OI^!^^^^^^!!^!!!^!^^!!^!!!!!!!!!!!||||I|I|II6666O6O66I|I6OQOQOOQQQQQQQQ!              
              ^I||6O66666IOO|^^^!^^^!^^!^!!^!^^!!!!^!!!!!!!!!!||||||II|II666OI6O6OII|I66OQO6O6QQOQOQOQI            
           6OI|O66|I6OO6II!^^^^!^^^!^^^!^^!!^!!^!^!^!!!!!!!|!|!|||||||III6I666O6OO666I6I6OOOOQOQQOQQOQQ.           
          IOOI!|!|II6QOO6|^^^^.^^!^^^!^!!^!^^^!!^!!^!!^!!!!!!!!||||||I|III66666OO6O6I||I6666OOOQQQOQOQQQ6          
         !OO6I|!^6QO6666!!^.^^^.^^^^^!^^!^^^^^^^!!^^!!!^!!!!!|!!||||||I|III6666O6OO66I!|6IIOOOOQOQQOQOQQQ.         
         O6OI^^666II66O|^!^.^^^^^^^^^^^^^^^^.^^^^^^!^!!!!^!!!!!||!!||I|IIIII66666OQOOII6OIO6I666OQOOQQOQQQ         
        OOO||!I^||IOO6!!^^^!^^^^^^^.^^.^^^^^^^.^^!^!!^!!!!!!!|!||!||||I|IIIII66666OOOQIO!I|66OOQOOQOQQOOQOQ^       
        OQIII|!!|II6O|^!^!!^^^^.^^.^..^^.^^^^.^.^^^^^^!^!!!!!|!!!|||||!||IIII6666OOO6I6||O6I6I6OQOQQOOQOQQOO       
       ^6OOI!66|I6OOI^^!^^^^.^.^^^..^.^^^.^^^.^^^^.^^^^!!!^!!!!|!||!|||I|II6I666666Q6IO6I666|6OOO6OQQQOOOQOQ       
       |OQOI!O|IOOO6|!^!!^^.^^^^..^..^^.^^^.^^^.^..^^!^!!^^!!!!|!||||!||I|III666OI6O666Q666QOQ66OOOOQOQOQQOO       
       !QOII6^!|6I6|!^^!^^..^.^^.....^^^^^^^.^.....^.^^^^^!!^|!|!||||||||IIIII66I66I6OII6QI|OOQ6QOO6OOOQOQ|^       
      !OOOO6|^!||I6!^!^^^..^.^... ....^.^^!^^... ....^^^.^^^!!!!!||||I||III6I6I666I6I66OIOO6OOO6OOQQOOQQO|         
       |!6O|^I|!^II^!^!^^..^.^....  ....^.^^^^. ...^^^^^^^.!!^!!!!||||||6|III66I6II66IIOO6QOQOQ66O6OQQOQO          
        I6!I|I||I|!^^!^!^!!^^^^^^.^.^!^^^.^^^^^..^^^!!^!!!||!|!!!!|||||III|III66I666OOOOQ6QOOO6Q6OO6OQOQQI         
         !666|!|II|^^!^^^!^!^|||||I||||!!!^^^^^^!^!|!||II|I|IIII||!|!|||II6III6I66I6OOOQOOQOOOOOQOOOQQOQI          
          ^|!I6OI|!!!!^^.^^!^|||IIII||I||!!^!^^!^!|!||III6|II|III|||||||IIIIII|6I6I66OOQOQOQQOOOQOOOOQOOO          
           I6I|II|!^!!^^^^^!^!^!^!^!!^^!!!!!^!!!!!||||!!^^^.^^.^^!!!I|III6I666I666I6I66OOQOOOOOQOQOQOQ!            
            ||IIO!^!^^^^^!...^^^!!!!!^^^^!^^^^^!!!!!!!!^....^|||!|!!|II|I66666I66I6666OOOOOQOO6QOOOOQ6.            
            .I|6O^^!^^^.^^.^!IIII66!!!!^!^^.^^.^^!||||!!!|||!!!|||IOO66III666I666666666OOOOOOOQOOOQOI              
             |III^^^^^^^^||!!IQQOQOO6II||!^^^^.!^!||I|||!!I6OOOOQQOOQOQO6O6666666I66I66OOO6OOQOQ6QOI               
               |^^^^.^!||!OQI^6QQOQ||QI||!^^^..^!!|III|!I66!^^|I66I|6OOQ6II6666IOI666666OOOQQOOQQOQ                
               !^!^^^^!I|^.^.^..!!!|I||!!!^^^..^!!I|II|^^^^^!^^^!!!|I||III|6III6I6I666666OOOQOO6OQO                
               !^.^...^^^^..^.!||||I|||^!^^^!.^^!||I|III|^!||!|!!!|!|||I|I||||||III66666OO6OQOII6OO!               
               !!^^^..^^!^^^||||I||!!!^^^^!^.^^!!||III|I|!^!^!!|||I||II||||!|||||IIII6O666OOO6|OOO66.              
               ^^.^.^..^!!^!!!|!!!!|!^.^^^^^^.^!^!|III|I|||!!!!!!||||I|||||||II6III6I6O66OOO6II66|O6I              
               ^^.^.^^^.!^^!!|!!!^!^.^^^^^!^..^!!|I|IIII|||!!!|!|!!|!|!||!|||IIII66I666O6OOOII||6!6I6              
               ^.^^^^...^^!^!^^^^..^.^^^^^!^^.^!!||II6I||!|!^!!!|!!!|!!|||!|I|II66I66666O6OO6II6II||I              
               !^^^.^.....^!^^^^^..^^^^!^!^^...^!|||II66I!!!^^!!!!!!!||!|!||I6II66I666I66O666I|||OII6              
               !^^^^^.^.. ^^.^.^.^^^!!|^!..  .^^!!III6666II!!^!^!!|!|!|!|||||6I66666I66O666O66||!6O66              
               !^^^^^^^^......^.^^!!|^^^^...^^^^^!|I666I666I|^!!!!!|||!!||||I6I666I666666O666I|I|I666              
               !^!^!^^^^.^.....^!|!||..^^!^^!!!!||III66I6I66I!^!!|!|!|!!||I6I6I6666666O66O6O6||||||66              
               !!^!!^!!^^.^^^^!!!|||!^^!!||!|||II6OO6II666O66||!!!|||!!!||II6I666I6666O6O66O6II|||II6.             
               .|!^!^^^!^!!^!!!|!||^^!!66QQQI66OOOQQQOQ666O66I6|!!!||!||I|III66666666O6OO66OII6II|I66              
                ^!!^^^!!^!!!!||I|!.^..^|66I!||OOOII|II6O6I6IIII|!!!!!||||I6I6O666666O6O6O6O6IIII6II!               
                .!^!^!^!!!!|!||I!^^^^^.^^^^^.!^^.^!||II6IIIII|II||!!!!|I|I6I666O66I6666O6O66II||I6I^               
                 !!!!^!!!!|!||||!!^!^!^^^^^.^^!!..^^!!!!|II|I6I6II!!|!||||6666666666666O6O66|!|II6|                
                 !^!^!!!!!|||||!|!!^!^^^..^^^!!^.^!!^^!!!!|IIII6I||!||||II66I66I6666OO66O666!!|II.                 
                 ^^!!!!|!!!||!||!!!^!^^^^..^^!^^.^^!!!!!!||II6III||||!!|I66I66666I66O66O6O66II|6^                  
                  ^!^!!!!!!!!!!|!^!!!!!!!|I|I||!I|6I6I6|IIIII6III|I|I|||II66I666666O66I66OO6.                      
                  .!^!!!^!!|!!!|^!|I66OOQO6O6666OOOOOQOOQOQQOOO6IIII|!|||6I6I666666666666O6O                       
                   !!^^!!^!!!!!||IO!^!!|!!^.^^^!!!!|!||I66666I6II66I!!|||II66666666I6666O66Q                       
                   !!^^!!!!^!^!||!^^^!^!!!!^^^!!!!!|||II|II6II|IIII||!||I6I66I66I66666O66OO6                       
                    ^^!^!!^^^!!!!^^^^!!!!!^!^!|!!!!!|I6I6I6III|III|I||||III6I66II66666O6OOO.                       
                    .!!!!^!^^!!!!!^!^!!!!||I6666O66666I6IIIIII|||I|||||III66I6II6666O6O6O6|                        
                     ^!!!^!!!^!!|!^!!^!!!!!!I|||II||||I||I|I|II||||!||II|II6II6I6666666O6OIO                       
                      ^!!!|!!!!!^!^^^!^^^!^!!^^!^.^!!!!|!!!|||||||II||II6II6I6I66I666OO66IO6O!                     
                       ^!!!!!!!!^^!^^^!^^^^^!^^!^!|6I|!!!!!|!|I||||II|I6I6I6I66I666OOO6O6|OO6O|                    
                        !!!!!|!||^!^!^!^^^!^^!^!!^!!|^!^!!!!|I|I|I|I66II6I6I6666666OOOOO!I66O6O!                   
                          |!||||||!!^!^^!^!!!!!^!!^!^^^!!|||I|IIII6666I6II6O66O6O6O6OOOI|666OOOQ6                  
                           ||||||!|!!^!^^!!!!!!!!!!!!!!!|||IIII6I6I66I6IO66666OOOO66OO6!6O6O6OOOO                  
                          !!!||I|||!|!|!|!!|!!|!|!||!!|||IIII666I666666OOOO66666O6I6OQ^I6O6OOOOOOO6                
                          !!!!|I6I|IIII|||I|I|I|IIIIIII6666O66O6I666O66O66OOO6666666I!666OOO6O6O6OOI               
                        ^||!||I|III|II66O6O6O6O6OOO6OO6666OO6666OO66O6OO666666666666!|6OO6OOOOO6O66OQ.             
                   .!!||!|!!!!I^|I|III6I6I6OO6OOOOOO66O66666666OO6666O6666666I66I6|!O66OOO6O6O6OO6O6OOOQO.         
            .!!!!^!^!!!!||!!!!|^!|IIIII6III6II66O6OO6O66O6OO6O666666666666I6II66I!I6O6666OOOOOO6666OOO6O6OO!       
         !I|^^!^!!^!!!!!|!|!^!|!^|||III|III6III6O6OOOO66OO66O666666OI66I66666II|!6OO6O6O6OO66O6O6OOOOOOOO6OOO^     
 .!!!!!!^^!!!!!^!!!!!|!|!!!|!^!| !||||||I|III6I66O6OO6OO66O66OO6I666666I66666!!I6666OO66O66O6OOO666OOOOOOOOOO6OOOI 
!!!!!|^!!^!!^!!!!!|!|!!!!!!|!^!!! .!|||||I|II66OO6OOO6O66O66I6666666I666I66!^666O66666OIOOOOOO6O66OQOOOOOOO66O6OO66
!!!!^!!^!!!!!^!!!!|||!!!!!!|!!!!!^.^!!||||||II6IO6OO666OO6666I6666I666I6|!!6O6O6O66O66O6O666OO6O66OOOO6OOOOOOOOOO6O
!!!!^!!!!!!!!!!!|!|!!^!!||!!|!|!!!|. ^!!||||||II666OO666I6O666666I6I66!^|66O666O66O6666OOO6O66O66OOOQOOOOOO6OOOO66O
^!!!^!!|!!!!!|!!^!!||!!!|!!|!!||!|!|!^ ^!I!|||||I|I6666O66666I6III6I.^6O6O6666I6O66666OO6O6O66O6O6666I6O66666OO6O6O6"""