#!/usr/bin/python

import os
import csv
import zipfile
from urlparse import urlparse, parse_qs

def parse_url(permalink):
    """ Take a permalink from the runaway ads spreadsheet, return list of
    newspaper ID, unique metapth ID for issues, and page for recomposition. 
    URLs take the form, http://texashistory.unt.edu/ark:/67531/metapth78134/m1/3/
    zoom/?zoom=6&lat=851.5&lon=996.5
    """
    parsed_url = urlparse(permalink)
    paths = parsed_url.path.split('/')[2:6]
    queries = parse_qs(parsed_url.query)
    lat, lon = queries['lat'], queries['lon']
    urlparts = paths + lat + lon
    return urlparts

def get_transcriptions_from_csv(fileobj):
    """ Take an opened CSV downloaded from Google Docs, return list of
    dictionaries. Each dictionary represents a transcribed ad and contains
    values for the YYYY, MM, DD, transcription, and the permalink for the ad.
    """
    reader = csv.DictReader(fileobj)
    fields = {'YYYY','MM','DD','PERMALINK','TRANSCRIPTION'}
    transcribed= []
    for row in reader:
        cleaned_row = {k: row[k] for k in row.viewkeys() & fields if row[k]}
        if 'TRANSCRIPTION' in cleaned_row: transcribed.append(cleaned_row)
    return transcribed

path = '/Users/wcm1/Inbox/csv'
z = zipfile.ZipFile('/Users/wcm1/Desktop/1836-1840.zip', 'a')

for file in os.listdir(path):
    if file.endswith('.csv'):
        f = open(path + '/' + file, 'rb')
        transcribed_ads = get_transcriptions_from_csv(f)
        for ad in transcribed_ads:
            for key in ad:
                if len(ad[key]) < 2: ad[key] = '0' + ad[key]
            paths = parse_url(ad['PERMALINK'])
            new_file_name = 'TX_' + ad['YYYY'] + ad['MM'] + ad['DD'] + '_Telegraph_' + '-'.join(paths) + '.txt'
            z.writestr(new_file_name, ad['TRANSCRIPTION'])
        f.close()

z.close()

