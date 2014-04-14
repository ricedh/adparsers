from geopy.geocoders import GoogleV3
import sys
import json
import time
import re

def count_states(ad_locs):
    """Converts a mapping of filenames to locations to a mapping
    of filenames to state names.
    Input:
    locs - dict
    Output:
    states - dict
    """
    ad_states = {}
    geolocator = GoogleV3()
    for ad, locs in ad_locs.items():
        mentions = set([])
        for loc in locs:
            try:
                address, (latitude, longitude) = geolocator.geocode(loc)
            except:
                continue
            state = address_to_state(address)
            if state:
                mentions.add(state)
            if mentions:
                ad_states[ad] = list(mentions)  # Sets not JSON serializable
            time.sleep(0.01)    # Should be under google's rate limit
    return ad_states


def address_to_state(address):
    """Extracts state initials from an address string.

    TODO:
    1. Make work with full state names, since Google API
    doesn't always return state initials.
    2. Do something else with D.C.?
    """
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA',
        'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA',
        'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO',
        'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH',
        'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT',
        'VA', 'WA', 'WV', 'WI', 'WY',
        'DC'
        ]
    words = re.findall(r'\w+', address)     # Strip punctuation
    for word in words:
        if word in states:
            return word
    else:
        return None


def main():
    """
    Create a JSON file storing states dictionary for each
        JSON locations file argument of the script

    TODO:
    Accept input of JSON location files and corresponding state name of
    that newspaper. Run count_states for each, and return a dictionary
    mapping the state name to the total number of references for each
    other state.
    """
    if len(sys.argv[1:]):
        for filename in sys.argv[1:]:
            with open(filename, 'r') as f:
                locs = json.loads(f.read())
            states = count_states(locs)
            with open(filename + '_states' + '.json', 'w') as f:
                f.write(json.dumps(states))

if __name__ == "__main__":
    main()