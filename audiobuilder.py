import pretty_midi
import numpy as np
import os
import midi

class NoteBuilder:
  def __init__(self, pm_num, start, stop):
    self.pm_num = pm_num
    self.start = start
    self.stop = stop

filename = '/Users/am-home/Desktop/training/Daft Punk - One More Time.mid'

#pm = pretty_midi.PrettyMIDI(filename)
midi.load(filename)
pm = midi.get_pm()

for instrument in pm.instruments:
	print(instrument.name + ' - ' + str(instrument.program) + ' - ' + midi.get_instrument_class(instrument.program))

#num_ticks = pm.time_to_tick(pm.get_end_time())
num_ticks = midi.get_maxtick()
end_time = pm.get_end_time()
print(str(num_ticks))
print(str(end_time))
sec_per_tick = end_time/num_ticks

for instrument in pm.instruments:
	if instrument.program == 48:
		matrix = np.zeros([num_ticks,83])
		midi.fill_notes(matrix, instrument)
		print(matrix)

print(str(matrix.shape[0]) + 'x' + str(matrix.shape[1]))

def notes_contain(notes, pm_num):
	for note in notes:
		if note.pm_num == pm_num:
			return True
	return False

def build_note_vector():
	notes = []
	current_notes = []
	rows = matrix.shape[0]
	cols = matrix.shape[1]

	for x in range(0, rows):

		temp = [note for note in current_notes if matrix[x, note.pm_num]==0]
		current_notes = [note for note in current_notes if matrix[x, note.pm_num==1]]
		while temp:
			note = temp.pop(0)
			note.stop = x
			notes.append(pretty_midi.Note(velocity=110, pitch=note.pm_num+24, start=note.start*sec_per_tick, end=note.stop*sec_per_tick))

		for y in range(0, cols):
			if matrix[x,y] == 1:
				if not notes_contain(current_notes, y):
					cnote = NoteBuilder(y, x, 0)
					current_notes.append(cnote)

	return notes


built_notes = build_note_vector()
built_notes.sort(key=lambda x: x.start, reverse=False)
#print(str(pm.instruments[5].program))
original_notes = pm.instruments[5].notes
#print(built_notes)
with open('built.txt', 'w') as f:
    for item in built_notes:
        f.write("%s\n" % item)

with open('original.txt', 'w') as f:
    for item in original_notes:
        f.write("%s\n" % item)

test_mid = pretty_midi.PrettyMIDI()
string_ensemble = pretty_midi.Instrument(program=48)
string_ensemble.notes = built_notes
test_mid.instruments.append(string_ensemble)
test_mid.write('built_string.mid')



