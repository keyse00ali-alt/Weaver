from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4


class WaterHeater(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    matter_device_id: str
    matter_device_ip: str
    matter_device_port: int = 5540
    power_usage_kw: float
    duration_seconds: int
    deadline: datetime
    current_temperature_c: float
    min_temperature_c: float = 45.0
    max_temperature_c: float = 75.0
    target_temperature_c: float | None = None

    @property
    def duration_hours(self) -> float:
        return self.duration_seconds / 3600

    @property
    def desired_temperature_c(self) -> float:
        if self.current_temperature_c < self.min_temperature_c:
            return max(self.min_temperature_c + 5, 50.0)
        return min(self.max_temperature_c, self.target_temperature_c or self.max_temperature_c)
