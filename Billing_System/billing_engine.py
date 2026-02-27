import pandas as pd
from config import *
from helpers import *
from charge_mapper import ChargeMapper
from annexure_builder import build_annexure_row


def process_billing(df):

    charge_mapper = ChargeMapper(INPUT_CHARGES_FILE)

    annex_rows = []
    error_rows = []

    for _, row in df.iterrows():

        start, end = get_billing_dates(row["Billing Cycle"], BILLING_MONTH, BILLING_YEAR)
        
        # ================= DIFFERENTIAL BILLING CHECK =================
        employee_type = str(row.get("Employee Type", "")).strip().lower()
        
        if "diffrential" in employee_type:
            # For differential billing, use full billing amount and calculate GST directly
            total_days = (end - start).days + 1
            payable_billing = row["Billing"]
            final_charge = 0
            total = payable_billing + final_charge + row["Out of Pocket Exp"] + row["Arrears"]
            
            gst = str(row.get("GST", "")).upper()
            if "IGST" in gst:
                igst = total * IGST_RATE
                cgst = sgst = 0
            else:
                cgst = total * CGST_RATE
                sgst = total * SGST_RATE
                igst = 0
            
            grand_total = total + cgst + sgst + igst
            
            # Build totals for annexure
            totals = {
                "total_days": 0,
                "eligible_days": 0,
                "sat": 0,
                "sun": 0,
                "total_billable_days": 0,
                "final_billable_days": 0,
                "payable_billing": payable_billing,
                "charges": final_charge,
                "total": total
            }

            gst_values = (cgst, sgst, igst, grand_total)
            annex_rows.append(build_annexure_row(row, totals, gst_values))
            continue

        # ================= DOJ VALIDATION =================
        effective_start = start
        if pd.notna(row.get("Date of Joining")):

            doj = row["Date of Joining"]

            # DOJ AFTER BILLING CYCLE → FULL EXCLUDE
            if doj > end:
                error_row = row.copy()
                error_row["System Error Reason"] = "DOJ after Billing Cycle"
                error_rows.append(error_row)
                continue

            # DOJ INSIDE BILLING CYCLE → PARTIAL BILLING
            elif doj > start:
                effective_start = doj
                doj_adjusted = True

        # ================= DOL VALIDATION =================
        dol_adjusted = False
        effective_end = end

        if pd.notna(row.get("LDW")):

            dol = row["LDW"]

            # DOL BEFORE BILLING CYCLE → FULL EXCLUDE
            if dol < start:
                error_row = row.copy()
                error_row["System Error Reason"] = "DOL before Billing Cycle"
                error_rows.append(error_row)
                continue

            # DOL INSIDE BILLING CYCLE → PARTIAL BILLING
            elif dol < end:
                effective_end = dol
                dol_adjusted = True

        # ================= TOTAL DAYS CALCULATION (FROM BILLING CYCLE ONLY) =================
        total_days = (end - start).days + 1

        # ================= ELIGIBLE DAYS CALCULATION (FROM DOJ, LDW) =================
        # Eligible Days = days employee is eligible for billing based on DOJ/LDW
        eligible_start = start
        eligible_end = end

        # Adjust for DOJ (New Joiners)
        if pd.notna(row.get("Date of Joining")):
            doj = row["Date of Joining"]
            if doj > start:
                eligible_start = doj

        # Adjust for LDW (Leavers)
        if pd.notna(row.get("LDW")):
            dol = row["LDW"]
            if dol < end:
                eligible_end = dol

        eligible_days = (eligible_end - eligible_start).days + 1

        # ================= ATTENDANCE CALC =================
        sat, sun = count_weekends(effective_start, effective_end, row["Workweek"])

        actual_present = row["Total Present"]

        total_billable_days = actual_present + sat + sun + row["No of Holidays"]
        final_billable_days = total_billable_days + row["Adjustment of Days"]

        payable_billing = (
            (final_billable_days / total_days) * row["Billing"]
            if total_days else 0
        )

        # ================= CHARGE CALC =================
        base_charge, application_mode = charge_mapper.get_charge_details(
            row["Kind Attention Person"],
            row.get("Position"),
            row["Billing"]
        )

        if application_mode.upper() == "FIXED":
            final_charge = base_charge
        else:
            if row["Billing"] > 0:
                final_charge = (payable_billing / row["Billing"]) * base_charge
            else:
                final_charge = 0

        # ================= TOTAL =================
        total = payable_billing + final_charge + row["Out of Pocket Exp"] + row["Arrears"]

        # ================= GST =================
        gst = str(row.get("GST", "")).upper()

        if "IGST" in gst:
            igst = total * IGST_RATE
            cgst = sgst = 0
        else:
            cgst = total * CGST_RATE
            sgst = total * SGST_RATE
            igst = 0

        grand_total = total + cgst + sgst + igst

        # ================= SYSTEM ERROR CHECKS =================
        error_reason = []

        if payable_billing > row["Billing"]:
            error_reason.append("Total Payable Billing greater than Billing")

        if final_billable_days > total_days:
            error_reason.append("Total Payable Days greater than Total Days")

        # Check if Eligible Days match Payable Days (for new joiners and leavers)
        if final_billable_days != eligible_days:
            error_reason.append(f"Eligible Days ({eligible_days}) not matching Payable Days ({final_billable_days})")

        if error_reason:
            error_row = row.copy()
            error_row["System Error Reason"] = " | ".join(error_reason)
            error_rows.append(error_row)

        # ================= ANNEX BUILD =================
        totals = {
            "total_days": total_days,
            "eligible_days": eligible_days,
            "sat": sat,
            "sun": sun,
            "total_billable_days": total_billable_days,
            "final_billable_days": final_billable_days,
            "payable_billing": payable_billing,
            "charges": final_charge,
            "total": total
        }

        gst_values = (cgst, sgst, igst, grand_total)

        annex_rows.append(build_annexure_row(row, totals, gst_values))

    return pd.DataFrame(annex_rows), pd.DataFrame(error_rows)
