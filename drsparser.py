#!/usr/bin/python

import os, re, shutil, sys

#############################################################################
# README: run from terminal in the following manner:
#       UNIX:$ python drsparser.py input_file_name
# This script will create a subfolder called 'out' containing parsed ads.
#############################################################################

monthDict = {"January":"01","February":"02","March":"03","April":"04","May":"05", "June":"06", "July":"07", "August":"08","September":"09","October":"10","November":"11","December":"12"}
dateRegex = re.compile('^(\d{1,2}) (%s) (\d{4})' % '|'.join(monthDict.keys())) # date regex with month in middle
reverseDateRegex = re.compile('\((%s) (\d{1,2}), (\d{4})\)' % '|'.join(monthDict.keys())) # date regex starting with month
newsRegex = re.compile("(.*?)\s*\((.*?)\)"); # newspaper regex

# Extend single-day date strings to appropriate size.
def doubleDate (dateString):
	if len(dateString) == 1:
		return "0" + dateString;
	return dateString;

# Make a folder to store the new files.
if 'out' in os.listdir(os.getcwd()):
	shutil.rmtree(os.getcwd() + '/out/');
os.mkdir('out');
fileNum = 0;

# Split all files and write with generic names.
with open(sys.argv[1], 'r') as f:
	outfile = open('out/' + str(fileNum) + '.txt','w+')
	for line in f:
		mo = dateRegex.search(line); # date search
		if mo:
			outfile.close();
			fileNum += 1;
			outfile = open('out/' + str(fileNum) + '.txt','w+'); # switch outfiles
		outfile.write(line);
	outfile.close();
	os.remove(os.getcwd()+'/out/0.txt'); # redundant, empty file

# Rename each file appropriately.
for eachFile in os.listdir(os.getcwd()+'/out/'):
	newFileName = "AR_";
	with open('out/'+eachFile, 'r') as oldFile:
		text = oldFile.readlines();
		top = text[0:2];

		# Get the first date into the new file name.
		mo = dateRegex.search(top[0]);
		if mo:
			dayNum = doubleDate(mo.group(1));
			newFileName += mo.group(3) + monthDict[mo.group(2)] + dayNum + "_";

		# Check if the notes are in the proper form.
		if '[duplicate]' not in top[1]:

			# Find the second date processes.
			mo = newsRegex.search(top[1]);
			if mo:
	 			newFileName = newFileName + mo.group(1).replace(" ", "-") + "_";
	 			otherMo = reverseDateRegex.search(top[1]);
 				if otherMo:
					newFileName = newFileName + otherMo.group(3);
					dayNum = doubleDate(otherMo.group(2));
					newFileName += monthDict[otherMo.group(1)] + dayNum;
		else:
			newFileName += "UNPROCESSED";


	# Rename the files, and rewrite without the first two lines. 
	os.remove(os.getcwd() + '/out/' + eachFile); 
	with open(os.getcwd() + '/out/' + newFileName + '.txt', 'w') as newFile:
		newFile.writelines(text[2:]);

