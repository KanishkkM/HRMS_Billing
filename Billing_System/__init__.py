"""
Billing System Package
======================

A modular Python billing system for processing employee attendance data
and generating invoice annexures and bills.

Main Entry Point:
    python main.py

Modules:
    - billing_engine: Core billing calculation logic
    - charge_mapper: Maps charges from external file
    - excel_writer: Writes Excel output files
    - unified_bill_generator: Generates bills from templates
    - helpers: Date/calendar utilities
    - annexure_builder: Builds annexure row data structures
    - config: Configuration settings
"""

__version__ = "1.0.0"
__author__ = "Billing System Team"

# Package metadata
__all__ = [
    "billing_engine",
    "charge_mapper",
    "excel_writer",
    "unified_bill_generator",
    "helpers",
    "annexure_builder",
    "config"
]