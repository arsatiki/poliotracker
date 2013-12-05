from datetime import datetime, date, timedelta
import csv
from itertools import islice, imap, ifilter
import re
import sys

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

def parse_days(data, out):
    rows = list(data)
    country_rows = rows[:-3]
    datestrings = (row['Date of most recent'] for row in country_rows)
    dates = ifilter(None, imap(parsedate, datestrings))

    diff = date.today() - max(dates).date()
    out.writerow((TODAY, diff.days))

def parse_cases(data, out):
    row = list(data)
    endemic, outbreak = row[-2], row[-1]
    out.writerow((LAST_YEAR, endemic['Total-py2d'], outbreak['Total-py2d']))
    out.writerow((TODAY, endemic['Total-cy2d'], outbreak['Total-cy2d']))

def parse_countries(data, out):
    rows = list(data)
    for r in rows[:-3]:
        past_total = r['Total-py2d']
        curr_total = r['Total-cy2d']
        if past_total:
            out.writerow((LAST_YEAR, r['Country'], past_total))
        if curr_total:
            out.writerow((TODAY, r['Country'], curr_total))

def main():
    if len(sys.argv) != 2:
        print >> sys.stdout, "Expected parse command" 
        sys.exit(1)
    
    parser = globals().get('parse_%s' % sys.argv[1], None)
    
    if parser is None:
        print >> sys.stdout, "Incorrect parse command:", sys.argv[1]
        sys.exit(1)
    
    data = csv.DictReader(sys.stdin, delimiter='\t')
    out = csv.writer(sys.stdout, delimiter='\t')
    
    parser(data, out)
    
if __name__ == '__main__':
    main()
