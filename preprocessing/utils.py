"""
The purpose of this file is to provide functions useful during preprocessing MIDI input files
"""

import numpy as np
import pypianoroll

def readLabels(instrProgram, instrName, is_drum):
    """
    Maps the label of a midi track to an instrument class
    """
    if (is_drum):
        return 'Percussion'
    elif ((instrProgram in range(32,40) or "bass" in instrName.lower())):
        return 'Bass'
    elif(("vocal" in instrName.lower()) or ("voice" in instrName.lower())):
        return 'Vocals'
    elif("chord" in instrName.lower()):
        return 'Chords'
    else:
        return None

def readNumbers(instrProgram):
    """
    Maps the program number of a midi instrument to a class
    """
    if((instrProgram in range(24,32) or instrProgram in range(40, 52))):
        return 'Strings'
    elif((instrProgram in range(80,96))):
        return 'Chords'
    elif((instrProgram in range(56, 80))):
        return 'Winds'
    else:
        return None

def phrases(instr_pianorolls, phrase_length):
    """
    Function used to create list of phrases from a list of pianorolls
    """
    X_instr_phrases = []
    y_instr_phrases = []

    for j, song in enumerate(instr_pianorolls):
        
        phrase_end = phrase_length # initialize the end of a phrase to be 4 bars from first tick
        # print(j)
        for phrase_start in range(0,len(song)-phrase_length + 1, phrase_length):
            # print(phrase_start, phrase_end)
            y_phrase = song[phrase_start:phrase_end] # grab a phrase
            
            if(np.any(np.count_nonzero(y_phrase, axis=1)) > 0): # if any string bar is not empty
                X_phrase = instr_pianorolls[j][phrase_start:phrase_end] # grab the input phrase at same song/indices
                
                if(np.any(np.count_nonzero(X_phrase, axis=1)) > 0):# if any melody bar is not empty
                    y_instr_phrases.append(y_phrase)
                    X_instr_phrases.append(X_phrase)
                    # print("adding phrases")
               
            phrase_end += phrase_length

    return X_instr_phrases, y_instr_phrases    

def get_metrics(instr_pianorolls, beat_resolution):
    """
    Metrics used for evaluating MIDI songs
    """
    EB, UPC, QN, DP = 0, 0, 0, 0

    for instr_pianoroll in instr_pianorolls:

        if np.sum(instr_pianoroll) > 0: # skip emp
            EB += pypianoroll.metrics.empty_beat_rate(instr_pianoroll, beat_resolution)
            UPC += pypianoroll.metrics.n_pitches_used(instr_pianoroll)
            try: # dim errors occur here
                QN += pypianoroll.metrics.qualified_note_rate(instr_pianoroll)
                DP += pypianoroll.metrics.drum_in_pattern_rate(instr_pianoroll, beat_resolution)
            except:
                continue

    EB = EB / len(instr_pianorolls)
    UPC = UPC / len(instr_pianorolls)
    QN = QN / len(instr_pianorolls)
    DP = DP / len(instr_pianorolls)

    return EB, UPC, QN, DP

def get_tonal_distance(instr_pianorolls, melody_pianorolls, beat_resolution):
    """
    Metric used for evaluating MIDI songs
    """
    TD = 0

    for i in range(0, len(instr_pianorolls)):
        TD += pypianoroll.metrics.tonal_distance(melody_pianorolls[i], instr_pianorolls[i], beat_resolution)

    TD = int(TD / len(instr_pianorolls))

    return TD