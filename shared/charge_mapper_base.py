"""
Shared Charge Mapper Base Class
================================
Base class for charge mapping used by both Billing_System and One_Time
"""

import pandas as pd


class ChargeMapperBase:
    """
    Base Charge Mapper class with common functionality.
    Extend this class for specific billing types.
    """
    
    # Default values - override in subclasses
    DEFAULT_CHARGE_TYPE = "percent"
    DEFAULT_APPLICATION_MODE = "proportionate"
    
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.df.columns = self.df.columns.str.strip()
        self._normalize_columns()
    
    def _normalize_columns(self):
        """Normalize text columns for matching"""
        
        # Kind Attention Person
        if "Kind Attention Person" not in self.df.columns:
            self.df["Kind Attention Person"] = ""
        
        self.df["Kind Attention Person"] = (
            self.df["Kind Attention Person"]
            .astype(str)
            .str.lower()
            .str.strip()
        )
        
        # Position
        if "Position" not in self.df.columns:
            self.df["Position"] = ""
        
        self.df["Position"] = (
            self.df["Position"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.strip()
        )
        
        # Charge Type
        if "Charge Type" not in self.df.columns:
            self.df["Charge Type"] = self.DEFAULT_CHARGE_TYPE
        
        self.df["Charge Type"] = (
            self.df["Charge Type"]
            .fillna(self.DEFAULT_CHARGE_TYPE)
            .astype(str)
            .str.lower()
            .str.strip()
        )
        
        # Application Mode
        if "Application Mode" not in self.df.columns:
            self.df["Application Mode"] = self.DEFAULT_APPLICATION_MODE
        
        self.df["Application Mode"] = (
            self.df["Application Mode"]
            .fillna(self.DEFAULT_APPLICATION_MODE)
            .astype(str)
            .str.lower()
            .str.strip()
        )
    
    def _parse_charge_value(self, raw):
        """Parse charge value from string/number"""
        if pd.isna(raw):
            return 0
        raw = str(raw).replace("%", "").strip()
        try:
            return float(raw)
        except:
            return 0
    
    def get_charge_details(self, kap, position, billing):
        """
        Get charge details for a given KAP and position.
        Override this method in subclass for custom logic.
        
        Args:
            kap: Kind Attention Person
            position: Position/Role
            billing: Billing amount
            
        Returns:
            tuple: (charge_value, application_mode)
        """
        if pd.isna(position):
            position = ""
        
        kap = str(kap).lower().strip()
        position = str(position).lower().strip()
        
        kap_rows = self.df[self.df["Kind Attention Person"] == kap]
        
        if kap_rows.empty:
            return 0, self.DEFAULT_APPLICATION_MODE
        
        # Single Entry for KAP
        if len(kap_rows) == 1:
            row = kap_rows.iloc[0]
        
        # Multiple Entries → Match Position
        else:
            match = kap_rows[kap_rows["Position"] == position]
            
            if match.empty:
                row = kap_rows.iloc[0]  # fallback
            else:
                row = match.iloc[0]
        
        return self._calculate_charge(row, billing)
    
    def _calculate_charge(self, row, billing):
        """
        Calculate charge from row data.
        Override this method in subclass for custom calculation.
        """
        charge_type = str(row["Charge Type"]).lower()
        charge_value = self._parse_charge_value(row.get("Charge Value", 0))
        application_mode = str(row["Application Mode"]).lower()
        
        # Base Charge Calculation
        if "percent" in charge_type:
            base_charge = billing * (charge_value / 100)
        else:
            base_charge = charge_value
        
        # Return based on application mode
        if "fixed" in application_mode:
            return base_charge, "FIXED"
        else:
            return base_charge, "PROPORTIONATE"
