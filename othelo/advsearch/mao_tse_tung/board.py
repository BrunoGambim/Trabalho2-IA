import math

def copy_opt_board(board):
    b = Opt_Board(board.player)
    b.player = board.player
    b.opponent = board.opponent

    b.piece_count = [board.piece_count[0], board.piece_count[1], board.piece_count[2]]
    for y in range(0,8):
        for x in range(0,8):
            b.tiles[y][x] = board.tiles[y][x]

    return b

def opt_board_from_string(string, player):
    b = Opt_Board(player)

    if player == b.CHAR_BLACK:
            b.player = b.BLACK
            b.opponent = b.WHITE
    else:
        b.player = b.WHITE
        b.opponent = b.BLACK

    b.piece_count = [0, 0, 0]
    for lineno, line in enumerate(string.strip().split('\n')):
        line.strip()  # cuts the \n
        for colno, col in enumerate(line):
            if col == b.CHAR_BLACK:
                b.tiles[lineno][colno] = b.BLACK
                b.piece_count[b.BLACK] += 1
            elif col == b.CHAR_WHITE:
                b.tiles[lineno][colno] = b.WHITE
                b.piece_count[b.WHITE] += 1
            else:
                b.piece_count[b.EMPTY] += 1

    b.player_moves = {}
    b.opponent_moves = {}

    b.player_moves = {}
    b.ordered_player_moves = list()
    b.opponent_moves = {}
    b.ordered_opponent_moves = list()

    b.init_moves()

    return b

