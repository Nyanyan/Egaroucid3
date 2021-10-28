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


line2_idx = [[8, 9, 10, 11, 12, 13, 14, 15], [48, 49, 50, 51, 52, 53, 54, 55], [1, 9, 17, 25, 33, 41, 49, 57], [6, 14, 22, 30, 38, 46, 54, 62]] # line2
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

diagonal8_idx = [[0, 9, 18, 27, 36, 45, 54, 63], [7, 14, 21, 28, 35, 42, 49, 56]]
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

def make_lines(board, patterns):
    res = []
    for pattern in patterns:
        tmp = []
        for elem in pattern:
            tmp.append(1.0 if board[elem] == '0' else 0.0)
        for elem in pattern:
            tmp.append(1.0 if board[elem] == '1' else 0.0)
        res.append(tmp)
    return res 


model = load_model('learned_data/30_40.h5')
hidden = Model(inputs=model.input, outputs=model.get_layer('line2_add').output)

board = '...0000.0.0001..001011..000101..001001...100011.1.1111......11..'
count = 60
for i in board:
    count -= i == '.'
print(count)

#in_arr = [make_lines(board, pattern_idx[i]) for i in range(len(pattern_idx))]
#in_arr = [np.array(i) for i in in_arr]

in_arr = []
for i in range(len(pattern_idx)):
    in_arr.extend(make_lines(board, pattern_idx[i]))
in_arr = [np.array([i]) for i in in_arr]

prediction = model.predict(in_arr)
print(prediction)
print(hidden.predict(in_arr))