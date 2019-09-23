"""
The purpose of this file is to supply functions used for melody identification
"""

from suffix_tree import Tree

def sublist(lst1, lst2):
    result = all(elem in lst2 for elem in lst1)
    return result

def notes_to_string(notes):
    notes_string = []
    for note in notes:
        notes_string.append(str(note.pitch))
    return ','.join(notes_string)

def get_notes_dict_int(pm):
    notes_dict = dict()
    for instrument in pm.instruments:
        pitches = []
        for note in instrument.notes:
            pitches.append(note.pitch)
        notes_dict[instrument.program] = pitches
    return notes_dict

def get_notes_dict(pm):
    notes_dict = dict()
    for instrument in pm.instruments:
        notes_dict[instrument.program] = notes_to_string(instrument.notes)
    return notes_dict

def grab_paths(tree):
    paths = []
    for C, path in sorted (tree.maximal_repeats ()):
        path_str = str(path)
        path_str.replace(' ', '')
        paths.append(path_str)
    paths.sort(key = len, reverse = True)
    return paths
    
def filter_paths(paths):
    results = []
    for path in paths:
        result = path.split(',')
        result2 = []
        for r in result:
            j = r.replace(' ', '')
            result2.append(j)
        result3 = list(filter(None, result2))
        result3 = [int(i) for i in result3]
        results.append(result3)
    return list(filter(None, results))

def construct_weighted_seq(filtered_paths, note_shift):
    weighted_seq = dict()
    for path in filtered_paths:
        max_pitch = max(path)
        min_pitch = min(path)
        if min_pitch >= note_shift:
            weighted_seq[len(path) * (max_pitch - min_pitch)] = path
    return weighted_seq

def get_melody_instrument(weighted_seq, notes_int):
    best_fit = max(weighted_seq.keys())
    seq = weighted_seq[best_fit]
    for key in notes_int.keys():
        list1 = notes_int[key]  
        if sublist(seq, list1):
            return key

def melody_identifier(pm, note_shift):
    notes_dict = get_notes_dict(pm)
    notes_int = get_notes_dict_int(pm)
    tree = Tree(notes_dict)
    paths = grab_paths(tree)
    results = filter_paths(paths)
    weighted_seq = construct_weighted_seq(results, note_shift)
    return get_melody_instrument(weighted_seq, notes_int)