def events: .features|map(.attributes);
def ms_to_date: (./1000)|strftime("%Y-%m-%d");
def get_year: (.PeriodStartDate/1000)|gmtime|.[0];

def select_case($code):
    map(select(.IndicatorCode == $code));

def count_by_indicator($code; $year):
    select_case($code) 
    | map(select(get_year == $year)) 
    | length
;
def max_by_indicator($code): 
    select_case($code
    )
    | map(.PeriodStartDate)
    | max 
    | if . then ms_to_date else "N/A" end
;

def country_row: [
    .[0].Admin0,    # Country
    count_by_indicator("WPV_CASE"; $current_year),
    count_by_indicator("VDPV_CASE"; $current_year),
    count_by_indicator("WPV_CASE_YTD_PY"; $current_year-1),
    count_by_indicator("cVDPV_CASE_YTD_PY"; $current_year-1),
    max_by_indicator("WPV_CASE"),
    max_by_indicator("VDPV_CASE")
];

[
    ["Country", "Total-cy2d-wpv", "Total-cy2d-cvdpv",
    "Total-py2d-wpv", "Total-py2d-cvdpv",
    "Date of most recent WPV",
    "Date of most recent cVDPV"],
    (.|events|group_by(.Admin0)|.[]|country_row)
] | .[] | @tsv

