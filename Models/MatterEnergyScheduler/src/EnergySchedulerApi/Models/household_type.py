from enum import Enum

class HouseholdType(Enum):
    GRID_ONLY = "grid_only"
    GRID_AND_PV = "grid_and_pv"
    GRID_PV_AND_BESS = "grid_pv_and_bess"