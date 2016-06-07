import sys
import os

import numpy as np
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import model_from_json
# from proper_encode_decode import midi_to_array, get_midi_events, array_to_midi
from midi_encoder import *

import midi

from directory_iterator import getFilePaths

#-------------------------------------Functions--------------------------------

def generate_next(input_sequence, model, settings):
	prediction = model.predict(input_sequence, batch_size=settings.batch_size)
	next_input = np.concatenate((input_sequence[0][1:], prediction), axis = 0).reshape([1, settings.sequence_size, settings.N_values])
	return prediction, next_input

# def smoothVelocities()

#-------------------------------------Code-------------------------------------


def generate_per_directory(model, settings, directory, smoothVelocities):


	filePaths = getFilePaths(directory, '.mid')
	for singleFile in filePaths:

		# Create empty arrays
		prediction_input = np.zeros((1, settings.sequence_size, settings.N_values), int)
		generated_encoding = np.zeros((settings.sequence_size + settings.generate_length, settings.N_values), dtype=int)

		# Read file and convert to encoding
		pattern = midi.read_midifile(singleFile)
		midi_events, headerInfo, totalTicks = get_midi_events(pattern, settings.resolution)
		encoded_input = midi_to_array(settings, totalTicks, midi_events)	

		# Put song in input
		prediction_input[0] = encoded_input[0:settings.sequence_size]

		# Setup I/O
		if smoothVelocities:
			smooth = 'smooth'
		else:
			smooth = ''
		output_file = 'generations/' + settings.filename + "/" + str(singleFile.split('/')[-1]) + "_l" + str(settings.generate_length) + smooth + ".mid"
		# count = 0
		# while os.path.exists(output_file):
		# 	output_file = 'generations/' + settings.filename + "/" + settings.filename + "_" + str(settings.generate_length) + "_" + str(count) + ".mid"
		# 	count += 1

		if not os.path.exists('generations/' + settings.filename):
		    os.makedirs('generations/' + settings.filename)
		
		# Put input sequence in file
		generated_encoding[0:settings.sequence_size] = prediction_input[0:settings.sequence_size]

		# Generation loop
		print("Generating")
		for i in range(settings.generate_length):
			if (i % 100) == 0:
				print "generating %d/%d" % (i, settings.generate_length)
			
			predicted_tick, next_input = generate_next(prediction_input, model, settings)
			generated_encoding[i + settings.sequence_size] = predicted_tick
			prediction_input = next_input

		# Post processing
		for t, tick in enumerate(generated_encoding):
			for p, val in enumerate(tick):
				if (val <= 2):
					generated_encoding[t][p] = 0 # remove low velocity notes
				elif (val > 128):
					generated_encoding[t][p] = 128 # clip high velocity notes
				elif (t != 0) and (abs(generated_encoding[t][p] - generated_encoding[t-1][p]) < 5) and smoothVelocities:
					generated_encoding[t][p] = generated_encoding[t-1][p]


				# else:
				# 	if smoothVelocities and (t != 0):
				# 		if (abs(val - generated_encoding[t][p]) < settings.smoothDifference):
				# 			print "we too small maaan: current %d, prev %d" % (generated_encoding[t][p], generated_encoding[t-1][p])
				# 			generated_encoding[t][p] = generated_encoding[t-1][p]



		# Convert to midi file
		pattern = midi.Pattern()
		pattern.resolution = settings.resolution
		track = array_to_midi(generated_encoding)
		pattern.append(track)

		# Append end of track event
		track.append(midi.EndOfTrackEvent(tick=1))

		# Save file
		midi.write_midifile(output_file, pattern)
		print 'generation saved to %s' % output_file

#--------------------------GRAVEYARD---------------------------------


# def generate_next_roll(input_sequence, model, settings):
# 	prediction = model.predict(input_sequence, batch_size=settings.batch_size)
# 	rolld = np.roll(input_sequence[0], -1, axis=0) # Roll ticks back one step
# 	rolld[-1] = prediction[0] # Set last value of input array to the predicted tick
	
# 	next_input = rolld.reshape([1, settings.sequence_size, settings.N_values]) # Assign as next_input
# 	return prediction, next_input


# def generate_next_bigdif(input_sequence, model):
# 	prediction = model.predict(input_sequence, batch_size=settings.batch_size)
	
# 	print input_sequence[0][-1]
# 	for i, val in enumerate(prediction[0]):
# 		if (abs(val - input_sequence[0][-1][v]) <= 10):
# 			prediction[0][i] = input_sequence[0][-1][i]

# 	next_input = np.concatenate((input_sequence[0][1:], prediction), axis = 0).reshape([1, sequence_size, N_values])
# 	return prediction, next_input

