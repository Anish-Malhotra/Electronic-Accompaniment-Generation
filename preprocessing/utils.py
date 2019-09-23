"""
The purpose of this file is to provide functions useful during preprocessing MIDI input files
"""
import numpy as np

# maps the label of a midi instrument to a class
def readLabels(instrProgram, instrName, is_drum):
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

# maps the program number of a midi instrument to a class
def readNumbers(instrProgram):
    if((instrProgram in range(24,32) or instrProgram in range(40, 52))):
        return 'Strings'
    elif((instrProgram in range(80,96))):
        return 'Chords'
    elif((instrProgram in range(56, 80))):
        return 'Winds'
    else:
        return None

# Function used to create list of phrases from a list of pianorolls
def phrases(instr_pianorolls, phrase_length):

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