#!/usr/bin/python

import sys
import csv
import zipfile

# Script requires three arguments at the command line.  The first should be
# a tab-delimited file produced by Mallet with --output-doc-topics.  The second
# and third arguments, separated by spaces, should be the numbers of the topics
# you want to use to divide the documents into two groups. The script outputs
# two new tab-delimited files: one containing documents more associated with
# the first topic than the second, and the other containing documents more
# associated with the second than the first.

f = open(sys.argv[1], 'rbU')
reader = csv.reader(f, delimiter='\t')

out = open('docs' + sys.argv[2] + 'gt' + sys.argv[3] + '.txt', 'wb')
put = open('docs' + sys.argv[3] + 'gt' + sys.argv[2] + '.txt', 'wb')
outz = zipfile.ZipFile('docs' + sys.argv[2] + 'gt' + sys.argv[3] + '.zip', 'a')
putz = zipfile.ZipFile('docs' + sys.argv[3] + 'gt' + sys.argv[2] + '.zip', 'a')

outwriter = csv.writer(out, delimiter='\t')
putwriter = csv.writer(put, delimiter='\t')

for row in reader:
    row = row[1:]
    filename = row[0].lstrip('file:')
    arcname = filename[filename.rfind('/') + 1:]
    if row.index(sys.argv[2]) < row.index(sys.argv[3]):
       outwriter.writerow(row)
       outz.write(filename, arcname)
    elif row.index(sys.argv[3]) < row.index(sys.argv[2]):
       putwriter.writerow(row)
       putz.write(filename, arcname)
    else:
       pass

