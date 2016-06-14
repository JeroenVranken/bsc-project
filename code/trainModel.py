import sys
import os

import midi
import numpy as np
from shutil import copyfile
from midi_encoder import *
from save_load_model import *
from directory_iterator import getFilePaths


def reTrainModel(settings, epochs, batch):
	originalFilename = settings.filename
	loadFilename = settings.filename
	for i in range (epochs):
		settings.filename = loadFilename
		model = load_model_scratch(settings, batch, loadWeights=True)
		settings.filename = originalFilename + "_ep" + str(i+1)
		loadFilename = settings.filename
		if settings.genres:
			trainModelGenres(model, settings)
		else:
			trainModel(model, settings)
		copyfile('/var/scratch/jvranken/models/' + originalFilename + '/model_settings.txt', '/var/scratch/jvranken/models/' + settings.filename + '/model_settings.txt')


def trainModel(model, settings):
	genre = ''

	print "Training model with the following settings:"
	for (setting, value) in vars(settings).items():
		print str(setting) + ': ' + str(value)

	filePaths = getFilePaths(settings.directoryPath, '.mid')
	print "total files: " + str(len(filePaths))


	# Training settings
	N_epochs = 1
	training_file_amount = 0
	model_batch_size = 240
	filePathIndex = 0


	# Load data dynamically, track length determines amount of tracks to use so memory doesn't overflow
	while (filePathIndex < (len(filePaths)-training_file_amount)):
		
		input_sequences = []
		next_values = []

		print("Loading files")
		while (len(input_sequences) < 140000):
		
			try:
				pattern = midi.read_midifile(filePaths[filePathIndex])
			except:
				print "Error while reading midi file:", filePaths[filePathIndex]
				for error in sys.exc_info():
					print error
			filePathIndex += 1

			midi_events, headerInfo, totalTicks = get_midi_events(pattern, settings.resolution)
			enc = midi_to_array(settings, totalTicks, midi_events, genre)

			# cut the corpus in semi-redundant sequences of sequence_size values
			for i in range(0, len(enc) - settings.sequence_size, settings.step):
			    input_sequences.append(enc[i: i + settings.sequence_size])
			    next_values.append(enc[i + settings.sequence_size])

			if (filePathIndex >= len(filePaths)-training_file_amount):
				break;

		print("Training model, " + settings.filename + '\n nb sequences: '+ str(len(input_sequences)) + " batch:" +str(filePathIndex))
		print np.asarray(input_sequences).shape, np.asarray(next_values).shape

		model.fit(np.asarray(input_sequences), np.asarray(next_values), batch_size=settings.batch_size, nb_epoch=settings.N_epochs)

		save_model_scratch(model, settings.filename, str(filePathIndex), True)


def trainModelGenres(model, settings):

	print "Training model with the following settings:"
	for (setting, value) in vars(settings).items():
		print str(setting) + ': ' + str(value)


	# Put jazz and classic files alternating in trainingset
	classicPaths = getFilePaths(settings.classicPath, '.mid')
	jazzPaths = getFilePaths(settings.jazzPath, '.mid')

	filePaths = []

	for i in range(len(jazzPaths)):
		filePaths.append(classicPaths[i])
		filePaths.append(jazzPaths[i])

	print "total files: " + str(len(filePaths))


	# Training settings
	N_epochs = 1
	training_file_amount = 0
	# model_batch_size = 240
	filePathIndex = 0


	# Load data dynamically, track length determines amount of tracks to use so memory doesn't overflow
	while (filePathIndex < (len(filePaths)-training_file_amount)):
		
		input_sequences = []
		next_values = []
		genre = ''

		print("Loading files")
		while (len(input_sequences) < 100000):

			if (filePathIndex % 2 == 0):
				genre = 'classical'
			elif (filePathIndex % 2 == 1):
				genre = 'jazz'
		
			try:
				pattern = midi.read_midifile(filePaths[filePathIndex])
			except:
				print "Error while reading midi file:", filePaths[filePathIndex]
				for error in sys.exc_info():
					print error
			filePathIndex += 1

			midi_events, headerInfo, totalTicks = get_midi_events(pattern, settings.resolution)
			
			# enc = midi_to_array_genre(settings, totalTicks, midi_events, genre)
			enc = midi_to_array(settings, totalTicks, midi_events, genre)

			# cut the corpus in semi-redundant sequences of sequence_size values
			for i in range(0, len(enc) - settings.sequence_size, settings.step):
			    input_sequences.append(enc[i: i + settings.sequence_size])
			    next_values.append(enc[i + settings.sequence_size])

			if (filePathIndex >= len(filePaths)-training_file_amount):
				break;

		print("Training model, " + settings.filename + '\n nb sequences: '+ str(len(input_sequences)) + " batch:" +str(filePathIndex))
		print np.asarray(input_sequences).shape, np.asarray(next_values).shape

		model.fit(np.asarray(input_sequences), np.asarray(next_values), batch_size=settings.batch_size, nb_epoch=settings.N_epochs)

		save_model_scratch(model, settings.filename, str(filePathIndex), True)


