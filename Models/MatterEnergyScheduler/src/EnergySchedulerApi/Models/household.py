from pydantic import BaseModel
from typing import Optional
from .household_type import HouseholdType


class Household(BaseModel):
    id: str
    household_type: HouseholdType
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    pv_capacity_kw: float = 0.0  # Solar panel capacity in kW
    bess_capacity_kwh: float = 0.0  # Battery capacity in kWh
    bess_min_soc_percent: float = 20.0  # Minimum state of charge (20% buffer)
    bess_device_id: Optional[str] = None
    bess_device_ip: Optional[str] = None
    bess_device_port: int = 5540
    bidding_zone: str = "10IEA-TRAN------M"  # Default to Ireland