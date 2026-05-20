from pydantic import BaseModel, Field
from uuid import uuid4
from typing import Optional


class MatterDevice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    matter_device_id: str
    ip_address: str
    port: int = 5540
    device_type: str
    command_path: str = "/matter/command"
    status_path: str = "/matter/status"

    # Matter protocol credentials (populated after commissioning)
    node_id: Optional[int] = None
    fabric_id: Optional[int] = None
    vendor_id: Optional[int] = None
    product_id: Optional[int] = None
    commissioning_date: Optional[str] = None
    operational_credentials: Optional[dict] = None  # Certificate and key data

    # Commissioning information
    setup_code: Optional[str] = None
    discriminator: Optional[int] = None
    commissioning_passcode: Optional[int] = None

    @property
    def is_commissioned(self) -> bool:
        """Check if device has been properly commissioned with Matter protocol"""
        return (
            self.node_id is not None and
            self.fabric_id is not None and
            self.operational_credentials is not None
        )
