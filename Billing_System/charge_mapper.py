import pandas as pd


class ChargeMapper:

    def __init__(self, file_path):

        self.df = pd.read_excel(file_path)
        self.df.columns = self.df.columns.str.strip()

        # ---------------- TEXT NORMALIZATION ----------------
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
            self.df["Charge Type"] = "percent"

        self.df["Charge Type"] = (
            self.df["Charge Type"].fillna("percent").astype(str).str.lower().str.strip()
        )

        # Application Mode → fixed / proportionate
        if "Application Mode" not in self.df.columns:
            self.df["Application Mode"] = "proportionate"

        self.df["Application Mode"] = (
            self.df["Application Mode"]
            .fillna("proportionate")
            .astype(str)
            .str.lower()
            .str.strip()
        )

    # -------------------------------------------------------
    def _parse_charge_value(self, raw):
        if pd.isna(raw):
            return 0
        raw = str(raw).replace("%", "").strip()
        try:
            return float(raw)
        except:
            return 0

    # -------------------------------------------------------
    def get_charge_details(self, kap, position, billing):

        if pd.isna(position):
            position = ""

        kap = str(kap).lower().strip()
        position = str(position).lower().strip()

        kap_rows = self.df[self.df["Kind Attention Person"] == kap]

        if kap_rows.empty:
            return 0, "proportionate"

        # ---- SINGLE ENTRY FOR KAP ----
        if len(kap_rows) == 1:
            row = kap_rows.iloc[0]

        # ---- MULTIPLE ENTRIES → MATCH POSITION ----
        else:
            match = kap_rows[kap_rows["Position"] == position]

            if match.empty:
                row = kap_rows.iloc[0]  # fallback
            else:
                row = match.iloc[0]

        charge_type = str(row["Charge Type"]).lower()
        charge_value = self._parse_charge_value(row.get("Charge Value", 0))
        application_mode = str(row["Application Mode"]).lower()

        # -------- BASE CHARGE CALCULATION --------
        if "percent" in charge_type:
            base_charge = billing * (charge_value / 100)
        else:
            base_charge = charge_value

        # -------- RETURN --------
        if "fixed" in application_mode:
            return base_charge, "FIXED"
        else:
            return base_charge, "PROPORTIONATE"
