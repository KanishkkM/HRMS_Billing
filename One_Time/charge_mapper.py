import pandas as pd


class ChargeMapperOneTime:
    """
    Charge Mapper for One_Time Billing
    Maps charges based on Kind Attention Person and Position
    """

    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.df.columns = self.df.columns.str.strip()

        # Text Normalization
        if "Kind Attention Person" not in self.df.columns:
            self.df["Kind Attention Person"] = ""

        self.df["Kind Attention Person"] = (
            self.df["Kind Attention Person"].astype(str).str.lower().str.strip()
        )

        if "Position" not in self.df.columns:
            self.df["Position"] = ""

        self.df["Position"] = (
            self.df["Position"].fillna("").astype(str).str.lower().str.strip()
        )

        # Charge Type → percent / fixed
        if "Charge Type" not in self.df.columns:
            self.df["Charge Type"] = "fixed"

        self.df["Charge Type"] = (
            self.df["Charge Type"].fillna("fixed").astype(str).str.lower().str.strip()
        )

        # Application Mode → fixed / proportionate
        if "Application Mode" not in self.df.columns:
            self.df["Application Mode"] = "fixed"

        self.df["Application Mode"] = (
            self.df["Application Mode"]
            .fillna("fixed")
            .astype(str)
            .str.lower()
            .str.strip()
        )

    def _parse_charge_value(self, raw):
        if pd.isna(raw):
            return 0
        raw = str(raw).replace("%", "").strip()
        try:
            return float(raw)
        except:
            return 0

    def get_charge_details(self, kap, position, billing):
        """
        Get charge details for a given KAP and position
        Returns: (charge_value, application_mode)
        """
        if pd.isna(position):
            position = ""

        kap = str(kap).lower().strip()
        position = str(position).lower().strip()

        kap_rows = self.df[self.df["Kind Attention Person"] == kap]

        if kap_rows.empty:
            return 0, "fixed"

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

        charge_type = str(row["Charge Type"]).lower()
        charge_value = self._parse_charge_value(row.get("Charge Value", 0))
        application_mode = str(row["Application Mode"]).lower()

        # Base Charge Calculation
        if "percent" in charge_type:
            base_charge = billing * (charge_value / 100)
        else:
            base_charge = charge_value

        # Return
        if "fixed" in application_mode:
            return base_charge, "FIXED"
        else:
            return base_charge, "PROPORTIONATE"
