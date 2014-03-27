#!/usr/bin/python
import os, re

dateRegex = re.compile('^(\d{1,2}) (\w+) (\d{4})'); # date regex with month in middle
reverseDateRegex = re.compile('(\w+) (\d{1,2}) (\d{4})') # date regex starting with month
newsRegex = re.compile("(.*?)\s*\((.*?)\)"); # newspaper regex
monthDict = {"January":"01","February":"02","March":"03","April":"04","May":"05", "June":"06", "July":"07",
	"August":"08","September":"09","October":"10","November":"11","December":"12"}

# Make a folder to store the new files.
if 'out' not in os.listdir(os.getcwd()):
	os.mkdir('out');
fileNum = 0;

# Split all files and write with generic names.
with open('arkansas-test.txt', 'r') as f:
	outfile = open('out/' + str(fileNum) + '.txt','w+')
	for line in f:
		mo = dateRegex.search(line) # date search
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
		top = [oldFile.next() for x in xrange(2)]

		# Get the first date into the new file name.
		mo = dateRegex.search(top[0])
		if mo:
			if len(mo.group(1)) == 1:
				dayNum = "0" + mo.group(1)
			else:
				dayNum = mo.group(1)
			newFileName += mo.group(3) + monthDict[mo.group(2)] + dayNum + "_"

		# Check if the notes are in the proper form.
		if '[duplicate]' in top[1]:
			newFileName += "UNPROCESSED"
			continue;

		# Find the second date processes.
		mo = newsRegex.search(top[1])
		if mo:
	 		newFileName = newFileName + mo.group(1).replace(" ", "-")
	 		otherMo = reverseDateRegex.search(line)
 			if otherMo:
				newFileName = newFileName + otherMo.group(3);
				if len(mo.group(2)) == 1:
					dayNum = "0" + otherMo.group(2)
				else:
					dayNum = otherMo.group(2)
				newFileName += monthDict[otherMo.group(1)] + dayNum;
	os.rename(os.getcwd() + '/out/' + eachFile, os.getcwd() + '/out/' + newFileName + '.txt');

