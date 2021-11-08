import subprocess
from tqdm import trange
from time import sleep
import sys

inf = 10000000.0

hw = 8
min_n_stones = 4 + 10

def digit(n, r):
    n = str(n)
    l = len(n)
    for i in range(r - l):
        n = '0' + n
    return n

def calc_n_stones(board):
    res = 0
    for elem in board:
        res += int(elem != '.')
    return res

evaluate = subprocess.Popen('./ai_add.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
sleep(1)
def collect_data(num):
    global all_data, all_labels
    new_data = []
    try:
        with open('data_player/' + digit(num, 7) + '.txt', 'r') as f:
            data = list(f.read().splitlines())
    except:
        print('cannot open')
        return
    for datum, _ in zip(data, trange(len(data))):
        board, player, result = datum.split()
        if min_n_stones <= calc_n_stones(board):
            board_proc = player + '\n'
            for i in range(hw):
                for j in range(hw):
                    board_proc += board[i * hw + j]
                board_proc += '\n'
            #print(board_proc)
            evaluate.stdin.write(board_proc.encode('utf-8'))
            evaluate.stdin.flush()
            vals = list(evaluate.stdout.readline().decode().strip().split())
            #print(score)
            tmp = [board, result]
            tmp.extend(vals)
            new_data.append(tmp)
    return new_data

for i in range(int(sys.argv[1]) // 100):
    try:
        data = collect_data(i)
        with open('data_additional/' + digit(i, 7) + '.txt', 'w') as f:
            for datum in data:
                f.write(' '.join(datum) + '\n')
    except:
        continue

evaluate.kill()