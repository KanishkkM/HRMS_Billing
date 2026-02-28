import pandas as pd
from datetime import date
import calendar
from config import *
from shared.helpers import get_billing_dates_pd
from charge_mapper import ChargeMapperOneTime
from annexure_builder import build_annexure_row


def get_billing_dates(cycle, month, year):
    """
    Get billing start and end dates based on billing cycle.
    Returns pandas Timestamps for comparison with datetime64 columns.
    cycle: string like "21-20", "25-24", "26-25" or empty for default month
    """
    return get_billing_dates_pd(cycle, month, year)


def process_onetime_billing(df, billing_month, billing_year):
    """
    Process One_Time billing for new joiners in the given month
    
    Key differences from recurring billing:
    - Filter by Date of Joining in the billing month
    - No attendance calculation
    - Fixed charges from Charges_OneTime file
    - Include Reporting Person and Date of Joining in output
    """
    
    charge_mapper = ChargeMapperOneTime(INPUT_CHARGES_FILE)
    
    # Ensure Date of Joining is in datetime format
    if "Date of Joining" in df.columns:
        df = df.copy()
        df["Date of Joining"] = pd.to_datetime(
            df["Date of Joining"],
            errors="coerce",
            dayfirst=True
        )
    
    annex_rows = []
    error_rows = []
    
    # Get billing cycle from employee data, default to empty if not present
    if "Billing Cycle" not in df.columns:
        df["Billing Cycle"] = ""
    
    # For each unique billing cycle, get the date range and filter employees who joined within that period
    new_joiners_list = []
    
    # Get unique billing cycles from employees
    unique_cycles = df["Billing Cycle"].fillna("").unique()
    
    for cycle in unique_cycles:
        cycle_str = str(cycle)
        start_date, end_date = get_billing_dates(cycle_str, billing_month, billing_year)
        
        # Filter employees who joined within this billing period
        cycle_new_joiners = df[
            (df["Billing Cycle"].fillna("").astype(str) == cycle_str) &
            (df["Date of Joining"] >= start_date) &
            (df["Date of Joining"] <= end_date)
        ]
        
        if not cycle_new_joiners.empty:
            new_joiners_list.append(cycle_new_joiners)
            print(f"Found {len(cycle_new_joiners)} new joiners for cycle {cycle_str} ({start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')})")
    
    # Combine all new joiners from different cycles
    if new_joiners_list:
        new_joiners = pd.concat(new_joiners_list, ignore_index=True)
    else:
        new_joiners = pd.DataFrame()
    
    print(f"Total new joiners found: {len(new_joiners)}")
    
    for _, row in new_joiners.iterrows():
        try:
            # Get charge details from mapper
            base_charge, application_mode = charge_mapper.get_charge_details(
                row["Kind Attention Person"],
                row.get("Position"),
                row["Billing"]
            )
            
            # Skip if no charge is defined for this employee
            if base_charge <= 0:
                print(f"Skipping {row.get('Employee Name', 'Unknown')}: No charge defined")
                continue
            
            # For One_Time, charges are typically fixed
            final_charge = base_charge
            
            # Calculate total (Only Charges - no Billing, Out of Pocket, or Arrears)
            total = final_charge
            
            # Calculate GST
            gst = str(row.get("GST", "")).upper() if pd.notna(row.get("GST")) else "CGST/SGST"
            
            if "IGST" in gst:
                igst = total * IGST_RATE
                cgst = sgst = 0
            else:
                cgst = total * CGST_RATE
                sgst = total * SGST_RATE
                igst = 0
            
            grand_total = total + cgst + sgst + igst
            
            # Build GST values tuple
            gst_values = (cgst, sgst, igst, grand_total)
            
            # Build annexure row
            annex_rows.append(build_annexure_row(row, final_charge, gst_values))
            
        except Exception as e:
            error_row = row.copy()
            error_row["System Error Reason"] = str(e)
            error_rows.append(error_row)
    
    return pd.DataFrame(annex_rows), pd.DataFrame(error_rows)
