from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
from stathat import StatHat
from fetcher import fetch
import sys


def parsepage(text):
    doc = BeautifulSoup(text, convertEntities="html")
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:-3]
    for c in countries:
        cells = c.findAll('td', text=True)
        while not cells[0].strip():
            cells.pop(0)
        while not cells[-1].strip():
            cells.pop(-1)
        yield cells[0], cells[-1]

def parsedate(d):
    formats = ('%d-%b-%y', '%d-%b-%Y', '%d -%b-%y' )
    for f in formats:
        try:
            return datetime.strptime(d, f)
        except ValueError:
            continue
    return None

def main():
    text, modified = fetch()
    if not modified:
        sys.exit()
        
    stats = StatHat()
    countries = parsepage(text)
    dates = filter(None, (parsedate(d) for (c, d) in countries))
    diff = date.today() - max(dates).date()
    stats.ez_post_value("site-stathat.com@ars.iki.fi", "time since last case", diff.days)
    
if __name__ == '__main__':
    main()
