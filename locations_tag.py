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
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as f:
                text = f.read()
                entities = tagger.get_entities(text)
                if 'LOCATION' in entities:
                    locations[filename] = entities['LOCATION']
    return locations

if __name__ == "__main__":
    """
    Create a json file storing locations dictionary for each
        directory argument of the script
    """
    if len(sys.argv[1:]):
        for directory in sys.argv[1:]:
            locations = locations_tag(directory)
            with open(directory + '.json', 'w') as f:
                f.write(json.dumps(locations))