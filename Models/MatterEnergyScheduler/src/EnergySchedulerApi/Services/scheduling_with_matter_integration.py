from __future__ import annotations

from datetime import date
from typing import List, Optional

from ..Models.appliance import Appliance
from ..Models.scheduled_appliance import ScheduledAppliance
from ..Models.water_heater import WaterHeater
from ..Models.scheduling_response import MatterScheduleConfig, ScheduleWithMatterResult
from ..Infrastructure.mock_price_provider import MockPriceProvider
from ..Infrastructure.mock_solar_forecast_service import MockSolarForecastService
from .matter_controller import MatterController, MatterControllerError
from .scheduling_strategies import (
    GridOnlyScheduler,
    GridAndPvScheduler,
    GridPvAndBessScheduler,
    WaterHeaterScheduler,
    MultiApplianceScheduler,
)


class SchedulingWithMatterIntegration:
    def __init__(
        self,
        matter_controller: MatterController,
        price_provider: Optional[MockPriceProvider] = None,
        solar_provider: Optional[MockSolarForecastService] = None,
    ):
        self.grid_only_scheduler = GridOnlyScheduler()
        self.grid_pv_scheduler = GridAndPvScheduler()
        self.grid_pv_bess_scheduler = GridPvAndBessScheduler()
        self.water_heater_scheduler = WaterHeaterScheduler()
        self.multi_appliance_scheduler = MultiApplianceScheduler()
        self.matter_controller = matter_controller
        self.price_provider = price_provider or MockPriceProvider()
        self.solar_provider = solar_provider or MockSolarForecastService()

    async def schedule_grid_only_with_matter(
        self,
        appliance: Appliance,
        household,
        target_date: Optional[date] = None,
        existing_schedules: Optional[List[ScheduledAppliance]] = None,
        house_limit_kw: float = 11.0,
        matter_config: Optional[MatterScheduleConfig] = None,
    ) -> ScheduleWithMatterResult:
        target_date = target_date or date.today()
        prices = await self.price_provider.get_day_ahead_prices(target_date)
        start_time = self.grid_only_scheduler.calculate_optimal_start_time(
            appliance,
            prices,
            existing_schedules,
            house_limit_kw,
        )
        return await self._build_schedule_result(
            start_time,
            appliance.duration_seconds,
            matter_config,
        )

    async def schedule_grid_pv_with_matter(
        self,
        appliance: Appliance,
        household,
        target_date: Optional[date] = None,
        existing_schedules: Optional[List[ScheduledAppliance]] = None,
        house_limit_kw: float = 11.0,
        matter_config: Optional[MatterScheduleConfig] = None,
    ) -> ScheduleWithMatterResult:
        target_date = target_date or date.today()
        prices = await self.price_provider.get_day_ahead_prices(target_date)
        solar = await self.solar_provider.get_forecast(target_date, household)
        start_time = self.grid_pv_scheduler.calculate_optimal_start_time(
            appliance,
            prices,
            solar,
            existing_schedules,
            house_limit_kw,
        )
        return await self._build_schedule_result(
            start_time,
            appliance.duration_seconds,
            matter_config,
        )

    async def schedule_grid_pv_bess_with_matter(
        self,
        appliance: Appliance,
        household,
        current_bess_soc_kwh: float,
        target_date: Optional[date] = None,
        existing_schedules: Optional[List[ScheduledAppliance]] = None,
        house_limit_kw: float = 11.0,
        matter_config: Optional[MatterScheduleConfig] = None,
    ) -> ScheduleWithMatterResult:
        if current_bess_soc_kwh is None:
            raise ValueError("current_bess_soc_kwh required for BESS scheduling")
        target_date = target_date or date.today()
        prices = await self.price_provider.get_day_ahead_prices(target_date)
        solar = await self.solar_provider.get_forecast(target_date, household)
        bess_min_soc = (
            household.bess_capacity_kwh * household.bess_min_soc_percent / 100
        )
        start_time = self.grid_pv_bess_scheduler.calculate_optimal_start_time(
            appliance,
            prices,
            solar,
            current_bess_soc_kwh,
            household.bess_capacity_kwh,
            bess_min_soc,
            existing_schedules,
            house_limit_kw,
        )
        return await self._build_schedule_result(
            start_time,
            appliance.duration_seconds,
            matter_config,
        )

    async def schedule_water_heater_with_matter(
        self,
        water_heater: WaterHeater,
        household,
        target_date: Optional[date] = None,
        current_bess_soc_kwh: Optional[float] = None,
        existing_schedules: Optional[List[ScheduledAppliance]] = None,
        house_limit_kw: float = 11.0,
        matter_config: Optional[MatterScheduleConfig] = None,
    ) -> ScheduleWithMatterResult:
        target_date = target_date or date.today()
        prices = await self.price_provider.get_day_ahead_prices(target_date)
        solar = await self.solar_provider.get_forecast(target_date, household)
        if household.bess_capacity_kwh > 0 and current_bess_soc_kwh is None:
            raise ValueError("current_bess_soc_kwh required for BESS water heater scheduling")
        bess_min_soc = (
            household.bess_capacity_kwh * household.bess_min_soc_percent / 100
        )
        start_time = self.water_heater_scheduler.calculate_optimal_start_time(
            water_heater,
            prices,
            solar,
            existing_schedules,
            house_limit_kw,
            current_bess_soc_kwh or 0.0,
            household.bess_capacity_kwh,
            bess_min_soc,
        )
        return await self._build_schedule_result(
            start_time,
            water_heater.duration_seconds,
            matter_config,
        )

    async def _build_schedule_result(
        self,
        start_time,
        duration_seconds: int,
        matter_config: Optional[MatterScheduleConfig],
    ) -> ScheduleWithMatterResult:
        result = ScheduleWithMatterResult(
            start_time=start_time,
            duration_seconds=duration_seconds,
            matter_device_id=(matter_config.matter_device_id if matter_config else None),
        )

        if matter_config and matter_config.auto_send_schedule and matter_config.matter_device_id:
            try:
                result.matter_command_result = await self.matter_controller.send_schedule_command(
                    matter_config.matter_device_id,
                    start_time,
                    duration_seconds,
                )
                result.matter_command_sent = True
            except (MatterControllerError, KeyError) as exc:
                result.matter_command_error = str(exc)

        return result
