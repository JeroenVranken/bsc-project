import midi
import sys
import numpy as np

np.set_printoptions(threshold=np.nan)

#-------------------------------Functions------------------------------------#
def convertVelocity(velocity):
	newVelocity = float(velocity)/128.0
	return newVelocity

def convertVelocityNegPos(velocity):
	newVelocity = (float(velocity)/64.0) - 1.0
	return newVelocity

def get_midi_events(pattern, resolution):
	originalResolution = pattern.resolution
	midi_events = []
	headerInfo = []
	totalTicks = 0
	singleStream = []
	
	
	# Extract only first stream
	if (len(pattern) >= 2):
		singleStream.append(pattern[0])
		singleStream.append(pattern[1])
	else:
		singleStream = pattern

	# Loop over each track
	for i, track in enumerate(singleStream):
		for event in track:
			event.tick = convertResolution(originalResolution, resolution, event.tick)
			# print'old tick: %d, new tick %d, reso %d' % (oldtick, new_tick, resolution)
			# print event

			# Put events in list if of type noteOn or noteOff
			if (midi.NoteOnEvent == type(event) or midi.NoteOffEvent == type(event)):
				totalTicks += event.tick
				midi_events.append(event)

			# Get header info
			elif (midi.TimeSignatureEvent == type(event) or midi.SetTempoEvent == type(event)):
				headerInfo.append(event)
				totalTicks += event.tick

			# Add controlChange ticks to totalticks (otherwise timing will be different)
			elif(midi.ControlChangeEvent == type(event)):
				midi_events.append(event)
				totalTicks += event.tick

	return midi_events, headerInfo, totalTicks


def midi_to_array(settings, totalTicks, midi_events, genre):

	currentTick = 0
	'''
	Create 3d encoding matrix 
	| axis 1 = ticks
	| axis 2 = pitch (between 0 and 127)
	| value = velocity (boolean)
	'''
	# if convert:
	# 	enc = np.zeros((totalTicks, 128), dtype='float16')
	# else:
		# enc = np.zeros((totalTicks, 128), dtype=int)
	# enc = np.full((totalTicks, 128), -1, dtype='float16')
	enc = np.zeros((totalTicks, settings.N_values), dtype=int)

	for event in midi_events:
		
		# Possible that multiple notes are playing at once
		if event.tick == 0:
			if (midi.ControlChangeEvent != type(event)):
				try:
					if (midi.NoteOffEvent == type(event)):
						enc[currentTick][event.pitch] = 0
					else:
						if settings.convertVelocity:
							enc[currentTick][event.pitch] = convertVelocityNegPos(event.pitch)
						else:
							if (event.velocity > 0):
								enc[currentTick][event.pitch] = event.velocity
				except:
					continue


		else:
			for i in range(event.tick): # Keep copying until tick of next event	
				currentVector = enc[currentTick]
				currentTick += 1
				# print(currentTick)
				try:
					enc[currentTick] = currentVector
				except:
					continue

			
			# Then add event at current Tick 
			try:
				if (midi.ControlChangeEvent != type(event)):
					if (midi.NoteOffEvent == type(event)):
						enc[currentTick][event.pitch] = 0
					else:	
						if settings.convertVelocity:
							enc[currentTick][event.pitch] = convertVelocityNegPos(event.pitch)
						else:
							if (event.velocity > 0):
								enc[currentTick][event.pitch] = event.velocity
			except:
				continue

	if settings.genres:
		if genre == 'classical':
			enc[:, 128] = 128
		elif genre == 'jazz':
			enc[:, 129] = 128
	return enc


