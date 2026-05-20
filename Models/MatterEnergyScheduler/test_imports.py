"""
Quick test to verify all imports and basic functionality
"""
import sys
from datetime import datetime, date, timedelta

# Add src to path for imports
sys.path.insert(0, 'src')

# Test basic imports
try:
    from EnergySchedulerApi.Models import (
        Appliance,
        EnergyPrice,
        Location,
        SolarProduction,
        HouseholdType,
        Household
    )
    print("✓ All models imported successfully")
except Exception as e:
    print(f"✗ Model import failed: {e}")
    sys.exit(1)

# Test service imports
try:
    from EnergySchedulerApi.Services import (
        SchedulingService,
        GridOnlyScheduler,
        GridAndPvScheduler,
        GridPvAndBessScheduler
    )
    print("✓ All scheduling services imported successfully")
except Exception as e:
    print(f"✗ Service import failed: {e}")
    sys.exit(1)

# Test infrastructure imports
try:
    from EnergySchedulerApi.Infrastructure import (
        MockPriceProvider,
        MockGeoService,
        MockSolarForecastService
    )
    print("✓ All mock providers imported successfully")
except Exception as e:
    print(f"✗ Infrastructure import failed: {e}")
    sys.exit(1)

# Test basic scheduling logic
try:
    scheduler = GridOnlyScheduler()
    
    # Create test data
    appliance = Appliance(
        name="Test Appliance",
        power_usage_kw=2.0,
        duration_seconds=3600,
        deadline=datetime.now() + timedelta(days=1),
        matter_device_id="test-001",
        matter_device_ip="127.0.0.1",
        matter_device_port=5540,
    )
    
    today = date.today()
    prices = [
        EnergyPrice(
            start_time=datetime.combine(today, datetime.min.time()) + timedelta(hours=i*0.5),
            price_per_kwh=0.15 + i*0.01
        )
        for i in range(48)
    ]
    
    start_time = scheduler.calculate_optimal_start_time(appliance, prices)
    print(f"✓ Grid-only scheduler works: optimal start time = {start_time}")
except Exception as e:
    print(f"✗ Scheduling test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)