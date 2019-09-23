import pypianoroll
import numpy as np
import pretty_midi
import os
import sys
import argparse
import glob

import melody
import utils
	
if __name__ == "__main__":
	
	# input arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--midi_folder", required=True, type=str, help="path of the raw MIDI input training set")
	parser.add_argument("--cleaned_folder", required=True, type=str, help="path of the cleaned MIDI input training set")
	parser.add_argument("--note_shift", required=False, type=int, nargs="?", default=24, help="starting note (shifted from octave -2)")
	parser.add_argument("--num_of_notes", required=False, type=int, nargs="?", default=83, help="number of notes to use (default=84)")
	parser.add_argument("--num_measures", required=False, type=float, nargs="?", default=0.25, help="number of measures for a phrase")
	parser.add_argument("--tpqn", required=False, type=int, nargs="?", default=96, help="ticks per quarter note (beat resolution)")
	args = parser.parse_args()
	
	midi_folder = args.midi_folder
	os.chdir(midi_folder)
	num_of_files = len(os.listdir(midi_folder))

	note_shift = args.note_shift
	num_of_notes = args.num_of_notes

	# Lists of pianorolls for each instrument class (num_ticks x num_notes)
	global strings_pianorolls
	strings_pianorolls = [0]*num_of_files

	global melody_pianorolls
	melody_pianorolls = [0]*num_of_files

	global percussion_pianorolls
	percussion_pianorolls = [0]*num_of_files

	global bass_pianorolls
	bass_pianorolls = [0]*num_of_files

	global winds_pianorolls
	winds_pianorolls = [0]*num_of_files

	global vocals_pianorolls
	vocals_pianorolls = [0]*num_of_files

	global chords_pianorolls
	chords_pianorolls = [0]*num_of_files

#=====================================================
#======= Collecting Pianorolls from Each Song ========
#=====================================================	
	i = 0
	j = 0
	i_loaded = 0
	melodyNumber = [0]*num_of_files
	stringsNumber = [0]*num_of_files
	chordsNumber = [0]*num_of_files
	vocalsNumber = [0]*num_of_files
	windsNumber = [0]*num_of_files
	percussionNumber = [0]*num_of_files
	bassNumber = [0]*num_of_files
	unclassifiedTracks = dict()

	for file in os.listdir(midi_folder):
	    filename = os.fsdecode(file)
	    print(str(j) + ' - ' + filename)
	    j+=1
	    

	    pr = pypianoroll.parse(midi_folder + filename)
	    pm_song = pretty_midi.PrettyMIDI(midi_folder + filename)

	    if(pm_song.resolution == 96): # need the file resolution to be constant
	        
	        tracklist = pr.tracks
	        for t, track in enumerate(tracklist):
	            instrument_class = utils.readLabels(track.program, track.name, track.is_drum)

	            if(t == 0): # do it for first track only as an initialization

	                # Initialize every entry with an empty pianoroll         
	                percussion_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	                melody_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	                bass_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	                vocals_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	                chords_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	                strings_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	                winds_pianorolls[i] = np.zeros(np.shape(track.pianoroll[:, note_shift:(note_shift+num_of_notes)]), dtype=np.uint8)
	               
	            # append the pianoroll that belongs to that instrument class matrix
	            if instrument_class=='Percussion':
	                percussion_pianorolls[i] = np.bitwise_or(percussion_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                percussionNumber[i] += track.program
	            elif instrument_class=='Vocals':
	                vocals_pianorolls[i] = np.bitwise_or(vocals_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                vocalsNumber[i] += track.program
	            elif instrument_class=='Bass':
	                bass_pianorolls[i] = np.bitwise_or(bass_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                bassNumber[i] += track.program
	            elif instrument_class=='Chords':
	                chords_pianorolls[i] = np.bitwise_or(chords_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                chordsNumber[i] += track.program

	            pr.remove_tracks(t) # remove the classified track afterwards to avoid reclassification

	            
	        melodyNumber[i] = melody.melody_identifier(pr.to_pretty_midi(), note_shift) # identify the melody
	        tracklist = pr.tracks
	        for t, track in enumerate(tracklist):            
	            if(track.program == melodyNumber[i]):
	                melody_pianorolls[i] = np.bitwise_or(melody_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                pr.remove_tracks(t)
	            else:
	                instrument_class = utils.readNumbers(track.program)
	                if instrument_class == 'Chords':
	                    chords_pianorolls[i] = np.bitwise_or(chords_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                    chordsNumber[i] += track.program
	                elif instrument_class == 'Strings':
	                    strings_pianorolls[i] = np.bitwise_or(strings_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                    stringsNumber[i] += track.program
	                elif instrument_class == 'Winds':
	                    winds_pianorolls[i] = np.bitwise_or(winds_pianorolls[i], track.pianoroll[:, note_shift:(note_shift+num_of_notes)])
	                    windsNumber[i] += track.program
	                pr.remove_tracks(t)

	        for track in pr.tracks:
	            unclassifiedTracks[filename] = (track.program, track.name)

	        i += 1
	    i_loaded += 1
	                                  
	print(i_loaded,'/', num_of_files, 'files loaded')
	print(i,'/', i_loaded,'files loaded with 96 resolution')

	# Remove any extra entries at the end if not all files had same resolution
	# i = num of files with 96 res

	strings_pianorolls = strings_pianorolls[:i]
	melody_pianorolls = melody_pianorolls[:i]
	percussion_pianorolls = percussion_pianorolls[:i]
	bass_pianorolls = bass_pianorolls[:i]
	chords_pianorolls = chords_pianorolls[:i]
	vocals_pianorolls = vocals_pianorolls[:i]
	winds_pianorolls = winds_pianorolls[:i]

#===========================================================
#======= Creating Phrases for Each Instrument Class ========
#===========================================================

	num_measures = args.num_measures
	tpqn = args.tpqn
	phrase_length = int(num_measures*4*tpqn) # in ticks

	X_strings_phrases, strings_phrases = utils.phrases(strings_pianorolls, phrase_length)

	X_percussion_phrases, percussion_phrases = utils.phrases(percussion_pianorolls, phrase_length)

	X_bass_phrases, bass_phrases = utils.phrases(bass_pianorolls, phrase_length)

	X_chords_phrases, chords_phrases = utils.phrases(chords_pianorolls, phrase_length)

	X_winds_phrases, winds_phrases = utils.phrases(winds_pianorolls, phrase_length)


#===========================================================
#============= Saving the CLeaned Phrase Data ==============
#===========================================================

	cleaned_data_folder = args.cleaned_folder

	os.chdir(cleaned_data_folder)

	files = glob.glob(cleaned_data_folder + '*')
	for f in files:
	    os.remove(f) # clear folder each time

	# Input Data
	np.save(cleaned_data_folder + 'X_strings', X_strings_phrases)
	np.save(cleaned_data_folder + 'X_chords', X_chords_phrases)
	np.save(cleaned_data_folder + 'X_bass', X_bass_phrases)
	np.save(cleaned_data_folder + 'X_winds', X_winds_phrases)
	np.save(cleaned_data_folder + 'X_percussion', X_percussion_phrases)

	# Output Data
	np.save(cleaned_data_folder + 'y_strings', strings_phrases)
	np.save(cleaned_data_folder + 'y_chords', chords_phrases)
	np.save(cleaned_data_folder + 'y_bass', bass_phrases)
	np.save(cleaned_data_folder + 'y_winds', winds_phrases)
	np.save(cleaned_data_folder + 'y_percussion', percussion_phrases)
