# encoding: utf-8

# read a TSV, print out same but with ISO timestamps
import csv
import sys
from datetime import datetime

r = csv.reader(sys.stdin, delimiter='\t')
w = csv.writer(sys.stdout, delimiter='\t')

w.writerow(r.next())
for row in r:
    stamp = datetime.fromtimestamp(int(row[0]) + 86400)
    row[0] = str(stamp.date())
    w.writerow(row)