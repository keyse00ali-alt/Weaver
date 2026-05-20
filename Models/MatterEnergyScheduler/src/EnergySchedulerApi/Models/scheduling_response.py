from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class MatterScheduleConfig(BaseModel):
    matter_device_id: Optional[str] = None
    auto_send_schedule: bool = True


class ScheduleWithMatterResult(BaseModel):
    start_time: datetime
    duration_seconds: int
    matter_device_id: Optional[str] = None
    matter_command_sent: bool = False
    matter_command_result: Optional[dict[str, Any]] = None
    matter_command_error: Optional[str] = None
