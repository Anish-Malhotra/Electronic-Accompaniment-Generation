# This file loads midi files, separates tracks inside the files by instrument class, creates matrices for these classes
# based on noteOn/Off events at each tick of the song, and then converts these instrument class matrices of bits into
# base 36 'words' which get passed into the Word2Vec word embedding in note_embedding.py
# This functions in this file get executed in preprocessor.py by calling get_ticks() at the bottom

from __future__ import print_function

import pretty_midi
import numpy as np

num_classes = 7
note_shift = 25
max_note = 77


def load(filename):
    global pm
    pm = pretty_midi.PrettyMIDI(filename)

    print("loaded songname: " + filename)

    if pm.get_end_time() < 30:
        return False
    if pm.instruments <= 3:
        return False

    init_matrices()
    return True


def init_matrices():
    global num_instruments
    num_instruments = len(pm.instruments)

    global num_ticks
    num_ticks = pm.time_to_tick(pm.get_end_time())

    global matrix_strings
    matrix_strings = np.zeros([num_ticks, max_note])
    global matrix_melody
    matrix_melody = np.zeros([num_ticks, max_note])
    global matrix_percussion
    matrix_percussion = np.zeros([num_ticks, max_note])
    global matrix_bass
    matrix_bass = np.zeros([num_ticks, max_note])
    global matrix_brass
    matrix_brass = np.zeros([num_ticks, max_note])
    global matrix_ensemble
    matrix_ensemble = np.zeros([num_ticks, max_note])

    global b36_list_strings
    b36_list_strings = []
    global b36_list_melody
    b36_list_melody = []
    global b36_list_percussion
    b36_list_percussion = []
    global b36_list_bass
    b36_list_bass = []
    global b36_list_brass
    b36_list_brass = []
    global b36_list_ensemble
    b36_list_ensemble = []


def get_instrument_class(instrNumber):
    if ((instrNumber in range(25, 33)) or (instrNumber in range(41, 53))):
        return 'String'
    elif ((instrNumber in range(1, 9)) or (instrNumber in range(17, 25)) or (instrNumber in range(81, 97))):
        return 'Melody'
    elif ((instrNumber in range(9, 17)) or (instrNumber in range(113, 121))):
        return 'Percussion'
    elif ((instrNumber in range(58, 62)) or (instrNumber in range(33, 41))):
        return 'Bass'
    elif (instrNumber in range(62, 65)):
        return 'Brass'
    elif (instrNumber in range(53, 57)):
        return 'Ensemble'
    else:
        return ''


def fill_notes(matrix, instrument):
    note_seq = instrument.notes
    for note in note_seq:
        if note.pitch in range(note_shift, max_note + note_shift):
            start_tick = pm.time_to_tick(note.start)
            end_tick = pm.time_to_tick(note.end)
            for tick in range(start_tick, end_tick):
                matrix[tick][note.pitch - note_shift] = 1


def matrix_class(x):
    return {
        'String': matrix_strings,
        'Melody': matrix_melody,
        'Percussion': matrix_percussion,
        'Bass': matrix_bass,
        'Brass': matrix_brass,
        'Ensemble': matrix_ensemble,
    }[x]


def b36_list_class(x):
    return {
        'String': b36_list_strings,
        'Melody': b36_list_melody,
        'Percussion': b36_list_percussion,
        'Bass': b36_list_bass,
        'Brass': b36_list_brass,
        'Ensemble': b36_list_ensemble,
    }[x]


def base36encode(list36, matrix):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for tick in range(matrix.shape[0]):
        base36 = ''
        note_seq = matrix[tick]
        bin_note = 0

        bin_zero = list('0' * max_note)
        for i in range(0, max_note):
            if note_seq[i] == 1:
                bin_zero[i] = '1'

        dec_val = int("".join(bin_zero), 2)  # creates a binary number out of the bit cells in matrix (of note events)

        if 0 <= dec_val < len(alphabet):
            base36 = alphabet[dec_val]

        while dec_val != 0:
            dec_val, i = divmod(dec_val, len(alphabet))
            base36 = alphabet[i] + base36

        # print(base36)
        np.append(list36, base36)


def get_ticks():
    for instrument in pm.instruments:
        print("Loading: " + instrument.name)
        instrument_class = get_instrument_class(instrument.program)
        matrix = matrix_class(instrument_class)
        print("Filling matrix of notes")
        fill_notes(matrix, instrument)
        b36_list = b36_list_class(instrument_class)
        print("Converting matrix to base 36 list of events")
        base36encode(b36_list, matrix)
        print("Next instrument")
    return (b36_list_strings, b36_list_melody, b36_list_percussion, b36_list_bass, b36_list_brass,
            b36_list_ensemble)
