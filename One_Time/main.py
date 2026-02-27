import pandas as pd
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from billing_engine import process_onetime_billing
from unified_bill_generator import generate_unified_bills


def main():
    print("=" * 60)
    print("ONE_TIME BILLING SYSTEM")
    print("For New Joiners in Billing Month")
    print("=" * 60)
    
    # Read employee data
    df = pd.read_excel(INPUT_EMPLOYEE_FILE)
    df.columns = df.columns.str.strip()
    
    # Parse Date of Joining as datetime (keep as datetime for filtering)
    if "Date of Joining" in df.columns:
        df["Date of Joining"] = pd.to_datetime(
            df["Date of Joining"],
            errors="coerce",
            dayfirst=True
        )
    
    # Note: LDW is not needed for One_Time billing (new joiners only)
    
    # Fill missing numeric columns
    numeric_cols = [
        "Billing",
        "Out of Pocket Exp",
        "Arrears"
    ]
    
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    print(f"\nBilling Month: {BILLING_MONTH}/{BILLING_YEAR}")
    
    # Process One_Time billing
    print("\nProcessing new joiners...")
    annex_df, error_df = process_onetime_billing(df, BILLING_MONTH, BILLING_YEAR)
    
    if annex_df.empty:
        print("No valid records found (no charges defined for new joiners)")
        return
    
    print(f"Processed {len(annex_df)} new joiner records")
    
    if not error_df.empty:
        print(f"Found {len(error_df)} error records")
        error_path = os.path.join(OUTPUT_FOLDER, "System_Error.xlsx")
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        error_df.to_excel(error_path, index=False)
        print(f"Error report saved: {error_path}")
    
    # Generate bills
    print("\nGenerating One_Time bills...")
    generate_unified_bills(annex_df)
    
    print("\n" + "=" * 60)
    print("ONE_TIME BILLING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nOutput Location: {OUTPUT_FOLDER}/")
    if not error_df.empty:
        print(f"Error Report: {OUTPUT_FOLDER}/System_Error.xlsx")
    print()


if __name__ == "__main__":
    main()
