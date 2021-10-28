from copy import deepcopy
import tensorflow as tf
from tensorflow.keras.datasets import boston_housing
from tensorflow.keras.layers import Activation, Add, BatchNormalization, Conv2D, Dense, GlobalAveragePooling2D, Input, concatenate, Flatten, Dropout, Lambda
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler, LambdaCallback, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
#from keras.layers.advanced_activations import LeakyReLU
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import plot_model
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
from random import randrange
import subprocess
import datetime
import os

inf = 10000000.0

min_n_stones = 4 + 10
max_n_stones = 4 + 20
game_num = 10000 #117000
test_ratio = 0.1
n_epochs = 200
one_board_num = 2


line2_idx = [[8, 9, 10, 11, 12, 13, 14, 15], [1, 9, 17, 25, 33, 41, 49, 57], [6, 14, 22, 30, 38, 46, 54, 62], [48, 49, 50, 51, 52, 53, 54, 55]] # line2
for pattern in deepcopy(line2_idx):
    line2_idx.append(list(reversed(pattern)))

line3_idx = [[16, 17, 18, 19, 20, 21, 22, 23], [2, 10, 18, 26, 34, 42, 50, 58], [5, 13, 21, 29, 37, 45, 53, 61], [40, 41, 42, 43, 44, 45, 46, 47]]
for pattern in deepcopy(line3_idx):
    line3_idx.append(list(reversed(pattern)))

line4_idx = [[24, 25, 26, 27, 28, 29, 30, 31], [3, 11, 19, 27, 35, 43, 51, 59], [4, 12, 20, 28, 36, 44, 52, 60], [32, 33, 34, 35, 36, 37, 38, 39]]
for pattern in deepcopy(line4_idx):
    line4_idx.append(list(reversed(pattern)))

diagonal5_idx = [[4, 11, 18, 25, 32], [24, 33, 42, 51, 60], [59, 52, 45, 38, 31], [39, 30, 21, 12, 3]]
for pattern in deepcopy(diagonal5_idx):
    diagonal5_idx.append(list(reversed(pattern)))

diagonal6_idx = [[5, 12, 19, 26, 33, 40], [16, 25, 34, 43, 52, 61], [58, 51, 44, 37, 30, 23], [47, 38, 29, 20, 11, 2]]
for pattern in deepcopy(diagonal6_idx):
    diagonal6_idx.append(list(reversed(pattern)))

diagonal7_idx = [[1, 10, 19, 28, 37, 46, 55], [48, 41, 34, 27, 20, 13, 6], [62, 53, 44, 35, 26, 17, 8], [15, 22, 29, 36, 43, 50, 57]]
for pattern in deepcopy(diagonal7_idx):
    diagonal7_idx.append(list(reversed(pattern)))

diagonal8_idx = [[0, 9, 18, 27, 36, 45, 54, 63], [0, 9, 18, 27, 36, 45, 54, 63], [7, 14, 21, 28, 35, 42, 49, 56], [7, 14, 21, 28, 35, 42, 49, 56]]
for pattern in deepcopy(diagonal8_idx):
    diagonal8_idx.append(list(reversed(pattern)))

edge_2x_idx = [[9, 0, 1, 2, 3, 4, 5, 6, 7, 14], [9, 0, 8, 16, 24, 32, 40, 48, 56, 49], [49, 56, 57, 58, 59, 60, 61, 62, 63, 54], [54, 63, 55, 47, 39, 31, 23, 15, 7, 14]]
for pattern in deepcopy(edge_2x_idx):
    edge_2x_idx.append(list(reversed(pattern)))

triangle_idx = [
    [0, 1, 2, 3, 8, 9, 10, 16, 17, 24], [0, 8, 16, 24, 1, 9, 17, 2, 10, 3], 
    [7, 6, 5, 4, 15, 14, 13, 23, 22, 31], [7, 15, 23, 31, 6, 14, 22, 5, 13, 4], 
    [63, 62, 61, 60, 55, 54, 53, 47, 46, 39], [63, 55, 47, 39, 62, 54, 46, 61, 53, 60],
    [56, 57, 58, 59, 48, 49, 50, 40, 41, 32], [56, 48, 40, 32, 57, 49, 41, 58, 50, 59]
]

corner25_idx = [
    [0, 1, 2, 3, 4, 8, 9, 10, 11, 12],[0, 8, 16, 24, 32, 1, 9, 17, 25, 33],
    [7, 6, 5, 4, 3, 15, 14, 13, 12, 11],[7, 15, 23, 31, 39, 6, 14, 22, 30, 38],
    [56, 57, 58, 59, 60, 48, 49, 50, 51, 52],[56, 48, 40, 32, 24, 57, 49, 41, 33, 25],
    [63, 62, 61, 60, 59, 55, 54, 53, 52, 51],[63, 55, 47, 39, 31, 62, 54, 46, 38, 30]
]


