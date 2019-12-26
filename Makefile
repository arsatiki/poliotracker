URL=https://extranet.who.int/maps/rest/services/POLIOWEBSITE/Poliowebsite_layers/MapServer/0/query?where=1%3D1&outFields=Admin0%2C+IndicatorCode%2C+PeriodStartDate%2C+PeriodEndDate&returnGeometry=false&f=json

all: db-update

db-update: scrub.sql data.json
	psql -b -q -f scrub.sql --single-transaction

data.json: FORCE
	curl -s "${URL}" > $@.temp
	cmp -s $@ $@.temp && rm $@.temp || mv $@.temp $@

FORCE:

.PHONY: all db-update
