import pandas as pd
from datetime import date, timedelta
import calendar


def clean_numeric(df, cols):
    for col in cols:
        if col not in df:
            df[col] = 0
        df[col] = (
            df[col]
            .replace(["-", "", " "], pd.NA)
            .pipe(pd.to_numeric, errors="coerce")
            .fillna(0.0)
        )
    return df


def get_billing_dates(cycle, month, year):

    text = str(cycle).lower()

    if "21" in text and "20" in text:
        start = date(year if month != 1 else year - 1, month - 1 if month != 1 else 12, 21)
        end = date(year, month, 20)

    elif "25" in text and "24" in text:
        start = date(year if month != 1 else year - 1, month - 1 if month != 1 else 12, 25)
        end = date(year, month, 24)

    elif "26" in text and "25" in text:
        start = date(year if month != 1 else year - 1, month - 1 if month != 1 else 12, 26)
        end = date(year, month, 25)

    else:
        start = date(year, month, 1)
        end = date(year, month, calendar.monthrange(year, month)[1])

    return start, end


def count_weekends(start, end, workweek):

    sat = 0
    sun = 0
    cur = start
    workweek_str = str(workweek).lower()

    while cur <= end:
        if cur.weekday() == 5:
            if "5" in workweek_str or "five" in workweek_str:
                sat += 1
        if cur.weekday() == 6:
            sun += 1
        cur += timedelta(days=1)

    return sat, sun
