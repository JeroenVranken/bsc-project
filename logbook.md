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
