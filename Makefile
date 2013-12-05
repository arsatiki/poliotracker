all: cases.tsv days-since.tsv country-history.tsv

cases.tsv: latest-week.tsv
	python parse.py cases < $< >> $@

days-since.tsv: latest-week.tsv
	python parse.py days < $< >> $@

country-history.tsv: latest-week.tsv
	python parse.py countries < $< >> $@

latest-week.tsv: FORCE
	python scrub.py > $@.temp
	cmp -s $@ $@.temp && rm $@.temp || mv $@.temp $@

FORCE:

.PHONY: all