# encoding: utf-8
import csv
import sys
from BeautifulSoup import BeautifulSoup
import requests

SOURCE = 'http://www.polioeradication.org/Dataandmonitoring/Poliothisweek.aspx'

def text(element):
    textnodes = element.findAll(text=True)
    return ''.join(textnodes)

def rowify(rows):
    for r in rows:
        cells = (text(c) for c in r.findAll('td'))
        cleaned = (c.strip() for c in cells)
        yield [c.encode('utf-8') for c in cleaned]

def write(doc, w):
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:]
    for row in rowify(countries):
        w.writerow(row)

def write_endemics(doc, w):
    casetable = doc.findAll('table')[0]
    totals = casetable.findAll('tr')[-2:]
    rows = list(rowify(totals))
    rows[0][0] = 'Endemic'
    rows[1][0] = 'Non-endemic'

    for row in rows:
        w.writerow(row)

def main():
    r = requests.get(SOURCE)
    doc = BeautifulSoup(r.text, convertEntities="html")
    w = csv.writer(sys.stdout, delimiter="\t")
    #TODO: Move this out.
    header = ("Country", "Total-cy2d-wpv", "Total-cy2d-cvdpv",
                         "Total-py2d-wpv", "Total-py2d-cvdpv",
                         "Total-pyf-wpv", "Total-pyf-cvdpv",
                        "Date of most recent WPV",
                        "Date of most recent cVDPV")
    w.writerow(header)
    write(doc, w)
    write_endemics(doc, w)
    
if __name__ == "__main__":
    main()