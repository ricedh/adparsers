#!/bin/bash

# Use this script to get a chronological count of ads in a directory.
# The script outputs a tabular count of ads by decade, year, and month.
# Save or move the script to the directory with the ads you want to count.
# Then, to get the counts, execute this from that directory:
#
#	./countads.sh
#
# You can output the printed numbers to a file like this:
#
#	./countads.sh > filename.txt
#
# You can then open that file in Microsoft Excel or a text editor.
# Give the file a descriptive name to remind yourself of which ads where
# in the directory that you were working with.
#
# If the above doesn't work, you may need to execute this command
# from the directory where you have downloaded the script:
#
#	chmod a+x countads.sh
#
# If you get a permissions error, try this, entering password when prompted:
#
#	sudo chmod a+x countads.sh
#

echo -e " \t "

DEC=3

echo -e "DEC\tADS"
while [ $DEC -lt 7 ]; do
	ADS=$(ls | grep -E "_18$DEC[0-9]{5}_" | wc -l | tr -d ' ')
	echo -e "18`echo $DEC`0s\t$ADS"
	let DEC=DEC+1
done

echo -e " \t "

YEAR=1830

echo -e "YEAR\tADS"
while [ $YEAR -lt 1861 ]; do
	ADS=$(ls | grep -E "_$YEAR[0-9]{4}_" | wc -l | tr -d ' ')
	echo -e "$YEAR\t$ADS"
	let YEAR=YEAR+1
done

echo -e " \t "

MONTH=1

echo -e "MONTH\tADS"
while [ $MONTH -lt 13 ]; do
	ADS=$(ls | grep -E "_[0-9]{4}$(printf "%02d" $MONTH)[0-9]{2}_" | wc -l | tr -d ' ')
	echo -e "$MONTH\t$ADS"
	let MONTH=MONTH+1
done
