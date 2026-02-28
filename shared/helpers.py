"""
Shared Helper Functions
=======================
Common utilities used by both Billing_System and One_Time
"""

import pandas as pd
from datetime import date, timedelta
import calendar


def clean_numeric(df, cols):
    """Clean numeric columns in a DataFrame"""
    for col in cols:
        if col not in df.columns:
            df[col] = 0
        df[col] = (
            df[col]
            .replace(["-", "", " "], pd.NA)
            .pipe(pd.to_numeric, errors="coerce")
            .fillna(0.0)
        )
    return df


def get_billing_dates(cycle, month, year):
    """
    Get billing start and end dates based on billing cycle.
    
    Args:
        cycle: string like "21-20", "25-24", "26-25" or empty for default month
        month: billing month (1-12)
        year: billing year
    
    Returns:
        tuple: (start_date, end_date) as date objects
    """
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
        # Default: use first to last day of the month
        start = date(year, month, 1)
        end = date(year, month, calendar.monthrange(year, month)[1])

    return start, end


def get_billing_dates_pd(cycle, month, year):
    """
    Get billing start and end dates as pandas Timestamps.
    Use this when comparing with pandas datetime64 columns.
    
    Args:
        cycle: string like "21-20", "25-24", "26-25" or empty for default month
        month: billing month (1-12)
        year: billing year
    
    Returns:
        tuple: (start_date, end_date) as pd.Timestamp objects
    """
    start, end = get_billing_dates(cycle, month, year)
    return pd.Timestamp(start), pd.Timestamp(end)


def count_weekends(start, end, workweek):
    """
    Count Saturdays and Sundays between start and end dates.
    
    Args:
        start: start date (date object)
        end: end date (date object)
        workweek: string describing workweek (e.g., "5.5", "6")
    
    Returns:
        tuple: (saturday_count, sunday_count)
    """
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
