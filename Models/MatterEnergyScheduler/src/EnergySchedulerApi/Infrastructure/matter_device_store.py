import json
from pathlib import Path
from typing import Dict, List

from ..Models.matter_device import MatterDevice


class MatterDeviceStore:
    """
    MVP persistence for commissioned devices.

    Stored as a JSON file under data/ so the API survives restarts without
    requiring a full DB setup.
    """

    def __init__(self, path: str = "data/commissioned_devices.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> Dict[str, MatterDevice]:
        if not self.path.exists():
            return {}
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            devices = {}
            for item in raw:
                device = MatterDevice(**item)
                devices[device.id] = device
            return devices
        except Exception:
            # If the file is corrupted, treat as empty (MVP) instead of crashing startup.
            return {}

    def save_all(self, devices: Dict[str, MatterDevice]) -> None:
        data: List[dict] = [d.model_dump() for d in devices.values()]
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

