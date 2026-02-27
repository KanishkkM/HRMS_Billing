import os
import pandas as pd
from config import *


# ================= ANNEX SPLIT FILES =================
def write_outputs(annex_df):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    annex_df["Split_Key"] = (
        annex_df["Kind Attention Person"].astype(str).str.replace(" ", "_")
        + "_"
        + annex_df["Company Name"].astype(str).str.replace(" ", "_")
    )

    for key, group in annex_df.groupby("Split_Key"):

        file_path = os.path.join(OUTPUT_DIR, f"{key}.xlsx")

        output_data = group.drop(columns=["Split_Key"])

        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:

            # ---------- WRITE DATA ----------
            output_data.to_excel(writer, sheet_name="Annexure", index=False)

            workbook = writer.book
            worksheet = writer.sheets["Annexure"]

            # ---------- FORMATS ----------
            bold_format = workbook.add_format({'bold': True})
            total_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF99'})
            whole_number_format = workbook.add_format({'num_format': '0'})

            # ---------- APPLY WHOLE NUMBER FORMAT ----------
            numeric_columns = [3,10,13,14,15,16,17,18,19,20,21,22,23]

            for col_idx in numeric_columns:
                col_letter = chr(65 + col_idx)
                worksheet.set_column(f'{col_letter}:{col_letter}', 18, whole_number_format)

            # ---------- TOTAL ROW ----------
            last_row = len(output_data) + 1

            worksheet.write(last_row, 0, "TOTAL", bold_format)

            # First, add formulas for all numeric columns except Grand Total to get their totals
            total_col = None
            cgst_col = None
            sgst_col = None
            igst_col = None
            grand_total_col = None
            
            for col_idx in numeric_columns:
                col_letter = chr(65 + col_idx)
                col_name = output_data.columns[col_idx]
                
                if col_name == "Grand Total":
                    grand_total_col = col_idx
                else:
                    if col_name == "CGST @9%" or col_name == "SGST @9%":
                        formula = f'=CEILING(SUM({col_letter}2:{col_letter}{last_row}), 1)'
                    else:
                        formula = f'=ROUND(SUM({col_letter}2:{col_letter}{last_row}), 0)'
                    worksheet.write_formula(last_row + 1, col_idx, formula, total_format)
                    
                    # Store column positions for Grand Total calculation
                    if col_name == "Total":
                        total_col = col_idx
                    elif col_name == "CGST @9%":
                        cgst_col = col_idx
                    elif col_name == "SGST @9%":
                        sgst_col = col_idx
                    elif col_name == "IGST @18%":
                        igst_col = col_idx
            
            # Now calculate Grand Total as sum of Total + CGST + SGST + IGST
            if grand_total_col is not None:
                grand_total_letter = chr(65 + grand_total_col)
                grand_total_formula_parts = []
                if total_col is not None:
                    grand_total_formula_parts.append(f"{chr(65 + total_col)}{last_row + 1}")
                if cgst_col is not None:
                    grand_total_formula_parts.append(f"{chr(65 + cgst_col)}{last_row + 1}")
                if sgst_col is not None:
                    grand_total_formula_parts.append(f"{chr(65 + sgst_col)}{last_row + 1}")
                if igst_col is not None:
                    grand_total_formula_parts.append(f"{chr(65 + igst_col)}{last_row + 1}")
                
                if grand_total_formula_parts:
                    formula = f'=ROUND(SUM({",".join(grand_total_formula_parts)}), 0)'
                    worksheet.write_formula(last_row + 1, grand_total_col, formula, total_format)


# ================= MASTER SUMMARY =================
def write_summary(annex_df):

    summary_path = os.path.join(OUTPUT_DIR, SUMMARY_FILE)

    with pd.ExcelWriter(summary_path, engine="xlsxwriter") as writer:

        annex_df.to_excel(writer, sheet_name="Master Summary", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Master Summary"]

        bold_format = workbook.add_format({'bold': True})
        total_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF99'})
        whole_number_format = workbook.add_format({'num_format': '0'})

        numeric_columns = [3,10,13,14,15,16,17,18,19,20,21,22,23]

        for col_idx in numeric_columns:
            col_letter = chr(65 + col_idx)
            worksheet.set_column(f'{col_letter}:{col_letter}', 18, whole_number_format)

        last_row = len(annex_df) + 1

        worksheet.write(last_row, 0, "TOTAL", bold_format)

        for col_idx in numeric_columns:
            col_letter = chr(65 + col_idx)
            # Determine column name from DataFrame to check if it's CGST or SGST
            col_name = annex_df.columns[col_idx]
            if col_name == "CGST @9%" or col_name == "SGST @9%":
                formula = f'=CEILING(SUM({col_letter}2:{col_letter}{last_row}), 1)'
            else:
                formula = f'=ROUND(SUM({col_letter}2:{col_letter}{last_row}), 0)'
            worksheet.write_formula(last_row, col_idx, formula, total_format)


# ================= SYSTEM ERROR FILE =================
def write_error_file(error_df):

    if error_df is None or error_df.empty:
        return

    error_path = os.path.join(OUTPUT_FOLDER, "System_Error.xlsx")

    error_df.to_excel(error_path, index=False)