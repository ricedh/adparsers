import os
import sys
import json
import ner  # pyner

def locations_tag(directory):
    """
    Finds location terms in all text files in a given directory

    Input:
    directory - string representing the local directory to analyze

    Output:
    locations - dictionary mapping each file containing location terms
                to the terms
    """
    locations = {}
    tagger = ner.SocketNER(host='localhost', port=8080)
    subs = {
        '\n': '.  ',
        'co.': 'County',
        'Co.': 'County',
        'county': 'County',
        'A.T.': 'Arkansas',
        'M.T.': 'Mississippi'
        }
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as f:
                text = f.read().decode("utf8")
                text = preprocess(text, subs)
                entities = tagger.get_entities(text)
                if 'LOCATION' in entities:
                    locs = merge_locations(entities['LOCATION'], text)
                    locations[filename] = locs
    return locations

def preprocess(text, subs):
    for from_, to_ in subs.items():
        text = text.replace(from_, to_)
    return text

def merge_locations(locs, text):
    idx = 0
    last_idx = len(locs) - 1
    merged = []
    while idx <= last_idx:
        loc = locs[idx]
        while not idx is last_idx:
            gap, text, merge = gap_length(locs[idx], locs[idx+1], text)
            if gap <= 2:
                loc += merge
                idx += 1
            else:
                break
        merged.append(loc)
        idx += 1
    return merged

def gap_length(word1, word2, text):
    pos1, pos2 = text.index(word1), text.index(word2)
    pos1_e, pos2_e = pos1 + len(word1), pos2 + len(word2)
    
    gap = pos2 - pos1_e
    edited_text = chr(0)*pos1_e + text[pos1_e:]
    inter_text = text[pos1_e:pos2_e]
    return gap, edited_text, inter_text

def main():
    """
    Create a json file storing locations dictionary for each
        directory argument of the script
    """
    if len(sys.argv[1:]):
        for directory in sys.argv[1:]:
            locations = locations_tag(directory)
            #print len(locations)
            with open(directory + '.json', 'w') as f:
                f.write(json.dumps(
                    locations,
                    indent=4,
                    separators=(',', ': ')
                    )
                )

if __name__ == "__main__":
    main()