# def threshAndBoost(predicted_tick):
	
# 	low_values_indices = predicted_tick[0] < threshold  # Find indices where values are low
# 	predicted_tick[0][low_values_indices] = 0  # All low values set to 0
# 	predicted_tick[0] = predicted_tick[0] * boost # Boost values above threshold
	
# 	return predicted_tick



# print("Creating input")
# # in_arr = np.zeros((1, 64, 128), dtype='float16')
# # tick = 0
# # for quarter in range(4):
# # 	for i in range(8):
# # 		if i == 7:
# # 			in_arr[0][tick][60] = 0
# # 			in_arr[0][tick][64] = 0
# # 			in_arr[0][tick][67] = 0
# # 		else:
# # 			in_arr[0][tick][60] = 0.8
# # 			in_arr[0][tick][64] = 0.8
# # 			in_arr[0][tick][67] = 0.8
# # 		tick += 1

# # for quarter in range(4):
# # 	for i in range(8):
# # 		if i == 7:
# # 			in_arr[0][tick][64] = 0
# # 		else:
# # 			in_arr[0][tick][64] = 0.8
# # 		tick += 1

# # print in_arr
# # print in_arr.shape

# # sys.exit()

# sequence_size = 128
# step = 1
# diversity = 0.5
# N_epochs = 5
# N_values = 128
# threshold = 8.0/128.0
# boost = 2


# # # MIDI settings
# smallest_timestep = 32 # 1/smallest_timestep
# resolution = smallest_timestep / 4


# modelName = "linear_nodes256_sequences128_L1(0.01)_only_classical_20epochs_128sequence_size_batch767"
# model = load_model(modelName)

# generate_name = "someRELUclassicalstuff

# prediction_input = np.load('models/prediction_input.npy')


	# for t in range(64, 192):
	# 	for v in range(0,127):
	# 		# print prediction_input.shape
	# 		# exit()
	# 		prediction_input[0][t-64][v] = enc[t][v]


	# print prediction_input
	# exit()

	# for t in range(0, settings.sequence_size):
	# 	for v in range(0, settings.N_values):
	# 		# print prediction_input.shape
	# 		# exit()
	# 		prediction_input[0][t][v] = enc[t][v]


	# print prediction_input.shape
	# print prediction_input
	# sys.exit()
	# print "generating %d/%d, %s" % (i, fileAmount, generate_name)
	# print prediction_input
	# print prediction_input.shape
	# sys.exit()
	# print prediction_input
	# print prediction_input.shape

	# prediction_input = in_arr


	# sys.exit()

	# output_file = "generations/" + str(settings.generate_length) + "_" +generate_name + ".mid"


	# pattern = midi.Pattern()
	# pattern.resolution = resolution

	# track = midi.Track()
	# pattern.append(track)

	# track.append(midi.NoteOnEvent(tick=0, velocity=64, pitch=60))
	# track.append(midi.NoteOnEvent(tick=7, velocity=0, pitch=60))
	# track.append(midi.NoteOnEvent(tick=1, velocity=64, pitch=60))
	# track.append(midi.NoteOnEvent(tick=7, velocity=0, pitch=60))

	# midi_events, headerInfo, totalTicks = get_midi_events(pattern, resolution)
	# print midi_events
	# print totalTicks
	# # sys.exit()

	# enc = midi_to_array(totalTicks, midi_events)

	# # print enc
	# # # sys.exit()
	# input_sequences = []
	# # next_values = []
	# # # cut the corpus in semi-redundant sequences of sequence_size values
	# # for i in range(0, len(enc) - sequence_size, step):
	# #     input_sequences.append(enc[i: i + sequence_size])
	# #     next_values.append(enc[i + sequence_size])

	# # print('nb sequences:', len(input_sequences))



	# # print input_sequences
	# # print input_sequences.shape

	# input_sequences.append(enc)



	# modelName = "disklavier_512_5epochs_64sequence_size"


		



		# print("Predicting...")


		# prediction_input = np.asarray(input_sequences)
		# prediction_input = X[:1]
		# print('input: ', prediction_input)


		# prediction = model.predict(prediction_input, batch_size=128)

	# print generated_encoding
	# exit()










	# music = []
	# for tick in prediction_input[0]:
	# 	music.append(tick)


	# enc = np.zeros((len(music) + settings.generate_length, settings.N_values), dtype=int)

# print music

	# Convert to encoding
	# print len(music)
	# print len(music[0])
	# enc = np.zeros((len(music), settings.N_values), dtype=int)

	# print enc.shape

	# enc = enc.clip(min=0)
	# low_values_indices = enc < 25
	# enc[low_values_indices] = 0


				# enc[t][v] = int(round(val * 128))

	# print enc
	# sys.exit()