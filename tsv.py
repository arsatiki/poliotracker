# encoding: utf-8
import csv
import sys
from fetcher import fetch
from BeautifulSoup import BeautifulSoup

def toTSV(doc, w):
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:]
    for country in countries:
        cells = country.findAll('td')
        row = [c.text.encode('utf-8') for c in cells]
        w.writerow(row)

def main():
    page, _ = fetch()
    doc = BeautifulSoup(page, convertEntities="html")
    w = csv.writer(sys.stdout, delimiter="\t")
    header = ("Country", "WPV1-cy2d", "WPV3-cy2d", "W1W3-cy2d", "Total-cy2d",
                         "WPV1-py2d", "WPV3-py2d", "W1W3-py2d", "Total-py2d",
                         "Total-pyf", "Date of most recent")
    w.writerow(header)
    toTSV(doc, w)
    
if __name__ == "__main__":
    main()