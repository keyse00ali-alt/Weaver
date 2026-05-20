from datetime import date
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from EnergySchedulerApi.Infrastructure.bidding_zones import BIDDING_ZONES
from EnergySchedulerApi.Infrastructure.entso_price_provider import EntsoePriceProvider


def test_all_configured_bidding_zones_have_explicit_fallback_baselines():
    missing = sorted(
        zone
        for zone in set(BIDDING_ZONES.values())
        if zone not in EntsoePriceProvider.FALLBACK_BASELINES_EUR_KWH
    )

    assert missing == []


def test_generated_fallback_prices_are_hourly_and_marked_non_real():
    provider = EntsoePriceProvider("unused")

    prices = provider._generate_fallback_prices(date(2026, 5, 3), "10YFR-RTE------C")

    assert len(prices) == 24
    assert all(price.is_real is False for price in prices)
    assert all(price.start_time.date() == date(2026, 5, 3) for price in prices)
    assert min(price.price_per_kwh for price in prices) < max(price.price_per_kwh for price in prices)
