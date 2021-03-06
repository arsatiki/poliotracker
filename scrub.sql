CREATE TEMPORARY TABLE polio_data_staging (
    data jsonb
);

\copy polio_data_staging FROM 'data.json';

create or replace view polio.latest_event_ts as (
	select country, max(ts) as max_ts
	from polio.events
	group by country
);

with stream as (
	select
		"Admin0" as country,
		date(to_timestamp("PeriodEndDate"/1000) at time zone 'utc')
		as ts
	from 
		polio_data_staging,
		jsonb_array_elements(data->'features') as r,
		jsonb_to_record(r.value->'attributes')
			AS event("Admin0" text, "IndicatorCode" text, "PeriodEndDate" bigint, "PeriodStartDate" bigint)
	where "IndicatorCode" = 'WPV_CASE' 
	order by ts 
)
insert into polio.events
select stream.*
from stream
	join polio.latest_event_ts using (country)
where
	ts > max_ts
;

CREATE OR REPLACE VIEW polio.combined_events AS
    SELECT
        ts,
        initcap(country) AS country,
        events
    FROM
        polio.manual_history_events

    UNION ALL

    SELECT
        ts,
        initcap(country),
        1 AS events
    FROM
        polio.events
;

