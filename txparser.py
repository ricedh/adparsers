#!/usr/bin/python

import csv

def parselink(permalink):
	"""
	Our ads have been collected with Portal of Texas History
	permalinks, which take this form:

	http://texashistory.unt.edu/ark:/67531/metapth47968/m1/4/zoom/?zoom=5&lat=3290self.5&lon=1499&layers=BT
	"""

def get_transcriptions_from_csv(fileobj):

	""" Take a file object (an opened CSV downloaded from
	Google Docs), return list of dictionaries. Each dictionary represents
	a transcribed ad and contains values for the YYYY, MM, DD, transcription,
	and the permalink for the ad.  """
	reader = csv.DictReader(fileobj)
	fields = {'YYYY','MM','DD','PERMALINK','TRANSCRIPTION'}
	transcribed= []
	for row in reader:
		cleaned_row = {k: row[k] for k in row.viewkeys() & fields if row[k]}
		if 'TRANSCRIPTION' in cleaned_row: transcribed.append(cleaned_row)
	return transcribed

f = open('/Users/wcm1/Inbox/telegraph-1838.csv', 'rb')
transcribed_ads = get_transcriptions_from_csv(f)