def array_to_midi(enc):

	# If genre encoding are attached, remove
	# if (len(enc[0]) > 128):
	# 	enc = enc[:, 0:127]


	track = midi.Track()
	
	currentVector = np.zeros(len(enc[0]))

	tickDifference = -1

	for i, tick in enumerate(enc):

		nextVector = enc[i]
		tickDifference += 1

		if not np.array_equal(currentVector, nextVector):
			diff = currentVector - nextVector
			# print diff
			for pitch, dVelocity in enumerate(diff):
				if (dVelocity != 0):
					if nextVector[pitch] < 1: # Create noteoff event in case of 0
						# track.append(midi.NoteOffEvent(tick=tickDifference,  pitch=pitch, velocity=(nextVector[pitch])))
						track.append(midi.NoteOffEvent(tick=tickDifference,  pitch=pitch, velocity=(0)))
					else:
						track.append(midi.NoteOffEvent(tick=tickDifference,  pitch=pitch, velocity=(0)))
						track.append(midi.NoteOnEvent(tick=tickDifference,  pitch=pitch, velocity=(nextVector[pitch])))
					tickDifference = 0
				# tickDifference = 0
		# else:
			# tickDifference += 1

		currentVector = nextVector	


		nextVector = enc[i]
	
	# Add noteOffEvent on all tracks
	for p in range(128):
		track.append(midi.NoteOffEvent(tick=0,  pitch=p, velocity=(0)))
	
	return track



def convertResolution(original, new, tick):
	return int(round((float(tick)/float(original))*float(new)))

def midi_to_array_genre(settings, totalTicks, midi_events, genre):


	currentTick = 0
	'''
	Create 3d encoding matrix 
	| axis 1 = ticks
	| axis 2 = pitch (between 0 and 127)
	| value = velocity (boolean)
	'''
	# if convert:
	# 	enc = np.zeros((totalTicks, 128), dtype='float16')
	# else:
		# enc = np.zeros((totalTicks, 128), dtype=int)
	# enc = np.full((totalTicks, 128), -1, dtype='float16')
	enc = np.zeros((totalTicks, settings.N_values), dtype=int)

	for event in midi_events:
		
		# Possible that multiple notes are playing at once
		if event.tick == 0:
			if (midi.ControlChangeEvent != type(event)):
				try:
					if (midi.NoteOffEvent == type(event)):
						enc[currentTick][event.pitch] = 0
					else:
						if settings.convertVelocity:
							enc[currentTick][event.pitch] = convertVelocityNegPos(event.pitch)
						else:
							if (event.velocity > 0):
								enc[currentTick][event.pitch] = event.velocity
				except:
					continue


		else:
			for i in range(event.tick): # Keep copying until tick of next event	
				currentVector = enc[currentTick]
				currentTick += 1
				# print(currentTick)
				try:
					enc[currentTick] = currentVector
				except:
					continue

			
			# Then add event at current Tick 
			try:
				if (midi.ControlChangeEvent != type(event)):
					if (midi.NoteOffEvent == type(event)):
						enc[currentTick][event.pitch] = 0
					else:	
						if settings.convertVelocity:
							enc[currentTick][event.pitch] = convertVelocityNegPos(event.pitch)
						else:
							if (event.velocity > 0):
								enc[currentTick][event.pitch] = event.velocity
			except:
				continue

	# print enc.shape
	# exit()
	if genre == 'classical':
		enc[:, 128] = 128
	elif genre == 'jazz':
		enc[:, 129] = 128
	return enc


#-------------------------------Code------------------------------------------#

# print("Parsing MIDI")
# # Parse the MIDI data for separate melody and accompaniment parts.
# midi_data = converter.parse(input_file)
# print("After converting")

# # Get first stream
# singleStream = midi_data.getElementsByClass(stream.Stream)[0]

# # Write back to disk
# singleStream.write('midi', 'singleTrack.mid')
# resolution = 8

# pattern = midi.read_midifile(input_file)
# midi_events, headerInfo, totalTicks = get_midi_events(pattern, resolution)

# print(str(totalTicks) +  " total ticks")

# # Setup pattern and track
# nPattern = midi.Pattern()
# nTrack = midi.Track()
# nPattern.append(nTrack)

# # Set resolution
# nPattern.resolution = resolution

# # Convert midi events to encoding
# enc = midi_to_array(totalTicks, midi_events)

# # Convert from encoding back to midi events
# array_to_midi(enc, nTrack)

# # Append end of track event
# nTrack.append(midi.EndOfTrackEvent(tick=1))	

# # Write to file
# midi.write_midifile(output_file, nPattern)

# sys.exit()
