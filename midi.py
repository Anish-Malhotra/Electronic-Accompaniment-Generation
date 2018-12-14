from __future__ import print_function

import pretty_midi
import numpy as np
from gensim.models import word2vec

num_classes = 7
note_shift = 25
max_note = 77

filename = 'Deadmau5 - Jaded.mid'
filename2 = 'calvin_harris-feel_so_close.mid'

pm = pretty_midi.PrettyMIDI(filename2)


def getInstrumentClass(instrNumber):
    if (instrNumber in range(24, 48)):
        return 'String'
    elif ((instrNumber in range(0, 8)) or (instrNumber in range(16, 24))):
        return 'Piano'
    elif ((instrNumber in range(8, 16)) or (instrNumber in range(112, 120))):
        return 'Percussion'
    elif (instrNumber in range(56, 64)):
        return 'Brass'
    elif (instrNumber in range(64, 80)):
        return 'Wind'
    elif (instrNumber in range(48, 56)):
        return 'Ensemble'
    else:
        return 'Ethnic'


def fillNotes(matrix, instrument):
    note_seq = instrument.notes
    for note in note_seq:
        if note.pitch in range(note_shift, max_note + note_shift):
            start_tick = pm.time_to_tick(note.start)
            end_tick = pm.time_to_tick(note.end)
            for tick in range(start_tick, end_tick):
                matrix[tick][note.pitch - note_shift] = 1


num_instruments = len(pm.instruments)
num_ticks = pm.time_to_tick(pm.get_end_time())

matrix_strings = np.zeros([num_ticks, max_note])
matrix_piano = np.zeros([num_ticks, max_note])
matrix_percussion = np.zeros([num_ticks, max_note])
matrix_brass = np.zeros([num_ticks, max_note])
matrix_wind = np.zeros([num_ticks, max_note])
matrix_ensemble = np.zeros([num_ticks, max_note])
matrix_ethnic = np.zeros([num_ticks, max_note])


def matrixClass(x):
    return {
        'String': matrix_strings,
        'Piano': matrix_piano,
        'Percussion': matrix_percussion,
        'Brass': matrix_brass,
        'Wind': matrix_wind,
        'Ensemble': matrix_ensemble,
        'Ethnic': matrix_ethnic
    }[x]


def base36encode(matrix):
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    matrix36 = np.empty(matrix.shape[0], dtype='S6', order='C')
    for tick in range(matrix.shape[0]):
        base36 = ''
        note_seq = matrix[tick]
        bin_note = 0

        bin_zero = list('0' * max_note)
        for i in range(0, max_note):
            if note_seq[i] == 1:
                bin_zero[i] = '1'
        bin_zero.reverse()

        dec_val = int("".join(bin_zero), 2)

        if 0 <= dec_val < len(alphabet):
            base36 = alphabet[dec_val]

        while dec_val != 0:
            dec_val, i = divmod(dec_val, len(alphabet))
            base36 = alphabet[i] + base36

        # print(base36)
        np.append(matrix36, base36)
    return matrix36


# Converts a base36 matrix into a Word2Vec encoded matrix
def sequenceEncoder(matrix, chords):
    model = word2vec.Word2Vec(matrix, size=100, window=500, min_count=100,
                              sample=1e-3, iter=50, workers=2)
    model.train(chords, total_examples=matrix.shape[0], total_words=1, epochs=10)

    return model


def chordlist():
    Cmaj = bin(145)
    Cmin = bin(145 + 12)
    Dmaj = bin(580)
    Dmin = bin(580 + 12)
    Emaj = bin(2320)
    Emin = bin(2320 + 12)
    Fmaj = bin(545)
    Fmin = bin(545 + 12)
    Gmaj = bin(2180)
    Gmin = bin(2180 + 12)
    Amaj = bin(530)
    Amin = bin(530 + 12)
    Bmaj = bin(2120)
    Bmin = bin(2120 + 12)

    chords = np.empty(112)  # 14 maj/min chords per octave for 8 octaves
    np.append(chords, [Cmaj, Cmin, Dmaj, Dmin, Emaj, Emin, Fmaj, Fmin, Gmaj, Gmin, Amaj, Amin, Bmaj, Bmin])
    for i in range(len(chords)):
        np.append(chords, [Cmaj*48, Cmin*48, Dmaj*48, Dmin*48, Emaj*48, Emin*48, Fmaj*48, Fmin*48, Gmaj*48, Gmin*48, Amaj*48, Amin*48, Bmaj*48, Bmin*48])


for instrument in pm.instruments:
    matrix = matrixClass(getInstrumentClass(instrument.program))
    fillNotes(matrix, instrument)

mat36 = base36encode(matrix_strings)
