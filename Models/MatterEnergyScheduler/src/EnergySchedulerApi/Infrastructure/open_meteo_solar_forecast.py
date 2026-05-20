from typing import List
from datetime import datetime, date, timedelta
import httpx
import json
import logging
from pathlib import Path
from ..Models.solar_production import SolarProduction
from ..Models.household import Household
from .provider_errors import ProviderError

logger = logging.getLogger(__name__)


class OpenMeteoSolarForecast:
    """Fetch solar forecast from Open-Meteo API with local caching"""
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    CACHE_DIR = Path("data/solar_cache")
    
    def __init__(self):
        # No API key needed for Open-Meteo
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_file(self, target_date: date, latitude: float, longitude: float) -> Path:
        """Get cache file path for a specific date and location"""
        # Include location in cache key to handle different households
        location_key = f"{latitude:.3f}_{longitude:.3f}"
        return self.CACHE_DIR / f"solar_{target_date.isoformat()}_{location_key}.json"
    
    def _save_forecast_to_cache(
        self,
        target_date: date,
        household: Household,
        productions: List[SolarProduction]
    ) -> None:
        """Save solar forecast to local cache"""
        try:
            cache_file = self._get_cache_file(target_date, household.location_latitude, household.location_longitude)
            data = [
                {
                    "time": p.time.isoformat(),
                    "kw_produced": p.kw_produced
                }
                for p in productions
            ]
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception:
            logger.warning(
                "Failed to write Open-Meteo solar cache for %s (%.3f, %.3f)",
                target_date,
                household.location_latitude,
                household.location_longitude,
                exc_info=True,
            )
    
    def _load_forecast_from_cache(
        self,
        target_date: date,
        household: Household
    ) -> List[SolarProduction]:
        """Load solar forecast from local cache"""
        cache_file = self._get_cache_file(target_date, household.location_latitude, household.location_longitude)
        if not cache_file.exists():
            return []
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
                productions = [
                    SolarProduction(
                        time=datetime.fromisoformat(p["time"]),
                        kw_produced=p["kw_produced"]
                    )
                    for p in data
                ]
                return productions
        except Exception:
            logger.warning(
                "Failed to read Open-Meteo solar cache for %s (%.3f, %.3f)",
                target_date,
                household.location_latitude,
                household.location_longitude,
                exc_info=True,
            )
            return []
    
    def _shift_forecast_to_date(
        self,
        productions: List[SolarProduction],
        target_date: date
    ) -> List[SolarProduction]:
        """Shift cached forecast from previous day to target date"""
        if not productions:
            return []
        
        # Get the date from the first production
        source_date = productions[0].time.date()
        days_diff = (target_date - source_date).days
        
        # Shift all productions by the date difference
        shifted_productions = [
            SolarProduction(
                time=p.time + timedelta(days=days_diff),
                kw_produced=p.kw_produced
            )
            for p in productions
        ]
        return shifted_productions
    
    async def get_forecast(
        self,
        target_date: date,
        household: Household
    ) -> List[SolarProduction]:
        """
        Fetch solar irradiance forecast for a household location with local caching.
        Checks cache first, then API, with fallback to previous day's cached data if API is unavailable.
        
        Args:
            target_date: Date to fetch forecast for
            household: Household with location info
        
        Returns:
            List of SolarProduction objects
        """
        # Check cache first
        cached_productions = self._load_forecast_from_cache(target_date, household)
        if cached_productions:
            return cached_productions
        
        # Open-Meteo provides forecast up to 16 days ahead
        start_date = target_date
        end_date = target_date + timedelta(days=1)  # Get full day
        
        params = {
            "latitude": household.location_latitude,
            "longitude": household.location_longitude,
            "hourly": "direct_normal_irradiance",  # DNI in W/m²
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "timezone": "UTC"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.BASE_URL,
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                
                data = response.json()
                productions = self._parse_open_meteo_response(data, household.pv_capacity_kw)
                
                # Cache successful forecast
                self._save_forecast_to_cache(target_date, household, productions)
                return productions
        except Exception as e:
            # Fallback to previous day's cached data
            previous_date = target_date - timedelta(days=1)
            cached_productions = self._load_forecast_from_cache(previous_date, household)
            
            if cached_productions:
                # Shift previous day's forecast to target date
                fallback_productions = self._shift_forecast_to_date(cached_productions, target_date)
                logger.info(
                    "Using previous day's solar forecast (%s) as fallback for %s",
                    previous_date,
                    target_date,
                )
                return fallback_productions
            else:
                # No cache available either
                raise ProviderError(
                    f"Failed to fetch Open-Meteo forecast and no previous-day cache available: {str(e)}"
                )
    
    def _parse_open_meteo_response(
        self,
        data: dict,
        pv_capacity_kw: float
    ) -> List[SolarProduction]:
        """Parse Open-Meteo response into SolarProduction objects"""
        productions = []
        
        try:
            times = data.get('hourly', {}).get('time', [])
            dni_values = data.get('hourly', {}).get('direct_normal_irradiance', [])
            
            if len(times) != len(dni_values):
                raise ValueError("Mismatched time and DNI data lengths")
            
            for time_str, dni in zip(times, dni_values):
                # Parse time
                period_time = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                
                # DNI is in W/m², convert to kW/m²
                dni_kw_per_m2 = dni / 1000
                
                # Estimate production: DNI * system efficiency * PV capacity
                # Assuming 20% system efficiency (panels + inverter losses)
                # pv_capacity_kw is the installed capacity
                # But DNI is irradiance, so production = DNI * efficiency * area
                # Since pv_capacity_kw = irradiance_at_stc * area * efficiency_stc
                # Roughly, production_kw = (DNI / 1000) * (pv_capacity_kw / 5) * 0.8 or something
                # For simplicity, scale by pv_capacity_kw assuming 5 kW/m² STC irradiance
                system_efficiency = 0.2  # 20% overall efficiency
                estimated_production_kw = dni_kw_per_m2 * system_efficiency * (pv_capacity_kw / 5.0) * 5.0
                
                productions.append(SolarProduction(
                    time=period_time,
                    kw_produced=max(0, estimated_production_kw)
                ))
            
            return sorted(productions, key=lambda p: p.time)
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Failed to parse Open-Meteo response: {str(e)}")
