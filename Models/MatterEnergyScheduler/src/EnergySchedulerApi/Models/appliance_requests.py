from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ApplianceRegistrationRequest(BaseModel):
    """Request to register a new appliance"""
    name: str
    power_usage_kw: float
    duration_seconds: int
    matter_device_id: str
    matter_device_ip: str
    matter_device_port: int = 5540
    matter_node_id: Optional[int] = None
    device_type: str = "generic"
    deadline: Optional[datetime] = None  # Optional initial deadline


class ApplianceUpdateRequest(BaseModel):
    """Request to update an appliance"""
    name: Optional[str] = None
    power_usage_kw: Optional[float] = None
    duration_seconds: Optional[int] = None
    matter_device_id: Optional[str] = None
    matter_device_ip: Optional[str] = None
    matter_device_port: Optional[int] = None
    matter_node_id: Optional[int] = None
    device_type: Optional[str] = None


class SetDeadlineRequest(BaseModel):
    """Request to set a deadline for an appliance"""
    deadline: datetime
