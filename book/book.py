import subprocess
from tqdm import trange
from copy import deepcopy

hw = 8
hw2 = 64
board_index_num = 38
dy = [0, 1, 0, -1, 1, 1, -1, -1]
dx = [1, 0, -1, 0, 1, -1, 1, -1]

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

all_chars = [
    '!', '#', '$', '&', "'", '(', ')', '*', 
    '+', ',', '-', '.', '/', '0', '1', '2', 
    '3', '4', '5', '6', '7', '8', '9', ':', 
    ';', '<', '=', '>', '?', '@', 'A', 'B', 
    'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '[', ']', '^', '_', '`', 'a', 'b', 'c', 
    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

print(''.join(all_chars[:hw2]))

char_dict = {}
for i in range(hw2):
    char_dict[all_chars[i]] = i

def to_str_record(record):
    res = ''
    for coord in record:
        res += all_chars[coord]
    return res

def to_str_record_human(record):
    res = ''
    for coord in record:
        res += chr(coord % hw + ord('A'))
        res += str(coord // hw + 1)
    return res

def empty(grid, y, x):
    return grid[y][x] == -1 or grid[y][x] == 2

def inside(y, x):
    return 0 <= y < hw and 0 <= x < hw

def check(grid, player, y, x):
    res_grid = [[False for _ in range(hw)] for _ in range(hw)]
    res = 0
    for dr in range(8):
        ny = y + dy[dr]
        nx = x + dx[dr]
        if not inside(ny, nx):
            continue
        if empty(grid, ny, nx):
            continue
        if grid[ny][nx] == player:
            continue
        #print(y, x, dr, ny, nx)
        plus = 0
        flag = False
        for d in range(hw):
            nny = ny + d * dy[dr]
            nnx = nx + d * dx[dr]
            if not inside(nny, nnx):
                break
            if empty(grid, nny, nnx):
                break
            if grid[nny][nnx] == player:
                flag = True
                break
            #print(y, x, dr, nny, nnx)
            plus += 1
        if flag:
            res += plus
            for d in range(plus):
                nny = ny + d * dy[dr]
                nnx = nx + d * dx[dr]
                res_grid[nny][nnx] = True
    return res, res_grid

def pot_canput_line(arr):
    res_p = 0
    res_o = 0
    for i in range(len(arr) - 1):
        if arr[i] == -1 or arr[i] == 2:
            if arr[i + 1] == 0:
                res_o += 1
            elif arr[i + 1] == 1:
                res_p += 1
    for i in range(1, len(arr)):
        if arr[i] == -1 or arr[i] == 2:
            if arr[i - 1] == 0:
                res_o += 1
            elif arr[i - 1] == 1:
                res_p += 1
    return res_p, res_o

class reversi:
    def __init__(self):
        self.grid = [[-1 for _ in range(hw)] for _ in range(hw)]
        self.grid[3][3] = 1
        self.grid[3][4] = 0
        self.grid[4][3] = 0
        self.grid[4][4] = 1
        self.player = 0 # 0: 黒 1: 白
        self.nums = [2, 2]

    def move(self, y, x):
        plus, plus_grid = check(self.grid, self.player, y, x)
        if (not empty(self.grid, y, x)) or (not inside(y, x)) or not plus:
            print('Please input a correct move')
            return 1
        self.grid[y][x] = self.player
        for ny in range(hw):
            for nx in range(hw):
                if plus_grid[ny][nx]:
                    self.grid[ny][nx] = self.player
        self.nums[self.player] += 1 + plus
        self.nums[1 - self.player] -= plus
        self.player = 1 - self.player
        return 0
    
    def check_pass(self):
        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == 2:
                    self.grid[y][x] = -1
        res = True
        for y in range(hw):
            for x in range(hw):
                if not empty(self.grid, y, x):
                    continue
                plus, _ = check(self.grid, self.player, y, x)
                if plus:
                    res = False
                    self.grid[y][x] = 2
        if res:
            #print('Pass!')
            self.player = 1 - self.player
        return res

    def output(self):
        print('  ', end='')
        for i in range(hw):
            print(chr(ord('a') + i), end=' ')
        print('')
        for y in range(hw):
            print(str(y + 1) + ' ', end='')
            for x in range(hw):
                print('○' if self.grid[y][x] == 0 else '●' if self.grid[y][x] == 1 else '* ' if self.grid[y][x] == 2 else '. ', end='')
            print('')
    
    def output_file(self):
        res = ''
        for y in range(hw):
            for x in range(hw):
                res += '*' if self.grid[y][x] == 0 else 'O' if self.grid[y][x] == 1 else '-'
        res += ' *'
        return res

    def end(self):
        if min(self.nums) == 0:
            return True
        res = True
        for y in range(hw):
            for x in range(hw):
                if self.grid[y][x] == -1 or self.grid[y][x] == 2:
                    res = False
        return res
    
    def judge(self):
        if self.nums[0] > self.nums[1]:
            #print('Black won!', self.nums[0], '-', self.nums[1])
            return 0
        elif self.nums[1] > self.nums[0]:
            #print('White won!', self.nums[0], '-', self.nums[1])
            return 1
        else:
            #print('Draw!', self.nums[0], '-', self.nums[1])
            return -1


n_eval = 12

depth = 15

def get_next_move(grids, player, mx_value):
    global evaluates
    evaluates = [subprocess.Popen('./ai.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) for _ in range(n_eval)]
    res = []
    for i, grid in zip(trange(len(grids)), grids):
        board = str(player) + '\n' + str(depth) + '\n'
        for y in range(hw):
            for x in range(hw):
                board += '0' if grid[y][x] == 0 else '1' if grid[y][x] == 1 else '.'
            board += '\n'
        evaluates[i % n_eval].stdin.write(board.encode('utf-8'))
        evaluates[i % n_eval].stdin.flush()
        if i % n_eval == n_eval - 1:
            for j in range(n_eval):
                try:
                    val, pol = evaluates[j].stdout.readline().decode().strip().split()
                    val = float(val)
                    pol = int(pol)
                    if abs(val) < mx_value:
                        res.append(pol)
                    else:
                        res.append(-1)
                except:
                    print(board)
                    res.append(-1)
    for j in range(len(grids) % n_eval):
        try:
            val, pol = evaluates[j].stdout.readline().decode().strip().split()
            val = float(val)
            pol = int(pol)
            if abs(val) < mx_value:
                res.append(pol)
            else:
                res.append(-1)
        except:
            print(board)
            res.append(-1)
    for i in range(n_eval):
        evaluates[i].kill()
    return res

def calc_mx(turn):
    if turn < 5:
        return 1000.0
    return 0.3 #10.0 / (1.0 + turn) + 3.0

book = {}
records = [[[37]] for _ in range(2)]
while True:
    for player in reversed(range(2)):
        grids = []
        for record in records[player]:
            rv = reversi()
            for mov in record:
                y = mov // hw
                x = mov % hw
                rv.move(y, x)
                rv.check_pass()
                if rv.check_pass():
                    break
            else:
                if rv.player == player:
                    grids.append([[i for i in record], [[i for i in j] for j in rv.grid]])
                else:
                    grid_bak = [[i for i in j] for j in rv.grid]
                    player_bak = rv.player
                    for y in range(hw):
                        for x in range(hw):
                            if rv.grid[y][x] == 2:
                                rv.move(y, x)
                                rv.check_pass()
                                if not rv.check_pass():
                                    if rv.player == player:
                                        n_record = [i for i in record]
                                        n_record.append(y * hw + x)
                                        grids.append([n_record, [[i for i in j] for j in rv.grid]])
                                rv.grid = [[i for i in j] for j in grid_bak]
                                rv.player = player_bak
        mx_val = calc_mx(len(records[player][0]))
        next_moves = get_next_move([i[1] for i in grids], player, mx_val)
        records[player] = []
        for i in range(len(grids)):
            if next_moves[i] != -1:
                book[to_str_record(grids[i][0])] = next_moves[i]
                grids[i][0].append(next_moves[i])
                records[player].append([i for i in grids[i][0]])
        #print(records)
        print(len(records[player][0]), len(book.keys()), len(records[player]), mx_val)

        with open('learned_data/book_' + str(len(records[player][0])) + '.txt', 'w') as f:
            for record in book.keys():
                f.write(record[1:] + ' ' + all_chars[book[record]])



