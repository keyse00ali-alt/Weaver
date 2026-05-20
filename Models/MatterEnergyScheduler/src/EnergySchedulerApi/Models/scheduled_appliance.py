from pydantic import BaseModel
from datetime import datetime


class ScheduledAppliance(BaseModel):
    appliance_id: str
    start_time: datetime
    duration_seconds: int
    power_usage_kw: float
