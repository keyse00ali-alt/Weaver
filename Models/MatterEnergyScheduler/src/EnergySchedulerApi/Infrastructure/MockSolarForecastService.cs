using EnergyScheduler.Api.Models;
using EnergyScheduler.Api.Interfaces;

namespace EnergyScheduler.Api.Infrastructure;

public class MockSolarForecastService : ISolarForecastService
{
    public Task<List<SolarProduction>> GetForecastAsync(DateTime date, Location location)
    {
        var productions = new List<SolarProduction>();
        for (int i = 0; i < 48; i++) // 24 hours * 2
        {
            var time = date.AddHours(i * 0.5);
            double production = 0;
            int hour = time.Hour;
            if (hour >= 6 && hour <= 18)
            {
                // Simple mock: peak at noon
                production = 3.0 * Math.Sin(Math.PI * (hour - 6) / 12);
            }
            productions.Add(new SolarProduction { Time = time, KwProduced = production });
        }
        return Task.FromResult(productions);
    }
}