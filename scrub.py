# encoding: utf-8
import csv
import sys
from BeautifulSoup import BeautifulSoup
import requests

SOURCE = 'http://www.polioeradication.org/Dataandmonitoring/Poliothisweek.aspx'

def text(element):
    textnodes = element.findAll(text=True)
    return ''.join(textnodes)

def write(doc, w):
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:]
    for country in countries:
        cells = (text(c) for c in country.findAll('td'))
        cleaned = (c.strip() for c in cells)
        row = [c.encode('utf-8') for c in cleaned]
        w.writerow(row)

def main():
    r = requests.get(SOURCE)
    doc = BeautifulSoup(r.text, convertEntities="html")
    w = csv.writer(sys.stdout, delimiter="\t")
    #TODO: Move this out.
    header = ("Country", "WPV1-cy2d", "WPV3-cy2d", "Total-cy2d",
                         "WPV1-py2d", "WPV3-py2d", "Total-py2d",
                         "Total-pyf", "Date of most recent")
    w.writerow(header)
    write(doc, w)
    
if __name__ == "__main__":
    main()