from typing import Dict, List
from datetime import datetime, date
import json
from pathlib import Path
from ..Models.scheduled_appliance import ScheduledAppliance


class ScheduleRegistry:
    """Manages persistently stored scheduled appliances with re-optimization capabilities"""

    def __init__(self, storage_path: str = "data/schedules.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.schedules: Dict[str, ScheduledAppliance] = {}
        self._load_from_disk()

    def _load_from_disk(self):
        """Load schedules from JSON file"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for schedule_data in data.values():
                        # Convert datetime strings back to datetime objects
                        if 'start_time' in schedule_data and schedule_data['start_time']:
                            schedule_data['start_time'] = datetime.fromisoformat(schedule_data['start_time'])
                        schedule = ScheduledAppliance(**schedule_data)
                        self.schedules[schedule.appliance_id] = schedule
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load schedules from {self.storage_path}: {e}")
                # Start with empty registry if file is corrupted

    def _save_to_disk(self):
        """Save schedules to JSON file"""
        data = {}
        for appliance_id, schedule in self.schedules.items():
            schedule_dict = schedule.dict()
            # Convert datetime to ISO string for JSON serialization
            if schedule_dict.get('start_time'):
                schedule_dict['start_time'] = schedule_dict['start_time'].isoformat()
            data[appliance_id] = schedule_dict

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def store_schedule(self, schedule: ScheduledAppliance) -> ScheduledAppliance:
        """Store a scheduled appliance"""
        self.schedules[schedule.appliance_id] = schedule
        self._save_to_disk()
        return schedule

    def get_schedule(self, appliance_id: str) -> ScheduledAppliance:
        """Get a scheduled appliance by ID"""
        if appliance_id not in self.schedules:
            raise KeyError(f"Schedule for appliance '{appliance_id}' not found")
        return self.schedules[appliance_id]

    def list_schedules(self) -> List[ScheduledAppliance]:
        """List all scheduled appliances"""
        return list(self.schedules.values())

    def get_schedules_for_date(self, target_date: date) -> List[ScheduledAppliance]:
        """Get all schedules for a specific date"""
        return [
            schedule for schedule in self.schedules.values()
            if schedule.start_time.date() == target_date
        ]

    def remove_schedule(self, appliance_id: str) -> ScheduledAppliance:
        """Remove a schedule from registry"""
        schedule = self.get_schedule(appliance_id)
        del self.schedules[appliance_id]
        self._save_to_disk()
        return schedule

    def clear_all_schedules(self):
        """Clear all stored schedules"""
        self.schedules.clear()
        self._save_to_disk()
