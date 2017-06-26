URL=https://extranet.who.int/maps/rest/services/POLIOWEBSITE/Poliowebsite_layers/MapServer/0/query?where=1%3D1&outFields=Admin0%2C+IndicatorCode%2C+PeriodStartDate%2C+PeriodEndDate&returnGeometry=false&f=json

all: cases.tsv days-since.tsv country-history.tsv

cases.tsv: latest-week.tsv
	python parse.py cases < $< >> $@

days-since.tsv: latest-week.tsv
	python parse.py days < $< >> $@

country-history.tsv: latest-week.tsv
	python parse.py countries < $< >> $@

latest-week.tsv: FORCE
	curl -s "$URL" | ../src/helb/jq --argjson current_year 2017 -rf scrub.jq > $@.temp
	cmp -s $@ $@.temp && rm $@.temp || mv $@.temp $@

FORCE:

.PHONY: all