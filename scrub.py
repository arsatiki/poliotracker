from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
from fetcher import fetch
import sys
import time

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

def publish(endemic, non_endemic, days_since_last=None, last_year=False):
    timestamp = int(time.time())
    if last_year:
        timestamp -= 365 * 24 * 60 * 60

    if days_since_last is not None:
        print "%d\t%d\t%d\t%d" % (timestamp, endemic, non_endemic, days_since_last)
    else:
        print "%d\t%d\t%d\tNaN" % (timestamp, endemic, non_endemic)

def parse_opts():
    global NO_UPLOAD, FORCE_FETCH
    if len(sys.argv) > 1:
        for opt in sys.argv[1:]:
            if opt == '-f':
                FORCE_FETCH = True

def main():
    parse_opts()

    text, modified = fetch()
    if not (modified or FORCE_FETCH):
        print "Not modified, skipping"
        sys.exit()
    
    doc = BeautifulSoup(text, convertEntities="html")
    
    countries = find_countries(doc)
    dates = filter(None, (parsedate(d) for (c, d) in countries))
    diff = date.today() - max(dates).date()
    
    this_year, last_year = find_counts(doc)
    publish(this_year[1], this_year[2], days_since_last=diff.days)
    publish(last_year[1], last_year[2], last_year=True)
    
if __name__ == '__main__':
    main()
