from __future__ import print_function

import pretty_midi
import numpy as np

num_classes = 7
note_shift = 25
max_note = 77

#filename = 'Deadmau5 - Jaded.mid'
#filename2 = 'calvin_harris-feel_so_close.mid'

#pm = pretty_midi.PrettyMIDI(filename)

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

    global b36_matrix_strings
    b36_matrix_strings = np.empty(num_ticks, dtype=str, order='C')
    global b36_matrix_melody
    b36_matrix_melody = np.empty(num_ticks, dtype=str, order='C')
    global b36_matrix_percussion
    b36_matrix_percussion = np.empty(num_ticks, dtype=str, order='C')
    global b36_matrix_bass
    b36_matrix_bass = np.empty(num_ticks, dtype=str, order='C')
    global b36_matrix_brass
    b36_matrix_brass = np.empty(num_ticks, dtype=str, order='C')
    global b36_matrix_ensemble
    b36_matrix_ensemble = np.empty(num_ticks, dtype=str, order='C')
    

def get_instrument_class(instrNumber):
    if ((instrNumber in range(25, 33)) or (instrNumber in range(41, 53))):
        return 'String'
    elif ((instrNumber in range(1, 9)) or (instrNumber in range(17, 25)) or (instrNumber in range(81,97))):
        return 'Melody'
    elif ((instrNumber in range(9, 17)) or (instrNumber in range(113, 121))):
        return 'Percussion'
    elif ((instrNumber in range(58, 62)) or (instrNumber in range(33,41))):
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

def b36_matrix_class(x):
    return {
        'String': b36_matrix_strings,
        'Melody': b36_matrix_melody,
        'Percussion': b36_matrix_percussion,
        'Bass': b36_matrix_bass,
        'Brass': b36_matrix_brass,
        'Ensemble': b36_matrix_ensemble,
    }[x]

def base36encode(matrix36, matrix):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for tick in range(matrix.shape[0]):
        base36 = ''
        note_seq = matrix[tick]
        bin_note = 0

        bin_zero = list('0' * max_note)
        for i in range(0,max_note):
            if note_seq[i] == 1:
                bin_zero[i] = '1'

        dec_val = int("".join(bin_zero),2)

        if 0 <= dec_val < len(alphabet):
            base36 = alphabet[dec_val]

        while dec_val != 0:
            dec_val, i = divmod(dec_val, len(alphabet))
            base36 = alphabet[i] + base36

        #print(base36)
        np.append(matrix36, base36)

def get_ticks():
    for instrument in pm.instruments:
        print("Loading: " + instrument.name)
        instrument_class = get_instrument_class(instrument.program)
        matrix = matrix_class(instrument_class)
        print("Filling matrix:")
        fill_notes(matrix, instrument)
        b36_matrix = b36_matrix_class(instrument_class)
        print("Converting matrix")
        base36encode(b36_matrix, matrix)
        print("Next instrument")
    return (b36_matrix_strings, b36_matrix_melody, b36_matrix_percussion, b36_matrix_bass, b36_matrix_brass, b36_matrix_ensemble)
