
if not os.path.exists('generations/' + modelName):
    os.makedirs('generations/' + modelName)


filePaths = getFilePaths('/home/jvranken/input_sequences/testing', '.npy')
fileAmount = 5

shortTicks = []

for i in range(0, fileAmount):
	generate_name = filePaths[i].split('/')[-1]
	prediction_input = np.zeros((1, sequence_size, 128), int)	
	songStart = np.load(filePaths[i])
	songStart = songStart[:sequence_size]

	for t, tick in enumerate(songStart):
		for v, val in enumerate(tick):
			prediction_input[0][t][v] = convertVelocityToNegPos(val)

	print "generating %d/%d, %s" % (i, fileAmount, generate_name)

	output_file = "generations/" + modelName + "/" + str(generate_length) + "_" + generate_name + ".mid"

	music = []
	for tick in songStart:
		music.append(tick)

	# print music
	print prediction_input[0]
	print("Generating")
	# Generation loop
	for i in range(generate_length):
		if (i % 100 == 0):
			print "iterating %d/%d" % (i, generate_length)
		# predicted_tick, next_input = generate_next(prediction_input, model)
		predicted_tick, next_input = generate_next_roll(prediction_input, model)
		# print predicted_tick
		# print predicted_tick.shape
		# sys.exit()
		shortTicks.append(predicted_tick[0])
		music.append(predicted_tick[0])
		prediction_input = next_input

	# print shortTicks
	# sys.exit()
	# print music

	# Convert to encoding
	# print len(music)
	# print len(music[0])
	enc = np.zeros((len(music), N_values), dtype=int)

	print enc.shape

	# enc = enc.clip(min=0)
	# low_values_indices = enc < 25
	# enc[low_values_indices] = 0

	for t, tick in enumerate(music):
		for v, val in enumerate(tick):
			enc[t][v] = convertNegPosToVelocity(val)

	# print enc
	# sys.exit()
	# np.savetxt('generated_frames.txt', enc)
	# sys.exit()
	pattern = midi.Pattern()
	pattern.resolution = resolution

	# track = midi.Track()

	track = array_to_midi(enc)
	pattern.append(track)
	# print pattern
	# Append end of track event
	track.append(midi.EndOfTrackEvent(tick=1))
	midi.write_midifile(output_file, pattern)