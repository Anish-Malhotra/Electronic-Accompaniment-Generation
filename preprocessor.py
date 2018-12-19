from __future__ import print_function

import pretty_midi
import numpy as np
import os

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
			song_matrix_string.append(matrix[0])
			print('Got string')
			song_matrix_melody.append(matrix[1])
			print('Got melody')
			song_matrix_percussion.append(matrix[2])
			print('Got perc')
			song_matrix_bass.append(matrix[3])
			print('Got bass')
			song_matrix_brass.append(matrix[4])
			print('Got brass')
			song_matrix_ensemble.append(matrix[5])
			print('Got ensemble')



