def build_annexure_row(row, totals, gst_values):

    cgst, sgst, igst, grand_total = gst_values

    return {
        "Kind Attention Person": row["Kind Attention Person"],
        "Working At": row.get("Working At", ""),
        "Company Name": row["Company Name"],
        "Employee Code": row["Employee Code"],
        "Employee Name": row["Employee Name"],
        "Billing Cycle": row.get("Billing Cycle"),  # Keep for bill template, removed from annexure output
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
        "CGST @9%": round(cgst, 2),
        "SGST @9%": round(sgst, 2),
        "IGST @18%": round(igst, 2),
        "Grand Total": round(grand_total, 2),
        "Remark": row.get("Remark", "")
    }
