from __future__ import print_function

import pretty_midi
import numpy as np

filename = ''
pm = pretty_midi.PrettyMIDI(filename)

def note_to_pitch(notes):
	pitch = []
	for note in notes:
		pitch.append(int(note.pitch))
	return pitch

def get_repeated_seq(seq, start, length):
    ref = seq[start:start+length]
    #print("Ref", ref)
    for pos in range(start+length, len(seq)-length):
        compare = seq[pos:pos+length]
        #print("Pos", pos, compare)
        if compare == ref:
            #print("Found", ref, "at", pos)
            return pos, length
    return False

def get_repeated_seqs(seq):
    reps = []
    for size in reversed(range(2, len(seq)//2)):
        for pos in range(0, len(seq)-size):
            #print("Check rep starting at pos %s for size %s" % (pos, size))
            rep = get_repeated_seq(seq, pos, size)
            if rep:
                reps.append(rep)
    return reps

def get_melody_instrument(pm):
	program = 0
	note_range = 0
	for instrument in pm.instruments:
		pitches = note_to_pitch(instrument.notes)
		sequence = get_repeated_seqs(pitches)[0] ? len(sequence) > 6 : wght(sequence) < 5.67
		temp_range = max(sequence) - min(sequence)
		if temp_range > note_range:
			note_range = temp_range
			program = instrument.program
	return program


