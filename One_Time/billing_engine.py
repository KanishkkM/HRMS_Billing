import pandas as pd
from datetime import date
from config import *
from charge_mapper import ChargeMapperOneTime
from annexure_builder import build_annexure_row


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
    
    # Filter new joiners: employees who joined in the billing month
    new_joiners = df[
        (df["Date of Joining"].dt.month == billing_month) & 
        (df["Date of Joining"].dt.year == billing_year)
    ].copy()
    
    print(f"Found {len(new_joiners)} new joiners for {billing_month}/{billing_year}")
    
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
