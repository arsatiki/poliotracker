# encoding: utf-8
import csv
import sys
from BeautifulSoup import BeautifulSoup
from fetcher import fetch

EXIT_UNMODIFIED = 1
FORCE_FETCH = False

def write(doc, w):
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:]
    for country in countries:
        cells = (c.text for c in country.findAll('td'))
        cleaned = (c.strip() for c in cells)
        row = [c.encode('utf-8') for c in cleaned]
        w.writerow(row)

def parse_opts():
    global FORCE_FETCH
    if len(sys.argv) > 1:
        for opt in sys.argv[1:]:
            if opt == '-f':
                FORCE_FETCH = True

def main():
    parse_opts()
    text, modified = fetch()
    if not (modified or FORCE_FETCH):
        print "Not modified, skipping"
        sys.exit(EXIT_UNMODIFIED)
    
    doc = BeautifulSoup(text, convertEntities="html")
    w = csv.writer(sys.stdout, delimiter="\t")
    #TODO: Move this out.
    header = ("Country", "WPV1-cy2d", "WPV3-cy2d", "W1W3-cy2d", "Total-cy2d",
                         "WPV1-py2d", "WPV3-py2d", "W1W3-py2d", "Total-py2d",
                         "Total-pyf", "Date of most recent")
    w.writerow(header)
    write(doc, w)
    
if __name__ == "__main__":
    main()