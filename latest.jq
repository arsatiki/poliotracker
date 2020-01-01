def events: .features|map(.attributes);
def ms_to_date: (./1000)|strftime("%Y-%m-%d");

def select_case($code):
    map(select(.IndicatorCode == $code));

def max_by_indicator($code): 
    select_case($code)
    | map(.PeriodStartDate)
    | max 
    | if . then ms_to_date else "N/A" end
;

events|max_by_indicator("WPV_CASE")
