from datetime import datetime, date, timedelta
import csv
from itertools import islice, imap, ifilter
import re
import sys
import time

UNCLEAN = re.compile(r'[^-A-Za-z0-9]')

TODAY = str(date.today())
LAST_YEAR = str(date.today() - timedelta(days=365))

def parsedate(d):
    d = UNCLEAN.sub('', d)
    formats = ('%d-%b-%y', '%d-%b-%Y')
    for f in formats:
        try:
            return datetime.strptime(d, f)
        except ValueError:
            continue
    return None

def days(data, out):
    rows = list(data)
    country_rows = rows[:-3]
    datestrings = (row['Date of most recent'] for row in country_rows)
    dates = ifilter(None, imap(parsedate, datestrings))

    diff = date.today() - max(dates).date()
    out.writerow((TODAY, diff.days))

def cases(data, out):
    row = list(data)
    endemic, outbreak = row[-2], row[-1]
    out.writerow((LAST_YEAR, endemic['Total-py2d'], outbreak['Total-py2d']))
    out.writerow((TODAY, endemic['Total-cy2d'], outbreak['Total-cy2d']))

def countries(data, out):
    rows = list(data)
    for r in rows[:-3]:
        out.writerow((LAST_YEAR, r['Country'], r['Total-py2d']))
        out.writerow((TODAY, r['Country'], r['Total-cy2d']))

PARSER = {
    'days': days,
    'cases': cases,
    'countries': countries
}

def main():
    if len(sys.argv) != 2:
        print >> sys.stdout, "Expected parse command" 
        sys.exit(1)
    
    subcommand = sys.argv[1]
    
    if subcommand not in PARSER:
        print >> sys.stdout, "Incorrect parse command:", subcommand
        sys.exit(1)
    
    data = csv.DictReader(sys.stdin, delimiter='\t')
    out = csv.writer(sys.stdout, delimiter='\t')
    
    PARSER[subcommand](data, out)
    
if __name__ == '__main__':
    main()
