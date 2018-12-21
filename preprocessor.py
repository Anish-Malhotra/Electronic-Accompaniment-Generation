from __future__ import print_function

import pretty_midi
import numpy as np
import os
import midi
import note_embedding
from gensim.test.utils import get_tmpfile
directory = "C:\Users\matta_000\Documents\training"  # CHANGE THIS OR WILL NOT WORK!

song_matrix_melody = [[]]
song_matrix_string = [[]]
song_matrix_percussion = [[]]
song_matrix_bass = [[]]
song_matrix_brass = [[]]
song_matrix_ensemble = [[]]


def buildPreEmbedding():
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


def chordlist():
    Cmaj = 145
    Cmin = 137
    Dmaj = 580
    Dmin = 548
    Emaj = 2320
    Emin = 2192
    Fmaj = 545
    Fmin = 529
    Gmaj = 2180
    Gmin = 2116
    Amaj = 530
    Amin = 522
    Bmaj = 2120
    Bmin = 2088

    # 14 maj/min chords per octave for 8 octaves
    chords = [Cmaj, Cmin, Dmaj, Dmin, Emaj, Emin, Fmaj, Fmin, Gmaj, Gmin, Amaj, Amin, Bmaj, Bmin]

    for i in range(1, 8):  # Want to insert chords for octaves 1 to 8
        chords += [Cmaj << 12, Cmin << 12, Dmaj << 12, Dmin << 12, Emaj << 12, Emin << 12, Fmaj << 12, Fmin << 12,
                   Gmaj << 12, Gmin << 12, Amaj << 12, Amin << 12, Bmaj << 12, Bmin << 12]
    return chords


# Setting up the Pre Embedding 2D arrays
buildPreEmbedding()

# Trains the word embedding models for each instrument class
melodyEmbedding = note_embedding.sequenceEncoder(song_matrix_melody)
temp_path1 = get_tmpfile("models/melodyEmbedding.model")  # creates a file path
melodyEmbedding.save(temp_path1)  # save the model

# stringEmbedding = note_embedding.sequenceEncoder(song_matrix_string)
# temp_path2 = get_tmpfile("models/stringEmbedding.model")  # creates a file path
# stringEmbedding.save(temp_path2)  # save the model
#
# brassEmbedding = note_embedding.sequenceEncoder(song_matrix_brass)
# temp_path3 = get_tmpfile("models/brassEmbedding.model")  # creates a file path
# brassEmbedding.save(temp_path3)  # save the model
#
# bassEmbedding = note_embedding.sequenceEncoder(song_matrix_bass)
# temp_path4 = get_tmpfile("models/bassEmbedding.model")  # creates a file path
# bassEmbedding.save(temp_path4)  # save the model
#
# ensembleEmbedding = note_embedding.sequenceEncoder(song_matrix_ensemble)
# temp_path5 = get_tmpfile("models/ensembleEmbedding,model")  # creates a file path
# ensembleEmbedding.save(temp_path5)  # save the model
#
# percussionEmbedding = note_embedding.sequenceEncoder(song_matrix_percussion)
# temp_path6 = get_tmpfile"models/percussionEmbedding.model")  # creates a file path
# percussionEmbedding.save(temp_path6)  # save the model





