from BeautifulSoup import BeautifulSoup
import requests

SOURCE = 'http://www.polioeradication.org/Dataandmonitoring/Poliothisweek.aspx'

def main():
    r = requests.get(SOURCE)
    doc = BeautifulSoup(r.text)
    casetable = doc.findAll('table')[1]
    countries = casetable.findAll('tr')[2:-3]
    for c in countries:
        cells = c.findAll('td', text=True)
        country_name = cells[1]
        last_case = cells[-1]
        print country_name, last_case
    
if __name__ == '__main__':
    main()