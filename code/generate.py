import sys

import numpy as np
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from encode_decode import midi_to_array, get_midi_events, array_to_midi

import midi


#-------------------------------------Functions--------------------------------
def load_model(filename):
	print("Loading model")
	model = model_from_json(open(filename + '.json').read())
	weights = np.load(filename + '_weights.npy')
	model.set_weights(weights)

	print("Compiling model")
	model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
	return model


def generate_next(input_sequence, model):
	prediction = model.predict(input_sequence, batch_size=128)
	# prediction = threshAndBoost(prediction)
	next_input = np.concatenate((input_sequence[0][1:], prediction), axis = 0).reshape([1, sequence_size, N_values])
	return prediction, next_input

def threshAndBoost(predicted_tick):
	
	low_values_indices = predicted_tick[0] < threshold  # Find indices where values are low
	predicted_tick[0][low_values_indices] = 0  # All low values set to 0
	predicted_tick[0] = predicted_tick[0] * boost # Boost values above threshold
	
	return predicted_tick


#-------------------------------------Code-------------------------------------

print("Creating input")
in_arr = np.zeros((1, 64, 128), dtype='float16')
tick = 0
for quarter in range(4):
	for i in range(8):
		if i == 7:
			in_arr[0][tick][60] = 0
			in_arr[0][tick][64] = 0
			in_arr[0][tick][67] = 0
		else:
			in_arr[0][tick][60] = 0.8
			in_arr[0][tick][64] = 0.8
			in_arr[0][tick][67] = 0.8
		tick += 1

for quarter in range(4):
	for i in range(8):
		if i == 7:
			in_arr[0][tick][64] = 0
		else:
			in_arr[0][tick][64] = 0.8
		tick += 1

# print in_arr
# print in_arr.shape

# sys.exit()

sequence_size = 64
step = 1
diversity = 0.5
N_epochs = 5
N_values = 128
threshold = 8.0/128.0
boost = 2


# # MIDI settings
smallest_timestep = 32 # 1/smallest_timestep
resolution = smallest_timestep / 4

generate_length = 128
modelName = "only_classical_20epochs_64sequence_size_batch1280"
generate_name = "someclassicalstuff"

# prediction_input = np.load('prediction_input.npy')
# print prediction_input
# print prediction_input.shape

prediction_input = in_arr


# sys.exit()

output_file = "generate_" + str(generate_length) + generate_name + ".mid"




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


model = load_model(modelName)



# print("Predicting...")


# prediction_input = np.asarray(input_sequences)
# prediction_input = X[:1]
# print('input: ', prediction_input)


# prediction = model.predict(prediction_input, batch_size=128)


music = []
for tick in in_arr[0]:
	music.append(tick)


print("Generating")
# Generation loop
for i in range(generate_length):
	predicted_tick, next_input = generate_next(prediction_input, model)
	# print predicted_tick
	# print predicted_tick.shape
	# sys.exit()
	music.append(predicted_tick[0])
	prediction_input = next_input

# print music

# Convert to encoding
print len(music)
print len(music[0])
enc = np.zeros((len(music), N_values), dtype=int)

print enc.shape

for t, tick in enumerate(music):
	for v, val in enumerate(tick):
		enc[t][v] = int(round(val * 128))

# print enc
# sys.exit()

pattern = midi.Pattern()
pattern.resolution = resolution

# track = midi.Track()

track = array_to_midi(enc)
pattern.append(track)
print pattern
# Append end of track event
track.append(midi.EndOfTrackEvent(tick=1))
midi.write_midifile(output_file, pattern)