pattern_idx = [line2_idx, line3_idx, line4_idx, diagonal5_idx, diagonal6_idx, diagonal7_idx, diagonal8_idx, edge_2x_idx, triangle_idx, corner25_idx]
#pattern_idx = [edge_2x_idx, triangle_idx]
all_data = [[] for _ in range(len(pattern_idx))]
all_labels = []

def calc_idx(board, patterns):
    res = []
    for pattern in patterns:
        tmp = 0
        for elem in pattern:
            tmp *= 3
            tmp += 0 if board[elem] == '0' else 1 if board[elem] == '1' else 2
        res.append(tmp)
    return res

def make_lines(board, patterns):
    res = []
    for _ in range(one_board_num):
        pattern = patterns[randrange(0, 8)]
        #for pattern in patterns:
        tmp = []
        for elem in pattern:
            tmp.append(1.0 if board[elem] == '0' else 0.0)
        for elem in pattern:
            tmp.append(1.0 if board[elem] == '1' else 0.0)
        res.append(tmp)
    return res

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

def collect_data(num):
    global all_data, all_labels
    try:
        with open('data_stones/' + digit(num, 7) + '.txt', 'r') as f:
            data = list(f.read().splitlines())
    except:
        print('cannot open')
        return
    for datum in data:
        board, score = datum.split()
        if min_n_stones <= calc_n_stones(board) < max_n_stones:
            #score = float(score)
            score = float(score)
            score = 1.0 if score > 0.0 else -1.0 if score < 0.0 else 0.0
            '''
            for i in range(len(pattern_idx)):
                lines = make_lines(board, pattern_idx[i])
                all_data[i].extend(lines)
            for _ in range(8):
                all_labels.append(score)
            '''
            for i in range(len(pattern_idx)):
                lines = make_lines(board, pattern_idx[i])
                for line in lines:
                    all_data[i].append(line)
            for _ in range(one_board_num):
                all_labels.append(score)
            

def LeakyReLU(x):
    return tf.math.maximum(0.01 * x, x)

y_all = None
x = [None for _ in range(len(pattern_idx))]
ys = []
names = ['line2', 'line3', 'line4', 'diagonal5', 'diagonal6', 'diagonal7', 'diagonal8', 'edge2X', 'triangle', 'corner25']
#names = ['edge2x', 'triangle']
for i in range(len(pattern_idx)):
    x[i] = Input(shape=(len(pattern_idx[i][0]) * 2), name=names[i] + '_in')
    y = Dense(16)(x[i])
    y = Lambda(lambda xx: LeakyReLU(xx))(y)
    y = Dense(16)(y)
    y = Lambda(lambda xx: LeakyReLU(xx))(y)
    y = Dense(1, name=names[i] + '_out')(y)
    ys.append(y)
y_all = Add()(ys)
model = Model(inputs=x, outputs=y_all)
model.summary()
plot_model(model, to_file='model.png', show_shapes=True)

for i in trange((game_num + 999) // 1000):
    collect_data(i)
len_data = len(all_labels)
print(len_data)
all_data = [np.array(arr) for arr in all_data]
all_labels = np.array(all_labels)

n_train_data = int(len_data * (1.0 - test_ratio))
n_test_data = int(len_data * test_ratio)

train_data = [arr[0:n_train_data] for arr in all_data]
train_labels = all_labels[0:n_train_data]
test_data = [arr[n_train_data:len_data] for arr in all_data]
test_labels = all_labels[n_train_data:len_data]

model.compile(loss='mse', metrics='mae', optimizer='adam')
print(model.evaluate(test_data, test_labels))
early_stop = EarlyStopping(monitor='val_loss', patience=5)
model_checkpoint = ModelCheckpoint(filepath=os.path.join('learned_data/models', 'model_{epoch:02d}_{val_loss:.5f}.h5'), monitor='val_loss', verbose=1)
history = model.fit(train_data, train_labels, epochs=n_epochs, validation_data=(test_data, test_labels), callbacks=[early_stop, model_checkpoint])

now = datetime.datetime.today()
print(str(now.year) + digit(now.month, 2) + digit(now.day, 2) + '_' + digit(now.hour, 2) + digit(now.minute, 2))
model.save('learned_data/model.h5')

for key in ['loss', 'val_loss']:
    plt.plot(history.history[key], label=key)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc='best')
plt.savefig('graph/loss.png')
plt.clf()