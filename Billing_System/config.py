import os

# Get the directory where config.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

BILLING_MONTH = 2
BILLING_YEAR = 2026

INPUT_EMPLOYEE_FILE = os.path.join(PROJECT_ROOT, "Data", "Employee.xlsx")
INPUT_CHARGES_FILE = os.path.join(PROJECT_ROOT, "Data", "Charges.xlsx")

TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "Templates")
ASSETS_FOLDER = os.path.join(PROJECT_ROOT, "Assets")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "Billing_Annexures")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "Bills")
SUMMARY_FILE = "Billing_Master_Summary.xlsx"

CGST_RATE = 0.09
SGST_RATE = 0.09
IGST_RATE = 0.18
