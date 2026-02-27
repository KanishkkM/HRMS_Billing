import pandas as pd
from config import *
from helpers import clean_numeric
from billing_engine import process_billing
from excel_writer import write_error_file
from unified_bill_generator import generate_unified_bills, create_placeholder_images



def main():
    print("UNIFIED BILLING SYSTEM")
    
    # Create placeholder images if they don't exist
    create_placeholder_images()
    
    df = pd.read_excel(INPUT_EMPLOYEE_FILE)
    df.columns = df.columns.str.strip()

    if "Date of Joining" in df.columns:
        df["Date of Joining"] = pd.to_datetime(
            df["Date of Joining"],
            errors="coerce",
            dayfirst=True
        ).dt.date

    if "LDW" in df.columns:
        df["LDW"] = pd.to_datetime(
            df["LDW"],
            errors="coerce",
            dayfirst=True
        ).dt.date

    numeric_cols = [
        "Billing",
        "No of Holidays",
        "Total Present",
        "Absents this Month",
        "Adjustment of Days",
        "Out of Pocket Exp",
        "Arrears"
    ]

    df = clean_numeric(df, numeric_cols)

    print("\nProcessing billing data...")
    annex_df, error_df = process_billing(df)

    print(f"Processed {len(annex_df)} employee records")
    
    if not error_df.empty:
        print(f"Found {len(error_df)} error records")
        write_error_file(error_df)
        pd.DataFrame(error_df).to_excel(
            f"{OUTPUT_FOLDER}/System_Error.xlsx",
            index=False
        )

    print("\nGenerating unified bills...")
    generate_unified_bills(annex_df)

    print("\n" + "=" * 60)
    print("BILLING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nOutput Location: {OUTPUT_FOLDER}/")
    if not error_df.empty:
        print(f"Error Report: {OUTPUT_FOLDER}/System_Error.xlsx")
    print()


if __name__ == "__main__":
    main()
