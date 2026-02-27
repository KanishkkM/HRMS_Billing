import pandas as pd

def build_annexure_row(row, charges, gst_values):
    """
    Build annexure row for One_Time billing
    
    Key differences from recurring:
    - Includes Reporting Person and Date of Joining
    - No attendance fields (No of days, Eligible Days, etc.)
    - Simple charge + tax calculation
    """
    
    cgst, sgst, igst, grand_total = gst_values
    
    # Format Date of Joining for display
    doj = row.get("Date of Joining", "")
    if doj:
        if hasattr(doj, 'strftime'):
            doj_display = doj.strftime("%d-%m-%Y")
        else:
            doj_display = str(doj)
    else:
        doj_display = ""
    
    return {
        "Kind Attention Person": row["Kind Attention Person"],
        "Working At": row.get("Working At", ""),
        "Company Name": row["Company Name"],
        "Employee Code": row["Employee Code"],
        "Employee Name": row["Employee Name"],
        "Reporting Person": row.get("Reporting Person", ""),
        "Date of Joining": doj_display,
        "Position": row.get("Position", ""),
        "Charges": round(charges, 2),
        "Total": round(charges, 2),
        "CGST @9%": round(cgst, 2),
        "SGST @9%": round(sgst, 2),
        "IGST @18%": round(igst, 2),
        "Grand Total": round(grand_total, 2),
        "Remark": row.get("Remark", "")
    }
