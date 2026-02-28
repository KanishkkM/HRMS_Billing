import os

# Get the directory where config.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# One_Time Billing Configuration
# ===============================

# Billing Month and Year
BILLING_MONTH = 2
BILLING_YEAR = 2026

# Input Files
INPUT_EMPLOYEE_FILE = os.path.join(PROJECT_ROOT, "Data", "Employee.xlsx")
INPUT_CHARGES_FILE = os.path.join(PROJECT_ROOT, "Data", "Charges_OneTime.xlsx")

# Template and Assets Folders
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "One_Time_Template")
ASSETS_FOLDER = os.path.join(PROJECT_ROOT, "Assets")

# Output Folders
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "One_Time_Annexures")
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "One_Time_Bills")
SUMMARY_FILE = "One_Time_Master_Summary.xlsx"

# Tax Rates
CGST_RATE = 0.09
SGST_RATE = 0.09
IGST_RATE = 0.18
