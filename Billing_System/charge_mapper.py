import sys
import os
# Add parent directory to path for shared module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Extend from shared base class
from shared.charge_mapper_base import ChargeMapperBase


class ChargeMapper(ChargeMapperBase):
    """
    Charge Mapper for Recurring Billing
    Uses percent-based charges by default
    Extends ChargeMapperBase with recurring billing defaults:
    - Default charge type: percent
    - Default application mode: proportionate
    """
    
    def __init__(self, file_path):
        # Override defaults for recurring billing
        self.DEFAULT_CHARGE_TYPE = "percent"
        self.DEFAULT_APPLICATION_MODE = "proportionate"
        super().__init__(file_path)
