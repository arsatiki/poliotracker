from datetime import datetime, date, timedelta
import csv
from itertools import islice, imap, ifilter
import re
import sys

UNCLEAN = re.compile(r'[^-A-Za-z0-9]')

# TODO: these should be scraped out of the data as well.
TODAY = str(date.today())


def parsedate(d):
    d = UNCLEAN.sub('', d)
    formats = ('%Y-%m-%d', '%d-%b-%y', '%d-%b-%Y')
    for f in formats:
        try:
            return datetime.strptime(d, f)
        except ValueError:
            continue
    return None


def parse_days(data, out):
    datestrings = (row['Date of most recent WPV'] for row in data)
    dates = ifilter(None, imap(parsedate, datestrings))
    diff = date.today() - max(dates).date()
    out.writerow((TODAY, diff.days))


def parse_cases(data, out):
    totals = (r['Total-cy2d-wpv']
              for r in data
              if r['Total-cy2d-wpv'] != 'N/A')
    out.writerow((TODAY, sum(map(int, totals))))


def parse_countries(data, out):
    for r in data:
        curr_total = r['Total-cy2d-wpv']
        if curr_total != "0":
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
