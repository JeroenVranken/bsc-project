# Logbook

## Week 3
### Tue 12 April
* Got assigned a project


### Wo 13 April
* Meeting with Stratis, discussed general project/ first steps. Need to find dataset! Received material/links to study.
* Watched RNN lecture
* Setup GitHub
* Created logbook

### Thu 14 April
* Searched for literature regarding RNN's, LSTM's and GRU's
* Looked for possible datasets
* New idea: instead of using music with differing genres, use discography's by different artists. The extra input unit would then correspond to the artist that the network is currently training. This should only require a different dataset (and maybe a different input vector).
* Created first draft of problem definition

### Fri 15 April
* Attended presentation session with Karen's group
* Received two possible datasets
* Created Research Territory Mapping
* Finished literature draft

## Week 4
### Mon 18 April
* Attended Deep Learning Lecture
* Started working on project proposal

### Tue 19 April
* Created Presentation Draft
* Created Planning Draft

### Wed 20 April
* Practiced Presentation
* Meeting with Stratis, talked about possible datasets

### Thu 21 April
* Finalized presentation
* Started writing project proposal

### Fri 22 April
* Project proposal presentation
* Finished Project proposal

## Week 5
### Mon 25 April
* DAS4 tutorial
* Gained better understanding of LSTM networks through: http://colah.github.io/posts/2015-08-Understanding-LSTMs/ and http://deeplearning4j.org/lstm.html

### Tue 26 April
* Learned the python-midi framework
* Meeting with Stratis, decided to start with running DeepJazz on own data: https://jisungk.github.io/deepjazz/

### Wed 27 April
* Kingsday

### Thu 28 April
* Work

### Fri 29 April
* Setup dependencies in DAS4 workspace
* Reserved node 421 for a looong time (ssh node412)
* Ran DeepJazz with one epoch to see if everything was setup correctly (it was)

## Week 6
### Mon 2 May
* Learned basics of music21
* Installed musicXML viewer (finale notepad)
* Read paper: https://arxiv.org/abs/1604.05358# 
* Created code overview of DeepJazz

### Tue 3 May
* Discussed inner working of DeepJazz with Josef and Stratis, concluded that it uses too much preprocessing for our objective.
* New plan: feed the network raw midi files, but encode midi in such a way that each frame going through the LSTM is of equal lenght. Basically 'unpacking' the MIDI file
* Created encoder

### Wed 4 May
* Created decoder
* Work

### Thu 5 May
* Fixed timing issue caused by controlChange events
* Edited encoder to only encode a single track, instead of concatenating each track after another. For normal instruments this wasn't really a problem, but drum tracks sound quite weird when you put them on a piano roll

### Fri 6 May
* Wrote code to create training examples
* First training with toy example (Major Scale)

### Sat 7 May
* Scale generation
* Created directory iterator
* Weight saving issue

## Week 7

### Mon 9 May
* Solved weight saving issue, they are now saved as numpy array
* First attempt at training with dataset
* Resolution too high -> out of RAM

### Tue 10 May
* Work

### Wed 11 May
* Created code to lower MIDI-resolution, now more files can be loaded
* Meeting with stratis
* Training on 5% of dataset

### Thu 12 May
* Started training a model on all classical files
* Started training a model on all midi files
* Fixed memory error issue (Some files are muuuch larger than others)

### Fri 13 May
* First generation of music
* Values seem to die out

## Week 8

### Mon 16 May
* Generation error is probably due to activation layer being a softmax. This makes sure all outputs sum to one which is undesired behaviour.
* Discovered error in midi_to_enc. Ticks we're incorrectly calculated due to integer/float division

### Tue 17 May
* Meeting Stratis
* Changed structure of network, now using linear and sigmoid output layers, finaly layer has L1 regularization (to increase sparsity in output)
* Fixed encoding error
* Started training of linear and sigmoid network

### Wed 18 May
* Work

### Thu 19 May
* Generated with newly trained models, sigmoid has really weird behaviour (All notes playing at once and then nothing). Linear does seem promising, the first generated tick is usually a nice continuation of the input, but then it seems to get stuck in the same pattern.

