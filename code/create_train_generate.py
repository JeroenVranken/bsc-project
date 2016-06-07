import random
import sys
from sklearn.cross_validation import train_test_split
import time

import numpy as np
import midi
from ModelSettings import *
from createModel import *
from midi_encoder import *
from save_load_model import *
from trainModel import *
from directory_iterator import getFilePaths
from generate_per_file import *
from generate_per_directory import *

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.regularizers import l1, activity_l1



#--------------------------Model settings-----------------------------------------

settings = ModelSettings()

settings.activation = 'linear'
settings.lossType = 'mean_squared_error'
settings.hiddenNodes = 512
settings.depth = 3
settings.dropoutAmount = 0.2
settings.l1Amount = 0.1
settings.l2Amount = 0
settings.batch_size = 900
settings.N_epochs = 1
settings.sequence_size = 64
settings.N_values = 128
settings.resolution = 8
settings.step = 1
# settings.directoryPath = '/home/jvranken/Disklavier/only_classical'
settings.directoryPath = '/home/jvranken/Disklavier/only_jazz'
settings.trainingset = 'classical_jazz'
settings.convertVelocity = False
settings.generate_length = 512
settings.modelType = 'normal'
settings.genres = False


# settings.filename = 'linear_only_classical_nodes512_depth3_seq64_drop0.2_L1r0.1_L2r0_ep10'
settings.filename = 'linear_only_classical_nodes512_depth3_seq64_drop0.2_L1r0.1_L2r0'
# settings.filename = 'linear_classical_jazz_nodes512_depth3_seq64_drop0.2_L1r0.1_L2r0'


# model = load_model_scratch(settings, batch=706, loadWeights=True)
model = load_model_scratch(settings, batch=991, loadWeights=True)
# model = load_model_scratch(settings, batch=1391, loadWeights=True)
# model.smoothDifference = 5
# print vars(settings)
# exit()


#------------------------------Training------------------------------------------------
# model = createModel(settings, createPlot=True)

# start = time.time()
# trainModelGenres(model, settings)
# end = time.time()
# print "training took %d second" % (end-start) 

# generate_per_directory(model, settings, '/home/jvranken/multiple/set3', smoothVelocities=True)
# reTrainModel(settings, epochs=10)
# 165-Satie Eric - Gymnopedie No-3.mid
# generate_per_file(model, settings, '/home/jvranken/single/moonlight/026-Beethoven - Moonlight Sonata Op-27 No-2 Mvt-1.mid', smoothVelocities=False)
generate_per_file(model, settings, '/home/jvranken/multiple/set4/blues.mid', smoothVelocities=False)
# generate_per_file(model, settings, '/home/jvranken/multiple/set4/melody.mid', smoothVelocities=True)
# generate_per_directory(model, settings, '/home/jvranken/multiple/set3', smoothVelocities=False)

# plot(model, to_file='model_layout' + settings.filename + '.png', show_shapes=True)

# filePaths = getFilePaths(settings.directoryPath, '.mid')
# print "total files: " + str(len(filePaths))



# # Training settings
# N_epochs = 20
# training_file_amount = 0
# model_batch_size = 240
# filePathIndex = 0



# # Load data dynamically, track length determines amount of tracks to use so memory doesn't overflow
# while (filePathIndex < (len(filePaths)-training_file_amount)):
	
# 	input_sequences = []
# 	next_values = []

# 	print("Loading files")
# 	while (len(input_sequences) < 100000):
	
# 		try:
# 			pattern = midi.read_midifile(filePaths[filePathIndex])
# 		except:
# 			print "Error while reading midi file:", filePaths[filePathIndex]
# 			for error in sys.exc_info():
# 				print error
# 		filePathIndex += 1

# 		midi_events, headerInfo, totalTicks = get_midi_events(pattern, settings.resolution)
# 		enc = midi_to_array(totalTicks, midi_events, settings.convertVelocity)

# 		# cut the corpus in semi-redundant sequences of sequence_size values
# 		for i in range(0, len(enc) - settings.sequence_size, settings.step):
# 		    input_sequences.append(enc[i: i + settings.sequence_size])
# 		    next_values.append(enc[i + settings.sequence_size])

# 		if (filePathIndex >= len(filePaths)-training_file_amount):
# 			break;

# 	print("Training model, " + ' nb sequences: '+ str(len(input_sequences)) + " batch:" +str(filePathIndex))
# 	print np.asarray(input_sequences).shape, np.asarray(next_values).shape

# 	model.fit(np.asarray(input_sequences), np.asarray(next_values), batch_size=model_batch_size, nb_epoch=N_epochs)

# 	save_model_scratch(model, settings.filename, str(filePathIndex), True)

# print "Generating"


