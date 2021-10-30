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

def LeakyReLU(x):
    return tf.math.maximum(0.01 * x, x)


inf = 10000000.0

min_n_stones = 4 + 50
max_n_stones = 4 + 60
game_num = 22000
test_ratio = 0.1
n_epochs = 200
n_input = 4

all_data = []
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
        with open('data_additional/' + digit(num, 7) + '.txt', 'r') as f:
            data = list(f.read().splitlines())
    except:
        print('cannot open')
        return
    for datum in data:
        board, result, v1, v2, v3, v4, v5, v6 = datum.split()
        if min_n_stones <= calc_n_stones(board) < max_n_stones:
            v1 = float(v1)
            v2 = float(v2) / 30
            v3 = float(v3) / 30
            v4 = float(v4) / 30
            v5 = float(v5) / 30
            v6 = float(v6) / 30
            result = float(result)
            all_data.append([v1, v2, v3, v4])
            all_labels.append(result)


x = Input(shape=(n_input))
y = Dense(16)(x)
y = LeakyReLU(y)
y = Dense(1)(y)

model = Model(inputs=x, outputs=y)
model.summary()
#plot_model(model, to_file='model_all_data.png', show_shapes=True)


for i in trange((game_num + 999) // 1000):
    collect_data(i)
len_data = len(all_labels)
print(len_data)
all_data = np.array(all_data)
all_labels = np.array(all_labels)

n_train_data = int(len_data * (1.0 - test_ratio))
n_test_data = int(len_data * test_ratio)

train_data = all_data[0:n_train_data]
train_labels = all_labels[0:n_train_data]
test_data = all_data[n_train_data:len_data]
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