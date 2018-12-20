from __future__ import print_function

import pretty_midi
import numpy as np
import os
from itertools import chain  # for concatenating lists
import midi

directory = "/Users/am-home/midi_processing/training_data/" #CHANGE THIS OR WILL NOT WORK!

song_matrix_melody = []
song_matrix_string = []
song_matrix_percussion = []
song_matrix_bass = []
song_matrix_brass = []
song_matrix_ensemble = []

for filename in os.listdir(directory):
	if filename.endswith(".mid"):
		if midi.load(directory + filename) == True:
			matrix = midi.get_ticks()
			song_matrix_string = chain(song_matrix_string, matrix[0])
			print('Got string')
			song_matrix_melody = chain(song_matrix_melody, matrix[1])
			print('Got melody')
			song_matrix_percussion = chain(song_matrix_percussion, matrix[2])
			print('Got perc')
			song_matrix_bass = chain(song_matrix_bass, matrix[3])
			print('Got bass')
			song_matrix_brass = chain(song_matrix_brass, matrix[4])
			print('Got brass')
			song_matrix_ensemble = chain(song_matrix_ensemble, matrix[5])
			print('Got ensemble')



