from BeautifulSoup import BeautifulSoup
from datetime import datetime, date
import requests

SOURCE = 'http://www.polioeradication.org/Dataandmonitoring/Poliothisweek.aspx'

def parsepage(text):
    doc = BeautifulSoup(text)
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:-3]
    for c in countries:
        cells = c.findAll('td', text=True)
        yield cells[1], cells[-1]

def main():
    r = requests.get(SOURCE)
    countries = parsepage(r.text)
    dates = (datetime.strptime(d, '%d-%b-%y') for (c, d) in countries)
    diff = date.today() - max(dates).date()
    print date.today(), diff.days
    
if __name__ == '__main__':
    main()