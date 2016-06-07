import random
import sys

import numpy as np
from sklearn.cross_validation import train_test_split
from save_load_model import *

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.regularizers import l1, l2, activity_l1, activity_l2
from keras.utils.visualize_util import plot


def createModel(settings, createPlot):
    print("Building Model...")
    model = Sequential()

    if (settings.depth > 1):
        model.add(LSTM(settings.hiddenNodes, return_sequences=True, input_shape=(settings.sequence_size, settings.N_values)))
        model.add(Dropout(settings.dropoutAmount))
    else :
        model.add(LSTM(settings.hiddenNodes, return_sequences=False, input_shape=(settings.sequence_size, settings.N_values)))
        model.add(Dropout(settings.dropoutAmount))

    for i in range(1, settings.depth-1):
        model.add(LSTM(settings.hiddenNodes, return_sequences=True))
        model.add(Dropout(settings.dropoutAmount))

    if (settings.depth > 1):
        model.add(LSTM(settings.hiddenNodes, return_sequences=False))
        model.add(Dropout(settings.dropoutAmount))

    
    if (settings.l1Amount > 0):
        model.add(Dense(settings.N_values, W_regularizer=l1(settings.l1Amount)))
    elif settings.l2Amount > 0:
        model.add(Dense(settings.N_values, W_regularizer=l2(settings.l2Amount)))
    else:
        model.add(Dense(settings.N_values))
    
    model.add(Activation(settings.activation))
    model.compile(loss=settings.lossType, optimizer=settings.optimizer)

    settings.filename = settings.activation + "_" + settings.trainingset + "_nodes" + str(settings.hiddenNodes) +"_depth" + str(settings.depth) + "_seq" + str(settings.sequence_size) + "_drop" + str(settings.dropoutAmount) + "_L1r" + str(settings.l1Amount) + "_L2r" + str(settings.l2Amount) 
    save_model_scratch(model, settings.filename, 0, False)
    
    with open('/var/scratch/jvranken/models/' + settings.filename + '/model_settings.txt', 'w') as settingsFile:
        for (setting, value) in vars(settings).items():
            settingsFile.write(setting + ': ' + str(value) + '\n')

    if createPlot:
        plot(model, to_file='/var/scratch/jvranken/models/' + settings.filename + '/model_layout.png', show_shapes=True)

    return model


#
# # build a 2 stacked LSTM
# print("Building Model...")
# model = Sequential()
# model.add(LSTM(hiddenNodes, return_sequences=True, input_shape=(sequence_size, N_values)))
# model.add(Dropout(dropoutAmount))
# model.add(LSTM(hiddenNodes, return_sequences=True))
# model.add(Dropout(dropoutAmount))
# model.add(LSTM(hiddenNodes, return_sequences=True))
# model.add(Dropout(dropoutAmount))
# model.add(LSTM(hiddenNodes, return_sequences=True))
# model.add(Dropout(dropoutAmount))
# model.add(LSTM(hiddenNodes, return_sequences=False))
# model.add(Dense(N_values, W_regularizer=l1(l1Amount)))
# model.add(Activation('linear'))
# model.compile(loss='mean_squared_error', optimizer='rmsprop')
#



