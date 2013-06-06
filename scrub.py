from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
import requests

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
    try:
        return datetime.strptime(d, '%d-%b-%y')
    except ValueError:
        return datetime.strptime(d, '%d-%b-%Y')

def main():
    r = requests.get(SOURCE)
    countries = parsepage(r.text)
    dates = (parsedate(d) for (c, d) in countries)
    diff = date.today() - max(dates).date()
    print date.today(), diff.days
    
if __name__ == '__main__':
    main()