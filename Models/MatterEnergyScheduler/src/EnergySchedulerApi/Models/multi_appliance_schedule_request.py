from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .appliance import Appliance
from .water_heater import WaterHeater
from .household import Household


class MultiApplianceScheduleRequest(BaseModel):
    appliances: List[Appliance]
    water_heaters: List[WaterHeater]
    household: Household
    target_date: Optional[date] = None
    current_bess_soc_kwh: Optional[float] = None
    house_limit_kw: float = 11.0