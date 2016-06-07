
import random
import sys

import numpy as np
from sklearn.cross_validation import train_test_split

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

import midi

from directory_iterator import getFilePaths
from proper_encoder_decoder import *

def save_model(model, filename):
	print("Saving model")
	json_string = model.to_json()
	open('models/' + filename + '.json', 'w').write(json_string)

	weights = model.get_weights()
	np.save('models/' + filename + '_weights', weights)

def load_model(filename):
	print("Loading model")
	model = model_from_json(open('models/' + filename + '.json').read())
	# weights = np.load('models/' + filename + '_weights.npy')
	# model.set_weights(weights)

	print("Compiling model")
	model.compile(loss=lossType, optimizer='rmsprop')
	return model



# MIDI settings
smallest_timestep = 32 # 1/smallest_timestep

resolution = smallest_timestep / 4


# model settings
sequence_size = 128
step = 1
diversity = 0.5
N_epochs = 1
N_values = 128
lossType = 'mean_squared_error'

# modelFilename = 'linear_nodes512_depth3_sequence32_L1(0.01)'

# name = modelFilename + "_only_classical"
# # name = 'linear_nodes256_sequences128_L1(0.01)_only_classical'
# modelName = name + "_" + str(N_epochs) + "epochs"


# Get all filenames
# directoryPath = '/home/jvranken/Disklavier'
onlyClassical = '/home/jvranken/Disklavier/only_classical'
directoryPath = onlyClassical

filePaths = getFilePaths(directoryPath, '.mid')
print "total files: " + str(len(filePaths))

training_file_amount = 0

# model_batch_size = 3000



# Divide into train and test set
# train, test = train_test_split(filePaths, test_size = 0.95)


# model = load_model(modelFilename)


filePathIndex = 804


# Load data dynamically, track length determines amount of tracks to use so memory doesn't overflow
while (filePathIndex < len(filePaths)-training_file_amount):
	input_sequences = []
	next_values = []
	print("Loading files")
	# while (len(input_sequences) < 240000):
	try:
		pattern = midi.read_midifile(filePaths[filePathIndex])
	except:
		print "Error while reading midi file:", filePaths[filePathIndex]
		for error in sys.exc_info():
			print error
	filePathIndex += 1

	midi_events, headerInfo, totalTicks = get_midi_events(pattern, resolution)
	# resolution = pattern.resolution
	enc = midi_to_array(totalTicks, midi_events, False)
	np.save('input_sequences/testing/' + filePaths[filePathIndex].split('/')[-1], enc[0:sequence_size])
	# 	continue

	# 	# cut the corpus in semi-redundant sequences of sequence_size values
	# 	for i in range(0, len(enc) - sequence_size, step):
	# 	    input_sequences.append(enc[i: i + sequence_size])
	# 	    next_values.append(enc[i + sequence_size])
		
	# 	if (filePathIndex >= len(filePaths)-training_file_amount):
	# 		break;

	
	# print("Training model, " + ' nb sequences: '+ str(len(input_sequences)) + " batch:" +str(filePathIndex))
	# # print('nb sequences:', len(input_sequences))
	# # print "batch", filePathIndex
	# modelName = name + "_" + str(N_epochs) + "epochs_" + "_batch" + str(filePathIndex)

	
	# model.fit(np.asarray(input_sequences), np.asarray(next_values), batch_size=model_batch_size, nb_epoch=N_epochs)

	# save_model(model, modelName)


# # Load data in batches
# for firstIndex in range(0, len(filePaths)-training_file_amount, file_batch_size):
	
# 	print "batch", firstIndex
# 	modelName = name + "_" + str(N_epochs) + "epochs_" + str(sequence_size) + "sequence_size" + "_batch" + str(firstIndex)
# 	input_sequences = []
# 	next_values = []

# 	print("Creating training examples")
# 	for i in range(firstIndex, firstIndex + file_batch_size):
# 		try:
# 			pattern = midi.read_midifile(filePaths[i])
# 		except:
# 		    print "Error while reading midi file:", sys.exc_info()[0]

# 		midi_events, headerInfo, totalTicks = get_midi_events(pattern, resolution)
# 		# resolution = pattern.resolution
# 		enc = midi_to_array(totalTicks, midi_events)

		
# 		# cut the corpus in semi-redundant sequences of sequence_size values
# 		for i in range(0, len(enc) - sequence_size, step):
# 		    input_sequences.append(enc[i: i + sequence_size])
# 		    next_values.append(enc[i + sequence_size])

# 	print('nb sequences:', len(input_sequences))

	# transform data into matrices
	# X = np.zeros((len(input_sequences), sequence_size, N_values), dtype='float16')
	# y = np.zeros((len(input_sequences), N_values), dtype='float16')

	# print "Created zero matrices"

	# print("transforming into matrices")
	# for i, sequence in enumerate(input_sequences):
	# 	# print("sequence: " + str(i) + '/' + str(len(input_sequences)))
	# 	for t, tick in enumerate(sequence):
	# 	# Convert to values between 0 and 1
	# 		X[i, t] = input_sequences[i][t] / N_values
	# 	y[i] = next_values[i] / N_values

	# prediction_input = X[:1]
	# np.save('prediction_input_batch' + str(firstIndex) , prediction_input)

	# print X.shape
	# print y.shape
	# sys.exit()


	# # build a 2 stacked LSTM
	# print("Building Model...")
	# model = Sequential()
	# model.add(LSTM(512, return_sequences=True, input_shape=(sequence_size, N_values)))
	# model.add(Dropout(0.2))
	# model.add(LSTM(512, return_sequences=False))
	# model.add(Dropout(0.2))
	# model.add(Dense(N_values))
	# model.add(Activation('softmax'))
	# model.compile(loss='categorical_crossentropy', optimizer='rmsprop')


	# print("Training model")
	# model.fit(np.asarray(input_sequences), np.asarray(next_values), batch_size=model_batch_size, nb_epoch=N_epochs)

	# save_model(model, modelName)
	# sys.exit()


