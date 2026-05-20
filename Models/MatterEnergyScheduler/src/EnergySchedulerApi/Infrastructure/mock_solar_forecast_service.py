from typing import List
from datetime import datetime, date, timedelta
import math
from ..Models.solar_production import SolarProduction


class MockSolarForecastService:
    async def get_forecast(self, target_date: date, household) -> List[SolarProduction]:
        """Mock solar forecast based on typical Ireland solar pattern"""
        productions = []
        base_time = datetime.combine(target_date, datetime.min.time())
        
        for i in range(48):
            time = base_time + timedelta(hours=i * 0.5)
            hour = time.hour + time.minute / 60
            production = 0
            
            # Simulate solar production curve (6 AM to 6 PM peak)
            if 6 <= hour <= 18:
                production = 3.0 * math.sin(math.pi * (hour - 6) / 12)
            
            productions.append(SolarProduction(time=time, kw_produced=production))
        
        return productions