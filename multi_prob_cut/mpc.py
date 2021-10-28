from random import randint
import subprocess
from tqdm import trange
from time import sleep
import statistics

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

evaluate = subprocess.Popen('./ai.out'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
sleep(1)

vhs = []
vds = []

vh_vd = []


def collect_data(num):
    global vhs, vds, vh_vd
    try:
        with open('data_player/' + digit(num, 7) + '.txt', 'r') as f:
            data = list(f.read().splitlines())
    except:
        print('cannot open')
        return
    for datum, _ in zip(data[:1000], trange(len(data[:1000]))):
        board, player = datum.split()
        if min_n_stones <= calc_n_stones(board):
            depth = randint(4, 10)
            board_proc = player + '\n' + str(int(depth / 4)) + '\n' + str(int(depth)) + '\n'
            for i in range(hw):
                for j in range(hw):
                    board_proc += board[i * hw + j]
                board_proc += '\n'
            #print(board_proc)
            evaluate.stdin.write(board_proc.encode('utf-8'))
            evaluate.stdin.flush()
            vd, vh = [float(i) for i in evaluate.stdout.readline().decode().strip().split()]
            #print(score)
            vhs.append(vh)
            vds.append(vd)

for i in range(1):
    collect_data(i)
print(vhs[:10])
print(vds[:10])
sm_vh = sum([abs(i) for i in vhs])
sm_vd = sum([abs(i) for i in vds])
print('sum', sm_vh, sm_vd)
a = sm_vh / sm_vd
vh_vd = [vhs[i] - a * vds[i] for i in range(len(vhs))]
sd = statistics.stdev(vh_vd)
print(a, sd)
evaluate.kill()