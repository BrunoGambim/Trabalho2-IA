def copy_opt_board(board):
    b = Opt_Board(board.player)
    b.player = board.player
    b.opponent = board.opponent

    b.piece_count = [board.piece_count[1], board.piece_count[0], board.piece_count[2]]
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
    b.init_moves()

    return b

class Opt_Board(object):
    BLACK = 0
    WHITE = 1
    EMPTY = 2

    CHAR_BLACK = 'B'
    CHAR_WHITE = 'W'
    CHAR_EMPTY = '.'

    OPPOSITE_DIRECTIONS = [1, 0, 3, 2, 7, 6, 5, 4]
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]

    def __init__(self, player):
        self.tiles = [[self.EMPTY] * 8 for i in range(8)]
        self.player_moves = {}
        self.opponent_moves = {}
                    
    def init_moves(self) -> None:
        for y in range(0,8):
            for x in range(0,8):
                self.init_moves_for_tile(x, y, self.tiles[y][x])


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
                        self.player_moves[(x1, y1)][1][self.OPPOSITE_DIRECTIONS[direction]] = counter
                        self.player_moves[(x1, y1)] = (self.player_moves[(x1, y1)][0] + counter, self.player_moves[(x1, y1)][1], self.player_moves[(x1, y1)][2])
                    else:
                        self.player_moves[(x1, y1)] = (counter, {self.OPPOSITE_DIRECTIONS[direction]: counter}, -1)

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
                        self.opponent_moves[(x1, y1)][1][self.OPPOSITE_DIRECTIONS[direction]] = counter
                        self.opponent_moves[(x1, y1)] = (self.opponent_moves[(x1, y1)][0] + counter, self.opponent_moves[(x1, y1)][1], self.opponent_moves[(x1, y1)][2])
                    else:
                        self.opponent_moves[(x1, y1)] = (counter, {self.OPPOSITE_DIRECTIONS[direction]: counter}, -1)

    def make_opponent_move(self, move, board_table):
        if self.opponent_moves[move][2] != -1:
            return board_table.get(self.opponent_moves[move][2])

        result = copy_opt_board(self)
        if move == None:
            result.init_moves()
            return result

        result.process_opponent_move(move, self.opponent_moves[move])

        boardId = result.boardId()
        self.opponent_moves[move] = (self.opponent_moves[move][0], self.opponent_moves[move][1], boardId)
        board_table.insert(boardId, result)
        return result

    def process_opponent_move(self, key, move):
        x , y = key[0], key[1]
        self.tiles[y][x] = self.opponent
        for direction in move[1].keys():
            x , y = key[0] + self.DIRECTIONS[direction][0], key[1] + self.DIRECTIONS[direction][1]
            while self.tiles[y][x] != self.opponent:
                self.tiles[y][x] = self.opponent
                x , y = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]
        self.init_moves()

    def make_player_move(self, move, board_table):
        if self.player_moves[move][2] != -1:
            return board_table.get(self.player_moves[move][2])

        result = copy_opt_board(self)
        if move == None:
            board.init_moves()
            return result

        result.process_player_move(move, self.player_moves[move])

        boardId = result.boardId()
        self.player_moves[move] = (self.player_moves[move][0], self.player_moves[move][1], result.boardId())
        board_table.insert(boardId, result)
        return result

    def process_player_move(self, key, move):
        x , y = key[0], key[1]
        self.tiles[y][x] = self.player
        for direction in move[1].keys():
            x , y = key[0] + self.DIRECTIONS[direction][0], key[1] + self.DIRECTIONS[direction][1]
            while self.tiles[y][x] != self.player:
                self.tiles[y][x] = self.player
                x , y = x + self.DIRECTIONS[direction][0], y + self.DIRECTIONS[direction][1]
        self.init_moves()
    
    def boardId(self):
        l0 = self.tiles[0][0]+self.tiles[0][1]*3+self.tiles[0][2]*9+self.tiles[0][3]*27+self.tiles[0][4]*81+self.tiles[0][5]*243+self.tiles[0][6]*729+self.tiles[0][7]*2187
        l1 = self.tiles[1][0]+self.tiles[1][1]*3+self.tiles[1][2]*9+self.tiles[1][3]*27+self.tiles[1][4]*81+self.tiles[1][5]*243+self.tiles[1][6]*729+self.tiles[1][7]*2187
        l2 = self.tiles[2][0]+self.tiles[2][1]*3+self.tiles[2][2]*9+self.tiles[2][3]*27+self.tiles[2][4]*81+self.tiles[2][5]*243+self.tiles[2][6]*729+self.tiles[2][7]*2187
        l3 = self.tiles[3][0]+self.tiles[3][1]*3+self.tiles[3][2]*9+self.tiles[3][3]*27+self.tiles[3][4]*81+self.tiles[3][5]*243+self.tiles[3][6]*729+self.tiles[3][7]*2187
        l4 = self.tiles[4][0]+self.tiles[4][1]*3+self.tiles[4][2]*9+self.tiles[4][3]*27+self.tiles[4][4]*81+self.tiles[4][5]*243+self.tiles[4][6]*729+self.tiles[4][7]*2187
        l5 = self.tiles[5][0]+self.tiles[5][1]*3+self.tiles[5][2]*9+self.tiles[5][3]*27+self.tiles[5][4]*81+self.tiles[5][5]*243+self.tiles[5][6]*729+self.tiles[5][7]*2187
        l6 = self.tiles[6][0]+self.tiles[6][1]*3+self.tiles[6][2]*9+self.tiles[6][3]*27+self.tiles[6][4]*81+self.tiles[6][5]*243+self.tiles[6][6]*729+self.tiles[6][7]*2187
        l7 = self.tiles[7][0]+self.tiles[7][1]*3+self.tiles[7][2]*9+self.tiles[7][3]*27+self.tiles[7][4]*81+self.tiles[7][5]*243+self.tiles[7][6]*729+self.tiles[7][7]*2187
        a = l0 + l1*2 + l2*4 + l3*8 + l4*16 + l5*32 + l6*64 + l7*128
        return (l0,l1,l2,l3,l4,l5,l6,l7)

    def legal_moves(self, color) -> set:
        if color == self.opponent:
            return self.opponent_moves.keys()
        else:
            return self.player_moves.keys()

    def print(self):
        b= self
        for y in range(0,8):
            print(b.tiles[y][0],b.tiles[y][1],b.tiles[y][2],b.tiles[y][3],b.tiles[y][4],b.tiles[y][5],b.tiles[y][6],b.tiles[y][7])
            #for x in range(0,8):
            #b.tiles[y][x] = board.tiles[y][x]
        print("")