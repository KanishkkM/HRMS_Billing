import pandas as pd
from shared.charge_mapper_base import ChargeMapperBase


class ChargeMapperOneTime(ChargeMapperBase):
    """
    Charge Mapper for One_Time Billing
    Maps charges based on Kind Attention Person and Position
    
    Extends ChargeMapperBase with One_Time specific defaults:
    - Default charge type: fixed (not percent)
    - Default application mode: fixed (not proportionate)
    """

    def __init__(self, file_path):
        # Override defaults for One_Time billing
        self.DEFAULT_CHARGE_TYPE = "fixed"
        self.DEFAULT_APPLICATION_MODE = "fixed"
        super().__init__(file_path)
