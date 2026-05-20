using EnergyScheduler.Api.Models;

namespace EnergyScheduler.Api.Interfaces;

public interface ISolarForecastService
{
    Task<List<SolarProduction>> GetForecastAsync(DateTime date, Location location);
}