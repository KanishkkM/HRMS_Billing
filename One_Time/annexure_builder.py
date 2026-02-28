import pandas as pd

def build_annexure_row(row, charges, gst_values):
    """
    Build annexure row for One_Time billing
    
    Key differences from recurring:
    - Includes Reporting Person and Date of Joining
    - No attendance fields (No of days, Eligible Days, etc.)
    - Simple charge + tax calculation
    - Only shows applicable GST columns (CGST+SGST OR IGST)
    """
    
    cgst, sgst, igst, grand_total = gst_values
    
    # Determine which GST type is being used
    has_igst = igst > 0
    
    # Format Date of Joining for display
    doj = row.get("Date of Joining", "")
    if doj:
        if hasattr(doj, 'strftime'):
            doj_display = doj.strftime("%d-%m-%Y")
        else:
            doj_display = str(doj)
    else:
        doj_display = ""
    
    # Build base row data (without GST columns)
    row_data = {
        "Kind Attention Person": row["Kind Attention Person"],
        "Working At": row.get("Working At", ""),
        "Company Name": row["Company Name"],
        "Employee Code": row["Employee Code"],
        "Employee Name": row["Employee Name"],
        "Reporting Person": row.get("Reporting Person", ""),
        "Date of Joining": doj_display,
        "Biiling": row.get("Billing", ""),
        "Charges": round(charges, 2),
        "Total": round(charges, 2),
        "Grand Total": round(grand_total, 2),
        "Remark": row.get("Remark", "")
    }
    
    # Add only the applicable GST columns
    if has_igst:
        row_data["IGST @18%"] = round(igst, 2)
    else:
        row_data["CGST @9%"] = round(cgst, 2)
        row_data["SGST @9%"] = round(sgst, 2)
    
    return row_data
