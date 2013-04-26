from BeautifulSoup import BeautifulSoup
from datetime import datetime
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
    d = {}
    for country, date in countries:
        d[country] = datetime.strptime(date, '%d-%b-%y')
    print d
    
if __name__ == '__main__':
    main()