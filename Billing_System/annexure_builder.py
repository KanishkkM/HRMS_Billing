def build_annexure_row(row, totals, gst_values):

    cgst, sgst, igst, grand_total = gst_values
    
    # Determine which GST type is being used
    has_igst = igst > 0
    
    # Build base row data (without GST columns)
    row_data = {
        "Kind Attention Person": row["Kind Attention Person"],
        "Company Name": row["Company Name"],
        "Employee Code": row["Employee Code"],
        "Employee Name": row["Employee Name"],
        "Billing Cycle": row.get("Billing Cycle"), 
        "Billing": round(row["Billing"], 2),
        "No of days": totals["total_days"],
        "Eligible Days": totals["eligible_days"],
        "No of Saturdays": totals["sat"],
        "No of Sundays": totals["sun"],
        "No of Holidays": row["No of Holidays"],
        "Total Present": row["Total Present"],
        "Total Working Days": round(totals["total_billable_days"], 2),
        "Absents this Month": row["Absents this Month"],
        "Adjustment of Days": row["Adjustment of Days"],
        "Total Payable Days": round(totals["final_billable_days"], 2),
        "Total Payable Billing": round(totals["payable_billing"], 2),
        "Charges": round(totals["charges"], 2),
        "Out of Pocket Exp": round(row["Out of Pocket Exp"], 2),
        "Arrears": round(row["Arrears"], 2),
        "Total": round(totals["total"], 2),
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