class Opt_Board(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    CHAR_BLACK = 'B'
    CHAR_WHITE = 'W'
    CHAR_EMPTY = '.'

    OPPOSITE_DIRECTIONS = [1, 0, 3, 2, 7, 6, 5, 4]
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]

    def __init__(self, player):
        self.tiles = [[self.EMPTY] * 8 for i in range(8)]
        self.player_moves = {}
        self.ordered_player_moves = list()
        self.opponent_moves = {}
        self.ordered_opponent_moves = list()
        self.mobility_table_ids = [0] * 38

    def init_moves(self) -> None:
        if self.piece_count[self.EMPTY] > self.piece_count[self.player] + self.piece_count[self.opponent]:
            for y in range(0,8):
                for x in range(0,8):
                    self.init_moves_for_tile(x, y, self.tiles[y][x])
        else:
            for y in range(0,8):
                for x in range(0,8):
                    self.init_moves_dense_board(x, y, self.tiles[y][x])


    def init_moves_for_tile(self, x, y, color) -> None:
        if color == self.player:
            for direction in range(0, 8):
                counter = 0
                x1, y1 = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]

                while x1 < 8 and y1 < 8 and x1 > -1 and y1 > -1 and self.tiles[y1][x1] == self.opponent:
                    counter += 1
                    x1, y1 = x1 + self.DIRECTIONS[direction][0], y1 + self.DIRECTIONS[direction][1]

                if x1 > 7 or y1 > 7 or x1 < 0 or y1 < 0:
                    continue
        
                if counter > 0 and self.tiles[y1][x1] == self.EMPTY:
                    if self.player_moves.get((x1, y1)) is not None:
                        self.player_moves[(x1, y1)][0].append(self.OPPOSITE_DIRECTIONS[direction])
                    else:
                        self.player_moves[(x1, y1)] = ([self.OPPOSITE_DIRECTIONS[direction]],-1)
                        self.ordered_player_moves.append(((x1, y1), -math.inf))
        elif color == self.opponent:
            for direction in range(0, 8):
                counter = 0
                x1, y1 = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]


                while x1 < 8 and y1 < 8 and x1 > -1 and y1 > -1 and self.tiles[y1][x1] == self.player:
                    counter += 1
                    x1, y1 = x1 + self.DIRECTIONS[direction][0], y1 + self.DIRECTIONS[direction][1]

                if x1 > 7 or y1 > 7 or x1 < 0 or y1 < 0:
                    continue

                if counter > 0 and self.tiles[y1][x1] == self.EMPTY:
                    if self.opponent_moves.get((x1, y1)) != None:
                        self.opponent_moves[(x1, y1)][0].append(self.OPPOSITE_DIRECTIONS[direction])
                    else:
                        self.opponent_moves[(x1, y1)] = ([self.OPPOSITE_DIRECTIONS[direction]],-1)
                        self.ordered_opponent_moves.append(((x1, y1), +math.inf))

    def init_moves_dense_board(self, x, y, color) -> None:
        if color == self.EMPTY:
            for direction in range(0, 8):
                counter = 1
                x1, y1 = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]
                if x1 < 8 and y1 < 8 and x1 > -1 and y1 > -1 and self.tiles[y1][x1] == self.opponent:
                    x1, y1 = x1 + self.DIRECTIONS[direction][0], y1 + self.DIRECTIONS[direction][1]
                    while x1 < 8 and y1 < 8 and x1 > -1 and y1 > -1 and self.tiles[y1][x1] == self.opponent:
                        counter += 1
                        x1, y1 = x1 + self.DIRECTIONS[direction][0], y1 + self.DIRECTIONS[direction][1]

                    if x1 > 7 or y1 > 7 or x1 < 0 or y1 < 0:
                        continue
            
                    if self.tiles[y1][x1] == self.player:
                        if self.player_moves.get((x, y)) is not None:
                            self.player_moves[(x, y)][0].append(direction)
                        else:
                            self.player_moves[(x, y)] = ([direction],-1)
                            self.ordered_player_moves.append(((x, y), -math.inf))
                elif x1 < 8 and y1 < 8 and x1 > -1 and y1 > -1 and self.tiles[y1][x1] == self.player:
                    x1, y1 = x1 + self.DIRECTIONS[direction][0], y1 + self.DIRECTIONS[direction][1]
                    while x1 < 8 and y1 < 8 and x1 > -1 and y1 > -1 and self.tiles[y1][x1] == self.player:
                        counter += 1
                        x1, y1 = x1 + self.DIRECTIONS[direction][0], y1 + self.DIRECTIONS[direction][1]

                    if x1 > 7 or y1 > 7 or x1 < 0 or y1 < 0:
                        continue
            
                    if self.tiles[y1][x1] == self.opponent:
                        if self.opponent_moves.get((x, y)) is not None:
                            self.opponent_moves[(x, y)][0].append(direction)
                        else:
                            self.opponent_moves[(x, y)] = ([direction],-1)
                            self.ordered_opponent_moves.append(((x, y), -math.inf))

    def make_opponent_move(self, move, board_table):
        if self.opponent_moves[move][1] != -1:
            return board_table.get(self.opponent_moves[move][1])

        result = copy_opt_board(self)
        result.process_opponent_move(move, self.opponent_moves[move][0])

        boardId = result.boardId()
        self.opponent_moves[move] = (self.opponent_moves[move][0], boardId)
        board_table.insert(boardId, result)
        return result

    def make_opponent_move_endgame(self, move):
        result = copy_opt_board(self)
        result.process_opponent_move(move, self.opponent_moves[move][0])
        return result

    def process_opponent_move(self, move, directions):
        x , y = move[0], move[1]
        self.tiles[y][x] = self.opponent
        self.piece_count[self.opponent] += 1
        self.piece_count[self.EMPTY] -= 1
        for direction in directions:
            x , y = move[0] + self.DIRECTIONS[direction][0], move[1] + self.DIRECTIONS[direction][1]
            while self.tiles[y][x] != self.opponent:
                self.piece_count[self.opponent] += 1
                self.piece_count[self.player] -= 1
                self.tiles[y][x] = self.opponent
                x , y = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]
        self.init_moves()

    def make_player_move(self, move, board_table):
        if self.player_moves[move][1] != -1:
            return board_table.get(self.player_moves[move][1])

        result = copy_opt_board(self)
        result.process_player_move(move, self.player_moves[move][0])

        boardId = result.boardId()
        self.player_moves[move] = (self.player_moves[move][0], boardId)
        board_table.insert(boardId, result)
        return result

    def make_player_move_endgame(self, move):
        result = copy_opt_board(self)
        result.process_player_move(move, self.player_moves[move][0])
        return result

    def process_player_move(self, move, directions):
        x , y = move[0], move[1]
        self.tiles[y][x] = self.player
        self.piece_count[self.EMPTY] -= 1
        self.piece_count[self.player] += 1
        for direction in directions:
            x , y = move[0] + self.DIRECTIONS[direction][0], move[1] + self.DIRECTIONS[direction][1]
            while self.tiles[y][x] != self.player:
                self.piece_count[self.player] += 1
                self.piece_count[self.opponent] -= 1
                self.tiles[y][x] = self.player
                x , y = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]
        self.init_moves()
    
    def boardId(self):
        self.mobility_table_ids[0] = self.tiles[0][0]+self.tiles[0][1]*3+self.tiles[0][2]*9+self.tiles[0][3]*27+self.tiles[0][4]*81+self.tiles[0][5]*243+self.tiles[0][6]*729+self.tiles[0][7]*2187
        self.mobility_table_ids[1] = self.tiles[1][0]+self.tiles[1][1]*3+self.tiles[1][2]*9+self.tiles[1][3]*27+self.tiles[1][4]*81+self.tiles[1][5]*243+self.tiles[1][6]*729+self.tiles[1][7]*2187
        self.mobility_table_ids[2] = self.tiles[2][0]+self.tiles[2][1]*3+self.tiles[2][2]*9+self.tiles[2][3]*27+self.tiles[2][4]*81+self.tiles[2][5]*243+self.tiles[2][6]*729+self.tiles[2][7]*2187
        self.mobility_table_ids[3] = self.tiles[3][0]+self.tiles[3][1]*3+self.tiles[3][2]*9+self.tiles[3][3]*27+self.tiles[3][4]*81+self.tiles[3][5]*243+self.tiles[3][6]*729+self.tiles[3][7]*2187
        self.mobility_table_ids[4] = self.tiles[4][0]+self.tiles[4][1]*3+self.tiles[4][2]*9+self.tiles[4][3]*27+self.tiles[4][4]*81+self.tiles[4][5]*243+self.tiles[4][6]*729+self.tiles[4][7]*2187
        self.mobility_table_ids[5] = self.tiles[5][0]+self.tiles[5][1]*3+self.tiles[5][2]*9+self.tiles[5][3]*27+self.tiles[5][4]*81+self.tiles[5][5]*243+self.tiles[5][6]*729+self.tiles[5][7]*2187
        self.mobility_table_ids[6] = self.tiles[6][0]+self.tiles[6][1]*3+self.tiles[6][2]*9+self.tiles[6][3]*27+self.tiles[6][4]*81+self.tiles[6][5]*243+self.tiles[6][6]*729+self.tiles[6][7]*2187
        self.mobility_table_ids[7] = self.tiles[7][0]+self.tiles[7][1]*3+self.tiles[7][2]*9+self.tiles[7][3]*27+self.tiles[7][4]*81+self.tiles[7][5]*243+self.tiles[7][6]*729+self.tiles[7][7]*2187
        
        self.mobility_table_ids[8] = self.tiles[0][0]+self.tiles[1][0]*3+self.tiles[2][0]*9+self.tiles[3][0]*27+self.tiles[4][0]*81+self.tiles[5][0]*243+self.tiles[6][0]*729+self.tiles[7][0]*2187
        self.mobility_table_ids[9] = self.tiles[0][1]+self.tiles[1][1]*3+self.tiles[2][1]*9+self.tiles[3][1]*27+self.tiles[4][1]*81+self.tiles[5][1]*243+self.tiles[6][1]*729+self.tiles[7][1]*2187
        self.mobility_table_ids[10] = self.tiles[0][2]+self.tiles[1][2]*3+self.tiles[2][2]*9+self.tiles[3][2]*27+self.tiles[4][2]*81+self.tiles[5][2]*243+self.tiles[6][2]*729+self.tiles[7][2]*2187
        self.mobility_table_ids[11] = self.tiles[0][3]+self.tiles[1][3]*3+self.tiles[2][3]*9+self.tiles[3][3]*27+self.tiles[4][3]*81+self.tiles[5][3]*243+self.tiles[6][3]*729+self.tiles[7][3]*2187
        self.mobility_table_ids[12] = self.tiles[0][4]+self.tiles[1][4]*3+self.tiles[2][4]*9+self.tiles[3][4]*27+self.tiles[4][4]*81+self.tiles[5][4]*243+self.tiles[6][4]*729+self.tiles[7][4]*2187
        self.mobility_table_ids[13] = self.tiles[0][5]+self.tiles[1][5]*3+self.tiles[2][5]*9+self.tiles[3][5]*27+self.tiles[4][5]*81+self.tiles[5][5]*243+self.tiles[6][5]*729+self.tiles[7][5]*2187
        self.mobility_table_ids[14] = self.tiles[0][6]+self.tiles[1][6]*3+self.tiles[2][6]*9+self.tiles[3][6]*27+self.tiles[4][6]*81+self.tiles[5][6]*243+self.tiles[6][6]*729+self.tiles[7][6]*2187
        self.mobility_table_ids[15] = self.tiles[0][7]+self.tiles[1][7]*3+self.tiles[2][7]*9+self.tiles[3][7]*27+self.tiles[4][7]*81+self.tiles[5][7]*243+self.tiles[6][7]*729+self.tiles[7][7]*2187

        self.mobility_table_ids[16] = self.tiles[0][5]+self.tiles[1][6]*3+self.tiles[2][7]*9
        self.mobility_table_ids[17] = self.tiles[0][4]+self.tiles[1][5]*3+self.tiles[2][6]*9+self.tiles[3][7]*27
        self.mobility_table_ids[18] = self.tiles[0][3]+self.tiles[1][4]*3+self.tiles[2][5]*9+self.tiles[3][6]*27+self.tiles[4][7]*81
        self.mobility_table_ids[19] = self.tiles[0][2]+self.tiles[1][3]*3+self.tiles[2][4]*9+self.tiles[3][5]*27+self.tiles[4][6]*81+self.tiles[5][7]*243
        self.mobility_table_ids[20] = self.tiles[0][1]+self.tiles[1][2]*3+self.tiles[2][3]*9+self.tiles[3][4]*27+self.tiles[4][5]*81+self.tiles[5][6]*243+self.tiles[6][7]*729
        self.mobility_table_ids[21] = self.tiles[0][0]+self.tiles[1][1]*3+self.tiles[2][2]*9+self.tiles[3][3]*27+self.tiles[4][4]*81+self.tiles[5][5]*243+self.tiles[6][6]*729+self.tiles[7][7]*2187
        self.mobility_table_ids[22] = self.tiles[1][0]+self.tiles[2][1]*3+self.tiles[3][2]*9+self.tiles[4][3]*27+self.tiles[5][4]*81+self.tiles[6][5]*243+self.tiles[7][6]*729
        self.mobility_table_ids[23] = self.tiles[2][0]+self.tiles[3][1]*3+self.tiles[4][2]*9+self.tiles[5][3]*27+self.tiles[6][4]*81+self.tiles[7][5]*243
        self.mobility_table_ids[24] = self.tiles[3][0]+self.tiles[4][1]*3+self.tiles[5][2]*9+self.tiles[6][3]*27+self.tiles[7][4]*81
        self.mobility_table_ids[25] = self.tiles[4][0]+self.tiles[5][1]*3+self.tiles[6][2]*9+self.tiles[7][3]*27
        self.mobility_table_ids[26] = self.tiles[5][0]+self.tiles[6][1]*3+self.tiles[7][2]*9

        self.mobility_table_ids[27] = self.tiles[5][7]+self.tiles[6][6]*3+self.tiles[7][5]*9
        self.mobility_table_ids[28] = self.tiles[4][7]+self.tiles[5][6]*3+self.tiles[6][5]*9+self.tiles[7][4]*27
        self.mobility_table_ids[29] = self.tiles[3][7]+self.tiles[4][6]*3+self.tiles[5][5]*9+self.tiles[6][4]*27+self.tiles[7][3]*81
        self.mobility_table_ids[30] = self.tiles[2][7]+self.tiles[3][6]*3+self.tiles[4][5]*9+self.tiles[5][4]*27+self.tiles[6][3]*81+self.tiles[7][2]*243
        self.mobility_table_ids[31] = self.tiles[1][7]+self.tiles[2][6]*3+self.tiles[3][5]*9+self.tiles[4][4]*27+self.tiles[5][3]*81+self.tiles[6][2]*243+self.tiles[7][1]*729
        self.mobility_table_ids[32] = self.tiles[0][7]+self.tiles[1][6]*3+self.tiles[2][5]*9+self.tiles[3][4]*27+self.tiles[4][3]*81+self.tiles[5][2]*243+self.tiles[6][1]*729+self.tiles[7][0]*2187
        self.mobility_table_ids[33] = self.tiles[0][6]+self.tiles[1][5]*3+self.tiles[2][4]*9+self.tiles[3][3]*27+self.tiles[4][2]*81+self.tiles[5][1]*243+self.tiles[6][0]*729
        self.mobility_table_ids[34] = self.tiles[0][5]+self.tiles[1][4]*3+self.tiles[2][3]*9+self.tiles[3][2]*27+self.tiles[4][1]*81+self.tiles[5][0]*243
        self.mobility_table_ids[35] = self.tiles[0][4]+self.tiles[1][3]*3+self.tiles[2][2]*9+self.tiles[3][1]*27+self.tiles[4][0]*81
        self.mobility_table_ids[36] = self.tiles[0][3]+self.tiles[1][2]*3+self.tiles[2][1]*9+self.tiles[3][0]*27
        self.mobility_table_ids[37] = self.tiles[0][2]+self.tiles[1][1]*3+self.tiles[2][0]*9

        return (self.mobility_table_ids[0],self.mobility_table_ids[1],self.mobility_table_ids[2],self.mobility_table_ids[3],self.mobility_table_ids[4],self.mobility_table_ids[5],self.mobility_table_ids[6],self.mobility_table_ids[7])

    def legal_moves(self, color):
        if color == self.opponent:
            return self.ordered_opponent_moves
        else:
            return self.ordered_player_moves

    def update_player_moves(self, move, value):
        l = len(self.ordered_player_moves)
        for i in range(0, l):
            if move == self.ordered_player_moves[i][0]:
                if self.ordered_player_moves[i][1] > value:
                    if l == i + 1:
                        self.ordered_player_moves[i] = (move, value)
                    else:
                        cond = True
                        for j in range(i + 1, l):
                            if self.ordered_player_moves[j][1] > value:
                                self.ordered_player_moves[j - 1] = self.ordered_player_moves[j]
                            else:
                                self.ordered_player_moves[j - 1] = (move, value)
                                cond = False
                                break
                        if cond:
                            self.ordered_player_moves[l - 1] = (move, value)
                    break
                else:
                    if 0 == i:
                        self.ordered_player_moves[i] = (move, value)
                    else:
                        cond = True
                        for j in range(0, i):
                            k = i - j
                            if self.ordered_player_moves[k - 1][1] < value:
                                self.ordered_player_moves[k] = self.ordered_player_moves[k - 1]
                            else:
                                self.ordered_player_moves[k] = (move, value)
                                cond = False
                                break
                        if cond:
                            self.ordered_player_moves[0] = (move, value)
                    break

    
    def update_opponent_moves(self, move, value):
        l = len(self.ordered_opponent_moves)
        for i in range(0, l):
            if move == self.ordered_opponent_moves[i][0]:
                if self.ordered_opponent_moves[i][1] < value:
                    if l == i + 1:
                        self.ordered_opponent_moves[i] = (move, value)
                    else:
                        cond = True
                        for j in range(i + 1, l):
                            if self.ordered_opponent_moves[j][1] < value:
                                self.ordered_opponent_moves[j - 1] = self.ordered_opponent_moves[j]
                            else:
                                self.ordered_opponent_moves[j - 1] = (move, value)
                                cond = False
                                break
                        if cond:
                            self.ordered_opponent_moves[l - 1] = (move, value)
                    break
                else:
                    if 0 == i:
                        self.ordered_opponent_moves[i] = (move, value)
                    else:
                        cond = True
                        for j in range(0, i):
                            k = i - j
                            if self.ordered_opponent_moves[k - 1][1] > value:
                                self.ordered_opponent_moves[k] = self.ordered_opponent_moves[k - 1]
                            else:
                                self.ordered_opponent_moves[k] = (move, value)
                                cond = False
                                break
                        if cond:
                            self.ordered_opponent_moves[0] = (move, value)
                    break

    def print(self):
        b= self
        for y in range(0,8):
            print(b.tiles[y][0],b.tiles[y][1],b.tiles[y][2],b.tiles[y][3],b.tiles[y][4],b.tiles[y][5],b.tiles[y][6],b.tiles[y][7])
        print("")