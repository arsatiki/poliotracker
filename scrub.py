from BeautifulSoup import BeautifulSoup
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
    
if __name__ == '__main__':
    main()