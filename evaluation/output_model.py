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
import sys

def LeakyReLU(x):
    return tf.math.maximum(0.01 * x, x)

def get_layer_index(model, layer_name, not_found=None):
    for i, l in enumerate(model.layers):
        if l.name == layer_name:
            return i
    return not_found

model = load_model('learned_data/' + sys.argv[1])

names = ['dense', 'dense_1', 'edge2x_out', 'dense_2', 'dense_3', 'triangle_out']

with open('learned_data/' + sys.argv[2], 'w') as f:
    for name in names:
        i = get_layer_index(model, name)
        try:
            #print(i, model.layers[i])
            dammy = model.layers[i]
            j = 0
            while True:
                try:
                    print(model.layers[i].weights[j].shape)
                    if len(model.layers[i].weights[j].shape) == 4:
                        for ll in range(model.layers[i].weights[j].shape[3]):
                            for kk in range(model.layers[i].weights[j].shape[2]):
                                for jj in range(model.layers[i].weights[j].shape[1]):
                                    for ii in range(model.layers[i].weights[j].shape[0]):
                                        f.write('{:.14f}'.format(model.layers[i].weights[j].numpy()[ii][jj][kk][ll]) + '\n')
                    elif len(model.layers[i].weights[j].shape) == 2:
                        for ii in range(model.layers[i].weights[j].shape[0]):
                            for jj in range(model.layers[i].weights[j].shape[1]):
                                f.write('{:.14f}'.format(model.layers[i].weights[j].numpy()[ii][jj]) + '\n')
                    elif len(model.layers[i].weights[j].shape) == 1:
                        for ii in range(model.layers[i].weights[j].shape[0]):
                            f.write('{:.14f}'.format(model.layers[i].weights[j].numpy()[ii]) + '\n')
                    j += 1
                except:
                    break
        except:
            break