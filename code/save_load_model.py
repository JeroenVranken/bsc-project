import os
import numpy as np
from keras.models import model_from_json


def save_model(model, filename, batch, saveWeights):
	if not os.path.exists('models/' + filename):
		os.makedirs('models/' + filename)

	print("Saving model")
	json_string = model.to_json()
	open('models/' + filename + '/batch' +  str(batch) + '.json', 'w').write(json_string)

	if saveWeights:
		weights = model.get_weights()
		np.save('models/' + filename + '/batch' + str(batch) + '_weights', weights)

def load_model(settings, batch, loadWeights):
	print("Loading model")
	model = model_from_json(open('models/' + settings.filename + '/batch' + str(batch) + '.json').read())
	
	if loadWeights:
		weights = np.load('models/' + settings.filename + '/batch' + str(batch) + '_weights.npy')
		model.set_weights(weights)

	print("Compiling model")
	model.compile(loss=settings.lossType, optimizer='rmsprop')
	# model.compile(loss='mean_squared_error', optimizer='rmsprop', activity_regularizer=activity_l1(0.01)))
	return model




def save_model_scratch(model, filename, batch, saveWeights):
	if not os.path.exists('/var/scratch/jvranken/models/' + filename):
		os.makedirs('/var/scratch/jvranken/models/' + filename)

	print("Saving model")
	json_string = model.to_json()
	open('/var/scratch/jvranken/models/' + filename + '/batch' +  str(batch) + '.json', 'w').write(json_string)

	if saveWeights:
		weights = model.get_weights()
		np.save('/var/scratch/jvranken/models/' + filename + '/batch' + str(batch) + '_weights', weights)

def load_model_scratch(settings, batch, loadWeights):
	# Print model settings
	print "Loading model %s with the following settings:" % (settings.filename)
	# with open('/var/scratch/jvranken/models/' + settings.filename + '/model_settings.txt', 'r') as reader:
	# 	model_settings = reader.read()
	# 	print model_settings
	# 	reader.close()

	model = model_from_json(open('/var/scratch/jvranken/models/' + settings.filename + '/batch' + str(batch) + '.json').read())
	
	if loadWeights:
		weights = np.load('/var/scratch/jvranken/models/' + settings.filename + '/batch' + str(batch) + '_weights.npy')
		model.set_weights(weights)

	print("Compiling model")
	model.compile(loss=settings.lossType, optimizer='adam')
	# model.compile(loss='mean_squared_error', optimizer='rmsprop', activity_regularizer=activity_l1(0.01)))
	return model

