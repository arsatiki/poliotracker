from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
from stathat import StatHat
from fetcher import fetch
import sys
import time

NO_UPLOAD = False
FORCE_FETCH = False

def find_countries(doc):
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:-3]
    for c in countries:
        cells = c.findAll('td', text=True)
        while not cells[0].strip():
            cells.pop(0)
        while not cells[-1].strip():
            cells.pop(-1)
        yield cells[0], cells[-1]

def find_counts(doc):
    def at(cell, x, y):
        return int(cell[x + 4 * y])
    
    cell = [c for c in doc.table(text=True) if c.strip()]

    this_year = (at(cell, 1, 1), at(cell, 1, 2), at(cell, 1, 3))
    last_year = (at(cell, 2, 1), at(cell, 2, 2), at(cell, 2, 3))

    return this_year, last_year

def parsedate(d):
    formats = ('%d-%b-%y', '%d-%b-%Y', '%d -%b-%y' )
    for f in formats:
        try:
            return datetime.strptime(d, f)
        except ValueError:
            continue
    return None

def publish(name, value, last_year=False):
    timestamp = None
    if last_year:
        timestamp = int(time.time()) - 365 * 24 * 60 * 60

    if NO_UPLOAD:
        print name, value, timestamp
        return

    stats = StatHat()
    stats.ez_post_value("site-stathat.com@ars.iki.fi", name, value, timestamp)

def parse_opts():
    global NO_UPLOAD, FORCE_FETCH
    if len(sys.argv) > 1:
        for opt in sys.argv[1:]:
            if opt == '-n':
                NO_UPLOAD = True
            if opt == '-f':
                FORCE_FETCH = True

def main():
    parse_opts()

    text, modified = fetch()
    if not (modified or FORCE_FETCH):
        print "Not modified, skipping"
        sys.exit()
    
    print "Sending results"
    doc = BeautifulSoup(text, convertEntities="html")
    
    countries = find_countries(doc)
    dates = filter(None, (parsedate(d) for (c, d) in countries))
    diff = date.today() - max(dates).date()
    publish("time since last case", diff.days)
    
    this_year, last_year = find_counts(doc)
    publish("cases globally", this_year[0])
    publish("cases in endemic countries", this_year[1])
    publish("cases in non-endemic countries", this_year[2])
    
    publish("cases globally", last_year[0], last_year=True)
    publish("cases in endemic countries", last_year[1], last_year=True)
    publish("cases in non-endemic countries", last_year[2], last_year=True)

    
if __name__ == '__main__':
    main()
