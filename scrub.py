from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
import requests
from stathat import StatHat

SOURCE = 'http://www.polioeradication.org/Dataandmonitoring/Poliothisweek.aspx'

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
    stats = StatHat()
    r = requests.get(SOURCE)
    countries = parsepage(r.text)
    dates = filter(None, (parsedate(d) for (c, d) in countries))
    diff = date.today() - max(dates).date()
    stats.ez_post_value("site-stathat.com@ars.iki.fi", "days since last case", diff.days)
    print date.today(), diff.days
    
if __name__ == '__main__':
    main()