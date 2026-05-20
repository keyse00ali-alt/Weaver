from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional

class Appliance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    power_usage_kw: float
    duration_seconds: int  # Duration in seconds for API serialization
    deadline: datetime
    matter_device_id: str
    matter_device_ip: str
    matter_device_port: int = 5540
    matter_node_id: Optional[int] = None
    device_type: str = "generic" # 'dishwasher', 'washer', 'ev_charger', etc.
    power_profile: list[float] = Field(default_factory=list) # List of kW values per 30m interval

    @property
    def duration(self) -> timedelta:
        return timedelta(seconds=self.duration_seconds)
