from pydantic import BaseModel
from datetime import datetime

class SolarProduction(BaseModel):
    time: datetime
    kw_produced: float