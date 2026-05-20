from pydantic import BaseModel
from datetime import datetime

class EnergyPrice(BaseModel):
    start_time: datetime
    price_per_kwh: float
    is_real: bool = True