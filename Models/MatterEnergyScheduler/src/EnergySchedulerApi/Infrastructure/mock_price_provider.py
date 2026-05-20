from typing import List
from datetime import datetime, date, timedelta
from ..Models.energy_price import EnergyPrice

class MockPriceProvider:
    async def get_day_ahead_prices(self, date: date, bidding_zone: str = "10IEA-TRAN------M") -> List[EnergyPrice]:
        # Generate a semi-deterministic seed based on the bidding zone
        # to ensure different zones have different (but stable) prices.
        zone_hash = sum(ord(c) for c in bidding_zone) % 10
        base_price = 0.15 + (zone_hash * 0.02) # Different base for each zone
        
        prices = []
        base_time = datetime.combine(date, datetime.min.time())
        for i in range(24): # 1-hour intervals
            start_time = base_time + timedelta(hours=i)
            # Create a simple "duck curve" mock: cheaper at night and midday, expensive in evening
            import math
            variation = 0.05 * math.sin((i - 6) * math.pi / 12) # Sine wave variation
            price = max(0.05, base_price + variation)
            prices.append(EnergyPrice(start_time=start_time, price_per_kwh=round(price, 3)))
        return prices