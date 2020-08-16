"""
The purpose of this file is to provide functions useful during preprocessing MIDI input files
"""

import numpy as np
from pypianoroll import metrics

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
    Creates list of phrases from a list of pianorolls
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

def qualified_note_rate(pianoroll, threshold=2):
    """
    Return the ratio of the number of the qualified notes (notes longer than
    `threshold` (in time step)) to the total number of notes in a pianoroll.

    """
    if np.issubdtype(pianoroll.dtype, np.bool_):
        pianoroll = pianoroll.astype(np.uint8)
    padded = np.pad(pianoroll, ((1, 1), (0, 0)), "constant")
    diff = np.diff(padded, axis=0).reshape(-1)
    onsets = (diff > 0).nonzero()[0]
    offsets = (diff < 0).nonzero()[0]
    if(len(offsets) == 0):
        offsets = np.empty(shape=onsets.shape)
    # print(offsets.shape, offsets)
    # print(onsets.shape, onsets)
    # print(threshold)
    n_qualified_notes = np.count_nonzero(offsets - onsets >= threshold)
    return n_qualified_notes / len(onsets)

def drum_in_pattern_rate(pianoroll, beat_resolution, tolerance=0.1):
    """
    Return the ratio of the number of drum notes that lie on the drum pattern
    (i.e. at certain time steps) to the total number of drum notes.

    """
    if beat_resolution not in (4, 6, 8, 9, 12, 16, 18, 24):
        raise ValueError(
            "Unsupported beat resolution. Only support 4, 6, 8 ,9, 12, 16, 18 and 42."
        )

    def _drum_pattern_mask(res, tol):
        """Return a drum pattern mask with the given tolerance."""
        if res == 24:
            drum_pattern_mask = np.tile([1.0, tol, 0.0, 0.0, 0.0, tol], pianoroll.shape[0]//6)
        elif res == 12:
            drum_pattern_mask = np.tile([1.0, tol, tol], 4)
        elif res == 6:
            drum_pattern_mask = np.tile([1.0, tol, tol], 2)
        elif res == 18:
            drum_pattern_mask = np.tile([1.0, tol, 0.0, 0.0, 0.0, tol], 3)
        elif res == 9:
            drum_pattern_mask = np.tile([1.0, tol, tol], 3)
        elif res == 16:
            drum_pattern_mask = np.tile([1.0, tol, 0.0, tol], 4)
        elif res == 8:
            drum_pattern_mask = np.tile([1.0, tol], 4)
        elif res == 4:
            drum_pattern_mask = np.tile([1.0, tol], 2)
        return drum_pattern_mask

    drum_pattern_mask = _drum_pattern_mask(beat_resolution, tolerance)
    n_in_pattern = np.sum(drum_pattern_mask * np.count_nonzero(pianoroll, 1))
    return n_in_pattern / np.count_nonzero(pianoroll)

def get_metrics(instr_pianorolls, beat_resolution):
    """
    Metrics used for evaluating MIDI songs
    """
    EB, UPC, QN, DP = 0, 0, 0, 0
    nonempty_pianorolls = 0
    
    for instr_pianoroll in instr_pianorolls:

        if np.sum(instr_pianoroll) > 0: # skip emp
            nonempty_pianorolls += 1
            EB += metrics.empty_beat_rate(instr_pianoroll, beat_resolution)
            UPC += metrics.n_pitches_used(instr_pianoroll)
            QN += qualified_note_rate(instr_pianoroll)
            DP += drum_in_pattern_rate(instr_pianoroll, beat_resolution)

    EB = EB / nonempty_pianorolls
    UPC = UPC / nonempty_pianorolls
    QN = QN / nonempty_pianorolls
    DP = DP / nonempty_pianorolls

    return EB, UPC, QN, DP