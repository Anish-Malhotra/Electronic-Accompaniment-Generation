"""
The purpose of this script is to calculate metrics for evaluating the quality of a set of MIDI files.

Metrics chosen were selected using and defined by "MuseGAN: Multi-track Sequential Generative Adversarial Networks for Symbolic Music Generation and Accompaniment"
by Hao-Wen Dong,* Wen-Yi Hsiao,* Li-Chia Yang, and Yi-Hsuan Yang

"""

import pypianoroll
import pretty_midi
import numpy as np
import os
import sys
import argparse
import glob

import utils
import melody

if __name__ == "__main__":
    
    # input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--midi_folder", required=True, type=str, help="path of the raw MIDI input training set")
    parser.add_argument("--metrics_folder", required=True, type=str, help="path of save folder")
    parser.add_argument("--note_shift", required=False, type=int, nargs="?", default=24, help="starting note (shifted from octave -2)")
    parser.add_argument("--tpqn", required=False, type=int, nargs="?", default=96, help="ticks per quarter note (beat resolution)")
    args = parser.parse_args()
    
    midi_folder = args.midi_folder + "\\"
    os.chdir(midi_folder)
    num_of_files = len(os.listdir(midi_folder))
    tpqn = args.tpqn
    note_shift = args.note_shift

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

#======================================================
#======== Metrics to Calculate for Each Class =========
#====================================================== 

    """
    Empty Beat Rate (EB):
    ratio of empty bars (in %).

    Used Pitch Classes (UPC):
    number of used pitch classes per bar (from 0 to 12)

    Qualified Notes (QN):
    ratio of “qualified” notes (in %). We consider a note no shorter than three time steps (i.e. a 32th note) as a qualified note. QN shows if the music is overly fragmented.

    Drum Pattern (DP):
    ratio of notes in 8- or 16-beat patterns, common ones for Rock songs in 4/4 time (in %).

    Tonal Distance (TD) between melody and all others:
    measures the hamornicity between a pair of tracks. Larger TD implies weaker inter-track harmonic relations

    """

#=====================================================
#======= Collecting Pianorolls from Each Song ========
#=====================================================  

    i = 0
    i_loaded = 0

    for j, file in enumerate(os.listdir(midi_folder)):
        filename = os.fsdecode(file)
        print(str(j) + ' - ' + filename)   

        pm_song = pretty_midi.PrettyMIDI(midi_folder + filename) # used solely to verify file resolution and find melody

        if(pm_song.resolution == tpqn): # need the file resolution to be consistant
            
            pr = pypianoroll.parse(midi_folder + filename)
            tracklist = pr.tracks

            # Classify using track label first to improve melody prediction
            for t, track in enumerate(tracklist):
                instrument_class = utils.readLabels(track.program, track.name, track.is_drum)
                
                # append the pianoroll and calculate metrics on it
                if instrument_class == 'Percussion':
                    percussion_pianorolls[i] = np.bitwise_or(percussion_pianorolls[i], track.pianoroll)

                elif instrument_class == 'Vocals':
                    vocals_pianorolls[i] = np.bitwise_or(vocals_pianorolls[i], track.pianoroll)

                elif instrument_class == 'Bass':
                    bass_pianorolls[i] = np.bitwise_or(bass_pianorolls[i], track.pianoroll)

                elif instrument_class == 'Chords':
                    chords_pianorolls[i] = np.bitwise_or(chords_pianorolls[i], track.pianoroll)

                pr.remove_tracks(t) # remove the classified track afterwards to avoid reclassification


            # identify the melody    
            melodyNumber = melody.melody_identifier(pr.to_pretty_midi(), note_shift) 
            
            tracklist = pr.tracks
            for t, track in enumerate(tracklist):            
                
                # Classify melody
                if(track.program == melodyNumber):
                    melody_pianorolls[i] = track.pianoroll
                
                else:

                    # Classify using program number
                    instrument_class = utils.readNumbers(track.program)

                    if instrument_class == 'Chords':
                        chords_pianorolls[i] = np.bitwise_or(chords_pianorolls[i], track.pianoroll)

                    elif instrument_class == 'Strings':
                        strings_pianorolls[i] = np.bitwise_or(strings_pianorolls[i], track.pianoroll)

                    elif instrument_class == 'Winds':
                        winds_pianorolls[i] = np.bitwise_or(winds_pianorolls[i], track.pianoroll)
                    
                pr.remove_tracks(t)

            i += 1
        i_loaded += 1

#=====================================================================
#============= Calculating the Instrument Class Metrics ==============
#=====================================================================

    melody_metrics = [utils.get_metrics(melody_pianorolls, pr.beat_resolution)]
    percussion_metrics = [utils.get_metrics(percussion_pianorolls, pr.beat_resolution)]
    strings_metrics = [utils.get_metrics(strings_pianorolls, pr.beat_resolution)]
    bass_metrics = [utils.get_metrics(bass_pianorolls, pr.beat_resolution)]
    winds_metrics = [utils.get_metrics(winds_pianorolls, pr.beat_resolution)]
    vocals_metrics = [utils.get_metrics(vocals_pianorolls, pr.beat_resolution)]
    chords_metrics = [utils.get_metrics(chords_pianorolls, pr.beat_resolution)]

#====================================================================
#=============== Saving the Instrument Class Metrics ================
#====================================================================

    metrics_folder = args.metrics_folder + "\\"

    os.chdir(metrics_folder)

    files = glob.glob(metrics_folder + '*')
    for f in files:
        os.remove(f) # clear folder each time

    print("Melody:", melody_metrics)
    print("Percussion:", percussion_metrics)
    print("Strings:", strings_metrics)
    print("Bass:", bass_metrics)
    print("Winds:", winds_metrics)
    print("Vocals:", vocals_metrics)
    print("Chords:", chords_metrics)

    np.save(metrics_folder + 'strings_metrics', strings_metrics)
    np.save(metrics_folder + 'chords_metrics', chords_metrics)
    np.save(metrics_folder + 'bass_metrics', bass_metrics)
    np.save(metrics_folder + 'winds_metrics', winds_metrics)
    np.save(metrics_folder + 'percussion_metrics', percussion_metrics)
    np.save(metrics_folder + 'vocals_metrics', vocals_metrics)
    np.save(metrics_folder + 'melody_metrics', melody_metrics)