### Fri 20 May
* Discussion with Joseph about continuation error.
* Started writing report

### Sat 21 May
* Talked to stratis, he suggested using a smaller sequence size.
* DAS4 down, so not possible to try it out.
* Wrote about preprocessing / encoding of data 

### Sun 22 May
* DAS4 still down

## Week 9

### Mon 23 May
* Trained three models with a shorter sequence size (32), with depth 1, 2, and 3 respectively. The one with depth 3 seemed most promising, but the produced velocities are really low and quickly die out. It does seem to have a feeling for music, as all generated notes are within the key and even generated within that key that weren't in the input sequence.
* Wrote some code to manage files / folder structure, was getting messy.

### Tue 24 May
* Meeting Stratis, todo points:
  1. Train network without any velocity values, just a binary encoding of on/off
  2. Plot LSTM variables over time
  3. Normalize velocity input to be between [0, 1]
  4. Normalize velocity input to be between [-1, 1]
  5. Boost current models while generating
  6. Bin velocities to create one-hot encoding of note/velocity pairs

### Wed 25 May
* Network with binary values and sigmoid activation and binary crossentropy loss just generates a probability distribution, always the same output irregardless of input: (G - A -C - D)  all played at once and no end notes.
* Same with using mean_squared_error as loss function (Same distribution even)

### Thu 26 May
* Meeting with stratis
* Probability distribution is possibly because of programming error.
* Created midterm presentation

### Fri 27 May
* Midterm presentation

## Week 10

### Mon 30 May
* Rewrote literature review for academic english assignment

### Tue 31 May
* Restructuring of code, using a ModelSettings class which holds all settings.

### Wed 1 June
* Work

### Thu 2 June
* Meeting with stratis & josef, josef had idea train network on one single track, see if it is able to replicate it.
* Trained a 3-stacked LSTM with 32 sequence size, it was able to play moonlight sonata up until a part which was equal to later parts, and it got confused there.

### Fri 3 June
* Started training on 'only_classical' files with many different L1, L2 and dropout settings. Network is now usually able to generate indefinitely.

### Sat/Sun 4/5 June
* Trained models with different settings (All with 512 hidden nodes per LSTM):
  1. Sequence size 32, no regularisation, no dropout: Trained on only moonlight sonata, was able to reproduce it
  2. Sequence size 32, L1 0,01: first silent, then all notes at once with high velocity
  3. Sequence size 32, L2 0,01: Short and low velocity, some random notes after a long period of time
  4. Sequence size 32, L1 0,001: High velocity only on start, afterwards sporadic output with velocities ranging from [1-4]
  5. Sequence size 32, L1 0,001 after 7 iterations on only_classical: Gets stuck in the last notes played
  6. Sequence size 64, L1 0,01, dropout 0.2: Interesting stuff!


## Week 11

### Mon 6 June
* Academic English college
* Continued training on model 6
* Meeting with Stratis, talked about how to implement genres


### Tue 7 June
* Started on implementation of genres, rewrote create_train_generate.py, generate_per_directory.py, midi_encoder.py and trainModel.py to accomodate genres

### Wed 8 June
* Work

### Thu 9 June
* Performed tests on various epochs
* Finished Introduction / Academic English assignment 2

### Sun 12 June
* Tested the genre model with custom input: Same input but different genre results in different output!

## Week 12

### Mon 13 June  
* Continued testing with custom input
  1. Single Notes (A - G)
  2. Chords (Major, Minor)
  3. Varying velocities
* Wrote overview of methodology

### Tue 14 June
* Wrote MIDI, Dataset, preprocessing, genres

### Wed 15 June
* Wrote network layout, training

### Thu 16 June
* Meeting with stratis, decided to conduct a survey
* Wrote generating, post-processing

### Fri 17 June
* Created and conducted survey

### Sat 18 June
* Wrote LSTM explananation

### Sun 19 June
* Digitized survey results
* Analyzed survey results
* Wrote layout of results section

## Week 13
