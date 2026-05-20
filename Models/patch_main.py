from pathlib import Path
path = Path(r'c:\Users\keyse\Desktop\Weaver\Models\MatterEnergyScheduler\main.py')
text = path.read_text(encoding='utf-8')
needle = '@app.get("/health")\nasync def health():\n    return {"status": "healthy"}\n'
insert = '@app.post("/schedule/water-heater")\nasync def schedule_water_heater(request: WaterHeaterScheduleRequest):\n    """Schedule a flexible water heater to use cheap electricity and solar."""\n    try:\n        target_date = request.target_date or datetime.now().date()\n        prices = await price_provider.get_day_ahead_prices(target_date)\n        solar = await solar_provider.get_forecast(\n            target_date,\n            request.household\n        )\n\n        bess_min_soc = (\n            request.household.bess_capacity_kwh *\n            request.household.bess_min_soc_percent / 100\n        )\n\n        if request.household.bess_capacity_kwh > 0 and request.current_bess_soc_kwh is None:\n            raise ValueError("current_bess_soc_kwh required for BESS water heater scheduling")\n\n        start_time = water_heater_scheduler.calculate_optimal_start_time(\n            request.water_heater,\n            prices,\n            solar,\n            request.existing_schedules,\n            request.house_limit_kw,\n            request.current_bess_soc_kwh or 0.0,\n            request.household.bess_capacity_kwh,\n            bess_min_soc\n        )\n        return {"start_time": start_time}\n    except ValueError as e:\n        raise HTTPException(status_code=400, detail=str(e))\n\n\n' + needle
if needle not in text:
    raise SystemExit('Needle not found')
text = text.replace(needle, insert, 1)
path.write_text(text, encoding='utf-8')
print('Inserted water heater endpoint')
